#!/usr/bin/env python3
"""
sync.py — dirigent för /sync-skills. Del av WDS (agents/wds/tools/sync.md).

Alla skills har en källa i ett git-repo. Det här skriptet:
  1. Sparar undan skills som ändrats för hand i ~/.claude/commands sedan förra synken
  2. Hämtar senaste versionen (git pull --ff-only) av alla källrepos och projektrepos
  3. Kör varje källas egen installation i ordning (skills.json) — senare vinner
  4. Rapporterar krockar (två källor skriver samma kommando)
  5. vendor-agents: kopierar t.ex. agents/wds/ in i projektrepon som har mappen, commit + push
  6. governance/: speglar WDS-standarden till governance/wds/ i WDS-repon som har governance/,
     och varje organisations governance/<org>/ från sitt källrepo till organisationens andra repon.
     Commit + push av bara de speglade mapparna.

Rör ALDRIG Agent Space-databasen. Tar bara bort filer i en speglad governance/<mapp>/ vars .source
namnger samma källa (filen är borttagen i källan). Inga andra filer tas bort.

    python sync.py              # full synk
    python sync.py --dry-run    # visa vad som skulle hända
    python sync.py --no-pull    # hoppa över git pull

Katalogen (skills.json) är personens egen och ligger i personens privata skåp: mappen som står på
raden "private:" i ~/.wds/me.md. Saknas den används ~/.wds/skills.json. WDS_CATALOG kan peka ut en annan fil.
Mall för en ny katalog: catalog-template.json bredvid skriptet.
"""

import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = Path(__file__).parent


def find_catalog():
    """Personens katalog: WDS_CATALOG, annars skills.json i det privata skåpet (private: i ~/.wds/me.md),
    annars ~/.wds/skills.json."""
    import os
    if os.environ.get("WDS_CATALOG"):
        return Path(os.environ["WDS_CATALOG"])
    me = Path.home() / ".wds" / "me.md"
    if me.exists():
        m = re.search(r"^private:\s*(\S.*?)\s*$", me.read_text(encoding="utf-8", errors="replace"), re.M)
        if m and (Path(m.group(1)) / "skills.json").exists():
            return Path(m.group(1)) / "skills.json"
    return Path.home() / ".wds" / "skills.json"


CATALOG = find_catalog()
if not CATALOG.exists():
    print(f"Ingen skillkatalog hittades ({CATALOG}). Idun skapar den vid installationen: "
          f"kopiera {HERE / 'catalog-template.json'} till ditt privata skåp som skills.json och fyll i den.")
    sys.exit(1)
SOURCES = json.loads(CATALOG.read_text(encoding="utf-8"))
CLAUDE = Path.home() / ".claude"
COMMANDS = CLAUDE / "commands"
STATE = CLAUDE / ".sync-skills-state.json"
BACKUPS = CLAUDE / "commands-local-edits"

ARGS = sys.argv[1:]
DRY = "--dry-run" in ARGS
NO_PULL = "--no-pull" in ARGS
# Okända flaggor (till exempel --help) synkar aldrig: visa hjälpen och avsluta.
# Incident 2026-10-03: "--help" startade en riktig synk.
UNKNOWN = [a for a in ARGS if a not in ("--dry-run", "--no-pull")]
if UNKNOWN:
    print(__doc__)
    print(f"Okänd flagga: {' '.join(UNKNOWN)}. Inget synkades.")
    sys.exit(2)


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def snapshot():
    if not COMMANDS.exists():
        return {}
    return {p.relative_to(COMMANDS).as_posix(): md5(p) for p in COMMANDS.rglob("*") if p.is_file()}


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout + r.stderr).strip()


# ── 1. Lokala ändringar ──────────────────────────────────────────────────────

