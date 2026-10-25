"""Bygger en HyperFrames-film ur en Viska-template, kundens designsystem och ett transkript med ordtider.

    python agents/wds/tools/hyperframes/film.py build <film.json> <projektmapp> [--overlay]
    python agents/wds/tools/hyperframes/film.py sheet <video> <kontaktark.jpg> [--every 1.0]

build skriver en vanlig HyperFrames-mapp (index.html med kundens CSS inlagd, assets/) som renderas med npx hyperframes.
Grafiken läggs på orden: varje ruta landar när ordet hörs. Siffror som inte sägs i talet eller står
i film.json under "belagt" stoppar bygget. --overlay utelämnar bildplattan och ger genomskinlig bakgrund,
för ett grafiklager ovanpå filmat material i Resolve.
"""
import argparse, html, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # agents/wds
TEMPLATES = ROOT / "viska" / "templates"
FILM_ROLES = ["--film-ground", "--film-ink", "--film-card", "--film-accent", "--film-accent-ink", "--film-on-plate",
              "--film-font", "--film-heavy", "--film-text", "--film-shadow", "--film-radius", "--film-line",
              "--film-margin", "--film-size-word", "--film-size-then", "--film-size-end", "--film-logo"]


def norm(w):
    return re.sub(r"[^\wåäöÅÄÖ°%]", "", w.lower())


def find_phrase(words, phrase, after=0.0):
    """Första förekomsten av frasen i transkriptet efter tiden after. Returnerar orden med tider."""
    want = [norm(w) for w in phrase.split() if norm(w)]
    toks = [(norm(w["word"]), w) for w in words if norm(w["word"])]
    for i in range(len(toks) - len(want) + 1):
        if toks[i][1]["start"] < after:
            continue
        if [t for t, _ in toks[i:i + len(want)]] == want:
            return [w for _, w in toks[i:i + len(want)]]
    sys.exit(f"Frasen \"{phrase}\" finns inte i transkriptet efter {after} s. Grafiken visar bara det som sägs.")


def check_numbers(texts, words, belagt):
    spoken = {norm(w["word"]) for w in words}
    proven = {n for b in belagt for n in re.findall(r"\d+", b["text"])}
    for t in texts:
        for n in re.findall(r"\d+", t):
            if not any(n in re.findall(r"\d+", s) for s in spoken) and n not in proven:
                sys.exit(f"Siffran {n} i \"{t}\" sägs inte i talet och står inte under \"belagt\" med källa. Inga påhittade siffror.")


def words_html(text, prefix):
    return "".join(f'<span class="w" id="{prefix}{k}">{html.escape(w)}</span>' for k, w in enumerate(text.split()))


