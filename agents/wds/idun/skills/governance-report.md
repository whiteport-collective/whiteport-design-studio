---
name: idun-governance-report
agent: idun
phase: 1
version: 0.4
inputs:
  - business name
  - org structure (size, roles, decision-makers)
  - AI tools currently in use
  - data categories handled
  - decision authority preferences
  - client transparency approach
  - incident response contacts
  - integration architecture (what AI connects to)
  - agent roster and autonomy levels
outputs:
  - {businessname}-agent-space GitHub repo
  - ai-governance/ folder with 12 documents (live-written, one commit per section)
  - an approved suite the organization keeps as its own evidence (nothing is filed with an authority)
---

## Intent

Produce a complete, signed AI governance suite for a WDS client. The suite is written live — one commit per dialog step — so the client follows progress in real time.

The suite is structured around the **AI Governance Stack** (Kenney, 2026): five layers covering Data, Model, System Integration, Control & Monitoring, and Audit & Evidence — plus a WDS-original Layer 2.5 for Agent Governance. The suite is designed to support compliance with GDPR (ROPA, DPIAs, Article 22) and the EU AI Act (Article 4 AI literacy, Article 50 transparency, and Articles 8–15 and 26 where a high-risk system is involved), and it maps to the NIST AI RMF (GOVERN, MAP, MEASURE, MANAGE functions). Writing the suite does not by itself make an organization compliant.

The repo and document skeletons exist before the first question is asked.

---

## Regulatory Foundation

Reference these frameworks throughout the dialog and documents:

| Framework | Key requirements | Applicability |
|-----------|-----------------|---------------|
| **GDPR** | Article 5 (7 principles), Article 22 (right not to be subject to a solely automated decision with legal or similarly significant effects, with limited exceptions), Article 30 (ROPA), Article 35 (DPIA) | Organizations in the EU processing personal data, and organizations outside the EU that offer goods or services to, or monitor, people in the EU |
| **EU AI Act 2024/1689** (as amended by the Digital Omnibus on AI, Regulation (EU) 2026/1744) | Article 4 AI literacy for all providers and deployers; Article 50 transparency (chatbots, synthetic content, deepfakes, AI-generated text published to inform the public, emotion recognition and biometric categorisation); Articles 8–15 (provider requirements) and Article 26 (deployer obligations) for high-risk systems; GPAI model rules (Articles 53–55) apply to model providers, not to organizations that only use the models | Providers and deployers of AI systems in the EU |
| **NIST AI RMF 1.0** (NIST AI 100-1, January 2023; a revision is in progress) | GOVERN, MAP, MEASURE, MANAGE | Voluntary. Often cited as a benchmark of reasonable care, but not a legal requirement |
| **EU AI Act timeline** (Article 113, as amended) | AI literacy (Article 4) and prohibited practices: 2 Feb 2025 ✓ · GPAI model obligations: 2 Aug 2025 ✓ · Article 50 transparency and most remaining provisions: 2 Aug 2026 ✓ (systems already on the market before 2 Aug 2026 have until 2 Dec 2026 for the Article 50(2) machine-readable marking) · New prohibitions on non-consensual intimate imagery and child sexual abuse material: 2 Dec 2026 · High-risk, Annex III: 2 Dec 2027 · High-risk, Annex I (regulated products): 2 Aug 2028 | |
| **Penalties** | EU AI Act (Article 99): up to €35M or 7% of global turnover for prohibited practices · up to €15M or 3% for most other obligations, including deployer duties (Article 26) and transparency (Article 50) · up to €7.5M or 1% for incorrect or misleading information to authorities · for SMEs, whichever is lower. GDPR (Article 83): up to €20M or 4% (e.g. principles, legal basis, Article 22, transfers) · up to €10M or 2% (e.g. Articles 30, 33, 35, 37) | |

---

## AI Governance Stack (Organizing Framework)

All 12 documents map to this stack. Use it to explain the structure to clients:

| Layer | Covers | Documents |
|-------|--------|-----------|
| Layer 1: Data Governance | Data inventory, classification, quality, privacy, bias | 03 (Data Processing Register, including Data Classification) |
| Layer 2: Model Governance | Architecture review, fairness testing, robustness, model cards | 07 (Model Governance / Human Oversight) |
| Layer 2.5: Agent Governance | Authorization profiles, agent-to-agent interaction, auditability, versioning | 12 (Agent Governance) |
| Layer 3: System Integration | Integration architecture, pipeline security, cascading failure, boundary testing | 11 (System Integration Governance) |
| Layer 4: Control & Monitoring | Access controls, real-time monitoring, incident response, deployment gates | 05 (Incident Response), 10 (Access Control Groups) |
| Layer 5: Audit & Evidence | Documentation standards, audit trails, review schedules | 09 (Audit & Review Log) |

