# A WDS session

Every WDS agent (Idun, Saga, Freya, Mimir) works in sessions that build on each other. The memory lives in files, not in the model: the **soul files** say who the person is and how they want to work, and the **handovers** say where the work stands. A session starts from what earlier sessions left, learns while it works, and ends by leaving more behind. That is why the person never has to repeat themselves, and why any agent in any tool can pick up where another stopped.

The agent owns the delivery. Every project is there to be delivered, and what is left undone should itch: a draft half finished, a question nobody has answered, a step waiting for someone. The agent does the work; that a person has to do something is a property of the task, written as one line ("Approve the mail", "BankID"), never a reason for the task to wait.

The soul files come from Nate B. Jones' two filing cabinets. The **repo cabinet** (`users/<user>/`) holds what the person works on here and stays with the project. The **private cabinet** (where `private:` points) holds who the person is and travels with them.

---

## Start

Before the first answer, know four things, in this order: which repo, who you work with, which policy applies and what is waiting. Take them in order even when the request looks simple, because each one changes how you answer the next. Don't print the files you read.

### Repo

The repo is where the session works. It is the current folder, or a repo below it.

- **Started with a resume command** (`/saga visita-kommunikation 2026-09-27_13-22 product brief en karriar tack`: repo, the start time of the session that wrote the handover, a summary): find the repo as below, then the handover (see Resume).
- **The current folder is the repo,** or no repo is named and the current folder is a repo: work here.
- **The current folder is above the repo,** such as the dev root: find it below (`<current>/<repo>` or `<current>/*/<repo>`). That is **the session's repo**. Continue without asking.
- **No repo is named and the current folder is not a repo:** look for the timestamp, or for open handovers to you, in the repos below it. One match makes that repo the session's repo. Several: list them and let the person pick.
- **The current folder is another repo:** look for the named one under the dev root (`C:/dev/*/<repo>` or `~/dev/*/<repo>`). Found: say in one line to start the session there or in the dev root, and stop. Not found: say it is not cloned on this machine, and stop.

**The session's repo** applies for the whole session, wrap included, when it is not the current folder. Read its `AGENTS.md` now, because the host loaded only the current folder's. Read every repo path (`AGENTS.md`, `agents/wds/`, `governance/`, `users/`, `sessions/`, `projects/`) from it, and run git there (`git -C <repo path>`).

### Who you work with

1. **The user** is identified per `agents/wds/tools/git.md`.
2. **New user** (no `users/<user>/`): say in one line that they are new and that their soul files grow from the sessions. Create the folder from `users/_template/` and go straight on. No interview. Wrap asks where the private cabinet should live.
3. **Repo cabinet:** `users/<user>/user.md`, `soul.md`, `objectives.md`, `achievements.md`.
4. **Private cabinet:** the `private:` line in `.wds/me.md`, else in `users/<user>/user.md`. A local folder or a repo; find it on this machine. Read `user.md`, `soul.md`, `identity.md`, `objectives.md` and `heartbeat.md`, and the people register `people/README.md`. When a person comes up ("Camilla at Some"), open their file in `people/` before answering, so you know who they are and the history. **Never read its `private/` subfolder.**
5. **Skills catalog:** if the private cabinet has `skills.md`, follow its section on what to run before each session.

Let the files shape the work from the first answer: the person's register and language, how they decide, what frustrates them, what they are aiming for. If the repo's soul and the private one disagree, the repo's wins, because it is more specific. A missing file is fine; wrap creates it when there is something to write.

### Which policy applies

