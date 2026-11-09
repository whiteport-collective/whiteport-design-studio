# Data

What data passes through {Org}'s AI tools, how sensitive it is, where it may live, and when a deeper assessment is needed.

Status: default (WDS)
Level: default
Tailor in dialog: step 5 (records of processing, DPIA), step 6 (classification, shared and private)

Part of the [framework](framework.md). Keeps principles P1, P2 and P3. Owner: the privacy contact.

## Records of processing

GDPR Art. 30(1). One row per processing activity that involves personal data, AI tools included. The register is kept in writing, may be electronic, and is shown to the supervisory authority on request (Art. 30(3)–(4)). The Art. 30(5) exemption for smaller organizations does not apply when processing is not occasional, and daily work with AI tools rarely is. WDS default: keep the register whatever the size.

| Activity | Purpose | Data subjects | Personal data | Legal basis (Art. 6; Art. 9 for special categories) | Recipients and processors | Transfer outside EU/EEA and safeguard | Erasure time limit | Security measures | Owner (role) | DPIA |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

The controller's name and contact details, and the data protection officer's if one is designated, are in the [framework](framework.md#accountability).

## Classification

Every piece of information has one tier. When in doubt, use the higher one.

| Tier | What it is | Examples | Controls | Into AI tools |
|---|---|---|---|---|
| **Public** | Meant for publication | Published pages, marketing copy, public reports | None | Any approved tool |
| **Internal** | Operational, not personal | Project notes, plans, code, design files | Access limited to the team | Approved tools on {Org}'s accounts |
| **Confidential** | Personal data, or sensitive business data | Contact details, client material, contracts, figures, recordings | Access logged, need-to-know, encrypted at rest and in transit | Tools approved for confidential data, with a DPA and no training. Minimize first: remove or pseudonymize what the task does not need. |
| **Restricted** | Special categories (GDPR Art. 9), criminal data (Art. 10), credentials, data whose loss would cause serious harm | Health data, ID numbers, passwords, keys | Encrypted, strictly need-to-know, named people only | None, unless the approver has approved the tool and the use, and a DPIA is done where required. Credentials: never. |

## Shared and private

Two cabinets, each with its own kind of content (principle P2).

The **repo** belongs to {Org}. It holds everything about the work, written freely: decisions, figures, clients, code, strategy, what is left and what comes next, and how the team works together and with its agents. Everything in it can be read by the team, by partners and, in time, by the client, so it is professional and shows people in a fair light. It stays when a person leaves.

The **private cabinet** belongs to one person and lives outside every repo {Org} owns: how the person likes to work, what they learned, how a session went for them, what they delivered, and personal matters. It follows the person.

| What | Where |
|---|---|
| Decisions, figures, client material, code, strategy, plans | Repo |
| What is left and what comes next, so that anyone can continue | Repo: the handover |
| How the team works together, and with agents, in this repo: roles, agreements, conventions | Repo: `users/<user>/` |
| How the person likes agents to work with them, everywhere: tone, pace, format, what annoys them | Private: `soul.md` |
| What the person learned, and how it went for them | Private: the personal part of the handover |
| What the person delivered, at the level of a CV ("built the open glass for Visita") | Private: `achievements.md` |
| Recordings: audio, screen video, images | Private: the person's media folder, on their computer or a network drive such as Google Drive. Never in git: too large. |
| The transcript of an official meeting, with everything private removed | Repo: the project's meeting archive |
| The transcript of any other conversation | Private: next to the recording |
| Personal finances, health, family, relationships | Private, with the person's own agent, never in the soul files |

**The private cabinet links to the work and never copies it.** It may name the client, the project and what was delivered. It never holds {Org}'s Internal, Confidential or Restricted information ([classification](#classification)): figures, client material, contracts, strategy, code, or copies of handovers, design logs and documents. A person who loses access to a repo keeps their own story and nothing of {Org}'s. Their links simply stop working.

**The repo never points to the private cabinet.** No links to it and no mention that a personal part exists.

**A handover has two parts with the same session id:** the work part in the repo, complete enough for anyone to continue from it alone, and the personal part in the private cabinet. When in doubt, ask whether someone else needs it to continue. If so, it belongs in the repo.

Never write in someone else's folder.

## Storage audit

Things land in the wrong cabinet. The storage audit finds them and cleans up, with an agent (Idun, `/idun audit storage`), one person at a time.

**When:** monthly (recommended, confirmed in step 14), and always before a person's access to a repo is removed, so that their own story leaves with them and {Org}'s information stays.

**What it checks:**
1. **The repo:** `users/<user>/`, the person's handovers and the design logs. Personal content (personal working style, how it went for them, achievements, personal matters) moves to the private cabinet and is removed from the repo. Personal matters in the git history are an incident ([incidents](incidents.md)).
2. **The private cabinet:** {Org}'s information moves to the repo it belongs to, or is deleted. A copy becomes a link.
3. **The soul files:** personal working style in the repo's `soul.md` moves to the private one; agreements about how the team works, found in the private one, move to the repo.

The agent proposes each move and the person approves, because the private cabinet is theirs. The result goes in the handover: what moved, from where to where, and any incident.

## Never in a repo

- credentials: passwords, keys, tokens, recovery codes (S2)
- Restricted data of any kind
- personal data beyond what the work needs (names and roles of the people involved are usually fine)
- raw exports, recordings and transcripts that contain personal data. They stay in the tool or in a restricted store. The repo holds a summary without personal data.
- other clients' confidential information
- private matters: personal finances, health, family

If something lands in a repo by mistake, it is an incident ([incidents](incidents.md)). Removing it also means removing it from the git history.

## DPIA

A data protection impact assessment is required before processing that is likely to result in a high risk to people's rights and freedoms, in particular when using new technologies (GDPR Art. 35(1)). It is always required for (Art. 35(3)):

- a systematic and extensive evaluation of people based on automated processing, including profiling, that leads to decisions with legal or similarly significant effects
- large-scale processing of special categories (Art. 9) or criminal data (Art. 10)
- systematic monitoring of a publicly accessible area on a large scale

Also check the supervisory authority's published list of processing that needs a DPIA (Art. 35(4)).

WDS triggers to consider a DPIA (recommendations): a new AI tool that receives Confidential personal data; profiling or scoring people; recording or transcribing people at scale; combining data sets about people; an agent with long-term memory of personal data.

The DPIA is kept internally, not filed. If it shows a high residual risk that cannot be mitigated, the supervisory authority must be consulted before processing starts (Art. 36).

## Data quality

Only when {Org} trains, fine-tunes or evaluates models, or builds data sets about people. GDPR Art. 5(1)(d) requires accurate data but sets no percentages. Recommended targets (Kenney 2026, not legal thresholds): completeness ≥95%, accuracy ≥98%, consistency ≥90%, timeliness ≤30 days stale. Document how the data's demographics compare with the people the system is used on, and look for proxy variables for protected characteristics.
