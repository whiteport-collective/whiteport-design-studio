# Getting Things Done (GTD)

**By:** David Allen (2001)
**Source:** "Getting Things Done: The Art of Stress-Free Productivity"

---

## Core Concept

GTD is a personal productivity methodology that helps manage commitments, information, and action. The core insight: your mind is for having ideas, not holding them. Capture everything externally, then organize and act systematically.

---

## The Five Steps

### 1. Capture
Collect everything that has your attention into a trusted system. Don't rely on memory.

### 2. Clarify
Process what you've captured:
- Is it actionable?
- What's the next action?
- What's the desired outcome?

### 3. Organize
Put things where they belong:
- Next Actions (by context)
- Projects (multi-step outcomes)
- Waiting For (delegated)
- Someday/Maybe (future ideas)
- Reference (information)

### 4. Reflect
Review your system regularly:
- Daily: Check calendar, review next actions
- Weekly: Full review of all lists, projects, commitments

### 5. Engage
Do the work with confidence, knowing your system has captured everything.

---

## The 2-Minute Rule

**If an action takes less than 2 minutes, do it immediately.**

This is one of GTD's most powerful and widely-adopted principles:

- The overhead of tracking a 2-minute task exceeds doing it
- Immediate completion clears mental clutter
- Builds momentum through quick wins
- Prevents small tasks from accumulating

### In Practice

| Situation | Action |
|-----------|--------|
| Quick email reply | Send now |
| Simple file rename | Do now |
| Brief clarification | Ask now |
| Small fix | Fix now |

### The Threshold

2 minutes is a guideline, not a strict rule. The principle is:

> **Planning overhead should not exceed task complexity.**

If documenting, categorizing, and scheduling a task takes longer than doing it — just do it.

---

## Applied in WDS Agentic Development

### Task Complexity Assessment

Before adding something to the plan, ask:

| Question | If Yes → |
|----------|----------|
| Can I fix this in < 2 minutes? | Do it now, log as sub-step |
| Does it need context I don't have? | Add to plan |
| Does it affect architecture? | Add to plan |
| Is it outside current scope? | Level 4 change request |

### Bug Fixes vs. Features

**Bugs (2-minute candidates):**
- Missing condition check
- Wrong variable name
- Off-by-one error
- Missing translation

**Features (need planning):**
- New component
- New state handling
- Architectural changes
- Multi-file refactors

### Sub-Step Pattern

When a 2-minute fix arises during planned work:

1. **Do** the fix immediately
2. **Log** it as a sub-step (e.g., 20a-1)
3. **Continue** with the main task

This maintains traceability without planning overhead.

---

## Why This Matters for AI Collaboration

Agentic development involves constant micro-decisions:
- Should I plan this?
- Should I do this now?
- Should I defer this?

The 2-minute rule provides a clear heuristic:

```
IF task_complexity < 2_minutes:
    execute_immediately()
    log_as_substep()
ELSE:
    add_to_plan()
```

This prevents:
- Analysis paralysis on trivial tasks
- Planning overhead exceeding task value
- Context switching from minor interruptions
- Accumulated technical debt from deferred tiny fixes

---

## Related Concepts

### Inbox Zero
Process everything to zero — don't leave items in limbo.

### Next Actions
Define the very next physical action for every project.

### Waiting For
Track delegated items so nothing falls through cracks.

### Weekly Review
Regular system maintenance keeps it trustworthy.

---

## Source Materials

### Book
- **"Getting Things Done: The Art of Stress-Free Productivity"** by David Allen (2001, revised 2015)

### Website
- [GettingThingsDone.com](https://gettingthingsdone.com)

### Key Articles
- "The 2-Minute Rule" — David Allen
- "GTD in 15 minutes" — Various summaries online

---

## WDS Integration Points

| WDS Context | GTD Application |
|-------------|-----------------|
| **Agentic Development** | 2-minute rule for bug fixes, sub-step logging |
| **Agent Dialogs** | Capture system for ideas (dialog files) |
| **Change Requests** | Someday/Maybe list for outside-scope items |
| **Progress Logs** | Review and reflect on completed work |
| **Session Start Protocol** | Weekly review concept (check reality vs. plan) |

---

## Quick Reference

### The 2-Minute Rule
> If it takes less than 2 minutes, do it now.

### The Core Principle
> Planning overhead should not exceed task complexity.

### Applied to Development
> Quick fixes → Do and log as sub-step
> Complex changes → Add to plan first

---

*Getting Things Done - Stress-free productivity through systematic capture and action.*
