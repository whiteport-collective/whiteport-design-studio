"""Lägger in en inspelnings stillbilder i Resolve Studio och sätter uppmätt vitbalans som CDL på nod 1.

    python stills_resolve.py "<delad enhet>/projects/<projekt>" <inspelning> --files P1000307,... [--strength 0.3] [--preview <mapp>]

Projektet får mappens namn. Bin <inspelning>/foto (JPEG) och <inspelning>/raw (RW2), tidslinjen "<inspelning> foto"
med JPEG-bilderna i 6000x4000. Vitbalansen mäts på mellantonerna (gråvärld i linjärt ljus, delstyrka, ljusheten behålls)
och blir CDL-slope i gammarummet, så att den syns och går att justera i Color. Originalen rörs aldrig.
"""
import argparse, csv, os, sys, time
from pathlib import Path

import numpy as np
from PIL import Image

API = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
os.environ.setdefault("RESOLVE_SCRIPT_API", str(API))
os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
sys.path.append(str(API / "Modules"))
import DaVinciResolveScript as dvr  # noqa: E402

FPS = 25


def slope(jpg: Path, strength: float):
    im = Image.open(jpg)
    im.draft("RGB", (1500, 1000))
    x = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    lin = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
    lum = lin.mean(axis=2)
    means = lin[(lum > 0.02) & (lum < 0.8)].mean(axis=0)
    g = (means.mean() / means) ** strength
    w = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    g *= (means @ w) / ((means * g) @ w)
    return g ** (1 / 2.2)


def sub(mp, parent, name):
    for f in parent.GetSubFolderList():
        if f.GetName() == name:
            return f
    return mp.AddSubFolder(parent, name)


def add(mp, storage, folder, paths):
    have = {c.GetClipProperty("File Path"): c for c in folder.GetClipList()}
    new = [str(p) for p in paths if str(p) not in have]
    mp.SetCurrentFolder(folder)
    if new:
        storage.AddItemListToMediaPool(new)
    return {c.GetClipProperty("File Path"): c for c in folder.GetClipList()}


def tc(frame):
    s, f = divmod(int(frame), FPS)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("recording")
    ap.add_argument("--files", required=True)
    ap.add_argument("--strength", type=float, default=0.3)
    ap.add_argument("--preview", type=Path)
    a = ap.parse_args()

    resolve = None
    for _ in range(90):
        resolve = dvr.scriptapp("Resolve")
        if resolve and resolve.GetProjectManager():
            break
        time.sleep(2)
    if not resolve:
        sys.exit("Resolve svarar inte: är Studio igång och står External scripting på Local?")
    pm = resolve.GetProjectManager()
    name = a.project.name
    project = pm.LoadProject(name) or pm.CreateProject(name)
    if not project:
        sys.exit(f"Kunde varken öppna eller skapa projektet {name}")
    if project.GetTimelineCount() == 0:
        project.SetSetting("timelineFrameRate", str(FPS))
        project.SetSetting("timelineResolutionWidth", "6000")
        project.SetSetting("timelineResolutionHeight", "4000")

    rec = a.project / a.recording
    src = next((rec / "original").iterdir())
    names = a.files.split(",")
    cat_f = rec / "innehall.csv"
    cat = {r["fil"]: r for r in csv.DictReader(open(cat_f, encoding="utf-8-sig"))} if cat_f.exists() else {}

    mp, storage = project.GetMediaPool(), resolve.GetMediaStorage()
    b = sub(mp, mp.GetRootFolder(), a.recording)
    jpgs = [src / f"{n}.JPG" for n in names]
    add(mp, storage, sub(mp, b, "raw"), [src / f"{n}.RW2" for n in names])
    clips = add(mp, storage, sub(mp, b, "foto"), jpgs)
    for path, clip in clips.items():
        r = cat.get(Path(path).name)
        if r:
            clip.SetMetadata({"Description": r.get("beskrivning", "")[:250], "Keywords": r.get("nyckelord", "").replace(";", ", ")})
            if r.get("favorit") == "ja":
                clip.SetClipColor("Green")

    tl_name = f"{a.recording} foto"
    tl = next((project.GetTimelineByIndex(i + 1) for i in range(project.GetTimelineCount())
               if project.GetTimelineByIndex(i + 1).GetName() == tl_name), None)
    if not tl:
        mp.SetCurrentFolder(b)
        tl = mp.CreateTimelineFromClips(tl_name, [clips[str(p)] for p in jpgs if str(p) in clips])
    project.SetCurrentTimeline(tl)

    items = tl.GetItemListInTrack("video", 1)
    resolve.OpenPage("color")
    if a.preview:
        a.preview.mkdir(parents=True, exist_ok=True)
    for it in items:
        jpg = Path(it.GetMediaPoolItem().GetClipProperty("File Path"))
        s = slope(jpg, a.strength)
        ok = it.SetCDL({"NodeIndex": "1", "Slope": " ".join(f"{v:.4f}" for v in s),
                        "Offset": "0 0 0", "Power": "1 1 1", "Saturation": "1"})
        print(f"{jpg.stem}: slope {np.round(s, 3)} {'ok' if ok else 'MISSLYCKADES'}", flush=True)
        if a.preview:
            tl.SetCurrentTimecode(tc(it.GetStart() + 1))
            time.sleep(0.5)
            project.ExportCurrentFrameAsStill(str(a.preview / f"{jpg.stem}.jpg"))
    pm.SaveProject()
    print(f"Klart: projektet {name}, tidslinjen {tl_name}, {len(items)} bilder")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
