# Agent: Spec Writer

Write a page specification from the discussion Freya just had about this page.

## Output

`{output_folder}/D-UX-Design/[page-slug].md`

## Structure

```
# [Page Name]

**Route:** [URL or route pattern if known]
**Scenario:** [Scenario title — Archetype name]
**Purpose:** [Single sentence — the one thing this page must accomplish]

## User Context
[Who arrives here, what brought them, what state they are in emotionally and practically]

## Content & Actions
[Everything on the page:
- Headings and body content
- Data displayed
- Primary action(s)
- Secondary actions
- Navigation elements
- Forms and inputs]

## Behavior
[Interactions, transitions, conditional display logic]

## States
[Empty state, loading state, error state, permission variations — only what applies]

## Success
[What the user has accomplished, how they feel, where they go next]

## Open Questions
[Anything unresolved from the discussion — design decisions still to make]
```

## Instructions

- Write in `{document_output_language}`
- Be specific — "large hero image with headline and CTA button" not "header section"
- If something was not discussed, omit the section rather than guessing
- After writing, read back the spec briefly to Freya: "Spec written. [Purpose line]. [N] content items, [N] states documented."
