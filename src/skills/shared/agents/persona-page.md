# Agent: Persona Page

Generate a visual persona page for one archetype from the Trigger Map.

Persona pages are reference documents — used by Freya when designing and by the team throughout the project. One page per archetype.

## Input

From the persona file (`NN-persona-*.md`) for this archetype:
- Name (alliterative, e.g., Harriet the Hairdresser)
- Profile: background, psychological profile, internal emotional state
- Driving forces: positive (what they move toward) and negative (what they move away from), WHAT + WHY + WHEN pattern, FIA scores
- Usage context: discovery path, emotional state on arrival, behavior pattern, decision criteria
- Business goal connections

From the Product Brief:
- Product name and concept (for context)

## Output

`{output_folder}/A-Product-Brief/personas/[archetype-slug].md`

## Structure

```
# [Archetype Name]
*[One-line character description — role, context, essence]*

---

## Who They Are
[2-3 sentences painting a vivid picture of this person's daily reality.
Concrete and specific — not "busy professional" but "runs a two-person salon,
answers her own phone, and hasn't taken a full week off in three years."]

## What Drives Them

**Toward** (positive forces, highest FIA score first):
→ **[Force name]:** [WHAT + WHY + WHEN — one sentence]
→ **[Force name]:** [WHAT + WHY + WHEN]

**Away from** (negative forces, highest FIA score first):
← **[Force name]:** [WHAT + WHY + WHEN — one sentence]
← **[Force name]:** [WHAT + WHY + WHEN]

## When They Show Up
[How they discover and arrive at the product — written as 2–3 vivid scenes from their Usage Context, not bullet points]

*"[Scene 1 — the discovery moment and emotional state on arrival]"*
*"[Scene 2 — a different context or usage moment]"*

## What Makes Them Hesitate
[Derived from top negative driving forces — the real barriers, honest and specific, not generic]

## What Winning Looks Like
[What achieving their top positive driving force actually looks like. Concrete: what they do, say, feel. Not a generic success state.]

---
*Derived from Trigger Map — [date]*
```

## Instructions

- Write in `{document_output_language}`
- The "Who They Are" section should read like a person, not a market segment — concrete and specific
- "When They Show Up" scenes should be vivid: the exact moment, the context, what they feel — derived from Usage Context discovery path and emotional state
- "What Makes Them Hesitate" must come from negative driving forces — not invented objections
- "What Winning Looks Like" must come from the top positive driving force — not a generic success state
- Keep the whole page readable in 90 seconds
- After writing, report path to the calling agent
