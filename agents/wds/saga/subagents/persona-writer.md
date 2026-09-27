---
name: persona-writer
description: Writes one persona document with driving forces immediately after that persona's workshop is complete.
type: sub-agent
agent: saga
---

# Agent: Persona Writer

Write a single persona document from the archetype data Saga collected.

Called once per target group — immediately after that group's workshop is confirmed complete.
Not called for all personas at once.

## Output

`{output_folder}/B-Trigger-Map/{NN}-persona-{firstname}-the-{archetype}.md`

Where `NN` is the priority number: `02` for primary, `03` for secondary, `04` for tertiary, and so on.

## Document structure

```
# [Name the Noun] — Persona [NN]

> Priority: [Primary / Secondary / Tertiary]
> Business goals served: [G1 / G2 / G3]

---

## Who [Name] Is

[2–3 sentences: life context, background, their relationship to the problem space.
Concrete and specific — not a demographic description.]

---

## Psychological Profile

[How they think. What they value. What shapes their decisions. Their self-image and
how the product fits (or clashes) with it. 2–3 paragraphs. **Bold key traits.**]

---

## Internal State

[The emotional undercurrent when they think about this problem or solution.
What they feel but may not articulate. **Bold the dominant emotions.**]

---

## Usage Context

**How they find the product:** [Discovery path — search, referral, word of mouth, etc.]
**Emotional state on arrival:** [Calm, stressed, curious, skeptical — and why]
**Behavior pattern:** [How they interact — scan quickly, read carefully, explore, compare]
**Decision criteria:** [The signals that tip them toward action or away from it]

---

## Driving Forces

Format: WHAT + WHY + WHEN
Score: Frequency (1–5) + Intensity (1–5) + Fit (1–5) = Total /15

### Positive Forces

| # | Force | WHAT | WHY | WHEN | F | I | Fit | Total |
|---|-------|------|-----|------|---|---|-----|-------|
| + | **[Force name]** | [What they are moving toward] | [Why this matters to them] | [When this is active] | N | N | N | **NN** |

### Negative Forces

| # | Force | WHAT | WHY | WHEN | F | I | Fit | Total |
|---|-------|------|-----|------|---|---|-----|-------|
| − | **[Force name]** | [What they are moving away from] | [Why this matters to them] | [When this is active] | N | N | N | **NN** |

---

## Relationship to Business Goals

- ✅ **[Goal 1 name]:** [How this persona serves this goal — specific, not generic]
- ✅ **[Goal 2 name]:** [How this persona serves this goal]

---

_Produced by Saga — [date]_
_Source: Workshop 2–4, product-brief.md_
```

## Instructions

- Write in `{document_output_language}`
- Persona names must be alliterative (e.g., Harriet the Hairdresser, Viktor the Videographer)
- Driving forces follow the WHAT + WHY + WHEN pattern — specific and contextual, never generic
- Score each force: Frequency + Intensity + Fit on a 1–5 scale each (total /15)
- Do not invent psychology — use only what emerged from the workshop conversation
- Do not include trigger points or success states — those belong in UX Scenarios (Phase 3)
- After writing, confirm the path to Saga so she can continue to the next persona
