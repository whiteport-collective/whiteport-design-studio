"""Inspelningens Resolve-dokument: de godtagbara bilderna och de rimliga klippen, med balanserad färg och stjärnor,
för personens godkännande (grön flagga). Sparas som <datum>-<plats>.drp i inspelningsmappen.

    python shoot_document.py "<delad enhet>/projects/<projekt>/<datum>-<plats>" [--limit N] [--replace]

Underlaget är inspelningens innehall.csv från katalogen (media-catalog): en rad per fil med betyg 1–5 och
forslag "bort" för det uppenbart dåliga. Bortvalda filer läggs inte i Resolve.

  - Ett Resolve-projekt med inspelningens namn (2026-10-22-linnesalen). Finns det öppnas det, och bara det som
    saknas läggs till; --replace gör om det från början.
  - Binarna foto och video, med en underbin per person och kamera (marten-lumix-s9).
  - Bilderna: RAW när den finns (RW2, DNG, CR3, NEF, ARW), annars JPEG/HEIC. Klippen: alla som inte är bortvalda.
  - Metadata: beskrivning, nyckelord, bedömningen som kommentar, och betyget som stjärnor (Rating 1–5).
  - Bilderna stannar i RAW i binen, för granskning, stjärnor och grön flagga (Mårten, 2026-10-24); Resolve kan inte
    visa Lumix S9:s RW2 på en tidslinje. En bild som ska användas på en tidslinje exporteras först till ett format
    som fungerar där, och då balanseras färgen.
  - Tidslinjen video i tagningsordning, med en balanserad färg per klipp på nod 1: utjämning och ljusets karaktär
    (looks.character: lysrör och dagsljus lite sterilt, glödljus varmare), mätt på proxyn och sparad som
    <klipp>/<klipp>.cube i mappen bredvid klippet.
  - Projektet sparas och exporteras som <inspelning>/<inspelning>.drp.
--limit N  bara de N första bilderna och klippen (för att prova).
"""
import argparse, csv, math, os, shutil, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import looks  # noqa: E402

RAW = {".rw2", ".dng", ".cr3", ".cr2", ".nef", ".arw", ".raf", ".orf"}
PHOTO = RAW | {".jpg", ".jpeg", ".heic", ".hif", ".png", ".tif", ".tiff"}
VIDEO = {".mp4", ".mov", ".mts", ".m2ts", ".mxf"}
SKIP_DIRS = {"klipp", "export", "mediabank", "inkorg", "resolve", "transkript"}


def resolve_app():
    api = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
    sys.path.append(str(api / "Modules"))
    import DaVinciResolveScript as dvr
    for _ in range(60):
        r = dvr.scriptapp("Resolve")
        if r:
            return r
        time.sleep(5)
    sys.exit("Resolve svarar inte (Studio, External scripting = Local)")


def originals(shoot: Path):
    """Originalen i inspelningen: filer direkt i kameramapparna, inte i en fils egen mapp eller i klipp/, export/ …"""
    out = []
    for p in shoot.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in PHOTO | VIDEO:
            continue
        rel = p.relative_to(shoot).parts
        if any(x in SKIP_DIRS for x in rel[:-1]) or ".proxy." in p.name or "-tvattad" in p.name or p.name.endswith(".part"):
            continue
        if p.parent.name == p.stem or p.name.startswith(p.parent.name + "."):
            continue
        out.append(p)
    return sorted(out)


def source_of(shoot: Path, p: Path) -> str:
    """person-kamera ur sökvägen: <person>/<kamera>/ (ny struktur) eller original/<person>-<kamera>/ (förra)."""
    parts = p.relative_to(shoot).parts[:-1]
    parts = [x for x in parts if x != "original"]
    return "-".join(parts) or "okand"


def lut_path(p: Path) -> Path:
    return p.parent / p.stem / f"{p.stem}.cube"


def make_lut(p: Path, measure_src: Path) -> Path:
    """Balanserad färg för en fil: utjämning och ljusets karaktär, i mappen bredvid filen."""
    lut = lut_path(p)
    if lut.exists():
        return lut
    try:
        rgb = looks.measure(measure_src)
    except Exception:
        rgb = [0.4, 0.4, 0.4]
    rb = math.log(max(rgb[0], 1e-3) / max(rgb[2], 1e-3))
    lut.parent.mkdir(exist_ok=True)
    looks.write_cube(lut, looks.gains(rgb), looks.LOOKS[looks.character(rb)])
    return lut


def lut_rel(project: str, lut: Path) -> str:
    """Resolve tar bara LUT:ar i sin egen LUT-mapp: kopiera dit och använd relativ sökväg."""
    master = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/LUT" / project
    master.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(lut, master / lut.name)
    return f"{project}/{lut.name}"