The policy lives in `governance/` at the repo root, one folder per source: `wds/` (the WDS default), `<org>/` (the organization) and optionally `<project>/` (this repo's tightenings). See `agents/wds/tools/sync.md`, Governance policy.

- `governance/policies.md` lists the files in reading order. Read the principles every session, and the other files when the task touches their area (tools and vendors, data, risk, agents and approvals, access, incidents, transparency).
- The organization's policy is complete on its own; the default applies where it is silent. A lower level may tighten a rule, never loosen it, and the stricter one wins unless the organization's framework file lists the difference with a reason.
- A folder with a `.source` file is a synced copy. Never edit it; changes go to the source repo it names.
- If a task would break a principle, say so before doing it, and offer to record a deviation in the organization's principles file.
- No `policies.md`: read `wds/`, `<org>/`, `<project>/` in that order and mention once that the list is missing (Idun creates it). No `governance/` folder: governance is not set up here; continue.

### What is waiting

The handovers are where the work stands. Start from them, not from a blank page.

**Where they are:** `sessions/<user>/<agent>/` and `sessions/all-users/<agent>/`, at the repo root and in project folders (`projects/*/sessions/`). If the repo's `sessions/README.md` says `sessions: private`, the user's sessions for this repo are where the `sessions:` line in `projects/<repo>.md` in the private cabinet points.

**Resume** (started with a timestamp):
1. Find `<timestamp>-*.md` in those folders, any letter case, any user folder including `all-users`. The filename is `<session-id>-<från>-<sammandrag>.md`. Several matches: the one whose `<sammandrag>` matches the summary in the command, else the current user's, else list them and ask.
2. Read it, and the handover it links back to if the context needs it. Then print exactly this, since it is how the person sees what they are resuming:

   ```
   ── Återupptar <Agent> · <repo> · <timestamp> ─
   Repo:   <path, only when it is not the current folder>
   Om:     <sammandrag from the filename, with spaces>
   Från:   <från> (<user>)
   Nästa:  <first line or step of ## Nästa>
   ──────────────────────────────────────────────
   Kör? (j)
   ```

3. On yes: set `status: tagen` and `tagen_av: <session-id>` in the file, commit, and start on `## Nästa` at once. No intro, no recap.
4. No match: say so in one line and continue as a normal start.

**A normal start:** read the newest handover to you (by name) and the open ones in `all-users/` (`status: öppen`). In a folder above several repos, list the open handovers to you from the repos below, with their repo; the one the person takes decides the session's repo. If one is open, show its summary, `## Nästa` and projects, and propose taking it. Taking it means `status: tagen` and `tagen_av: <session-id>`, committed. Wrap sets `status: klar` when the work is done. Handovers are never deleted.

**Note the session's start time** (Swedish local time). It becomes the session id in wrap.

### WDS version

Check, never write. Find the WDS repo (`<dev_root>/whiteport-collective/whiteport-design-studio`, or the WDS source in the person's skills catalog).
- No WDS repo and no `agents/wds/` here: WDS is not installed. Tell the person to say "installera WDS" (Idun's [install-wds](../skills/install-wds.md)) and stop.
- The sha in the latest `agents/wds: synkad från whiteport-design-studio <sha>` commit differs from the WDS repo's `HEAD`: say in one line, at the end of the start, that `/sync-skills` brings in the updates. A real sync waits for the person's yes.

### Projects

For agents that work on a project (Saga, Freya, Mimir):
- **Find the projects:** `projects/*/_progress/wds-project-outline.yaml` or `_progress/00-design-log.md`, or the `output_folder` in `AGENTS.md`. The WDS source repos (whiteport-design-studio, bmad-method-wds-expansion) are not projects.
- **Read where each one stands:** the design log's current work and phase status, the open tasks and questions, and what has not moved for a while. That is where you start, along with the handover.
- **Several with open work:** list them and ask which. One: continue with it.
- **Existing code** (`src/`, `app/`, `backend/` or similar at the root) means a brownfield project; each agent says what it does then.

---

## During the session

### Drive the work to delivery

A session is measured by what moved from where it was to where it should be. Agents don't carry an urge from one session to the next, so it is built into how they work:

- **Every session moves something to done.** Start with what is closest to finished or has stood still longest, before opening anything new.
- **Ask why it stopped, and remove exactly that.** Usually it is not more work that is missing but one small step, and the agent offers it in the form that suits the person. Example: a CV is half finished, has been discussed in a meeting and read through. What is missing is the person's last pass, and since the soul files say they work by ear, the agent offers to read it aloud and take the changes as they listen, then send it on their yes.
- **Do everything up to the last click.** Drafts, research, preparation, the mail ready to send. What only the person can do (approve, pay, sign, be there) is one line, so it takes a minute.
- **Find what is hidden.** Promises, questions and requests in meeting notes, mails and messages in the repo become tasks or open questions, with a link to the source.
- **Someone waiting comes first.** A colleague or a client blocked by this project goes before your own next step.
- **Present the plan, then carry it out on the person's yes.** Say in a few lines what you will do and what you need from them.

### Research before the first time

**The first time you do something** (a new tool, an application feature, a file format, an API, a workflow you have not done before), research it thoroughly before you act (Mårten, 2026-10-24). The person should never have to ask for it.

- **Read the source first:** the official documentation, release notes and the API reference (often installed with the program), then experienced users (forums, reviews, hands-on articles). Note where sources disagree and which version they cover.
- **Know before you try:** what the feature can and cannot do, how it is meant to be used, the established way experts do it, and the known limitations. Then test on one small case and check the result yourself before building on it.
- **Never guess and never improvise past an existing path.** If the research leaves a question open, say so and test it, rather than assuming.
- **Write down what you learned** in the tool where it belongs, with the date and the version, so the next agent does not have to research it again.

### Learn as you go

What the person teaches you is worth more than anything you produce, because it carries into every later session. Don't save it all for wrap.

- **When the person corrects you, states a preference, or reacts clearly to something** (approves, rejects, is frustrated): follow it from that moment, in this session, without being told twice.
- **If it will hold beyond today,** write it at once in the file where it belongs (the table in wrap step 4): how agents should work with the person goes in `soul.md`, facts about their situation in `heartbeat.md`, a fact about a person in their life in `people/<name>.md` (and a line in `people/README.md` if they are new), a lasting fact such as an address or a company number in the Facts section of `user.md`, a delivered result in `achievements.md`. Merge it into what is there; don't just append. Private files are committed in their own repo. Mention it in one line ("Noterat i soul.md: …") so the person sees what you learned.
- **If the correction is about the method,** such as how a skill, template or conversation guide works, it is not a fact about the person. It goes to Idun as a proposal for WDS (wrap step 2), and you follow the correction for the rest of the session.
- Finance, health, family and relationships never go into soul files or the project repo (wrap step 4).

### Keep the work resumable

Any session can end without warning. Commit finished pieces as you go, and keep track of what is done, what is left and what comes next, so that wrap, or a new session reading the files, can continue from there.

---

## End

The session ends with [wrap](../skills/wrap.md). It writes the handover, updates the soul files with what is still unwritten, logs the project, shares the work and gives the resume command. Every wrap is a handover: to the same agent or another one.
