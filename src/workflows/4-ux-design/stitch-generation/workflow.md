---
name: Stitch UI Generation
description: AI-assisted UI design using Google Stitch from specifications and sketches
web_bundle: true
---

# Stitch UI Generation

**Goal:** Generate production-quality UI designs using Google Stitch AI

**Your Role:** Guide the user through preparing inputs and creating a Stitch generation dialog

---

## OVERVIEW

Google Stitch is an AI-powered UI design tool that transforms text prompts, sketches, and reference images into responsive interfaces.

**Input Formula:**
```
Visual Reference + Sketch + Specification = Stitch Generation
```

**Output:** UI designs exportable to Figma or HTML/CSS

---

## WHEN TO USE STITCH

**Use Stitch when:**
- ✅ New page with detailed specification ready
- ✅ Have a visual reference (existing design or screenshot)
- ✅ Have a sketch showing layout structure
- ✅ Want rapid visual design iteration
- ✅ Need production-quality mockups quickly

**Skip Stitch when:**
- ❌ Building design system components (use tokens instead)
- ❌ Minor updates to existing designs (edit directly)
- ❌ No specification exists yet (write spec first)
- ❌ Complex multi-screen flows (do 2-3 screens at a time)

---

## BEFORE STARTING

### Prerequisites

1. **Specification exists** for the screen(s) to generate
2. **Visual reference available:**
   - Screenshot of existing implemented page, OR
   - Approved design that establishes visual language
3. **Sketch available** showing layout structure

### Decision: What Visual Reference?

| Situation | Reference Choice |
|-----------|------------------|
| Code exists and looks correct | Screenshot of running code |
| Starting fresh, no code | Original sketch or moodboard |
| Code exists but needs redesign | Original sketch |
| Want style from one page, layout from sketch | Both (upload 2 images) |

---

## WORKFLOW

### Step 1: Create Dialog

Create a Stitch generation dialog in the project's Agent Dialogs folder.

**Template:** Use `9-agent-dialogs/templates/dialog-types/stitch-generation.template.md`

**Location:** `docs/F-Agent-Dialogs/{YYYY-MM-DD}-freya-stitch-{feature}/`

**Dialog captures:**
- Which screens to generate
- What visual reference to use
- Pre-crafted prompts
- Generation results and decisions

---

### Step 2: Answer Pre-Generation Questions

For each potential screen, decide:

**Question 1: Generate in Stitch?**

| Screen | Has Code? | Has Sketch? | Generate? | Why |
|--------|-----------|-------------|-----------|-----|
| {screen} | ✅/❌ | ✅/❌ | ✅/❌ | {reason} |

**Question 2: What reference?**

| Screen | Reference | Source |
|--------|-----------|--------|
| {screen} | Code screenshot / Sketch | {path or action} |

---

### Step 3: Gather Inputs

For each screen to generate:

| Input | Action |
|-------|--------|
| **Visual Reference** | Take screenshot OR locate existing design |
| **Sketch** | Locate in spec's `Sketches/` folder |
| **Prompt** | Prepare using template (see Step 3a) |

---

### Step 3a: Prepare the Prompt

**DO NOT paste raw specifications into Stitch.** They contain:
- Object IDs (not useful for design generation)
- Multiple translations (confusing)
- Technical implementation details

**Instead, use the prompt template:** [stitch-prompt.template.md](stitch-prompt.template.md)

The prompt should include:

| Section | Source |
|---------|--------|
| **Project Context** | Design System overview, Product Brief |
| **Design System** | Color-Palette.md, Typography-System.md |
| **Component Styles** | Button/Input specs from Design System |
| **Screen Content** | Specification (ONE language, no Object IDs) |
| **Current State Notes** | What's ShadCN default vs custom |

**Important notes:**
- Use actual hex colors from your design system
- Describe component styles (rounded buttons, gradients, etc.)
- Include only ONE language (primary language)
- Note what's currently using default styling that needs brand styling

---

### Step 4: Generate in Stitch

