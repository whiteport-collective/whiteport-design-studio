#!/usr/bin/env python3
"""
render.py: the Trigger Map from one data file to every artefact, the same template every time.
Part of WDS (agents/wds/tools/trigger-map-render.md).

    python render.py <B-Trigger-Map folder>                 # trigger-map.yaml -> md, svg and html
    python render.py <B-Trigger-Map folder> --theme <css>   # a specific theme instead of the visual identity
    python render.py import <B-Trigger-Map folder>          # existing WDS documents -> trigger-map.yaml

The look comes from agents/wds/tools/theme: neutral.css, overridden by the brand's tokens.css
(brand/design-system/tokens.css, nearest level above the folder).
Requires: PyYAML.
"""

import html
import io
import re
import sys
import textwrap
from datetime import date
from pathlib import Path

import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "theme"))
from theme import Theme  # noqa: E402  the shared look, agents/wds/tools/theme
GENERATED = "<!-- Generated from trigger-map.yaml by agents/wds/tools/trigger-map-render. Edit the yaml and render again. -->"
PRIORITY = {
    "primary": ("Primary", "👥"),
    "secondary": ("Secondary", "👤"),
    "tertiary": ("Tertiary", "·"),
    "gatekeeper": ("Gatekeeper", "🔑"),
}


# ── data ────────────────────────────────────────────────────────────────

def slug(text):
    t = text.lower().translate(str.maketrans("åäöé", "aaoe"))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def first_name(name):
    return name.split()[0]


def load(folder):
    path = folder / "trigger-map.yaml"
    if not path.exists():
        sys.exit(f"No trigger-map.yaml in {folder}. Create it, or run: python render.py import {folder}")
    d = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    d.setdefault("goals", [])
    d.setdefault("personas", [])
    d.setdefault("features", [])
    d.setdefault("points", [])
    for i, p in enumerate(d["personas"]):
        p.setdefault("id", slug(first_name(p["name"])))
        p["nn"] = f"{i + 2:02d}"
        p["file"] = f"{p['nn']}-persona-{slug(p['name'])}"
        p.setdefault("priority", "primary")
        p.setdefault("goals", [])
        p.setdefault("forces", [])
        counts = {"+": 0, "-": 0}
        for f in p["forces"]:
            f["dir"] = "-" if str(f.get("dir", "+")).strip() in ("-", "−", "negative") else "+"
            counts[f["dir"]] += 1
            f.setdefault("id", f"{p['id']}.{'p' if f['dir'] == '+' else 'n'}{counts[f['dir']]}")
            f["total"] = int(f.get("f", 0)) + int(f.get("i", 0)) + int(f.get("fit", 0))
            f["persona"] = p
    return d


def forces(d):
    return [f for p in d["personas"] for f in p["forces"]]


def top_forces(p, per_direction):
    out = []
    for direction in "+-":
        fs = sorted([f for f in p["forces"] if f["dir"] == direction], key=lambda f: -f["total"])
        out += fs[:per_direction]
    return out


def feature_scores(d):
    by_id = {f["id"]: f for f in forces(d)}
    rows = []
    for feat in d["features"]:
        per = {p["id"]: 0.0 for p in d["personas"]}
        for fid, s in (feat.get("serves") or {}).items():
            f = by_id.get(fid)
            if f:
                per[f["persona"]["id"]] += float(s) * f["total"] / 15
        rows.append({**feat, "per": per, "weighted": round(sum(per.values()), 1)})
    rows.sort(key=lambda r: -r["weighted"])
    top = rows[0]["weighted"] if rows else 0
    for r in rows:
        r.setdefault("priority", "high" if r["weighted"] >= top * 0.66 else "medium" if r["weighted"] >= top * 0.33 else "low")
    return rows


# ── markdown ────────────────────────────────────────────────────────────

def header(title, lines):
    out = [GENERATED, "", f"# {title}", ""]
    out += [f"> {l}" for l in lines if l]
    return out + ["", "---", ""]


def footer(d, sources):
    out = ["---", "", f"_Produced by Saga, {d.get('date') or date.today().isoformat()}_"]
    if sources:
        out.append(f"_Source: {sources}_")
    return out


def status_line(d, note=None):
    if note:
        return f"Status: {note}"
    return "Status: confirmed" if d.get("status") == "confirmed" else "Status: draft, pending review"


