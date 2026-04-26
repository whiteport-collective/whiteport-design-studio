---
name: wds-install
description: Whiteport Design Studio installer and version registry. Fetch this file to install or update WDS. Agents read the versions block to check if skills are current.
wds-version: "1.0.0"
released: "2026-04-26"
repo: "https://github.com/whiteport-collective/whiteport-design-studio"

skills:
  saga: "1.0.0"
  freya: "1.0.0"
  mimir: "1.0.0"
  feedback: "1.0.0"

tools:
  wireframe: "1.0.0"
  sync: "1.0.0"
  git: "1.0.0"
  persona-page: "1.0.0"
  prd-writer: "1.0.0"
  prd-workflow: "1.0.0"

rendering:
  excalidraw: "0.3.0"
  pencil: "0.1.0"
  nanobanana: "0.1.0"
---

# Install Whiteport Design Studio

You are installing Whiteport Design Studio (WDS) — a multi-agent UX and product design methodology.

Follow these steps in order. Do not skip any step.

---

## Step 1 — Detect home directory

Determine the platform and home directory:
- Mac/Linux: run `echo $HOME`
- Windows: run `echo %USERPROFILE%`

Store the result as `{home}`. All WDS files install under `{home}/.claude/`.

---

## Step 2 — Check for existing installation

Check if `{home}/.claude/wds/` exists.

**If it exists — check version:**

Read `{home}/.claude/wds/install.md` (if it exists).

IF `install.md` is missing OR has no `wds-version` in frontmatter:
> ⚠️ Found an older WDS installation at `{home}/.claude/wds/` that is not version-managed.
> It must be removed before installing the new version.
> Remove it and continue? (yes / no)
- If yes: delete `{home}/.claude/wds/` and any old WDS command files from `{home}/.claude/commands/`, then continue
- If no: stop. "Remove `{home}/.claude/wds/` manually, then run the installer again."

IF `install.md` exists and has `wds-version`:
> Found WDS v[installed-version]. This installer is v[this-version].
> Updating to latest — continuing.
Skip to Step 4.

**If it does not exist:** continue to Step 3.

---

## Step 3 — Prepare and install

Create these directories if they do not exist:
- `{home}/.claude/`
- `{home}/.claude/commands/`

Clone the WDS repo:
```bash
git clone https://github.com/whiteport-collective/whiteport-design-studio.git {home}/.claude/wds/
```

---

## Step 4 — Pull latest

```bash
git -C {home}/.claude/wds/ pull
```

Read `{home}/.claude/wds/install.md` frontmatter and note the installed version.

---

## Step 5 — Write wds-config.yaml

Write `{home}/.claude/wds-config.yaml` if it does not already exist:

```yaml
sync-source: https://github.com/whiteport-collective/whiteport-design-studio
branch: main
```

If it already exists: leave it unchanged. The user may have customised the sync source.

---

## Step 6 — Write command files

Write one file per agent to `{home}/.claude/commands/`. Replace `{home}` with the actual expanded path from Step 1.

**`saga.md`**
```
# Saga — WDS Strategic Analyst
WDS base: {home}/.claude/wds/src/skills/saga
Read the file at {home}/.claude/wds/src/skills/saga/SKILL.md and follow the instructions exactly. Resolve all relative file references (workflows/, agents/, references/) against the WDS base path above.
```

**`freya.md`**
```
# Freya — WDS UX Designer
WDS base: {home}/.claude/wds/src/skills/freya
Read the file at {home}/.claude/wds/src/skills/freya/SKILL.md and follow the instructions exactly. Resolve all relative file references (workflows/, agents/, references/) against the WDS base path above.
```

**`mimir.md`**
```
# Mimir — WDS Implementation Agent
WDS base: {home}/.claude/wds/src/skills/mimir
Read the file at {home}/.claude/wds/src/skills/mimir/SKILL.md and follow the instructions exactly. Resolve all relative file references (workflows/, agents/, references/) against the WDS base path above.
```

**`sync.md`**
```
# WDS Sync
WDS base: {home}/.claude/wds
Read the file at {home}/.claude/wds/src/tools/sync/SKILL.md and follow the instructions exactly.
```

---

## Step 7 — Verify

Confirm:
- `{home}/.claude/wds/` exists and contains the repo
- `{home}/.claude/wds-config.yaml` exists
- `{home}/.claude/commands/` contains: `saga.md`, `freya.md`, `mimir.md`, `sync.md`

Print:

```
✓ Whiteport Design Studio installed
  Version: [wds-version from install.md frontmatter]
  Location: {home}/.claude/wds/
  Sync source: [from wds-config.yaml]
  Commands: /saga  /freya  /mimir  /sync
```

---

## Step 8 — Project setup

Ask:

> Which project repo should I set up the design process folder in?
> Give me the path, or say "skip" to do it later.

**If a path is given:**
- Check if `_progress/` exists in that path
- If not: create `_progress/wds-project-outline.yaml` with the starter template below
- Print: "✓ Design process folder ready. Run /saga to start."

**If skipped:**
- Print: "✓ WDS ready. Navigate to a project repo and run /saga."

---

## Starter `wds-project-outline.yaml`

```yaml
wds-version: "1.0.0"
project: ""
created: "{today}"
rendering-tool: excalidraw

phases:
  product-brief: not-started
  trigger-map: not-started
  ux-scenarios: not-started
  ux-design: not-started
  development: not-started

output-folder: docs
```

---

*Whiteport Design Studio — https://github.com/whiteport-collective/whiteport-design-studio*
