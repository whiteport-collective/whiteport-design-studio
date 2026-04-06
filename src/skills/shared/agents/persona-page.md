# Agent: Persona Page

Generate a visual persona page for one archetype from the Trigger Map.

Persona pages are reference documents — used by Freya when designing and by the team throughout the project. One page per archetype.

## Input

From the Trigger Map for this archetype:
- Name (alliterative, e.g., Harriet the Hairdresser)
- Situation
- Driving forces (toward + away from + underlying need)
- Trigger points (with emotional states)
- Objections
- Success state

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
→ **Moving toward:** [aspiration]
← **Moving away from:** [fear or frustration]
◎ **Underlying need:** [the deeper human need beneath the surface motivations]

## When They Reach for This
[The specific trigger moments — written as short scenes, not bullet points]

*"[Scene 1 — describe the exact moment and what they're feeling]"*
*"[Scene 2]"*
*"[Scene 3]"*

## What Makes Them Hesitate
[The real objections — honest, not dismissive]

## What Success Looks Like
[Six months later. What has changed. What do they tell a friend.]

---
*Derived from Trigger Map — [date]*
```

## Instructions

- Write in `{document_output_language}`
- The "Who They Are" section should read like a person, not a market segment
- Trigger scenes should be vivid and specific — the reader should recognize this person
- Keep the whole page readable in 90 seconds
- After writing, report path to the calling agent