def build(film_path, out, overlay):
    film_path = Path(film_path).resolve()
    base = film_path.parent
    f = json.loads(film_path.read_text(encoding="utf-8"))
    tpl = TEMPLATES / f["template"] / "index.html"
    if not tpl.exists():
        sys.exit(f"Templaten {f['template']} finns inte i {TEMPLATES}")
    brand = (base / f["brand"]).resolve()
    tokens, roles = brand / "tokens.css", brand / "film.css"
    for p in (tokens, roles):
        if not p.exists():
            sys.exit(f"{p} saknas. Looken kommer ur kundens brand/design-system/; skriv film.css där (se templatens template.md).")
    missing = [r for r in FILM_ROLES if r not in roles.read_text(encoding="utf-8")]
    if missing:
        sys.exit(f"film.css saknar {', '.join(missing)}")

    words = json.loads((base / f["words"]).read_text(encoding="utf-8"))
    fps, W, H, D = f.get("fps", 25), f.get("width", 1080), f.get("height", 1920), f["duration"]
    cuts = sorted(f.get("cuts", []))
    end_at = f["end"]["at"] if f.get("end") else D

    texts, beats, markup = [], [], []
    out = Path(out)
    (out / "assets").mkdir(parents=True, exist_ok=True)
    # Kundens CSS läggs in i sidan: HyperFrames hittar inte typsnitt i länkade filer och faller då tillbaka på Arial
    brand_css = tokens.read_text(encoding="utf-8") + "\n" + roles.read_text(encoding="utf-8")

    if not overlay:
        shutil.copy2(base / f["plate"], out / "assets" / "plate.mp4")
        markup.append('      <video id="plate" class="clip" src="assets/plate.mp4" data-start="0" '
                      f'data-duration="{D}" data-has-audio="true" data-track-index="0"></video>')

    for i, b in enumerate(f.get("beats", [])):
        hit = find_phrase(words, b["ord"], b.get("efter", 0.0))
        start = hit[0]["start"]
        until = b.get("till") or next((c for c in cuts if c > start), end_at)
        beat = {"word_start": round(start, 3), "until": round(until, 3)}
        texts.append(b["ord"])
        if b.get("linje"):
            lw = find_phrase(words, b["linje"], start)
            beat["line"] = {"start": lw[0]["start"], "end": lw[-1]["end"]}
        then_html = ""
        if b.get("sedan"):
            tw = find_phrase(words, b["sedan"], start)
            beat["then"] = [{"start": w["start"]} for w in tw]
            texts.append(b["sedan"])
            then_html = f'<span class="then" id="b{i}-then">{words_html(b["sedan"], f"b{i}-t")}</span>'
        t_in = max(0.0, start - 0.5)
        dur = round(until - t_in, 3)
        y = b.get("y", 0.62)
        line_html = f'<span class="line" id="b{i}-line"></span>' if b.get("linje") else ""
        markup.append(
            f'      <div id="b{i}" class="beat clip" data-start="{t_in:.3f}" data-duration="{dur}" data-track-index="{i + 1}">\n'
            f'        <div class="box" id="b{i}-box" style="top:{y * 100:.1f}%">\n'
            f'          <div id="b{i}-wrap" style="position:relative;display:inline-block">\n'
            f'            <span class="box-shadow" id="b{i}-shadow"></span><span class="box-card" id="b{i}-card"></span>\n'
            f'            <div class="box-text" id="b{i}-text">{html.escape(b["ord"])}{line_html}</div>\n'
            f'          </div>\n'
            f'          {then_html}\n'
            f'        </div>\n'
            f'      </div>')
        beats.append(beat)

    end = None
    if f.get("end"):
        e = f["end"]
        for key in ("photo", "logo"):
            if e.get(key):
                shutil.copy2(base / e[key], out / "assets" / Path(e[key]).name)
        texts += [e.get("title", ""), e.get("sub", "")]
        end = {"at": e["at"], "title_words": e.get("title", "").split(), "sub_words": e.get("sub", "").split()}
        photo = f'<div id="end-photo-frame"><img id="end-photo" src="assets/{Path(e["photo"]).name}" alt="" ' \
                f'style="object-position:{e.get("focus", "50% 50%")}" /></div>' if e.get("photo") else ""
        logo = f'<img id="end-logo" src="assets/{Path(e["logo"]).name}" alt="" style="top:{e.get("logo_y", 0.86) * 100:.1f}%" />' if e.get("logo") else ""
        t0 = max(0.0, e["at"] - 1.0)
        markup.append(
            f'      <div id="end-host" class="clip" data-start="{t0:.3f}" data-duration="{round(D - t0, 3)}" data-track-index="9" style="position:absolute;inset:0;z-index:3">\n'
            f'        <div id="end"><div id="end-line"></div>\n'
            f'          {photo}\n'
            f'          <div id="end-text" style="top:{e.get("text_y", 0.68) * 100:.1f}%">\n'
            f'            <div id="end-title">{words_html(e.get("title", ""), "end-t")}</div>\n'
            f'            <div id="end-sub">{words_html(e.get("sub", ""), "end-s")}</div>\n'
            f'          </div>\n'
            f'          {logo}\n'
            f'        </div>\n'
            f'      </div>')

    check_numbers([t for t in texts if t], words, f.get("belagt", []))

    data = {"fps": fps, "width": W, "height": H, "duration": D, "beats": beats, "end": end}
    page = tpl.read_text(encoding="utf-8")
    for k, v in {"%%WIDTH%%": str(W), "%%HEIGHT%%": str(H), "%%DURATION%%": str(D),
                 "%%PAGE_BG%%": "transparent" if overlay else "#000", "%%BRAND_CSS%%": brand_css, "%%MARKUP%%": "\n".join(markup),
                 "%%FILM_JSON%%": json.dumps(data, ensure_ascii=False)}.items():
        page = page.replace(k, v)
    (out / "index.html").write_text(page, encoding="utf-8")
    (out / "hyperframes.json").write_text(json.dumps({"paths": {"blocks": "compositions", "assets": "assets"}}, indent=2), encoding="utf-8")
    print(f"{out / 'index.html'}: {len(beats)} ord på bild, slut {'vid ' + str(end['at']) + ' s' if end else 'saknas'}"
          f"{', overlay utan platta' if overlay else ''}")


def sheet(video, out, every):
    """Kontaktark: en bild per `every` sekund, fyra i bredd, med tiden i hörnet."""
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True, check=True).stdout.strip())
    n = int(dur // every) + 1
    rows = -(-n // 4)
    # drawtext behöver en typsnittsfil på Windows (ffmpeg utan fontconfig kraschar annars)
    font = next((p for p in ("C:/Windows/Fonts/arial.ttf", "/System/Library/Fonts/Helvetica.ttc",
                             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf") if Path(p).exists()), None)
    stamp = (f"drawtext=fontfile='{font.replace(':', chr(92) + ':')}':text='%{{pts\\:hms}}':x=8:y=8:fontsize=18:"
             f"fontcolor=white:box=1:boxcolor=black@0.6," if font else "")
    # tidsstämpeln skrivs före urvalet, så den visar den valda bildrutans verkliga tid
    vf = f"scale=270:-2,{stamp}select='isnan(prev_selected_t)+gte(t-prev_selected_t\\,{every}-0.001)',tile=4x{rows}:padding=4:color=white"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-fps_mode", "passthrough", "-frames:v", "1", out], check=True)
    print(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("film"); b.add_argument("out"); b.add_argument("--overlay", action="store_true")
    s = sub.add_parser("sheet"); s.add_argument("video"); s.add_argument("out"); s.add_argument("--every", type=float, default=1.0)
    a = ap.parse_args()
    build(a.film, a.out, a.overlay) if a.cmd == "build" else sheet(a.video, a.out, a.every)
