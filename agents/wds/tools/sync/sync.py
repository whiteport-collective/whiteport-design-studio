#!/usr/bin/env python3
"""
sync.py — conductor for /sync-skills. Part of WDS (agents/wds/tools/sync.md).

Every skill has a source in a git repo. This script:
  1. Saves skills edited by hand in ~/.claude/commands since the last sync
  2. Fetches the latest version (git pull --ff-only) of every source repo and project repo
  3. Runs each source's own installation in order (skills.json) — later wins
  4. Reports clashes (two sources writing the same command)
  5. vendor-agents: copies e.g. agents/wds/ into the project repos that have the folder, commit + push
  6. governance/: mirrors the WDS default to governance/wds/ in WDS repos that have governance/,
     and each organization's governance/<org>/ from its source repo to the organization's other repos.
     Commit + push of only the mirrored folders.

NEVER touches the Agent Space database. Only deletes files in a mirrored governance/<folder>/ whose .source
names the same source (the file was deleted in the source). No other files are deleted.

    python sync.py              # full sync
    python sync.py --dry-run    # show what would happen
    python sync.py --no-pull    # skip git pull

The catalog (skills.json) is the person's own and lives in the person's private cabinet: the folder on
the "private:" line in ~/.wds/me.md. If it is missing, ~/.wds/skills.json is used. WDS_CATALOG can point to another file.
Template for a new catalog: catalog-template.json next to the script.
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

# write_text(newline=...) needs 3.10. The Mac's /usr/bin/python3 is Apple's 3.9 and comes before Homebrew in PATH
# if brew shellenv is missing from ~/.zprofile (agents/wds/tools/machine.md).
if sys.version_info < (3, 10):
    sys.exit(f"sync.py needs Python 3.10 or newer, but ran with {sys.version.split()[0]} ({sys.executable}).\n"
             "Install a newer Python and run again. Mac: see agents/wds/tools/machine.md.")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = Path(__file__).parent


def find_catalog():
    """The person's catalog: WDS_CATALOG, else skills.json in the private cabinet (private: in ~/.wds/me.md),
    else ~/.wds/skills.json."""
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
    print(f"No skill catalog found ({CATALOG}). Idun creates it during installation: "
          f"copy {HERE / 'catalog-template.json'} to your private cabinet as skills.json and fill it in.")
    sys.exit(1)
SOURCES = json.loads(CATALOG.read_text(encoding="utf-8"))


def machine_dev_root(catalog_root):
    """Where the repos live on this particular computer. The catalog is shared between the person's computers, so dev_root: in
    ~/.wds/me.md (one per computer) wins; else the catalog's dev_root if it exists here, else ~/dev."""
    me = Path.home() / ".wds" / "me.md"
    if me.exists():
        m = re.search(r"^dev_root:\s*(\S.*?)\s*$", me.read_text(encoding="utf-8", errors="replace"), re.M)
        if m:
            return Path(m.group(1)).expanduser().as_posix()
    if catalog_root and Path(catalog_root).exists():
        return catalog_root
    return (Path.home() / "dev").as_posix()


CATALOG_ROOT = SOURCES.get("dev_root", "")
DEV_ROOT = machine_dev_root(CATALOG_ROOT)


def local_path(p):
    """A path from the catalog on this computer: <dev_root>/…, or a path under the catalog's dev_root
    that was written on another computer (C:/dev/WDS/… becomes ~/dev/WDS/… on a Mac)."""
    if not isinstance(p, str):
        return p
    if p.startswith("<dev_root>"):
        return DEV_ROOT + p[len("<dev_root>"):]
    if CATALOG_ROOT and CATALOG_ROOT != DEV_ROOT and p.lower().startswith(CATALOG_ROOT.lower()):
        return DEV_ROOT + p[len(CATALOG_ROOT):]
    return p


for _s in SOURCES.get("sources", []):
    if "repo" in _s:
        _s["repo"] = local_path(_s["repo"])
SOURCES["dev_root"] = DEV_ROOT
CLAUDE = Path.home() / ".claude"
COMMANDS = CLAUDE / "commands"
STATE = CLAUDE / ".sync-skills-state.json"
BACKUPS = CLAUDE / "commands-local-edits"

ARGS = sys.argv[1:]
DRY = "--dry-run" in ARGS
NO_PULL = "--no-pull" in ARGS
# Unknown flags (for example --help) never sync: show the help and exit.
# Incident 2026-10-03: "--help" started a real sync.
UNKNOWN = [a for a in ARGS if a not in ("--dry-run", "--no-pull")]
if UNKNOWN:
    print(__doc__)
    print(f"Unknown flag: {' '.join(UNKNOWN)}. Nothing was synced.")
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


