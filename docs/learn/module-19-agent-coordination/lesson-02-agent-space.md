# Lesson 2: Agent Space & Session Tokens

**Module 19 | Time: 10 min**

---

## Beyond the Progress Folder

The `_progress/` system handles handoffs within a project. Agent Space handles something different: resuming *your own session* in a new conversation window, with full context intact.

When you run `/wrap`, the agent:
1. Saves state to `_progress/[agent].md` — the project-level handoff
2. Publishes a session token to Agent Space — a 6-character code you can use to resume

```
── Handover ──────────────────────────────────
Next:    MODEL:Sonnet — Design the walker-profile page
Plan:    UX Design phase, 2/7 pages complete
Open:    None
Learned: None
──────────────────────────────────────────────

/saga a3f9c1
```

That last line is your resume prompt. Copy it, open a new chat, paste it. Saga finds the token in Agent Space and picks up exactly where you left off.

---

## How It Works

Agent Space is a Supabase backend. When you wrap:

1. The wrap skill writes `session-wrap.md` to the repo root
2. `wrap_publish.py` POSTs the session content to Agent Space as a notification message addressed to your agent (`saga`, `freya`, or `mimir`)
3. A 6-character token is returned from the message UUID
4. On the next session start, the agent fetches its inbox and scans for the token prefix

```
/saga a3f9c1
         └── prefix match against Agent Space inbox
             → finds the session content
             → resumes immediately
```

---

## Configuration

Agent Space credentials live in `~/.claude/wds-config.yaml`:

```yaml
agent-space:
  url: https://uztngidbpduyodrabokm.supabase.co
  anon-key: eyJhbGci...
  agents:
    saga: saga
    freya: freya
    mimir: mimir
```

The anon key is read-only — it can only fetch messages addressed to you. Safe to share, safe to commit to a team config.

**Personal install:** uses the shared WDS Agent Space. Works out of the box.

**Org install:** your admin hosts a `wds-config.yaml` with your org's own Supabase instance. Every employee's sessions go to your org's space, not the shared one.

---

## Choosing the Right Handoff Method

| Situation | Use |
|-----------|-----|
| Handing off to a different agent | `/wrap [agent]` → `_progress/[agent].md` |
| Resuming your own session in a new window | `/wrap` → Agent Space token |
| Both | `/wrap [agent]` does both simultaneously |
| Token not working | Fall back to `/saga _progress/saga.md` |

---

## Troubleshooting Tokens

**Token not found** — The most common cause is a stale session from before the Agent Space routing was fixed. Fall back to the progress file:

```
/saga _progress/saga.md
```

**Wrong inbox** — If your `wds-config.yaml` has a different `agents:` mapping than the default, the token may route to a different agent ID. Check that the agent ID in config matches what `session-start` expects.

**Agent Space down** — The wrap skill completes the progress file regardless. You always have `_progress/[agent].md` as a fallback.

---

[← Lesson 1: The `_progress/` System](lesson-01-progress-system.md) | [Tutorial 19 →](tutorial-19.md)

*Part of Module 19: Agent Coordination*
