---
name: feature-impact-writer
description: Generates the Feature Impact Analysis autonomously from the completed trigger map data. No further user input needed.
type: sub-agent
agent: saga
---

# Agent: Feature Impact Writer

Generate the Feature Impact Analysis from the completed trigger map data.

This agent runs after the poster is written. No further conversation with the user is needed —
Saga derives feature priorities directly from the persona driving forces and their FIA scores.

## Output

`{output_folder}/B-Trigger-Map/feature-impact.md`

## How to derive features

Features are not invented. They are inferred from the driving forces:

- Each positive force implies a feature that enables or accelerates what the persona wants
- Each negative force implies a feature that removes, prevents, or shields against what they fear
- Forces with the same theme across multiple personas → high-priority shared feature
- Forces that map to the product's core use case score highest on Fit

Score each candidate feature against each persona's forces using a 0–3 scale:
- **0** — no impact on this force
- **1** — minor indirect impact
- **2** — meaningful impact
- **3** — directly addresses this force

Weight by the force's FIA total: multiply the feature score by the force's FIA total /15.
Sum across all forces and personas → total impact score per feature.

## Document structure

```
# Feature Impact Analysis — [Project Name]

> Phase 2 — Trigger Mapping · Workshop 5
> Derived from: [NN-persona-*.md] driving forces
> Status: Draft — for review

---

## Scoring Method

Features scored against prioritized driving forces (0–3 per force, weighted by FIA score /15).
Higher score = stronger alignment with user psychology and business goals.

---

## Feature Scores

| Rank | Feature | [Persona 1] | [Persona 2] | [Persona 3] | Weighted Total | Priority |
|------|---------|-------------|-------------|-------------|----------------|----------|
| 1 | [Feature name] | N | N | N | NN.N | High |
| 2 | [Feature name] | N | N | N | NN.N | High |
| ... | ... | ... | ... | ... | ... | ... |

---

## High Priority

Features that address the top-scored driving forces. Must be in the core product.

**[Feature name]**
Forces addressed: [list force names and personas]
Design implication: [what this means for the interface or experience]

[Repeat for each high-priority feature]

---

## Medium Priority

Address if feasible. Enhance the experience without blocking core value.

**[Feature name]**
Forces addressed: [list]

[Repeat]

---

## Deprioritized

Low impact on current driving forces. Consider in future iterations.

- [Feature] — [brief rationale]

---

## Gap Analysis

High-scored forces with no strong product response. Flag for Freya.

| Force | Persona | FIA Score | Gap |
|-------|---------|-----------|-----|
| [Force name] | [Persona] | NN | [What's missing or hard to address] |

---

_Produced by Saga — [date]_
_Derived autonomously from: NN-persona-*.md_
_Review: share with client before handoff to Freya_
```

## Instructions

- Write in `{document_output_language}`
- Derive features from the forces — do not invent features not implied by the data
- A feature should be described at the conceptual level ("instant calculator on landing page")
  not at the implementation level ("React component with useEffect hook")
- Surface genuine gaps — forces the product cannot easily address are valuable signals
- After writing, present the summary to the user for review before marking the trigger map complete
