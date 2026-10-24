"""Klipp till mediebanken: varje utvalt klipp blir en tidslinje i Resolve med två versioner, hela bilden och stående 9:16
med egen följning som riktiga nyckelpunkter, neutral färg (utjämning, inget utseende), en .drt bredvid råklippet och
rendering i full upplösning, 10 bitar.

    python mediabank.py "<delad enhet>/projects/<projekt>" [--only P1000708-01] [--replace] [--render] [--open P1000708-01]

Urvalet står i <projekt>/resolve/mediabank-urval.json, ett klipp per rad:
  {"id": "P1000708-01", "rec": "2026-10-22-linnesalen", "stem": "P1000708", "in": 0.4, "out": 31.0,
   "title": "Servitris bär förrätten från passet till bordet", "description": "...", "keywords": ["servering", "följbild"],
   "x": [[0.4, 0.70], [5.0, 0.35], [30.0, 0.40]]}
"x" är rutans mittpunkt över bredden (0–1) vid en tid i råklippet; ett tal ger fast utsnitt. Mellan punkterna glider
rutan mjukt (smooth). I Resolve är det vanliga nyckelpunkter på Position (Inspector → Transform) som går att flytta.

Varje klipp:
  1. två tidslinjer i binen mediabank: <id> med hela bilden i råklippets upplösning, och <id>-9x16 stående
     (1440x2560 ur 3840x2560) med följningen som nyckelpunkter (FCPXML, ImportTimelineFromFile). En tidslinje som
     redan finns rörs inte utan --replace, så att justeringar som gjorts i Resolve finns kvar.
  2. neutral färg på nod 1: klippet mäts över tiden (looks.light_segments), och skiftar ljuset (kök till sal) delas det
     i ljuszoner med var sin utjämning, <klipp>.mediabank-01.ljus-N.cube bredvid råklippet, och en övertoning där ljuset
     skiftar, så att färgen glider utan hopp. Varje zon får karaktär efter ljuset: lysrör sterilt, glödljus varmt
     (looks.character); "look": "neutral" på ett klipp i urvalet stänger av det
  3. en .drt per tidslinje bredvid råklippet, P1000708.mediabank-01.drt och P1000708.mediabank-01.9x16.drt:
     allt om klippet följer med råklippet
  4. med --render: <projekt>/export/mediabank/<inspelning>/<id>_<titel>.mp4 (hela bilden) och ..._9x16.mp4
     (1440x2560 ur 3840x2560), HEVC Main 10, med titel, beskrivning och nyckelord inskrivna (exiftool), och en rad i
     <projekt>/export/mediabank/mediabank.csv
--out <mapp>  renderar dit i stället för till projektet (extern disk när C: är full); kopiera sedan till export/mediabank
--open <id> eller <id>-9x16  gör tidslinjen aktuell i Resolve, för att rätta efter feedback (importerar .drt om tidslinjen saknas)
"""
import argparse, csv, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
import looks  # noqa: E402

VIDEO_DIR = "original"


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


def probe(src: Path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate:format=duration",
                        "-of", "json", str(src)], capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    st = j["streams"][0]
    num, den = map(int, st["r_frame_rate"].split("/"))
    return st["width"], st["height"], round(num / den), float(j["format"]["duration"])