# ── 1. Local edits ───────────────────────────────────────────────────────────

def rescue_local_edits():
    if not STATE.exists():
        # First run: nothing to compare with — save the whole folder before anything is overwritten
        if not DRY and COMMANDS.exists():
            dest = BACKUPS / (datetime.now().strftime("%Y-%m-%d-%H%M") + "-forsta-synken")
            shutil.copytree(COMMANDS, dest)
            print(f"First sync — all of commands/ saved in {dest}\n")
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
        return "not a git repo"
    if out:
        return "skipped — has uncommitted changes"
    code, out = run(["git", "pull", "--ff-only", "-q"], cwd=repo)
    if code != 0:
        return "pull failed: " + out.splitlines()[-1] if out else "pull failed"
    return None


# ── 3. Sources ───────────────────────────────────────────────────────────────

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
        # Without name: the folder's name for skill.md, else the file's name
        name = (m.group(1).strip() if m else (f.parent.name if f.name.lower() == "skill.md" else f.stem)).strip("\"'")
        prefix = s.get("prefix", "")
        targets[name if name.startswith(prefix) else prefix + name] = f
    for name, rel in s.get("agents", {}).items():
        targets[name] = repo / rel
    for name, f in targets.items():
        # The repo's own command wins over the user-level one (story 5.7 in HeimAI-Dev, 2026-11-20):
        # a Heim points its agents at agents/heim/, and Claude Code would otherwise run this file instead.
        repo_first = (
            f"If the repo you work in has its own `.claude/commands/{name}.md`, read that file and follow it "
            f"instead, and ignore the rest of this one.\n"
        )
        if s.get("base") == "repo":
            # WDS: paths in the files start from the repo root, but the work happens in the repo you stand in
            sub = s.get("subdir", "agents")
            body = (
                f"# {name} (from {repo.name})\n"
                + repo_first +
                f"Read the file {f.as_posix()} and follow the instructions exactly.\n"
                f"Paths that start with `{sub}/` are read from the repo you work in if it has the folder, else from {repo.as_posix()}. "
                f"Relative links start from the file's folder. Everything else, such as sessions/, users/ and project folders, belongs to the repo you work in.\n"
            )
        else:
            body = (
                f"# {name} (from {repo.name})\n"
                + repo_first +
                f"Base: {f.parent.as_posix()}\n"
                f"Read the file {f.as_posix()} and follow the instructions exactly. "
                f"Resolve every relative file reference against the base folder above.\n"
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
    """All git repos under dev_root, down to project_discovery.max_depth."""
    root = Path(SOURCES["dev_root"])
    found = []
    for depth in range(1, SOURCES["project_discovery"]["max_depth"] + 1):
        found += [d for d in root.glob("/".join(["*"] * depth)) if (d / ".git").exists()]
    return found


def not_ready(repo):
    """Same conditions as the agent sync: the default branch and clean. Returns the reason, or None."""
    if not on_default_branch(repo):
        return "not on the default branch"
    if run(["git", "status", "--porcelain"], cwd=repo)[1]:
        return "uncommitted changes"
    return None


def commit_push(repo, paths, message):
    """Commits only paths and pushes. Returns None if nothing changed, else a short result."""
    run(["git", "add", "--"] + paths, cwd=repo)
    c, _ = run(["git", "diff", "--cached", "--quiet", "--"] + paths, cwd=repo)
    if c == 0:
        return None
    run(["git", "commit", "-q", "-m", message, "--"] + paths, cwd=repo)
    run(["git", "pull", "-q", "--rebase"], cwd=repo)
    pc, pout = run(["git", "push", "-q"], cwd=repo)
    return "updated" if pc == 0 else f"updated, PUSH FAILED: {pout.splitlines()[-1] if pout else '?'}"


def wds_targets(s):
    """The WDS projects that get <subdir>: (repos, skipped).
    WDS project = has one of s["markers"] or <subdir>/.wds-sync. Without .wds-sync the repo must be
    owned by someone in s["owners"] and have a commit within s["active_days"] days.
    The repo must be on its default branch and clean."""
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
            skipped.append(f"{rel} (other owner: {owner(d) or 'no remote'})")
            continue
        if not opt_in and s.get("active_days"):
            _, ct = run(["git", "log", "-1", "--format=%ct"], cwd=d)
            last = datetime.fromtimestamp(int(ct)) if ct.isdigit() else datetime.min
            if (datetime.now() - last).days > s["active_days"]:
                skipped.append(f"{rel} (inactive since {last:%Y-%m-%d})")
                continue
        problem = not_ready(d)
        if problem:
            skipped.append(f"{rel} ({problem})")
            continue
        targets.append(d)
    return targets, skipped


def src_vendor_agents(s):
    """Copies <repo>/<subdir> to every WDS project under dev_root (see wds_targets).
    Also writes the adapters in <subdir>/shared/adapters/ to the repo root (.claude/commands, .github/prompts …).
    <subdir> is mirrored: files deleted in the source are deleted in the copy (mirror_agents). Commits and pushes only those files.
    If the source has "governance_templates", governance/ is synced afterwards (see sync_governance)."""
    src = Path(s["repo"]) / s["subdir"]
    adapters = src / s.get("adapters", "adapters")
    if not adapters.is_dir():
        adapters = src / "shared" / "adapters"  # older location
    # The source must be on its default branch and clean, or an unmerged branch spreads.
    # Applies to both the agents and governance. Incident 2026-10-03: agents/wds was synced from a PR branch to six repos.
    _, dirty = run(["git", "status", "--porcelain"], cwd=s["repo"])
    if not on_default_branch(Path(s["repo"])) or dirty:
        _, cur = run(["git", "branch", "--show-current"], cwd=s["repo"])
        return False, (f"the source is on '{cur}'{' with uncommitted changes' if dirty else ''}. Agents and "
                       f"governance are synced only from the default branch with no changes. No sync.")
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
            # The adapters (.claude/commands, .github/prompts …) go in the repo root
            paths = [s["subdir"]]
            if adapters.is_dir():
                shutil.copytree(adapters, d, dirs_exist_ok=True)
                paths += [f.relative_to(adapters).as_posix() for f in adapters.rglob("*") if f.is_file()]
            result = commit_push(d, paths, f"{s['subdir']}: synced from {Path(s['repo']).name} {sha}")
            if result:
                done.append(f"{d.name} ({result})")
                continue
        done.append(d.name)
    info = f"{s['subdir']} {sha} → " + (", ".join(done) or "no projects")
    if skipped:
        info += "\n       skipped: " + "\n                ".join(skipped)
    if s.get("governance_templates"):
        info += "\n" + sync_governance(s, targets)
    return True, info


def mirror_agents(src_repo, subdir, src_sha, dest):
    """Mirrors <subdir> in the source's HEAD to dest. Files not in the source are deleted, except .source and .wds-sync.
    A copy without .source counts as an older copy of the same source (agents/wds is never changed locally).
    Returns a reason if the folder must not be touched, else None."""
    have = source_of(dest) if dest.exists() else None
    if have and have != src_repo.name:
        return f"{subdir}/.source names {have}, not {src_repo.name}"
    files = git_files(src_repo, subdir)
    if not files:
        return f"no committed files in {src_repo.name}/{subdir}"
    if DRY:
        return None
    keep = {".source", ".wds-sync"}
    for name in files:
        code, body = git_show(src_repo, f"{subdir}/{name}")
        if code != 0:
            return f"could not read {subdir}/{name}"
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
# governance/ in a target repo consists of folders that each mirror one source:
#   governance/wds/    = <subdir>/<governance_templates>/ in the WDS source repo → WDS repos where Idun has run
#   governance/<org>/  = governance/<org>/ in the organization's source repo      → the organization's other repos
# The files are copied as they are, with the same names. Each mirrored folder has governance/<folder>/.source with the line
# "source: <source repo>@<sha>". A folder without .source is a source or hand-made and is never written to.
# Mirroring means files deleted in the source are deleted in the copy, but only in a folder whose .source
# names the same source. Everything is read from the source's HEAD (git ls-tree / git show), never from the working copy.

def git_show(repo, path):
    """The content of a committed file (HEAD) as bytes, with the original line endings."""
    r = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=repo, capture_output=True)
    return r.returncode, r.stdout


