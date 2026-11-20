#!/usr/bin/env python3
"""
refine.py: the thorough transcription after a recording. Part of WDS (agents/wds/tools/meeting-live.md).

The live transcription makes trade-offs to keep up: a small model, short pieces, a fast search. Afterwards there
is time. refine takes the recording's audio per channel (them.wav, me.wav) and transcribes it in one pass with a
larger model and a more thorough search, removes the echo (what the microphone heard from the speakers) and writes
final.jsonl in the same format as the live transcript, so that `live.py archive` takes it.

    python refine.py <recording folder> [--model KBLab/kb-whisper-medium] [--lang sv] [--device auto|gpu|cpu]

Requires: faster-whisper. KB-Whisper medium is downloaded the first time (about 1.5 GB).
On the processor, medium takes about half the conversation's length per channel.

NVIDIA card (--device cuda, or auto): faster-whisper on CUDA, float16; requires the CUDA libraries that setup.ps1
installs. Intel graphics (--device gpu, or auto): OpenVINO (the packages openvino-genai and,
once for the conversion, optimum-intel[openvino]). The model is converted the first time to
~/.venvs/models/<model>-int8-ov (an existing <model>-ov is used first). faster-whisper still finds where there is speech (VAD), so that
the silence is never transcribed; the speech is transcribed on the graphics card in pieces of at most 28 seconds. Without a graphics card,
or if something goes wrong there, the processor is used.
"""

import argparse
import difflib
import io
import json
import re
import sys
import time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
sys.path.insert(0, str(Path(__file__).parent))
from local import RATE, cuda_available, is_speech  # noqa: E402  the same filter against made-up text as live


def read_wav(path):
    import wave
    import numpy as np
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def sounding(x):
    """Seconds with any sound at all. Filled-in silence is exactly zero; a microphone always hisses a little."""
    secs = len(x) // RATE
    return int((x[:secs * RATE].reshape(secs, RATE) != 0).any(axis=1).sum()) if secs else 0


def clock(sec):
    s = int(sec)
    return f"{s // 60}:{s % 60:02d}"


def norm(text):
    return re.sub(r"\W+", " ", text.lower()).strip()


def echo(mine, theirs):
    """A line from the microphone that is almost word for word something that just came from the computer is echo from the speakers."""
    a = norm(mine["text"])
    for t in theirs:
        if abs(t["start"] - mine["start"]) <= 4 and difflib.SequenceMatcher(None, a, norm(t["text"])).ratio() >= 0.6:
            return True
    return False


def ov_model_dir(model):
    """The model in OpenVINO format, in ~/.venvs/models where KB-Whisper small already was (2026-10-14).
    If <name>-ov (fp16) exists it is used, otherwise <name>-int8-ov, which is converted once with optimum-intel."""
    import subprocess
    root = Path.home() / ".venvs" / "models"
    name = model.split("/")[-1]
    for d in (root / f"{name}-ov", root / f"{name}-int8-ov"):
        if (d / "openvino_tokenizer.xml").exists():
            return d
    out = root / f"{name}-int8-ov"
    print(f"Converting {model} to OpenVINO (once, a few minutes) …")
    subprocess.run([sys.executable, "-m", "optimum.commands.optimum_cli", "export", "openvino",
                    "--model", model, "--weight-format", "int8", str(out)], check=True)
    return out


def gpu_available():
    try:
        import openvino
        import openvino_genai  # noqa: F401
        return "GPU" in openvino.Core().available_devices
    except Exception:
        return False


def speech_chunks(x, max_len=28.0, gap=1.5):
    """Where there is speech (faster-whisper's VAD), merged into pieces of at most max_len seconds."""
    from faster_whisper.vad import VadOptions, get_speech_timestamps
    chunks = []
    for s in get_speech_timestamps(x, VadOptions()):
        if chunks and s["end"] - chunks[-1][0] <= max_len * RATE and s["start"] - chunks[-1][1] <= gap * RATE:
            chunks[-1][1] = s["end"]
        else:
            chunks.append([s["start"], s["end"]])
    return chunks


