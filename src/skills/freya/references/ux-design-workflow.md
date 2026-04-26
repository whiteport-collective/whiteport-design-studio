---
name: ux-design-workflow
description: The Design Loop — how Freya moves one page from scenario to implemented, reviewed, and token-extracted. Principles, sequencing, and wireframe guidance.
---

# UX Design Workflow Reference

The Design Loop runs once per page. Eight steps, in order. Do not skip steps.

---

## Loop overview

| Step | Name | Blocks on |
|---|---|---|
| 1 | Discuss | — |
| 2 | Spec | — |
| 3 | Wireframe | — |
| 4 | Approve | **User — hard stop** |
| 5 | Update spec | — |
| 6 | Implement | Developer / Mimir |
| 7 | Browser review | — |
| 8 | Extract tokens | — |

A page is only complete at step 8 (`T`). Never consider a page done before then.

---

## Step 1 — Discussion

The discussion is a conversation, not a form. Start from the scenario:

"In the scenario, [User] arrives here after [X]. What's the most important thing this page needs to do for them?"

Work through five questions (one at a time, not as a list):
- **Purpose** — what job does this page do for the user at this moment?
- **Content** — what information, data, or options does it show?
- **Actions** — what can the user do here?
- **Emotional arc** — what state do they arrive in? What state should they leave in?
- **Edge cases** — what are the empty, loading, and error states?

When discussion feels complete: "I think I have a solid picture. Ready to write the spec?"
Wait for confirmation before calling Spec Writer.

---

## Step 2 — Spec

Spec Writer generates the page spec from the discussion. After writing:
- Present it briefly
- Ask the user to read through it
- Accept adjustments

The spec is the source of truth. What's not in the spec will not be built.

---

## Step 3 — Wireframe

Wireframes are structural layouts, not visual designs. See `wireframe/SKILL.md` for the complete rule set.

Key principles:
- Show layout regions, interactive elements, real labels and placeholder text
- No annotations, callouts, or design rationale in the wireframe — that lives in the spec
- One screen at a time. Present and wait for feedback before continuing.

If the wireframe process reveals decisions that contradict the spec, note them — they will be reconciled in step 5.

---

## Step 4 — Approval gate

Hard stop. Do not proceed to implementation without explicit user confirmation.

"Does this wireframe work? Approve to move to implementation, or tell me what to change."

- If approved → step 5
- If changes → iterate wireframe, return to gate

---

## Step 5 — Spec update

After approval, reconcile the spec to exactly match the approved wireframe. Any decisions made during wireframing that changed the spec must land here.

Mimir builds from the spec. If spec and wireframe disagree, Mimir follows the spec — so they must agree.

---

## Steps 6–8 — Build, review, tokens

**Step 6:** Hand off to Mimir (or developer) with the approved spec and wireframe. Update Design Loop Status to `B`.

**Step 7:** After implementation is confirmed, invoke Design Reviewer with the built page URL, spec, and approved wireframe. If issues found — discuss severity and fix priority before marking reviewed.

**Step 8:** After browser review passes, invoke Token Extractor. Extract new colors, typography, spacing, and component patterns. Update the token registry.

---

## Design Loop Status codes

Update the design log after each step:

`○` not started · `S` speccing · `S✓` spec approved · `W` wireframed · `✓` approved · `✓S` spec synced · `B` building · `B✓` built · `R` reviewed · `T` tokens extracted

---

## Principles

**Spec before wireframe.** The spec defines intent. The wireframe expresses it visually. Never draw without a spec.

**Approval is a contract.** Once approved, the wireframe is the implementation target. Don't change it after step 4 without going back through the gate.

**Mimir reads specs, not feelings.** Implementation briefs describe what the spec says, not what the design discussion felt like.

**Tokens accumulate.** Each page adds to the shared token registry. By the end of Phase 4, the registry should represent the full design system.