**Critical Integration Rule**: Failures cascade upward through the Stack. Layer 1 failures corrupt Layer 2 outputs, which corrupt Layer 3 behavior, which evade Layer 4 detection. Every layer must have exactly one primary owner.

---

## Governance Maturity Target

| Level | Description | Target |
|-------|-------------|--------|
| 1 — Ad Hoc | No systematic governance | |
| 2 — Defined | Policies exist, implementation inconsistent | |
| **3 — Managed** | **Processes standardized and consistently applied. Metrics tracked.** | **← WDS default target** |
| 4 — Measured | Governance effectiveness quantitatively measured | |
| 5 — Optimized | Fully automated governance integrated into development workflows | |

Recommended target (Kenney 2026, not a legal requirement): high-risk AI systems at Level 3 minimum at all five layers.

---

## Process

### Step 0 — Create repo and skeleton BEFORE the first question

As soon as the client provides their business name, execute all of the following before asking anything else:

1. Create GitHub repo: `{org}/{businessname}-agent-space` (private) — or confirm it exists
2. Create folder: `ai-governance/`
3. Write 12 skeleton documents (see Document Skeletons section below)
4. Commit: `chore: create AI governance suite skeleton — 12 documents`
5. Tell the user: "The repo is live at {url}. You can follow the documents being written in real time. Let's begin."
6. Then ask the first question.

---

### Step 0.5 — AI Adoption Assessment + Management Sign-off

This step has two parts: Idun assesses the current level from the conversation, then surfaces it to management for explicit confirmation and target commitment.

---

**Part A — Current Level Assessment (Idun infers silently)**

Listen for signals across the Shapiro/AE-MM levels (both models run from Level 0 to Level 5):

| What they say | Level |
|--------------|-------|
| "We use ChatGPT, Copilot helps us write things" | 0–1 |
| "Everyone uses the same AI tools, we have shared setup" | 2 |
| "Our agents execute tasks end-to-end, humans validate" | 3 |
| "Agents own delivery pipelines, we handle exceptions" | 4 |
| "Anyone can spec something and agents build it" | 5 |

Do not ask the client to classify themselves by number. Infer from context. If ambiguous, continue — the rest of the dialog will clarify.

**Scope gate:** Level 0–1 → not WDS-E. Redirect to standard WDS. No agent governance needed yet.

---

**Part B — Management Sign-off Questions**

Once current level is assessed, present it and ask these four questions. One at a time. These are not technical questions — they are management decisions that require the decision-maker's voice.

**Question 1 — Confirm current level:**
> "Based on what you've described, I'd place you at Level [X] — [name]. Does that match how you see it?"

