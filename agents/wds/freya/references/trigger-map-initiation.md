---
name: trigger-map-initiation
description: How to read a completed Trigger Map and set up UX Scenarios — persona extraction, scenario scoping, and mode selection.
---

# Trigger Map Initiation

Loaded when starting UX Scenarios from a completed Trigger Map.

---

## What the Trigger Map gives you

The Trigger Map is four layers, read left to right:

1. **Business Goals** — what the business is trying to achieve (vision + SMART objectives)
2. **Product** — the solution connecting goals to users
3. **Target Groups** — prioritized personas (primary 👥, secondary 👤, tertiary)
4. **Driving Forces** — per persona: positive forces (what they move toward) and negative forces (what they move away from), WHAT + WHY + WHEN, FIA scored

Each persona also has a dedicated file (`NN-persona-*.md`) with:
- **Psychological Profile** — how they think, what they value
- **Internal State** — their emotional relationship to the problem
- **Usage Context** — how they find the product, emotional state on arrival, behavior pattern, decision criteria
- **Business Goal Connections** — which goals this persona serves

Read `B-Trigger-Map/00-trigger-map.md` for the overview, then each persona file for the depth needed to write scenarios.

---

## From Trigger Map to Scenarios

One scenario per persona — each scenario follows that archetype through a complete flow.

**Entry point** — from the persona's Usage Context: their discovery path (how they find the product)
**Emotional state** — from Usage Context: what they feel when they arrive
**Goal** — the persona's primary positive driving force: the outcome they are moving toward
**End state** — when the persona achieves that goal, the scenario is complete

For each persona, extract before starting:
- Archetype name and priority
- Discovery path (how they find the product)
- Emotional state on arrival
- Primary positive driving force (the scenario's goal)
- Business goal connections (what the scenario demonstrates for the business)

---

## Mode selection

| Product scale | Mode | Behaviour |
|---|---|---|
| < 20 pages | Dream | Generate all scenario outlines up front, present for confirmation |
| 20–100 pages | Suggest | Propose the scenario list, then walk through each conversationally |
| 100+ pages | Dialog | Scope first — one scenario at a time, no assumptions |

Do not announce or explain the mode to the user. Just run it.
Switch mode only if the user explicitly asks.

---

## Opening the conversation

Present the scenario plan before starting:

"I've read the brief and trigger map. Here's what I'm thinking:

[Site/app type] — estimated [N] pages
[N] scenarios, one for each archetype:
1. [Name the Noun] — [Core goal from positive driving force] — entry: [discovery path]
2. ...

I'll walk through these with you one at a time. Does this feel right?"

Wait for confirmation before starting the first walkthrough.
