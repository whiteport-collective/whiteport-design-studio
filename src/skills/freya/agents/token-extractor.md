# Agent: Token Extractor

Read the implemented page and extract design tokens. Update the token registry.

## Input

- Implemented page (inspect via browser tools or read source)
- Page spec: `{output_folder}/D-UX-Design/[page-slug].md`
- Existing registry: `{output_folder}/D-UX-Design/design-tokens.md` (may not exist yet)

## What to extract

**Colors** — every color in use: backgrounds, text, borders, interactive states, semantic colors (success/warning/error)
Name as: `color-[semantic-name]` (e.g., `color-brand-primary`, `color-text-muted`, `color-error`)

**Typography** — every type style in use: font, size, weight, line-height, letter-spacing
Name as: `text-[role]` (e.g., `text-heading-xl`, `text-body`, `text-label-sm`)

**Spacing** — every spacing value in use: padding, gap, margin patterns, layout units
Name as: `space-[N]` or `space-[semantic]` (e.g., `space-4`, `space-section`)
Flag named layout units (header height, sidebar width, content max-width) as spacing objects.

**Component candidates** — recurring UI patterns seen on this page or across pages. Flag for design system phase, do not extract yet.

## Registry update

Read existing `design-tokens.md` if it exists. Add new tokens. Do not remove or rename existing ones without flagging the conflict explicitly.

**Registry format:**
```
# Design Tokens — [Project Name]
Last updated: [date] — after [Page name]

## Colors
| Token | Value | First seen |
|---|---|---|

## Typography
| Token | Value | First seen |
|---|---|---|

## Spacing
| Token | Value | First seen |
|---|---|---|

## Component Candidates
| Pattern | Pages | Notes |
|---|---|---|
```

## Return to Freya

- [N] new tokens added (broken down by type)
- Any conflicts found
- Component candidates worth noting
