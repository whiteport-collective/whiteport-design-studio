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

Two cabinets. The **repo** is shared: everything in it can be read by the team, by partners and, in time, by the client. It is professional and shows people in a fair light. The **private cabinet** belongs to one person and lives outside every shared repo: personal notes, feedback, opinions about people, clients and vendors, commercial reasoning and anything unprofessional or controversial.

Handovers between sessions and agents contain only what everyone on the project may read. Private context goes in the private cabinet.

Never write in someone else's folder.

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
