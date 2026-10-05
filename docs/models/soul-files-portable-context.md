# Soul Files: Portable AI Context

**By:** Nate B. Jones (2026)
**Source:** Nate's Newsletter and the AI News & Strategy Daily channel, where he calls it "Bring Your Own Context"

---

## Core Concept

Your AI context is professional capital, as real as your skills, network, credentials and track record. Unlike the others, it lives on servers you don't control and disappears when you cross a platform boundary.

> "Memory replaced the model as the moat of 2026."

The fix is to own your context as plain files that any agent can read: **USER.md**, **SOUL.md** and **HEARTBEAT.md**. You keep them in your own filing cabinet, separate from your employer's.

---

## The Four Layers of AI Working Intelligence

What an AI learns about you over hundreds of conversations:

| Layer | What it is |
|---|---|
| **Domain encoding** | Industry vocabulary, products, market context, acronyms. Built in tiny pieces, and you can't list it all. |
| **Workflow calibration** | How you want research structured, code reviewed, memos formatted. |
| **Behavioral relationship** | The unstated preferences: when to challenge and when to execute, how technical to go, how much preamble you tolerate. Built through hundreds of micro-corrections. |
| **Demonstrated capability** | What you have actually built. Today it is largely invisible. |

**The honing effect:** "The worse a new AI feels when you start, the better job you've done encoding into the old one. The friction is the receipt."

---

## The Four Boundaries Where Context Is Lost

1. **Platform switch.** You face a blank screen, and import tools move only fragments.
2. **Enterprise wall.** A managed company account can't merge with your personal context.
3. **Job change.** There is no way to separate what is yours from what is theirs.
4. **Hiring market.** Demonstrated AI capability can't be seen.

---

## Two Filing Cabinets

| Cabinet | Holds | Owned by | When you leave |
|---|---|---|---|
| **Yours** | How you work: communication style, expertise, working patterns | You | Travels with you |
| **Theirs** | What you worked on: strategy, client data, project knowledge | The organization | Stays |

---

## The Expertise Trap, and Nate's Answer

Nate argues that you can't write your SOUL.md from scratch: "The more senior you are, the less visible your own operating system becomes to you."

His answer is an **interview**. A 45-minute prompt turns the AI into an interviewer instead of an assistant. It asks the questions, draws out how you work, and writes the files.

In a related piece he suggests capturing every time you *reject* AI output as a reusable constraint. A rejection shows a standard you hold but never wrote down.

---

## How WDS Differs: Every Session Is a Source

Nate asks questions once. **WDS learns from every session.**

| | Nate: the interview | WDS: the session |
|---|---|---|
| **When** | Once, in 45 minutes | Continuously, at every wrap |
| **Source** | What you can put into words when asked | What actually happens when you work |
| **Expertise trap** | Reduced by good questions | Avoided: the operating system shows in your corrections, even when you can't describe it |
| **Freshness** | A snapshot that ages | Updated, merged and pruned every session |
| **Effort** | A dedicated session | None. It is part of the wrap |

A correction ("don't do X, do Y"), a rejected proposal, a fact mentioned in passing ("my new manager is…"), a goal that shifts: each one is a data point the interview would never catch. The wrap collects them, and the next session starts from a sharper baseline.

---

## Applied in WDS

### The two cabinets in WDS

| Cabinet | Where | Files |
|---|---|---|
| **Repo:** what you work on here | `users/<user>/` in the project repo, shared with the team | `user.md` (role in the project), `soul.md` (how agents work with you *in this repo*), `objectives.md`, `achievements.md` |
| **Private:** who you are | a local folder or a repo you own, pointed to by `private:` in `users/<user>/user.md`, with a copy in `.wds/me.md` | `user.md` (professional profile), `soul.md` (how agents work with you *everywhere*), `identity.md` (values, drivers, ways of thinking), `objectives.md`, `heartbeat.md` (current state: workplace, role, manager, colleagues, what has happened), `log.md` (one line per session), `skills.md` + `skills.json` (the skills catalog: every source repo, and the sync to run before each session). Private handovers go in `sessions/` in the same repo |

`<user>` is the GitHub username in lowercase. `.wds/me.md` is local to each machine and never committed. The location of the private cabinet can be stored openly in the repo's `user.md`, because a path reveals nothing. The contents stay private.

The private folder may contain a `private/` subfolder for finances, health, family and relationships. **Work agents never read or write it.**

### At session start

Every WDS agent (Saga, Freya, Mimir) runs **Step: soul** in `agents/wds/data/shared-activation.md`:

1. Identify the user from `.wds/me.md`, or through the git tool.
2. Read the repo cabinet and the private cabinet, but never `private/`.
3. Follow both soul files. If they conflict, the repo's soul wins because it is more specific.
4. Keep what was read as **the baseline** for the session.
5. If the private cabinet has a skills catalog, run its sync so the latest skills are installed locally.

