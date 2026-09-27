# WDS Shared Activation Steps

Common startup sequence for all WDS agents (Saga, Freya, Mimir).
Each agent's SKILL.md references this file instead of repeating these steps.

---

## Step: sync

Silently sync WDS skills before doing anything else.
Read `agents/wds/shared/tools/sync.md` and run it in startup mode.
If WDS is not installed: print install instructions and stop.
If updates were pulled: note them — report at end of activation.
Continue regardless of sync outcome.

---

## Step: state

Check for session state via the memory tool.
Read `agents/wds/shared/tools/memory.md` and follow the `load` operation for the current agent_id.
If state found: show resume prompt. Wait for user response before continuing.

---

## Step: resume (timestamp)

Used when the agent is started with a timestamp: `/saga 2026-09-27_13-22`.
The timestamp is the start time of the session that wrote the handover.

1. Find the file `sessions/*/<agent_id>/<timestamp>-*.md` (any user folder, including `all-users`). Several matches: prefer the current user's folder, else list them and ask.
2. Read it. Print EXACTLY:

   ── Återupptar <Agent> · <timestamp> ─────────
   Från:   <från> (<user>)
   Nästa:  <first line or step of ## Nästa>
   ──────────────────────────────────────────────
   Kör? (j)

3. On confirmation: set `status: tagen` and `tagen_av: <session-id>` in the file, commit, and start on `## Nästa` immediately. No intro, no recap.
4. No match: say so in one line and continue with the normal activation.

---

## Step: handovers

Read the latest handover to this agent: `sessions/<user>/<agent_id>/` (newest file by name).
Also check `sessions/all-users/<agent_id>/` for files with `status: öppen` (handovers to anyone running this agent).
IF an open handover exists: show it (Nästa + projects) and propose taking it.
When the user accepts: set `status: tagen` and `tagen_av: <session-id>` in the file, commit.
Wrap sets `status: klar` when the work is done. Never delete a handover.

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
