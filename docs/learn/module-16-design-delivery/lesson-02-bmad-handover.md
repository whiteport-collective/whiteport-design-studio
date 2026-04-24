# Lesson 2: BMAD Handover — Connecting Design to Coding Agents

**Module 16 | Time: 15 min | Skill: `/design-delivery`**

---

## The Gap Between Design and Code

You've packaged your design. The DD file is complete. The acceptance criteria are written.

Now you run `/mimir` — and the coding agent starts building. But it doesn't look at your design specs. It reads the PRD.

This is the handover gap: **your specs live in D-UX-Design, but the coding agent reads the PRD.** Unless you bridge these two documents, the agent builds from the PRD's outline alone — missing all the detail Freya put into the page specs.

---

## The Fix: `/design-delivery`

`/design-delivery` is a one-command bridge. It:

1. Scans your `D-UX-Design/` folder for completed page specs
2. Finds the BMAD PRD in `_bmad-output/`
3. Matches each spec to the right PRD section
4. Injects a `**Design spec:**` reference line into each section

After running it, the PRD becomes the single entry point: the coding agent follows it, finds the design reference, reads the full spec. Nothing is missed.

---

## When to Run It

Run `/design-delivery` **after** you've packaged a flow (Lesson 1) and **before** you wake Mimir to build it.

```
Design complete → /design-delivery → /mimir → Build
```

It's idempotent — safe to run again if specs change. It updates existing references rather than duplicating them.

---

## How It Works

### Interactive mode (no arguments)

```
/design-delivery
```

Freya shows you the inventory:

```
📦 Design Delivery — Dog Week

Available specs:
  ✓  owner-signup         (/signup)          — approved
  ✓  walker-profile       (/walkers/:id)      — approved
  ⏳  booking-flow         (/book)             — in progress
  ○  payment              (/checkout)         — not started

Which pages to deliver? (enter names or "all approved")
```

Type `all approved` or name specific pages. Freya injects and reports:

```
── Design Delivery ───────────────────────────
PRD: _bmad-output/docs/prd.md

Delivered:
  ✓  owner-signup   → 3.1 User Registration
  ✓  walker-profile → 3.4 Walker Profiles

Unmatched (add manually):
  (none)

PRD updated. Coding agents will now find design specs automatically.
─────────────────────────────────────────────
```

### Targeted mode (with arguments)

```
/design-delivery owner-signup walker-profile
```

Delivers only the named pages. Useful mid-flow when you want to hand off part of the work while continuing to design the rest.

---

## The Agent Handoff

After delivering, Freya writes a handoff file for Mimir at `_progress/mimir.md`:

```
Context: Design delivery complete. 2 page specs injected into PRD.
Pages: owner-signup, walker-profile
Next: Run /mimir to plan and execute the build.
```

Open a new session and run `/mimir` — it picks up from there.

---

## What Happens in the PRD

Before `/design-delivery`:

```markdown
### 3.1 User Registration

New users can create an account using email and password.
- Email must be unique
- Password minimum 8 characters
```

After `/design-delivery`:

```markdown
### 3.1 User Registration

**Design spec:** `_bmad/wds/D-UX-Design/owner-signup.md`

New users can create an account using email and password.
- Email must be unique
- Password minimum 8 characters
```

The coding agent reads the PRD, follows the reference, opens the full spec. Every state, every error message, every interaction — all there.

---

## When Sections Don't Match

If a spec can't be matched to a PRD section, `/design-delivery` reports it as unmatched rather than guessing. Add the reference manually in those cases, or update the PRD section heading to include the page name.

---

## The Rule

**Every approved spec should be in the PRD before Mimir builds it.**

Don't rely on Mimir to find the specs on its own. The PRD is the contract — make it complete.

---

## Summary

| What | Why |
|------|-----|
| Run after packaging (Lesson 1) | Specs are complete and stable |
| Run before `/mimir` | Coding agent reads PRD first |
| Safe to re-run | Updates references, never duplicates |
| Unmatched = fix PRD heading | Don't force-insert into wrong section |

---

[← Lesson 1: Validation and Packaging](lesson-01-validation-packaging.md) | [Tutorial 16 →](tutorial-16.md)

*Part of Module 16: Design Delivery*
