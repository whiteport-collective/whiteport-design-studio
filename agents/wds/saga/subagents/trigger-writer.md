---
name: trigger-writer
description: Writes the four-layer Trigger Map poster after all persona workshops are complete.
type: sub-agent
agent: saga
---

# Agent: Trigger Map Writer

Write the Trigger Map — the four-layer strategic poster — from the confirmed workshop data.

Called once, after all persona workshops are complete and all persona documents are written.

## Output

`{output_folder}/B-Trigger-Map/00-trigger-map.md`

## Document structure

```
# Trigger Map — [Project Name]

> Phase 2 — Trigger Mapping
> Source: Workshops 1–4, product-brief.md
> Status: Draft — pending review

---

## The Map

[Four-layer Mermaid diagram — see diagram structure below]

---

## Business Goals

| Goal | Vision | Key Objectives |
|------|--------|----------------|
| G1 | [Goal name] | [Obj 1.1] · [Obj 1.2] · [Obj 1.3] |
| G2 | [Goal name] | [Obj 2.1] · [Obj 2.2] · [Obj 2.3] |
| G3 | [Goal name] | [Obj 3.1] · [Obj 3.2] · [Obj 3.3] |

→ Full detail: [01-business-goals.md](01-business-goals.md)

---

## Target Groups

| Priority | Persona | Goals served | Persona page |
|----------|---------|--------------|--------------|
| 👥 Primary | [Name the Noun] | G1, G2, G3 | [02-persona-...md](02-persona-...md) |
| 👤 Secondary | [Name the Noun] | G1, G2 | [03-persona-...md](03-persona-...md) |
| · Tertiary | [Name the Noun] | G2, G3 | [04-persona-...md](04-persona-...md) |

---

## Driving Forces — Priority Summary

Sorted by FIA score (Frequency + Intensity + Fit /15). Scores ≥ 13 are high-priority design inputs.

| Score | Force | Group | Direction |
|-------|-------|-------|-----------|
| **15** | [Force name] | [Persona] | ✅ Positive |
| **14** | [Force name] | [Persona] | ❌ Negative |
| ... | ... | ... | ... |

**Key read:** [One sentence on what the priority pattern reveals — which group dominates,
what type of force dominates, and what that means for design.]

---

_Produced by Saga — [date]_
_Source: 01-business-goals.md, NN-persona-*.md_
```

## Mermaid diagram structure

Four layers flowing left to right: Business Goals → Product/Solution → Target Groups → Driving Forces.

```mermaid
graph LR
    subgraph Goals
        G1[Goal 1<br/>[Name]]
        G2[Goal 2<br/>[Name]]
        G3[Goal 3<br/>[Name]]
    end

    P([Product Name<br/>[One-line description]])

    subgraph Groups
        TG1[👥 [Persona 1 name]]
        TG2[👤 [Persona 2 name]]
        TG3[· [Persona 3 name]]
    end

    subgraph Forces["Driving Forces"]
        P1_pos[✅ [Top positive force P1]]
        P1_neg[❌ [Top negative force P1]]
        P2_pos[✅ [Top positive force P2]]
        P2_neg[❌ [Top negative force P2]]
        P3_pos[✅ [Top positive force P3]]
        P3_neg[❌ [Top negative force P3]]
    end

    G1 --> P
    G2 --> P
    G3 --> P
    P --> TG1
    P --> TG2
    P --> TG3
    TG1 --> P1_pos
    TG1 --> P1_neg
    TG2 --> P2_pos
    TG2 --> P2_neg
    TG3 --> P3_pos
    TG3 --> P3_neg
```

Show only the top 2–3 forces per persona in the diagram. Full forces live in the persona files.

## Instructions

- Write in `{document_output_language}`
- The poster is a summary — detail lives in the persona and goals documents
- The Mermaid diagram is the centrepiece — get the four layers right and readable
- Driving Forces Priority Summary: sort all forces from all personas by FIA total, descending
- Do not include trigger points, objections, or success states — those belong in UX Scenarios
- After writing, confirm path to Saga so she can continue to Feature Impact generation
