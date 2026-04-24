# Lesson 6: Multi-Agent Sessions

**Module 14 | Time: 20 min**

---

## One Agent Is Not Enough

WDS uses two agents for a reason. Saga thinks strategically — she doesn't design. Freya designs — she doesn't write the product brief. When you need both in the same project, you're running a multi-agent workflow.

The problem: agents don't remember each other. Saga finishes the strategy, you open a new chat for Freya, and Freya starts from nothing. You paste the brief. You explain the trigger map. You repeat yourself.

This is the multi-agent coordination problem. It's solvable.

---

## How WDS Handles It: The `_progress/` Folder

WDS agents leave notes for each other in `_progress/`. When Saga finishes, she runs `/wrap saga freya` — this writes a handoff file at `_progress/freya.md` containing:

- What was decided
- What files were created
- What Freya needs to do next

When Freya starts, she runs `/freya _progress/freya.md` — she reads the handoff and picks up immediately. No re-explanation needed.

```
Saga session ends   →  /wrap saga freya  →  _progress/freya.md
Freya session starts →  /freya _progress/freya.md  →  continues
```

The same pattern repeats at every agent boundary:

```
_progress/
├── saga.md          ← Saga's own state (resume anytime)
├── freya.md         ← Handoff from Saga to Freya
└── mimir.md         ← Handoff from Freya to Mimir (written by /design-delivery)
```

---

## The Three Handoff Moments

### 1. Strategy → Design

Saga completes the Product Brief and Trigger Map. She wraps and passes to Freya:

```
/wrap freya
```

Freya opens and continues:

```
/freya _progress/freya.md
```

### 2. Design → Build

Freya finishes designing a flow and runs `/design-delivery`. This injects specs into the PRD and writes `_progress/mimir.md` automatically. Mimir picks up from there.

### 3. Mid-session handoffs

If you're deep in a session and need to switch agents, `/handoff [agent]` writes the handoff without ending your session. Use it when work changes character mid-conversation.

---

## What Good Handoffs Look Like

A good handoff answers three questions for the receiving agent:

1. **What was done?** — Specific artifacts, decisions made, state of work
2. **What matters most?** — Non-obvious constraints, taste decisions, things that were tried and rejected
3. **What's next?** — Single immediately-actionable step

A bad handoff is vague ("do the design stuff") or missing context ("see the files"). The receiving agent will either stall or start over.

WDS agents write good handoffs automatically when you use `/wrap` and `/design-delivery`. Your job is to start the next session by pointing the agent at the handoff file.

---

## Summary

| Mechanism | Scope | Setup required |
|-----------|-------|---------------|
| `/wrap [agent]` | Within project | None — built in |
| `/handoff [agent]` | Within session | None — built in |
| `/design-delivery` | Design → Build | None — built in |

---

[← Lesson 5: Git Discipline](lesson-05-git-discipline.md) | [Tutorial 14 →](tutorial-14.md)

*Part of Module 14: Agentic Development*
