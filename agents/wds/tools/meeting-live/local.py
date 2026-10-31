#!/usr/bin/env python3
"""
local.py: det som hörs på datorn, utskrivet lokalt med Whisper medan det pågår. Del av WDS
(agents/wds/tools/meeting-live.md). Ljudet lämnar aldrig datorn.

Lyssnar på datorns ljud ut (loopback, det du hör) och mikrofonen (du). Ingen bot går med i mötet,
så det fungerar oavsett vem som bjudit in och på vilken plattform. Med --no-mic bara datorns ljud,
för videor, webbinarier och poddar.

Ljudet klipps vid naturliga pauser, när någon har pratat klart, och skrivs ut direkt. Fördröjningen
blir ungefär yttrandets längd plus en sekund. Ett långt yttrande klipps senast efter --max sekunder.
Raderna hamnar i samma jsonl-format som live.py, så `live.py watch` och `live.py archive` fungerar.

Inspelningen och utskriften går var för sig: ljudet skrivs alltid till fil, och hinner utskriften inte
med hoppar den över det äldsta (refine.py tar det efteråt). En statusrad varje minut visar ljudnivån
per kanal och hur långt efter utskriften ligger.

    python local.py --list-screens                                                       # skärmarna att välja mellan
    python local.py --dir <mapp> [--screen [--monitor 1]] [--them "De andra"] [--me "Mårten Angner"]   # en inspelning, allt i mappen
    python local.py <utfil.jsonl> [--them "De andra"] [--me "Mårten Angner"] [--lang sv | auto]
    python local.py <utfil.jsonl> --no-mic --them "Videon"   # bara datorns ljud

Windows (WASAPI loopback). Kräver: python -m pip install pyaudiowpatch faster-whisper numpy
Svenska använder KB-Whisper (KBLab/kb-whisper-small), som laddas ned första gången.
Först använd i welqora-analysis 2026-10-14, när Fireflies transkriberade ett svenskt möte på engelska.
"""

import argparse
import datetime
import io
import json
import math
import queue
import re
import sys
import threading
import time

import numpy as np

RATE = 16000
THREADS = 3  # kärnor till Whisper: lika snabbt som 4 (2026-10-21), och en kärna blir kvar till ljud, video och mötet
STATUS_FIRST, STATUS_EVERY = 10, 60  # sekunder till första statusraden, och sedan mellan dem


def to16k(rate, x):
    if rate == RATE or len(x) == 0:
        return x.astype(np.float32)
    m = int(len(x) * RATE / rate)
    return np.interp(np.linspace(0, len(x) - 1, m), np.arange(len(x)), x).astype(np.float32)


def cuda_available():
    """Ett NVIDIA-kort som faster-whisper (CTranslate2) kan använda."""
    try:
        import ctranslate2
        return ctranslate2.get_cuda_device_count() > 0
    except Exception:
        return False


def is_speech(seg, no_speech=0.6, logprob=-1.0):
    """Whisper hittar ibland på text i brus och korta ljud. Släpp bara igenom det modellen själv tror är tal.

    Bort: tomma rader och skiljetecken ("."), Whispers interna märken ("<|nospeech|>"), rader utan
    bokstäver ("000"), och det modellen bedömer som troligen inte tal eller som osäkra ord."""
    text = seg.text.strip()
    if not text or "<|" in text or not re.search(r"[^\W\d_]", text):
        return False
    if getattr(seg, "no_speech_prob", 0) > no_speech:
        return False
    return getattr(seg, "avg_logprob", 0) > logprob


