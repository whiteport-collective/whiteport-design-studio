# Framework

How {Org} governs its work with AI agents: where the policy lives, what it covers, who is accountable, how it is reviewed and who approves it.

Status: default (WDS)
Level: default
Tailor in dialog: step 0 (set up), step 0.5 (maturity), step 1 (scope), step 2 (accountability), step 14 (review), step 17 (approval)

## Where the policy lives

All policy files are in one flat folder, `governance/`, at the root of every repo {Org} works in. An agent often sees only one repo, so each repo carries the whole policy. Each file name starts with its source:

| Files | Level | Source | Edited where |
|---|---|---|---|
| `wds-*.md` | Default | WDS: `agents/wds/idun/templates/governance/` in whiteport-design-studio | Never in a project repo. Read-only copy, synced. |
| `<org>-*.md` | Organization | {Org}'s source repo for its policy: `{org-source-repo}` | Only in the source repo. Every other {Org} repo gets a read-only copy through sync. |
| `<project>-*.md` | Project | This repo | Here. Only tightens. |

- {Org} has exactly one source repo for its policy. The policy may be localized, file names included (for example `<org>-ramverk.md`). The framework file links the others.
- Every copied file starts with the line `Copy. Edit in <source repo>.` Never edit a copy. Change the source and sync.
- Every policy file states its level on its `Level:` line: default, organization or project.
- In the `wds-*` files, `{Org}` and the other `{…}` placeholders stand for the organization and its own details.

## Precedence

WDS default < organization < project.

- **The organization policy is complete on its own.** People and agents working for {Org} follow the `<org>-*` files. The WDS default applies only where the organization policy is silent.
- **A lower level may tighten a rule, never loosen it.** When two levels say different things, the stricter one wins, unless the difference is recorded below with a reason and approved. A recorded difference never goes below what the law requires.
- A project tightening names the rule it tightens. It cannot loosen anything.

## Differences from the WDS default

Every place where {Org}'s policy differs from the WDS default is listed here. Everything not listed follows the default. Idun keeps this table current with a conflict check whenever the default changes (see Review).

| Area / principle | WDS default | {Org} rule | Why |
|---|---|---|---|
| *None yet* | | | |

## Scope

- **Applies to:** {Org} ({units}), every repo and system where {Org} works with AI, and every person and AI agent working on {Org}'s behalf, contractors included.
- **Out of scope:** {anything explicitly excluded, with the reason}.
- **Regulation it is built on:** GDPR, the EU AI Act (Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744), with NIST AI RMF 1.0 and ISO/IEC 42001:2023 as voluntary benchmarks. Writing this policy does not by itself make {Org} compliant.

## Principles

A principle is like a goal but stays within the constraints. It is never done. It is measured in deviations, not progress, and every deviation gets an action. The principles and the current deviations: [principles]({org}-principles.md).

## Maturity

| | Level | Recorded |
|---|---|---|
| AI adoption today | {Level X: name} | step 0.5 |
| AI adoption target | {Level Y: name}, by {when}, because {driver} | step 0.5 |
| Governance maturity target | Level 3, Managed: processes standardized, applied consistently, metrics tracked | WDS recommendation, not law |

- **Adoption owner:** {role}. **Confirmed by:** {role, date}.
- Level-up plans (what changes, who owns it, which authority is granted) are added here per level in step 0.6.

## Accountability

Roles, not names. One person may hold several roles in a small organization. Every area of this policy has exactly one owner. Names appear only in the approval block. (GDPR Art. 5(2) accountability; ISO/IEC 42001 clause 5.3; NIST AI RMF GOVERN 2.1.)

| Role | Accountable for | Default owner of |
|---|---|---|
| **Approver** | The policy as a whole. Approves it, its changes and every recorded difference from the default. | framework |
| **Policy owner** | Keeps the policy current, runs the reviews, keeps the deviations table. | principles, risk |
| **Privacy contact** (the DPO, if one is designated) | Records of processing, DPIAs, personal data breach assessment. | data, transparency |
| **Agent owner** (one per agent) | What the agent does: its authorization profile, its skills, its overrides. | agents |
| **Access owner** | Accounts, credentials, integrations, kill switch, access reviews. | access, tools |
| **Incident lead** | Runs incidents from report to closure. | incidents |
| **Everyone** | Follows the principles. Reports deviations and incidents at once. | |

The person who delivers work is responsible for it, whether a person, an agent or a contractor produced it.

## AI literacy