*Listen for:* Pushback (they may think they're higher — explore why), agreement, nuance ("we're level 2 in some teams, level 1 in others").

**Question 2 — Target level:**
> "Where do you want to be — and what's driving that? Is there a deadline, a competitive pressure, a specific capability you need to unlock?"

*Listen for:* Specific level or capability ("we want agents executing end-to-end"), timeline ("by end of year"), driver ("our competitors are already there", "we need to ship faster").

**Question 3 — What changes:**
> "Moving from Level [X] to Level [Y] means changing how decisions get made and what people are empowered to do on their own. What are you prepared to change — and what's off the table?"

*Listen for:* What the org is willing to restructure vs. protect. This reveals the real constraint. Common answers: "we can't change sign-off processes" (culture barrier), "we're open to anything" (often not true), "we need to keep legal/finance out of it" (realistic constraint).

**Question 4 — Named owner:**
> "Who in your organization is personally accountable for this adoption journey — the person whose name goes on the commitment?"

*Listen for:* Named principal. If they name someone who isn't in the room, flag it — the commitment needs the decision-maker's sign-off, not a delegate.

---

**Governance implication by level:**

| Current → Target | WDS-E scope |
|-----------------|------------|
| L1–2 → L3 | Full 12-doc governance suite — must be in place before L3 deployment |
| L3 → L4 | Governance suite + per-user authorization profiles + AIVSS scoring |
| L3 (retroactive) | Same suite + gap assessment of live agent deployments |
| L4+ | Targeted governance audit — not standard onboarding |

---

**Write into `00-introduction.md`:**

> ## AI Adoption Commitment
>
> **Current level:** Level [X] — [Name]
> **Target level:** Level [Y] — [Name]
> **Timeline:** [When]
> **Driver:** [What's pushing this]
> **What changes:** [What the org commits to restructuring]
> **What's protected:** [Explicit constraints]
> **Adoption owner:** [Named person, title]
> **Confirmed by:** [Decision-maker name, title, date]

**Commit:** `docs: 00 — AI adoption commitment`

---

### Step 0.6 — Level-Up Dialog

Once current and target levels are confirmed, Idun walks through each intermediate level — one at a time. For each level on the path, she describes what it looks like in practice and asks what needs to change.

**The pattern for each level:**

1. Idun describes the level in plain language (see scripts below)
2. Ask: *"What would need to be different in your organization to operate this way?"*
3. Listen — probe with: *"Who currently has the authority to approve that change?"*
4. Capture: what changes, who owns it, who must grant authority

Repeat for each level between current and target. Do not rush. One level at a time.

---

**Level descriptions (Idun's voice — plain, concrete, no jargon):**

**Level 1 → Level 2:**
> "At Level 2, everyone uses the same AI tools with the same setup. No individual experimentation — it's organized. Shared prompt library, shared configuration, a basic policy for what AI can and can't be used for. Your team knows what tools they have and how to use them consistently."

**Level 2 → Level 3:**
> "At Level 3, agents execute tasks end-to-end. A person defines what needs to happen — the agent does it — the person validates the outcome. The agent can access your systems, do research, write documents, coordinate with other agents. You're not reviewing every step. You're approving results. The human role shifts from doing to defining and validating."

**Level 3 → Level 4:**
> "At Level 4, agents own delivery pipelines. People write specifications — what needs to exist, what it should do, what success looks like — and agents build, test, and deploy from that. Your team's job is directing, not executing. Architecture decisions and exceptions still come to humans. Everything else runs."

**Level 4 → Level 5:**
> "At Level 5, anyone in your organization can come up with an initiative, work it through with an agent, and deploy it — within defined guardrails. The organization moves at the speed of ideas. The constraint is no longer 'who has the resources to build this.' It's 'can we describe it well enough for agents to build it safely.'"

---

**For each level, capture a Level-Up Plan:**

| What needs to change | Who owns this change | Who must approve it | By when |
|---------------------|---------------------|--------------------|---------| 
| [e.g. agents get write access to staging environment] | [e.g. CTO] | [e.g. CTO + Security lead] | [Q3 2026] |

**Also capture Authority Grants** — explicit permissions that must be issued for the level to work:

| Permission | Currently held by | Granted to | Condition |
|-----------|------------------|-----------|-----------|
| [e.g. agents can send external communications] | [Principal only] | [Named agents with escalation] | [Human review at gate] |
| [e.g. anyone can propose an initiative via Idun] | [Management only] | [All staff] | [Idun qualification required] |

---

**What blocks most organizations at each level:**

| Transition | Most common blocker |
|-----------|-------------------|
| L1 → L2 | No one owns the standardization decision |
| L2 → L3 | Trust — people can't let go of reviewing every output |
| L3 → L4 | Spec-writing skill — people don't know how to describe what they want precisely enough |
| L4 → L5 | Authority distribution — leadership won't give individuals the power to deploy |

Surface the blocker explicitly: *"What you're describing sounds like [blocker]. Is that accurate? What would need to be true for that to change?"*

---

**Write into `00-introduction.md`:**

For each level on the path, a section:

> ## Level-Up Plan: Level [X] → Level [Y]
>
> **What Level [Y] looks like for [Org]:**
> [2–3 sentences in their words, not Idun's description]
>
> **Changes required:**
> | What changes | Owner | Authority required | Timeline |
>
> **Authority grants:**
> | Permission | From | To | Condition |
>
> **Known blockers:**
> [What they identified as the hard part]
>
> **Signed off by:** [Name, title, date]

**Commit per level:** `docs: 00 — Level-up plan L[X] to L[Y]`

---

### Step 1 — Organization

**Question:** "Tell me about your organization — what do you do, where are you based, and who is the decision-maker?"

**Listen for:** Business type, location (Sweden/EU = GDPR + EU AI Act), org size, principal name, sub-contractors or external parties.

**Governance implication:** Swedish organization → IMY is the GDPR supervisory authority. For the EU AI Act, the government has given interim assignments (decision 12 June 2026, until 31 December 2026, pending national legislation) to PTS (single point of contact), IMY (for example law enforcement and creditworthiness AI), Finansinspektionen, Läkemedelsverket and Swedac. Any sub-contractor or tool outside the EU/EEA that receives personal data triggers the GDPR Chapter V transfer rules (Articles 44–49). Document explicitly.

**Write:** `00-introduction.md` — Organization section + Document Index
**Commit:** `docs: 00 — Introduction and organization`

---

### Step 2 — Accountability

**Question:** "Who is personally responsible for everything that leaves your business — including work done by AI or sub-contractors?"

**Listen for:** Named principal, chain of accountability, whether any governance board or compliance function exists.

**Governance implication:** GDPR Article 5(2) makes the controller accountable for, and able to demonstrate, compliance. For high-risk AI systems, EU AI Act Article 17(1)(m) requires providers to have an accountability framework in their quality management system, and Article 26(2) requires deployers to assign human oversight to people with the necessary competence, training and authority. (Article 9 is the risk management system, not a governance structure.) Solo principal = clear and auditable. Multi-person orgs need documented authority chains.

**Write:** Accountability section in `00-introduction.md`, named principal in signature block
**Commit:** `docs: 00 — Accountability structure`

---

### Step 3 — AI Risk Classification

**Question:** "Which of these describes how your AI works? (a) You use commercial AI tools as assistants — they help you produce work that you then review and deliver. (b) Your AI makes recommendations or decisions that directly affect your clients or their end users. (c) Your AI operates in a high-stakes domain — healthcare, hiring, credit, legal, safety."

**Listen for:** Classification signals for EU AI Act risk tier.

**EU AI Act classification decision tree:**

| If... | Then... | Layer activation |
|-------|---------|-----------------|
| None of the rows below applies (also an Annex III system that only performs a narrow procedural task, Article 6(3), unless it profiles people) | Minimal risk — no specific obligations beyond Article 4 AI literacy; voluntary codes of conduct (Article 95) | Baseline |
| AI interacts directly with people (chatbot), generates synthetic audio, image, video or text, produces deepfakes or AI-generated text published to inform the public on matters of public interest, or performs emotion recognition or biometric categorisation | Limited risk — Article 50 transparency (applies from 2 Aug 2026) | Layers 1–3 |
| AI used in Annex III areas (biometrics, critical infrastructure, education, employment, access to essential private and public services such as public benefits, credit scoring, life and health insurance pricing and emergency call triage, law enforcement, migration and border control, justice and democratic processes), or AI that is a safety component of a product under Annex I (e.g. medical devices, toys, lifts) | **High risk** — Articles 8–15 (providers) and Article 26 (deployers); applies from 2 Dec 2027 (Annex III) and 2 Aug 2028 (Annex I) | All 5 layers at maximum rigor |
| The org itself provides a GPAI model (systemic risk is presumed above 10^25 FLOP of training compute, Article 51). Using a GPAI model through a tool does not make the org a GPAI provider | GPAI provider obligations (Article 53), plus systemic-risk obligations (Article 55); apply from 2 Aug 2025 | Enhanced Layer 2 + 5 |

**Write:** `04-ai-risk-assessment.md` — risk classification section
**Commit:** `docs: 04 — AI risk classification`

**If high-risk classification applies:** Document the Articles 8–15 requirements (providers) and the Article 26 deployer obligations, plus a fundamental rights impact assessment (Article 27) where the deployer is a public body, provides public services, or uses credit scoring or life and health insurance pricing. This is not optional. The binding dates are 2 December 2027 for Annex III systems and 2 August 2028 for Annex I products, as amended by the Digital Omnibus on AI (Regulation (EU) 2026/1744).

---

### Step 3.5 — AIVSS Agentic Risk Scoring

No additional question needed. Based on Steps 3 and 4 answers, silently assess the agentic risk profile.

**Silently score the 10 AIVSS amplification factors** based on what the client has described:

| Factor | Description | 0.0 | 0.5 | 1.0 |
|--------|-------------|-----|-----|-----|
| Autonomy | Agent acts without human co-sign | Never | Non-critical paths only | Production/critical systems |
| Tools | Breadth/privilege of external tools | Read-only | Mixed, scoped | Broad: cloud, DB, CI/CD |
| Language | NL drives agent control logic | Structured API only | NL for retrieval only | NL drives execution |
| Context | Environmental signals drive decisions | None | Narrow signals | Broad signals → autonomous |
| Non-Determinism | Variance in outputs | Deterministic | Bounded | High variance, weak guards |
| Opacity | Decision logic traceable | Full traceability | Partial logs | Cannot trace why action taken |
| Persistence | Memory across sessions | Stateless | Session-only | Long-term (vector DB) |
| Identity | Dynamic role/identity changes | Fixed | Scoped swaps | Cross-tenant dynamic |
| Multi-Agent | Coordinates with other agents | Isolated | 1–2 known agents | Complex orchestration |
| Self-Mod | Can alter own tools/code/goals | None | Own prompts only | Tools, control flow, code |

**Calculate Factor_Sum** (0.0–10.0). Use it to classify:

| Factor_Sum | Risk Level | Governance implication |
|-----------|-----------|----------------------|
| 0–4 | **Low** | Standard 12-doc suite sufficient |
| 4.1–7 | **Moderate** | All docs mandatory; Section 11 + 12 at full depth; named approver required |
| 7.1–10 | **High** | Full suite + AIVSS-specific controls in docs 11 and 12; pre-deployment sign-off required; kill switch and prompt injection defense must be built before go-live |

These Factor_Sum bands are a WDS heuristic. AIVSS v0.8 itself uses Factor_Sum inside a per-vulnerability formula together with a CVSS v4.0 base score, and its severity bands (Low 0.1–3.9, Medium 4.0–6.9, High 7.0–8.9, Critical 9.0–10.0) apply to that final score.

**Key signals that push toward High:**
- Agent sends external communications autonomously (Autonomy 1.0)
- Agent accesses production databases or APIs with write access (Tools 1.0)
- No human checkpoint before client-facing output (Autonomy 1.0)
- No way to trace why the agent took an action (Opacity 1.0)
- Agent coordinates with other agents in workflows (Multi-Agent 0.5+)

**Mandatory additions at Moderate/High:**
- Doc 04 gets AIVSS score and factor breakdown
- Doc 11 gets tool inventory, DLP, and kill switch sections
- Doc 12 gets memory scope policy, prompt injection defense, and governance structure

**Write:** AIVSS Factor_Sum, risk level, and factor breakdown into `04-ai-risk-assessment.md`
**Commit:** `docs: 04 — AIVSS agentic risk scoring`

---

### Step 4 — AI Tools in Use

**Question:** "What AI tools do you currently use, and what does each one do?"

**Probe for:** Core tools (LLMs), agentic tools (that take actions autonomously), task-specific tools, tools used by sub-contractors.

**Write:** `02-ai-use-policy.md` — Tool table: Tool | Provider | Role | Type (Core / Agentic / Task-specific) | Data processor location

**GDPR flag (mandatory):** If any tool's data processor is outside EU/EEA, note the cross-border transfer basis explicitly: an adequacy decision (Article 45) or appropriate safeguards such as SCCs (Article 46). For US processors, the EU–US Data Privacy Framework covers only certified organizations. The General Court upheld it on 3 September 2025 (T-553/23, Latombe), and an appeal (C-703/25 P) is pending at the Court of Justice, so note a fallback such as SCCs.

**Commit:** `docs: 02 — AI tools in use`

---

### Step 5 — Data Handling

**Question:** "What kinds of data pass through your AI tools? Think about client data, personal information, financial records, code, credentials."

**Probe for:** Data categories, special categories (health, biometrics, financial), credential handling, sub-contractor data access.

**Recommended data quality targets to introduce** (Kenney 2026, control DG-2 and data governance decision rules; not legal thresholds. GDPR Article 5(1)(d) requires accurate data but sets no percentages):
- Completeness ≥95%, Accuracy ≥98%, Consistency ≥90%, Timeliness ≤30 days stale
- Training data: document demographic distribution vs. deployment population
- Identify proxy variables with >0.7 correlation to protected characteristics

**Write:** `03-data-processing-register.md` — ROPA (GDPR Article 30): Data subject | Data category | Legal basis | Processor | Retention | Cross-border transfer

**Commit:** `docs: 03 — Data processing register (ROPA)`

---

### Step 6 — Data Classification

**Question:** "How sensitive is the data you handle? Does any of it include personal data, health information, financial records, or credentials?"

**Write:** Data classification section in `03-data-processing-register.md` — classification tiers:

| Tier | Definition | Examples | Required controls |
|------|-----------|---------|------------------|
| Public | Intended for external publication | Marketing copy, public docs | None |
| Internal | Operational data, not personal | Project notes, code | Basic access control |
| Confidential | Personal or sensitive business data | Client details, financial | Encrypted, access-logged |
| Restricted | Special categories, credentials | Health data, passwords | Encrypted, strictly need-to-know |

**Commit:** `docs: 03 — Data classification`

---

### Step 7 — Agent Authorization Framework

**Question:** "For each AI agent in your system — what can it do on its own, and what needs your approval first?"

Walk through categories if needed: client communications, code commits, deployments, financial documents, access management, public publishing, credential access.

**Authorization levels:**
- **Autonomous** — agent completes without review
- **Escalate** — agent prepares, human approves before execution
- **Prohibited** — agent may never initiate

**Key defaults:**
- Anything that leaves the org's systems → Escalate (not autonomous)
- Multi-agent outputs → always require human review before client delivery
- Financial commitments, credential access, production deployments → Prohibited without explicit human initiation

**Override rate target** (heuristic from Kenney 2026, not a legal requirement): 5–20%. Below 2% = possible automation bias. Above 20% = possible model performance issue.

**Write:** `12-agent-governance.md` — agent roster with authorization profiles, escalation thresholds, coordination failure controls

**Commit:** `docs: 12 — Agent governance`

---

### Step 8 — Human Oversight Protocol

**Question:** "How do you stay in the loop? Walk me through what happens before something goes to a client."

**Listen for:** Review gates, approval steps, what the human actually sees before approving.

**Human oversight checklist** (WDS, based on EU AI Act Article 14(4) and Article 26(2). Those articles bind high-risk systems only; WDS applies the checklist to every agent as good practice):
- Human can see what inputs the AI used ✓/✗
- Confidence or reasoning is visible to reviewer ✓/✗
- Human can override or reject at any point ✓/✗
- Override decisions are logged ✓/✗
- No auto-advance or timer pressure ✓/✗

**Automation bias warning:** If the review process shows "AI recommended X — approve?" without showing the reasoning, document this as a governance gap. Humans must have genuine authority to override, not just a confirm button.

**Write:** `07-human-oversight-protocol.md` — autonomy levels, review gates, override logging, override rate monitoring

**Commit:** `docs: 07 — Human oversight protocol`

---

### Step 9 — System Integration Governance

**Question:** "What does your AI connect to? Think about APIs, databases, client systems, CRMs, or other tools that your agents read from or write to."

**Probe for:** Number of integrations, whether integrations cross organizational boundaries, cascading failure risk, whether consequential actions are triggered automatically.

**Cascade risk assessment:**
- >3 downstream dependencies from a single AI output → circuit breaker required
- AI output triggers financial record creation → human-in-the-loop required before the record is created
- Data pipeline crosses org boundary → integrity verification at the boundary required

**Write:** `11-system-integration-governance.md` — integration architecture, data pipeline security, circuit breaker plan, boundary condition testing

**Commit:** `docs: 11 — System integration governance`

---

### Step 10 — Incident Response

**Question:** "If an AI agent makes a mistake that affects a client — who handles it, and what are the first three things they do?"

**GDPR 72-hour breach notification:** If the incident involves a personal data breach, GDPR Article 33 requires notification to the supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware of it, unless the breach is unlikely to result in a risk to people's rights and freedoms. Every breach must be documented internally, whether notified or not. Named principal must know this obligation exists and have IMY contact ready. (The general Digital Omnibus, COM(2025) 837, proposes 96 hours and notification only of high-risk breaches. It is proposed, not adopted.)

**Incident categories to cover:**
1. Wrong content sent to client
2. Personal data processed without valid basis
3. AI output caused incorrect advice given to client
4. Security incident / unauthorized access
5. Meeting recorded without consent

**Write:** `05-incident-response-plan.md` — step-by-step procedures per incident type, GDPR 72-hour clock, named contacts

**Commit:** `docs: 05 — Incident response plan`

---

### Step 11 — Vendor Assessment

**Question:** "For each AI tool you use — do you know whether they use your data for model training, and where they store it?"

**Write:** `06-vendor-assessment.md` — Due diligence table: Vendor | Service | Data location | GDPR compliant | Trains on data | Risk rating | Required actions

**Commit:** `docs: 06 — Third-party vendor assessment`

---

### Step 12 — Client Transparency

**Question:** "Do your clients know you use AI tools? How do you communicate this?"

**If not in client agreements yet, offer the recommended addition:**

> {Business} uses AI-assisted tools in the delivery of services. All work is reviewed and approved by {Principal} before delivery. {Business} remains fully responsible for the quality and accuracy of all deliverables. Clients may request information about which AI tools were used in the delivery of any specific project.

**EU AI Act Article 50 (applies from 2 August 2026):** People must be told when they interact with an AI system such as a chatbot (50(1)). Providers of generative AI must mark output as AI-generated in a machine-readable way (50(2)). Deployers must inform people exposed to emotion recognition or biometric categorisation (50(3)), and must disclose deepfakes (50(4)). Under 50(4), AI-generated or manipulated text published to inform the public on matters of public interest must be disclosed, unless it has gone through human review or editorial control and a person or organization holds editorial responsibility. This clause matters for communications departments. If any applies, this is mandatory — not optional.

**Write:** `08-client-disclosure-policy.md` — disclosure text, timing, client objection handling, meeting recording consent (if Fireflies or equivalent)

**Commit:** `docs: 08 — Client disclosure policy`

---

### Step 13 — AI Skill Governance

**Question:** "Agents can create and use custom skills and instructions. Should all skills used in your organization be registered in Agent Space so they can be audited?"

This is almost always yes. Explain if needed:
> "Registration means Idun can see every custom instruction any agent is running and flag anything that looks dangerous or violates your policies. Agents can still create and use personal skills freely — they just get uploaded so there's visibility."

Three stances:
- **Open** — agents register skills voluntarily, no enforcement
- **Managed** (recommended default) — all skills must be registered; unregistered skills in active use = governance violation
- **Strict** — skills must be approved by Idun before use

Default: **Managed** unless the org explicitly chooses otherwise.

**Write into `12-agent-governance.md`:**

| Action | Agent can do autonomously | Requires approval |
|--------|--------------------------|------------------|
| Use a personal/custom skill | ✓ | — |
| Register a skill in Agent Space | ✓ (required) | — |
| Promote a skill to org-wide use | — | ✓ Idun |
| Modify an existing org-level skill | — | ✓ Idun |

**Commit:** `docs: 12 — AI skill governance added`

---

### Step 14 — Monitoring and Audit Schedule

No additional questions needed. Based on all previous answers, establish the monitoring schedule.

**Write:** `09-audit-review-log.md` — review schedule with named responsible parties:

| Cadence | Who | What |
|---------|-----|------|
| **Daily** | Principal | Pending approvals in Agent Space; any circuit breaker trips |
| **Monthly** | Idun (automated) | Skill audit, override rate, audit log anomalies, governance manifest check |
| **Quarterly** | Principal | Tool and access review, override rate analysis, vendor assessment refresh |
| **Annually** | Principal | Full governance suite review, GDPR safeguards, EU AI Act re-classification, version increment |

**Trigger reviews** (immediate):
- New AI tool or sub-contractor added
- Personal data breach or near-miss
- Agent acts outside its authorized scope
- Relevant regulatory change (EU AI Act guidance, IMY ruling)

**Commit:** `docs: 09 — Monitoring and audit schedule`

---

### Step 15 — Agent Space Implementation Requirements

No additional questions needed. Map each governance section to a concrete Agent Space build requirement.

**Write:** Implementation requirements section in `00-introduction.md`:

| Governance area | Required Agent Space capability | Status |
|----------------|--------------------------------|--------|
| Org identity | Org record in `orgs` table | Built / Pending |
| Agent identity gate | No anonymous agent access; all messages tagged with org_id | Built / Pending |
| Authorization profiles | `escalate_types` and `prohibited_types` per agent | Built / Pending |
| Outbound gate | `approval_status: "pending"` for Level 2 actions | Built / Pending |
| Audit trail | Append-only `agent_audit_log` with actor attribution | Built / Pending |
| Data scope | Project-strict filtering in `check` action | Built / Pending |
| Skill registry | Skills table with status lifecycle + Idun audit queue | Built / Pending |
| Circuit breakers | Circuit breaker status in agent presence | Built / Pending |

Mark Built only if already confirmed. Everything else: Pending.

**Commit:** `docs: 00 — Agent Space implementation requirements`

---

### Step 16 — Build Verification

Write one test per capability confirming it actually works. Short and actionable.

**Write:** Verification section in `00-introduction.md`

**Commit:** `docs: 00 — Build verification tests`

---

### Step 17 — Finalize

1. Remove "Status: In progress" from all document headers
2. Add approval block to `00-introduction.md`:

```markdown
---

## Approval

**Approved by:** {Principal Name}
**Title:** {Title}
**Date:** {Date}
**Signature:** ________________________
```

3. Update `00-introduction.md` Document Index to list all 12 documents accurately
4. Final commit: `docs: AI governance suite v1.0 — complete (12 documents)`
5. Show completed document index in chat for review
6. Tell the client: the suite is the organization's own evidence. It is not filed with any authority. It is kept up to date and shown on request, for example during an inspection.

---

### No filing — what does go to an authority

The governance suite is never submitted. Neither GDPR nor the EU AI Act requires an organization to file its governance documents. Do not offer to submit them.

Only these events involve an authority, and each one is documented in its own document:

| Event | Authority | Document |
|-------|-----------|----------|
| Personal data breach that is likely to result in a risk to people (GDPR Article 33, where feasible within 72 hours) | Supervisory authority (IMY in Sweden) | 05 Incident response |
| A DPIA shows high residual risk that cannot be mitigated (GDPR Article 36, prior consultation) | Supervisory authority | 03 Data processing register |
| A data protection officer is designated (GDPR Article 37(7): the DPO's contact details are communicated to the authority) | Supervisory authority | 00 Introduction |

**Flag explicitly:**
- Special category data (health, biometrics, ethnicity, etc.) → a DPIA under Article 35 may be required. It is kept internally, not filed.
- High-risk classification under the EU AI Act (Step 3) → refer to legal review for the obligations that involve an authority: registration in the EU database (Article 49; for deployers, only public authorities), notifying the results of a fundamental rights impact assessment (Article 27(3)), and reporting serious incidents (Articles 26(5) and 73).

---

## Document Skeletons

Create these 12 files in `ai-governance/` before the first question. All sections marked `*[In progress]*`:

```
00-introduction.md           — Org overview, AI adoption commitment (current level / target / owner / sign-off), document index, implementation requirements, approval block
02-ai-use-policy.md          — Permitted/prohibited uses, tool table, tool-specific rules
03-data-processing-register.md — ROPA (Article 30), all processing activities, legal basis, cross-border transfers
04-ai-risk-assessment.md     — EU AI Act risk classification, risk register per tool, AIVSS agentic risk score + factor breakdown
05-incident-response-plan.md — Step-by-step procedures per incident type, GDPR 72h clock
06-vendor-assessment.md      — Due diligence table for every AI vendor
07-human-oversight-protocol.md — Autonomy levels, review gates, override logging and rate monitoring
08-client-disclosure-policy.md — Disclosure text, client objection handling, meeting consent
09-audit-review-log.md       — Review schedule, version history, trigger review events
10-access-control-groups-policy.md — Role-based access, least privilege, access review cadence
11-system-integration-governance.md — Integration architecture, pipeline security, circuit breakers, boundary testing,
                                      tool inventory + authentication controls, outbound DLP, kill switch protocol,
                                      supply chain vetting for tool integrations
12-agent-governance.md       — Agent authorization profiles, agent-to-agent rules, auditability, versioning,
                                pre-deployment AIVSS classification, memory scope isolation, goal integrity /
                                prompt injection defense, AI governance structure
```

---

## Quality Rules

- Repo and skeletons MUST exist before the first question. No exceptions.
- One commit per section. Never batch commits.
- Never skip a section — even "not applicable" must be written explicitly with rationale.
- GDPR cross-border transfer note is mandatory if any party or tool is outside EU/EEA.
- EU AI Act risk classification is mandatory — every org must know which tier they are in.
- Authorization table (Step 7) must have an explicit default rule: anything leaving the org requires human review.
- Final document must have a named approver and signature block before it is complete.
- AI Skill Governance is mandatory for any org using Agent Space — never skip it.
- Sections covering implementation requirements, verification tests, and audit schedule are mandatory — a governance document without operational controls is a paper artifact, not a live system.
- Sections 11 (System Integration) and 12 (Agent Governance) are mandatory for any org deploying agentic AI.
- AIVSS agentic risk scoring (Step 3.5) is mandatory for any org with autonomous agents — the Factor_Sum must appear in Doc 04 before the suite is complete.
- At Moderate AIVSS risk (Factor_Sum 4.1–7): docs 11 and 12 must include all AIVSS-specific sections (tool inventory, kill switch, memory scope, prompt injection defense).
- At High AIVSS risk (Factor_Sum 7.1–10): a named pre-deployment approver and sign-off date must appear in Doc 12 before any agent goes live.

## Reference

Canonical example: `whiteport-collective/whiteport-agent-space` — `ai-governance/`
Produced during Idun dry run with Whiteport (Mårten Angner, April 2026).

Regulatory framework: Governing Intelligence — Law, Privacy, Security, and Compliance in the Age of Artificial Intelligence (Noah M. Kenney, Digital 520, 2026). Full text: `docs/references/governing-intelligence.md` in WDS-EC repo.

Security risk framework: AIVSS Scoring System For OWASP Agentic AI Core Security Risks v0.8 (OWASP AI Vulnerability Scoring System project, aivss.owasp.org; v1.0 announced but not yet published). Full text: `docs/references/aivss-scoring-system.md`. Gap analysis vs. docs 11 and 12: `docs/references/aivss-extraction.md`. Both in WDS-EC repo.

Maturity model: ENDGAME Agentic Engineering Maturity Model (AE-MM) — Alex Barády, LinkedIn post and infographic, 2026 (not verified). Full text: `docs/references/ae-maturity-model.md`. WDS-E implications: `docs/references/ae-maturity-model-extraction.md`. Both in WDS-EC repo.

Adoption levels: Dan Shapiro, "The Five Levels: from Spicy Autocomplete to the Dark Factory" (blog post, January 2026; Levels 0–5), popularized by Nate B Jones. Full analysis: `martens-documents/Projects/WDS/References/five-levels-of-ai-coding.md`. Core insight: the bottleneck moves from "can we build it" to "can we specify it." Level 5 (Dark Factory) requires spec-writing ability — WDS is the specification factory that enables it.
