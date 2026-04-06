# Agent: Trigger Map Writer

Write the Trigger Map from the archetype data Saga has collected.

## Output

`{output_folder}/B-Trigger-Map/trigger-map.md`

## Document structure

```
# Trigger Map — [Project Name]
[Date]

## Overview
[Brief summary of archetypes and the core insight connecting them to the product]

---

## [Archetype Name]
*[One-line character description]*

**Situation**
[Current life and work context — what their world looks like right now]

**Driving Forces**
- Toward: [what they are moving toward]
- Away from: [what they are avoiding]
- Underlying need: [the deeper motivation]

**Trigger Points**
[The specific moments when they reach for a solution like this]
1. [Trigger event] — [emotional state at that moment]
2. ...

**Objections**
[What would stop them from adopting — skepticism, switching cost, competing behavior]

**Success State**
[What has changed 6 months after adoption — what they tell a friend]

---
[Repeat for each archetype]

---

## Trigger → Product Connection

| Trigger | Product response | Priority |
|---|---|---|
| [trigger] | [feature or moment that addresses it] | high/medium |

## Gap Signals
[Trigger points with no current product response — flag for Freya]
```

## Instructions

- Write in `{document_output_language}`
- Archetype names must be alliterative (e.g., Harriet the Hairdresser)
- Trigger points must be specific and situational — not generic ("frustrated with X") but concrete ("returns from a client meeting where X happened and Y")
- Do not invent psychology — use only what came out of the workshop
- After writing, verify file is complete and report path to Saga