def md_goals(d):
    o = header(f"Business Goals: {d['project']}", ["Phase 2, Trigger Mapping · Workshop 1",
                                                  f"Source: {d['goals_source']}" if d.get("goals_source") else None,
                                                  status_line(d, d.get("goals_status"))])
    o += ["## Vision", "", d.get("vision", "").strip(), "", "---", "", "## Strategic Goals", ""]
    for n, g in enumerate(d["goals"], 1):
        o += [f"### Goal {n}: {g['name']}", ""]
        if g.get("why"):
            o += [g["why"].strip(), ""]
        o += ["| # | Objective | Target |", "|---|-----------|--------|"]
        for k, ob in enumerate(g.get("objectives", []), 1):
            o.append(f"| {n}.{k} | {ob['objective']} | {ob.get('target', '')} |")
        o += ["", "---", ""]
    return o[:-3] + [""] + footer(d, d.get("goals_footer", "01-product-brief.md, Workshop 1"))


def force_table(fs):
    o = ["| # | Force | WHAT | WHY | WHEN | F | I | Fit | Total |", "|---|-------|------|-----|------|---|---|-----|-------|"]
    for f in fs:
        mark = "+" if f["dir"] == "+" else "−"
        o.append(f"| {mark} | **{f['name']}** | {f.get('what', '')} | {f.get('why', '')} | {f.get('when', '')} | "
                 f"{f.get('f', '')} | {f.get('i', '')} | {f.get('fit', '')} | **{f['total']}** |")
    return o


def md_persona(d, p):
    label = PRIORITY.get(p["priority"], (p["priority"].title(), ""))[0]
    first = first_name(p["name"])
    note = p.get("priority_note", "")
    note = (note if note[:1] in ".,:" else " " + note) if note else ""
    o = header(f"{p['name']}: Persona {p['nn']}", [f"Priority: {label}{note}",
                                                   f"Business goals served: {', '.join(p['goals'])}",
                                                   status_line(d, p.get("status_note"))])
    for title, key in ((f"Who {first} Is", "who"), ("Psychological Profile", "psychology"), ("Internal State", "internal_state")):
        if p.get(key):
            o += [f"## {title}", "", p[key].strip(), "", "---", ""]
    u = p.get("usage") or {}
    if u:
        o += ["## Usage Context", ""]
        for lab, key in (("How they find it", "discovery"), ("Emotional state on arrival", "arrival"),
                         ("Behavior pattern", "behaviour"), ("Decision criteria", "decision")):
            if u.get(key):
                o.append(f"**{lab}:** {u[key].strip()}  ")
        o += ["", "---", ""]
    o += ["## Driving Forces", "", "Format: WHAT + WHY + WHEN · Score: Frequency + Intensity + Fit (1–5 each) = /15" + (f" · {d['scores_note']}" if d.get("scores_note") else ""), ""]
    for title, direction in (("Positive Forces", "+"), ("Negative Forces", "-")):
        fs = [f for f in p["forces"] if f["dir"] == direction]
        if fs:
            o += [f"### {title}", ""] + force_table(fs) + [""]
    o += ["---", ""]
    links = p.get("goal_links") or {}
    if links:
        names = {g["id"]: g["name"] for g in d["goals"]}
        o += ["## Relationship to Business Goals", ""]
        o += [f"- ✅ **{gid} {names.get(gid, '')}:** {text.strip()}" for gid, text in links.items()]
        o += [""]
    return o + footer(d, p.get("sources", "the persona workshop, 01-product-brief.md"))


