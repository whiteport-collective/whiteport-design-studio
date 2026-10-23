"""Bygger en reel i DaVinci Resolve Studio ur en klipplista: egen tidslinje i valfritt format, Smart Reframe,
klippens LUT, utan klippljud, och renderar den.

    python reel.py "<delad enhet>/projects/<projekt>" klipplista.json --name reel-9x16-v3 [--size 1080x1920] [--render <mapp>]

klipplista.json: [{"rec": "2026-10-22-koket", "stem": "P1000561", "start": 66.5, "dur": 2.6, "vad": "..."}, ...]
  "reframe": false på ett klipp behåller det breda utsnittet (rummet), utan Smart Reframe.
Klippen läggs i listans ordning med bara bild (mediaType 1), så att musik läggs på utan klippljud. Varje klipp får
Smart Reframe (Studio) och sin LUT ur <projekt>/resolve/lut/<inspelning>/<klipp>.cube om den finns i Resolves
LUT-mapp (looks.py --apply lägger dem där). --render exporterar H.264 i tidslinjens format till mappen.
"""
import argparse, json, os, sys, time
from pathlib import Path

API = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
sys.path.append(str(API / "Modules"))
import DaVinciResolveScript as dvr  # noqa: E402

REFRAME_FPS = 0.6   # Smart Reframe på Surface Pro 7 (Iris Plus): cirka 0,7 bildrutor/s


def clips_by_path(mp):
    out, stack = {}, [mp.GetRootFolder()]
    while stack:
        f = stack.pop()
        stack += f.GetSubFolderList()
        for c in f.GetClipList():
            out[os.path.normcase(c.GetClipProperty("File Path") or "")] = c
    return out


def wait_ready(probe, timeout=600):
    """Smart Reframe analyserar i en modal ruta; under tiden svarar API:t None. Vänta tills det svarar igen."""
    t0 = time.time()
    while probe() is None and time.time() - t0 < timeout:
        time.sleep(2)


def finish(project, tl, project_name, segs=None):
    """LUT och Smart Reframe på varje klipp i tidslinjen, ett i taget. Ett klipp med "reframe": false i
    klipplistan behåller det breda utsnittet (rummet och publiken), utan Smart Reframe."""
    project.SetCurrentTimeline(tl)
    project.RefreshLUTList()
    reframed = luts = 0
    for n, item in enumerate(tl.GetItemListInTrack("video", 1) or []):
        seg = segs[n] if segs and n < len(segs) else {}
        wait_ready(lambda: item.GetName())
        fp = item.GetMediaPoolItem().GetClipProperty("File Path")
        rec, stem = Path(fp).parents[2].name, Path(fp).stem
        for _ in range(10):                      # Resolve kan vara upptaget en stund efter förra analysen
            if item.SetLUT(1, f"{project_name}/{rec}/{stem}.cube"):
                luts += 1; break
            time.sleep(3)
        frames = item.GetDuration() or 60
        if seg.get("reframe") is False:
            print(f"  {item.GetName()}: brett utsnitt, ingen Smart Reframe", flush=True)
            continue
        for _ in range(5):
            if item.SmartReframe():
                reframed += 1; break
            time.sleep(5)
        # analysen går i en modal ruta i ungefär REFRAME_FPS bildrutor per sekund; vänta ut den
        time.sleep(max(8, frames / REFRAME_FPS))
        wait_ready(lambda: item.GetName())
        print(f"  {item.GetName()}: klar", flush=True)
    return reframed, luts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("segments", type=Path)
    ap.add_argument("--name", required=True)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--fps", type=float, default=25)
    ap.add_argument("--render", type=Path)
    ap.add_argument("--finish-only", action="store_true", help="bara LUT och Smart Reframe på en befintlig tidslinje")
    ap.add_argument("--replace", action="store_true", help="ta bort en tidigare tidslinje med samma namn (en avbruten omtagning)")
    a = ap.parse_args()
    segs = json.loads(a.segments.read_text(encoding="utf-8"))
    resolve = dvr.scriptapp("Resolve")
    pm = resolve.GetProjectManager()
    project = pm.LoadProject(a.project.name)
    mp = project.GetMediaPool()
    names = [project.GetTimelineByIndex(i + 1).GetName() for i in range(project.GetTimelineCount())]
    if a.finish_only:
        tl = next(project.GetTimelineByIndex(i + 1) for i in range(project.GetTimelineCount()) if project.GetTimelineByIndex(i + 1).GetName() == a.name)
        r, l = finish(project, tl, a.project.name, segs)
        pm.SaveProject()
        print(f"{a.name}: Smart Reframe på {r}, LUT på {l}")
        if not a.render:
            return
        w, h = a.size.split("x")
        render(project, a, w, h)
        return
    if a.name in names and a.replace:
        wait_ready(lambda: project.GetName())
        old = [project.GetTimelineByIndex(i + 1) for i in range(project.GetTimelineCount())
               if project.GetTimelineByIndex(i + 1).GetName() == a.name]
        project.SetCurrentTimeline(project.GetTimelineByIndex(1))
        mp.DeleteTimelines(old)
        names = [project.GetTimelineByIndex(i + 1).GetName() for i in range(project.GetTimelineCount())]
    if a.name in names:
        sys.exit(f"Tidslinjen {a.name} finns redan; välj ett nytt namn (ett nytt versionsnummer).")
    mp.SetCurrentFolder(mp.GetRootFolder())
    tl = mp.CreateEmptyTimeline(a.name)
    w, h = a.size.split("x")
    tl.SetSetting("useCustomSettings", "1")
    tl.SetSetting("timelineResolutionWidth", w)
    tl.SetSetting("timelineResolutionHeight", h)
    tl.SetSetting("timelineInputResMismatchBehavior", "scaleToCrop")
    project.SetCurrentTimeline(tl)
    pool = clips_by_path(mp)
    infos = []
    for s in segs:
        path = a.project / s["rec"] / "original" / s.get("source", "marten-lumix-s9") / f"{s['stem']}.MP4"
        clip = pool.get(os.path.normcase(str(path)))
        if not clip:
            print(f"saknas i Media Pool: {path}"); continue
        start = int(round(s["start"] * a.fps))
        end = start + int(round(s["dur"] * a.fps)) - 1
        infos.append({"mediaPoolItem": clip, "startFrame": start, "endFrame": end, "mediaType": 1})
    items = mp.AppendToTimeline(infos) or []
    reframed, luts = finish(project, tl, a.project.name, segs)
    pm.SaveProject()
    print(f"{a.name}: {len(items)} klipp, Smart Reframe på {reframed}, LUT på {luts}, "
          f"{sum(s['dur'] for s in segs):.1f} s, {w}x{h}")
    if a.render:
        render(project, a, w, h)


def render(project, a, w, h):
    if True:
        a.render.mkdir(parents=True, exist_ok=True)
        project.SetCurrentRenderFormatAndCodec("mp4", "H264")
        project.SetRenderSettings({"SelectAllFrames": True, "TargetDir": str(a.render), "CustomName": a.name,
                                   "FormatWidth": int(w), "FormatHeight": int(h), "ExportVideo": True, "ExportAudio": False})
        job = project.AddRenderJob()
        project.StartRendering(job)
        while project.IsRenderingInProgress():
            time.sleep(5)
        print(f"Renderad: {a.render / (a.name + '.mp4')}", project.GetRenderJobStatus(job))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