def sub(mp, parent, name):
    return next((f for f in parent.GetSubFolderList() if f.GetName() == name), None) or mp.AddSubFolder(parent, name)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shoot", type=Path)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args()
    shoot, name = a.shoot, a.shoot.name

    cat = {}
    if (shoot / "innehall.csv").exists():
        with open(shoot / "innehall.csv", encoding="utf-8-sig", newline="") as f:
            cat = {r["fil"]: r for r in csv.DictReader(f)}
    files = originals(shoot)
    rejected = {Path(k).stem for k, r in cat.items() if r.get("forslag", "").strip().lower() == "bort"}

    photos, by_stem = [], {}
    for p in files:
        if p.suffix.lower() in PHOTO:
            by_stem.setdefault((p.parent, p.stem), []).append(p)
    for (_, stem), ps in sorted(by_stem.items(), key=lambda kv: kv[0][1]):
        if stem in rejected:
            continue
        raw = [p for p in ps if p.suffix.lower() in RAW]
        jpg = [p for p in ps if p.suffix.lower() not in RAW]
        photos.append((raw[0] if raw else jpg[0], jpg[0] if jpg else (raw[0] if raw else None)))
    clips = [p for p in files if p.suffix.lower() in VIDEO and p.stem not in rejected]
    if a.limit:
        photos, clips = photos[:a.limit], clips[:a.limit]
    print(f"{name}: {len(photos)} bilder och {len(clips)} klipp till Resolve, {len(rejected)} bortvalda filnamn rörs inte", flush=True)

    luts = {}
    for c in clips:
        luts[c] = make_lut(c, looks.src_for(c))
    print(f"  färg mätt för {len(luts)} klipp", flush=True)

    r = resolve_app()
    pm = r.GetProjectManager()
    cur = pm.GetCurrentProject()
    if cur:
        pm.SaveProject()
    if a.replace and name in (pm.GetProjectListInCurrentFolder() or []):
        pm.CloseProject(pm.GetCurrentProject()) if cur and cur.GetName() == name else None
        pm.DeleteProject(name)
    project = pm.LoadProject(name) or pm.CreateProject(name)
    if not project:
        sys.exit(f"projektet {name} gick inte att skapa eller öppna i Resolve")
    # cachen följer projektet, inte datorn: varje nytt projekt får datorns cachemapp (på Surface Pro 7 den externa disken)
    cache = Path(os.environ.get("WDS_RESOLVE_CACHE", r"E:\DaVinci Resolve Cache"))
    if cache.exists():
        for k, sub_ in (("perfCacheClipsLocation", "CacheClip"), ("colorGalleryStillsLocation", "gallery"), ("projectMediaLocation", "media")):
            (cache / sub_).mkdir(exist_ok=True)
            project.SetSetting(k, str(cache / sub_))
    mp, storage = project.GetMediaPool(), r.GetMediaStorage()
    root = mp.GetRootFolder()

    rels = {p: lut_rel(name, l) for p, l in luts.items()}
    project.RefreshLUTList()
    items = {}
    for kind, paths in (("foto", [p for p, _ in photos]), ("video", clips)):
        top = sub(mp, root, kind)
        for src in sorted({source_of(shoot, p) for p in paths}):
            b = sub(mp, top, src)
            mine = [p for p in paths if source_of(shoot, p) == src]
            have = {c.GetClipProperty("File Name"): c for c in b.GetClipList()}
            mp.SetCurrentFolder(b)
            new = [str(p) for p in mine if p.name not in have]
            for i in range(0, len(new), 50):
                storage.AddItemListToMediaPool(new[i:i + 50])
            have = {c.GetClipProperty("File Name"): c for c in b.GetClipList()}
            for p in mine:
                if p.name in have:
                    items[p] = have[p.name]

    for p, clip in items.items():
        row = cat.get(p.name) or cat.get(p.with_suffix(".JPG").name) or {}
        md = {"Description": row.get("beskrivning", "")[:250],
              "Keywords": row.get("nyckelord", "").replace(";", ","),
              "Comments": f"Teknik {row.get('teknik', '-')}: {row.get('teknik_kommentar', '')} Konst {row.get('konst', '-')}: {row.get('konst_kommentar', '')}"[:250]}
        clip.SetMetadata(md)
        if row.get("betyg", "").strip().isdigit():
            clip.SetMetadata("Rating", row["betyg"].strip())

    for kind, paths in (("video", clips),):
        tl_items = [items[p] for p in paths if p in items]
        if not tl_items:
            continue
        tl = next((project.GetTimelineByIndex(i) for i in range(1, project.GetTimelineCount() + 1)
                   if project.GetTimelineByIndex(i).GetName() == kind), None)
        if not tl:
            mp.SetCurrentFolder(root)                      # tidslinjerna överst, inte i en bin
            tl = mp.CreateEmptyTimeline(kind)
            project.SetCurrentTimeline(tl)
            mp.AppendToTimeline(tl_items)
        project.SetCurrentTimeline(tl)
        by_name = {Path(p).name: p for p in paths}
        done = 0
        for ti in tl.GetItemListInTrack("video", 1) or []:
            mpi = ti.GetMediaPoolItem()
            p = by_name.get(mpi.GetClipProperty("File Name")) if mpi else None
            if p and ti.SetLUT(1, rels[p]):
                done += 1
        print(f"  tidslinjen {kind}: {len(tl.GetItemListInTrack('video', 1) or [])} filer, färg på {done}", flush=True)

    pm.SaveProject()
    drp = shoot / f"{name}.drp"
    ok = pm.ExportProject(name, str(drp))
    print(f"  sparat: {drp.name if ok else 'exporten misslyckades'}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