def md_map(d):
    o = header(f"Trigger Map: {d['project']}", ["Phase 2, Trigger Mapping",
                                               "Source: [01-business-goals.md](01-business-goals.md), the persona files, [01-product-brief.md](../A-Product-Brief/01-product-brief.md)",
                                               status_line(d, d.get("status_note"))])
    o += ["## The Map", "", "![The trigger map](00-trigger-map.svg)", "",
          "The poster in full: [00-trigger-map.html](00-trigger-map.html)", "", "---", "",
          "## Business Goals", "", "| Goal | Vision | Key Objectives |", "|------|--------|----------------|"]
    for g in d["goals"]:
        objs = " · ".join(ob.get("short", ob["objective"]) for ob in g.get("objectives", []))
        o.append(f"| {g['id']} | {g['name']} | {objs} |")
    o += ["", "→ Full detail: [01-business-goals.md](01-business-goals.md)", "", "---", "",
          "## Target Groups", "", "| Priority | Persona | Goals served | Persona page |", "|----------|---------|--------------|--------------|"]
    for p in d["personas"]:
        label, icon = PRIORITY.get(p["priority"], (p["priority"].title(), ""))
        who = f"{p['name']}: {p['one_line']}" if p.get("one_line") else p["name"]
        o.append(f"| {icon} {label} | {who} | {', '.join(p['goals'])} | [{p['file']}.md]({p['file']}.md) |")
    o += ["", "---", "", "## Driving Forces: Priority Summary", "",
          "Sorted by FIA score (Frequency + Intensity + Fit /15). Scores of 13 or more are high-priority inputs.", "",
          "| Score | Force | Group | Direction |", "|-------|-------|-------|-----------|"]
    for f in sorted(forces(d), key=lambda f: -f["total"]):
        score = f"**{f['total']}**" if f["total"] >= 13 else str(f["total"])
        direction = "✅ Positive" if f["dir"] == "+" else "❌ Negative"
        o.append(f"| {score} | {f['name']} | {first_name(f['persona']['name'])} | {direction} |")
    if d.get("key_read"):
        o += ["", f"**Key read:** {d['key_read'].strip()}"]
    if d["points"]:
        o += ["", "---", "", "## Points to consider", ""] + [f"- {pt.strip()}" for pt in d["points"]]
    if d["features"]:
        o += ["", "→ Feature impact: [feature-impact.md](feature-impact.md)"]
    return o + ["", ""] + footer(d, "01-business-goals.md, the persona files")


def md_features(d):
    rows = feature_scores(d)
    names = [first_name(p["name"]) for p in d["personas"]]
    o = header(f"Feature Impact Analysis: {d['project']}", ["Phase 2, Trigger Mapping · Workshop 5",
                                                           "Derived from the driving forces in the persona files",
                                                           status_line(d)])
    o += ["## Scoring Method", "", "Each feature is scored 0–3 against the driving forces it serves, weighted by the force's FIA score (/15).", "",
          "---", "", "## Feature Scores", "",
          "| Rank | Feature | " + " | ".join(names) + " | Weighted Total | Priority |",
          "|------|---------|" + "|".join("-" * (len(n) + 2) for n in names) + "|----------------|----------|"]
    for i, r in enumerate(rows, 1):
        per = " | ".join(f"{r['per'][p['id']]:.1f}" for p in d["personas"])
        o.append(f"| {i} | {r['name']} | {per} | {r['weighted']} | {r['priority'].title()} |")
    by_id = {f["id"]: f for f in forces(d)}
    for level in ("high", "medium", "low"):
        rs = [r for r in rows if r["priority"] == level]
        if not rs:
            continue
        o += ["", "---", "", f"## {level.title()} Priority", ""]
        for r in rs:
            served = ", ".join(f"{by_id[k]['name']} ({first_name(by_id[k]['persona']['name'])})" for k in (r.get("serves") or {}) if k in by_id)
            o += [f"**{r['name']}**  ", f"Forces addressed: {served}  "]
            if r.get("implication"):
                o.append(f"Design implication: {r['implication'].strip()}")
            o.append("")
    return o + footer(d, "the persona files")


# ── svg poster ──────────────────────────────────────────────────────────

FS, LH, CW = 13, 17, 7.1  # font size, line height, average character width of the body font


def wrap(text, width):
    return textwrap.wrap(text, max(8, int(width / CW))) or [""]


