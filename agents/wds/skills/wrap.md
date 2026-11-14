---
name: wrap
source: wds
description: End a session. Turns the session file into the handover, in two parts (the project part in the repo, the personal part in the private cabinet), to the same or another agent; compares the session with every soul file and updates them in the repo and privately; moves skill changes to their source repo and the catalog; reports incidents and proposes G&C points; updates the project log and shares the work.
used_by: [idun, saga, freya, mimir]
tools: [wds/git]
---

# Wrap: end the session

Agent-independent. The skill says *what* to do. How git is used is in the [git tool](../tools/git.md). The words written into files (statuses, fields, headings) are the English ones in [i18n.yaml](../data/i18n.yaml); the text written for the person follows their language.

**Wrap does not ask what happened.** The agent was in the conversation and takes what was done, what is left and the next step from the conversation, the session file and git. The only questions are where the sessions and the private cabinet should live, and only when the answer is missing (steps 1 and 4).

**The work stays with the work, the person stays with the person** (principle P2 in `governance/wds/principles.md`, Mårten 2026-11-01). Everything about the work is written freely in the repo: decisions, figures, clients, code, what is left and how the team works together. Everything about the person is written freely in the private cabinet: how they like to work, what they learned, how it went and what they delivered. Neither part needs censoring, and neither copies from the other. The private part links to the work, so nothing of the organisation's follows a person who is removed from a repo.

## 1. Who, which session, to whom

- **User:** identify per the git tool. That gives `<user>`, the GitHub username in lowercase.
- **Session id:** `YYYY-MM-DD_HH-MM-<user>`, in Swedish local time at the **start of the session**. The agent noted the time at start ([session.md](../data/session.md)). If it did not: the time of the session's first commit, else the time now.
- **From:** the agent that was active (saga, freya, mimir, ivonne …), whatever the model. Without an agent: the model name in lowercase with hyphens, for example `claude-opus-5-5`.
- **To:** who takes the next step. Usually the same agent, and then the wrap is a handover to itself. When the next step belongs to another agent, it is that agent.
- **What:** find what changed per the git tool. With that, the session file and the conversation: which projects were touched, what got done and what is left?
- **Project root:** the folder where the project lives. The repo root, except when the repo has several projects. Then it is the project's own folder, for example `projects/<project>/`, and the repo's `AGENTS.md` says which. A session that touched no single project: the repo root.
- **Sessions folder:** where the handovers are kept. Normally `<project root>/sessions/`. The repo can decide otherwise in `<project root>/sessions/README.md`:
  - `sessions: private` means nobody keeps sessions in the repo, which suits a public repo many work in. Each person picks a place in their private cabinet. The place is in the cabinet's `projects/<repo>.md` on the line `sessions:`, as a link relative to that file. It applies only to repos whose content is already public; a repo with an organisation's internal material keeps the project part in the repo.
  - The line is missing: ask the person once where the sessions for this repo should live, and write the answer there. No cabinet, or the person declines: the handover is shown in the chat only and not saved.
- **Private sessions folder:** where the personal part is kept, `sessions/` at the root of the repo or local folder where the private cabinet (`private:`) lives.

## 2. The handover, in two parts

Every wrap is a handover in two parts with the same session id:

- **The project part** in the repo: everything about the work, complete enough for anyone to continue from it alone. It never mentions that a personal part exists and never links to it.
- **The personal part** in the private sessions folder (step 1): what concerns only the person, and a link to each project part. It copies nothing from the project part.

The test for each line: does someone else need this to continue? Then it belongs in the project part. Without a private cabinet only the project part is written.

### From the session file

The session file (`<session-id>-<agent>-active.md`, [session.md](../data/session.md), Keep the work resumable) becomes the project part. No session file: write the project part from scratch in the format below.

Go through `## In progress` and decide what follows along:
- **Finished** (a checklist all ticked, a tour walked through): one line under `## Done`.
- **To continue** (an unfinished checklist, an open tour, a value the next session needs): under `## Left` or `## Next`, the checklist itself when the next session works from it.
- **Working notes** that served only this session: struck. Git keeps them.

Then remove `## In progress`, set `status: open`, and rename the file (`git mv`) to the name below. When the next step belongs to another agent, it moves to that agent's folder.

### The project part

The folder is the **recipient's**. The filename is `<session-id>-<from>-<summary>.md`:

- `<session-id>` = `YYYY-MM-DD_HH-MM-<user>`: the timestamp and who ran it.
- `<from>` = the agent that wrote it.
- `<summary>` = what the session did, 3 to 6 words, lowercase, hyphens, å/ä → a and ö → o. Example: `2026-09-27_13-22-martenangner-ivonne-product-brief-career-track.md`.

