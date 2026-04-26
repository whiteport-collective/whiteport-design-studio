---
name: rendering-excalidraw
version: "0.3.0"
description: Render wireframes as Excalidraw JSON files. Called by the wireframe tool or directly when Excalidraw output is requested.
agents: [freya]
---

# Excalidraw Renderer

Produces `.excalidraw` JSON files from wireframe content descriptions.

---

## Canvas

| Context | Size |
|---------|------|
| Desktop | 1440 × 900 |
| Mobile | 390 × 844 |

Background: `#f8f9fa`

---

## Element rules

- `roughness: 0` — clean lines
- `strokeWidth: 1` — uniform
- `fillStyle: "solid"`
- Rounded corners on cards and inputs: `{ "type": 3, "value": 4–8 }`

## Colour palette

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

## Body text rule

Represent body text as grey filled rectangles: `backgroundColor: "#dee2e6"`, `height: 10`, no stroke. Use real text only when content is critical for understanding the screen.

## Grouping

Buttons and their labels must always be grouped (`groupIds: ["same-id"]`).

---

## Output

`{output_folder}/D-UX-Design/wireframes/[page-slug].excalidraw`
PNG export at `{output_folder}/D-UX-Design/wireframes/[page-slug].png`