def node(x, y, w, lines, cls, label=None, score=None):
    h = len(lines) * LH + 22 + (14 if label else 0)
    out = [f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{{radius}}"/>']
    ty = y + 18
    if label:
        out.append(f'<text class="label" x="{x + 14}" y="{ty}">{html.escape(label)}</text>')
        ty += 14
    for line in lines:
        out.append(f'<text class="t {cls}-t" x="{x + 14}" y="{ty + 4}">{html.escape(line)}</text>')
        ty += LH
    if score is not None:
        out.append(f'<text class="score" x="{x + w - 12}" y="{y + 18}" text-anchor="end">{score}</text>')
    return out, h


def edge(x1, y1, x2, y2, cls="edge"):
    dx = (x2 - x1) * 0.5
    return f'<path class="{cls}" d="M{x1},{y1} C{x1 + dx},{y1} {x2 - dx},{y2} {x2},{y2}"/>'


def svg_map(d, t):
    per_dir = int((d.get("map") or {}).get("forces_per_direction", 1))
    cols = {"goal": (40, 230), "product": (340, 200), "group": (610, 220), "force": (900, 300)}
    top, gap_force, gap_group = 96, 10, 30
    body, y = [], top
    group_boxes, force_boxes = [], []
    for p in d["personas"]:
        start = y
        for f in top_forces(p, per_dir):
            x, w = cols["force"]
            lines = wrap(f["name"], w - 60)
            cls = "force-pos" if f["dir"] == "+" else "force-neg"
            mark = "+" if f["dir"] == "+" else "−"
            el, h = node(x, y, w, [f"{mark}  {lines[0]}"] + [f"   {l}" for l in lines[1:]], cls, score=f["total"])
            body += el
            force_boxes.append((p, f, y + h / 2))
            y += h + gap_force
        y = y - gap_force
        x, w = cols["group"]
        label, _ = PRIORITY.get(p["priority"], (p["priority"].title(), ""))
        lines = wrap(p["name"], w - 28)
        gh = len(lines) * LH + 36
        gy = max(start, (start + y) / 2 - gh / 2)
        el, gh = node(x, gy, w, lines, "group", label=label.upper())
        body += el
        group_boxes.append((p, gy + gh / 2))
        y = max(y, gy + gh) + gap_group
    bottom = y - gap_group
    height = bottom - top

    goal_els, goal_hs = [], []
    x, w = cols["goal"]
    for g in d["goals"]:
        lines = wrap(g["name"], w - 28)
        goal_hs.append(len(lines) * LH + 36)
    gsum = sum(goal_hs) + 18 * (len(goal_hs) - 1)
    gy = top + max(0, (height - gsum) / 2)
    goal_mid = []
    for g, h in zip(d["goals"], goal_hs):
        el, h = node(x, gy, w, wrap(g["name"], w - 28), "goal", label=g["id"])
        goal_els += el
        goal_mid.append(gy + h / 2)
        gy += h + 18

    px, pw = cols["product"]
    prod = d.get("product") or {}
    plines = wrap(prod.get("name", d["project"]), pw - 28)
    sub = wrap(prod.get("line", ""), pw - 28) if prod.get("line") else []
    ph = (len(plines) + len(sub)) * LH + 30
    py = top + (height - ph) / 2
    prod_els = [f'<rect class="product" x="{px}" y="{py}" width="{pw}" height="{ph}" rx="{{radius}}"/>']
    ty = py + 22
    for l in plines:
        prod_els.append(f'<text class="t product-t" x="{px + 14}" y="{ty}">{html.escape(l)}</text>')
        ty += LH
    for l in sub:
        prod_els.append(f'<text class="t sub" x="{px + 14}" y="{ty}">{html.escape(l)}</text>')
        ty += LH
    pmid = py + ph / 2

    edges = [edge(cols["goal"][0] + cols["goal"][1], m, px, pmid) for m in goal_mid]
    edges += [edge(px + pw, pmid, cols["group"][0], m) for _, m in group_boxes]
    gmid = {p["id"]: m for p, m in group_boxes}
    edges += [edge(cols["group"][0] + cols["group"][1], gmid[p["id"]], cols["force"][0], m,
                   "edge-pos" if f["dir"] == "+" else "edge-neg") for p, f, m in force_boxes]

    W, H = cols["force"][0] + cols["force"][1] + 40, bottom + 40
    heads = [(cols["goal"][0], "BUSINESS GOALS"), (cols["product"][0], "PRODUCT"), (cols["group"][0], "TARGET GROUPS"), (cols["force"][0], "DRIVING FORCES")]
    v = t.get
    style = f"""
      .bg{{fill:{v('--wds-paper')}}}
      .t{{font-family:{v('--wds-font-body')};font-size:{FS}px;fill:{v('--wds-ink')}}}
      .head{{font-family:{v('--wds-font-mono')};font-size:11px;letter-spacing:.08em;fill:{v('--wds-ink-3')}}}
      .title{{font-family:{v('--wds-font-display')};font-size:22px;fill:{v('--wds-ink')}}}
      .label{{font-family:{v('--wds-font-mono')};font-size:10px;letter-spacing:.06em;fill:{v('--wds-ink-3')}}}
      .score{{font-family:{v('--wds-font-mono')};font-size:12px;fill:{v('--wds-ink-2')}}}
      .goal,.group,.force-pos,.force-neg{{fill:{v('--wds-paper')};stroke:{v('--wds-line')};stroke-width:1}}
      .product{{fill:{v('--wds-ink')};stroke:none}}
      .product-t{{fill:{v('--wds-paper')};font-weight:600}}
      .sub{{fill:{v('--wds-paper')};opacity:.85;font-size:12px}}
      .group-t{{font-weight:600}}
      .force-pos{{stroke:{v('--wds-positive')}}} .force-neg{{stroke:{v('--wds-negative')}}}
      .force-pos-t{{fill:{v('--wds-ink')}}} .force-neg-t{{fill:{v('--wds-ink')}}}
      .edge,.edge-pos,.edge-neg{{fill:none;stroke:{v('--wds-line')};stroke-width:1.2}}
      .edge-pos{{stroke:{v('--wds-positive')};opacity:.55}} .edge-neg{{stroke:{v('--wds-negative')};opacity:.55}}
    """
    radius = re.sub(r"[^\d.]", "", v("--wds-radius", "0")) or "0"
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" role="img" aria-label="Trigger map: {html.escape(d["project"])}">',
             f"<style>{style}</style>", f'<rect class="bg" width="{W}" height="{H:.0f}"/>',
             f'<text class="title" x="40" y="44">{html.escape(d["project"])}</text>']
    parts += [f'<text class="head" x="{x}" y="80">{h}</text>' for x, h in heads]
    parts += edges + goal_els + prod_els + body + ["</svg>"]
    return "\n".join(parts).replace("{radius}", radius)


