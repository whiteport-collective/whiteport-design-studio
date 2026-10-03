# Soul Elicitation

An optional head start for a person's soul files. By default WDS needs no interview: every wrap compares the session with the soul files and updates them from what actually happened. The interview is for people who want their agents calibrated from day one, or whose files have drifted.

Based on Nate B. Jones' interview approach (see `docs/models/soul-files-portable-context.md`): the more senior the person, the less visible their own operating system is to them, so good questions beat a blank page.

## Where the results go

| What | File | Cabinet |
|---|---|---|
| How agents should work with the person everywhere | `soul.md` | private |
| Who the person is: values, drivers, ways of thinking | `identity.md` | private |
| Current state: workplace, role, manager, colleagues, key dependencies | `heartbeat.md` | private |
| Professional profile | `user.md` | private |
| How agents should work with the person in this repo only | `soul.md` | repo (`users/<user>/`) |

Never: finances, health, family or relationships. Never the `private/` subfolder. An agent's own method never goes into a soul file.

---

## Mode: create (interview, about 20 minutes)

Check first: if the person already has soul files, switch to **review**. Never overwrite without confirmation.

Frame it:

> This takes about 20 minutes. Five layers of questions about how you actually work, not the official version. After each layer you confirm what I captured before we move on. Nothing is saved until you approve all five.

One question per message. After each layer: summarize in your own words and ask, "Does that match how it actually works? Anything to correct?" Take notes in the conversation; write nothing until the end.

### Layer 1 — Operating rhythm

How do your days and weeks actually run?
- What does a typical morning look like before anything goes wrong?
- When are you best at hard thinking? At communication?
- Are there days that always go a certain way?
- When does energy drop, and what do you do about it?
- What's the practical difference between a good week and a bad one?

→ private `soul.md` (when and how to bring things), `heartbeat.md` (current rhythm)

### Layer 2 — Decision patterns

What recurring decisions do you make, and what do you need to make them well?
- Which decisions do you make most often?
- Which are easy and automatic? Which drain you?
- What do you need to know before deciding, and what happens when you don't have it?
- What would need to be true for you to delegate a decision?

→ private `soul.md` (when to ask and when to act, how much to propose unasked), `identity.md` (how they decide)

### Layer 3 — Dependencies and trust

Who and what do you depend on, and when does that become a problem?
- Who do you regularly need things from?
- Is there one person or system that, if it breaks, breaks your day?
- Which external triggers reliably affect your work (emails, reports, meetings, people)?
- What is your rule for credentials and secrets?

→ `heartbeat.md` (people and systems), private `soul.md` (security rules)

### Layer 4 — Domain standards

What do you know that others around you don't?
- What could you explain to a smart new colleague that isn't in any document?
- Which mistakes do others make that you never would, and why?
- Which standards do you hold that you've never written down?
- What context do agents or colleagues constantly lack?

→ private `soul.md` (standards to follow), `identity.md` (expertise), repo `soul.md` for standards specific to this project

### Layer 5 — Communication friction

What in how agents communicate with you costs time or energy it shouldn't?
- What do you explain over and over?
- What length and shape do you actually want? Terse or detailed, bullets or prose, what to skip?
- Forbidden patterns: words, symbols, tone?
- What does a good end-of-session message look like? A bad one?
- Where would an agent save you the most time?

→ private `soul.md` (communication)

### Output

Draft every file change and show it in the chat, file by file and cabinet by cabinet. Write after a yes. A private repo cabinet is committed and pushed; a local folder is just saved. The repo cabinet is committed with the git tool.

---

## Mode: synthesize (draft from history, then validate)

For a person with substantial history: many handovers, corrections and wraps.

1. **Gather evidence** from the files: handovers the person ran (`sessions/<user>/*/`), the "Corrections" sections of their repo `soul.md` files across repos, their private `log.md`, and their objectives.
2. **Cluster** into the five layers. Look for direct corrections ("don't do X"), repeated approvals ("yes, exactly"), and implicit norms (every commit or wrap has the same shape).
3. **Cite.** Every proposed line names at least one source (file and date) so the person can check it.
4. **Validate.** Show the draft and ask: anything wrong, anything missing, anything over-fitted (a one-time correction that became a rule)? Iterate, then write as in create mode.

The validation pass replaces most of the interview; ask only about layers the history doesn't cover.

---

## Mode: review (drift check)

When the soul files are older than about a month, or recent sessions clearly contradict them:

1. Read the current soul files (both cabinets).
2. Read the last 30–60 days of handovers and corrections.
3. List each line the evidence contradicts, and each recurring pattern that isn't captured.
4. For each: quote the evidence, propose the change, ask for confirmation.
5. Apply confirmed changes. Update and prune; don't just append. Date the change.
