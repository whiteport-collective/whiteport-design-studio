"""Filmens dokument blir filmen: film.yaml skrivs ut som manus och byggs som tidslinje i Resolve Studio.

    python film_build.py manus  "projects/<projekt>/film/<film>"            # manus.md ur film.yaml
    python film_build.py bygg   "projects/<projekt>/film/<film>" [--ersatt] [--render <fil.mp4> [--bredd 960]]

film.yaml (fälten står i skillen film-production; här det bygget läser):

    film: <namn>
    mal_sekunder: 60
    resolve: {projekt, tidslinje, bredd, hojd, bps}
    rot: <mediarot på den delade enheten>
    kallor: {<alias>: <sökväg under roten, eller absolut>}
    musik: [<händelse>, ...]                 # placeras från filmens början
    slag:
      - id, roll, krafter, bild, ljud, text_i_bild, sekunder, kalla, status
        klipp: [<händelse>, ...]             # placeras från slagets början

En händelse: {spar: V1|V2|V3|A1|A2|A3|AV1, kalla, in, ut, pa, overgang: {typ, rutor, justering}, fart,
toning_in, toning_ut, egenskaper: {...}}. in och ut är sekunder i källan, pa sekunder från slagets
(eller filmens) början, negativt för J-klipp; utan pa läggs händelsen efter den förra på samma spår.
AV1 är bild och ljud tillsammans (V1 och A1). Varje slag får en markör med sitt id, så att feedback i
Resolve hittar tillbaka till raden i dokumentet.
"""
import argparse, json, math, os, statistics, sys, time
from pathlib import Path

import yaml

TRACK = {"V": "video", "A": "audio"}


# ---------- dokumentet ----------

def load(folder: Path):
    return yaml.safe_load((folder / "film.yaml").read_text(encoding="utf-8"))


def cell(s):
    return str(s or "").replace("|", "/").replace("\n", " ").strip()


