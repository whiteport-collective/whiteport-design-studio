#!/usr/bin/env python3
"""
local.py: what is heard on the computer, transcribed locally with Whisper while it happens. Part of WDS
(agents/wds/tools/meeting-live.md). The audio never leaves the computer.

Listens to the computer's audio out (loopback, what you hear) and the microphone (you). No bot joins the meeting,
so it works whoever sent the invitation and on any platform. With --no-mic only the computer's audio,
for videos, webinars and podcasts.

The audio is cut at natural pauses, when someone has finished speaking, and transcribed straight away. The delay
is about the length of the utterance plus one second. A long utterance is cut after --max seconds at the latest.
The lines use the same jsonl format as live.py, so `live.py watch` and `live.py archive` work.

The recording and the transcription run separately: the audio is always written to file, and if the transcription
cannot keep up it skips the oldest (refine.py takes it afterwards). A status line every minute shows the sound level
per channel and how far behind the transcription is.

    python local.py --list-screens                                                       # the screens to choose from
    python local.py --dir <folder> [--screen [--monitor 1]] [--them "De andra"] [--me "Mårten Angner"]   # one recording, everything in the folder
    python local.py <outfile.jsonl> [--them "De andra"] [--me "Mårten Angner"] [--lang sv | auto]
    python local.py <outfile.jsonl> --no-mic --them "The video"   # only the computer's audio

Windows (WASAPI loopback). Requires: python -m pip install pyaudiowpatch faster-whisper numpy
Swedish uses KB-Whisper (KBLab/kb-whisper-small), which is downloaded the first time.
First used in welqora-analysis 2026-10-14, when Fireflies transcribed a Swedish meeting in English.
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
THREADS = 3  # cores for Whisper: as fast as 4 (2026-10-21), and one core is left for audio, video and the meeting
STATUS_FIRST, STATUS_EVERY = 10, 60  # seconds to the first status line, and then between them


def to16k(rate, x):
    if rate == RATE or len(x) == 0:
        return x.astype(np.float32)
    m = int(len(x) * RATE / rate)
    return np.interp(np.linspace(0, len(x) - 1, m), np.arange(len(x)), x).astype(np.float32)


def cuda_available():
    """An NVIDIA card that faster-whisper (CTranslate2) can use."""
    try:
        import ctranslate2
        return ctranslate2.get_cuda_device_count() > 0
    except Exception:
        return False


def is_speech(seg, no_speech=0.6, logprob=-1.0):
    """Whisper sometimes makes up text in noise and short sounds. Only let through what the model itself thinks is speech.

    Removed: empty lines and punctuation ("."), Whisper's internal markers ("<|nospeech|>"), lines without
    letters ("000"), and what the model judges as probably not speech or as uncertain words."""
    text = seg.text.strip()
    if not text or "<|" in text or not re.search(r"[^\W\d_]", text):
        return False
    if getattr(seg, "no_speech_prob", 0) > no_speech:
        return False
    return getattr(seg, "avg_logprob", 0) > logprob


class Segmenter:
    """Collects audio from one source and hands over an utterance when the speaker pauses.

    feed(x) takes new samples (16 kHz) and returns finished utterances as (start time, audio).
    The start time is counted in samples from the start of the recording, so it matches the audio file. skip(n) moves
    the time forward when the sound card delivered nothing."""

    FRAME = 0.1  # seconds per analysis frame

    def __init__(self, threshold=0.006, pause=0.5, max_len=8.0, min_len=0.6):
        self.threshold, self.pause, self.max_len, self.min_len = threshold, pause, max_len, min_len
        self.buf = np.zeros(0, dtype=np.float32)
        self.speech = False    # does the buffer hold speech
        self.silence = 0.0     # seconds of silence since the last speech
        self.pending = np.zeros(0, dtype=np.float32)
        self.pos = 0           # samples analysed, from the start of the recording
        self.env_t, self.env = [], []  # the sound level per analysis frame over the last minutes, for the echo check

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
                # Only silence: keep the last 0.3 seconds, so that the start of the next word is included.
                keep = int(0.3 * RATE)
                self.buf = self.buf[-keep:]
        return out

    def skip(self, n):
        """n samples of silence the sound card did not deliver: ends an utterance in progress and moves the time forward."""
        out = self.flush()
        self.pos += len(self.pending) + n
        self.pending = np.zeros(0, dtype=np.float32)
        return out

    def envelope(self, times):
        """The sound level at the given times; silence where no sound came."""
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
    """When the speakers are heard in the microphone, the microphone's sound level follows the computer's audio up and
    down. Then the utterance is echo, not the person. When the person speaks, the computer's audio is silent or out of
    step. Compares the level curves (100 ms per point) for the utterance's time; theirs is the segmenter for the computer's audio."""
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
    """Utterances waiting for transcription are merged per speaker, up to 25 seconds. Whisper always computes on
    30 seconds of audio, so a piece of 2 s costs almost as much as one of 25 (2.4 against 4.1 s on Mårten's computer).
    Without this the transcription could not keep up when the microphone gave many short pieces. jobs: (speaker, start, end, audio)."""
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
    """One channel on the recording's timeline: the audio to file (if there is one) and to utterances.

    Windows delivers nothing from the speaker output when nothing is playing. The silence is therefore filled in by
    the clock, so that audio file, transcript and screen share the same time and the file is as long as the recording."""

    def __init__(self, segmenter, path=None):
        self.seg, self.pos, self.wav = segmenter, 0, None
        self.sq, self.count = 0.0, 0  # for the status line
        if path:
            import wave
            self.wav = wave.open(str(path), "wb")
            self.wav.setnchannels(1)
            self.wav.setsampwidth(2)
            self.wav.setframerate(RATE)

    def add(self, x, now):
        out = []
        gap = int(now * RATE) - len(x) - self.pos
        if gap > RATE // 5:  # more than 0.2 s missing: fill with silence
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
        """The sound level since the last call in dB (0 is full, -60 almost silent), or None if no sound came."""
        rms = math.sqrt(self.sq / self.count) if self.count else 0.0
        self.sq, self.count = 0.0, 0
        return max(-90, round(20 * math.log10(rms))) if rms > 0 else None

    def close(self, now):
        out = self.seg.flush()
        rest = int(now * RATE) - self.pos  # silence up to the stop
        if rest > 0:
            self._silence(rest)
        if self.wav:
            self.wav.close()
        return out


def status_text(row):
    """The status line as text, the same as live.py shows."""
    levels = ", ".join(f"{k} {'no sound' if v is None else f'{v} dB'}" for k, v in row["levels"].items())
    s = f"Status {int(row['start']) // 60:02d}:{int(row['start']) % 60:02d}: {levels}"
    if row.get("lag") is not None:
        s += f" · text {row['lag']} s behind the speech"
    if row.get("skipped"):
        s += f" · {row['skipped']} s skipped live (included in the thorough transcript)"
    if row.get("echo"):
        s += f" · {row['echo']} s echo from the speakers in the microphone"
    if row.get("dropped"):
        s += " · audio blocks dropped: " + ", ".join(f"{k} {v}" for k, v in row["dropped"].items())
    return s


def frames_loop(folder, write, t0, stop, bbox=None, every=5.0, change=4.0):
    """A picture of the screen when it has changed, checked every five seconds. The line in the transcript points to the picture.
    bbox: the chosen screen (left, top, right, bottom); otherwise the main screen."""
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
    """The connected screens in Windows order: number, name, position and size in real pixels, main screen."""
    import ctypes
    from ctypes import wintypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # real pixels, not scaled
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
    """Windows can throttle a process running in the background (EcoQoS), for example when it was started by an agent
    and a video meeting has the foreground. Then the transcription cannot keep up. Turn off the throttling for this process."""
    if sys.platform != "win32":
        return
    import ctypes
    from ctypes import wintypes

    class State(ctypes.Structure):
        _fields_ = [("Version", wintypes.ULONG), ("ControlMask", wintypes.ULONG), ("StateMask", wintypes.ULONG)]

    k = ctypes.windll.kernel32
    k.GetCurrentProcess.restype = wintypes.HANDLE
    k.SetProcessInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    s = State(1, 0x1, 0)  # PROCESS_POWER_THROTTLING_EXECUTION_SPEED, off
    k.SetProcessInformation(k.GetCurrentProcess(), 4, ctypes.byref(s), ctypes.sizeof(s))  # ProcessPowerThrottling


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", help="the transcript's jsonl file; with --dir it becomes <dir>/transcript.jsonl")
    ap.add_argument("--dir", help="the recording's folder: transcript, audio per channel, screen video and pictures")
    ap.add_argument("--screen", action="store_true", help="record the screen as video and save a picture when it changes")
    ap.add_argument("--monitor", type=int, help="which screen (number from --list-screens); without it all screens")
    ap.add_argument("--region", help="only part of the screen, as fractions of it: left,top,width,height, for example 0,0,0.5,0.5 for the top left quarter")
    ap.add_argument("--list-screens", action="store_true", help="list the screens and exit")
    ap.add_argument("--them", default="De andra")
    ap.add_argument("--me", default="Jag")
    ap.add_argument("--lang", default="sv", help="sv, en … or auto: the language is detected for each utterance")
    ap.add_argument("--no-mic", action="store_true", help="only the computer's audio, for example a video or a webinar")
    ap.add_argument("--mic", help="microphone whose name contains the text, for example Surface; without it the Windows default microphone")
    ap.add_argument("--pause", type=float, default=0.5, help="seconds of silence that end an utterance")
    ap.add_argument("--max", type=float, default=8.0, help="longest utterance before it is cut")
    ap.add_argument("--threshold", type=float, default=0.006, help="sound level that counts as speech")
    ap.add_argument("--max-lag", type=float, default=30.0, help="seconds behind the speech at which the transcription skips an utterance")
    ap.add_argument("--model", default=None, help="default: KBLab/kb-whisper-small for Swedish, otherwise small")
    ap.add_argument("--threads", type=int, default=THREADS, help="cores for the speech recognition; the rest for audio, video and the meeting")
    a = ap.parse_args()
    if a.list_screens:
        for m in screens():
            print(f"{m['n']}. {m['name']} ({m['device']}): {m['width']}x{m['height']}"
                  f"{' (main screen)' if m['primary'] else ''}, position {m['x']},{m['y']}")
        return
    monitor = None
    if a.monitor:
        a.screen = True
        monitor = next((m for m in screens() if m["n"] == a.monitor), None)
        if not monitor:
            ap.error(f"screen {a.monitor} does not exist; see --list-screens")
        if a.region:
            # A smaller video: only the part of the screen that shows what the conversation is about. Even sizes for x264.
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
        ap.error("give an output file or --dir")

    try:
        import pyaudiowpatch as pyaudio
        from faster_whisper import WhisperModel
    except ImportError:
        print("Packages missing: python -m pip install pyaudiowpatch faster-whisper numpy")
        sys.exit(1)

    no_power_throttling()
    # The model is loaded before the recording. Audio that came during loading used to land before the clock's start,
    # and the times at the beginning became negative.
    model_name = a.model or ("KBLab/kb-whisper-small" if a.lang == "sv" else "small")
    print(f"Loading the speech recognition ({model_name}) …")
    if cuda_available():  # NVIDIA card: faster-whisper on CUDA
        model = WhisperModel(model_name, device="cuda", compute_type="float16")
        print("Speech recognition on the NVIDIA card (CUDA)")
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
                ap.error(f"no microphone has {a.mic!r} in its name")
        sources.append((a.me, "me", mic))
    incoming = {name: [] for name, _, _ in sources}
    dropped = {name: 0 for name, _, _ in sources}  # blocks the sound card dropped because we did not fetch them in time
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
        print(f"Listening: {name} <- {dev['name']} ({rate} Hz)")

    wlock = threading.Lock()

    def write(row):
        with wlock, open(a.out, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    write({"event": "joined", "title": f"Local transcript ({model_name})", "participants": [s for s, _, _ in sources],
           "channels": {role: name for name, role, _ in sources},
           "at": datetime.datetime.fromtimestamp(t0).isoformat(timespec="seconds")})

    # The computer must not fall asleep while the recording runs, even if nobody touches it. The screen may turn off.
    keep_awake = None
    if sys.platform == "win32":
        import ctypes
        keep_awake = ctypes.windll.kernel32.SetThreadExecutionState
        keep_awake(0x80000000 | 0x00000001)  # ES_CONTINUOUS | ES_SYSTEM_REQUIRED

    stop = threading.Event()
    screen = None
    if folder and a.screen:
        import subprocess
        # The video gets lower priority than the transcription: it can wait, the live transcription cannot.
        region = ["-offset_x", str(monitor["x"]), "-offset_y", str(monitor["y"]),
                  "-video_size", f"{monitor['width']}x{monitor['height']}"] if monitor else []
        screen = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "gdigrab", "-framerate", "5", *region, "-i", "desktop",
                                   "-vf", "scale=-2:1080", "-c:v", "libx264", "-preset", "veryfast", "-crf", "30",
                                   "-pix_fmt", "yuv420p", str(folder / "screen.mp4")], stdin=subprocess.PIPE,
                                  creationflags=getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0))
        bbox = (monitor["x"], monitor["y"], monitor["x"] + monitor["width"], monitor["y"] + monitor["height"]) if monitor else None
        threading.Thread(target=frames_loop, args=(folder / "frames", write, t0, stop, bbox), daemon=True).start()
        which = f"screen {monitor['n']}, {monitor['name']} {monitor['width']}x{monitor['height']}" if monitor else "all screens"
        print(f"Recording the screen ({which}): screen.mp4, and a picture in frames/ when the screen changes.")
    print(f"File: {a.out}. Transcribes when the speaker pauses. Stop with a file named STOP in the folder, or Ctrl+C.")

    # The transcription in its own thread, so that it never holds up the recording. What is waiting is merged per speaker.
    # If it is still more than --max-lag seconds behind the speech it skips the utterance; the audio is in the file
    # and refine.py takes it afterwards.
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
                except Exception as e:  # the transcription must not die silently; the audio is recorded anyway
                    write({"event": "error", "message": f"transcription: {e}"})
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
                stats["echo"] += len(x) / RATE  # the speakers in the microphone; refine.py removes the echo from its transcript
                continue
            jobs.put((name, start, start + len(x) / RATE, x))

    def take(now):
        with lock:
            taken = {k: v for k, v in incoming.items()}
            for k in incoming:
                incoming[k] = []
        for name, parts in taken.items():  # the computer's audio first, so that the echo check has it
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
        take(end)  # what came in since last time
        stopping.set()
        for name, t in tracks.items():
            queue_up(name, t.close(end))
        jobs.put(None)
        if screen:
            try:
                screen.communicate(b"q", timeout=20)  # ffmpeg finishes the video properly
            except Exception:
                screen.kill()
        worker.join(timeout=60)
        if stopfile and stopfile.exists():
            stopfile.unlink()
        if keep_awake:
            keep_awake(0x80000000)  # back to normal: the computer may sleep again
        write({"event": "ended", "reason": "stopped", "at": datetime.datetime.now().isoformat(timespec="seconds"),
               "duration": round(end, 1)})
        print(f"The recording stopped after {int(end) // 60} min {int(end) % 60} s.")


if __name__ == "__main__":
    main()