### At wrap: the soul review

Wrap step 4 compares the whole session with the baseline and sorts every new item into the right file:

| New information | File | Cabinet |
|---|---|---|
| Current state: workplace, role, manager, colleagues, clients, what has happened | `heartbeat.md` | private |
| How agents should work with the person everywhere | `soul.md` | private |
| How agents should work with the person in this repo | `soul.md` | repo |
| Who the person is: values, drivers, ways of thinking | `identity.md` | private |
| Professional profile: skills, experience, working style | `user.md` | private |
| Role in this project | `user.md` | repo |
| Goals | `objectives.md` | private or repo |
| Delivered in the project | `achievements.md` | repo |
| Finances, health, family, relationships | a handover to the person's private agent in `sessions/` | private, never in the soul files or the project repo |

**Rules:**
- **Update and optimize, don't just append.** Merge duplicates, replace what no longer holds, prune what is outdated, and keep each file short. Date corrections and events.
- **The agent's method never goes into a soul file.** If the person corrects how an agent follows its own method (a conversation guide, a template), the agent instructions have a gap. That is fixed upstream, not in someone's soul.
- **Repo files are shared.** Nothing private goes there, and no one edits another person's folder.
- **Private files are written directly.** A repo is committed and pushed, and a local folder is just saved. The wrap receipt shows exactly what changed, file by file and cabinet by cabinet.

### A new user

WDS notices a new user and builds the cabinets from the first session on:

1. **At start:** the agent can't find the user in `.wds/me.md` or `users/`. It says the person is new, identifies them through the git tool, and creates `users/<user>/` from `users/_template/`. The work begins right away. No interview is needed.
2. **At wrap:** if `private:` is empty or points to a folder that doesn't exist on this machine, the agent **asks where the private soul files should be stored**. The answer can be a local folder or a repo the person owns, never the project repo.
   - The person gives a location: the agent writes it to `private:` in `users/<user>/user.md` and in `.wds/me.md`, creates the files and writes the private items from the session. A repo is committed and pushed. A local folder is just saved.
   - The person declines: the agent writes only the repo cabinet and lists in the receipt what it would have saved privately. The question comes back at the next wrap.

---

## In Daily Work

**Morning.** You start an agent. It already knows your role, your manager's name, what you are working towards, and that you want answers first and preamble never. You don't brief it.

**During the session.** You work as usual. When you correct the agent, reject a proposal or mention something new ("we signed the contract", "I'm moving to Gothenburg"), nothing extra is needed. It is all in the conversation.

**Wrap.** The agent writes the handover, runs the soul review and shows you the receipt:

> *soul.md (private): merged two rules on brevity into one. heartbeat.md (private): new client added, old manager removed. achievements.md (repo): product brief delivered.*

**Next session.** It starts from the improved baseline. Over weeks, the files become a more accurate picture than any interview could give, and they stay yours when you change tools, employers or machines.

---

## Source Materials

### Articles and videos by Nate B. Jones
- **"Your agent needs a SOUL.md you can't write from scratch. I built a 45-minute prompt that writes it for you."** Nate's Newsletter, 15 April 2026. [natesnewsletter.substack.com](https://natesnewsletter.substack.com/p/your-agent-needs-a-soulmd-you-cant)
- **Bring Your Own Context**: portable AI working intelligence, the four layers, the four boundaries and the two filing cabinets. [YouTube](https://www.youtube.com/watch?v=4KAF72BTyCE)
- **"The most expensive AI mistake isn't …"**: capturing rejections of AI output as reusable constraints. [natesnewsletter.substack.com](https://natesnewsletter.substack.com/p/the-most-expensive-ai-mistake-isnt)

### Website
- [natebjones.com](https://www.natebjones.com/)

---

## WDS Integration Points

| WDS context | Soul files application |
|---|---|
| **Agent activation** | Step: soul reads both cabinets before any work |
| **Wrap** | Soul review: compare, route, update, optimize |
| **Handovers** (`sessions/`) | The raw record of each session, where the soul review gets its material |
| **New user** | Detected at start. Asked at wrap where the private cabinet should live |
| **Team repos** | Repo cabinet shared, private cabinet never copied in |
| **Agent instructions** | Method corrections go upstream, never into a soul |
| **Skills catalog** | Synced before every session. Wrap moves skill changes to their source repo and updates the catalog |

---

## Quick Reference

### The core idea
> Own your AI context as files, in your own cabinet.

### The WDS twist
> Don't interview once. Learn from every session.

### The wrap rule
> Compare, route, optimize. Never just append.

---

*Soul Files: your context is yours, and every session makes it sharper.*