def write_manus(folder: Path, f):
    total = sum(float(b.get("sekunder") or 0) for b in f["slag"])
    rows = [f"# {f.get('titel', f['film'])}\n",
            f"Manus ur `film.yaml`, utskrivet {time.strftime('%Y-%m-%d %H:%M')}. Ändra i `film.yaml`, inte här.\n",
            f"**Längd:** {total:.0f} s av målet {f.get('mal_sekunder', '?')} s · **Format:** "
            f"{f['resolve'].get('bredd')}x{f['resolve'].get('hojd')}, {f['resolve'].get('bps', 25)} bilder/s\n",
            "| Slag | Bild | Ljud | Text i bild | Källa |", "|---|---|---|---|---|"]
    t = 0.0
    for b in f["slag"]:
        sek = float(b.get("sekunder") or 0)
        head = f"**{b['id']}** {b.get('roll', '')}<br>{fmt(t)}–{fmt(t + sek)}<br>{', '.join(b.get('krafter') or [])}"
        src = cell(b.get("kalla")) + ("<br>" + "<br>".join(
            f"{e['kalla']} {e.get('in', 0):.1f}–{e.get('ut', 0):.1f}" for e in b.get("klipp") or [] if e.get("kalla")) if b.get("klipp") else "")
        rows.append(f"| {head} | {cell(b.get('bild'))} | {cell(b.get('ljud'))} | {cell(b.get('text_i_bild'))} | {src} |")
        t += sek
    (folder / "manus.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"manus.md: {len(f['slag'])} slag, {total:.0f} s")


def fmt(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


# ---------- Resolve ----------

def resolve_app():
    api = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
    sys.path.append(str(api / "Modules"))
    import DaVinciResolveScript as dvr
    r = dvr.scriptapp("Resolve")
    if not r:
        sys.exit("Resolve svarar inte: är Studio igång och står External scripting på Local?")
    return r


def proxy_for(p: Path):
    for c in (p.with_suffix(".proxy.mov"), p.parent / p.stem / f"{p.stem}.proxy.mov"):
        if c.exists():
            return c
    return None


def media(mp, f, folder):
    root = Path(f.get("rot", ""))
    paths = {a: (Path(v) if Path(v).is_absolute() else root / v) for a, v in f["kallor"].items()}
    bin_ = mp.GetRootFolder()
    for part in ["film", f["film"]]:
        bin_ = next((x for x in bin_.GetSubFolderList() if x.GetName() == part), None) or mp.AddSubFolder(bin_, part)
    mp.SetCurrentFolder(bin_)
    have = {Path(c.GetClipProperty("File Path")).as_posix().lower(): c for c in bin_.GetClipList()}
    new = [str(p) for p in paths.values() if p.as_posix().lower() not in have]
    missing = [str(p) for p in paths.values() if not p.exists()]
    if missing:
        sys.exit("Saknas: " + ", ".join(missing))
    if new:
        mp.ImportMedia(new)  # ordboksformen gav None i 21.1.1; listan med sökvägar fungerar
    have = {Path(c.GetClipProperty("File Path")).as_posix().lower(): c for c in bin_.GetClipList()}
    items = {}
    for a, p in paths.items():
        it = have.get(p.as_posix().lower())
        if not it:
            sys.exit(f"Kunde inte importera {p}")
        px = proxy_for(p)
        if px and not it.GetClipProperty("Proxy Media Path"):
            it.LinkProxyMedia(str(px))
        items[a] = it
    return items


def src_fps(item, fallback):
    try:
        v = float(item.GetClipProperty("FPS"))
        return v if v > 0 else fallback
    except (TypeError, ValueError):
        return fallback


def plan(f):
    """Gör om slagen till absoluta händelser (sekunder från filmens början)."""
    fps = float(f["resolve"].get("bps", 25))
    events, marks, t = [], [], 0.0
    for e in f.get("musik") or []:
        events.append(dict(e, start=float(e.get("pa", 0)), slag="musik"))
    for b in f["slag"]:
        cursor = {}
        end = t
        for e in b.get("klipp") or []:
            tr = e["spar"]
            dur = (float(e["ut"]) - float(e["in"])) * 100.0 / float(e.get("fart", 100))
            start = t + float(e["pa"]) if "pa" in e else cursor.get(tr, t)
            cursor[tr] = start + dur
            end = max(end, start + dur)
            events.append(dict(e, start=start, slag=b["id"]))
        length = float(b["sekunder"]) if b.get("sekunder") else end - t
        marks.append((b, t, length))
        t += length
    return events, marks, t, fps


def build(folder: Path, f, replace=False, render=None, width=960):
    r = resolve_app()
    pm = r.GetProjectManager()
    cfg = f["resolve"]
    project = pm.LoadProject(cfg["projekt"]) or pm.CreateProject(cfg["projekt"])
    fps = float(cfg.get("bps", 25))
    if project.GetTimelineCount() == 0:
        for k, v in {"timelineFrameRate": str(int(fps)), "timelineResolutionWidth": str(cfg.get("bredd", 1920)),
                     "timelineResolutionHeight": str(cfg.get("hojd", 1080)),
                     "timelineInputResMismatchBehavior": "scaleToCrop"}.items():
            project.SetSetting(k, v)
    mp = project.GetMediaPool()
    items = media(mp, f, folder)

    name = cfg["tidslinje"]
    old = next((project.GetTimelineByIndex(i + 1) for i in range(project.GetTimelineCount())
                if project.GetTimelineByIndex(i + 1).GetName() == name), None)
    if old and not replace:
        sys.exit(f"Tidslinjen {name} finns redan; ge en ny version eller --ersatt")
    if old:
        mp.DeleteTimelines([old])
    tl = mp.CreateEmptyTimeline(name)
    project.SetCurrentTimeline(tl)
    t0 = tl.GetStartFrame()

    events, marks, total, _ = plan(f)
    need = {"video": 1, "audio": 1}
    for e in events:
        kind, n = ("video", int(e["spar"][2:])) if e["spar"].startswith("AV") else (TRACK[e["spar"][0]], int(e["spar"][1:]))
        need[kind] = max(need[kind], n)
        if e["spar"].startswith("AV"):
            need["audio"] = max(need["audio"], n)
    while tl.GetTrackCount("video") < need["video"]:
        tl.AddTrack("video")
    while tl.GetTrackCount("audio") < need["audio"]:
        tl.AddTrack("audio", "stereo")

    placed = []
    for e in sorted(events, key=lambda x: x["start"]):
        it = items[e["kalla"]]
        sf = src_fps(it, fps)
        info = {"mediaPoolItem": it, "startFrame": round(float(e["in"]) * sf), "endFrame": round(float(e["ut"]) * sf),
                "recordFrame": t0 + round(e["start"] * fps)}
        if e["spar"].startswith("AV"):
            info["trackIndex"] = int(e["spar"][2:])
        else:
            info["trackIndex"] = int(e["spar"][1:])
            info["mediaType"] = 1 if e["spar"][0] == "V" else 2
        res = mp.AppendToTimeline([info]) or []
        if not res:
            print(f"MISSLYCKADES: {e['slag']} {e['spar']} {e['kalla']} {e['in']}-{e['ut']}", flush=True)
        for ti in res:
            placed.append((e, ti))
            if e.get("fart"):
                ti.SetSpeed({"Percentage": float(e["fart"])})
            fades = {k2: round(float(e[k1]) * fps) for k1, k2 in (("toning_in", "FadeIn"), ("toning_ut", "FadeOut")) if e.get(k1)}
            if fades:
                ti.SetFades(fades)
            if e.get("egenskaper"):
                ti.SetProperties(e["egenskaper"])

    trans = 0
    for e, ti in placed:
        o = e.get("overgang")
        if o and ti.GetType() == "video":
            ok = ti.AddTransition({"type": o.get("typ", "Cross Dissolve"), "category": o.get("kategori", "simple"),
                                   "position": o.get("position", "start"), "alignment": o.get("justering", "center"),
                                   "duration": int(o.get("rutor", 10))})
            trans += bool(ok)
            if not ok:
                print(f"övergången gick inte: {e['slag']} {e['kalla']} (handtag?)", flush=True)

    # talet på A1 till tal_lufs; händelser med eget lufs (musik, miljö) för sig
    levels = {}
    for e, ti in placed:
        if ti.GetType() != "audio":
            continue
        if e.get("lufs") is not None:
            levels.setdefault(float(e["lufs"]), []).append(ti)
        elif e["spar"].startswith("AV") or e["spar"] == "A1":
            levels.setdefault(float(f.get("tal_lufs", -14)), []).append(ti)
    for target, group in levels.items():
        if not tl.NormalizeAudioLevel(group, {"normalizationMode": "EBU R128", "targetLoudness": target}):
            print(f"ljudnivån {target} LUFS gick inte att sätta", flush=True)

    colors = {"krok": "Red", "problem": "Orange", "vinst": "Green", "belägg": "Blue", "första-steg": "Cyan", "cta": "Purple"}
    for b, start, length in marks:
        tl.AddMarker(round(start * fps), colors.get(b.get("roll"), "Yellow"), f"{b['id']} {b.get('roll', '')}",
                     (b.get("bild") or "")[:200], max(1, round(length * fps)), b["id"])

    pm.SaveProject()
    report = check(tl, f, placed, marks, total, fps, trans)
    (folder / "bygg.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in report.items():
        print(f"{k}: {v}", flush=True)

    if render:
        project.SetCurrentRenderFormatAndCodec("mp4", "H264")
        h = round(width * int(cfg.get("hojd", 1080)) / int(cfg.get("bredd", 1920)) / 2) * 2
        out = Path(render)
        project.SetRenderSettings({"SelectAllFrames": True, "TargetDir": str(out.parent), "CustomName": out.stem,
                                   "FormatWidth": width, "FormatHeight": h})
        job = project.AddRenderJob()
        project.StartRendering(job)
        while project.IsRenderingInProgress():
            time.sleep(2)
        print("rendering:", project.GetRenderJobStatus(job), flush=True)


def check(tl, f, placed, marks, total, fps, trans):
    """De regler i film-assembly som går att räkna på tidslinjen."""
    t0 = tl.GetStartFrame()
    vids = sorted(((ti.GetStart() - t0) / fps, (ti.GetEnd() - t0) / fps) for e, ti in placed if ti.GetType() == "video")
    cuts = sorted({round(s, 2) for s, _ in vids} | {round(e, 2) for _, e in vids if e < total - 0.05})
    shots = [b - a for a, b in zip(cuts, cuts[1:] + [total]) if b - a > 0.04]
    asl = statistics.mean(shots) if shots else 0
    cv = statistics.pstdev(shots) / asl if shots and asl else 0
    picture = {e["slag"]: min(ti.GetStart() for e2, ti in placed if e2["slag"] == e["slag"] and ti.GetType() == "video")
               for e, _ in placed if e["slag"] != "musik" and any(e2["slag"] == e["slag"] and t.GetType() == "video" for e2, t in placed)}
    sound = {e["slag"]: min(ti.GetStart() for e2, ti in placed if e2["slag"] == e["slag"] and ti.GetType() == "audio")
             for e, _ in placed if e["slag"] != "musik" and any(e2["slag"] == e["slag"] and t.GetType() == "audio" for e2, t in placed)}
    split = sum(1 for k in sound if k in picture and abs(sound[k] - picture[k]) >= 6)
    music = [ti for e, ti in placed if e["slag"] == "musik"]
    music_end = max(((ti.GetEnd() - t0) / fps for ti in music), default=None)
    layers = 0
    aud = [((ti.GetStart() - t0) / fps, (ti.GetEnd() - t0) / fps) for e, ti in placed if ti.GetType() == "audio"]
    for s, _ in aud:
        layers = max(layers, sum(1 for a, b in aud if a <= s < b))
    minutes = max(total / 60, 1e-6)
    res = {
        "längd": f"{total:.1f} s (mål {f.get('mal_sekunder', '?')} s)",
        "bilder": f"{len(shots)}, snittlängd {asl:.1f} s, variation {cv:.2f} {'ok' if cv >= 0.3 else 'ENFORMIGT (<0,3)'}",
        "övergångar": f"{trans} ({trans / minutes:.1f}/min) {'ok' if trans / minutes <= 2 else 'FÖR MÅNGA (>2/min)'}",
        "j- och l-klipp": f"{split} av {len(sound)} slag med ljud har ljudet förskjutet mot bilden",
        "musiken slutar": "ingen musik" if music_end is None else f"{music_end:.2f} s, bilden {total:.2f} s "
                          f"{'ok' if abs(music_end - total) <= 1 / fps + 1e-6 else 'SLUTAR INTE MED BILDEN'}",
        "ljudlager samtidigt": f"{layers} {'ok' if layers <= 5 else 'FÖR MÅNGA (>5)'}",
        "slag utan bild": [b["id"] for b, s, l in marks if b["id"] not in picture] or "inga",
    }
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["manus", "bygg"])
    ap.add_argument("folder", type=Path)
    ap.add_argument("--ersatt", action="store_true")
    ap.add_argument("--render")
    ap.add_argument("--bredd", type=int, default=960)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    f = load(a.folder)
    if a.cmd == "manus":
        write_manus(a.folder, f)
    else:
        write_manus(a.folder, f)
        build(a.folder, f, a.ersatt, a.render, a.bredd)


if __name__ == "__main__":
    main()
