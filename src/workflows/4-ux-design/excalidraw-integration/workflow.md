---
name: Excalidraw Integration
description: Optional sketching tool setup and usage guides for visual design thinking
web_bundle: true
---

# Excalidraw Integration

**Goal:** Set up and use Excalidraw for WDS sketching workflows

**Your Role:** Guide reference for optional Excalidraw integration

---

## OVERVIEW

This is a **guide collection** for using Excalidraw with WDS, not a step-by-step workflow.

**Excalidraw:** Free, open-source whiteboard tool that creates hand-drawn style diagrams.

**Status:** Optional - Only needed if user chooses Excalidraw as sketching tool

---

## WHEN TO USE

**Use Excalidraw if:**
- ✅ Prefer digital sketching over paper
- ✅ Want collaborative design sessions
- ✅ Need AI-generated layout variations
- ✅ Want version-controlled wireframes
- ✅ Like hand-drawn aesthetic

**Skip Excalidraw if:**
- ❌ Happy with paper and pen
- ❌ Using other tools (Figma, iPad, etc.)
- ❌ Don't need digital sketching

---

## AVAILABLE GUIDES

### 1. Getting Started

**[Excalidraw Guide](guides/excalidraw-guide.md)**
- Overview and quick start
- When to use Excalidraw
- Installation options
- Component library setup

**Use when:** First time setting up Excalidraw for WDS

---

### 2. Setup & Configuration

**[Excalidraw Setup](guides/excalidraw-setup.md)**
- Detailed installation steps
- VS Code extension setup
- Project configuration
- Component library loading

**Use when:** Installing and configuring Excalidraw

---

### 3. Sketching Workflow

**[Sketching Guide](guides/sketching-guide.md)**
- How to sketch with Excalidraw
- WDS sketching patterns
- Component usage
- Best practices

**Use when:** Creating sketches with Excalidraw

---

### 4. AI Collaboration

**[AI Collaboration](guides/ai-collaboration.md)**
- Using AI to generate sketches
- Prompt patterns for layouts
- Iterating with AI assistance
- Converting ideas to diagrams

**Use when:** Want AI help generating sketches

---

### 5. Export & Documentation

**[Export Workflow](guides/export-workflow.md)**
- Exporting .excalidraw to PNG/SVG
- Manual export steps
- Automated export (optional)
- GitHub display setup

**Use when:** Need to export sketches for documentation

---

## QUICK REFERENCE

### Enable in Project

Edit: `project-config.yaml`

```yaml
sketching:
  tool: excalidraw # or "paper" or "figma" or "other"
  excalidraw:
    enabled: true
    auto_export: false # Auto-generate PNG/SVG
    use_library: true # Load WDS components
```

---

### Installation

**VS Code Extension (Recommended):**
1. Open Extensions (Ctrl+Shift+X)
2. Search "Excalidraw"
3. Install "Excalidraw Editor"

**Web Version:**
- https://excalidraw.com (no installation)

---

### Basic Usage

**Create sketch:**
1. Create `.excalidraw` file in project
2. Open in VS Code (Excalidraw editor opens)
3. Sketch your design
4. Save file

**Export for docs:**
1. Open `.excalidraw` file
2. Hamburger menu → Export image
3. Choose PNG (recommended)
4. Save to same folder

---

## FILE ORGANIZATION

### Sketch Files

```
docs/D-UX-Design/[scenario-name]/sketches/
├── page-name.excalidraw     ← Source (editable)
├── page-name.png            ← Display (GitHub)
└── page-name.svg            ← Optional (scalable)
```

**Convention:**
- `.excalidraw` = Source file (version controlled)
- `.png` = Export for GitHub display
- `.svg` = Optional scalable export

---

## INTEGRATION POINTS

### With WDS Workflows

**Scenario Initialization →** Excalidraw Sketching

After completing scenario initialization, use Excalidraw to:
1. Sketch the shortest path journey
2. Create page layouts for each step
3. Visualize user flow

**Page Specifications →** Excalidraw Reference

When writing page specs, reference Excalidraw sketches:
- Embed PNG exports in spec documents
- Link to source `.excalidraw` files
- Use sketches for layout guidance

---

## TROUBLESHOOTING

### VS Code Extension Not Opening Files

**Solution:** Ensure file has `.excalidraw` extension

### Exports Not Rendering in GitHub

**Solution:** Make sure `.png` files are committed alongside `.excalidraw` source

### Component Library Not Loading

**Solution:** Check `project-config.yaml` has `use_library: true`

---

## SUPPORT

**Official Documentation:**
- https://docs.excalidraw.com

**WDS-Specific Help:**
- See guides in `guides/` folder
- Each guide covers specific use case

---

## NOTES

**This is optional tooling** - WDS works with any sketching method:
- Paper and pen
- Figma
- iPad/Procreate
- Excalidraw
- Other tools

Choose what works best for your workflow.

---

_Excalidraw Integration - Optional sketching tool for WDS_