class Segmenter:
    """Samlar ljud från en källa och lämnar ifrån sig ett yttrande när talaren pausar.

    feed(x) tar emot nya sampel (16 kHz) och ger tillbaka färdiga yttranden som (starttid, ljud).
    Starttiden räknas i sampel från inspelningens start, så den stämmer med ljudfilen. skip(n) flyttar
    fram tiden när ljudkortet inte levererade något."""

    FRAME = 0.1  # sekunder per analysruta

    def __init__(self, threshold=0.006, pause=0.5, max_len=8.0, min_len=0.6):
        self.threshold, self.pause, self.max_len, self.min_len = threshold, pause, max_len, min_len
        self.buf = np.zeros(0, dtype=np.float32)
        self.speech = False    # har bufferten tal
        self.silence = 0.0     # sekunder tystnad sedan senaste tal
        self.pending = np.zeros(0, dtype=np.float32)
        self.pos = 0           # sampel som har analyserats, från inspelningens start
        self.env_t, self.env = [], []  # ljudnivån per analysruta de senaste minuterna, för ekokontrollen

    def feed(self, x):
        out = []
        self.pending = np.concatenate([self.pending, x])
        step = int(self.FRAME * RATE)
        while len(self.pending) >= step:
            frame, self.pending = self.pending[:step], self.pending[step:]
            self.buf = np.concatenate([self.buf, frame])
            rms = float(np.sqrt(np.mean(frame ** 2)))
            self.env_t.append(self.pos / RATE)
            self.env.append(rms)
            if len(self.env) > 3000:
                del self.env_t[:1000], self.env[:1000]
            self.pos += step
            if rms > self.threshold:
                self.speech, self.silence = True, 0.0
            else:
                self.silence += self.FRAME
            dur = len(self.buf) / RATE
            if self.speech and (self.silence >= self.pause or dur >= self.max_len):
                out += self.flush()
            elif not self.speech and dur > 1.0:
                # Bara tystnad: behåll de sista 0,3 sekunderna, så att början på nästa ord kommer med.
                keep = int(0.3 * RATE)
                self.buf = self.buf[-keep:]
        return out

    def skip(self, n):
        """n sampel tystnad som ljudkortet inte levererade: avslutar ett påbörjat yttrande och flyttar fram tiden."""
        out = self.flush()
        self.pos += len(self.pending) + n
        self.pending = np.zeros(0, dtype=np.float32)
        return out

    def envelope(self, times):
        """Ljudnivån vid de givna tiderna; tystnad där inget ljud kom."""
        if not self.env_t:
            return np.zeros(len(times))
        return np.interp(times, self.env_t, self.env, left=0.0, right=0.0)

    def flush(self):
        out = []
        if self.speech and len(self.buf) / RATE - self.silence >= self.min_len:
            out.append(((self.pos - len(self.buf)) / RATE, self.buf))
        self.buf = np.zeros(0, dtype=np.float32)
        self.speech, self.silence = False, 0.0
        return out


def is_echo(start, x, theirs, limit=0.6):
    """Hörs högtalarna i mikrofonen följer mikrofonens ljudnivå datorns ljud upp och ner. Då är yttrandet eko,
    inte personen. När personen pratar själv är datorns ljud tyst eller går i otakt. Jämför nivåkurvorna
    (100 ms per punkt) för yttrandets tid; theirs är segmenteraren för datorns ljud."""
    step = int(Segmenter.FRAME * RATE)
    k = len(x) // step
    if k < 5:
        return False
    mine = np.sqrt(np.mean(x[:k * step].reshape(k, step) ** 2, axis=1))
    other = theirs.envelope(start + np.arange(k) * Segmenter.FRAME)
    if other.max() < theirs.threshold:
        return False
    a, b = np.log10(mine + 1e-4), np.log10(other + 1e-4)
    if a.std() < 1e-3 or b.std() < 1e-3:
        return False
    return float(np.corrcoef(a, b)[0, 1]) > limit


def merge(jobs, longest=25.0):
    """Yttranden som väntar på utskrift slås ihop per talare, upp till 25 sekunder. Whisper räknar alltid på
    30 sekunder ljud, så en bit på 2 s kostar nästan lika mycket som en på 25 (2,4 mot 4,1 s på Mårtens dator).
    Utan det hann utskriften inte med när mikrofonen gav många korta bitar. jobs: (talare, start, slut, ljud)."""
    groups, latest = [], {}
    for name, start, end, x in jobs:
        g = latest.get(name)
        if g and end - g[1] <= longest:
            g[2] = end
            g[3] += [np.zeros(int(0.2 * RATE), dtype=np.float32), x]
        else:
            g = latest[name] = [name, start, end, [x]]
            groups.append(g)
    return [(name, start, end, np.concatenate(parts)) for name, start, end, parts in sorted(groups, key=lambda g: g[1])]


