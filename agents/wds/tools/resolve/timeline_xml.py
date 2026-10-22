"""Bygger en startfil för DaVinci Resolve (FCP 7 XML) ur ett projekts katalog, utan Resolve och utan skript-API.

    python timeline_xml.py "<delad enhet>/projects/<projekt>" [--out <fil.xml>] [--still 4] [--with-rejects]

Läser varje inspelnings innehall.csv och skriver en fil med flera tidslinjer:
  - en per inspelning: foton (JPEG) och klipp i tidsordning, utan dem som föreslås bort
  - favoriter: alla filer med favorit = ja, i tidsordning
  - talen, tvättade: de tvättade versionerna i <inspelning>/klipp/
Varje foto och klipp får en markör med katalogens beskrivning. Mediet länkas där det ligger, inget kopieras.
I Resolve: File → Import → Timeline, välj filen. Utskrifterna (<klipp>.srt) dras in som undertextspår.

Standard ut-fil: <projekt>/resolve/<projekt>-start.xml.
"""
import argparse, csv, json, subprocess, sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

PHOTO = {".jpg", ".jpeg"}
VIDEO = {".mp4", ".mov"}


@lru_cache(maxsize=None)
def probe(path: Path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", str(path)],
                       capture_output=True, text=True)
    info = json.loads(r.stdout or "{}")
    v = next((s for s in info.get("streams", []) if s["codec_type"] == "video"), {})
    a = next((s for s in info.get("streams", []) if s["codec_type"] == "audio"), None)
    return {"w": int(v.get("width", 0)), "h": int(v.get("height", 0)),
            "rate": Fraction(v.get("r_frame_rate", "25/1")), "dur": float(info.get("format", {}).get("duration", 0)),
            "audio": int(a["channels"]) if a else 0}


def url(p: Path):
    return "file://localhost/" + quote(p.resolve().as_posix(), safe="/:")


class Seq:
    def __init__(self, name, rate, w, h):
        self.name, self.rate, self.w, self.h = name, rate, w, h
        self.v, self.a, self.markers, self.pos = [], [], [], 0

    def fr(self, s):
        return int(round(s * float(self.rate)))

    def ratex(self):
        ntsc = "TRUE" if self.rate.denominator == 1001 else "FALSE"
        return f"<rate><timebase>{round(float(self.rate))}</timebase><ntsc>{ntsc}</ntsc></rate>"

    def add(self, path: Path, files: dict, still: float, note: str):
        is_photo = path.suffix.lower() in PHOTO
        # foton från samma källa har samma format: läs ett per mapp i stället för varje fil över Drive
        info = probe(next(iter(sorted(path.parent.glob("*" + path.suffix))), path)) if is_photo else probe(path)
        length = self.fr(still) if is_photo else max(1, self.fr(info["dur"]))
        first = str(path) not in files   # filen beskrivs en gång i hela projektet, sedan bara med id
        fid = files.setdefault(str(path), f"file-{len(files) + 1}")
        media = (f"<media><video><samplecharacteristics><width>{info['w']}</width><height>{info['h']}</height>"
                 f"</samplecharacteristics></video>"
                 + (f"<audio><channelcount>{info['audio']}</channelcount></audio>" if info["audio"] else "") + "</media>")
        fx = (f'<file id="{fid}"><name>{escape(path.name)}</name><pathurl>{url(path)}</pathurl>{self.ratex()}'
              f"<duration>{length}</duration>{media}</file>") if first else f'<file id="{fid}"/>'
        n = len(self.v) + 1
        self.v.append(f'<clipitem id="v{n}"><name>{escape(path.name)}</name>{self.ratex()}<start>{self.pos}</start>'
                      f"<end>{self.pos + length}</end><in>0</in><out>{length}</out>{fx}</clipitem>")
        if info["audio"]:
            self.a.append(f'<clipitem id="a{n}"><name>{escape(path.name)}</name>{self.ratex()}<start>{self.pos}</start>'
                          f'<end>{self.pos + length}</end><in>0</in><out>{length}</out><file id="{fid}"/>'
                          "<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack></clipitem>")
        if note:
            self.markers.append(f"<marker><name>{escape(path.stem)}</name><comment>{escape(note)}</comment>"
                                f"<in>{self.pos}</in><out>-1</out></marker>")
        self.pos += length

    def xml(self):
        fmt = (f"<format><samplecharacteristics>{self.ratex()}<width>{self.w}</width><height>{self.h}</height>"
               "</samplecharacteristics></format>")
        return (f"<sequence><name>{escape(self.name)}</name>{self.ratex()}<duration>{self.pos}</duration>"
                f"{''.join(self.markers)}<media><video>{fmt}<track>{''.join(self.v)}</track></video>"
                f"<audio><track>{''.join(self.a)}</track></audio></media></sequence>")


def rows(rec: Path):
    f = rec / "innehall.csv"
    return list(csv.DictReader(open(f, encoding="utf-8-sig"))) if f.exists() else []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--still", type=float, default=4.0, help="sekunder per foto i tidslinjen")
    ap.add_argument("--with-rejects", action="store_true", help="ta med filer som föreslås bort")
    a = ap.parse_args()
    proj = a.project
    # inspelningarna i den ordning de spelades in (första tagen-tiden i katalogen), inte i bokstavsordning
    recs = sorted((p for p in proj.iterdir() if p.is_dir() and (p / "original").is_dir()),
                  key=lambda r: min((x["tagen"] for x in rows(r)), default=r.name))
    # tidslinjens format = det vanligaste videoklippets
    sample = next((v for r in recs for v in (r / "original").rglob("*") if v.suffix.lower() in VIDEO), None)
    base = probe(sample) if sample else {"rate": Fraction(25), "w": 3840, "h": 2160}
    files, seqs, favs = {}, [], []
    for rec in recs:
        s = Seq(rec.name, base["rate"], base["w"], base["h"])
        for r in sorted(rows(rec), key=lambda r: (r["tagen"], r["fil"])):
            p = rec / "original" / r["kalla"] / r["fil"]
            if p.suffix.lower() not in PHOTO | VIDEO or not p.exists():
                continue
            note = f"{r['beskrivning']} · betyg {r['betyg']}" + (" · favorit" if r.get("favorit") == "ja" else "")
            if r.get("favorit") == "ja":
                favs.append((r["tagen"], p, note))
            if r.get("forslag") == "bort" and not a.with_rejects:
                continue
            s.add(p, files, a.still, note)
        if s.v:
            seqs.append(s)
    if favs:
        s = Seq("favoriter", base["rate"], base["w"], base["h"])
        for _, p, note in sorted(favs, key=lambda x: x[0]):
            s.add(p, files, a.still, note)
        seqs.append(s)
    washed = sorted(p for rec in recs for p in (rec / "klipp").glob("*-tvattad.mp4"))
    if washed:
        s = Seq("talen, tvättade", base["rate"], base["w"], base["h"])
        for p in washed:
            s.add(p, files, a.still, f"{p.parent.parent.name}: tvättad version av {p.name.split('-tvattad')[0]}")
        seqs.append(s)
    out = a.out or proj / "resolve" / f"{proj.name}-start.xml"
    out.parent.mkdir(parents=True, exist_ok=True)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="5">'
           f"<project><name>{escape(proj.name)}</name><children>{''.join(s.xml() for s in seqs)}</children></project></xmeml>\n")
    out.write_text(xml, encoding="utf-8")
    for s in seqs:
        print(f"{s.name}: {len(s.v)} filer, {s.pos / float(s.rate) / 60:.1f} min")
    print(f"Skrivet: {out}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
