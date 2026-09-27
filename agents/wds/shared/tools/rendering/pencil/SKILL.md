---
name: rendering-pencil
version: "0.1.0"
description: Render wireframes using Pencil.dev via MCP. Called by the wireframe tool or directly when Pencil output is requested.
agents: [freya]
---

# Pencil Renderer

Produces wireframe designs in Pencil.dev via the Pencil MCP server.

---

## Usage

Requires the Pencil MCP server to be active in the current session.

Receives wireframe content from the wireframe tool and translates it into Pencil batch_design operations.

---

## Output

Pencil document at the path configured in the active Pencil session.
PNG export at `{output_folder}/D-UX-Design/wireframes/[page-slug].png`

---

## Status

Early implementation. Use Excalidraw renderer for production wireframes until this renderer is fully validated.