1. Go to [stitch.withgoogle.com](https://stitch.withgoogle.com)
2. Upload **visual reference** image
3. Upload **sketch** image (if different from reference)
4. Paste **specification** as prompt
5. Add instruction: *"Generate this screen matching the visual style of the reference and layout of the sketch."*
6. Generate 2-3 variants
7. Select best result

**Settings:**
- Standard Mode: Quick iteration
- Pro Mode: Higher fidelity (uses more quota)
- Viewport: Mobile 390px or Desktop 1440px

---

### Step 5: Review Against Spec

| Check | Pass? |
|-------|-------|
| Content/copy matches spec | ✅/❌ |
| Layout follows sketch | ✅/❌ |
| Visual style matches reference | ✅/❌ |
| All key elements present | ✅/❌ |

**If issues:** Re-prompt with specific corrections or edit in Stitch.

---

### Step 6: Export & Store

| Format | When | Destination |
|--------|------|-------------|
| **Figma** | Team collaboration, design system work | Figma project |
| **HTML/CSS** | Code reference, rapid prototypes | `{spec-folder}/Visual-Design/` |
| **Screenshot** | Documentation | `{spec-folder}/Visual-Design/` |

**Naming:** `{screen-name}-stitch-v{#}.{ext}`

---

### Step 7: Update Specification

Add to the specification file:

```markdown
## Visual Design

**Stitch Generated:** [sign-in-stitch-v1.png](Visual-Design/sign-in-stitch-v1.png)
```

---

## STITCH CAPABILITIES & LIMITS

### What Stitch Does Well
- Single screen generation from prompts
- Style matching from reference images
- Responsive layouts (mobile/desktop)
- Clean HTML/CSS export
- Figma-compatible output

### Current Limitations
- Best with 2-3 screens at a time
- Layouts can be generic (need refinement)
- Doesn't capture deep UX nuance
- No built-in design system awareness
- Free tier: 350 standard + 200 pro screens/month

---

## PROMPT TIPS

### Effective Prompts Include

1. **App type:** "Mobile sign-in screen for..."
2. **Context:** "...a Swedish family dog walk coordination app"
3. **Visual direction:** "Match the attached reference..."
4. **Key elements:** List all major UI elements
5. **Content:** Include actual copy/text
6. **Mood:** "Friendly, trustworthy, family-oriented"

### Example Prompt Structure

```
[App type] [screen name] for [product description].

Visual style: Match the attached reference exactly.

Screen layout:
- [Section 1]: [elements and content]
- [Section 2]: [elements and content]
- [Section 3]: [elements and content]

Key interactions: [primary action], [secondary action]

Mood: [brand tone and feel]
Viewport: [Mobile 390px / Desktop 1440px]
```

---

## INTEGRATION WITH WDS

### Workflow Position

```
Specification → Stitch Generation → Visual Design → Implementation
     ↓                  ↓                 ↓              ↓
  Content         AI-Assisted        Approved       Code
  & Structure      Design           Mockups        Build
```

### Related Workflows

- **Before Stitch:** Page Specification workflow (create the spec first)
- **After Stitch:** Prototype Implementation dialog (build from the design)
- **Alternative:** Design Exploration dialog (if exploring multiple directions)

---

## QUICK START

**Fastest path:**

1. User: "I want to generate a UI design for [screen name]"
2. Freya: Creates Stitch dialog from template
3. Freya: Asks pre-generation questions (which screens, what reference)
4. User: Provides answers, takes screenshot if needed
5. User: Goes to Stitch, uploads inputs, pastes spec
6. User: Generates, reviews, exports
7. Freya: Updates dialog with results, links in spec

---

## SUPPORT

**Google Stitch:**
- [stitch.withgoogle.com](https://stitch.withgoogle.com)
- [Google Developers Blog - Introducing Stitch](https://developers.googleblog.com/stitch-a-new-way-to-design-uis/)

**WDS Templates:**
- Dialog template: `9-agent-dialogs/templates/dialog-types/stitch-generation.template.md`

---

_Stitch UI Generation Workflow — Freya WDS Designer — Phase 4 UX Design_
