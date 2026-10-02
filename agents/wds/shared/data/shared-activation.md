# WDS Shared Activation Steps

Common startup sequence for all WDS agents (Idun, Saga, Freya, Mimir).
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

1. Identify the user per `agents/wds/shared/tools/git.md`.
2. **New user?** If `users/<user>/` doesn't exist, tell the person in one line that they are new and that their soul files will be built from the sessions. Create the folder from `users/_template/` and go straight on to the work. No interview is needed. Wrap asks where the private cabinet should live.
3. **Repo cabinet:** read `users/<user>/user.md`, `soul.md`, `objectives.md` and `achievements.md`.
4. **Private cabinet:** its location is `private:`. Read it from `.wds/me.md` first, then from `users/<user>/user.md`. It can be a local folder or a repo. For a repo, find its folder on this machine. If found, read `user.md`, `soul.md`, `identity.md`, `objectives.md` and `heartbeat.md` there. **Never read the `private/` subfolder.**
5. Follow both soul files. If they conflict, the repo's soul wins because it is more specific.
6. Keep what you read as the baseline for the session. Wrap compares the session against it (wrap step 4).
7. **Skills:** if the private cabinet has a skills catalog (`skills.md`), follow its section on what to run before each session, so the latest versions are installed locally.

Do not print the files. If a file is missing, continue. Wrap creates it when there is something to write.

Then run "Step: governance". Every agent that runs this step runs that one too.

---

## Step: governance

Read the policy before any work, and follow it. It lives in `governance/` at the repo root, one flat folder, each file prefixed with its source (`agents/wds/shared/tools/sync.md`, Governance policy).

1. **Read the principles, in this order:**
   - `governance/wds-principles.md`: the WDS default
   - the organization's principles: `governance/<org>-principles.md`, or the localized file that the organization's framework file links to (Visita: `visita-principer.md`, linked from `visita-ramverk.md`)
   - this repo's tightenings, if any: `governance/<project>-*.md`
   Each file states its level on its `Level:` line (default, organization, project).
2. **Follow them.** The organization's policy is complete on its own; the default applies only where it is silent. A lower level may tighten a rule, never loosen it. When two levels say different things, the stricter one wins, unless the organization's framework file lists the difference with a reason.
3. **Read the other policy files when a task touches their area:** tools and vendors, data, risk, agents and approvals, access, incidents, transparency. Same order, same precedence.
4. **Never edit a copy.** A file whose first line is `Copy. Edit in <source repo>.` is changed in that repo, then synced.
5. If a task would break a principle, say so before doing it, and offer to record a deviation in the organization's principles file.

No `governance/` folder: continue, and mention once that the repo has no policy yet (Idun sets it up).

Do not print the files.

---

## Step: resume (timestamp)

Used when the agent is started with a resume command: `/saga visita-kommunikation 2026-09-27_13-22 product brief en karriar tack`.
First the repo, then the start time of the session that wrote the handover, then a short summary of what the handover is about. The repo and the summary may be left out. The file is found by the timestamp; the summary is there so the user knows what the command is for.

1. **Right repo?** Compare the repo name with the current repo folder.
   - Same, or no repo given: continue.
   - Different: look for it under the dev root (`C:/dev/*/<repo>` or `~/dev/*/<repo>`). Found: tell the user in one line to start the session there, and stop. Agent sessions should run in the repo they work in. Not found: say the repo is not cloned on this machine and stop.
2. Find the file `<timestamp>-*.md` in `sessions/*/<agent_id>/` at the repo root or in a project folder (`projects/*/sessions/*/<agent_id>/`, any letter case). If the repo's `sessions/README.md` says `sessions: private`, look in the user's own sessions folder for this repo instead: the `sessions:` line in `projects/<repo>.md` in the private cabinet (wrap step 1). Filename: `<session-id>-<från>-<sammandrag>.md`, any user folder including `all-users`. Several matches: pick the one whose `<sammandrag>` matches the summary in the command, else prefer the current user's folder, else list them and ask.
3. Read it. Print EXACTLY:

   ── Återupptar <Agent> · <repo> · <timestamp> ─
   Om:     <sammandrag from the filename, with spaces>
   Från:   <från> (<user>)
   Nästa:  <first line or step of ## Nästa>
   ──────────────────────────────────────────────
   Kör? (j)

4. On confirmation: set `status: tagen` and `tagen_av: <session-id>` in the file, commit, and start on `## Nästa` immediately. No intro, no recap.
5. No match: say so in one line and continue with the normal activation.

---

## Step: handovers

Read the latest handover to this agent: `sessions/<user>/<agent_id>/` (newest file by name), at the repo root and in project folders (`projects/*/sessions/`). If the repo's `sessions/README.md` says `sessions: private`, read from the user's own sessions folder for this repo instead (see resume, step 2).
Also check `sessions/all-users/<agent_id>/` for files with `status: öppen` (handovers to anyone running this agent).
IF an open handover exists: show it (summary from the filename, Nästa and projects) and propose taking it.
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
