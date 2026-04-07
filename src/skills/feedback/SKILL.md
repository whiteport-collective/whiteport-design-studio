---
name: feedback
description: Live feedback rounds. User browses and reports issues in natural language, agent captures structured FB-XX items, triages severity, fixes quick items inline, delegates bigger fixes to parallel sub-agents. Use when the user says "I want to give feedback", "I have feedback", "let's review", or /feedback.
argument-hint: "[optional: area to focus on, e.g. 'checkout', 'home page']"
---

# Feedback — Live Review & Fix Rounds

## Overview

This skill turns live browsing sessions into structured fix plans with tracked outcomes. The user speaks freely while the agent does all the structuring, investigating, and fixing.

Available to: **Freya**, **Saga**, **any WDS agent**

---

## On Activation

1. Create a feedback file: `design-process/E-Development/WO-{N}-{NN}-{area}-feedback.md`
   - Link it to the nearest relevant WO, or create a standalone one
   - Initialize with a header, date, reporter, and empty summary table

2. Respond:

```
I'm listening. Browsing or reporting?
```

If the dev server isn't running, start it. If the user is browsing live, follow along with screenshots.

---

## Feedback Loop

Repeat for each issue the user reports:

### 1. Receive

Let the user describe the issue in their own words. Any language. Do not interrupt. Do not ask for clarification you can find yourself in the code.

### 2. Investigate

Actively look for the issue:
- Read the relevant files — note file path and line number(s)
- Check git log for recent changes to affected areas
- If a browser is available, reproduce visually with screenshot
- Understand the root cause, not just the symptom

### 3. Log

Add the issue to the feedback file immediately as `FB-{XX}`:

```markdown
## FB-XX: [Short title]

**Observed:** [What the user described]

**Root cause:** [What you found in the code]

**File:** `path/to/file.tsx:line`

**Fix:** [Concrete change needed]

**Severity:** Low | Medium | High
**Assigned to:** [Self | Mimir | Codex | Deferred]
```

Update the summary table at the bottom of the file.

### 4. Acknowledge

Keep it short:

```
Noted — FB-XX. Next?
```

Do NOT summarize what they just said back to them. Do NOT give lengthy explanations unless asked.

---

## Triage Rules

Assign each issue based on complexity:

| Complexity | Action |
|-----------|--------|
| One-line CSS/label change | Fix inline yourself, mark Fixed |
| Small component change (< 20 lines) | Fix inline yourself, mark Fixed |
| Architectural change or multi-file | Assign to sub-agent (Mimir/Codex) |
| Needs design decision or spec update | Mark Open, discuss with user |
| Not needed now | Mark Deferred with reason |

---

## When the User Is Done

### 1. Commit baseline

Always commit all current changes before spawning fix agents:

```
git add [changed files]
git commit -m "docs: capture feedback round FB-01 through FB-XX"
```

### 2. Fix quick items

Fix all Low-severity inline items yourself first. Commit them.

### 3. Spawn parallel agents

Group remaining issues by file ownership — never let two agents edit the same file. Spawn them in parallel using background agents:

```
Agent 1: FB-03, FB-07 (both in shipping/index.tsx)
Agent 2: FB-05, FB-11 (both in payment/index.tsx)
Agent 3: FB-09 (architectural — checkout-panel-content)
```

Each agent prompt must include:
- The exact file path(s)
- What to change and why
- Instruction to read the file first
- No other files to touch

### 4. Evaluate results

As each agent completes:
- Check the change makes sense
- Run TypeScript check on affected files
- Update FB status in the feedback file

### 5. Browser verify

After all agents complete:
- Reload the site
- Walk through the affected flow
- Take screenshots of fixed items
- Note any regressions

### 6. Final commit

```
git commit -m "fix: resolve N feedback points (FB-XX through FB-YY)"
```

---

## Feedback File Format

```markdown
# WO-{N}-{NN} — {Area} Feedback

**Status:** Open | Complete
**Reporter:** [name]
**Date:** [YYYY-MM-DD]
**Context:** [what was being reviewed]

---

## FB-01: [Title]

**Observed:** ...
**Root cause:** ...
**File:** `path/to/file.tsx:line`
**Fix:** ...
**Severity:** Low | Medium | High
**Assigned to:** ...

---

## Summary

| ID | Issue | Severity | Status |
|----|-------|----------|--------|
| FB-01 | ... | Low | Fixed |
| FB-02 | ... | High | Open |

---

_Feedback collected by [agent] — Whiteport Design Studio_
```

---

## Tone

Stay in character. Keep responses short during the listening phase — one-line acknowledgments, not paragraphs. The user is in flow and doesn't want to read essays between observations.

Save the full summary for after they say they're done.

---

## Key Principles

1. **Never disable the user's flow.** Capture fast, investigate async.
2. **Fix what you can, delegate what you can't.** Don't batch everything to Mimir if you can fix 5 of 8 items in 30 seconds.
3. **Commit before spawning.** Always have a clean baseline.
4. **One agent per file.** Never let two agents edit the same file.
5. **Verify in browser.** Fixes aren't done until they're visually confirmed.
6. **The feedback file is the source of truth.** Everything tracked there, not in conversation memory.
