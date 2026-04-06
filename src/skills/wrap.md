# /wrap — Session Wrap Skill

**Invocation:** `/wrap`
**Works for:** any agent (saga, freya, mimir, idun)

---

## Purpose

Saves the current session state to a file in the project repo so the next session can resume exactly where this one left off — no re-scanning, no re-discovering the obvious.

State is stored locally by default and ignored by git. The user can opt in to sharing it via git with one command.

---

## Behavior When Invoked

### 1. Detect Active Agent

Identify which agent is currently active from the agent's own persona and identity. The state file will be named after that agent (e.g., `_bmad/_state/saga.md`, `_bmad/_state/freya.md`).

### 2. Conversational Wrap

Ask the following four questions **one at a time**, waiting for the answer before asking the next. Keep it conversational — this is a closing conversation, not a form.

**Question 1:**
```
What were you working on?
```
(Prompt if needed: which phase, which artifact, where in the process)

**Question 2:**
```
Any open questions or blockers?
```
(Prompt if needed: things that need answers before we can move forward, decisions that are pending, external dependencies)

**Question 3:**
```
What's the very first thing to do next session?
```
(This needs to be specific enough to act on immediately — not "continue the brief", but "finish the competitive landscape section and draft the positioning statement")

**Question 4:**
```
Any context I'd lose if we started fresh?
```
(Prompt if needed: key decisions made, constraints discovered, things the user explained that aren't written down anywhere, approaches ruled out and why)

### 3. Write State File (Primary)

Write `_bmad/_state/[agent].md` in the current project repo. Overwrite if it already exists.

Use this exact format:

```markdown
# [Agent] — Session State
**Repo:** [repo-folder-name]
**Wrapped:** [YYYY-MM-DD]

## Where I Left Off
[Answer from Question 1]

## Open Questions
[Answer from Question 2 — or "None" if no blockers]

## Next Action
[Answer from Question 3 — specific enough to act on immediately]

## Context
[Answer from Question 4 — key decisions, constraints, anything needed to not re-discover the obvious]
```

### 4. Push to Agent Space (if available)

If Agent Space is configured, do two things in this order. If any step fails, log the error and continue — local state file is already saved.

**4a. Push design-process folder**

Scan the project for a `design-process/` folder (or equivalent WDS artifact folder). Push all `.md` files to Agent Space via `repo-files`:

```bash
curl -X POST "{BASE_URL}/functions/v1/repo-files" \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "put-batch",
    "project": "[repo-folder-name]",
    "files": [
      { "path": "design-process/A-Product-Brief/product-brief.md", "content": "..." },
      ...
    ]
  }'
```

**4b. Update presence with session state**

```
POST https://uztngidbpduyodrabokm.supabase.co/functions/v1/agent-messages
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV6dG5naWRicGR1eW9kcmFib2ttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI1MTc3ODksImV4cCI6MjA4ODA5Mzc4OX0.FNnTd5p9Qj3WeD0DxQORmNf2jgaVSZ6FU1EGy0W7MRo

{
  "action": "wrap",
  "agent_id": "[agent]",
  "repo": "[repo-folder-name]",
  "last_status_report": "[full state file content]",
  "working_on": "[Next Action — one line]"
}
```

**4c. Send handover message**

Send a directed message to the same agent so the next session picks it up via `check`:

```
POST https://uztngidbpduyodrabokm.supabase.co/functions/v1/agent-messages
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV6dG5naWRicGR1eW9kcmFib2ttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI1MTc3ODksImV4cCI6MjA4ODA5Mzc4OX0.FNnTd5p9Qj3WeD0DxQORmNf2jgaVSZ6FU1EGy0W7MRo

{
  "action": "send",
  "from_agent": "[agent]",
  "target_agent": "[agent]",
  "message_type": "handoff",
  "project": "[repo-folder-name]",
  "content": "[full state file content]"
}
```

This is the handover the next session finds at boot via `{"action":"check"}`. The format must include a `Next:` line so the agent can mirror it back and wait for confirmation before starting.

### 5. Confirm

Print:
```
State saved to `_bmad/_state/[agent].md`

To preserve across sessions: git add -f _bmad/_state/[agent].md && git push
```

---

## Notes

- The `_bmad/_state/` folder is gitignored by default. The user must explicitly opt in with `git add -f` to share state across machines or with collaborators.
- Local state file is always written first — Agent Space sync is optional and non-blocking.
- If the agent can't determine the current project repo, ask the user to confirm which project they're in before writing.
- Do not add a summary or closing remarks after the confirmation — the wrap is complete.

### 5. Output the handoff token

Parse the handoff ID from the `Handoff posted: {id}` line printed by the script. Take only the **first 6 characters** of the UUID. Output this code block so the user can copy it for the next session:

```
/[agent] [6chars]
```

Replace `[agent]` with the base agent name (saga/freya/idun/mimir) and `[6chars]` with the first 6 characters of the UUID (e.g. `319e3c` from `319e3c56-5adf-4864-80a2-3113feb32041`).

The user copies this and pastes as their first message in the next session. The agent detects the ID and loads the handover directly — no message triage, no scanning.