# ── html ────────────────────────────────────────────────────────────────

def inline(md):
    s = html.escape(md)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    return s


def paras(text):
    return "".join(f"<p>{inline(p.strip())}</p>" for p in re.split(r"\n\s*\n", (text or "").strip()) if p.strip())


PAGE_CSS = """
*{box-sizing:border-box}
body{margin:0;background:var(--wds-paper);color:var(--wds-ink);font:16px/1.6 var(--wds-font-body)}
main{max-width:1240px;margin:0 auto;padding:48px 32px 80px}
.meta{font:12px/1.4 var(--wds-font-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--wds-ink-3)}
h1{font:400 40px/1.15 var(--wds-font-display);margin:.3em 0 .4em}
h2{font:400 26px/1.2 var(--wds-font-display);margin:2.2em 0 .6em;padding-top:1em;border-top:1px solid var(--wds-line)}
.lede{font-size:19px;color:var(--wds-ink-2);max-width:62ch}
.status{display:inline-block;margin-top:8px;padding:6px 12px;border:1px solid var(--wds-line);border-radius:var(--wds-radius);font-size:14px;color:var(--wds-ink-2);max-width:80ch}
.poster{margin:32px 0;overflow-x:auto;border:1px solid var(--wds-line);border-radius:var(--wds-radius)}
.poster svg{display:block;max-width:100%;height:auto}
table{border-collapse:collapse;width:100%;font-size:15px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--wds-line)}
th{font:12px var(--wds-font-mono);letter-spacing:.05em;text-transform:uppercase;color:var(--wds-ink-3);font-weight:400}
td.num{font-family:var(--wds-font-mono);white-space:nowrap}
.pos{color:var(--wds-positive)} .neg{color:var(--wds-negative)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:40px}
@media (max-width:760px){.cols{grid-template-columns:1fr} main{padding:32px 16px}}
.force{padding:14px 0;border-bottom:1px solid var(--wds-line)}
.force b{display:block;font-weight:600}
.force .fia{float:right;font-family:var(--wds-font-mono);color:var(--wds-ink-2)}
.force p{margin:.3em 0 0;color:var(--wds-ink-2);font-size:15px}
.force .k{display:inline-block;width:3.6em;font:11px var(--wds-font-mono);letter-spacing:.05em;text-transform:uppercase;color:var(--wds-ink-3)}
.scene{border-left:2px solid var(--wds-accent);padding-left:16px;color:var(--wds-ink-2);font-style:italic}
a{color:var(--wds-accent-ink)}
footer{margin-top:64px;font-size:13px;color:var(--wds-ink-3)}
"""


