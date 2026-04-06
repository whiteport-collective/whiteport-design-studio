---
name: feedback
description: Feedback collection and fix planning. Use when the user says "I want to give feedback", "I have feedback", or /feedback. Listens to reported issues, investigates the repo, builds a fix plan, then spawns Mimir to implement everything at once.
argument-hint: "[optional: brief description of the issue]"
---

# Feedback — Issue Collection & Fix Planning

## Overview

This skill turns user feedback sessions into structured fix plans ready for implementation. It listens, investigates, plans — then delegates all fixes to Mimir in one go.

Available to: **Freya**, **Saga**, **any WDS agent**

---

## On Activation

Respond immediately with:

```
I'm listening.
```

Nothing else. Wait for the user to start describing issues.

---

## Feedback Loop

Repeat this cycle for each issue the user reports:

### 1. Receive

Let the user describe the issue in their own words. Do not interrupt.

### 2. Investigate

Actively look for the issue in the repo:
- Read the relevant files (components, routes, specs)
- Check git log for recent changes to affected areas
- Try to understand exactly what causes the problem
- Note the file path and line number(s)

### 3. Assess

State clearly what you found:
- **Confirmed** — you found the bug/issue and understand why it happens
- **Likely** — probable cause based on code review, not 100% certain
- **Can't reproduce** — code looks correct, ask a follow-up question

### 4. Clarify (if needed)

Ask one focused question at a time. Examples:
- "Does this happen only on mobile or desktop too?"
- "Which step in the flow triggers it?"
- "Is this a visual bug or does it affect functionality?"

Do NOT ask for information you can find yourself in the code.

### 5. Log

Internally track each confirmed issue with:
- Short title
- File(s) affected
- Root cause
- Proposed fix

---

## Continuing

After each issue is assessed, say:

```
Got it. Anything else?
```

Keep listening until the user signals they're done (e.g. "that's all", "det är allt", "go ahead and fix", "kör").

---

## When the User Is Done

1. **Present the fix plan** — a numbered list of all confirmed issues with:
   - What's broken
   - What file/component
   - What the fix is

2. **Ask for confirmation:**
   ```
   Should I send this to Mimir to implement?
   ```

3. **On confirmation** — spawn a Mimir sub-agent with the complete fix plan as a single work order. Include:
   - All confirmed issues
   - File paths and line numbers
   - Exact fixes or clear instructions per issue
   - Context about the overall flow/feature so Mimir can make good judgment calls

---

## Tone

Stay in character as your active agent (Freya or Saga). Keep responses short during the listening phase — you're a detective, not a commentator. Save the summary for the end.

---

## Mimir Handoff Template

When spawning Mimir, use this format:

```
# Fix Plan — [date]

## Context
[Brief description of the feature/flow being fixed]

## Issues

### 1. [Issue title]
- **File:** `path/to/file.tsx:line`
- **Problem:** [what's wrong]
- **Fix:** [what to change]

### 2. [Issue title]
...

## Notes
[Any shared context, constraints, or edge cases Mimir should know]
```
