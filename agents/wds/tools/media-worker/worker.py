"""Mediaarbetaren: gör de långa jobben på mediet i de delade enheterna, utan AI och utan server.

    python worker.py run    [--root "G:/Shared drives"] [--every 300] [--once]
    python worker.py status [--root "G:/Shared drives"]
    python worker.py wash   <klipp> [--out <mapp>]
    python worker.py batch  <klippmapp> <utmapp>

run     söker igenom <root>/*/projects/*/<inspelning>/original/** och gör två sorters jobb:
        1. Utskrift: varje videoklipp utan <inspelning>/transkript/<grundnamn>.srt skrivs ut
           (transcribe-toolet, med tid per ord).
        2. Tvätt: varje jobbfil <projekt>/jobb/*.tvatta (en rad: klippets sökväg under projektet)
           tvättar ett klipp till. Varje klipp med tal tvättas också automatiskt. Den tvättade versionen
           (<inspelning>/klipp/<klipp>-tvattad.mp4 + .csv + .srt + .xml) är utan hummanden, utfyllnadsord,
           upprepningar och långa pauser. Jobbfilen flyttas till jobb/klara/.
        Varje klart jobb blir en rad i projektets logg.md. --once kör ett varv och slutar.
status  visar vad som väntar och vad som är klart, per projekt.
wash    tvättar ett klipp direkt (kräver <grundnamn>.words.json i inspelningens transkript/).
batch   skriver ut och tvättar alla klipp i en lokal mapp till <utmapp>/transkript/ och <utmapp>/klipp/,
        utan Drive och utan AI. Används i den lokala arbetsmappen innan resultatet läggs i Drive.

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
MIN_WORDS = 15   # klipp med minst så många ord tvättas automatiskt
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


def pending_washes(rec: Path):
    """Klipp med tal (minst MIN_WORDS ord) som saknar en tvättad version."""
    todo = []
    for c in clips(rec):
        words_f = rec / "transkript" / (c.stem + ".words.json")
        if (rec / "klipp" / f"{c.stem}-tvattad.mp4").exists() or not words_f.exists():
            continue
        if len(json.loads(words_f.read_text(encoding="utf-8"))) >= MIN_WORDS:
            todo.append(c)
    return todo


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


def wash(clip: Path, out: Path | None = None, words_f: Path | None = None, render: bool = True):
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
    # skarvarna på hela bildrutor, så att bild, ljud och tidkodskartan stämmer exakt
    fps = float(info["rate"])
    snap = lambda s: round(s * fps) / fps
    keep = [(snap(a), snap(b)) for a, b in keep if snap(b) > snap(a)]

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
    Path(f"{base}.srt").write_text(washed_srt(words, keep), encoding="utf-8")
    if render:
        render_washed(clip, keep, Path(f"{base}.mp4"))
    removed = info["dur"] - pos
    return {"klipp": clip.name, "behallna": len(keep), "bort": len(cuts), "sekunder_bort": round(removed, 1),
            "csv": f"{base}.csv", "xml": f"{base}.xml", "mp4": f"{base}.mp4" if render else ""}


def to_washed(t: float, keep):
    """Rå tid -> tid i den tvättade versionen, eller None om tiden är bortklippt."""
    pos = 0.0
    for a, b in keep:
        if a <= t <= b:
            return pos + t - a
        pos += b - a
    return None


def washed_srt(words, keep, max_words=8, gap=0.6):
    """Undertexter till den tvättade versionen: de behållna orden, med tvättade tider."""
    lines, cur = [], []
    for w in words:
        s, e = to_washed(w["start"], keep), to_washed(w["end"], keep)
        if s is None or e is None:
            continue
        if cur and (len(cur) >= max_words or s - cur[-1][1] > gap or cur[-1][2].rstrip().endswith((".", "?", "!"))):
            lines.append(cur); cur = []
        cur.append((s, e, w["word"]))
    if cur:
        lines.append(cur)
    ts = lambda t: f"{int(t // 3600):02}:{int(t % 3600 // 60):02}:{int(t % 60):02},{int(round(t % 1 * 1000)) % 1000:03}"
    return "".join(f"{n}\n{ts(l[0][0])} --> {ts(l[-1][1])}\n{''.join(x[2] for x in l).strip()}\n\n"
                   for n, l in enumerate(lines, 1))


def render_washed(clip: Path, keep, mp4: Path):
    """Renderar den tvättade versionen som ett sammanhängande klipp, i råfilens upplösning och bildfrekvens.

    En enda genomläsning med select/aselect (ingen buffring av bitarna), HEVC 10-bit med Intel Quick Sync
    om det finns, annars libx265. Skrivs till .part och döps om när den är klar."""
    expr = "+".join(f"between(t,{a:.4f},{b - 0.0005:.4f})" for a, b in keep)
    graph = (f"[0:v]select='{expr}',setpts=N/FRAME_RATE/TB[v];"
             f"[0:a]aselect='{expr}',asetpts=N/SR/TB[a]")
    script = mp4.with_suffix(".filter.txt")
    script.write_text(graph, encoding="utf-8")
    part = mp4.with_name(mp4.stem + ".part.mp4")
    enc = (["-c:v", "hevc_qsv", "-profile:v", "main10", "-pix_fmt", "p010le", "-b:v", "50M", "-maxrate", "60M", "-bufsize", "100M"]
           if encoder_ok("hevc_qsv") else ["-c:v", "libx265", "-pix_fmt", "yuv420p10le", "-crf", "18", "-preset", "fast"])
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(clip), "-/filter_complex", str(script),
           "-map", "[v]", "-map", "[a]", *enc, "-tag:v", "hvc1", "-c:a", "aac", "-b:a", "320k",
           "-map_metadata", "0", "-movflags", "+faststart", str(part)]
    try:
        subprocess.run(cmd, check=True)
        os.replace(part, mp4)
    finally:
        script.unlink(missing_ok=True)
        part.unlink(missing_ok=True)


_enc = {}
def encoder_ok(name: str):
    if name not in _enc:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc2=s=256x256:d=0.2",
                            "-c:v", name, "-pix_fmt", "p010le", "-f", "null", "-"], capture_output=True)
        _enc[name] = r.returncode == 0
    return _enc[name]


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


# ---------- lokalt ----------

def batch(src: Path, out: Path):
    """Skriver ut och tvättar alla videoklipp i en lokal mapp, utan Drive och utan AI.

    Utskrift till <out>/transkript/, tvättade versioner till <out>/klipp/. Det som redan finns hoppas över."""
    todo = sorted(p for p in src.rglob("*") if p.suffix.lower() in VIDEO and not p.name.endswith(".part"))
    tr, kl = out / "transkript", out / "klipp"
    for n, clip in enumerate(todo, 1):
        t0 = time.time()
        words_f = tr / (clip.stem + ".words.json")
        if not words_f.exists():
            subprocess.run([sys.executable, str(TRANSCRIBE), str(clip), str(tr), "--words"], check=False)
        if not words_f.exists():
            print(f"{n}/{len(todo)} {clip.name}: utskriften misslyckades", flush=True)
            continue
        words = json.loads(words_f.read_text(encoding="utf-8"))
        if len(words) < MIN_WORDS:
            print(f"{n}/{len(todo)} {clip.name}: {len(words)} ord, tvättas inte ({time.time() - t0:.0f} s)", flush=True)
            continue
        if not (kl / f"{clip.stem}-tvattad.mp4").exists():
            r = wash(clip, kl, words_f)
            print(f"{n}/{len(todo)} {clip.name}: {len(words)} ord, {r['sekunder_bort']} s bort ({time.time() - t0:.0f} s)", flush=True)
    print(f"{now()} klart: {len(todo)} klipp i {src}", flush=True)


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
            washed = []
            for clip in pending_washes(rec):
                try:
                    r = wash(clip)
                except Exception as e:  # görs om nästa varv
                    print(f"{clip.name}: {e}", flush=True)
                    continue
                washed.append(f"{r['klipp']} ({r['sekunder_bort']} s bort)")
            if washed:
                log(project, f"Tvätt: {rec.name}, {len(washed)} klipp med tal, tvättade versioner i klipp/ ({', '.join(washed[:5])}{' …' if len(washed) > 5 else ''})")
                done += len(washed)
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
    b = sub.add_parser("batch"); b.add_argument("src", type=Path); b.add_argument("out", type=Path)
    a = ap.parse_args()
    if a.cmd == "batch":
        batch(a.src, a.out)
    elif a.cmd == "status":
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
