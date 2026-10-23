"""Gör proxyfiler för ett projekts videoklipp och kopplar dem till klippen i DaVinci Resolve Studio.

    python proxies.py "<delad enhet>/projects/<projekt>" [--out <mapp>] [--height 1080] [--no-link]

Proxyn: H.264 med Intel Quick Sync om det finns (annars libx264), höjd 1080 med bevarat bildformat,
en nyckelbild var tolfte bildruta så att det går lätt att spola, ljudet som AAC. Skrivs lokalt till
<out>/<inspelning>/<klipp>.mov (standard ~/Pictures/wds-arbete/<projekt>/proxy). Finns proxyn redan
hoppas den över. Därefter kopplas varje proxy till sitt klipp i projektet med samma namn som mappen
(MediaPoolItem.LinkProxyMedia); originalen används fortfarande vid färgsättning och export.
"""
import argparse, os, subprocess, sys
from pathlib import Path

VIDEO = {".mp4", ".mov", ".mxf", ".mts"}


def qsv_ok():
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc2=s=256x256:d=0.2",
                        "-c:v", "h264_qsv", "-f", "null", "-"], capture_output=True)
    return r.returncode == 0


def make(src: Path, dst: Path, height: int, qsv: bool):
    dst.parent.mkdir(parents=True, exist_ok=True)
    part = dst.with_name(dst.stem + ".part.mov")
    enc = (["-c:v", "h264_qsv", "-global_quality", "23", "-g", "12"] if qsv
           else ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-g", "12"])
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"scale=-2:{height},format=nv12",
           *enc, "-c:a", "aac", "-b:a", "160k", "-map_metadata", "0", str(part)]
    subprocess.run(cmd, check=True)
    os.replace(part, dst)


def link(project_dir: Path, out: Path):
    api = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
    sys.path.append(str(api / "Modules"))
    import DaVinciResolveScript as dvr
    resolve = dvr.scriptapp("Resolve")
    project = resolve.GetProjectManager().LoadProject(project_dir.name)
    if not project:
        print("Projektet finns inte i Resolve; kör import_project.py först."); return
    linked = 0
    stack = [project.GetMediaPool().GetRootFolder()]
    while stack:
        f = stack.pop()
        stack += f.GetSubFolderList()
        for clip in f.GetClipList():
            p = Path(clip.GetClipProperty("File Path") or "")
            if p.suffix.lower() not in VIDEO or "original" not in p.parts:
                continue
            rec = p.parents[[x.name for x in p.parents].index("original") + 1].name
            proxy = out / rec / (p.stem + ".mov")
            if proxy.exists() and clip.LinkProxyMedia(str(proxy)):
                linked += 1
    resolve.GetProjectManager().SaveProject()
    print(f"{linked} proxyfiler kopplade i Resolve")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--no-link", action="store_true")
    a = ap.parse_args()
    out = a.out or Path.home() / "Pictures" / "wds-arbete" / a.project.name / "proxy"
    clips = sorted(p for p in a.project.glob("*/original/**/*") if p.suffix.lower() in VIDEO)
    qsv = qsv_ok()
    for n, src in enumerate(clips, 1):
        rec = src.parents[[x.name for x in src.parents].index("original") + 1].name
        dst = out / rec / (src.stem + ".mov")
        if dst.exists():
            continue
        make(src, dst, a.height, qsv)
        print(f"{n}/{len(clips)} {rec}/{src.name}", flush=True)
    print(f"{len(clips)} klipp, proxyfiler i {out}", flush=True)
    if not a.no_link:
        link(a.project, out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
