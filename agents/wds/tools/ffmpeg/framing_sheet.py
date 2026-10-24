"""Karta för egen omformatering till 9:16: början, en tredjedel, två tredjedelar och slutet av varje videoklipp i klipplistan,
med ett rutnät 1–9 över bredden, så att agenten kan läsa var ansiktena och handlingen är och sätta nyckelpunkterna ("x").

    python framing_sheet.py "<delad enhet>/projects/<projekt>" klipplista.json <utmapp> [--only 5,8]

Skriver <utmapp>/rowNN.jpg (en rad per klipp, NN = platsen i listan) och <utmapp>/karta.jpg med alla rader.
Med "speed" eller "ramp" visas hela den del av originalet som klippet läser.
"""
import argparse, json, subprocess, sys
from pathlib import Path

FONT = "C\\:/Windows/Fonts/arial.ttf" if sys.platform == "win32" else "/System/Library/Fonts/Supplemental/Arial.ttf"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("segments", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--only", help="bara dessa platser i listan, kommaseparerat")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",")} if a.only else None
    segs = json.loads(a.segments.read_text(encoding="utf-8"))
    a.out.mkdir(parents=True, exist_ok=True)
    grid = ",".join(f"drawbox=x=iw*{k / 10}:y=0:w=1:h=ih:color=yellow@0.7:t=1" for k in range(1, 10))
    labels = ",".join(f"drawtext=fontfile='{FONT}':text='{k}':x=w*{k / 10}+2:y=h-18:fontsize=14:fontcolor=yellow" for k in range(1, 10))
    rows = []
    for n, s in enumerate(segs):
        if s.get("still") or (only is not None and n not in only):
            continue
        src = a.project / s["rec"] / "original" / s.get("source", "marten-lumix-s9") / f"{s['stem']}.MP4"
        sd = s["ramp"][-1][0] if s.get("ramp") else s["dur"] * s.get("speed", 1.0)
        tiles = []
        for k, t in enumerate((0.1, sd * 0.33, sd * 0.66, sd - 0.1)):
            tile = a.out / f"seg{n:02}_{k}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['start'] + t:.2f}", "-i", str(src), "-frames:v", "1",
                            "-vf", f"scale=480:-2,{grid},{labels},drawtext=fontfile='{FONT}':text='seg{n:02} {s['stem']} +{t:.1f}s':"
                                   f"x=4:y=4:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6", str(tile)], check=True)
            tiles.append(tile)
        row = a.out / f"row{n:02}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", str(t)] for t in tiles), []),
                        "-filter_complex", "[0:v][1:v][2:v][3:v]hstack=4", "-frames:v", "1", str(row)], check=True)
        for t in tiles:
            t.unlink()
        rows.append(row)
        print(n, s["stem"], flush=True)
    if rows:
        subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", str(r)] for r in rows), []),
                        "-filter_complex", f"vstack={len(rows)}" if len(rows) > 1 else "null", "-frames:v", "1",
                        str(a.out / "karta.jpg")], check=True)
        print(a.out / "karta.jpg")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
