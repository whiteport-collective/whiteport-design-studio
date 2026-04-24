# Lesson 1: The `_progress/` System

**Module 19 | Time: 10 min**

---

## Built-In Coordination

Every WDS project has a `_progress/` folder. This is where agents leave state for each other — and for their future selves.

```
_progress/
├── saga.md        ← Saga's last state
├── freya.md       ← Current handoff target for Freya
├── mimir.md       ← Set by /design-delivery when build is ready
└── project-index.md  ← What exists in this repo, updated on every wrap
```

No setup required. These files are created and updated automatically by WDS agents when you use the built-in skills.

---

## The Three Skills

### `/wrap [agent]`

Ends your session and saves state. With an optional target agent, also writes a handoff.

```
/wrap           → saves your own state to _progress/[you].md
/wrap freya     → saves your state + writes _progress/freya.md
```

The handoff contains: what was done, what's next, what was learned, any spec changes.

### `/handoff [agent]`

Passes a specific task mid-session without ending your own work. Use when the work changes character — strategy is done, design should start — but you're still in the same conversation.

```
/handoff mimir   → writes _progress/mimir.md, session continues
```

### `/start [file]`

Resumes from a handoff file. Agents call this at activation when a progress file exists.

```
/freya _progress/freya.md   → Freya reads handoff and begins immediately
```

---

## The Handoff Format

Every `_progress/` file follows the same structure:

```markdown
## Wrapped
2026-04-22 10:47

## Context
[What was done. State of artifacts. Open threads.]

## Plan
[Where we are in the project. What remains.]

## Next
MODEL:Sonnet — [Single immediately-actionable next step]

## Learned
[Non-obvious decisions, rejected paths, taste constraints]

## Spec Sync
[Any changes that diverged from written specs]
```

**The "Next" line is the most important.** It should be so specific that the receiving agent can start without asking any questions. "Continue designing" is bad. "Design the walker-profile page — specs are in D-UX-Design/walker-profile-spec.md, scenario is C-UX-Scenarios/S02-Walker-Discovery" is good.

---

## The Project Index

Every wrap also updates `_progress/project-index.md` — a running map of what exists in the repo.

```markdown
## Project Index
Updated: freya 2026-04-22 a3f9c12

## Phase Status
Strategy: complete
Design: in progress (3/7 pages)
Build: not started

## Artifacts
_bmad/wds/A-Product-Brief/product-brief.md — brief — Dog Week product strategy
_bmad/wds/B-Trigger-Map/trigger-map.md — trigger-map — User activation triggers
_bmad/wds/D-UX-Design/owner-signup.md — spec — Owner signup flow, 3 pages
```

An agent loading into a new session reads this index before anything else. It tells them what exists without searching.

---

## Complete Flow

Here's how a full Saga → Freya → Mimir handoff works in practice:

```
1. You run /saga
   Saga works through strategy phases
   
2. You run /wrap freya
   Saga saves state to _progress/saga.md
   Saga writes handoff to _progress/freya.md
   Saga prints: "→ Open a new chat and run: /freya _progress/freya.md"

3. You open a new chat, run /freya _progress/freya.md
   Freya reads the handoff
   Freya knows exactly what was decided, what to do next
   Freya starts designing immediately

4. You run /design-delivery
   Freya injects specs into PRD
   Freya writes _progress/mimir.md automatically

5. You open a new chat, run /mimir
   Mimir reads _progress/mimir.md
   Mimir builds from the spec
```

One project. Three agents. Every handoff is a file — no context lost.

---

[← Module Overview](module-19-overview.md) | [Tutorial 19 →](tutorial-19.md)

*Part of Module 19: Agent Coordination*
