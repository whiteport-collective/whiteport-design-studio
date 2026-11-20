---
name: sync
type: script
version: "2.0.0"
description: Runs the sync of skills, agents and governance between the WDS repo, the person's private repo, the project repos and the computer's .claude folder. The script is in sync/sync.py.
used_by: [sync-skills, install-wds, librarian, org-onboarding, project-setup]
---

# WDS Sync

How the sync is run. What it is for and when it runs is in the skill [sync-skills](../skills/sync-skills.md).

## Where everything lives

| What | Where |
|---|---|
| The script | `agents/wds/tools/sync/sync.py` in the WDS repo on the computer |
| The person's catalog | `skills.json` in the private cabinet, that is the folder on the `private:` line in `~/.wds/me.md`. If it is missing: `~/.wds/skills.json`. |
| Template for the catalog | `agents/wds/tools/sync/catalog-template.json` |
| State and saved local edits | `~/.claude/.sync-skills-state.json` and `~/.claude/commands-local-edits/` |

**One repo and one private repo are enough** (Mårten, 2026-11-04): the script is in every WDS repo, in the copy of `agents/wds/`, and is kept in step by the sync. Someone who does not spread WDS runs it from there, from their main repo (the organization's repo): `<repo>/agents/wds/tools/sync/sync.py`. Someone who spreads WDS to the repos (the vendor-agents sources) runs it from the WDS repo's own clone, so the latest version is used; in the default location `<dev_root>/whiteport-collective/whiteport-design-studio`.

## Running

**Where the repos live** is in `dev_root:` in each computer's `~/.wds/me.md`. The catalog is shared by all the person's computers, so its paths are written as `<dev_root>/…`; a path written on another computer (`C:/dev/…`) is recalculated from this computer's `dev_root`. If `dev_root:` is missing, the catalog's is used if it exists on the computer, else `~/dev`. The sync's first line says which folder it reads.

Needs Python 3.10 or newer. On a Mac the command is `python3`, and `/usr/bin/python3` is Apple's 3.9: see [machine](machine.md) for how Homebrew's Python comes first. With a Python that is too old the script exits with an error message without writing anything.

```bash
python "<wds-repo>/agents/wds/tools/sync/sync.py"             # full sync
python "<wds-repo>/agents/wds/tools/sync/sync.py" --dry-run   # show only
python "<wds-repo>/agents/wds/tools/sync/sync.py" --no-pull   # skip git pull
```

Unknown flags never sync. The script then shows the help and exits.

## What the script does

1. **Saves local edits.** Commands edited directly in `~/.claude/commands/` since the last sync are copied to `~/.claude/commands-local-edits/` before anything is overwritten.
2. **Fetches the latest version** (`git pull --ff-only`) of every source repo and project repo. Repos with uncommitted changes are skipped.
3. **Runs the sources in the catalog's order.** A later source wins on a name clash.
   - `vendor-agents`: copies `agents/wds/` and the adapters into every WDS repo, and mirrors governance (see below). Only from the source's default branch with no changes, and only to repos on the default branch with no changes. Commit and push of only those files, with the message `agents/wds: synced from <repo> <short sha>` (before 2026-11-14: `agents/wds: synkad från <repo> <short sha>`).
   - `pointer-skills`: writes pointers in `~/.claude/commands/`, one file per agent or skill, that read the original.
   - `capabilities-py`: an older source kind that runs the source's own install script.
4. **Reports clashes**, that is the same command from several sources.

## The catalog

```json
{
  "dev_root": "C:/dev",
  "sources": [ { "name": "...", "kind": "vendor-agents | pointer-skills | ...", "repo": "...", ... } ],
  "project_discovery": { "max_depth": 2, "markers": [".claude/skills", ".claude/commands"] }
}
```

The template shows the default sources: the WDS agents to every WDS repo, the WDS commands globally and the person's private repo last. A new source is a new entry. Each entry has `why`, which explains why the source exists.

## Receipt

The script prints what it did per source, the repos that were skipped with the reason, locally edited commands, clashes and the governance line. The skill summarizes it for the person.

---

## Governance policy

Keeps the policy folders in `governance/` current in every repo where governance is set up, because an agent often sees only one repo. It touches `governance/` only; how `agents/` is synced does not change.

- **On agent startup** it is a dry run: it lists what would change and writes nothing.
- **On a direct request** it writes, commits and pushes, after the person's yes. A real sync writes into repos other than the one the session works in, so it is never run without asking (principle H1 in the WDS default policy). Unknown or misspelled options never start a real sync.

### Folders

Each folder in `governance/` has one owner (`agents/wds/data/repo-structure.md`). A synced folder is a copy of a whole folder, like `agents/wds/`:

| Folder | Source | Synced to |
|---|---|---|
| `governance/wds/` | `agents/wds/data/templates/governance/` in whiteport-design-studio, file names kept (`framework.md`, `principles.md` …) | every repo where governance is set up (G1) |
| `governance/<org>/` | `governance/<org>/` in the organization's one source repo. File names may be localized (`governance/visita/ramverk.md`). | the organization's other repos |
| `governance/<project>/` | the repo itself | never synced |
| `governance/policies.md` | the repo itself. Idun creates it at setup. | never synced |

### The rules

- **A copy is a mirror of its source.** The sync replaces the whole folder: changed files are updated, new files are added, and files removed from the source are removed from the copy.
- **`.source` shows the version.** Every synced folder holds `governance/<folder>/.source` with one line:

  ```
  source: <repo>@<sha>
  ```

  `<repo>` is the source repo and `<sha>` the commit the copy was made from.
- **No `.source`, no write.** The sync writes only into a folder that has `.source`, or creates a folder that does not exist yet (with its `.source`). A folder without `.source` is a source or a local folder: the sync leaves it alone and reports it.
- **A copy is never edited.** Agents never change a folder that has `.source`. Changes are made in the source and reach the copies at the next sync. If a copy differs from the version its `.source` names, it has been edited locally: the sync reports it, leaves it, and offers to move the change to the source.
- **No governance folder, no sync.** `governance/wds/` is written only into a repo that already has a `governance/` folder, or that the sync config names as an organization's source or target. Where Idun has not set up governance there is no `governance/` folder, and the sync does not create one.
- **Only reviewed content spreads.** The source is read from its default branch, committed content only, and only when the source repo's checkout is on its default branch and clean. Otherwise nothing is synced from it, and the sync says why.
- **The target must be ready.** Same conditions as the agent sync: the target repo is on its default branch and clean. Skip and report otherwise.
- `governance/policies.md` and `governance/<project>/` are never touched.

### G1 — Find the repos and the sources

Repos are found by folder name under the dev root, as in the resume step of `agents/wds/data/session.md`. No path is hard-coded: repos are named, and resolved under the dev root.

The organizations come from **the sync config**, the same file that lists the sources of vendor agents to sync. The WDS vendor-agents source has a `governance` list, one entry per organization:

```json
"governance": [
  { "org": "<org>", "governance_source": "<repo>", "repos": ["<repo>", "<repo>"] }
]
```

- `org`: the folder name under `governance/`, lowercase
- `governance_source`: the one repo where `governance/<org>/` is edited
- `repos`: the organization's other repos

**Targets for `governance/wds/`:** every repo that already has a `governance/` folder, plus every `governance_source` and every repo in a `repos` list.
**Targets for `governance/<org>/`:** the repos in its `repos` list, plus every repo whose `governance/<org>/.source` names its `governance_source`, so a repo that has had one sync stays in step even on a machine whose config lacks it.

No `governance` entry: only `governance/wds/` is synced, and only into repos that already have `governance/`.

### G2 — Sync the default

For each target repo except whiteport-design-studio:
1. `governance/wds/` exists without `.source`: skip the repo and report it.
2. Mirror `agents/wds/data/templates/governance/` into `governance/wds/` as it is. The templates link within their folder, so nothing is rewritten.
3. Write `.source`: `source: whiteport-design-studio@<sha>`.
4. Note whether anything changed (for G4).

### G3 — Sync each organization's policy

For each organization, read the committed `governance/<org>/` in `governance_source`. For each of its targets:
1. `governance/<org>/` exists without `.source`: skip and report. It is a source or a local folder.
2. Mirror the folder, then write `.source`: `source: <governance_source>@<sha>`.

The source repo's own `governance/<org>/` has no `.source` and is never written.

### Commit

Commit only `governance/` paths, then push:

```bash
git -C <repo> add -A -- governance/
git -C <repo> commit -m "governance: synced from <source repo> <short sha>" -- governance/
# before 2026-11-14 the message was "governance: synkad från …"
git -C <repo> push
```

### G4 — Flag a conflict check

If G2 changed `governance/wds/` in a repo that holds an organization's policy, report it, in a dry run too:

> The WDS default changed. <org> needs a conflict check: run `/idun audit governance` in <governance_source>.

The check itself is Idun's (`agents/wds/skills/librarian.md`, governance-check). The sync never changes an organization's rules.