EU AI Act Art. 4: providers and deployers "shall take measures to support the development of AI literacy of their staff and other persons dealing with the operation and use of AI systems on their behalf". (ISO/IEC 42001 clauses 7.2 and 7.3; NIST AI RMF GOVERN 2.2.)

Defaults (recommendations):
- **Before first use:** everyone who works with AI for {Org} reads the principles, the tool limits ([tools]({org}-tools.md)), the review gate ([agents]({org}-agents.md)) and how to report an incident.
- **By role:** agent owners and approvers also learn how the agents they own work, where they fail, and what automation bias looks like.
- **Refresh:** yearly, and when a tool or an agent's autonomy changes.
- **Record:** who, what, when, in {Org}'s own people records.

## Documents

| File | Covers | Dialog steps |
|---|---|---|
| [framework]({org}-framework.md) | Where the policy lives, precedence, differences, scope, maturity, accountability, AI literacy, review, approval | 0, 0.5, 0.6, 1, 2, 14, 17 |
| [principles]({org}-principles.md) | The principles and the deviations now | all |
| [tools]({org}-tools.md) | AI tools and vendors: permitted and prohibited uses, due diligence, transfers | 4, 11 |
| [data]({org}-data.md) | Records of processing, classification, what never goes into a repo, DPIA | 5, 6 |
| [risk]({org}-risk.md) | AI Act classification, agentic risk score, risk register | 3, 3.5 |
| [agents]({org}-agents.md) | Authorization levels, review gate, overrides, skill governance, controls | 7, 8, 13, 15, 16 |
| [access]({org}-access.md) | Accounts, least privilege, credentials, integrations, kill switch, access review | 9 |
| [incidents]({org}-incidents.md) | Roles, procedures, the personal data breach clock, logs | 10 |
| [transparency]({org}-transparency.md) | Disclosure to clients and the public, consent, objections | 12 |

## Review

Cadences are recommendations. Who and how often is confirmed in step 14. (NIST AI RMF GOVERN 1.5; ISO/IEC 42001 clauses 9.3 and 10.2.)

| Cadence | Who | What |
|---|---|---|
| Each working day | Agent owners | Pending approvals. Any kill switch or circuit breaker trip. |
| Monthly | Idun, reported to the policy owner | Skill audit, override rate, deviations table, unregistered tools. |
| Quarterly | Policy owner, access owner | Tool and vendor review, access review, risk register, open deviations. |
| Yearly | Approver | Full review of the policy, AI Act re-classification, GDPR safeguards, new version. |

**Review at once when:**
- a new AI tool, vendor, integration or contractor is added
- an agent gets more autonomy, or acts outside its authorization
- a personal data breach or a near miss happens
- personal data is processed in a new way
- the law or guidance changes (AI Act acts and guidelines, a supervisory authority decision)
- **the WDS default changes:** the conflict check below

**Conflict check (Idun).** When the `wds-*` files change at sync, or on request, Idun compares {Org}'s policy with the default. A new default rule that {Org} has not addressed, or an {Org} rule that is looser than the default, becomes a row in the deviations table in [principles]({org}-principles.md). The stricter rule applies until {Org} decides: adopt the default, or record a difference in the table above with a reason, approved by the approver.

## Not filed with any authority

This policy is {Org}'s own evidence. It is not filed with any authority. Neither GDPR nor the EU AI Act requires an organization to file its governance documents. It is kept current and shown on request, for example during an inspection.

Only these events involve an authority, and each is handled in its own file:

| Event | Authority | File |
|---|---|---|
| A personal data breach likely to result in a risk to people (GDPR Art. 33) | The supervisory authority ({supervisory authority}) | [incidents]({org}-incidents.md) |
| A DPIA shows high residual risk that cannot be mitigated (GDPR Art. 36, prior consultation) | The supervisory authority | [data]({org}-data.md) |
| A data protection officer is designated (GDPR Art. 37(7)) | The supervisory authority | this file, Accountability |

A high-risk classification under the AI Act brings obligations that involve an authority (registration, Art. 49; fundamental rights impact assessment results, Art. 27(3); serious incidents, Arts. 26(5) and 73). See [risk]({org}-risk.md) and get legal review.

## Approval

**Approved by:** {name}
**Role:** Approver, {title}
**Date:** {date}
**Signature:** ________________________

## Version history

| Version | Date | Change | Approved by (role) |
|---|---|---|---|
| 0.1 | {date} | Copied from the WDS default | |
