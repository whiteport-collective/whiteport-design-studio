"""Färgsättning i två steg per klipp, som LUT-filer: utjämning (vitbalans och exponering) och ett utseende.

    python looks.py "<delad enhet>/projects/<projekt>" --map "<inspelning>=<utseende>,..." [--preview] [--apply]

Steg 1, utjämning: medel-R, G, B och luminans mäts på fem bilder ur klippet (proxyfilen <klipp>.proxy.mov
om den finns, annars originalet). Kanalerna dras mot neutralt grått (STRENGTH) och ljusheten mot TARGET_Y,
med tak så att en svag kanal inte förstärks till brus.
Steg 2, utseendet (LOOKS nedan), till exempel:
  varm        varm och härlig: gyllene högdagrar, mjukt lyfta skuggor, mjukare kontrast, lite mer färg
  frisk-varm  fräsch fast varm: rena vita, varm hud och mat, stål som går mot varmt, mer klarhet
Båda stegen bakas ihop till en LUT per klipp: <projekt>/resolve/lut/<inspelning>/<klipp>.cube (33³).
--preview  skriver en före/efter-bild per inspelning till <projekt>/resolve/lut/<inspelning>-fore-efter.jpg
--apply    lägger LUT:en på nod 1 för varje klipp i projektets tidslinjer i Resolve Studio (TimelineItem.SetLUT)
"""
import argparse, array, json, math, os, subprocess, sys
from pathlib import Path

VIDEO = {".mp4", ".mov", ".mxf", ".mts"}
STRENGTH, TARGET_Y = 0.55, 0.42
N = 33

LOOKS = {
    # temp: + varmt (R upp, B ned) i högdagrarna och mitten; lift: skuggornas golv; contrast: mitten-kontrast;
    # sat: mättnad; clean: hur mycket nästan vita ytor dras mot neutralt vitt (rena kockrockar)
    "varm": {"temp_hi": 0.03, "temp_mid": 0.03, "temp_lo": 0.01, "lift": 0.02, "contrast": 1.0, "sat": 1.08, "clean": 0.35, "roll": 0.98},
    "frisk-varm": {"temp_hi": 0.025, "temp_mid": 0.05, "temp_lo": 0.0, "lift": 0.02, "contrast": 1.06, "sat": 1.14, "clean": 0.6, "roll": 0.985},
}


def src_for(clip: Path):
    px = clip.with_name(clip.stem + ".proxy.mov")
    if px.exists():
        return px
    local = Path.home() / "Pictures" / "wds-arbete" / clip.parents[2].parent.name / "proxy" / clip.parents[2].name
    for cand in (local / (clip.stem + ".proxy.mov"), local / (clip.stem + ".mov")):
        if cand.exists():
            return cand
    return clip


def measure(p: Path):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                             capture_output=True, text=True).stdout.strip() or 1)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"fps=5/{max(d, 0.5)},scale=96:64",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    a = array.array("B", raw); n = len(a) // 3 or 1
    return [sum(a[c::3]) / n / 255 for c in range(3)]


def gains(rgb):
    r, g, b = rgb
    gray = (r + g + b) / 3
    wb = [min(1.5, max(0.7, (gray / max(c, 1e-3)) ** STRENGTH)) for c in rgb]
    luma = lambda gs: 0.2126 * r * gs[0] + 0.7152 * g * gs[1] + 0.0722 * b * gs[2]
    keep = luma([1, 1, 1]) / max(luma(wb), 1e-3)
    wb = [x * keep for x in wb]
    expo = min(1.3, max(0.9, (TARGET_Y / max(luma(wb), 1e-3)) ** 0.6))
    return [min(1.9, x * expo) for x in wb]


def look_fn(L):
    def f(r, g, b):
        y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        # tonkurva: mjukt lyft golv, kontrast kring mitten, mjuk rullning i toppen
        def tone(v):
            v = L["lift"] + (1 - L["lift"]) * v
            v = 0.5 + (v - 0.5) * L["contrast"]
            v = v if v < 0.8 else 0.8 + (v - 0.8) * L["roll"] / (1 + (v - 0.8) * 0.5)
            return min(1.0, max(0.0, v))
        r, g, b = tone(r), tone(g), tone(b)
        # värme fördelad på skuggor, mitten och högdagrar
        hi, lo = max(0.0, (y - 0.5) * 2), max(0.0, (0.5 - y) * 2)
        mid = 1 - hi - lo
        t = L["temp_hi"] * hi + L["temp_mid"] * mid + L["temp_lo"] * lo
        r, g, b = r * (1 + t), g * (1 + t * 0.35), b * (1 - t)
        # mättnad
        y2 = 0.2126 * r + 0.7152 * g + 0.0722 * b
        r, g, b = (y2 + (c - y2) * L["sat"] for c in (r, g, b))
        # rena vita: nästan vita ytor dras mot neutralt, så att kockrockar och porslin är vita, inte gula
        if L["clean"] and y2 > 0.7:
            k = L["clean"] * min(1.0, (y2 - 0.7) / 0.25)
            r, g, b = (c + (y2 - c) * k for c in (r, g, b))
        return [min(1.0, max(0.0, c)) for c in (r, g, b)]
    return f


