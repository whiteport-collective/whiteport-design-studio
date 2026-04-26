---
name: rendering-nanobanana
version: "0.1.0"
description: Render wireframes as images using NanoBanana (Gemini image generation). Called by the wireframe tool or directly when image-based wireframe output is requested.
agents: [freya]
---

# NanoBanana Renderer

Produces wireframe images via NanoBanana (Gemini image generation MCP).

---

## Usage

Requires the NanoBanana MCP server to be active in the current session.

Translates wireframe content descriptions into image generation prompts optimised for structural wireframe output — no colour, clear layout, labelled elements.

---

## Prompt pattern

```
Wireframe for [page name]. Low fidelity. No colour. White background, grey borders.
Show: [layout regions]. Include: [interactive elements with labels].
Style: clean structural diagram, not a mockup.
```

---

## Output

Image saved to `{output_folder}/D-UX-Design/wireframes/[page-slug].png`

---

## Status

Early implementation. Use Excalidraw renderer for production wireframes until this renderer is fully validated.