def slug(s: str) -> str:
    s = s.lower().translate(str.maketrans("åäöé", "aaoe"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def fcpxml(e, src: Path, w, h, fps, dur_src, zones, vertical=False):
    """En tidslinje för en version: hela bilden (råklippets upplösning) eller stående 9:16 (1440x2560 ur 3840x2560)
    med följningen som nyckelpunkter. zones ur looks.light_segments: en del per ljuszon, med en övertoning (samma
    bildrutor, olika färg) där ljuset skiftar, så att färgen glider utan hopp."""
    t = lambda sec: f"{int(round(sec * fps))}/{fps}s"
    d = e["out"] - e["in"]
    vw = int(round(h * 9 / 16 / 2)) * 2 if vertical else w
    half = (w - vw) / 2 / w                                # hur långt mittpunkten får gå innan rutan går utanför bilden
    clamp = lambda x: min(1 - half, max(half, x))
    pos = lambda x: f"{(0.5 - clamp(x)) * w / h * 100:.3f} 0"   # FCPXML: procent av bildens höjd (provat: -30 = -768 px i 3840x2560)
    transform = ""
    if vertical:
        # Final Cuts standard är att passa in hela bilden (svart runt om); fill fyller rutan i full höjd
        conform = '            <adjust-conform type="fill"/>\n'
        xs = e.get("x", 0.5)
        if isinstance(xs, list):
            kf = "\n".join(f'                  <keyframe time="{t(s)}" value="{pos(x)}" curve="smooth"/>' for s, x in xs)
            transform = conform + (f'            <adjust-transform position="{pos(xs[0][1])}">\n              <param name="position">\n'
                         f'                <keyframeAnimation>\n{kf}\n                </keyframeAnimation>\n              </param>\n'
                         f'            </adjust-transform>')
        else:
            transform = conform + f'            <adjust-transform position="{pos(xs)}"/>'
    uri = "file:///" + quote(str(src).replace("\\", "/"), safe="/:")
    parts = []
    for i, (s, en, _, fade, *_) in enumerate(zones):
        body = f">\n{transform}\n            </asset-clip>" if transform else "/>"
        parts.append(f'            <asset-clip ref="r2" name="{e["id"]} {i + 1}" offset="{t(s - e["in"])}" '
                     f'start="{t(s)}" duration="{t(en - s)}" format="r1"{body}')
        if fade and i < len(zones) - 1:
            parts.append(f'            <transition name="Cross Dissolve" offset="{t(en - e["in"] - fade / 2)}" duration="{t(fade)}">'
                         f'<filter-video ref="r4" name="Cross Dissolve"/></transition>')
    spine = "\n".join(parts)
    name = e["id"] + ("-9x16" if vertical else "")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.9">
  <resources>
    <format id="r1" frameDuration="1/{fps}s" width="{w}" height="{h}"/>
    <format id="r3" frameDuration="1/{fps}s" width="{vw}" height="{h}"/>
    <asset id="r2" name="{src.stem}" start="0s" duration="{t(dur_src)}" hasVideo="1" hasAudio="1" format="r1" src="{uri}"/>
    <effect id="r4" name="Cross Dissolve" uid="FxPlug:4731E73A-8DAC-4113-9A30-AE85B1761265"/>
  </resources>
  <library>
    <event name="mediabank">
      <project name="{name}">
        <sequence format="r3" duration="{t(d)}" tcStart="0s" tcFormat="NDF">
          <spine>
{spine}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
"""


def lut_rel(project_dir: Path, lut: Path, rec: str) -> str:
    """Resolve tar bara LUT:ar i sin egen LUT-mapp: kopiera dit och använd relativ sökväg."""
    master = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/LUT" / project_dir.name / "neutral" / rec
    master.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(lut, master / lut.name)
    return f"{project_dir.name}/neutral/{rec}/{lut.name}"


def find_timeline(project, name):
    for i in range(1, project.GetTimelineCount() + 1):
        tl = project.GetTimelineByIndex(i)
        if tl and tl.GetName() == name:
            return tl
    return None


def drt_path(src: Path, eid: str, vertical=False) -> Path:
    return src.with_name(f"{src.stem}.mediabank-{eid.rsplit('-', 1)[-1]}{'.9x16' if vertical else ''}.drt")


def render(r, project, tls, e, src, out_dir: Path):
    """tls: [(tidslinje, suffix)]; varje tidslinje renderas hel i sin egen upplösning."""
    out_dir.mkdir(parents=True, exist_ok=True)
    base = f"{e['id']}_{slug(e.get('title', ''))}".rstrip("_")
    for old in out_dir.glob(f"{e['id']}_*.mp4"):              # förra renderingen till papperskorgen, aldrig överskriven
        if sys.platform == "win32":
            subprocess.run(["powershell", "-NoProfile", "-Command", "Add-Type -AssemblyName Microsoft.VisualBasic; "
                            f"[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile('{old}', 'OnlyErrorDialogs', 'SendToRecycleBin')"], check=False)
    jobs = []
    for tl, suffix in tls:
        project.SetCurrentTimeline(tl)
        project.SetCurrentRenderFormatAndCodec("mp4", "H265")
        project.SetRenderSettings({"SelectAllFrames": True, "TargetDir": str(out_dir), "CustomName": base + suffix,
                                   "FormatWidth": int(tl.GetSetting("timelineResolutionWidth")),
                                   "FormatHeight": int(tl.GetSetting("timelineResolutionHeight")),
                                   "EncodingProfile": "Main10", "ExportVideo": True, "ExportAudio": True})
        jobs.append(project.AddRenderJob())
    t0 = time.time()
    project.StartRendering(jobs)
    while project.IsRenderingInProgress():
        time.sleep(1)
    files = []
    for j, (_, suffix) in zip(jobs, tls):
        st = project.GetRenderJobStatus(j)
        project.DeleteRenderJob(j)
        if st.get("JobStatus") != "Complete":
            sys.exit(f"rendering misslyckades: {e['id']}{suffix}: {st}")
        files.append(out_dir / f"{base}{suffix}.mp4")
    for f in files:
        subprocess.run(["exiftool", "-q", "-overwrite_original", f"-XMP-dc:Title={e.get('title', '')}",
                        f"-XMP-dc:Description={e.get('description', '')}", *[f"-XMP-dc:Subject={k}" for k in e.get("keywords", [])],
                        "-XMP-dc:Creator=Mårten Angner", "-XMP-dc:Rights=Visita", f"-XMP-dc:Source={src.name}", str(f)], check=False)
    print(f"  renderat på {time.time() - t0:.0f} s: {', '.join(f.name for f in files)}", flush=True)
    return files


def update_index(index: Path, e, files, src: Path):
    rows = []
    if index.exists():
        with index.open(encoding="utf-8", newline="") as f:
            rows = [r for r in csv.DictReader(f) if r["id"] != e["id"]]
    rows.append({"id": e["id"], "titel": e.get("title", ""), "beskrivning": e.get("description", ""),
                 "nyckelord": ";".join(e.get("keywords", [])), "inspelning": e["rec"], "raklipp": src.name,
                 "in": e["in"], "ut": e["out"], "hela": files[0].name, "stående": files[1].name})
    with index.open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(sorted(rows, key=lambda r: r["id"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--only", help="bara dessa id, kommaseparerat")
    ap.add_argument("--replace", action="store_true", help="gör om tidslinjer som redan finns (justeringar i Resolve försvinner)")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--open", help="gör klippets tidslinje aktuell i Resolve")
    ap.add_argument("--out", type=Path, help="rendera hit i stället för <projekt>/export/mediabank (till exempel en extern disk när C: är full)")
    a = ap.parse_args()
    sel = json.loads((a.project / "resolve" / "mediabank-urval.json").read_text(encoding="utf-8"))
    r = resolve_app()
    pm = r.GetProjectManager()
    for _ in range(60):                                       # Resolve kan svara innan projekten går att öppna
        project = pm.GetCurrentProject()
        if not project or project.GetName() != a.project.name:
            project = pm.LoadProject(a.project.name)
        if project:
            break
        time.sleep(5)
    else:
        sys.exit(f"projektet {a.project.name} går inte att öppna i Resolve")
    mp = project.GetMediaPool()
    root = mp.GetRootFolder()
    bin_ = next((f for f in root.GetSubFolderList() if f.GetName() == "mediabank"), None) or mp.AddSubFolder(root, "mediabank")
    mp.SetCurrentFolder(bin_)

    if a.open:
        eid = a.open.removesuffix("-9x16")
        e = next(x for x in sel if x["id"] == eid)
        src = a.project / e["rec"] / VIDEO_DIR / e.get("source", "marten-lumix-s9") / f"{e['stem']}.MP4"
        tl = find_timeline(project, a.open) or mp.ImportTimelineFromFile(str(drt_path(src, eid, a.open.endswith("-9x16"))),
                                                                       {"timelineName": a.open})
        project.SetCurrentTimeline(tl)
        r.OpenPage("edit")
        print(f"öppnad: {a.open}")
        return

    only = set(a.only.split(",")) if a.only else None
    for e in sel:
        if only and e["id"] not in only:
            continue
        src = a.project / e["rec"] / VIDEO_DIR / e.get("source", "marten-lumix-s9") / f"{e['stem']}.MP4"
        w, h, fps, dur_src = probe(src)
        zones, luts, tls = None, [], []
        for vertical in (False, True):
            name = e["id"] + ("-9x16" if vertical else "")
            tl = find_timeline(project, name)
            if tl and a.replace:
                mp.DeleteTimelines([tl])
                tl = None
            if not tl:
                if zones is None:
                    zones = looks.light_segments(src, e["in"], e["out"])
                    for i, (_, _, gn, _, rb, *_) in enumerate(zones):
                        cube = src.with_name(f"{src.stem}.mediabank-{e['id'].rsplit('-', 1)[-1]}.ljus-{i + 1}.cube")
                        looks.write_cube(cube, gn, looks.LOOKS[e.get("look") or looks.character(rb)])
                        luts.append(lut_rel(a.project, cube, e["rec"]))
                    project.RefreshLUTList()
                with tempfile.TemporaryDirectory() as td:
                    x = Path(td) / f"{name}.fcpxml"
                    x.write_text(fcpxml(e, src, w, h, fps, dur_src, zones, vertical), encoding="utf-8")
                    tl = mp.ImportTimelineFromFile(str(x), {"timelineName": name, "importSourceClips": True})
                if not tl:
                    sys.exit(f"importen misslyckades: {name} (renderar Resolve? då krävs omstart)")
                items = [it for it in tl.GetItemListInTrack("video", 1) or [] if it.GetMediaPoolItem()]   # inte övertoningarna
                for k, it in enumerate(items):
                    it.SetLUT(1, luts[k])
                print(f"{name}: {tl.GetSetting('timelineResolutionWidth')}x{tl.GetSetting('timelineResolutionHeight')}, "
                      f"ljuszoner: {', '.join(e.get('look') or looks.character(z[4]) for z in zones)}", flush=True)
            else:
                print(f"{name}: tidslinjen finns, rörs inte (--replace gör om den)", flush=True)
            drt = drt_path(src, e["id"], vertical)
            tl.Export(str(drt), r.EXPORT_DRT)
            print(f"  {drt.name} bredvid råklippet", flush=True)
            tls.append((tl, "_9x16" if vertical else ""))
        if a.render:
            out_root = a.out or a.project / "export" / "mediabank"
            files = render(r, project, tls, e, src, out_root / e["rec"])
            update_index(out_root / "mediabank.csv", e, files, src)
        project.SetCurrentTimeline(tls[-1][0])
    pm.SaveProject()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