def transcribe_gpu(pipe, x, lang):
    """The speech is transcribed piece by piece on the graphics card. Yields (start, text) in seconds from the start of the file."""
    from types import SimpleNamespace
    cfg = pipe.get_generation_config()
    cfg.task = "transcribe"
    cfg.return_timestamps = True
    if lang != "auto":
        cfg.language = f"<|{lang}|>"
    pad = int(0.2 * RATE)
    for a, b in speech_chunks(x):
        a0 = max(0, a - pad)
        res = pipe.generate(x[a0:b + pad].tolist(), cfg)
        parts = res.chunks or [SimpleNamespace(start_ts=0.0, text=res.texts[0])]
        for c in parts:
            seg = SimpleNamespace(text=c.text)
            if is_speech(seg):
                yield a0 / RATE + max(0.0, c.start_ts), c.text.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--model", default="KBLab/kb-whisper-medium")
    ap.add_argument("--lang", default="sv", help="sv, en … or auto")
    ap.add_argument("--device", default="auto", choices=["auto", "gpu", "cuda", "cpu"],
                    help="auto: NVIDIA (CUDA) or Intel graphics (OpenVINO) when present, otherwise the processor")
    ap.add_argument("--first", type=float, help="only the first N seconds (for measuring)")
    ap.add_argument("--out", default="final.jsonl", help="file name in the folder (default final.jsonl)")
    a = ap.parse_args()
    folder = Path(a.dir)
    live = folder / "transcript.jsonl"
    head = {}
    if live.exists():
        head = next((json.loads(l) for l in live.read_text(encoding="utf-8").splitlines() if '"joined"' in l), {})
    channels = head.get("channels") or {"them": "De andra", "me": "Jag"}
    end = {}
    if live.exists():
        end = next((json.loads(l) for l in live.read_text(encoding="utf-8").splitlines() if '"ended"' in l), {})

    pipe, model, device = None, None, "cpu"
    if a.device == "cuda" or (a.device == "auto" and cuda_available()):
        from faster_whisper import WhisperModel
        model, device = WhisperModel(a.model, device="cuda", compute_type="float16"), "cuda"
    elif a.device == "gpu" or (a.device == "auto" and gpu_available()):
        try:
            import openvino_genai
            md = ov_model_dir(a.model)
            pipe = openvino_genai.WhisperPipeline(str(md), "GPU", CACHE_DIR=str(md / "cache"))  # compiled kernels are saved, faster start
            device = "gpu"
        except Exception as e:
            print(f"The graphics card could not be used ({e}); running on the processor.")
    if pipe is None and model is None:
        from faster_whisper import WhisperModel
        model = WhisperModel(a.model, device="cpu", compute_type="int8")
    print("Device: " + {"gpu": "Intel graphics (OpenVINO)", "cuda": "the NVIDIA card (CUDA, faster-whisper)"}.get(device, "the processor (faster-whisper)"))
    rows = {}
    for role in ("them", "me"):
        wav = folder / f"{role}.wav"
        if not wav.exists():
            continue
        x = read_wav(wav)
        if a.first:
            x = x[:int(a.first * RATE)]
        print(f"{wav.name}: {clock(len(x) / RATE)} long, sound in {clock(sounding(x))} of it (the rest is filled-in silence)")
        t = time.time()
        speaker = channels.get(role, role)
        if pipe is not None:
            rows[role] = [{"start": round(st, 1), "speaker": speaker, "text": tx, "lang": a.lang}
                          for st, tx in transcribe_gpu(pipe, x, a.lang)]
        else:
            segs, info = model.transcribe(x, language=None if a.lang == "auto" else a.lang,
                                          vad_filter=True, beam_size=5, condition_on_previous_text=True)
            rows[role] = [{"start": round(s.start, 1), "speaker": speaker, "text": s.text.strip(), "lang": info.language}
                          for s in segs if is_speech(s)]
        took = time.time() - t
        print(f"{wav.name}: {len(rows[role])} lines in {took:.0f} s ({len(x) / RATE / max(took, 1):.1f}x real time)")

    theirs = rows.get("them", [])
    mine = [r for r in rows.get("me", []) if not echo(r, theirs)]
    removed = len(rows.get("me", [])) - len(mine)
    merged = sorted(theirs + mine, key=lambda r: r["start"])
    out = folder / a.out
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"event": "joined", "title": f"Thorough transcript ({a.model}, {device})", "participants": list(channels.values()),
                             "at": head.get("at", "")}, ensure_ascii=False) + "\n")
        for i, r in enumerate(merged, 1):
            fh.write(json.dumps({"n": i, **r}, ensure_ascii=False) + "\n")
        # End time and length from the recording, so that archive gets the right time and length.
        fh.write(json.dumps({"event": "ended", "reason": "thorough transcript",
                             **{k: end[k] for k in ("at", "duration") if k in end}}) + "\n")
    print(f"{out}: {len(merged)} lines, {removed} echoes removed")


if __name__ == "__main__":
    main()
