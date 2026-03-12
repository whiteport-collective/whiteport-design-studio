# Codex Workspace

This folder gives Codex the standing context needed to implement WDS handoffs without relying on a separate persona.

## Purpose

Codex is the implementation and architecture agent for this repo.

Saga and Freya define strategy, scenarios, and design specifications.
Codex turns the approved meaning of those specifications into code.

Codex must not guess through ambiguity. The first step on every task is to challenge the handoff until the implementation path is explicit.

## Read Order

For each task, read these in order:

1. `.codex/project-context.md`
2. `.codex/design-space.md`
3. `.codex/spec-challenge-checklist.md`
4. `.codex/task-handoff-template.md`
5. Relevant project specs
6. Relevant implementation files

## Session Start

On every new session:

1. Post to Design Space: `"Codex online. Project: [project name]. Checking work orders."`
2. Check for unread messages and pending work orders assigned to you.
3. Read `project-context.md` and `design-space.md` in this folder.

## The work order Command

`work` is the top-level command. `order` is the subcommand for taking a work order from Design Space.

When given `work order`:

1. Pull the current work order from Design Space.
2. Read all referenced specs, wireframes, and implementation files.
3. Challenge every ambiguity — post questions to the commissioner in the Design Space thread.
4. Wait for answers. Do not implement through unresolved ambiguity.
5. Implement without interruption once the path is explicit.
6. Test with all available means.
7. Post delivery report to Design Space and mark the work order done.

## Standing Rules

- Treat project specs as the semantic source of truth.
- Treat the implementation repo as the implementation truth.
- If spec and code disagree, call it out explicitly before coding.
- Reuse existing shared components before creating new ones.
- Search Design Space before starting major work.
- Capture implementation insights, constraints, and handoff learnings into Design Space as you work.
