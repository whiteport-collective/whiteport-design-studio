# Work Order

## Meta

- **Task ID:** {{task_id}}
- **Project:** {{project_name}}
- **Created by:** {{agent_name}} ({{phase}})
- **Type:** {{implementation | design | specification | analysis | testing}}
- **Target:** {{target — self | codex | saga | freya | bmad-agent | unassigned}}
- **Priority:** {{critical | high | normal | low}}
- **Status:** ready

---

## Why

What product or user outcome should this work achieve?

> {{Business intent and user value}}

Where does this sit in the WDS flow?

> {{Phase and upstream decision that produced this task}}

---

## What

### Scope

{{Exact scope — what is being built or changed}}

### Deliverable

{{Exact deliverable — files, components, pages, features}}

### Acceptance Criteria

- [ ] {{Criterion 1}}
- [ ] {{Criterion 2}}
- [ ] {{Criterion 3}}

### Non-Goals

- {{What is explicitly out of scope}}

---

## How

### Spec Files

| File | Purpose |
|------|---------|
| {{path}} | {{what it defines}} |

### Implementation Files

| File | Purpose |
|------|---------|
| {{path}} | {{what to create or modify}} |

### Technical Constraints

- {{Stack, dependency, or architecture constraints}}

### Reuse Expectations

- {{Existing components to use or extend}}
- {{Design system tokens or patterns to follow}}

### Reporting

- **Design Space thread:** {{thread_id or "none"}}
- **Design Log update:** {{what status to set on completion}}

---

## Definition of Done

- [ ] Code changes implemented
- [ ] Build passes
- [ ] Acceptance criteria verified
- [ ] Spec drift documented
- [ ] Design Log updated
- [ ] Reusable learnings captured to Design Space

---

## Context Attachments

> Optional: paste or link relevant spec excerpts, wireframes, design tokens, or prior Design Space entries that the implementer needs.