def page(title, th, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
{th.style(PAGE_CSS)}</head>
<body><main>
{body}
<footer>Generated from trigger-map.yaml by agents/wds/tools/trigger-map-render.</footer>
</main></body></html>
"""


def html_map(d, svg, th):
    b = [f'<div class="meta">Trigger map · {html.escape(str(d.get("date", "")))}</div>',
         f"<h1>{html.escape(d['project'])}</h1>"]
    if d.get("vision"):
        b.append(f'<p class="lede">{inline(d["vision"].strip())}</p>')
    b.append(f'<div class="status">{inline(status_line(d, d.get("status_note")))}</div>')
    b.append(f'<div class="poster">{svg}</div>')
    b.append("<h2>Business goals</h2><table><tr><th>Goal</th><th>Objective</th><th>Target</th></tr>")
    for g in d["goals"]:
        for k, ob in enumerate(g.get("objectives", []), 1):
            first = f"<strong>{g['id']}</strong> {inline(g['name'])}" if k == 1 else ""
            b.append(f"<tr><td>{first}</td><td>{inline(ob['objective'])}</td><td>{inline(str(ob.get('target', '')))}</td></tr>")
    b.append("</table><h2>Target groups</h2><table><tr><th>Priority</th><th>Persona</th><th>Goals</th></tr>")
    for p in d["personas"]:
        label = PRIORITY.get(p["priority"], (p["priority"].title(), ""))[0]
        who = f'<a href="{p["file"]}.html">{html.escape(p["name"])}</a>' + (f"<br>{inline(p['one_line'])}" if p.get("one_line") else "")
        b.append(f"<tr><td>{label}</td><td>{who}</td><td>{', '.join(p['goals'])}</td></tr>")
    b.append("</table><h2>Driving forces by priority</h2><table><tr><th>FIA</th><th>Force</th><th>Group</th><th>Direction</th></tr>")
    for f in sorted(forces(d), key=lambda f: -f["total"]):
        cls, word = ("pos", "Toward") if f["dir"] == "+" else ("neg", "Away from")
        b.append(f'<tr><td class="num">{f["total"]}</td><td>{inline(f["name"])}</td><td>{html.escape(first_name(f["persona"]["name"]))}</td><td class="{cls}">{word}</td></tr>')
    b.append("</table>")
    if d.get("key_read"):
        b.append(f"<h2>Key read</h2>{paras(d['key_read'])}")
    if d["points"]:
        b.append("<h2>Points to consider</h2><ul>" + "".join(f"<li>{inline(p)}</li>" for p in d["points"]) + "</ul>")
    return page(f"Trigger map: {d['project']}", th, "\n".join(b))


def html_persona(d, p, th):
    label = PRIORITY.get(p["priority"], (p["priority"].title(), ""))[0]
    names = {g["id"]: g["name"] for g in d["goals"]}
    b = [f'<div class="meta">Persona {p["nn"]} · {label} · {html.escape(d["project"])}</div>',
         f"<h1>{html.escape(p['name'])}</h1>"]
    if p.get("one_line"):
        b.append(f'<p class="lede">{inline(p["one_line"])}</p>')
    if p.get("status_note"):
        b.append(f'<div class="status">{inline(p["status_note"])}</div>')
    if p.get("who"):
        b.append(f"<h2>Who {html.escape(first_name(p['name']))} is</h2>{paras(p['who'])}")
    b.append('<h2>What drives them</h2><div class="cols">')
    for title, direction, cls in (("Toward", "+", "pos"), ("Away from", "-", "neg")):
        b.append(f'<div><div class="meta {cls}">{title}</div>')
        for f in sorted([f for f in p["forces"] if f["dir"] == direction], key=lambda f: -f["total"]):
            detail = "".join(f'<p><span class="k">{k}</span>{inline(f[key])}</p>' for k, key in (("What", "what"), ("Why", "why"), ("When", "when")) if f.get(key))
            b.append(f'<div class="force"><span class="fia">{f["total"]}/15</span><b>{inline(f["name"])}</b>{detail}</div>')
        b.append("</div>")
    b.append("</div>")
    if p.get("scenes"):
        b.append("<h2>When they show up</h2>" + "".join(f'<p class="scene">{inline(s)}</p>' for s in p["scenes"]))
    u = p.get("usage") or {}
    if u:
        b.append("<h2>How they meet it</h2><table>")
        for lab, key in (("How they find it", "discovery"), ("On arrival", "arrival"), ("Behaviour", "behaviour"), ("Decides on", "decision")):
            if u.get(key):
                b.append(f"<tr><th>{lab}</th><td>{inline(u[key])}</td></tr>")
        b.append("</table>")
    if p.get("psychology"):
        b.append(f"<h2>How they think</h2>{paras(p['psychology'])}")
    if p.get("internal_state"):
        b.append(f"<h2>What they feel</h2>{paras(p['internal_state'])}")
    if p.get("goal_links"):
        b.append("<h2>Business goals</h2><table>" + "".join(
            f"<tr><th>{gid}</th><td><strong>{inline(names.get(gid, ''))}</strong><br>{inline(t)}</td></tr>" for gid, t in p["goal_links"].items()) + "</table>")
    b.append('<p><a href="00-trigger-map.html">The whole trigger map</a></p>')
    return page(p["name"], th, "\n".join(b))


# ── render ──────────────────────────────────────────────────────────────

def write(path, text):
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8", newline="\n")
    print(f"  {path.name}")


def render(folder, theme_path=None):
    d = load(folder)
    th = Theme(folder, theme_path)
    print(f"Tema: {th.describe()}")
    write(folder / "01-business-goals.md", "\n".join(md_goals(d)))
    for p in d["personas"]:
        write(folder / f"{p['file']}.md", "\n".join(md_persona(d, p)))
        write(folder / f"{p['file']}.html", html_persona(d, p, th))
    svg = svg_map(d, th)
    write(folder / "00-trigger-map.svg", svg)
    write(folder / "00-trigger-map.html", html_map(d, svg, th))
    write(folder / "00-trigger-map.md", "\n".join(md_map(d)))
    if d["features"]:
        write(folder / "feature-impact.md", "\n".join(md_features(d)))
    stale = {f.name for f in folder.glob("[0-9][0-9]-persona-*.*")} - {f"{p['file']}{ext}" for p in d["personas"] for ext in (".md", ".html")}
    for name in sorted(stale):
        print(f"  ! {name} no longer belongs to any persona in trigger-map.yaml. Delete it if it is not needed.")


# ── import ──────────────────────────────────────────────────────────────

def sections(text):
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^## (.+)", line)
        if m:
            cur = m.group(1).strip()
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return {k: re.sub(r"\A(\s*---\s*\n)+|(\n\s*---\s*)+\Z", "", "\n".join(v).strip()).strip() for k, v in out.items()}


def quote(text, key):
    m = re.search(rf"^> {key}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def table_rows(text):
    return [[c.strip() for c in l.strip().strip("|").split("|")] for l in text.splitlines()
            if l.strip().startswith("|") and not re.match(r"^\|\s*-", l.strip()) and not re.match(r"^\|\s*#\s*\|", l.strip())]


def import_md(folder):
    goals_md = (folder / "01-business-goals.md").read_text(encoding="utf-8")
    d = {"project": re.search(r"^# .*?[:—-]\s*(.+)$", goals_md, re.M).group(1).strip(), "status": "draft",
         "date": date.today().isoformat(), "goals": [], "personas": [], "points": []}
    gs = sections(goals_md)
    d["vision"] = gs.get("Vision", "")
    d["goals_status"] = quote(goals_md, "Status")
    d["goals_source"] = quote(goals_md, "Source")
    src = re.findall(r"^_Source: (.+)_$", goals_md, re.M)
    if src:
        d["goals_footer"] = src[-1]
    personas_md = "\n".join(f.read_text(encoding="utf-8") for f in sorted(folder.glob("[0-9][0-9]-persona-*.md")))
    note = re.search(r"/15 · (.+)$", personas_md, re.M)
    if note:
        d["scores_note"] = note.group(1).strip()
    for i, block in enumerate(re.split(r"^### ", gs.get("Strategic Goals", ""), flags=re.M)[1:], 1):
        title, _, rest = block.partition("\n")
        name = re.sub(r"^Goal \d+\s*[:—-]\s*", "", title).strip()
        why = "\n".join(l for l in rest.splitlines() if l.strip() and not l.strip().startswith(("|", "_")) and l.strip() != "---").strip()
        objs = [{"objective": r[1], "target": r[2] if len(r) > 2 else ""} for r in table_rows(rest) if len(r) >= 2]
        d["goals"].append({"id": f"G{i}", "name": name, "why": why, "objectives": objs})

    map_md = (folder / "00-trigger-map.md").read_text(encoding="utf-8") if (folder / "00-trigger-map.md").exists() else ""
    m = re.search(r"P\(\[(.+?)<br/>(.+?)\]\)", map_md)
    if m:
        d["product"] = {"name": m.group(1), "line": m.group(2)}
    ms = sections(map_md)
    goals_by_id = {g["id"]: g for g in d["goals"]}
    for r in table_rows(ms.get("Business Goals", "")):
        if len(r) >= 3 and r[0] in goals_by_id:
            for ob, short in zip(goals_by_id[r[0]]["objectives"], [s.strip() for s in r[2].split("·")]):
                if short and short != ob["objective"]:
                    ob["short"] = short
    one_lines = {}
    for r in table_rows(ms.get("Target Groups", "")):
        if len(r) >= 2 and ":" in r[1]:
            n, _, ol = r[1].partition(":")
            one_lines[n.strip()] = ol.strip()
    k = re.search(r"\*\*Key read:\*\*\s*(.+)", map_md)
    if k:
        d["key_read"] = k.group(1).strip()
    d["points"] = [re.sub(r"^- ", "", l).strip() for l in ms.get("Points to consider", "").splitlines() if l.startswith("- ")]
    d["status_note"] = quote(map_md, "Status")

    for f in sorted(folder.glob("[0-9][0-9]-persona-*.md")):
        t = f.read_text(encoding="utf-8")
        name = re.sub(r"\s*[:—-]\s*Persona \d+$", "", re.search(r"^# (.+)$", t, re.M).group(1)).strip()
        s = sections(t)
        word, _, rest = (quote(t, "Priority") or "Primary").partition(" ")
        p = {"name": name, "priority": word.strip(".,:").lower(),
             "goals": [g.strip() for g in (quote(t, "Business goals served") or "").split(",") if g.strip()]}
        if rest.strip():
            # Keep the note exactly as written, with the punctuation that followed the level ("Gatekeeper. Not a target …").
            p["priority_note"] = (word[-1] + " " if word[-1] in ".,:" else "") + rest.strip()
        if name in one_lines:
            p["one_line"] = one_lines[name]
        note = quote(t, "Status")
        if note:
            p["status_note"] = note
        for key, val in s.items():
            if key.startswith("Who "):
                p["who"] = val
        p["psychology"] = s.get("Psychological Profile", "")
        p["internal_state"] = s.get("Internal State", "")
        usage = {}
        for lab, keyname in (("How", "discovery"), ("Emotional", "arrival"), ("Behavio", "behaviour"), ("Decision", "decision")):
            mm = re.search(rf"^\*\*{lab}[^*]*:\*\*\s*(.+)$", s.get("Usage Context", ""), re.M)
            if mm:
                usage[keyname] = mm.group(1).strip()
        p["usage"] = usage
        p["forces"] = []
        for r in table_rows(s.get("Driving Forces", "")):
            if len(r) >= 9 and r[0] in ("+", "−", "-"):
                p["forces"].append({"dir": "+" if r[0] == "+" else "-", "name": r[1].strip("*"), "what": r[2], "why": r[3], "when": r[4],
                                    "f": int(r[5]), "i": int(r[6]), "fit": int(r[7])})
        links = {}
        for l in s.get("Relationship to Business Goals", "").splitlines():
            mm = re.match(r"^- \S*\s*\*\*(G\d+)[^*]*:\*\*\s*(.+)$", l.strip())
            if mm:
                links[mm.group(1)] = mm.group(2).strip()
        p["goal_links"] = links
        src = re.findall(r"^_Source: (.+)_$", t, re.M)
        if src:
            p["sources"] = src[-1]
        d["personas"].append(p)

    d = {k: v for k, v in d.items() if v not in (None, "", [], {})}
    out = folder / "trigger-map.yaml"
    out.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8", newline="\n")
    print(f"Wrote {out}. Read it through, then render: python render.py {folder}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__)
    elif args[0] == "import":
        import_md(Path(args[1]))
    else:
        th = args[args.index("--theme") + 1] if "--theme" in args else None
        render(Path(args[0]), th)
