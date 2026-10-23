"""Lägger in ett projekts media i DaVinci Resolve Studio med skript-API:t, ordnat som i katalogen.

    python import_project.py "<delad enhet>/projects/<projekt>" [--fps 25] [--res 3840x2160]

Kräver Resolve Studio igång och Preferences → System → General → External scripting using: Local.
Miljön sätts av skriptet själv (Windows-sökvägarna nedan).

Skapar (eller öppnar) projektet med mappens namn och, per inspelning i inspelningsordning:
  bin <inspelning>/ med video, foto (JPEG), raw (RW2 m.fl.) och tal-tvattade (klipp/*-tvattad.mp4)
Varje klipp får katalogens beskrivning, nyckelord och bedömning som metadata (Description, Keywords,
Comments), favoriter blir gröna och de som föreslås bort röda. Tidslinjer: en per inspelning med
videoklippen i tidsordning (utan bortvalda) och en med alla favoritklipp. Mediet länkas där det ligger.
Redan importerade filer hoppas över, så skriptet kan köras igen när material tillkommer.
"""
import argparse, csv, os, sys
from pathlib import Path

API = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
os.environ.setdefault("RESOLVE_SCRIPT_API", str(API))
os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
sys.path.append(str(API / "Modules"))
import DaVinciResolveScript as dvr  # noqa: E402

VIDEO = {".mp4", ".mov", ".mxf", ".mts", ".braw"}
PHOTO = {".jpg", ".jpeg", ".heic", ".png", ".tif", ".tiff"}
RAW = {".rw2", ".dng", ".cr3", ".cr2", ".nef", ".arw", ".raf", ".orf"}


def catalog(rec: Path):
    f = rec / "innehall.csv"
    return {r["fil"]: r for r in csv.DictReader(open(f, encoding="utf-8-sig"))} if f.exists() else {}


def sub(mp, parent, name):
    for f in parent.GetSubFolderList():
        if f.GetName() == name:
            return f
    return mp.AddSubFolder(parent, name)


def existing(folder):
    return {c.GetClipProperty("File Path"): c for c in folder.GetClipList()}


def add(mp, storage, folder, paths):
    have = existing(folder)
    new = [str(p) for p in paths if str(p) not in have]
    mp.SetCurrentFolder(folder)
    for i in range(0, len(new), 50):          # i omgångar, så att ett fel inte stoppar allt
        storage.AddItemListToMediaPool(new[i:i + 50])
    return existing(folder)


def annotate(clips, cat):
    for path, clip in clips.items():
        r = cat.get(Path(path).name)
        if not r:
            continue
        clip.SetMetadata({"Description": r.get("beskrivning", "")[:250],
                          "Keywords": r.get("nyckelord", "").replace(";", ", "),
                          "Comments": f"betyg {r.get('betyg')} · teknik {r.get('teknik')}: {r.get('teknik_kommentar', '')} · "
                                      f"konst {r.get('konst')}: {r.get('konst_kommentar', '')}"[:500]})
        if r.get("favorit") == "ja":
            clip.SetClipColor("Green")
        elif r.get("forslag") == "bort":
            clip.SetClipColor("Red")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--fps", default="25")
    ap.add_argument("--res", default="3840x2160")
    a = ap.parse_args()
    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        sys.exit("Resolve svarar inte: är Studio igång och står External scripting på Local?")
    pm = resolve.GetProjectManager()
    name = a.project.name
    project = pm.LoadProject(name) or pm.CreateProject(name)
    w, h = a.res.split("x")
    if project.GetTimelineCount() == 0:
        project.SetSetting("timelineFrameRate", a.fps)
        project.SetSetting("timelineResolutionWidth", w)
        project.SetSetting("timelineResolutionHeight", h)
    mp, storage = project.GetMediaPool(), resolve.GetMediaStorage()
    root = mp.GetRootFolder()
    recs = [p for p in a.project.iterdir() if p.is_dir() and (p / "original").is_dir()]
    recs.sort(key=lambda r: min((x["tagen"] for x in catalog(r).values()), default=r.name))
    favs = []
    for rec in recs:
        cat = catalog(rec)
        files = sorted((p for p in (rec / "original").rglob("*") if p.is_file()),
                       key=lambda p: (cat.get(p.name, {}).get("tagen", ""), p.name))
        b = sub(mp, root, rec.name)
        groups = {"video": [p for p in files if p.suffix.lower() in VIDEO],
                  "foto": [p for p in files if p.suffix.lower() in PHOTO],
                  "raw": [p for p in files if p.suffix.lower() in RAW],
                  "tal-tvattade": sorted((rec / "klipp").glob("*-tvattad.mp4"))}
        for g, paths in groups.items():
            if not paths:
                continue
            clips = add(mp, storage, sub(mp, b, g), paths)
            annotate(clips, cat)
            print(f"{rec.name}/{g}: {len(clips)} i Media Pool", flush=True)
            if g == "video":
                keep = [clips[str(p)] for p in paths if str(p) in clips and cat.get(p.name, {}).get("forslag") != "bort"]
                favs += [clips[str(p)] for p in paths if str(p) in clips and cat.get(p.name, {}).get("favorit") == "ja"]
                names = {project.GetTimelineByIndex(i + 1).GetName() for i in range(project.GetTimelineCount())}
                if keep and rec.name not in names:
                    mp.SetCurrentFolder(b)
                    mp.CreateTimelineFromClips(rec.name, keep)
    names = {project.GetTimelineByIndex(i + 1).GetName() for i in range(project.GetTimelineCount())}
    if favs and "favoriter, klipp" not in names:
        mp.SetCurrentFolder(root)
        mp.CreateTimelineFromClips("favoriter, klipp", favs)
    pm.SaveProject()
    print(f"Klart: projektet {name}, {project.GetTimelineCount()} tidslinjer")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