class Track:
    """En kanal på inspelningens tidslinje: ljudet till fil (om det finns en) och till yttranden.

    Windows levererar inget från högtalarutgången när inget spelas. Tystnaden fylls därför i efter
    klockan, så att ljudfil, utskrift och skärm har samma tid och filen blir lika lång som inspelningen."""

    def __init__(self, segmenter, path=None):
        self.seg, self.pos, self.wav = segmenter, 0, None
        self.sq, self.count = 0.0, 0  # för statusraden
        if path:
            import wave
            self.wav = wave.open(str(path), "wb")
            self.wav.setnchannels(1)
            self.wav.setsampwidth(2)
            self.wav.setframerate(RATE)

    def add(self, x, now):
        out = []
        gap = int(now * RATE) - len(x) - self.pos
        if gap > RATE // 5:  # mer än 0,2 s som saknas: fyll med tystnad
            self._silence(gap)
            out += self.seg.skip(gap)
        if self.wav:
            self.wav.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
        self.pos += len(x)
        self.sq += float(np.sum(x.astype(np.float64) ** 2))
        self.count += len(x)
        return out + self.seg.feed(x)

    def _silence(self, n):
        if self.wav:
            self.wav.writeframes(bytes(2 * n))
        self.pos += n

    def level(self):
        """Ljudnivån sedan förra frågan i dB (0 är fullt, -60 nästan tyst), eller None om inget ljud kom."""
        rms = math.sqrt(self.sq / self.count) if self.count else 0.0
        self.sq, self.count = 0.0, 0
        return max(-90, round(20 * math.log10(rms))) if rms > 0 else None

    def close(self, now):
        out = self.seg.flush()
        rest = int(now * RATE) - self.pos  # tystnad fram till stoppet
        if rest > 0:
            self._silence(rest)
        if self.wav:
            self.wav.close()
        return out


def status_text(row):
    """Statusraden som text, samma som live.py visar."""
    levels = ", ".join(f"{k} {'inget ljud' if v is None else f'{v} dB'}" for k, v in row["levels"].items())
    s = f"Status {int(row['start']) // 60:02d}:{int(row['start']) % 60:02d}: {levels}"
    if row.get("lag") is not None:
        s += f" · text {row['lag']} s efter talet"
    if row.get("skipped"):
        s += f" · {row['skipped']} s hoppades över live (kommer med i den grundliga utskriften)"
    if row.get("echo"):
        s += f" · {row['echo']} s eko från högtalarna i mikrofonen"
    if row.get("dropped"):
        s += " · ljudblock tappade: " + ", ".join(f"{k} {v}" for k, v in row["dropped"].items())
    return s


def frames_loop(folder, write, t0, stop, bbox=None, every=5.0, change=4.0):
    """En bild av skärmen när den har ändrats, kontrollerat var femte sekund. Raden i utskriften pekar på bilden.
    bbox: den valda skärmen (vänster, topp, höger, botten); annars huvudskärmen."""
    from PIL import Image, ImageGrab
    folder.mkdir(exist_ok=True)
    last = None
    while not stop.wait(every):
        try:
            img = ImageGrab.grab(bbox=bbox, all_screens=bool(bbox))
        except Exception:
            continue
        small = np.asarray(img.convert("L").resize((96, 54)), dtype=np.float32)
        if last is None or np.mean(np.abs(small - last)) > change:
            last = small
            now = time.time() - t0
            name = f"{int(now) // 60:02d}-{int(now) % 60:02d}.jpg"
            if img.width > 1600:
                img = img.resize((1600, round(img.height * 1600 / img.width)), Image.LANCZOS)
            img.convert("RGB").save(folder / name, quality=82)
            write({"event": "frame", "start": round(now, 1), "file": str(folder / name)})


def screens():
    """De anslutna skärmarna i Windows ordning: nummer, namn, position och storlek i riktiga bildpunkter, huvudskärm."""
    import ctypes
    from ctypes import wintypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # riktiga bildpunkter, inte skalade
    except Exception:
        pass

    class MonitorInfo(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT), ("rcWork", wintypes.RECT),
                    ("dwFlags", wintypes.DWORD), ("szDevice", wintypes.WCHAR * 32)]

    class DisplayDevice(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("DeviceName", wintypes.WCHAR * 32), ("DeviceString", wintypes.WCHAR * 128),
                    ("StateFlags", wintypes.DWORD), ("DeviceID", wintypes.WCHAR * 128), ("DeviceKey", wintypes.WCHAR * 128)]

    u = ctypes.windll.user32
    found = []
    proc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HMONITOR, wintypes.HDC, ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)

    def each(hmon, hdc, rect, data):
        mi = MonitorInfo()
        mi.cbSize = ctypes.sizeof(mi)
        u.GetMonitorInfoW(hmon, ctypes.byref(mi))
        dd = DisplayDevice()
        dd.cb = ctypes.sizeof(dd)
        name = dd.DeviceString if u.EnumDisplayDevicesW(mi.szDevice, 0, ctypes.byref(dd), 0) else mi.szDevice
        r = mi.rcMonitor
        found.append({"name": name, "device": mi.szDevice, "x": r.left, "y": r.top,
                      "width": r.right - r.left, "height": r.bottom - r.top, "primary": bool(mi.dwFlags & 1)})
        return True

    u.EnumDisplayMonitors(None, None, proc(each), 0)
    return [{"n": i, **s} for i, s in enumerate(found, 1)]