The filename starts with the timestamp and ends with the summary. The resume command (step 9) finds the file by its timestamp and shows the summary, so the person sees what the handover is about before running it.

| Recipient | Path |
|---|---|
| Same person, same agent (a usual wrap) | `<sessions folder>/<user>/<from>/<session-id>-<from>-<summary>.md` |
| Same person, another agent | `<sessions folder>/<user>/<to>/<session-id>-<from>-<summary>.md` |
| Another known person | `<sessions folder>/<person>/<to>/<session-id>-<from>-<summary>.md` |
| We don't know who runs it | `<sessions folder>/all-users/<to>/<session-id>-<from>-<summary>.md` |
| A proposal for the WDS method (steps 4 and 6) | Idun at whoever maintains WDS, see below |

**Proposals for the WDS method** concern the agents, their skills and tools, and the WDS default policy. They change only in the WDS source repo, whiteport-design-studio, and Mårten Angner approves. The proposal becomes its own handover to Idun, who gathers the proposals from every client's wraps and takes them to the source repo:
- **Whoever maintains WDS runs the wrap:** in their own sessions folder for the WDS source repo, `<sessions folder>/<user>/idun/`. The source repo's `sessions/README.md` decides where it is; if it says `sessions: private`, it is the person's private sessions folder for whiteport-design-studio.
- **Someone else runs the wrap:** in the WDS source repo's `sessions/all-users/idun/` if the repo keeps sessions and the agent may write there. Otherwise in this repo's `<sessions folder>/all-users/idun/`, where Idun picks it up when she goes through the client's repos.
- Write only what everyone in the project can read: the gap, what happened and the proposal, with a link to the incident if there is one.

```markdown
---
session: YYYY-MM-DD_HH-MM-<user>
start: YYYY-MM-DDTHH:MM+01:00
end: YYYY-MM-DDTHH:MM+01:00
user: <user>
from: <agent or model>
to: <agent or model>
model: <model id>
tool: <claude|copilot|codex|...>
projects: [<project>, ...]
repos: [<repo>, ...]
status: open
taken_by:
---

## Done
- ...

## Left
- ...

## Next
Concrete steps in order for the recipient.

## Files
- [relative/path](../../../relative/path)
```

- Keep it short. It should read in a minute. `projects: []` when the session touched no specific project.
- **Done means delivered.** Under `## Done` goes only what the recipient actually has: published live and checked in the browser, sent or approved. What exists only locally, in a draft or in a database nobody sees, goes under `## Left`, marked with `label.only_local` and what stops it. An assignment with such things left never gets `status: done`.
- **To another agent:** also write a short wrap to yourself if you have threads of your own left, and link the handover from there.
- **Status:** the recipient sets `status: taken` and `taken_by: <session-id>` when they start ([session.md](../data/session.md), What is waiting). If this session took a handover: set `status: done` in that file when the assignment is done.
- **Handovers are never deleted.** `sessions/all-users/` is neutral and has no user id. Who ran it shows from the session that takes it (`taken_by: <session-id>`).
- **Writing in someone else's folder:** the only thing allowed is adding a *new* file in their `sessions/<person>/<agent>/`.

### The personal part

In `<private sessions folder>/<user>/<to>/`, with the same filename as the project part. When the session touched several repos it gets one summary for the whole session. One personal part per session, however many repos it touched.

```markdown
---
session: YYYY-MM-DD_HH-MM-<user>
user: <user>
from: <agent or model>
to: <agent or model>
part: personal
repos: [<repo>, ...]
status: open
taken_by:
---

## Project parts
- <repo>: `sessions/<user>/<to>/<filename>.md`

## For you
How it went, what chafed, what you learned, how you sounded and what gave energy. Free and uncensored, but never the organisation's information.

## Next
Only what is yours, beyond the project parts' Next: threads in other repos, things you want to do yourself.
```

- **What may be written:** the client's and project's name, what was delivered, how it felt and what you learned. **Not:** figures, client data, strategy, code, decisions or copies from the project part (`governance/wds/data.md`, Shared and private).
- **Finance, health and family** still go to the person's own agent (step 4), not here.
- Nothing new for the person: still write the part with the links, so the session is in the person's history.

## 3. The project log: the team's shared timeline

For each project touched: add an entry to the project's design log. It is in the project root, or in the folder above the sessions folder when sessions are kept privately. Take whichever exists of `_progress/00-design-log.md`, `design-process/_progress/00-design-log.md`, `00-design-log.md` and `design-log.md`. If the log has a `## Log` heading the entry goes at the top under it, else at the top of the file, at the same heading level as the entries already there. No log: skip the step.

```markdown
### YYYY-MM-DD_HH-MM-<user> (<from> → <to>)
- One to three points on what happened in the project. [Handover](<relative path to the handover>)
```

