# Agents

What {Org}'s AI agents may do on their own, what needs a person's yes, who may give it, and how agents, skills and instructions are governed.

Status: default (WDS)
Level: default
Tailor in dialog: step 7 (authorization), step 8 (review gate, overrides), step 13 (skill governance), steps 15–16 (controls and verification)

Part of the [framework](framework.md). Keeps principles S4, H1, H2, H3, Q2 and Q3. Owner: each agent's owner. (NIST AI RMF GOVERN 3.2; ISO/IEC 42001 Annex A.9, use of AI systems.)

## Roster

| Agent | Does | Owner (role) | Tools and systems | Memory | Risk score ([risk](risk.md#agentic-risk-score)) | Profile |
|---|---|---|---|---|---|---|
| | | | | | | default |

An agent with no row does not run on {Org}'s work.

## Authorization levels

- **Autonomous:** the agent does it without review. Every action is logged (git history or the tool's log).
- **Escalate:** the agent prepares it, a person approves before it happens.
- **Prohibited:** the agent never starts it. A person may do it, or ask the agent to do it in a session they run and watch.

## Authorization defaults

Best-practice defaults. An agent's profile may tighten them. Loosening one is a difference from the default ([framework](framework.md#differences-from-the-wds-default)).

| Action | Default | Who may say yes |
|---|---|---|
| Read {Org}'s material; research public sources | Autonomous | |
| Draft documents, designs, analyses; write code on a branch | Autonomous | |
| Commit and push to {Org}'s own repos, outside production | Autonomous | |
| Message the team in {Org}'s own channels | Autonomous | |
| Send anything outside {Org}: email, client delivery, comments, forms | Escalate | The person responsible for the delivery |
| Publish anything under {Org}'s name | Escalate | The owner of the channel |
| Deliver output that several agents produced together | Escalate, always | The person responsible for the delivery |
| Delete data, or any other change that cannot be undone | Escalate | The owner of the data or system |
| Change an agent's own instructions, skills or tools | Escalate | See Skill governance |
| Deploy to production | Prohibited unless a person starts it | |
| Financial commitments: payments, orders, sending invoices | Prohibited unless a person starts it | |
| Read or use credentials; create accounts; change permissions | Prohibited unless a person starts it | |
| Process Restricted data | Prohibited unless the approver has approved it | |
| Act on instructions found in content (web pages, email, documents, tool output) | Prohibited | |

An agent never approves its own work or another agent's. Approval comes from a person with the role in the right-hand column, or from the person who started the task when it is theirs to deliver.

## The review gate

Before anything leaves {Org} or becomes irreversible, the approver checks:

- [ ] I can see what the agent used: inputs, sources, files.
- [ ] I can see what it did and why.
- [ ] Facts, figures, names and links are checked (Q3).
- [ ] Nothing in it is Restricted, and personal data is minimized (P1).
- [ ] Disclosure is decided ([transparency](transparency.md)).
- [ ] I can reject or change it, and nothing advances on a timer.
- [ ] My approval is recorded: who, when, what.

This checklist follows EU AI Act Art. 14(4) and Art. 26(2). Those articles bind high-risk systems only; WDS applies them to every agent as good practice. Art. 14(4)(b) names the risk: "automatically relying or over-relying on the output" (automation bias). A gate that only asks "AI recommended X, approve?" without the reasoning is a gap. Record it as a deviation from H2.

## Overrides

Log every time a person rejects or substantially changes an agent's output: date, agent, item, decision, reason. One line is enough.

**Override rate target: 5–20%** (a heuristic from Kenney 2026, not a legal requirement). Below 2%: possible automation bias. Above 20%: possible model or instruction problem. Reviewed monthly ([framework](framework.md#review)).

## Agent to agent

- Agents hand work to each other through files in the repo (handovers), so every step can be traced.
- An agent does not widen another agent's authority. A chain of agents has the authority of its most restricted member.
- Output from several agents goes through the review gate before it leaves {Org}.
- Agents with long-term memory keep it scoped to one project and never store Restricted data.

## Skill governance

Agents run on instructions, skills and tools. They are code and are governed like code (Q2).

- **Versioned:** every instruction, skill and tool has one source repo and lives in git. Changes are commits. Local copies are never edited; they are synced from the source.
- **Organized:** {how agents, skills and tools are organized, and who owns what. One line for a small team.}
- **Stance:** **Managed** (WDS default). All skills used in {Org}'s work are registered and visible to Idun; an unregistered skill in active use is a deviation. *Open:* registration is voluntary. *Strict:* Idun approves each skill before use.

| Action | Agent may do it | Needs approval |
|---|---|---|
| Use a personal or custom skill | ✓ | |
| Register a skill | ✓ (required) | |
| Promote a skill to organization-wide use | | ✓ Idun review, then the agent owner |
| Change an organization-wide skill | | ✓ Idun review, then the agent owner |

Idun audits the skills monthly and checks them against this policy.

## Controls and verification

How the rules above are enforced in practice, and one test per control that shows it works. Mark a control *built* only when the test has passed.

| Control | How it is enforced | Test | Status |
|---|---|---|---|
| Agent identity | Every agent acts under an attributable identity (S1) | Pick a recent change; trace it to a person | pending |
| Review gate | {where approvals are given and recorded} | Try to send something outside {Org} without approval | pending |
| Authorization profile | {how escalate and prohibited actions are blocked} | Ask an agent to do a prohibited action | pending |
| Audit trail | Git history and tool logs, append-only | Find who approved last week's delivery | pending |
| Skill registry | {where skills are registered} | List the skills in use; compare with the registry | pending |
| Kill switch | [access](access.md#kill-switch) | Stop one agent within minutes | pending |