def write_cube(path: Path, gn, L):
    f = look_fn(L)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f'TITLE "{path.stem}"', f"LUT_3D_SIZE {N}"]
    for bi in range(N):
        for gi in range(N):
            for ri in range(N):
                r, g, b = ri / (N - 1) * gn[0], gi / (N - 1) * gn[1], bi / (N - 1) * gn[2]
                lines.append("%.6f %.6f %.6f" % tuple(f(min(r, 1.0), min(g, 1.0), min(b, 1.0))))
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def preview(rec: Path, items, out: Path):
    tiles = []
    tmp = out.parent / f".{rec.name}-tmp"; tmp.mkdir(exist_ok=True)
    for i, (clip, lut) in enumerate(items[:6]):
        s = src_for(clip)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(s)],
                                 capture_output=True, text=True).stdout.strip() or 1)
        a, b = tmp / f"{i}a.jpg", tmp / f"{i}b.jpg"
        lutp = str(lut).replace("\\", "/").replace(":", "\\:")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d / 2:.2f}", "-i", str(s), "-frames:v", "1", "-vf", "scale=480:-2", str(a)])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d / 2:.2f}", "-i", str(s), "-frames:v", "1",
                        "-vf", f"scale=480:-2,lut3d='{lutp}'", str(b)])
        tiles += [a, b]
    inputs = sum((["-i", str(t)] for t in tiles), [])
    n = len(tiles) // 2
    layout = "|".join(f"{(k % 2) * 480}_{(k // 2) * 320}" for k in range(len(tiles)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                    f"{''.join(f'[{k}:v]scale=480:320,setsar=1[t{k}];' for k in range(len(tiles)))}"
                    f"{''.join(f'[t{k}]' for k in range(len(tiles)))}xstack=inputs={len(tiles)}:layout={layout}",
                    "-frames:v", "1", str(out)])
    for t in tmp.iterdir():
        t.unlink()
    tmp.rmdir()


def apply(project_dir: Path, luts: dict):
    api = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
    sys.path.append(str(api / "Modules"))
    import DaVinciResolveScript as dvr
    resolve = dvr.scriptapp("Resolve")
    project = resolve.GetProjectManager().LoadProject(project_dir.name)
    done = 0
    for i in range(project.GetTimelineCount()):
        tl = project.GetTimelineByIndex(i + 1)
        for item in tl.GetItemListInTrack("video", 1) or []:
            mpi = item.GetMediaPoolItem()
            path = mpi.GetClipProperty("File Path") if mpi else ""
            lut = luts.get(Path(path).name)
            if lut and item.SetLUT(1, str(lut)):
                done += 1
    resolve.GetProjectManager().SaveProject()
    print(f"LUT lagd på {done} klipp i tidslinjerna")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--map", required=True, help='"2026-10-22-koket=frisk-varm,*=varm"')
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", help="bara dessa inspelningar, kommaseparerat")
    a = ap.parse_args()
    mapping = dict(x.split("=") for x in a.map.split(","))
    lutdir = a.project / "resolve" / "lut"
    luts, log = {}, {}
    recs = [p for p in sorted(a.project.iterdir()) if p.is_dir() and (p / "original").is_dir()]
    if a.only:
        recs = [r for r in recs if r.name in a.only.split(",")]
    for rec in recs:
        look = mapping.get(rec.name, mapping.get("*", "varm"))
        items = []
        for clip in sorted(p for p in (rec / "original").rglob("*") if p.suffix.lower() in VIDEO
                           and ".proxy." not in p.name and "-tvattad" not in p.name):
            rgb = measure(src_for(clip))
            gn = gains(rgb)
            lut = lutdir / rec.name / f"{clip.stem}.cube"
            write_cube(lut, gn, LOOKS[look])
            luts[clip.name] = lut
            items.append((clip, lut))
            log[clip.name] = {"inspelning": rec.name, "utseende": look, "rgb": [round(x, 3) for x in rgb], "gains": [round(x, 3) for x in gn]}
            print(f"{rec.name}/{clip.name}: {look}, förstärkning {gn[0]:.2f}/{gn[1]:.2f}/{gn[2]:.2f}", flush=True)
        if a.preview and items:
            preview(rec, items, lutdir / f"{rec.name}-fore-efter.jpg")
    (lutdir / "looks.json").write_text(json.dumps({"looks": LOOKS, "klipp": log}, ensure_ascii=False, indent=1), encoding="utf-8")
    if a.apply:
        apply(a.project, luts)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