def no_power_throttling():
    """Windows kan strypa en process som körs i bakgrunden (EcoQoS), till exempel när den startats av en agent
    och ett videomöte har förgrunden. Då hinner utskriften inte med. Stäng av strypningen för den här processen."""
    if sys.platform != "win32":
        return
    import ctypes
    from ctypes import wintypes

    class State(ctypes.Structure):
        _fields_ = [("Version", wintypes.ULONG), ("ControlMask", wintypes.ULONG), ("StateMask", wintypes.ULONG)]

    k = ctypes.windll.kernel32
    k.GetCurrentProcess.restype = wintypes.HANDLE
    k.SetProcessInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    s = State(1, 0x1, 0)  # PROCESS_POWER_THROTTLING_EXECUTION_SPEED, av
    k.SetProcessInformation(k.GetCurrentProcess(), 4, ctypes.byref(s), ctypes.sizeof(s))  # ProcessPowerThrottling


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", help="utskriftens jsonl-fil; med --dir blir den <dir>/transcript.jsonl")
    ap.add_argument("--dir", help="inspelningens mapp: utskrift, ljud per kanal, skärmvideo och bilder")
    ap.add_argument("--screen", action="store_true", help="spela in skärmen som video och spara en bild när den ändras")
    ap.add_argument("--monitor", type=int, help="vilken skärm (nummer från --list-screens); utan den alla skärmar")
    ap.add_argument("--region", help="bara en del av skärmen, som andelar av den: vänster,topp,bredd,höjd, till exempel 0,0,0.5,0.5 för övre vänstra fjärdedelen")
    ap.add_argument("--list-screens", action="store_true", help="lista skärmarna och avsluta")
    ap.add_argument("--them", default="De andra")
    ap.add_argument("--me", default="Jag")
    ap.add_argument("--lang", default="sv", help="sv, en … eller auto: språket upptäcks för varje yttrande")
    ap.add_argument("--no-mic", action="store_true", help="bara datorns ljud, till exempel en video eller ett webbinarium")
    ap.add_argument("--mic", help="mikrofon vars namn innehåller texten, till exempel Surface; utan den Windows standardmikrofon")
    ap.add_argument("--pause", type=float, default=0.5, help="sekunder tystnad som avslutar ett yttrande")
    ap.add_argument("--max", type=float, default=8.0, help="längsta yttrande innan det klipps")
    ap.add_argument("--threshold", type=float, default=0.006, help="ljudnivå som räknas som tal")
    ap.add_argument("--max-lag", type=float, default=30.0, help="sekunder efter talet då utskriften hoppar över ett yttrande")
    ap.add_argument("--model", default=None, help="standard: KBLab/kb-whisper-small för svenska, annars small")
    ap.add_argument("--threads", type=int, default=THREADS, help="kärnor till taligenkänningen; resten till ljud, video och mötet")
    a = ap.parse_args()
    if a.list_screens:
        for m in screens():
            print(f"{m['n']}. {m['name']} ({m['device']}): {m['width']}x{m['height']}"
                  f"{' (huvudskärm)' if m['primary'] else ''}, position {m['x']},{m['y']}")
        return
    monitor = None
    if a.monitor:
        a.screen = True
        monitor = next((m for m in screens() if m["n"] == a.monitor), None)
        if not monitor:
            ap.error(f"skärm {a.monitor} finns inte; se --list-screens")
        if a.region:
            # En mindre video: bara den del av skärmen som visar det samtalet handlar om. Jämna mått för x264.
            fx, fy, fw, fh = (float(v) for v in a.region.split(","))
            w, h = monitor["width"], monitor["height"]
            monitor = dict(monitor, x=monitor["x"] + round(fx * w), y=monitor["y"] + round(fy * h),
                           width=round(fw * w) // 2 * 2, height=round(fh * h) // 2 * 2)
    from pathlib import Path
    folder = Path(a.dir) if a.dir else None
    if folder:
        folder.mkdir(parents=True, exist_ok=True)
        a.out = str(folder / "transcript.jsonl")
    if not a.out:
        ap.error("ange en utfil eller --dir")

    try:
        import pyaudiowpatch as pyaudio
        from faster_whisper import WhisperModel
    except ImportError:
        print("Paket saknas: python -m pip install pyaudiowpatch faster-whisper numpy")
        sys.exit(1)

    no_power_throttling()
    # Modellen laddas före inspelningen. Ljud som kom under laddningen hamnade förut före klockans start,
    # och tiderna i början blev negativa.
    model_name = a.model or ("KBLab/kb-whisper-small" if a.lang == "sv" else "small")
    print(f"Laddar taligenkänningen ({model_name}) …")
    if cuda_available():  # NVIDIA-kort: faster-whisper på CUDA
        model = WhisperModel(model_name, device="cuda", compute_type="float16")
        print("Taligenkänning på NVIDIA-kortet (CUDA)")
    else:
        model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=a.threads)

    pa = pyaudio.PyAudio()
    sources = [(a.them, "them", pa.get_default_wasapi_loopback())]
    if not a.no_mic:
        mic = pa.get_default_input_device_info()
        if a.mic:
            wasapi = pa.get_host_api_info_by_type(pyaudio.paWASAPI)["index"]
            mic = next((d for d in (pa.get_device_info_by_index(i) for i in range(pa.get_device_count()))
                        if d["hostApi"] == wasapi and d["maxInputChannels"] > 0 and not d.get("isLoopbackDevice")
                        and a.mic.lower() in d["name"].lower()), None)
            if not mic:
                ap.error(f"ingen mikrofon heter något med {a.mic!r}")
        sources.append((a.me, "me", mic))
    incoming = {name: [] for name, _, _ in sources}
    dropped = {name: 0 for name, _, _ in sources}  # block som ljudkortet tappade för att vi inte hann hämta dem
    tracks = {name: Track(Segmenter(a.threshold, a.pause, a.max), folder / f"{role}.wav" if folder else None)
              for name, role, _ in sources}
    lock = threading.Lock()
    streams = []
    t0 = time.time()
    for name, _, dev in sources:
        rate, ch = int(dev["defaultSampleRate"]), max(1, min(2, dev["maxInputChannels"]))

        def cb(data, frames, info, status, name=name, ch=ch, rate=rate):
            if status & pyaudio.paInputOverflow:
                dropped[name] += 1
            x = np.frombuffer(data, dtype=np.int16).reshape(-1, ch).mean(axis=1) / 32768.0
            with lock:
                incoming[name].append(to16k(rate, x))
            return (None, pyaudio.paContinue)

        streams.append(pa.open(format=pyaudio.paInt16, channels=ch, rate=rate, input=True,
                               input_device_index=dev["index"], frames_per_buffer=4096, stream_callback=cb))
        print(f"Lyssnar: {name} <- {dev['name']} ({rate} Hz)")

    wlock = threading.Lock()

    def write(row):
        with wlock, open(a.out, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    write({"event": "joined", "title": f"Lokal utskrift ({model_name})", "participants": [s for s, _, _ in sources],
           "channels": {role: name for name, role, _ in sources},
           "at": datetime.datetime.fromtimestamp(t0).isoformat(timespec="seconds")})

    # Datorn får inte somna medan inspelningen pågår, även om ingen rör den. Skärmen får släckas.
    keep_awake = None
    if sys.platform == "win32":
        import ctypes
        keep_awake = ctypes.windll.kernel32.SetThreadExecutionState
        keep_awake(0x80000000 | 0x00000001)  # ES_CONTINUOUS | ES_SYSTEM_REQUIRED

    stop = threading.Event()
    screen = None
    if folder and a.screen:
        import subprocess
        # Videon får lägre prioritet än utskriften: den tål att vänta, det gör inte liveutskriften.
        region = ["-offset_x", str(monitor["x"]), "-offset_y", str(monitor["y"]),
                  "-video_size", f"{monitor['width']}x{monitor['height']}"] if monitor else []
        screen = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "gdigrab", "-framerate", "5", *region, "-i", "desktop",
                                   "-vf", "scale=-2:1080", "-c:v", "libx264", "-preset", "veryfast", "-crf", "30",
                                   "-pix_fmt", "yuv420p", str(folder / "screen.mp4")], stdin=subprocess.PIPE,
                                  creationflags=getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0))
        bbox = (monitor["x"], monitor["y"], monitor["x"] + monitor["width"], monitor["y"] + monitor["height"]) if monitor else None
        threading.Thread(target=frames_loop, args=(folder / "frames", write, t0, stop, bbox), daemon=True).start()
        which = f"skärm {monitor['n']}, {monitor['name']} {monitor['width']}x{monitor['height']}" if monitor else "alla skärmar"
        print(f"Skärmen spelas in ({which}): screen.mp4, och en bild i frames/ när skärmen ändras.")
    print(f"Fil: {a.out}. Skriver ut när talaren pausar. Stoppa med en fil som heter STOP i mappen, eller Ctrl+C.")

    # Utskriften i en egen tråd, så att den aldrig håller upp inspelningen. Det som väntar slås ihop per talare.
    # Ligger den ändå mer än --max-lag sekunder efter talet hoppar den över yttrandet; ljudet finns i filen
    # och refine.py tar det efteråt.
    jobs = queue.Queue()
    stats = {"n": 0, "lag": [], "skipped": 0.0, "echo": 0.0}
    stopping = threading.Event()

    def transcriber():
        while True:
            batch = [jobs.get()]
            while True:
                try:
                    batch.append(jobs.get_nowait())
                except queue.Empty:
                    break
            for name, start, end, x in merge([j for j in batch if j]):
                if not stopping.is_set() and time.time() - t0 - end > a.max_lag:
                    stats["skipped"] += len(x) / RATE
                    continue
                try:
                    segs, info = model.transcribe(x, language=None if a.lang == "auto" else a.lang, vad_filter=True,
                                                  beam_size=1, temperature=0.0, condition_on_previous_text=False,
                                                  without_timestamps=True)
                    text = " ".join(s.text.strip() for s in segs if is_speech(s))
                except Exception as e:  # utskriften får inte dö tyst; ljudet spelas in ändå
                    write({"event": "error", "message": f"utskriften: {e}"})
                    continue
                stats["lag"].append(time.time() - t0 - end)
                if text:
                    stats["n"] += 1
                    write({"n": stats["n"], "start": round(start, 1), "speaker": name, "text": text, "lang": info.language})
            if None in batch:
                return

    worker = threading.Thread(target=transcriber, daemon=True)
    worker.start()

    them = tracks[a.them].seg

    def queue_up(name, found):
        for start, x in found:
            if name != a.them and is_echo(start, x, them):
                stats["echo"] += len(x) / RATE  # högtalarna i mikrofonen; refine.py tar bort ekot ur sin utskrift
                continue
            jobs.put((name, start, start + len(x) / RATE, x))

    def take(now):
        with lock:
            taken = {k: v for k, v in incoming.items()}
            for k in incoming:
                incoming[k] = []
        for name, parts in taken.items():  # datorns ljud först, så att ekokontrollen har det
            if parts:
                queue_up(name, tracks[name].add(np.concatenate(parts), now))

    def status(now):
        lags = sorted(stats["lag"])
        row = {"event": "status", "start": round(now, 1), "levels": {name: t.level() for name, t in tracks.items()},
               "lag": round(lags[len(lags) // 2]) if lags else None, "skipped": round(stats["skipped"]),
               "echo": round(stats["echo"]), "dropped": {k: v for k, v in dropped.items() if v}}
        stats["lag"], stats["skipped"], stats["echo"] = [], 0.0, 0.0
        for k in dropped:
            dropped[k] = 0
        write(row)
        print(status_text(row))

    stopfile = (folder / "STOP") if folder else None
    next_status = STATUS_FIRST
    try:
        while not (stopfile and stopfile.exists()):
            time.sleep(0.2)
            now = time.time() - t0
            take(now)
            if now >= next_status:
                status(now)
                next_status += STATUS_EVERY
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        for s in streams:
            s.stop_stream()
            s.close()
        pa.terminate()
        end = time.time() - t0
        take(end)  # det som kom in sedan sist
        stopping.set()
        for name, t in tracks.items():
            queue_up(name, t.close(end))
        jobs.put(None)
        if screen:
            try:
                screen.communicate(b"q", timeout=20)  # ffmpeg avslutar videon ordentligt
            except Exception:
                screen.kill()
        worker.join(timeout=60)
        if stopfile and stopfile.exists():
            stopfile.unlink()
        if keep_awake:
            keep_awake(0x80000000)  # tillbaka till vanligt: datorn får somna igen
        write({"event": "ended", "reason": "stoppad", "at": datetime.datetime.now().isoformat(timespec="seconds"),
               "duration": round(end, 1)})
        print(f"Inspelningen är stoppad efter {int(end) // 60} min {int(end) % 60} s.")


if __name__ == "__main__":
    main()
