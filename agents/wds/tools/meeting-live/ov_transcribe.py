"""Transcribes audio on Intel's GPU with OpenVINO (KB-Whisper), with times per word.
Usage: python ov_transcribe.py <model folder> <work folder> <id> [<id> ...]
Writes <id>.txt (timestamped segments) and <id>.words.json (words with start and end)."""
import json, os, subprocess, sys, time
import soundfile as sf
import openvino_genai as og

model, work, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
t0 = time.time()
pipe = og.WhisperPipeline(model, "GPU", word_timestamps=True, CACHE_DIR=os.path.join(model, "cache"))
print("GPU loaded in", round(time.time() - t0, 1), "s", flush=True)
for v in ids:
    out = os.path.join(work, f"{v}.txt")
    if os.path.exists(out):
        continue
    src = next(os.path.join(work, f) for f in os.listdir(work) if f.startswith(v + ".") and f.endswith((".mp4", ".m4a", ".webm")))
    wav = os.path.join(work, f"{v}.wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", wav], check=True)
    audio, _ = sf.read(wav, dtype="float32")
    t0 = time.time()
    r = pipe.generate(audio.tolist(), language="<|sv|>", task="transcribe", return_timestamps=True, word_timestamps=True)
    dt = time.time() - t0
    lines = [f"[{int(c.start_ts // 60):02d}:{int(c.start_ts % 60):02d}] {c.text.strip()}" for c in r.chunks]
    words = [{"w": w.word, "start": round(w.start_ts, 3), "end": round(w.end_ts, 3)} for w in (r.words or [])]
    json.dump(words, open(os.path.join(work, f"{v}.words.json"), "w", encoding="utf-8"), ensure_ascii=False)
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    os.remove(wav)
    print(v, f"done, {len(audio)/16000/60:.1f} min of audio in {dt/60:.1f} min ({len(audio)/16000/dt:.1f}x real time), {len(words)} words", flush=True)
print("ALL DONE", flush=True)
