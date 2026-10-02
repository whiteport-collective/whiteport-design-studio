---
name: sync
version: "1.0.0"
description: Syncs all WDS skills from the configured source, and the governance policy into every repo. Called automatically by agents on startup, or directly by the user at any time.
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
> Governance: wds → [N repos] · [org] from [source repo] → [N repos] · [skipped, locally edited]

---

## Governance policy

Runs after step 4 (or after "Already up to date"), in both modes. It keeps the policy folder `governance/` current in every WDS repo, because an agent often sees only one repo. It adds `governance/` only: how `agents/` is synced does not change.

`governance/` is one flat folder at the repo root. Each file name starts with its source:

| Files | Source | Synced to |
|---|---|---|
| `wds-<name>.md` | `agents/wds/idun/templates/governance/<name>.md` in whiteport-design-studio | every WDS repo (a repo with `agents/wds/`) |
| `<org>-<name>.md` (may be localized, e.g. `visita-ramverk.md`) | `governance/<org>-*.md` in the organization's one source repo | the organization's other repos |
| `<project>-<name>.md` | the repo itself | never synced |

Every copy starts with one line, then a blank line, then the source content:

```
Copy. Edit in <source repo>.
```

For `wds-*`: `Copy. Edit in whiteport-design-studio: agents/wds/idun/templates/governance/<name>.md.`

### G1 — Find the repos and the sources

Repos are found by folder name under the dev root, as in the resume step of `agents/wds/shared/data/shared-activation.md`. The organizations come from the same config file as step 2, `{home}/.claude/wds-config.yaml`:

```yaml
dev-root: <folder that holds the repos>   # optional; default: the dev root the resume step uses
governance:
  - org: <org>                            # the file prefix, lowercase
    governance_source: <repo>             # the one repo where governance/<org>-*.md is edited
    repos: [<repo>, <repo>]               # the organization's other repos (optional)
```

An organization's repos are the ones listed in `repos:`, plus every repo whose `governance/` already holds an `<org>-*` copy. Its header names the source, so a repo that has had one sync stays in step even on a machine whose config lacks it. No path is ever hard-coded: repos are named, and resolved under the dev root.

No `governance:` entry and no copies: the organization has no policy of its own yet, and only `wds-*` is synced.

### G2 — Sync the default

For each WDS repo except whiteport-design-studio, for each file in `agents/wds/idun/templates/governance/`:
1. Build the copy: the header line, then the template with the link prefix `{org}-` replaced by `wds-`.
2. Write it to `governance/wds-<name>.md`. Note every file whose content changed (for G4).

### G3 — Sync each organization's policy

For each organization: read the committed `governance/<org>-*.md` files in `governance_source` (never uncommitted changes there). For each of the organization's other repos, write each file with the header `Copy. Edit in <governance_source>.`

### Rules for G2 and G3

- **Never overwrite a file without the copy header.** It is a source or a local edit. Report it as locally edited and offer to move the change to its source, as for agent copies.
- **Never write into the source repo's own `<org>-*` files.**
- **Never delete.** A file removed at the source is reported, not deleted in the copies.
- Same conditions as the agent sync: the target repo is on its default branch and clean. Skip and report otherwise.
- Commit only `governance/` paths, then push:

```bash
git -C <repo> add -- governance/
git -C <repo> commit -m "governance: synced from <source repo> <short sha>" -- governance/
git -C <repo> push
```

### G4 — Flag a conflict check

If G2 changed any `wds-*` file in a repo that also has `<org>-*` files, report, in startup mode too:

> WDS default policy changed. Conflict check due for <org>: run `/idun audit governance` in <governance_source>.

The check itself is Idun's (`agents/wds/idun/skills/librarian.md`, governance-check). The sync never changes an organization's rules.
