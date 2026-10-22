"""Mediaarbetaren: gör de långa jobben på mediet i de delade enheterna, utan AI och utan server.

    python worker.py run    [--root "G:/Shared drives"] [--every 300] [--once]
    python worker.py status [--root "G:/Shared drives"]
    python worker.py wash   <klipp> [--out <mapp>]

run     söker igenom <root>/*/projects/*/<inspelning>/original/** och gör två sorters jobb:
        1. Utskrift: varje videoklipp utan <inspelning>/transkript/<grundnamn>.srt skrivs ut
           (transcribe-toolet, med tid per ord).
        2. Tvätt: varje jobbfil <projekt>/jobb/*.tvatta (en rad: klippets sökväg under projektet)
           ger en tvättad tidslinje i <inspelning>/klipp/: utan hummanden, utfyllnadsord,
           upprepningar och långa pauser. Jobbfilen flyttas till jobb/klara/.
        Varje klart jobb blir en rad i projektets logg.md. --once kör ett varv och slutar.
status  visar vad som väntar och vad som är klart, per projekt.
wash    tvättar ett klipp direkt (kräver <grundnamn>.words.json i inspelningens transkript/).

Inget skrivs i original/. Jobb som avbryts görs om nästa varv; ett klart jobb görs aldrig om.
"""
import argparse, csv, datetime as dt, json, os, re, subprocess, sys, time
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
TRANSCRIBE = HERE.parent / "transcribe" / "transcribe.py"
VIDEO = {".mp4", ".mov", ".mts", ".m2ts", ".mxf"}
HESITATIONS = {"eh", "ehm", "eeh", "öh", "öhm", "öhh", "äh", "ähm", "hm", "hmm", "mm", "mhm", "um", "uh", "uhm", "ah"}
FILLERS = {"liksom", "typ", "alltså", "ba", "asså", "såhär", "ju"}
PAUSE = 0.6      # längre tystnad än så kortas
KEEP = 0.15      # så mycket luft som lämnas vid varje skarv
NAME = "media-worker"


def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def projects(root: Path):
    return sorted(p for p in root.glob("*/projects/*") if p.is_dir())


def recordings(project: Path):
    return sorted(p for p in project.iterdir() if p.is_dir() and (p / "original").is_dir())


def clips(rec: Path):
    return sorted(p for p in (rec / "original").rglob("*") if p.suffix.lower() in VIDEO)


def log(project: Path, text: str):
    f = project / "logg.md"
    lines = f.read_text(encoding="utf-8").splitlines() if f.exists() else ["# Logg", ""]
    i = next((n for n, l in enumerate(lines) if l.startswith("- ")), len(lines))
    lines.insert(i, f"- {now()[:10]} · {NAME} · {text}")
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")


def pending_transcripts(rec: Path):
    out = rec / "transkript"
    return [c for c in clips(rec) if not (out / (c.stem + ".srt")).exists()]


def transcribe(rec: Path, clip: Path):
    r = subprocess.run([sys.executable, str(TRANSCRIBE), str(clip), str(rec / "transkript"), "--words"])
    return r.returncode == 0


# ---------- tvätt ----------

def probe(clip: Path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", str(clip)],
                       capture_output=True, text=True)
    info = json.loads(r.stdout)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    rate = Fraction(v.get("r_frame_rate", "25/1"))
    return {"rate": rate, "w": int(v["width"]), "h": int(v["height"]), "dur": float(info["format"]["duration"])}


def classify(word: str, prev: str):
    w = re.sub(r"[^\wåäö]", "", word.lower())
    if w in HESITATIONS:
        return "humm"
    if w in FILLERS:
        return "utfyllnad"
    if w and w == prev:
        return "upprepning"
    return None


