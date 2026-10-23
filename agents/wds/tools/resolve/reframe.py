"""Egen omformatering till 9:16 med följning: varje klipp beskärs med nyckelpunkter som glider mjukt (ease in/out)
mellan varandra, får sin LUT och sparas som ett eget klipp. Utan Smart Reframe (Mårten, 2026-10-23).

    python reframe.py "<delad enhet>/projects/<projekt>" klipplista.json <utmapp> [--size 1080x1920]

I klipplistan har varje videoklipp "x": en lista med rutans mittpunkt över bredden (0 = vänsterkant, 1 = högerkant),
en per nyckelpunkt. Nyckelpunkterna ligger jämnt fördelade i klippet (första vid 0,1 s, sista 0,1 s före slutet), och
utsnittet glider mellan dem med en mjuk kurva (smoothstep), som Ease In/Out i Premiere eller Resolve. Ett enda tal
ger ett fast utsnitt. "speed": 1.7 spelar klippet 1,7 gånger snabbare (läser dur * speed sekunder av originalet). Rutan är alltid så hög som bilden (9:16 ur 3:2 är 37,5 % av bredden; ur en stående bild 84 %).
LUT: <projekt>/resolve/lut/<inspelning>/<klipp>.cube om den finns (looks.py). Klippen sparas som
<utmapp>/segNN-<klipp>.mp4, där NN är platsen i klipplistan, så att reel_assemble.py hittar dem.
"""
import argparse, json, subprocess, sys
from pathlib import Path


def x_expr(xs, dur):
    """ffmpeg-uttryck för rutans mittpunkt (andel av bredden) över tiden t, mjukt mellan nyckelpunkterna."""
    if not isinstance(xs, list):
        xs = [xs]
    if len(xs) == 1:
        return f"{xs[0]}"
    ts = [0.1 + (dur - 0.2) * k / (len(xs) - 1) for k in range(len(xs))]
    expr = f"{xs[-1]}"
    for k in range(len(xs) - 2, -1, -1):
        a, b, t0, t1 = xs[k], xs[k + 1], ts[k], ts[k + 1]
        u = f"clip((t-{t0:.3f})/{t1 - t0:.3f},0,1)"
        seg = f"({a}+({b - a})*({u})*({u})*(3-2*({u})))"
        expr = f"if(lt(t,{t1:.3f}),{seg},{expr})"
    return expr


def render(src: Path, start: float, dur: float, xs, lut: Path | None, out: Path, w: int, h: int, speed: float = 1.0):
    """dur är klippets längd i reelen; med speed > 1 läses dur * speed sekunder av originalet och spelas upp snabbare."""
    src_dur = dur * speed
    cx = x_expr(xs, src_dur)
    vf = []
    if lut and lut.exists():
        vf.append("lut3d='" + str(lut).replace("\\", "/").replace(":", "\\:") + "'")
    # rutan: full höjd, 9:16 bred; mittpunkten följer nyckelpunkterna och hålls innanför bilden
    vf.append(f"crop=w=ih*9/16:h=ih:x='clip(({cx})*iw-ih*9/32,0,iw-ih*9/16)':y=0")
    vf.append(f"scale={w}:{h}:flags=lanczos")
    if speed != 1.0:
        vf.append(f"setpts=(PTS-STARTPTS)/{speed}")
    vf.append("fps=25,format=yuv420p")
    out.parent.mkdir(parents=True, exist_ok=True)
    part = out.with_name(out.stem + ".part.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start}", "-t", f"{src_dur}", "-i", str(src), "-vf", ",".join(vf),
                    "-t", f"{dur}", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-movflags", "+faststart", str(part)], check=True)
    part.replace(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("segments", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--only", help="bara dessa platser i listan, kommaseparerat (till exempel 2,9)")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",")} if a.only else None
    w, h = map(int, a.size.split("x"))
    segs = json.loads(a.segments.read_text(encoding="utf-8"))
    for n, s in enumerate(segs):
        if s.get("still") or (only is not None and n not in only):
            continue
        src = a.project / s["rec"] / "original" / s.get("source", "marten-lumix-s9") / f"{s['stem']}.MP4"
        lut = a.project / "resolve" / "lut" / s["rec"] / f"{s['stem']}.cube"
        out = a.out / f"seg{n:02}-{s['stem']}.mp4"
        render(src, s["start"], s["dur"], s.get("x", 0.5), lut, out, w, h, s.get("speed", 1.0))
        print(f"seg{n:02} {s['stem']} x={s.get('x', 0.5)}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
