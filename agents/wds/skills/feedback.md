---
name: feedback
description: Live feedback rounds. User browses and reports issues in natural language, agent captures structured FB-XX items and sorts each one. Bugs (spec right, code wrong) are fixed inline or delegated. Spec issues go through the spec first, then to Mimir as a spec delta. Use when the user says "I want to give feedback", "I have feedback", "let's review", or /feedback.
used_by: [freya, saga, mimir]
argument-hint: "[optional: area to focus on, e.g. 'checkout', 'home page']"
---

# Feedback — Live Review & Fix Rounds

## Overview

This skill turns live browsing sessions into structured fix plans with tracked outcomes. The user speaks freely while the agent does all the structuring, investigating, and fixing.

Every WDS agent can run it. Freya owns the spec route.

**The one rule:** feedback never goes to code when the spec is what's wrong. Each item is either a **bug** (the spec is right, the code doesn't follow it: fix it) or a **spec issue** (the spec is wrong or missing something: change the spec first, then brief Mimir with the spec delta).

---

## On Activation

1. Create a feedback file: `{output_folder}/E-Development/WO-{N}-{NN}-{area}-feedback.md`
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
- Read the spec for the page (`{output_folder}/D-UX-Design/[page-slug].md`) and decide the **type**:

| Type | Meaning | Route |
|---|---|---|
| Bug | The spec is right, the code doesn't follow it | Fix (triage below) |
| Content gap | Something is missing from the spec | Spec |
| Content conflict | The spec says one thing, the feedback another | Spec |
| Behavior change | An interaction or state needs to change | Spec |
| Structure change | Layout, hierarchy or flow needs to change | Spec |
| Out of scope | New work, not in the current spec | Backlog |
| Unclear | Can't be mapped without more information | Ask one focused question |

### 3. Log

Add the issue to the feedback file immediately as `FB-{XX}`:

```markdown
## FB-XX: [Short title]

**Observed:** [What the user described]

**Root cause:** [What you found in the code]

**File:** `path/to/file.tsx:line`

**Type:** Bug | Content gap | Content conflict | Behavior change | Structure change | Out of scope

**Fix:** [Concrete change needed, or the spec change for spec issues]

**Severity:** Low | Medium | High
**Assigned to:** [Self | Mimir | Codex | Spec | Deferred]
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

Spec issues are never fixed in code during the round: mark them **Spec** and handle them in "Spec issues" below. Assign each **bug** based on complexity:

| Complexity | Action |
|-----------|--------|
| One-line CSS/label change | Fix inline yourself, mark Fixed. Visual fixes follow `../data/taste.md` |
| Small component change (< 20 lines) | Fix inline yourself, mark Fixed |
| Architectural change or multi-file | Assign to sub-agent (Mimir/Codex) |
| Needs a design decision | Mark Open, discuss with user |
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

## Spec issues

Handled after the round, page by page. The spec is the source of truth.

1. **Analyse.** Group the spec items per page and present them: "[Page]: [item] → [type]: [what changes in the spec]". Out-of-scope items listed separately. Wait for confirmation.
2. **Propose the edit.** Per change: section, before, after. Wait for explicit approval. Never update the spec before it.
3. **Update the spec** with [spec-writer](../freya/subagents/spec-writer.md) in update mode: only the approved changes, nothing else rewritten.
4. **Brief Mimir** with [mimir-brief](../freya/subagents/mimir-brief.md): the approved spec changes, the affected pages and acceptance criteria. The original feedback is context only. Mimir builds from what the spec now says, not from what anyone felt.
5. **Close.** Mark the FB items done in the feedback file, log it in the design log (feedback received, spec updated, Mimir briefed), and offer to add out-of-scope items to the backlog.

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
2. **Spec before code.** A spec issue changes the spec first. Only bugs go straight to code.
3. **Fix what you can, delegate what you can't.** Don't batch everything to Mimir if you can fix 5 of 8 items in 30 seconds.
4. **Commit before spawning.** Always have a clean baseline.
5. **One agent per file.** Never let two agents edit the same file.
6. **Verify in browser.** Fixes aren't done until they're visually confirmed.
7. **The feedback file is the source of truth.** Everything tracked there, not in conversation memory.