def git_files(repo, folder):
    """The files under folder/ in HEAD, relative to folder. Empty list if the folder is missing."""
    pre = folder.rstrip("/") + "/"
    _, out = run(["git", "-c", "core.quotepath=off", "ls-tree", "-r", "--name-only", "HEAD", "--", pre], cwd=repo)
    return sorted(p[len(pre):] for p in out.splitlines() if p.startswith(pre))


def source_of(folder):
    """The source repo's name in <folder>/.source ("source: <repo>@<sha>"), "" if the line is missing, None if the file is missing."""
    f = folder / ".source"
    if not f.is_file():
        return None
    m = re.search(r"^source:\s*([^@\s]+)", f.read_text(encoding="utf-8", errors="replace"), re.M)
    return m.group(1) if m else ""


def same(a, b):
    """Same content, regardless of line endings (autocrlf gives CRLF in the working copy)."""
    return a.replace(b"\r\n", b"\n") == b.replace(b"\r\n", b"\n")


def mirror(src, src_folder, files, src_sha, repo, folder, report):
    """Mirrors src_folder in src (HEAD) to repo/governance/<folder>/.
    Returns True if anything changed (or would change in a dry run)."""
    dest = repo / "governance" / folder
    rel = f"{repo.name}/governance/{folder}"
    if dest.exists():
        have = source_of(dest)
        if have is None:
            report["local"].append(f"{rel}/ (no .source: a source or hand-made folder)")
            return False
        if have != src.name:
            report["local"].append(f"{rel}/ (.source names {have or '?'}, not {src.name})")
            return False
    plan = {"new": [], "update": [], "delete": []}
    contents = {}
    for name in files:
        code, body = git_show(src, f"{src_folder}/{name}")
        if code != 0:
            report["missing"].append(f"{src.name}: could not read {src_folder}/{name}")
            return False
        contents[name] = body
        target = dest / name
        if not target.exists():
            plan["new"].append(name)
        elif not same(target.read_bytes(), body):
            plan["update"].append(name)
    if dest.exists():
        for f in sorted(dest.rglob("*")):
            name = f.relative_to(dest).as_posix()
            if f.is_file() and name != ".source" and name not in contents:
                plan["delete"].append(name)
    if not any(plan.values()):
        return False
    report["writes"][rel] = {k: v for k, v in plan.items() if v}
    if not DRY:
        for name in plan["new"] + plan["update"]:
            (dest / name).parent.mkdir(parents=True, exist_ok=True)
            (dest / name).write_bytes(contents[name])
        for name in plan["delete"]:
            (dest / name).unlink()
        for d in sorted((p for p in dest.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
        (dest / ".source").write_text(f"source: {src.name}@{src_sha}\n", encoding="utf-8", newline="\n")
    return True


def sync_governance(s, wds_repos):
    """governance/wds/ and governance/<org>/. wds_repos = the repos that got <subdir> (on the default branch and clean).
    The WDS source repo is already checked (default branch and clean) in src_vendor_agents."""
    wds_src = Path(s["repo"])
    tmpl_rel = f"{s['subdir']}/{s['governance_templates']}"
    _, wds_sha = run(["git", "rev-parse", "--short", "HEAD"], cwd=wds_src)
    report = {"writes": {}, "local": [], "skipped": [], "missing": []}
    touched = {}         # repo → {folder: "source@sha"}, for the commit
    wds_changed = set()  # repos where governance/wds/ changed

    # governance/wds/ only to WDS repos where Idun has run: repos that already have governance/,
    # and the organizations' source and target repos in the configuration. Repos without governance/ get no folder.
    tmpl_files = git_files(wds_src, tmpl_rel)
    gov_names = set()
    for g in s.get("governance", []):
        gov_names.add(g["governance_source"])
        gov_names.update(g.get("repos", []))
    wds_gov = [r for r in wds_repos if (r / "governance").is_dir() or r.name in gov_names]
    if not tmpl_files:
        report["missing"].append(f"wds: no committed templates in {wds_src.name}/{tmpl_rel}/")
    else:
        for repo in wds_gov:
            if mirror(wds_src, tmpl_rel, tmpl_files, wds_sha, repo, "wds", report):
                touched.setdefault(repo, {})["wds"] = f"{wds_src.name}@{wds_sha}"
                wds_changed.add(repo)

    # governance/<org>/ from the organization's source repo to the organization's other repos
    by_name = {}
    for d in all_repos():
        by_name.setdefault(d.name, d)
    ready = {r: None for r in wds_repos}  # already checked
    orgs = []
    for g in s.get("governance", []):
        org, src_name = g["org"].lower(), g["governance_source"]
        src = by_name.get(src_name)
        if not src:
            report["missing"].append(f"{org}: the source repo {src_name} is missing under {SOURCES['dev_root']}")
            continue
        files = git_files(src, f"governance/{org}")
        _, src_sha = run(["git", "rev-parse", "--short", "HEAD"], cwd=src)
        # The organization's repos: the listed ones, plus all whose governance/<org>/.source names the source
        members = []
        for name in g.get("repos", []):
            if name in by_name:
                members.append(by_name[name])
            else:
                report["missing"].append(f"{org}: the repo {name} is missing under {SOURCES['dev_root']}")
        for d in by_name.values():
            if d not in members and source_of(d / "governance" / org) == src_name:
                members.append(d)
        members = [d for d in members if d != src]  # the source's own governance/<org>/ is never touched
        orgs.append((org, src_name, src, members))
        if not files:
            report["missing"].append(f"{org}: no committed files in {src_name}/governance/{org}/")
            continue
        for repo in members:
            if repo not in ready:
                ready[repo] = not_ready(repo)
            if ready[repo]:
                report["skipped"].append(f"{repo.name} ({org}: {ready[repo]})")
                continue
            if mirror(src, f"governance/{org}", files, src_sha, repo, org, report):
                touched.setdefault(repo, {})[org] = f"{src_name}@{src_sha}"

    # One commit per repo, only the mirrored folders
    results = []
    if not DRY:
        for repo, folders in touched.items():
            msg = "governance: synced from " + ", ".join(dict.fromkeys(folders.values()))
            r = commit_push(repo, [f"governance/{f}" for f in folders], msg)
            if r:
                results.append(f"{repo.name} ({r})")

    # Report
    lines = [f"       governance{' (dry run)' if DRY else ''}: wds {wds_sha} → {len(wds_gov)} repos"
             + "".join(f" · {org} from {src_name} → {len(m)} repos" for org, src_name, _, m in orgs)]
    if report["writes"]:
        lines.append(f"         {'would change' if DRY else 'changed'}:")
        for rel, plan in report["writes"].items():
            lines.append(f"           {rel}/: " + " · ".join(f"{v} ({len(fs)}): {', '.join(fs)}" for v, fs in plan.items()))
    for key, title in (("local", "not touched"), ("skipped", "skipped"), ("missing", "missing")):
        if report[key]:
            lines.append(f"         {title} ({len(report[key])}):")
            lines += [f"           {x}" for x in report[key]]
    if results:
        lines.append("         committed: " + ", ".join(results))
    # governance/wds/ changed in a repo that belongs to the organization: time for a conflict check
    for org, src_name, src, members in orgs:
        if wds_changed & set(members + [src]):
            lines.append(f"       The WDS default changed. {org} needs a conflict check: "
                         f"run `/idun audit governance` in {src_name}.")
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
    print("=== /sync-skills" + (" (dry run)" if DRY else "") + " ===")
    where = "" if DEV_ROOT == CATALOG_ROOT else f" (the catalog says {CATALOG_ROOT})"
    print(f"The repos on this computer: {DEV_ROOT}{where}\n")

    edited = rescue_local_edits()
    if edited:
        print(f"Edited locally since the last sync ({len(edited)}) — saved in {BACKUPS.name}/ before overwriting:")
        for f in edited:
            print(f"  ! {f}")
        print("  Move the changes to the source repo if they are to be kept.\n")

    source_repos = [Path(s["repo"]) for s in SOURCES["sources"]]
    projects = [p for p in discover_projects() if p not in source_repos]
    if not NO_PULL and not DRY:
        print("Fetching the latest version:")
        for repo in source_repos + projects:
            if not repo.exists():
                print(f"  MISSING  {repo} — clone it")
                continue
            problem = pull(repo)
            print(f"  {'!' if problem else 'ok'}  {repo.name}" + (f" — {problem}" if problem else ""))
        print()

    writers = {}
    print("Installing skills (later source wins):")
    for s in SOURCES["sources"]:
        if not Path(s["repo"]).exists():
            print(f"  MISSING  {s['name']}")
            continue
        before = snapshot()
        ok, info = KINDS[s["kind"]](s)
        after = snapshot()
        for f, h in after.items():
            if before.get(f) != h:
                writers.setdefault(f, []).append(s["name"])
        print(f"  {'ok' if ok else 'ERROR'}  {s['name']}: {info}")

    clashes = {f: w for f, w in writers.items() if len(w) > 1}
    if clashes:
        print(f"\nClashes ({len(clashes)}) — the same command from several sources, the last one won:")
        for f, w in sorted(clashes.items()):
            print(f"  {f}: {' → '.join(w)}")

    print(f"\nProject repos with their own skills ({len(projects)}) — apply only in their own repo:")
    for p in projects:
        print(f"  {p.relative_to(SOURCES['dev_root']).as_posix()}")

    if not DRY:
        STATE.write_text(json.dumps(snapshot(), indent=1), encoding="utf-8")
    print("\nDone. New skills show up in the next session.")


if __name__ == "__main__":
    main()
