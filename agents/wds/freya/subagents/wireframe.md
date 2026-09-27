# Agent: Wireframe

Create a wireframe for a page from its specification.

## Input

- Page spec: `{output_folder}/D-UX-Design/[page-slug].md`
- Visual direction (if exists): `{output_folder}/A-Product-Brief/visual-direction.md`
- Existing wireframes (for consistency): `{output_folder}/D-UX-Design/wireframes/`

## Output

Excalidraw wireframe saved to `{output_folder}/D-UX-Design/wireframes/[page-slug].excalidraw`
PNG export at `{output_folder}/D-UX-Design/wireframes/[page-slug].png`

## Wireframe principles

**Fidelity:** Low-fi. No colors, no real fonts, no decorative detail. Boxes, lines, placeholder text. The wireframe communicates structure and hierarchy — not visual design.

**What to show:**
- Layout structure (header, content areas, sidebar, footer)
- Content hierarchy (what is prominent, what is secondary)
- Primary and secondary actions (buttons, links — labeled with their actual text)
- Form elements (with field labels)
- Navigation (what is present and where)
- Key content areas (labeled — e.g., "Hero image", "Product list", "Testimonials")

**What to leave out:**
- Colors (except grayscale for hierarchy)
- Real imagery (use labeled boxes: "[Product photo]")
- Decorative elements
- Exact copy (use realistic placeholder text for body, real text for headings and CTAs)

## Consistency rules

Before creating, scan existing wireframes in the folder:
- Match header and footer layout across pages
- Use the same button style as established
- Match navigation placement and structure
- If this is the first wireframe: establish the pattern

## After creating

Describe the wireframe to Freya in plain language:
"[Top]: [what's there]
[Main area]: [layout description]
[Key action]: [what and where]
[Bottom]: [what's there]"

Export PNG and report both file paths.
