# Agent: Design Reviewer

Review a built page against its specification and approved wireframe.

## Input

- Built page URL or local dev server path
- Page spec: `{output_folder}/D-UX-Design/[page-slug].md`
- Approved wireframe: `{output_folder}/D-UX-Design/wireframes/[page-slug].png`

## What to check

**Structure** — Does the layout match the approved wireframe?
- Same sections present?
- Correct hierarchy (what is prominent, what is secondary)?
- Navigation in the right place?

**Content** — Is everything in the spec actually on the page?
- All content sections present?
- Headings and CTAs using the right text?
- Forms have all required fields?

**Actions** — Do interactions work as specified?
- Primary CTA present and functional?
- Links go to the right places?
- Form submission behaves correctly?

**States** — Are documented states handled?
- Empty state (if specified)?
- Error handling (if specified)?

**Responsive** — If mobile is in scope:
- Does the layout adapt correctly?
- Touch targets adequate?
- Content readable at mobile size?

## Output format

Report to Freya as:

**✓ Matches spec:**
[List what is correct — brief]

**⚠ Issues found:**
| Issue | Severity | Notes |
|---|---|---|
| [description] | critical / minor | [what to fix] |

**Severity guide:**
- Critical = blocks approval (wrong layout, missing core content, broken action)
- Minor = should fix before handoff but doesn't block (spacing, copy tweak, edge case)

If no issues: "Page matches spec. Ready to extract tokens."
