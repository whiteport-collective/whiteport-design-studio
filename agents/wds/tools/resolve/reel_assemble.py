"""Sätter ihop en reel ur klipp renderade per klipp (reel.py --per-clip) och stillbilder, med övertoningar och musik.

    python reel_assemble.py "<delad enhet>/projects/<projekt>" klipplista.json <klippmapp> <ut.mp4> [--music <fil>] [--xfade 0.3]

klipplista.json är samma lista som till reel.py. Videoklipp hämtas som <klippmapp>/segNN*.mp4 (NN = platsen i listan), från reframe.py eller reel.py --per-clip.
Stillbilder ({"still": "<sökväg under projektet>", "move": "pan"|"zoom", "dur": s}) görs rörliga här:
  pan   panorerar långsamt från vänster till höger över bilden i 9:16 (gruppbilder: man ser hela raden)
  zoom  zoomar långsamt in mot mitten (detaljer, dukning), som i film
  push  zoomar in nära mot en person ("focus": [x, y], andel av bilden; "zoom": [från, till]) med en liten glidning, personen i mitten hela tiden
Stillbilderna sparas som <klippmapp>/segNN-still-<bild>.mp4, så att rörelsen syns när klippen läggs i Resolve.
Reelen tonar ut till svart på slutet (--fade-out, 1,2 s).
Varje del ska vara "want" + övertoningen lång (reel.py:s "dur"), så att slutlängden blir summan av "want".
Musiken läggs under hela reelen med mjuk in- och uttoning och ljudnivå för sociala medier (-14 LUFS).
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path

from reframe import encoder   # Intel Quick Sync när den finns, annars libx264

W, H, FPS = 1080, 1920, 25


def image_size(img: Path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", str(img)], capture_output=True, text=True, check=True)
    return tuple(int(v) for v in r.stdout.strip().split(",")[:2])


def still_clip(img: Path, dur: float, move: str, out: Path, focus=None, zoom=(1.25, 1.4)):
    frames = int(round(dur * FPS))
    if move == "push":
        # inzoomning mot en person (focus = [x, y] som andel av bilden), med en liten sidledsglidning
        fx, fy = focus or (0.5, 0.5)
        iw, ih = image_size(img)
        cw = ih * 9 / 16
        left = min(max(fx * iw - cw / 2, 0), iw - cw)
        cx = (fx * iw - left) / cw
        vf = (f"crop={int(cw)}:{ih}:{int(left)}:0,scale={W * 2}:{H * 2},"
              f"zoompan=z='{zoom[0]}+{zoom[1] - zoom[0]:.3f}*on/{frames}':"
              f"x='max(0,min(iw-iw/zoom,({cx:.4f}-0.015+0.03*on/{frames})*iw-iw/zoom/2))':"
              f"y='max(0,min(ih-ih/zoom,{fy:.4f}*ih-ih/zoom/2))':d={frames}:s={W}x{H}:fps={FPS}")
    elif move == "zoom":
        # 9:16 ur mitten, hög upplösning in i zoompan så att rörelsen blir mjuk
        vf = (f"crop=ih*9/16:ih,scale={W * 2}:{H * 2},"
              f"zoompan=z='1+0.10*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}")
    else:
        # panorering vänster till höger över hela bredden, lätt inzoomad så att höjden fylls
        vf = (f"scale=-2:{int(H * 1.08)},crop={W}:{H}:x='(iw-{W})*(0.15+0.70*t/{dur})':y='(ih-{H})/2',fps={FPS}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{dur}", "-i", str(img), "-vf", vf + ",format=yuv420p",
                    "-frames:v", str(frames), *encoder(), "-an", str(out)], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("segments", type=Path)
    ap.add_argument("clips", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--music", type=Path)
    ap.add_argument("--xfade", type=float, default=0.3)
    ap.add_argument("--fade-out", type=float, default=1.2, help="tona ut till svart på slutet, sekunder (0 = ingen)")
    a = ap.parse_args()
    segs = json.loads(a.segments.read_text(encoding="utf-8"))
    X = a.xfade
    with tempfile.TemporaryDirectory() as td:
        parts = []
        for n, s in enumerate(segs):
            if s.get("still"):
                # sparas bland klippen, så att rörelsen följer med när klippen läggs i Resolve
                p = a.clips / f"seg{n:02}-still-{Path(s['still']).stem}.mp4"
                still_clip(a.project / s["still"], s["dur"], s.get("move", "pan"), p, s.get("focus"), s.get("zoom", (1.25, 1.4)))
            else:
                found = sorted(a.clips.glob(f"seg{n:02}*.mp4"))   # segNN.mp4 (reel.py) eller segNN-<klipp>.mp4 (reframe.py)
                found = [f for f in found if ".part" not in f.name]
                if not found:
                    sys.exit(f"saknas: {a.clips}/seg{n:02}*.mp4")
                p = found[0]
            parts.append((p, s["dur"]))
        inputs, chain, offset = [], [], 0.0
        for i, (p, d) in enumerate(parts):
            inputs += ["-i", str(p)]
            chain.append(f"[{i}:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                         f"format=yuv420p,trim=duration={d},setpts=PTS-STARTPTS[v{i}]")
        last = "v0"
        for i in range(1, len(parts)):
            offset += parts[i - 1][1] - X
            chain.append(f"[{last}][v{i}]xfade=transition=fade:duration={X}:offset={offset:.3f}[x{i}]")
            last = f"x{i}"
        total = sum(d for _, d in parts) - X * (len(parts) - 1)
        if a.fade_out:
            chain.append(f"[{last}]fade=t=out:st={total - a.fade_out:.3f}:d={a.fade_out}[vout]")
            last = "vout"
        cmd = ["ffmpeg", "-v", "error", "-y", *inputs]
        maps = ["-map", f"[{last}]"]
        if a.music:
            cmd += ["-i", str(a.music)]
            m = len(parts)
            chain.append(f"[{m}:a]atrim=duration={total},afade=t=in:d=0.4,afade=t=out:st={total - 1.8:.2f}:d=1.8,"
                         f"loudnorm=I=-14:TP=-1.5[a]")
            maps += ["-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
        cmd += ["-filter_complex", ";".join(chain), *maps, *encoder(),
                "-movflags", "+faststart", "-t", f"{total:.3f}", str(a.out)]
        subprocess.run(cmd, check=True)
    print(f"Klar: {a.out} ({total:.1f} s, {len(parts)} delar, övertoning {X} s)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