def rescue_local_edits():
    if not STATE.exists():
        # Första körningen: inget facit — spara hela mappen innan något skrivs över
        if not DRY and COMMANDS.exists():
            dest = BACKUPS / (datetime.now().strftime("%Y-%m-%d-%H%M") + "-forsta-synken")
            shutil.copytree(COMMANDS, dest)
            print(f"Första synken — hela commands/ sparad i {dest}\n")
        return []
    last = json.loads(STATE.read_text(encoding="utf-8"))
    now = snapshot()
    edited = [f for f, h in now.items() if f in last and last[f] != h]
    if edited and not DRY:
        dest = BACKUPS / datetime.now().strftime("%Y-%m-%d-%H%M")
        for f in edited:
            (dest / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(COMMANDS / f, dest / f)
    return edited


# ── 2. Git pull ──────────────────────────────────────────────────────────────

def discover_projects():
    cfg = SOURCES["project_discovery"]
    root = Path(SOURCES["dev_root"])
    found = []
    for depth in range(1, cfg["max_depth"] + 1):
        for d in root.glob("/".join(["*"] * depth)):
            if (d / ".git").exists() and any((d / m).exists() for m in cfg["markers"]):
                found.append(d)
    return found


def pull(repo):
    code, out = run(["git", "status", "--porcelain"], cwd=repo)
    if code != 0:
        return "inte ett git-repo"
    if out:
        return "hoppade över — har osparade ändringar"
    code, out = run(["git", "pull", "--ff-only", "-q"], cwd=repo)
    if code != 0:
        return "pull misslyckades: " + out.splitlines()[-1] if out else "pull misslyckades"
    return None


# ── 3. Källor ────────────────────────────────────────────────────────────────

def src_agent_space_js(s):
    cmd = ["node", "sync.js", "--local", "--no-db"] + (["--dry-run"] if DRY else [])
    code, out = run(cmd, cwd=s["repo"])
    installed = len(re.findall(r"^(?:installed|\[dry-run\] install) ", out, re.M))
    return code == 0, f"{installed} skills" if code == 0 else out[-300:]


def src_capabilities_py(s):
    cmd = [sys.executable, str(Path(s["repo"]) / s["script"]), "--platform", "desktop"] + (["--dry-run"] if DRY else [])
    code, out = run(cmd)
    m = re.search(r"Done: (\d+) capabilities", out)
    return code == 0, f"{m.group(1)} skills" if m else out[-300:]


def src_pointer_skills(s):
    repo = Path(s["repo"])
    targets = {}
    for f in sorted(repo.glob(s["skills_glob"])) if s.get("skills_glob") else []:
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(.+)$", text, re.M)
        # Utan name: mappens namn för skill.md, annars filens namn
        name = (m.group(1).strip() if m else (f.parent.name if f.name.lower() == "skill.md" else f.stem)).strip("\"'")
        prefix = s.get("prefix", "")
        targets[name if name.startswith(prefix) else prefix + name] = f
    for name, rel in s.get("agents", {}).items():
        targets[name] = repo / rel
    for name, f in targets.items():
        if s.get("base") == "repo":
            # WDS: sökvägar i filerna utgår från repots rot, men arbetet sker i det repo man står i
            sub = s.get("subdir", "agents")
            body = (
                f"# {name} (från {repo.name})\n"
                f"Läs filen {f.as_posix()} och följ instruktionerna exakt.\n"
                f"Sökvägar som börjar med `{sub}/` läses från det repo du arbetar i om det har mappen, annars från {repo.as_posix()}. "
                f"Relativa länkar utgår från filens mapp. Allt annat, som sessions/, users/ och projektmappar, gäller det repo du arbetar i.\n"
            )
        else:
            body = (
                f"# {name} (från {repo.name})\n"
                f"Bas: {f.parent.as_posix()}\n"
                f"Läs filen {f.as_posix()} och följ instruktionerna exakt. "
                f"Lös alla relativa filreferenser mot basmappen ovan.\n"
            )
        if not DRY:
            (COMMANDS / f"{name}.md").write_text(body, encoding="utf-8")
    return True, f"{len(targets)} skills"


def owner(repo):
    _, url = run(["git", "remote", "get-url", "origin"], cwd=repo)
    m = re.search(r"github\.com[:/]([^/]+)/", url)
    return m.group(1).lower() if m else ""


def on_default_branch(repo):
    _, cur = run(["git", "branch", "--show-current"], cwd=repo)
    code, ref = run(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"], cwd=repo)
    return cur == (ref.split("/", 1)[1] if code == 0 else cur if cur in ("main", "master") else "")


def all_repos():
    """Alla git-repon under dev_root, ner till project_discovery.max_depth."""
    root = Path(SOURCES["dev_root"])
    found = []
    for depth in range(1, SOURCES["project_discovery"]["max_depth"] + 1):
        found += [d for d in root.glob("/".join(["*"] * depth)) if (d / ".git").exists()]
    return found


def not_ready(repo):
    """Samma villkor som agentsynken: standardbranchen och rent. Returnerar skälet, eller None."""
    if not on_default_branch(repo):
        return "inte på standardbranchen"
    if run(["git", "status", "--porcelain"], cwd=repo)[1]:
        return "osparade ändringar"
    return None


def commit_push(repo, paths, message):
    """Committar bara paths och pushar. Returnerar None om inget ändrades, annars ett kort resultat."""
    run(["git", "add", "--"] + paths, cwd=repo)
    c, _ = run(["git", "diff", "--cached", "--quiet", "--"] + paths, cwd=repo)
    if c == 0:
        return None
    run(["git", "commit", "-q", "-m", message, "--"] + paths, cwd=repo)
    run(["git", "pull", "-q", "--rebase"], cwd=repo)
    pc, pout = run(["git", "push", "-q"], cwd=repo)
    return "uppdaterad" if pc == 0 else f"uppdaterad, PUSH MISSLYCKADES: {pout.splitlines()[-1] if pout else '?'}"


def wds_targets(s):
    """WDS-projekten som får <subdir>: (repon, hoppade över).
    WDS-projekt = har någon av s["markers"] eller <subdir>/.wds-sync. Utan .wds-sync krävs att repot
    ägs av någon i s["owners"] och har en commit inom s["active_days"] dagar.
    Repot måste stå på sin standardbranch och vara rent."""
    root = Path(SOURCES["dev_root"])
    owners = {o.lower() for o in s.get("owners", [])}
    exclude = set(s.get("exclude", []))
    targets, skipped = [], []
    for d in all_repos():
        if d == Path(s["repo"]) or d.name in exclude:
            continue
        opt_in = (d / s["subdir"] / ".wds-sync").exists()
        if not opt_in and not any(any(d.glob(m)) for m in s.get("markers", [])):
            continue
        rel = d.relative_to(root).as_posix()
        if not opt_in and owner(d) not in owners:
            skipped.append(f"{rel} (annan ägare: {owner(d) or 'ingen remote'})")
            continue
        if not opt_in and s.get("active_days"):
            _, ct = run(["git", "log", "-1", "--format=%ct"], cwd=d)
            last = datetime.fromtimestamp(int(ct)) if ct.isdigit() else datetime.min
            if (datetime.now() - last).days > s["active_days"]:
                skipped.append(f"{rel} (inaktivt sedan {last:%Y-%m-%d})")
                continue
        problem = not_ready(d)
        if problem:
            skipped.append(f"{rel} ({problem})")
            continue
        targets.append(d)
    return targets, skipped


def src_vendor_agents(s):
    """Kopierar <repo>/<subdir> till varje WDS-projekt under dev_root (se wds_targets).
    Skriver också adaptrarna i <subdir>/shared/adapters/ till repots rot (.claude/commands, .github/prompts …).
    <subdir> speglas: filer som tagits bort i källan tas bort i kopian (mirror_agents). Committar och pushar bara de filerna.
    Har källan "governance_templates" synkas därefter governance/ (se sync_governance)."""
    src = Path(s["repo"]) / s["subdir"]
    adapters = src / s.get("adapters", "adapters")
    if not adapters.is_dir():
        adapters = src / "shared" / "adapters"  # äldre plats
    # Källan måste stå på sin standardbranch och vara ren, annars sprids en omergad gren.
    # Gäller både agenterna och governance. Incident 2026-10-03: agents/wds synkades från en PR-gren till sex repon.
    _, dirty = run(["git", "status", "--porcelain"], cwd=s["repo"])
    if not on_default_branch(Path(s["repo"])) or dirty:
        _, cur = run(["git", "branch", "--show-current"], cwd=s["repo"])
        return False, (f"källan står på '{cur}'{' med ocommittade ändringar' if dirty else ''}. Agenter och "
                       f"governance synkas bara från standardbranchen utan ändringar. Ingen synk.")
    code, sha = run(["git", "rev-parse", "--short", "HEAD"], cwd=s["repo"])
    targets, skipped = wds_targets(s)
    done = []
    for d in targets:
        if not DRY:
            dest = d / s["subdir"]
            problem = mirror_agents(Path(s["repo"]), s["subdir"], sha, dest)
            if problem:
                skipped.append(f"{d.relative_to(Path(SOURCES['dev_root'])).as_posix()} ({problem})")
                continue
            # Adaptrarna (.claude/commands, .github/prompts …) läggs i repots rot
            paths = [s["subdir"]]
            if adapters.is_dir():
                shutil.copytree(adapters, d, dirs_exist_ok=True)
                paths += [f.relative_to(adapters).as_posix() for f in adapters.rglob("*") if f.is_file()]
            result = commit_push(d, paths, f"{s['subdir']}: synkad från {Path(s['repo']).name} {sha}")
            if result:
                done.append(f"{d.name} ({result})")
                continue
        done.append(d.name)
    info = f"{s['subdir']} {sha} → " + (", ".join(done) or "inga projekt")
    if skipped:
        info += "\n       hoppade över: " + "\n                     ".join(skipped)
    if s.get("governance_templates"):
        info += "\n" + sync_governance(s, targets)
    return True, info


def mirror_agents(src_repo, subdir, src_sha, dest):
    """Speglar <subdir> i källans HEAD till dest. Filer som inte finns i källan tas bort, utom .source och .wds-sync.
    En kopia utan .source räknas som en äldre kopia av samma källa (agents/wds ändras aldrig lokalt).
    Returnerar ett skäl om mappen inte får röras, annars None."""
    have = source_of(dest) if dest.exists() else None
    if have and have != src_repo.name:
        return f"{subdir}/.source namnger {have}, inte {src_repo.name}"
    files = git_files(src_repo, subdir)
    if not files:
        return f"inga committade filer i {src_repo.name}/{subdir}"
    if DRY:
        return None
    keep = {".source", ".wds-sync"}
    for name in files:
        code, body = git_show(src_repo, f"{subdir}/{name}")
        if code != 0:
            return f"kunde inte läsa {subdir}/{name}"
        target = dest / name
        if not target.exists() or not same(target.read_bytes(), body):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
    wanted = set(files)
    if dest.exists():
        for f in sorted(dest.rglob("*")):
            name = f.relative_to(dest).as_posix()
            if f.is_file() and name not in wanted and name not in keep:
                f.unlink()
        for d in sorted((p for p in dest.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
    (dest / ".source").write_text(f"source: {src_repo.name}@{src_sha}\n", encoding="utf-8", newline="\n")
    return None


# ── governance/ ─────────────────────────────────────────────────────────────
# governance/ i ett målrepo består av mappar som var och en speglar en källa:
#   governance/wds/    = <subdir>/<governance_templates>/ i WDS-källrepot → WDS-repon där Idun har kört
#   governance/<org>/  = governance/<org>/ i organisationens källrepo     → organisationens andra repon
# Filerna kopieras som de är, med samma namn. Varje speglad mapp har governance/<mapp>/.source med raden
# "source: <källrepo>@<sha>". En mapp utan .source är en källa eller handgjord och skrivs aldrig i.
# Spegling betyder att filer som tagits bort i källan tas bort i kopian, men bara i en mapp vars .source
# namnger samma källa. Allt läses från källans HEAD (git ls-tree / git show), aldrig från arbetskopian.

def git_show(repo, path):
    """Innehållet i en committad fil (HEAD) som bytes, med originalradbrytningar."""
    r = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=repo, capture_output=True)
    return r.returncode, r.stdout


def git_files(repo, folder):
    """Filerna under folder/ i HEAD, relativt folder. Tom lista om mappen saknas."""
    pre = folder.rstrip("/") + "/"
    _, out = run(["git", "-c", "core.quotepath=off", "ls-tree", "-r", "--name-only", "HEAD", "--", pre], cwd=repo)
    return sorted(p[len(pre):] for p in out.splitlines() if p.startswith(pre))


def source_of(folder):
    """Källrepots namn i <folder>/.source ("source: <repo>@<sha>"), "" om raden saknas, None om filen saknas."""
    f = folder / ".source"
    if not f.is_file():
        return None
    m = re.search(r"^source:\s*([^@\s]+)", f.read_text(encoding="utf-8", errors="replace"), re.M)
    return m.group(1) if m else ""


def same(a, b):
    """Samma innehåll, oavsett radbrytningar (autocrlf ger CRLF i arbetskopian)."""
    return a.replace(b"\r\n", b"\n") == b.replace(b"\r\n", b"\n")


def mirror(src, src_folder, files, src_sha, repo, folder, report):
    """Speglar src_folder i src (HEAD) till repo/governance/<folder>/.
    Returnerar True om något ändrades (eller skulle ändras i dry run)."""
    dest = repo / "governance" / folder
    rel = f"{repo.name}/governance/{folder}"
    if dest.exists():
        have = source_of(dest)
        if have is None:
            report["local"].append(f"{rel}/ (saknar .source: källa eller handgjord mapp)")
            return False
        if have != src.name:
            report["local"].append(f"{rel}/ (.source namnger {have or '?'}, inte {src.name})")
            return False
    plan = {"ny": [], "uppdatera": [], "ta bort": []}
    contents = {}
    for name in files:
        code, body = git_show(src, f"{src_folder}/{name}")
        if code != 0:
            report["missing"].append(f"{src.name}: kunde inte läsa {src_folder}/{name}")
            return False
        contents[name] = body
        target = dest / name
        if not target.exists():
            plan["ny"].append(name)
        elif not same(target.read_bytes(), body):
            plan["uppdatera"].append(name)
    if dest.exists():
        for f in sorted(dest.rglob("*")):
            name = f.relative_to(dest).as_posix()
            if f.is_file() and name != ".source" and name not in contents:
                plan["ta bort"].append(name)
    if not any(plan.values()):
        return False
    report["writes"][rel] = {k: v for k, v in plan.items() if v}
    if not DRY:
        for name in plan["ny"] + plan["uppdatera"]:
            (dest / name).parent.mkdir(parents=True, exist_ok=True)
            (dest / name).write_bytes(contents[name])
        for name in plan["ta bort"]:
            (dest / name).unlink()
        for d in sorted((p for p in dest.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
        (dest / ".source").write_text(f"source: {src.name}@{src_sha}\n", encoding="utf-8", newline="\n")
    return True


def sync_governance(s, wds_repos):
    """governance/wds/ och governance/<org>/. wds_repos = repona som fick <subdir> (på standardbranchen och rena).
    WDS-källrepot är redan kontrollerat (standardbranchen och rent) i src_vendor_agents."""
    wds_src = Path(s["repo"])
    tmpl_rel = f"{s['subdir']}/{s['governance_templates']}"
    _, wds_sha = run(["git", "rev-parse", "--short", "HEAD"], cwd=wds_src)
    report = {"writes": {}, "local": [], "skipped": [], "missing": []}
    touched = {}         # repo → {mapp: "källa@sha"}, för commit
    wds_changed = set()  # repon där governance/wds/ ändrades

    # governance/wds/ bara till WDS-repon där Idun har kört: repon som redan har governance/,
    # och organisationernas käll- och målrepon i konfigurationen. Repon utan governance/ får ingen mapp.
    tmpl_files = git_files(wds_src, tmpl_rel)
    gov_names = set()
    for g in s.get("governance", []):
        gov_names.add(g["governance_source"])
        gov_names.update(g.get("repos", []))
    wds_gov = [r for r in wds_repos if (r / "governance").is_dir() or r.name in gov_names]
    if not tmpl_files:
        report["missing"].append(f"wds: inga committade mallar i {wds_src.name}/{tmpl_rel}/")
    else:
        for repo in wds_gov:
            if mirror(wds_src, tmpl_rel, tmpl_files, wds_sha, repo, "wds", report):
                touched.setdefault(repo, {})["wds"] = f"{wds_src.name}@{wds_sha}"
                wds_changed.add(repo)

    # governance/<org>/ från organisationens källrepo till organisationens andra repon
    by_name = {}
    for d in all_repos():
        by_name.setdefault(d.name, d)
    ready = {r: None for r in wds_repos}  # redan kontrollerade
    orgs = []
    for g in s.get("governance", []):
        org, src_name = g["org"].lower(), g["governance_source"]
        src = by_name.get(src_name)
        if not src:
            report["missing"].append(f"{org}: källrepot {src_name} saknas under {SOURCES['dev_root']}")
            continue
        files = git_files(src, f"governance/{org}")
        _, src_sha = run(["git", "rev-parse", "--short", "HEAD"], cwd=src)
        # Organisationens repon: de listade, plus alla vars governance/<org>/.source namnger källan
        members = []
        for name in g.get("repos", []):
            if name in by_name:
                members.append(by_name[name])
            else:
                report["missing"].append(f"{org}: repot {name} saknas under {SOURCES['dev_root']}")
        for d in by_name.values():
            if d not in members and source_of(d / "governance" / org) == src_name:
                members.append(d)
        members = [d for d in members if d != src]  # källans egen governance/<org>/ rörs aldrig
        orgs.append((org, src_name, src, members))
        if not files:
            report["missing"].append(f"{org}: inga committade filer i {src_name}/governance/{org}/")
            continue
        for repo in members:
            if repo not in ready:
                ready[repo] = not_ready(repo)
            if ready[repo]:
                report["skipped"].append(f"{repo.name} ({org}: {ready[repo]})")
                continue
            if mirror(src, f"governance/{org}", files, src_sha, repo, org, report):
                touched.setdefault(repo, {})[org] = f"{src_name}@{src_sha}"

    # En commit per repo, bara de speglade mapparna
    results = []
    if not DRY:
        for repo, folders in touched.items():
            msg = "governance: synkad från " + ", ".join(dict.fromkeys(folders.values()))
            r = commit_push(repo, [f"governance/{f}" for f in folders], msg)
            if r:
                results.append(f"{repo.name} ({r})")

    # Rapport
    lines = [f"       governance{' (dry run)' if DRY else ''}: wds {wds_sha} → {len(wds_gov)} repon"
             + "".join(f" · {org} från {src_name} → {len(m)} repon" for org, src_name, _, m in orgs)]
    if report["writes"]:
        lines.append(f"         {'skulle ändra' if DRY else 'ändrade'}:")
        for rel, plan in report["writes"].items():
            lines.append(f"           {rel}/: " + " · ".join(f"{v} ({len(fs)}): {', '.join(fs)}" for v, fs in plan.items()))
    for key, title in (("local", "rördes inte"), ("skipped", "hoppade över"), ("missing", "saknas")):
        if report[key]:
            lines.append(f"         {title} ({len(report[key])}):")
            lines += [f"           {x}" for x in report[key]]
    if results:
        lines.append("         committat: " + ", ".join(results))
    # governance/wds/ ändrades i ett repo som hör till organisationen: dags för konfliktkontroll
    for org, src_name, src, members in orgs:
        if wds_changed & set(members + [src]):
            lines.append(f"       WDS-standarden ändrades. Konfliktkontroll behövs för {org}: "
                         f"kör `/idun audit governance` i {src_name}.")
    return "\n".join(lines)


KINDS = {
    "agent-space-js": src_agent_space_js,
    "capabilities-py": src_capabilities_py,
    "pointer-skills": src_pointer_skills,
    "vendor-agents": src_vendor_agents,
}


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    COMMANDS.mkdir(parents=True, exist_ok=True)
    print("=== /sync-skills" + (" (dry run)" if DRY else "") + " ===\n")

    edited = rescue_local_edits()
    if edited:
        print(f"Lokalt ändrade sedan förra synken ({len(edited)}) — sparade i {BACKUPS.name}/ innan överskrivning:")
        for f in edited:
            print(f"  ! {f}")
        print("  Flytta ändringarna till källrepot om de ska behållas.\n")

    source_repos = [Path(s["repo"]) for s in SOURCES["sources"]]
    projects = [p for p in discover_projects() if p not in source_repos]
    if not NO_PULL and not DRY:
        print("Hämtar senaste versionen:")
        for repo in source_repos + projects:
            if not repo.exists():
                print(f"  SAKNAS  {repo} — klona det")
                continue
            problem = pull(repo)
            print(f"  {'!' if problem else 'ok'}  {repo.name}" + (f" — {problem}" if problem else ""))
        print()

    writers = {}
    print("Installerar skills (senare källa vinner):")
    for s in SOURCES["sources"]:
        if not Path(s["repo"]).exists():
            print(f"  SAKNAS  {s['name']}")
            continue
        before = snapshot()
        ok, info = KINDS[s["kind"]](s)
        after = snapshot()
        for f, h in after.items():
            if before.get(f) != h:
                writers.setdefault(f, []).append(s["name"])
        print(f"  {'ok' if ok else 'FEL'}  {s['name']}: {info}")

    clashes = {f: w for f, w in writers.items() if len(w) > 1}
    if clashes:
        print(f"\nKrockar ({len(clashes)}) — samma kommando från flera källor, sista vann:")
        for f, w in sorted(clashes.items()):
            print(f"  {f}: {' → '.join(w)}")

    print(f"\nProjektrepos med egna skills ({len(projects)}) — gäller bara i respektive repo:")
    for p in projects:
        print(f"  {p.relative_to(SOURCES['dev_root']).as_posix()}")

    if not DRY:
        STATE.write_text(json.dumps(snapshot(), indent=1), encoding="utf-8")
    print("\nKlart. Nya skills syns i nästa session.")


if __name__ == "__main__":
    main()
