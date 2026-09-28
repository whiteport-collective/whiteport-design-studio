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

## Step: soul

Read the user's soul files before any work. This is how the agent knows who it works with.
Based on Nate B. Jones' two filing cabinets: the **repo cabinet** holds what the person works on here and stays with the project. The **private cabinet** holds who the person is and travels with them.

1. Identify the user per `agents/wds/shared/tools/git.md`. `.wds/me.md` gives `user:` and `private:`.
2. **Repo cabinet:** read `users/<user>/user.md`, `soul.md`, `objectives.md` and `achievements.md`.
3. **Private cabinet:** if `private:` points to a folder on this machine, read `user.md`, `soul.md`, `identity.md`, `objectives.md` and `heartbeat.md` there. **Never read the `private/` subfolder.**
4. Follow both soul files. If they conflict, the repo's soul wins because it is more specific.
5. Keep what you read as the baseline for the session. Wrap compares the session against it (wrap step 4).

Do not print the files. If a file is missing, continue. Wrap creates it when there is something to write.

---

## Step: resume (timestamp)

Used when the agent is started with a resume command: `/saga visita-kommunikation 2026-09-27_13-22`.
First the repo, then the start time of the session that wrote the handover. The repo may be left out.

1. **Right repo?** Compare the repo name with the current repo folder.
   - Same, or no repo given: continue.
   - Different: look for it under the dev root (`C:/dev/*/<repo>` or `~/dev/*/<repo>`). Found: tell the user in one line to start the session there, and stop. Agent sessions should run in the repo they work in. Not found: say the repo is not cloned on this machine and stop.
2. Find the file `sessions/*/<agent_id>/<timestamp>-*.md` (filename: `<session-id>-<från>-<sammandrag>.md`, any user folder including `all-users`). Several matches: prefer the current user's folder, else list them and ask.
3. Read it. Print EXACTLY:

   ── Återupptar <Agent> · <repo> · <timestamp> ─
   Från:   <från> (<user>)
   Nästa:  <first line or step of ## Nästa>
   ──────────────────────────────────────────────
   Kör? (j)

4. On confirmation: set `status: tagen` and `tagen_av: <session-id>` in the file, commit, and start on `## Nästa` immediately. No intro, no recap.
5. No match: say so in one line and continue with the normal activation.

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
