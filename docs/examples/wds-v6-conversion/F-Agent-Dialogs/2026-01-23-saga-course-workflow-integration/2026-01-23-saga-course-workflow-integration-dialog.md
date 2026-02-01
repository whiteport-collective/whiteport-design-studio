# 2026-01-23 WDS Course — New Features Integration — Capture

## Meta

| Field | Value |
|-------|-------|
| **Date** | 2026-01-23 |
| **Type** | 💾 Capture |
| **Agent** | SAGA |
| **Feature** | WDS Course New Features Integration |
| **Specification** | N/A — Course content update |
| **Status** | Not Started |

---

## Purpose

Integrate recently added WDS features into the course materials:
1. Agent Dialog Workflow
2. Page Specification Open Questions (Audit)
3. Eira Visual Design Agent integration

---

## Captured Thoughts

### Feature 1: Agent Dialog Workflow

**Location:** `src/workflows/9-agent-dialogs/`

**Key concepts to teach:**
- **Bridge concept** — Dialogs connect specifications to development
- **Single Source of Truth** — Specs are authoritative, dialogs link to them
- **Object ID Implementation Maps** — Step files map Object IDs to spec line numbers
- **Dialog types** — Prototype Implementation, Bug Fix, Design Exploration, Capture, Generic

**Key files:**
- `workflow.md` — Main workflow documentation
- `templates/dialog.template.md` — Generic dialog template
- `templates/step.template.md` — Step file template
- `templates/dialog-types/` — Type-specific templates

---

### Feature 2: Page Specification Open Questions (Audit)

**Location:** `src/workflows/4-ux-design/` (page specification templates)

**Key concepts to teach:**
- **Open Questions section** — Every page spec should track unresolved questions
- **Question status tracking** — 🔴 Open | 🟡 In Discussion | 🟢 Resolved
- **Auto-population** — Agent instructions to identify gaps during spec creation

**Key files:**
- `open-questions.instructions.md` — Instructions for agents to auto-populate questions
- Page specification templates with Open Questions section

**Example from Dog Week:**
```markdown
## Open Questions

| # | Question | Context | Status |
|---|----------|---------|--------|
| 1 | What happens if network fails during booking? | Error handling | 🔴 Open |
| 2 | Should "Cancel booking" show confirmation? | UX decision | 🔴 Open |
```

---

### Feature 3: Eira Visual Design Agent

**Location:** Check existing Eira dialog in F-Agent-Dialogs

**Key concepts to teach:**
- Visual design agent persona
- Design exploration workflow
- Integration with Freya (UX) workflow

---

### Why These Matter

- **Agent Dialogs**: Critical for bridging spec → code without losing traceability
- **Open Questions**: Prevents shipping specs with unresolved decisions
- **Eira Integration**: Completes the design agent ecosystem

### Rough Approach

1. Create new learn-wds module: "Working with Agent Dialogs"
2. Update page specification lessons to include Open Questions
3. Add Eira to agent personas documentation
4. Create hands-on exercises for each feature

### Notes

- Dog Week project has real examples of all three features
- The "bridge diagram" is a powerful teaching visual
- Emphasize "Link, Don't Duplicate" as a core principle

---

## Context for Next Agent

### Current Thinking

These three features represent significant additions to the WDS methodology:

1. **Agent Dialogs** — Mature enough to teach. Key insight: dialogs are a **navigation layer** between specs and code.
2. **Open Questions** — Simple but powerful. Ensures specs don't ship with unresolved decisions.
3. **Eira** — Completes the design agent ecosystem (Freya for UX, Eira for Visual).

### Open Questions

- Which learn-wds module should Agent Dialogs go in? (New module or extend existing?)
- Should Open Questions be part of the page specification lesson or standalone?
- Is Eira documented enough to add to the course, or needs more definition first?
- Should we create a dedicated example project showcasing all three features?

### Concerns

- Learners might still try to copy spec content into step files
- The line number references (L149-L158) in Object ID maps may feel tedious
- Open Questions might be seen as "extra work" rather than essential

### Suggestions

- Use Dog Week as the running example — it has all three features in action
- Create a "before/after" showing spec duplication vs. linking
- Include the bridge diagram in course materials — it's a powerful visual
- Show how Open Questions prevented shipping a broken feature

---

## When I Return

1. Review all three feature locations and documentation
2. Check existing learn-wds modules for best placement
3. Draft course content outline for each feature
4. Create hands-on exercises
5. Identify any gaps in feature documentation that need filling first

---

## References

| Feature | Location | Example |
|---------|----------|---------|
| Agent Dialogs | `src/workflows/9-agent-dialogs/` | Dog Week booking-details-overlay |
| Open Questions | Page spec templates | Dog Week 3.2-Booking-Details.md |
| Eira Integration | F-Agent-Dialogs | 2026-01-04-eira-visual-design-integration.md |

---

_Capture Agent Dialog — to be expanded later_
