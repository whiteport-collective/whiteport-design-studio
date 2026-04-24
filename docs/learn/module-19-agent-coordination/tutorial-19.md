# Tutorial 19: Your First Cross-Agent Session

**Hands-on guide to running a full Saga → Freya → Mimir handoff**

---

## Overview

**Time:** 20 minutes
**Prerequisites:** Modules 14, 16 complete. A project with at least one completed WDS phase.
**What you'll do:** Run a complete agent handoff chain using `_progress/` files.

---

### Step 1: Wrap Saga and Pass to Freya (5 min)

In your Saga session, after completing strategy:

**You say:**
> `/wrap freya`

**Saga writes and reports:**
```
── Handover ──────────────────────────────────
Next:    MODEL:Sonnet — Start UX Scenarios. Brief and trigger map complete.
Plan:    Design phase. 4 scenarios to cover from trigger map.
Open:    None
Learned: Client prioritizes mobile. Walker search is the core flow.
──────────────────────────────────────────────

Saved to _progress/saga.md — index updated (3 files)
→ Open a new chat and run:
/freya _progress/freya.md
```

**Check the file:**
Open `_progress/freya.md` — confirm it has Context, Next, Learned.

---

### Step 2: Freya Picks Up (5 min)

Open a new chat. Run:

```
/freya _progress/freya.md
```

**Freya reads the handoff and reports:**
```
✨ Dog Week — resuming from Saga handoff

Strategy: complete
  Product Brief     ✓
  Trigger Map       ✓

Design:
  UX Scenarios      ○ not started
  UX Design         ○ not started

Saga noted: Client prioritizes mobile. Walker search is the core flow.

Starting with UX Scenarios — 4 flows from the trigger map.
```

No re-briefing. No explaining the project. Freya starts designing.

---

### Step 3: Design Delivery (5 min)

After Freya finishes one flow, run:

```
/design-delivery owner-signup
```

**Freya delivers:**
```
── Design Delivery ───────────────────────────
PRD: _bmad-output/docs/prd.md

Delivered:
  ✓  owner-signup → 3.1 User Registration

PRD updated. Mimir handoff written to _progress/mimir.md.
─────────────────────────────────────────────
```

---

### Step 4: Mimir Picks Up (5 min)

Open a new chat. Run:

```
/mimir
```

Mimir reads `_progress/mimir.md`, opens the PRD, finds the design reference, and starts building.

**Result:** Full Saga → Freya → Mimir chain, zero context lost, no re-explanation.

---

## What You've Learned

| Mechanism | When | Command |
|-----------|------|---------|
| Wrap with handoff | End of phase | `/wrap [agent]` |
| Resume from handoff | Start of next phase | `/[agent] _progress/[agent].md` |
| Design delivery | After approving specs | `/design-delivery` |

---

## Congratulations

You've completed the WDS Course.

**What you can do now:**

- Run complete WDS projects from brief to shipped product
- Coordinate multiple agents without losing context
- Deliver specifications that coding agents can build from

**The paradigm shift is real:** the design is the specification. The specification is the product. The code is just the printout.

---

**[← Back to Module 19 Overview](module-19-overview.md)**
**[← Back to Course Overview](../00-course-overview/00-course-overview.md)**

*Part of the WDS Course: From Designer to Linchpin*
