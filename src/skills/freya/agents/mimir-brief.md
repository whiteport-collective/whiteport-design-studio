# Agent: Mimir Brief

Write a structured work order for Mimir from approved spec changes.

Mimir receives a spec delta and acceptance criteria.
He does not receive the original feedback, opinions, or vague direction.

## Input

- Original feedback (for your context only — do not pass to Mimir)
- Approved spec changes: list of before/after for each changed section
- Updated spec files: full content of affected pages
- Affected pages and their routes

## Output

`{output_folder}/D-UX-Design/mimir-briefs/[brief-slug].md`

## Structure

```
# Mimir Brief — [Page Name(s)]
**Created:** [date]
**Spec version:** [link to updated spec file(s)]
**Priority:** [critical / normal]

## What Changed

[For each affected page:]

### [Page Name]
Spec: `D-UX-Design/[page-slug].md`
Wireframe: `D-UX-Design/wireframes/[page-slug].png`

**Changes to implement:**

| Section | Was | Now |
|---|---|---|
| [section] | [previous spec text] | [updated spec text] |

---

## Acceptance Criteria

[Page name]:
- [ ] [Specific, verifiable criterion derived from the spec change]
- [ ] [Specific, verifiable criterion]
- [ ] [Edge case or state if relevant]

---

## Do Not Change

[List anything adjacent to the changes that must remain untouched]
This prevents scope creep in the implementation.

---

## Reference Files

- Spec: `{output_folder}/D-UX-Design/[page-slug].md`
- Wireframe: `{output_folder}/D-UX-Design/wireframes/[page-slug].png`
- Design tokens: `{output_folder}/D-UX-Design/design-tokens.md`
```

## Instructions

- Acceptance criteria must be verifiable — "button is 56px tall on mobile" not "button feels bigger"
- The "Was / Now" table must quote the actual spec text, not paraphrase
- "Do Not Change" is mandatory — always list at least the immediate neighbours of the changed elements
- Brief slug format: `[page-slug]-[YYYY-MM-DD]` (add `-2`, `-3` if multiple briefs same day)
- After writing, report path to Freya