def wash(clip: Path, out: Path | None = None, words_f: Path | None = None):
    rec = clip.parents[[p.name for p in clip.parents].index("original") + 1] if "original" in [p.name for p in clip.parents] else clip.parent
    words_f = words_f or rec / "transkript" / (clip.stem + ".words.json")
    words = json.loads(words_f.read_text(encoding="utf-8"))
    info = probe(clip)
    out = out or rec / "klipp"
    out.mkdir(parents=True, exist_ok=True)

    cuts, keep, prev, t = [], [], "", 0.0
    seg_start = None
    for w in words:
        kind = classify(w["word"], prev)
        prev = re.sub(r"[^\wåäö]", "", w["word"].lower())
        if kind:
            cuts.append((w["start"], w["end"], w["word"].strip(), kind))
            if seg_start is not None:
                keep.append((seg_start, min(w["start"], t + KEEP)))
                seg_start = None
            t = w["end"]
            continue
        if seg_start is None:
            seg_start = max(0.0, w["start"] - KEEP) if keep or w["start"] > KEEP else 0.0
        elif w["start"] - t > PAUSE:
            keep.append((seg_start, t + KEEP))
            cuts.append((t + KEEP, w["start"] - KEEP, "", f"paus {w['start'] - t:.1f} s"))
            seg_start = w["start"] - KEEP
        t = w["end"]
    if seg_start is not None:
        keep.append((seg_start, min(info["dur"], t + KEEP)))

    # tidkodskarta: rå tid <-> tvättad tid
    rows, pos = [], 0.0
    for a, b in keep:
        rows.append({"typ": "behall", "start_ra": round(a, 2), "slut_ra": round(b, 2),
                     "start_tvattad": round(pos, 2), "slut_tvattad": round(pos + b - a, 2), "ord": "", "varfor": ""})
        pos += b - a
    for a, b, word, why in cuts:
        rows.append({"typ": "bort", "start_ra": round(a, 2), "slut_ra": round(b, 2),
                     "start_tvattad": "", "slut_tvattad": "", "ord": word, "varfor": why})
    rows.sort(key=lambda r: r["start_ra"])
    base = out / f"{clip.stem}-tvattad"
    with open(f"{base}.csv", "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=["typ", "start_ra", "slut_ra", "start_tvattad", "slut_tvattad", "ord", "varfor"])
        wr.writeheader(); wr.writerows(rows)
    Path(f"{base}.xml").write_text(xmeml(clip, info, keep, cuts), encoding="utf-8")
    removed = info["dur"] - pos
    return {"klipp": clip.name, "behallna": len(keep), "bort": len(cuts), "sekunder_bort": round(removed, 1),
            "csv": f"{base}.csv", "xml": f"{base}.xml"}


def xmeml(clip: Path, info, keep, cuts):
    """FCP 7 XML, som DaVinci Resolve och Premiere läser (File → Import → Timeline)."""
    rate = info["rate"]
    ntsc = rate.denominator == 1001
    tb = round(float(rate))
    fr = lambda s: int(round(s * float(rate)))
    url = "file://localhost/" + quote(clip.resolve().as_posix(), safe="/:")
    rate_x = f"<rate><timebase>{tb}</timebase><ntsc>{'TRUE' if ntsc else 'FALSE'}</ntsc></rate>"
    file_x = (f'<file id="f1"><name>{clip.name}</name><pathurl>{url}</pathurl>{rate_x}<duration>{fr(info["dur"])}</duration>'
              f'<media><video><samplecharacteristics><width>{info["w"]}</width><height>{info["h"]}</height></samplecharacteristics></video>'
              f'<audio><channelcount>2</channelcount></audio></media></file>')
    vid, aud, markers, pos = [], [], [], 0
    for n, (a, b) in enumerate(keep, 1):
        ln = fr(b) - fr(a)
        f = file_x if n == 1 else '<file id="f1"/>'
        vid.append(f"<clipitem id=\"v{n}\"><name>{clip.stem} {n}</name>{rate_x}<start>{pos}</start><end>{pos + ln}</end>"
                   f"<in>{fr(a)}</in><out>{fr(b)}</out>{f}</clipitem>")
        aud.append(f"<clipitem id=\"a{n}\"><name>{clip.stem} {n}</name>{rate_x}<start>{pos}</start><end>{pos + ln}</end>"
                   f"<in>{fr(a)}</in><out>{fr(b)}</out><file id=\"f1\"/><sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack></clipitem>")
        pos += ln
        if n < len(keep):
            nxt = keep[n][0]
            what = ", ".join((c[2] or c[3]) for c in cuts if b - KEEP <= c[0] < nxt + KEEP) or "paus"
            markers.append(f"<marker><name>bort: {what}</name><comment>rå {b:.2f}–{nxt:.2f} s</comment><in>{pos}</in><out>-1</out></marker>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4"><sequence>'
            f"<name>{clip.stem} tvättad</name>{rate_x}<duration>{pos}</duration>{''.join(markers)}"
            f"<media><video><format><samplecharacteristics>{rate_x}<width>{info['w']}</width><height>{info['h']}</height></samplecharacteristics></format>"
            f"<track>{''.join(vid)}</track></video><audio><track>{''.join(aud)}</track></audio></media></sequence></xmeml>\n")


# ---------- jobbkön ----------

def wash_jobs(project: Path):
    d = project / "jobb"
    return sorted(d.glob("*.tvatta")) if d.is_dir() else []


def run_once(root: Path):
    done = 0
    for project in projects(root):
        for rec in recordings(project):
            todo = pending_transcripts(rec)
            ok = [c for c in todo if transcribe(rec, c)]
            if ok:
                log(project, f"Utskrift: {rec.name}, {len(ok)} klipp ({', '.join(c.name for c in ok[:5])}{' …' if len(ok) > 5 else ''})")
                done += len(ok)
        for job in wash_jobs(project):
            clip = project / job.read_text(encoding="utf-8").strip().replace("\\", "/")
            try:
                rec = clip.parents[[p.name for p in clip.parents].index("original") + 1]
                if not (rec / "transkript" / (clip.stem + ".words.json")).exists():
                    transcribe(rec, clip)
                r = wash(clip)
            except Exception as e:  # jobbet ligger kvar och görs om nästa varv
                print(f"{job.name}: {e}", flush=True)
                continue
            (project / "jobb" / "klara").mkdir(exist_ok=True)
            os.replace(job, project / "jobb" / "klara" / job.name)
            log(project, f"Tvätt: {r['klipp']}, {r['bort']} bitar bort ({r['sekunder_bort']} s), tidslinje i {Path(r['xml']).parent.name}/{Path(r['xml']).name}")
            done += 1
    return done


def status(root: Path):
    for project in projects(root):
        recs = recordings(project)
        n_clips = sum(len(clips(r)) for r in recs)
        n_todo = sum(len(pending_transcripts(r)) for r in recs)
        jobs = wash_jobs(project)
        if n_clips or jobs:
            print(f"{project.parent.parent.name} / {project.name}: {n_clips} klipp, {n_clips - n_todo} utskrivna, "
                  f"{n_todo} väntar, {len(jobs)} tvättjobb väntar")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("--root", default="G:/Shared drives", type=Path)
    r.add_argument("--every", type=int, default=300); r.add_argument("--once", action="store_true")
    s = sub.add_parser("status"); s.add_argument("--root", default="G:/Shared drives", type=Path)
    w = sub.add_parser("wash"); w.add_argument("clip", type=Path); w.add_argument("--out", type=Path); w.add_argument("--words", type=Path)
    a = ap.parse_args()
    if a.cmd == "status":
        status(a.root)
    elif a.cmd == "wash":
        print(json.dumps(wash(a.clip, a.out, a.words), ensure_ascii=False, indent=1))
    else:
        while True:
            n = run_once(a.root)
            print(f"{now()} varv klart, {n} jobb", flush=True)
            if a.once:
                break
            time.sleep(a.every)
