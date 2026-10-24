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
--apply    lägger LUT:en på nod 1 för varje klipp i projektets tidslinjer i Resolve Studio (TimelineItem.SetLUT).
           LUT:arna kopieras till Resolves LUT-mapp (<ProgramData>/.../Support/LUT/<projekt>/), annars vägrar SetLUT.
--apply-only  lägger på befintliga LUT:ar utan att mäta om
--neutral  bara utjämningen, inget utseende, och LUT:en läggs bredvid klippet som <klipp>.cube (mottagningen, mediebanken).
           Utseendet läggs sedan ovanpå i Resolve eller som ett andra steg i ffmpeg.
"""
import argparse, array, json, math, os, shutil, subprocess, sys
from pathlib import Path

VIDEO = {".mp4", ".mov", ".mxf", ".mts"}
STRENGTH, TARGET_Y = 0.55, 0.42
N = 33

LOOKS = {
    # temp: + varmt (R upp, B ned) i högdagrarna och mitten; lift: skuggornas golv; contrast: mitten-kontrast;
    # sat: mättnad; clean: hur mycket nästan vita ytor dras mot neutralt vitt (rena kockrockar)
    "varm": {"temp_hi": 0.03, "temp_mid": 0.03, "temp_lo": 0.01, "lift": 0.02, "contrast": 1.0, "sat": 1.08, "clean": 0.35, "roll": 0.98},
    "frisk-varm": {"temp_hi": 0.025, "temp_mid": 0.05, "temp_lo": 0.0, "lift": 0.02, "contrast": 1.06, "sat": 1.14, "clean": 0.6, "roll": 0.985},
    # bara utjämningen, inget utseende: materialet i mottagningen och klippen till mediebanken (Mårten, 2026-10-24)
    # karaktär efter ljuset i en zon (Mårten, 2026-10-24): kök med lysrör lite sterilt, restaurang med glödljus tydligt varmare
    "steril": {"temp_hi": -0.01, "temp_mid": -0.005, "temp_lo": 0.0, "lift": 0.0, "contrast": 1.04, "sat": 1.0, "clean": 0.6, "roll": 0.99},
    "restaurang": {"temp_hi": 0.05, "temp_mid": 0.07, "temp_lo": 0.025, "lift": 0.02, "contrast": 1.03, "sat": 1.12, "clean": 0.3, "roll": 0.98},
    "neutral": {"temp_hi": 0.0, "temp_mid": 0.0, "temp_lo": 0.0, "lift": 0.0, "contrast": 1.0, "sat": 1.0, "clean": 0.0, "roll": 1.0},
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


def gains(rgb, max_expo=1.3):
    r, g, b = rgb
    gray = (r + g + b) / 3
    wb = [min(1.5, max(0.7, (gray / max(c, 1e-3)) ** STRENGTH)) for c in rgb]
    luma = lambda gs: 0.2126 * r * gs[0] + 0.7152 * g * gs[1] + 0.0722 * b * gs[2]
    keep = luma([1, 1, 1]) / max(luma(wb), 1e-3)
    wb = [x * keep for x in wb]
    expo = min(max_expo, max(0.9, (TARGET_Y / max(luma(wb), 1e-3)) ** 0.6))
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


def character(rb: float) -> str:
    """Karaktär efter ljusets färg i originalet (log R/B): lysrör och dagsljus blir sterilt, glödljus varmt."""
    return "restaurang" if rb > 0.3 else "steril" if rb < 0.15 else "neutral"


def light_segments(clip: Path, t_in: float, t_out: float, fps=2, jump=0.18, min_len=2.0, max_fade=4.0):
    """Ljuszoner i klippet mellan t_in och t_out, när ljuset skiftar (kök med lysrör, sal med glödljus):
    [(start, slut, gains)], där varje övergång är tiden mellan två zoner (en övertoning läggs där).
    Färgtemperaturen följs som log(R/B) i två bilder per sekund. Mörka partier (en dörröppning) blir egna zoner
    med kraftigare exponering, så att de lättas upp (Mårten, 2026-10-24)."""
    src = src_for(clip)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t_in}", "-t", f"{t_out - t_in}", "-i", str(src),
                          "-vf", f"fps={fps},scale=96:64", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr, samples = 96 * 64 * 3, []
    for k in range(len(raw) // fr):
        a = array.array("B", raw[k * fr:(k + 1) * fr]); n = len(a) // 3
        rgb = [sum(a[c::3]) / n / 255 for c in range(3)]
        y = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
        samples.append((t_in + k / fps, rgb, math.log(max(rgb[0], 1e-3) / max(rgb[2], 1e-3)), y > 0.25))
    # en ny zon när färgtemperaturen hoppar eller när det blir mörkt (en dörröppning, en korridor) eller ljust igen
    zones, cur = [], []
    for s in samples:
        ref = sorted(x[2] for x in cur if x[3])[len([x for x in cur if x[3]]) // 2] if any(x[3] for x in cur) else s[2]
        if cur and (s[3] != cur[-1][3] or (s[3] and abs(s[2] - ref) > jump)):
            zones.append(cur); cur = []
        cur.append(s)
    if cur:
        zones.append(cur)
    # korta ljusa zoner (övergångar) slås ihop med grannen; mörka zoner behålls från en halv sekund, för att lättas upp
    keep = [z for z in zones if (z[-1][0] - z[0][0] + 1 / fps) >= (0.5 if not z[0][3] else min_len)]
    zones = keep or [max(zones, key=len)]
    out = []
    for i, z in enumerate(zones):
        rgb = [sum(s[1][c] for s in z) / len(z) for c in range(3)]
        dark = not z[0][3]
        pad = 0.4 if dark else 0.0                         # mörka zoner breddas, så att upplättningen går mjukt upp och ned
        out.append([t_in if i == 0 else None, z[0][0] - pad, z[-1][0] + 1 / fps + pad, gains(rgb, 1.8 if dark else 1.3),
                    sum(s[2] for s in z) / len(z), dark])
    segs = []
    for i, (start, first, last, gn, rb, dark) in enumerate(out):
        if i:
            gap = first - out[i - 1][2]                    # tiden mellan zonerna: där skiftar ljuset
            cut = (first + out[i - 1][2]) / 2
            prev_len = cut - segs[-1][0]
            next_len = (out[i + 1][1] if i + 1 < len(out) else t_out) - cut
            fade = min(max_fade, max(2.0, gap), 0.8 * prev_len, 0.8 * next_len)   # aldrig längre än zonerna själva
            segs[-1][1] = cut
            segs[-1][3] = round(fade, 2)
            start = cut
        segs.append([start, t_out, gn, 0.0, rb, dark])
    return [tuple(s) for s in segs]          # (start, slut, gains, övertoning till nästa zon, log R/B, mörk)


def neutral_cube(clip: Path) -> Path:
    """Utjämningen för ett klipp, bredvid klippet: <klipp>.cube. Mäts och skrivs om den saknas."""
    lut = clip.with_suffix(".cube")
    if not lut.exists():
        write_cube(lut, gains(measure(src_for(clip))), LOOKS["neutral"])
    return lut


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
    # Resolve tar bara LUT:ar som ligger i dess LUT-mapp: kopiera dit och använd relativ sökväg
    master = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/LUT" / project_dir.name
    rel = {}
    for name, lut in luts.items():
        dst = master / lut.parent.name / lut.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(lut, dst)
        rel[name] = f"{project_dir.name}/{lut.parent.name}/{lut.name}"
    project.RefreshLUTList()
    done = 0
    for i in range(project.GetTimelineCount()):
        tl = project.GetTimelineByIndex(i + 1)
        for item in tl.GetItemListInTrack("video", 1) or []:
            mpi = item.GetMediaPoolItem()
            path = mpi.GetClipProperty("File Path") if mpi else ""
            lut = rel.get(Path(path).name)
            if lut and item.SetLUT(1, lut):
                done += 1
    resolve.GetProjectManager().SaveProject()
    print(f"LUT lagd på {done} klipp i tidslinjerna")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--map", default="*=neutral", help='"2026-10-22-koket=frisk-varm,*=varm"')
    ap.add_argument("--neutral", action="store_true", help="bara utjämning, LUT:en bredvid klippet")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", help="bara dessa inspelningar, kommaseparerat")
    ap.add_argument("--apply-only", action="store_true", help="lägg på befintliga LUT:ar utan att mäta om")
    a = ap.parse_args()
    mapping = dict(x.split("=") for x in a.map.split(","))
    lutdir = a.project / "resolve" / "lut"
    luts, log = {}, {}
    if a.apply_only:
        for lut in lutdir.glob("*/*.cube"):
            for clip in (a.project / lut.parent.name / "original").rglob(lut.stem + ".*"):
                if clip.suffix.lower() in VIDEO and ".proxy." not in clip.name:
                    luts[clip.name] = lut
        apply(a.project, luts)
        return
    recs = [p for p in sorted(a.project.iterdir()) if p.is_dir() and (p / "original").is_dir()]
    if a.only:
        recs = [r for r in recs if r.name in a.only.split(",")]
    for rec in recs:
        look = "neutral" if a.neutral else mapping.get(rec.name, mapping.get("*", "varm"))
        items = []
        for clip in sorted(p for p in (rec / "original").rglob("*") if p.suffix.lower() in VIDEO
                           and ".proxy." not in p.name and "-tvattad" not in p.name):
            rgb = measure(src_for(clip))
            gn = gains(rgb)
            lut = clip.with_suffix(".cube") if a.neutral else lutdir / rec.name / f"{clip.stem}.cube"
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
