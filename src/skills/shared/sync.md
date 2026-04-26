---
name: wds-sync
version: "1.0.0"
description: Syncs all WDS skills from GitHub. Called automatically by agents on startup, or directly by the user at any time.
agents: [saga, freya, mimir]
---

# WDS Sync

Keeps WDS skills current against the GitHub repository.

---

## Entry points

**On agent startup** — run silently. Only surface to the user if:
- WDS is not installed
- Updates were pulled (report what changed)
- An error occurred

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

### 2 — Read local manifest

Read `{home}/.claude/wds/wds-manifest.yaml`.
Note current installed version.

### 3 — Check for updates

```bash
git -C {home}/.claude/wds/ fetch origin
git -C {home}/.claude/wds/ log HEAD..origin/main --oneline
```

IF no changes:
- Startup: finish silently
- Direct call: report "Already up to date."

IF changes found: continue to step 4.

### 4 — Pull updates

```bash
git -C {home}/.claude/wds/ pull
```

Read updated `wds-manifest.yaml`. Note new version.

### 5 — Verify command files

Check that `{home}/.claude/commands/` has: `saga.md`, `freya.md`, `mimir.md`, `sync.md`.
If any are missing: recreate them following install.md Step 4.

### 6 — Report

**Startup:**
> ✓ WDS updated to [new-version] — [N] changes pulled.

**Direct call:**
> WDS synced.
> [list of commit messages pulled]  —or—  Already up to date.
> Version: [version]
> Commands: /saga ✓  /freya ✓  /mimir ✓  /sync ✓
