# Agentation

**Category:** Review & Annotation Tool
**Purpose:** Visual markup and annotation for live web pages — AI agent feedback loop
**Repository:** <https://github.com/nicholasgriffintn/agentation>

---

## What It Is

Agentation is an npm package that overlays a toolbar on any web page, letting users and AI agents annotate elements with comments, drawings, and structured feedback. In WDS, it bridges the gap between visual review and actionable design feedback.

Key capabilities:

1. **Element selection** — Click any element to annotate it, or draw a bounding box to select an area
2. **Drawing overlay** — Freehand pen, arrows, and rectangles directly on the page
3. **Structured output** — Annotations export as markdown with element metadata, CSS selectors, and base64 drawing attachments
4. **Agent-readable** — Output format is designed for AI agents to parse and act on

**Output formats:**
- **Markdown** — Structured annotation report with element details
- **JSON** — DrawStroke data for each annotation
- **PNG** — Base64-encoded drawing overlays attached to annotations

---

## Why WDS Recommends It

**Visual Feedback Loop:**
- Freya builds a page → reviewer annotates directly on the live output
- Annotations include exact CSS selectors and bounding boxes — no ambiguity
- Drawing overlay lets reviewers circle problems, draw arrows to issues, sketch corrections
- Structured output feeds directly back into the agent workflow

**Speed:**
- No screenshots, no separate tools, no copy-paste coordinates
- Click element → type comment → add drawing → submit
- All annotations collected in one structured export

**Integration:**
- Drop-in React component — works with any framework that renders HTML
- Toolbar auto-excludes itself from annotation targets
- Dark and light mode support
- Keyboard shortcuts for common actions

---

## Setup Instructions

### 1. Installation

```bash
npm install agentation
```

### 2. Add to Project

```tsx
import { Agentation } from 'agentation';

function App() {
  return (
    <>
      <YourApp />
      <Agentation
        onOutput={(markdown) => {
          // Send to agent, save to file, or display
          console.log(markdown);
        }}
      />
    </>
  );
}
```

### 3. WDS Integration

For Astro projects, add Agentation as a client-side React island:

```astro
---
import { Agentation } from 'agentation';
---
<Agentation client:only="react" />
```

For review workflows, install as a dev dependency and conditionally render in development mode only.

---

## WDS Workflows

### Workflow A: Design Review Feedback

The primary WDS use case — Freya builds, reviewer annotates:

```
1. Freya delivers page build on dev branch
2. Reviewer opens page in browser with Agentation enabled
3. Reviewer selects elements, adds comments and drawings
4. Reviewer exports structured annotation report
5. Report feeds back to Freya as actionable fix list
6. Freya applies fixes, reviewer re-checks
```

### Workflow B: Drawing Annotations for Visual Issues

For layout, spacing, and alignment issues that are hard to describe in text:

```
1. Select area with bounding box tool
2. Click pen icon in feedback popup to activate drawing
3. Use freehand, arrow, or rectangle tools to mark issues
4. Type description in comment field simultaneously
5. Submit — drawing is encoded as base64 PNG attachment
6. Agent receives both text description and visual markup
```

### Workflow C: Agent Self-Review

Agents can programmatically trigger Agentation to audit their own output:

```
1. Agent renders page in headless browser
2. Agentation toolbar provides element inspection
3. Agent uses structured output to identify issues
4. Agent fixes issues and re-renders
5. Cycle until output passes quality checks
```

---

## Drawing Tools

The drawing overlay provides three tools:

| Tool | Icon | Use |
|------|------|-----|
| **Freehand** | Pen | Circle problems, underline text, sketch corrections |
| **Arrow** | Arrow | Point to specific elements, show flow direction |
| **Rectangle** | Square | Highlight areas, mark bounding boxes |

Drawing data is stored as structured JSON:

```json
{
  "type": "free",
  "color": "#ff3333",
  "size": 2,
  "points": [[120, 45], [125, 48], [130, 50]]
}
```

Undo support removes the last stroke. Drawings persist until the annotation is submitted or discarded.

---

## WDS Best Practices

### DO

**1. Annotate Specific Elements**
- Click the exact element that needs changes
- The structured output includes CSS selector and bounding box
- This gives agents precise targeting information

**2. Combine Drawing + Text**
- Draw an arrow pointing to the problem area
- Type a clear description of what's wrong and what's expected
- Visual + text gives agents the best context

**3. Use for Iterative Review Cycles**
- First pass: major layout and content issues
- Second pass: spacing, alignment, typography
- Third pass: interactions, hover states, edge cases

**4. Export and Version Control Reports**
- Save annotation exports alongside the page spec
- Track review history in git
- Reference specific annotations in commit messages

### DON'T

**1. Don't Annotate Pixel-Level Issues in Wireframe Phase**
- Agentation is for live rendered pages, not wireframes
- Use Excalidraw annotations for wireframe feedback
- Save Agentation for Phase 5+ when pages are built

**2. Don't Leave Agentation Enabled in Production**
- Dev/review dependency only
- Strip from production builds
- Use environment flags to conditionally render

**3. Don't Submit Empty Annotations**
- Always add a comment describing the issue
- Drawing alone without text context is hard for agents to interpret

---

## When to Use

### Use Agentation for:

- **Phase 5+ design review** — Annotating live rendered pages
- **QA feedback** — Marking visual bugs with drawings and comments
- **Agent feedback loops** — Structured output that agents can parse and act on
- **Client review** — Simple enough for non-technical reviewers to use
- **Iterative refinement** — Quick annotate → fix → re-check cycles

### Don't use for:

- **Wireframe feedback** — Use Excalidraw annotations instead
- **Code review** — Use GitHub PR comments for code-level feedback
- **Production monitoring** — Dev/review tool only
- **Design system documentation** — Use Figma or code-based tokens

---

## Resources

- Repository: <https://github.com/nicholasgriffintn/agentation>
- npm: `npm install agentation`

---

[← Back to Tools](wds-tools-guide.md)
