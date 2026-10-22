"""Skriver ut talet i videoklipp till SubRip (.srt) på datorn, med faster-whisper.

    python transcribe.py <mapp eller fil> <utmapp> [--model KBLab/kb-whisper-medium] [--lang sv|en|auto] [--words]

Varje klipp får <utmapp>/<grundnamn>.srt. Ett klipp som redan har en .srt hoppas över, så körningen
kan avbrytas och startas om. Klipp utan tal får en tom .srt, så att de inte körs igen.
--words skriver också <grundnamn>.words.json med tid per ord, för klippning.
Ljudet tas ut med ffmpeg till en tillfällig wav; ingenting skrivs bredvid originalen.
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path

VIDEO = {".mp4", ".mov", ".mts", ".m2ts", ".mxf", ".avi", ".mkv", ".wav", ".mp3", ".m4a"}


def ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--model", default="KBLab/kb-whisper-medium")
    ap.add_argument("--lang", default="sv", help="sv, en … eller auto")
    ap.add_argument("--words", action="store_true")
    a = ap.parse_args()

    clips = [a.source] if a.source.is_file() else sorted(p for p in a.source.rglob("*") if p.suffix.lower() in VIDEO)
    todo = [p for p in clips if not (a.out / (p.stem + ".srt")).exists()]
    print(f"{len(clips)} klipp, {len(clips) - len(todo)} redan utskrivna, {len(todo)} kvar", flush=True)
    if not todo:
        return 0
    a.out.mkdir(parents=True, exist_ok=True)

    from faster_whisper import WhisperModel
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    for i, clip in enumerate(todo, 1):
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "a.wav"
            r = subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(clip), "-vn", "-ac", "1", "-ar", "16000", str(wav)])
            if r.returncode or not wav.exists():
                print(f"  {clip.name}: inget ljud", flush=True)
                (a.out / (clip.stem + ".srt")).write_text("", encoding="utf-8")
                continue
            segs, info = model.transcribe(str(wav), language=None if a.lang == "auto" else a.lang,
                                          vad_filter=True, word_timestamps=a.words)
            segs = list(segs)
        lines, words = [], []
        for n, s in enumerate(segs, 1):
            lines += [str(n), f"{ts(s.start)} --> {ts(s.end)}", s.text.strip(), ""]
            if a.words and s.words:
                words += [{"start": round(w.start, 2), "end": round(w.end, 2), "word": w.word} for w in s.words]
        tmp_srt = a.out / (clip.stem + ".srt.part")
        tmp_srt.write_text("\n".join(lines), encoding="utf-8")
        tmp_srt.replace(a.out / (clip.stem + ".srt"))
        if a.words:
            (a.out / (clip.stem + ".words.json")).write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
        print(f"  {i}/{len(todo)} {clip.name}: {len(segs)} repliker ({info.language})", flush=True)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
