---
name: freya-wireframe
version: 0.3.0
description: Rules for drawing Excalidraw wireframes in WDS projects.
agents: [freya]
---

# Freya — Wireframe Skill

Rules for producing Excalidraw wireframes. The spec file documents intent — the wireframe only shows structure.

---

## Golden rule

**No annotations or comments in the wireframe.** The step spec file (`{step}.md`) explains what things do and why. The wireframe shows layout and structure only.

---

## File location

```
{output_folder}/C-UX-Scenarios/{scenario}/{step}/Sketches/{step}.excalidraw
```

---

## Canvas

| Context | Size |
|---------|------|
| Desktop | 1440 × 900 |
| Mobile | 390 × 844 |

Background: `#f8f9fa` (light grey — distinguishes canvas from content).

---

## Element rules

- `roughness: 0` — clean lines, not hand-drawn
- `strokeWidth: 1` — uniform
- `fillStyle: "solid"`
- Rounded corners on cards and inputs: `{ "type": 3, "value": 4–8 }`

### Grouping

Buttons and their labels must always be grouped together (`groupIds: ["same-id"]`). This keeps them movable as a unit and makes the structure unambiguous for developers reading the wireframe.

### Colour palette

| Role | Colour |
|------|--------|
| Background | `#f8f9fa` |
| Surface / card | `#ffffff` |
| Border / stroke | `#dee2e6` |
| Input border | `#adb5bd` |
| Label text | `#495057` |
| Body text | `#212529` |
| Placeholder text | `#adb5bd` |
| Primary button fill | `#212529` |
| Primary button text | `#ffffff` |
| Destructive | `#e03131` |

---

## Approval loop

1. Draw one screen.
2. Present to user: `Wireframe {step} done — approve to continue to {next-step}?`
3. Wait for explicit approval before drawing the next screen.
4. Do not move forward on assumption.

---

## What goes in a wireframe

- Layout regions (nav, sidebar, content area, footer)
- All interactive elements (inputs, buttons, links, selects)
- Real labels and placeholder text — no "Lorem ipsum"
- Correct relative sizing between elements

### Body text rule

Body text (paragraph content, list items, descriptions) is represented as **text markers** — grey filled rectangles that indicate a line of text without showing actual words. Use `backgroundColor: "#dee2e6"`, `height: 10`, no stroke.

**Exception:** When the actual text content is critical for understanding what the screen does — data values, agent messages, order details, customer names — use real text. The test: would a developer misunderstand the screen without reading the actual words?

## What does NOT go in a wireframe

- Annotations, callouts, arrows pointing at things
- Design rationale or explanations
- Open questions
- Colour beyond the palette above
- Icons (use labelled rectangles if an icon slot is needed)