**The folder presentations.** For each WDS folder in the project the session changed (`A-Product-Brief/` to `E-Development/`): update the folder's `presentation.md` so it shows the folder as it stands after the session, render it and include it in the commit. How and what: [folder-presentation](folder-presentation/SKILL.md). A folder without a presentation that got its first real content: create it.

## 4. Soul review: compare and update

**Where is the private cabinet?** In `private:` in `users/<user>/user.md`, with a copy in `.wds/me.md`. It can be a local folder or a repo.
- **`private:` is missing, or the folder is not on this computer:** ask the person where the private soul files should be kept. Suggest a folder in a repo the person owns, or a local folder, never the project repo. Write the answer in `private:` in `user.md` and in `.wds/me.md`, and create the folder and the files needed.
- **The person declines:** write only in the repo's cabinet. Show in the receipt what would have been saved privately, and ask again at the next wrap.

The agent read the soul files at start and wrote in what should last already during the session ([session.md](../data/session.md), Start and During the session). Wrap is the safety net: go through the whole conversation, compare it with what the files say now and write in what is not there yet. Look for everything new or changed:

- **Facts about the person:** where they work, role, manager and colleagues, clients, what has happened, addresses, companies
- **People in the person's life:** who someone is, the relationship and what you have done together
- **Corrections** of the agent, and what the person appreciated or rejected
- **Insights** into how the person thinks, decides and what they value
- **Goals** added, changed or reached
- Things **delivered**

Each new thing goes to the right file:

| New | File | Cabinet |
|---|---|---|
| Current situation: workplace, role, manager, colleagues, clients, what has happened | `heartbeat.md` | private |
| The person's own style: how agents should work with them everywhere (tone, pace, format, what irritates), also when learned in this repo | `soul.md` | private |
| How we work together in this repo: roles, agreements, ways of working in the team and with the agents | `soul.md` | repo |
| Who the person is: values, drives, ways of thinking | `identity.md` | private |
| Professional profile: skills, experience, way of working | `user.md` | private |
| Lasting facts: addresses, companies with registration numbers, homes, contact channels | `user.md`, the Facts section | private |
| People: colleagues, clients, partners, family and friends. Who, the relationship, history with dates and sources. Contact details stay in the person's address book (for example Google Contacts) and the file refers there, never a copy | `people/<name>.md`, and a line in `people/README.md` | private |
| Role in this project | `user.md` | repo |
| Personal goals | `objectives.md` | private |
| The project's goals and the person's goals in the project | `objectives.md` | repo |
| Delivered, at CV level: what, for whom and when ("built the open glass for Visita"), never how it was done inside the client | `achievements.md` | private, at the top, with a link to the project part. The project's own timeline is the design log (step 3) |
| Finance, health and sensitive details about relationships (conflicts, private life) | a handover to the person's private agent in `sessions/<user>/<agent>/` in the private cabinet's repo (or local folder) | private, never in the soul files and never in the project repo |

The repo's files are in `users/<user>/`. The private ones are where `private:` points.

**Rules**
- **Update and optimise; don't just add lines.** Write the new where it belongs, merge duplicates, replace what no longer holds and strike what is out of date. Keep each file short and easy to read. Corrections and events get dates.
- **The agent's method does not belong in soul.** When the person corrects how the agent follows its own method, for example the conversation guide or a template, it is a gap in the agent instructions. Propose a change upstream instead of writing in anyone's soul. For the WDS agents the proposal becomes a handover to Idun at whoever maintains WDS (step 2, Proposals for the WDS method).
- **The repo's files are shared with the team.** Never write anything private there, and never change anything in someone else's folder.
- **The private files never hold the organisation's information.** A lesson is written as the person's own ("wants the figure before the reasoning"), not as the client's business ("Visita's budget is …").
- **Private files are written directly.** If the cabinet is a repo, commit and push per the git tool. If it is a local folder, the files are just saved. The receipt shows what changed.
- Touch only the files where something new actually happened. `heartbeat.md` is created the first time there is something to write.

## 5. Skills: the catalog and the source repos

Skills live in the repo of the project, initiative or company they serve. The person's catalog (`skills.md` and `skills.json` in the private cabinet) lists the person's own skills and every repo the person works in.

- **New project:** if this repo is not in the catalog, add it with its path, GitHub address and what it holds. From now on it is synced at every wrap.

The rest applies when the session created, changed, moved or removed a skill, a tool or a script.

