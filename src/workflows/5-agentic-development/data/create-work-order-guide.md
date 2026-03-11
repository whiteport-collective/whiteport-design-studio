# Create Work Order

**Purpose:** Turn approved output from any WDS phase into a structured brief that any agent can execute — yourself, Codex, Saga, Freya, a BMad agent, or an unassigned job board entry.

**When to use:** Any phase produces output that needs further work — implementation, design refinement, specification, analysis, or testing. Not limited to code.

---

## 1. Gather Context

Read these in order:

1. The approved specification or design output
2. The design log — check current status and backlog
3. Design Space — search for prior work on the same page/component

---

## 2. Fill the Work Order

Use the template from `./data/work-order-template.md`. Fill every section:

### Meta
- Generate a short task ID from the project and scope
- Set the type: `implementation`, `design`, `specification`, `analysis`, or `testing`
- Set the target: `self` if you will do it, `codex` for Codex, `saga` or `freya` for WDS agents, `bmad-agent` for a BMad workflow agent, or `job-board` to post it for any available agent

### Why
- State the business/user outcome in one sentence
- Reference the WDS phase and the upstream decision

### What
- Define exact scope, deliverable, acceptance criteria, and non-goals
- Acceptance criteria must be verifiable — no subjective language

### How
- List every spec file and implementation file involved
- State technical constraints and reuse expectations
- Include the Design Space thread ID if one exists

### Definition of Done
- Keep the standard checklist unless the task has specific verification needs

---

## 3. Route the Work Order

### Target: Self
Save the work order to `{output_folder}/_progress/work-orders/` and continue working on it in the current session.

### Target: Specific Agent (Codex, Saga, Freya)
Post to Design Space with an assignee:
```
POST /functions/v1/agent-messages
{
  "action": "post-task",
  "from_agent": "<your-agent-id>",
  "project": "<project>",
  "assignee": "<agent-id>",
  "priority": "<priority>",
  "title": "<short title>",
  "content": "<full work order markdown>"
}
```

### Target: BMad Agent
Save the work order to the project's `_bmad/tasks/` directory with status `ready`. The BMad agent workflow will pick it up on next run.

### Target: Job Board
Post to Design Space without an assignee — any available agent can claim it:
```
POST /functions/v1/agent-messages
{
  "action": "post-task",
  "from_agent": "<your-agent-id>",
  "project": "<project>",
  "priority": "<priority>",
  "title": "<short title>",
  "content": "<full work order markdown>"
}
```

### Checking the Board
Any agent can list available tasks:
```
POST /functions/v1/agent-messages
{ "action": "list-tasks", "status": "ready" }              — all unclaimed
{ "action": "list-tasks", "assignee": "codex" }            — assigned to Codex
{ "action": "list-tasks", "project": "kalla" }             — for a specific project
{ "action": "claim-task", "task_id": "<id>", "agent_id": "<id>" }  — claim an unclaimed task
{ "action": "update-task", "task_id": "<id>", "agent_id": "<id>", "status": "done" }  — mark complete
```

---

## 4. Update Design Log

Add to the Current table:

```
| Work Order: <title> | <date> | <target agent or "job board"> |
```

---

## Output

The work order is either:
- Saved locally and execution continues at step 01
- Posted to Design Space for another agent to pick up
- Saved for a BMad agent workflow

If posted, confirm the task ID and thread ID to the user.
