"""Lägger en reel i Resolve som egen tidslinje av de färdiga klippen (reframe.py och reel_assemble.py), med musiken.

    python reel_timeline.py "<delad enhet>/projects/<projekt>" v7

Klippen hämtas ur <projekt>/resolve/reel-<version>-klipp/segNN-*.mp4 (stillbilderna som rörliga klipp) och läggs i binen
reel-<version>-klipp, tidslinjen heter reel-9x16-<version>. Väntar på att Resolve startat och öppnar projektet med mappens namn.
Justeringar som Resolve kan göra görs här och inte genom att rendera om (Mårten, 2026-10-24): "resolve" på en del i
klipplistan sätts med SetProperty på klippet i tidslinjen, till exempel {"RotationAngle": -1.5, "ZoomX": 1.05, "ZoomY": 1.05}.
"""
import DaVinciResolveScript as dvr, json, sys, time
from pathlib import Path
P = Path(sys.argv[1])
NAME = P.name
V = sys.argv[2]
for _ in range(180):
    r = dvr.scriptapp("Resolve")
    if r:
        pm = r.GetProjectManager(); p = pm.GetCurrentProject()
        if p and p.GetName() == NAME: break
        if p and p.GetName() != NAME:
            p = pm.LoadProject(NAME)
            if p: break
    time.sleep(5)
else:
    raise SystemExit("Resolve svarar inte")
mp = p.GetMediaPool(); root = mp.GetRootFolder()
b = next((f for f in root.GetSubFolderList() if f.GetName() == f"reel-{V}-klipp"), None) or mp.AddSubFolder(root, f"reel-{V}-klipp")
import glob
folder = b
mp.SetCurrentFolder(b)
have = {c.GetName(): c for c in b.GetClipList()}
segs = json.loads((P / f"resolve/reel-9x16-{V}-klipplista.json").read_text(encoding="utf-8"))
extra = sorted(glob.glob(str(P / f"resolve/reel-{V}-klipp/seg*.mp4"))) + sorted(glob.glob(str(P / f"export/sociala-medier/*-reel-highlights-{V}.mp4")))
for f in extra:
    if Path(f).name not in have:
        for it in mp.ImportMedia([f]) or []:
            have[it.GetName()] = it
tl = next((p.GetTimelineByIndex(i) for i in range(1, p.GetTimelineCount() + 1) if p.GetTimelineByIndex(i).GetName() == f"reel-9x16-{V}"), None)
if not tl:
    tl = mp.CreateEmptyTimeline(f"reel-9x16-{V}")
    for k, v in (("useCustomSettings", "1"), ("timelineResolutionWidth", "1080"), ("timelineResolutionHeight", "1920"),
                 ("timelineInputResMismatchBehavior", "scaleToCrop")):
        tl.SetSetting(k, v)
    p.SetCurrentTimeline(tl)
    infos = []
    for n, s in enumerate(segs):
        it = next(c for nm, c in sorted(have.items()) if nm.startswith(f"seg{n:02}-"))
        infos.append({"mediaPoolItem": it, "startFrame": 0, "endFrame": int(round(s["want"] * 25)) - 1, "mediaType": 1})
    items = mp.AppendToTimeline(infos) or []
    # justeringar som görs i Resolve i stället för att rendera om klippet: "resolve": {"RotationAngle": -1.0, "ZoomX": 1.05, ...}
    for it, s in zip(items, segs):
        for k, v in (s.get("resolve") or {}).items():
            it.SetProperty(k, v)
    mus = next((f for f in root.GetSubFolderList() if f.GetName() == "musik"), None)
    if mus and mus.GetClipList():
        mp.AppendToTimeline([{"mediaPoolItem": mus.GetClipList()[0], "startFrame": 0, "endFrame": int(sum(s["want"] for s in segs) * 25) - 1, "mediaType": 2}])
p.SetCurrentTimeline(tl)
r.OpenPage("edit")
pm.SaveProject()
print(tl.GetName(), len(tl.GetItemListInTrack("video", 1)), "delar,", len(tl.GetItemListInTrack("audio", 1) or []), "musik")
