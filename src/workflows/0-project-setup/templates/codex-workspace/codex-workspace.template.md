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

## MCP Prerequisites

- Preferred Design Space path: `design-space-personal` MCP in Codex.
- Optional database/admin path: `supabase` MCP in Codex.
- Codex reads MCP servers from `C:/Users/marte/.codex/config.toml`.
- First-time setup instructions live in `.codex/design-space.md`.
- If MCP is unavailable in the current session, use the HTTP fallback instead of skipping Design Space.

## Session Start

On every new session:

1. Access Design Space through the best available path:
   - Use the `design-space-personal` MCP server if available.
   - If it is not installed, follow `.codex/design-space.md` first-time setup.
   - If it is unavailable in the current session, use the HTTP fallback documented in `.claude/commands/u.md` and `_bmad/wds/data/design-space-config.md`.
2. Register (`action: "register", agent_id: "codex", pronouns: "he/him", repo: "<repo-folder-name>"`) — this is your identity in Design Space.
3. Tell the human:
   > Online as **Codex-[number]**[· ⎇ repo-name if defined]
   > Also online: [Agent-Name · ⎇ repo if defined] — or "no one else"
4. Check for unread messages and pending work orders assigned to you.
5. Read `project-context.md` and `design-space.md` in this folder.

## The /work Command

`/work` is the command for taking work from Design Space and driving it through delivery.

When given `/work`:

1. Access Design Space through the best available path:
   - Use the `design-space-personal` MCP server if available.
   - If it is not installed, follow `.codex/design-space.md` first-time setup.
   - If it is unavailable in the current session, use the HTTP fallback documented in `.claude/commands/u.md` and `_bmad/wds/data/design-space-config.md`.
2. Sign in or register presence if needed.
3. Read the manifest and current Design Space context.
4. Check for unread messages addressed to `codex` or to you specifically.
5. Look for pending work orders relevant to this repo.
6. Confirm whether you should start work now based on the work order state and latest messages.
7. Read all referenced specs and implementation files.
8. Challenge every ambiguity and gap. Post questions to the commissioner in the Design Space thread.
9. Wait for answers. Do not implement through unresolved ambiguity.
10. Implement once the path is explicit.
11. Test with all available means.
12. Post delivery report to Design Space and mark the work order done.

## Standing Rules

- Treat project specs as the semantic source of truth.
- Treat the implementation repo as the implementation truth.
- If spec and code disagree, call it out explicitly before coding.
- Reuse existing shared components before creating new ones.
- Search Design Space before starting major work.
- If direct Design Space access is unavailable, use the HTTP fallback instead of skipping the Design Space step.
- Express your intentions, experiences, and plans to Design Space on an ongoing basis during the session so work can be resumed cleanly after interruption.
- Capture implementation insights, constraints, and handoff learnings into Design Space as you work.
