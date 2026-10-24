"""Renderar varje bild på en stillbildstidslinje som en JPEG, en ruta per klipp, i en eller flera storlekar.

    python render_stills.py <tidslinje> <ut-mapp>=<bredd>x<höjd>:<namnmall> [...] [--formats]

Namnmallen får {nn} (löpnummer i tidslinjens ordning) och {stem} (originalets filnamn).
Resolve lägger till ett rutnummer på bildsekvenser; det tas bort efteråt.
"""
import os, sys, time
from pathlib import Path

API = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
os.environ.setdefault("RESOLVE_SCRIPT_API", str(API))
os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
sys.path.append(str(API / "Modules"))
import DaVinciResolveScript as dvr  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        sys.exit("Resolve svarar inte")
    project = resolve.GetProjectManager().GetCurrentProject()
    if "--formats" in sys.argv:
        fmts = project.GetRenderFormats()
        print(fmts)
        for k in ("jpg", "jpeg", "JPEG", "tif"):
            if k in fmts.values() or k in fmts:
                print(k, project.GetRenderCodecs(fmts.get(k, k)))
        return
    name, targets = sys.argv[1], sys.argv[2:]
    tl = next(project.GetTimelineByIndex(i + 1) for i in range(project.GetTimelineCount())
              if project.GetTimelineByIndex(i + 1).GetName() == name)
    project.SetCurrentTimeline(tl)
    resolve.OpenPage("deliver")
    items = [it for it in tl.GetItemListInTrack("video", 1) if it.GetMediaPoolItem()]
    project.DeleteAllRenderJobs()
    jobs = []
    for t in targets:
        out, spec = t.rsplit("=", 1)
        size, tmpl = spec.split(":", 1)
        w, h = (int(v) for v in size.split("x"))
        Path(out).mkdir(parents=True, exist_ok=True)
        for n, it in enumerate(items, 1):
            stem = Path(it.GetMediaPoolItem().GetClipProperty("File Path")).stem
            final = tmpl.format(nn=f"{n:02d}", stem=stem)
            project.SetCurrentRenderFormatAndCodec("jpg", "YUV444_8")
            ok = project.SetRenderSettings({"SelectAllFrames": False, "MarkIn": it.GetStart() + 1, "MarkOut": it.GetStart() + 1,
                                            "TargetDir": out, "CustomName": final, "FormatWidth": w, "FormatHeight": h,
                                            "ExportVideo": True, "ExportAudio": False})
            jobs.append((project.AddRenderJob(), Path(out), final, ok))
    print(f"{len(jobs)} jobb", flush=True)
    project.StartRendering([j[0] for j in jobs], False)
    while project.IsRenderingInProgress():
        time.sleep(2)
    for job, out, final, ok in jobs:
        st = project.GetRenderJobStatus(job)
        hits = sorted(out.glob(f"{final}*.jpg"))
        target = out / f"{final}.jpg"
        if hits and hits[0] != target:
            if target.exists():
                target.unlink()
            hits[0].rename(target)
        print(f"{target.name}: {st.get('JobStatus')} {'ok' if target.exists() else 'SAKNAS'}", flush=True)


if __name__ == "__main__":
    main()
