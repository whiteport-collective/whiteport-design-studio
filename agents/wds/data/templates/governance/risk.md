# Risk

How {Org}'s use of AI is classified under the EU AI Act, how much risk its agents carry, and which risks are being managed.

Status: default (WDS)
Level: default
Tailor in dialog: step 3 (AI Act classification), step 3.5 (agentic risk score), step 4 (risk register per tool)

Part of the [framework](framework.md). Owner: the policy owner. (NIST AI RMF MAP; ISO/IEC 42001 clauses 6.1.2, AI risk assessment, and 6.1.4, AI system impact assessment.)

## AI Act classification

Classify every AI system and use, and record the role {Org} has: **deployer** (uses an AI system under its own authority) or **provider** (develops one, or has one developed, and places it on the market or puts it into service under its own name). Building your own chatbot or agent product can make {Org} a provider.

Work through the questions in order. Stop at the first that applies.

1. **Prohibited?** Is the use a prohibited practice (Art. 5)? Then stop using it. Prohibitions apply from 2 Feb 2025. New prohibitions on non-consensual intimate imagery and child sexual abuse material apply from 2 Dec 2026.
2. **High risk?** Is the AI used in an Annex III area (biometrics, critical infrastructure, education, employment, access to essential private and public services such as public benefits, credit scoring, life and health insurance pricing and emergency call triage, law enforcement, migration and border control, justice and democratic processes), or is it a safety component of a product under Annex I (e.g. medical devices, toys, lifts)? Then Articles 8–15 apply to providers and Article 26 to deployers, from **2 Dec 2027** (Annex III) and **2 Aug 2028** (Annex I), as amended by Regulation (EU) 2026/1744. An Annex III system that only performs a narrow procedural task is not high risk, unless it profiles people (Art. 6(3)). A fundamental rights impact assessment (Art. 27) is needed where the deployer is a public body, provides public services, or uses credit scoring or life and health insurance pricing. Get legal review.
3. **Transparency?** Does the AI interact directly with people (a chatbot), generate synthetic audio, image, video or text, produce deepfakes or AI-generated text published to inform the public on matters of public interest, or perform emotion recognition or biometric categorisation? Then Art. 50 applies, from 2 Aug 2026. See [transparency](transparency.md).
4. **Otherwise: minimal risk.** No specific obligations beyond Art. 4 AI literacy. Voluntary codes of conduct (Art. 95).

**GPAI** obligations (Arts. 53 and 55, from 2 Aug 2025) apply only if {Org} itself provides a general-purpose AI model. Using a GPAI model through a tool does not make {Org} a GPAI provider.

Most work with AI assistants and agents that produce work a person reviews and delivers is minimal risk, with Art. 50 where content is published or people talk to an AI. Check each use.

| AI system or use | {Org}'s role | Tier | Why | Obligations | Reviewed |
|---|---|---|---|---|---|
| | | | | | |

## Agentic risk score

A WDS heuristic, not law. It uses the ten amplification factors from the OWASP AI Vulnerability Scoring System (AIVSS v0.8). Score each agent, 0.0, 0.5 or 1.0 per factor:

| Factor | 0.0 | 0.5 | 1.0 |
|---|---|---|---|
| Autonomy: acts without a human co-sign | Never | Non-critical paths only | Production or critical systems |
| Tools: breadth and privilege | Read-only | Mixed, scoped | Broad: cloud, databases, CI/CD |
| Language: natural language drives control | Structured API only | Retrieval only | Drives execution |
| Context: environment drives decisions | None | Narrow signals | Broad signals, autonomous |
| Non-determinism | Deterministic | Bounded | High variance, weak guards |
| Opacity | Fully traceable | Partial logs | Cannot trace why |
| Persistence: memory | Stateless | Session only | Long-term |
| Identity: role changes | Fixed | Scoped swaps | Cross-tenant, dynamic |
| Multi-agent | Isolated | 1–2 known agents | Complex orchestration |
| Self-modification | None | Own prompts only | Tools, control flow, code |

| Factor sum | Level | What it requires |
|---|---|---|
| 0–4 | Low | This policy as is |
| 4.1–7 | Moderate | A named approver per agent; tool inventory, outbound data controls and a tested kill switch in [access](access.md); memory scope and prompt injection defense in [agents](agents.md) |
| 7.1–10 | High | All of Moderate, plus pre-deployment sign-off with a named approver and date in [agents](agents.md), and the kill switch and prompt injection defense built before go-live |

These bands are a WDS heuristic. AIVSS v0.8 itself uses the factor sum inside a per-vulnerability formula together with a CVSS v4.0 base score, and its severity bands apply to that final score.

| Agent | Factor scores (A T L C N O P I M S) | Sum | Level | Scored |
|---|---|---|---|---|
| | | | | |

## Risk register

One row per risk, per tool or agent. The defaults below apply to most agentic work; keep, adjust or close them.

| Risk | Where | Likelihood | Impact | Control | Owner (role) | Review |
|---|---|---|---|---|---|---|
| Prompt injection: content steers an agent (OWASP LLM01:2025) | Agents that read web, email or documents | | | S4; agents act only within their profile | Agent owner | Quarterly |
| Excessive agency: an agent can do more than the task needs (OWASP LLM06:2025) | Agentic tools | | | S3; authorization defaults; kill switch | Agent owner | Quarterly |
| Sensitive information disclosure (OWASP LLM02:2025) | All tools | | | Classification; P1; vendor due diligence | Privacy contact | Quarterly |
| Misinformation: wrong facts reach a client or the public (OWASP LLM09:2025) | Content and analysis | | | Q3; review gate | Deliverer | Quarterly |
| Automation bias: approvals become a rubber stamp | Review gate | | | H2; override rate | Agent owner | Monthly |
| Vendor change: terms, location or training change | All vendors | | | Quarterly vendor review | Access owner | Quarterly |

Likelihood and impact: low, medium or high.
