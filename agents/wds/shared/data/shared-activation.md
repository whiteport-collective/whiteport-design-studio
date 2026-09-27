# WDS Shared Activation Steps

Common startup sequence for all WDS agents (Saga, Freya, Mimir).
Each agent's SKILL.md references this file instead of repeating these steps.

---

## Step: sync

Silently sync WDS skills before doing anything else.
Read `~/.claude/wds/src/tools/sync/SKILL.md` and run it in startup mode.
If WDS is not installed: print install instructions and stop.
If updates were pulled: note them — report at end of activation.
Continue regardless of sync outcome.

---

## Step: state

Check for session state via the memory tool.
Read `~/.claude/wds/src/tools/memory/SKILL.md` and follow the `load` operation for the current agent_id.
If state found: show resume prompt. Wait for user response before continuing.

---

## Step: scan

Scan workspace for WDS projects:
- Find repos with `_progress/wds-project-outline.yaml` or `_progress/00-design-log.md`
- Skip system repos (bmad-method-wds-expansion, whiteport-design-studio)
- For each project: read design log, note phase status and in-progress work
- Also check current directory for design process folders (A-Product-Brief/ through E-Development/) and any context documents at repo root

---

## Step: select

IF multiple projects found with open work:
  List them, ask which to work on.
IF single project:
  Continue to agent-specific activation.

---

## Step: brownfield-detect

Check if the project has a codebase (src/, backend/, storefront/, app/, or similar code folders at repo root).
IF codebase found → go to agent-specific brownfield handling.
IF no codebase → continue to agent-specific greenfield flow.
