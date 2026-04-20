# /start — Session Resume Skill

**Invocation:** `/start` (also called automatically from agent activation files)
**Works for:** any agent (saga, freya, mimir)

---

## Purpose

Detects whether a previous session was saved for the active agent and offers to resume it. If no state file exists, proceeds silently with the normal activation sequence.

---

## Behavior When Invoked

### 1. Detect Active Agent

Identify which agent is currently active. Look for `progress/[agent].md` in the current project repo.

### 2. Load State

Check for `progress/[agent].md` in the project root. This is the authoritative source.

**Fallback chain:** `progress/[agent].md` → fresh start

### 3. If State Found

Parse the state file for:
- "Where I Left Off" / Context section
- "Next Action" / Next section — extract MODEL prefix if present (MODEL:Sonnet or MODEL:Opus)
- "Plan" / Milestones section — extract milestone list if present

**Display:**

```
⏸ Previous session found ([date from Wrapped field])

Where I left off: [content from Context/Where I Left Off section]
Next action:      [Next — strip MODEL prefix, show as plain task]
Model needed:     [Sonnet | Opus — from MODEL prefix, or inferred from task type]

[If milestones present:]
── Session Plan ──────────────────────────────
[DONE] Milestone 1 — description
[CURRENT] Milestone 2 — description (~N sessions)
[ ] Milestone 3 — description (~N sessions)
──────────────────────────────────────────────

Resume where we left off, or start fresh?
```

Wait for the user's response.

**Model inference (if no MODEL prefix in Next):**
Model selection = task type × complexity × stakes:
- Any code, build, deploy, implement → Opus
- High-stakes work (production systems, financial data, billing, compliance) → Opus regardless of task type
- Long or complex multi-step tasks where a mistake is costly → Opus
- Moderate complexity: strategy, spec, dialog, UX, config, analysis → Sonnet
- Simple, low-stakes, short → Haiku
- Default to the lightest model that fits. Escalate only when stakes or complexity genuinely justify it — not as a precaution

**If resume:**
- Read the full state file, including the Context and Open Questions sections
- Jump straight to the Next Action — no scanning, no re-introduction, no status report
- Treat the context as already established — don't re-explain what was already known

**If fresh:**
- Proceed with the normal activation sequence for this agent
- Do not delete the state file (the user may want to refer back to it)

### 4. If Nothing Found

Proceed with the normal activation sequence.

**If the user describes a multi-session task at the start of a fresh session:**

Offer to break it into milestones before diving in:

```
This looks like multi-session work. Want me to map it into milestones first?
(Adds ~2 min upfront, saves context thrashing later.)
```

If yes: produce a milestone plan before starting work:
```
── Session Plan ──────────────────────────────
[ ] Milestone 1 — description (~1 session) — MODEL:Sonnet
[ ] Milestone 2 — description (~1 session) — MODEL:Opus
[ ] Milestone 3 — description (~2 sessions) — MODEL:Opus
──────────────────────────────────────────────
Starting with Milestone 1.
```

If no: proceed directly. Do not mention milestones again unless the user brings it up.

If the work appears to be a single session (clear, bounded task): do not ask. Proceed directly.

Do not mention /start or the absence of a state file.

---

## Notes

- The state file is written by `/wrap`. If no `/wrap` was run at the end of the previous session, there will be no file to find.
- The state file lives at `progress/[agent].md` relative to the project root.
- On resume, prioritize getting back to work quickly. The user already knows the context — they don't need a recap beyond what's shown in the summary.
- MODEL prefix in Next is set by `/wrap`. Selection = task type × complexity × stakes. Haiku = simple/low-stakes. Sonnet = strategy/dialog/spec/UX. Opus = all code, high-stakes work, or complex long-running tasks. Never guess wrong — surface the recommendation and let the user confirm.