- **Nothing that works stays in a temporary folder.** Go through the session's working folder (scratchpad, `%TEMP%`, session folders) and environments outside the repos (for example `~/.venvs`). A script, an install or a setting that worked moves to the source repo of the tool it belongs to, with paths and measurements in the tool's description. The OpenVINO transcription from 2026-10-14 lived only in a temporary folder and was rebuilt nine days later (2026-10-23).
- **The change lives in the source.** Every skill has exactly one source repo. A change made in a local copy, for example `~/.claude/commands`, an adapter folder or a synced `agents/wds/`, moves to the source repo. Commit and push there. External sources are changed upstream.
- **One commit per skill or tool.** Each changed skill or tool gets its own commit with only that file and its scripts, never other work. The message is `skill(<name>): <what changed and why>` or `tool(<name>): …`. Then `git log -- <file>` shows how the skill has developed.
- **The catalog is updated.** If the person has a skills catalog in their private cabinet (`skills.md`, and `skills.json` if it exists), add new skills and sources, and change the line for what was moved or removed. Overwrite nothing. Update the line where the skill stands.
- **Spread the version.** Run the sync per the catalog, so every repo and this computer get the new version.
- **Confirmation:** a sync, a new line in the catalog, and commit and push in the person's own repos are done without asking, and the receipt shows what happened. The person confirms only when the change goes to a public repo, lands in someone else's repo, or removes or moves a skill.
- **Skill and tool are kept apart** per `agents/wds/README.md` (Skills and tools). Check that the skill lists its tools in `tools:` and that each tool lists its skills in `used_by:`. Commands that ended up in a skill move to a tool.

## 6. G&C: incidents and proposals

Governance says *what* applies and why: the principles, the policies and who decides. Compliance is *how* we keep to them: routines, checks, deviations and incidents. Any session can show that the framework lacks something, and wrap is the safety net that catches it.

Go through the session and look for:
- **Incident:** something happened that breaks a principle, or nearly did. Example: a password the project uses is in a public database after a leak.
- **Deviation:** something in the repo or the way of working does not follow a principle right now.
- **Gap:** a case the framework does not cover, so the agent had to improvise.

For each finding:
1. **Urgent first.** If a secret is exposed or damage is ongoing, say so in the session when it is found, not at wrap. The human acts, for example changes the password.
2. **Incident report** in the incident log `governance/policies.md` points to for the right level: the organisation's (`governance/<org>/incidents.md`, or the local name, for example `governance/visita/incidenter.md`) or the project's. If the organisation's folder has a `.source` file it is a copy: write the report in the source repo `.source` names, and if the agent cannot write there the report becomes a handover to the policy's owner. Write the date, what happened, the impact, what was done and who knows. **Never write the secret itself**, only where it was and whether it has been changed.
3. **Proposed new point:** a routine for how we act (compliance), or a new principle when the case shows one is missing (governance). Mark it `proposal`, with a date and a link to the incident.
4. **The mandate:** the agent may report, propose and tighten. It may never itself loosen or remove a principle, or widen what agents may do. That takes the human's explicit yes. The policy's owner approves the proposals. That goes for Idun too.
5. **The WDS default policy** changes in the source, whiteport-design-studio, never in the synced copy `governance/wds/`. The proposal becomes a handover to Idun at whoever maintains WDS (step 2, Proposals for the WDS method).
6. **No `governance/` or incident log** in the repo: write the finding under `## G&C` in the handover.

No finding: skip the step.

## 7. Share

Save and share the project part, the project logs and the repo's user files per the git tool. The personal part and the private files are shared in their own repo. The commit message is `wrap: <session-id> — <one line>`.

## 8. Other repos and the personal log

- **Other repos in the same session:** write a project part with **the same session id** in their `<sessions folder>/<user>/<to>/`, or run their own wrap. Each repo gets only its own part. The personal part links to them all. With the same id, the session can be found in every repo.
- **Private log:** if `private:` points to a folder on this computer, add a line at the top of `log.md` there: `- <session-id> <repo, …> (<from> → <to>): one line · <the personal part's path>`. Create the file if it is missing. If the cabinet is a repo it is shared there.

## 9. Receipt

Show the user:
- the session id, the recipient and the paths to the project part or parts and to the personal part
- both parts in full, so the person sees that the focus is right and that nothing of the organisation's ended up in the personal one
- what changed in the soul files, per file and cabinet (repo or private), or "nothing new"
- the private handover, if anything about finance, health or family came up
- skills that changed: where they live now and that the catalog is updated
- G&C: incidents reported and points proposed, or "nothing new"
- the commit hash and that the push went through

End with the resume command as its own code block, so it copies with one click. `<to>` is the receiving agent, `<repo>` is the repo's folder name, the timestamp is the session's start and `<summary>` is the same words as in the filename, with spaces instead of hyphens:

````
```
/<to> <repo> YYYY-MM-DD_HH-MM <summary>
```
````

Example: `/ivonne martens-documents 2026-09-27_13-22 product brief career track`. Without the summary nobody knows what the command is about when it sits among others.
