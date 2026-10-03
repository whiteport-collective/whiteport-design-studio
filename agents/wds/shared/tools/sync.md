---
name: sync
version: "1.0.0"
description: Syncs all WDS skills from the configured source, and the governance policy folders into every repo where governance is set up. Called automatically by agents on startup, or directly by the user at any time.
agents: [idun, saga, freya, mimir]
---

# WDS Sync

Keeps WDS skills current against the configured source repository.

---

## Entry points

**On agent startup** — run silently. Only surface to the user if:
- WDS is not installed
- Updates were pulled (report what changed)
- An error occurred
- The WDS default policy changed (a conflict check is due, see G4)

**Direct user request** ("sync", "update WDS", "sync all skills", "check for updates") — run verbosely, report each step.

---

## Steps

### 1 — Locate installation

Detect home directory (Mac/Linux: `$HOME`, Windows: `%USERPROFILE%`).
Check if `{home}/.claude/wds/` exists and is a git repo.

IF not found:
> ⚠️ WDS not installed.
> Tell Claude: "install whiteport-design-studio from GitHub" to set it up.

Stop.

### 2 — Read config

Read `{home}/.claude/wds-config.yaml`.

```yaml
sync-source: https://github.com/whiteport-collective/whiteport-design-studio
branch: main
```

If the file does not exist: use defaults above.
Store `sync-source` and `branch` for use in step 3.

Read frontmatter of `{home}/.claude/wds/install.md` — note current `wds-version`.

### 3 — Check for updates

```bash
git -C {home}/.claude/wds/ fetch origin
git -C {home}/.claude/wds/ log HEAD..origin/{branch} --oneline
```

IF no changes:
- Startup: finish silently
- Direct call: report "Already up to date."

IF changes found: continue to step 4.

### 4 — Pull updates

```bash
git -C {home}/.claude/wds/ pull
```

Read updated `install.md` frontmatter. Note new `wds-version`.

### 5 — Verify command files

Check that `{home}/.claude/commands/` has: `idun.md`, `saga.md`, `freya.md`, `mimir.md`, `sync.md`.
If any are missing: recreate them following install.md Step 6.

### 6 — Report

**Startup:**
> ✓ WDS updated to [new-version] — [N] changes pulled.

**Direct call:**
> WDS synced.
> Source: [sync-source]
> [list of commit messages pulled]  —or—  Already up to date.
> Version: [version]
> Commands: /idun ✓  /saga ✓  /freya ✓  /mimir ✓  /sync ✓
> Governance: wds@[sha] → [N repos] · [org] from [source repo]@[sha] → [N repos] · skipped: [repo: no .source / edited locally / not clean]

---

## Governance policy

Keeps the policy folders in `governance/` current in every repo where governance is set up, because an agent often sees only one repo. It touches `governance/` only; how `agents/` is synced does not change.

- **On agent startup** it is a dry run: it lists what would change and writes nothing.
- **On a direct request** it writes, commits and pushes, after the person's yes. A real sync writes into repos other than the one the session works in, so it is never run without asking (principle H1 in the WDS default policy). Unknown or misspelled options never start a real sync.

### Folders

Each folder in `governance/` has one owner (`agents/wds/shared/data/repo-structure.md`). A synced folder is a copy of a whole folder, like `agents/wds/`:

| Folder | Source | Synced to |
|---|---|---|
| `governance/wds/` | `agents/wds/idun/templates/governance/` in whiteport-design-studio, file names kept (`framework.md`, `principles.md` …) | every repo where governance is set up (G1) |
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

Repos are found by folder name under the dev root, as in the resume step of `agents/wds/shared/data/shared-activation.md`. No path is hard-coded: repos are named, and resolved under the dev root.

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
2. Mirror `agents/wds/idun/templates/governance/` into `governance/wds/` as it is. The templates link within their folder, so nothing is rewritten.
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
git -C <repo> push
```

### G4 — Flag a conflict check

If G2 changed `governance/wds/` in a repo that holds an organization's policy, report it, in a dry run too:

> WDS default policy changed. Conflict check due for <org>: run `/idun audit governance` in <governance_source>.

The check itself is Idun's (`agents/wds/idun/skills/librarian.md`, governance-check). The sync never changes an organization's rules.
