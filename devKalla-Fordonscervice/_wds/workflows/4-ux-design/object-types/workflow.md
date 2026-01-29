---
name: Object Type Router
description: Intelligent object detection and routing system for page specification
web_bundle: true
---

# Object Type Router

**Goal:** Analyze sketch objects, detect type, assess complexity, and route to appropriate specification template

**Your Role:** Intelligent router providing object analysis and specification guidance

---

## OVERVIEW

This is a **router workflow** used within the page specification process.

**Purpose:** Detect what UI objects are in a sketch and guide proper specification

**Key Features:**
- ✅ Text detection priority (horizontal line pairs = text)
- ✅ Intelligent object interpretation
- ✅ Complexity assessment and routing
- ✅ User confirmation of interpretations
- ✅ Decomposition coaching for complex components

---

## WHEN TO USE

**Use this router when:**
- ✅ In page specification process (step 4c-03)
- ✅ Need to identify object type from sketch
- ✅ Want AI interpretation of UI elements
- ✅ Need complexity routing for components
- ✅ Require specification template for object

**This is NOT a standalone workflow:**
- ❌ Don't call directly from user request
- ❌ Only used within page specification workflow
- ❌ Part of larger specification process

---

## HOW IT WORKS

### The 3-Step Process

**Step 1: Detection**
- Apply text detection rules (priority)
- Analyze visual characteristics
- Consider context and placement

**Step 2: Interpretation**
- Suggest object type with confidence
- Explain reasoning
- Request user confirmation

**Step 3: Routing**
- Route to appropriate template
- Load object-specific instructions
- Guide specification process

---

## ROUTING LOGIC

### Text Detection Priority

**FIRST:** Check for horizontal line pairs
- 2 parallel lines = 1 line of text
- Multiple pairs = multiple text lines
- Single lines = decorative (borders, dividers)

**If text detected:**
→ Route immediately to [heading-text.md](templates/heading-text.md)

**Reference:** [TEXT-DETECTION-PRIORITY.md](TEXT-DETECTION-PRIORITY.md)

---

### Object Type Detection

**If not text, analyze:**
- Visual shape and style
- Interactive indicators
- Context and placement
- Common UI patterns

**Make interpretation:**
- Suggest object type
- Explain reasoning
- Get user confirmation

**Reference:** [object-router.md](object-router.md)

---

### Complexity Assessment

**After type confirmed:**

**Simple Component:**
- Single state
- No complex interactions
- No business logic
→ Document in page specification only

**Complex Component:**
- Multiple states (3+)
- Business rules
- Multi-step interactions
- State machines
→ Route to decomposition coaching

**Reference:** [COMPLEXITY-ROUTER.md](COMPLEXITY-ROUTER.md)

---

## AVAILABLE OBJECT TYPES

### Text Elements

**[Heading / Text](templates/heading-text.md)**
- Headings (H1-H6)
- Paragraphs
- Labels
- Captions
- Includes sketch analysis (line pairs, character capacity)

---

### Interactive Elements

**[Button](templates/button.md)**
- Primary, secondary, tertiary buttons
- Icon buttons
- Button groups

**[Text Input](templates/text-input.md)**
- Single-line inputs
- Search fields
- Form inputs

**[Link](templates/link.md)**
- Text links
- Navigation links
- Action links

**[Image](templates/image.md)**
- Static images
- Responsive images
- Image placeholders

**Additional (referenced):**
- Textarea
- Select dropdown
- Checkbox
- Radio button
- Toggle switch

---

### Container Elements

**Referenced:**
- Card
- Modal/Dialog
- Table
- List

---

### Navigation Elements

**Referenced:**
- Navigation menu
- Tabs
- Breadcrumbs

---

### Status Elements

**Referenced:**
- Badge
- Alert/Toast
- Progress indicator

---

### Custom Components

**Referenced:**
- Custom components (unique to project)

---

## ROUTING FLOW

```
Start
  ↓
[1] Text Detection Priority
  ├─ Horizontal line pairs?
  │   ├─ YES → Route to heading-text.md ✓
  │   └─ NO → Continue to [2]
  ↓
[2] Object Analysis
  ├─ Analyze visual/context
  ├─ Suggest interpretation
  ├─ Get user confirmation
  └─ Confirmed type → Continue to [3]
  ↓
[3] Complexity Assessment
  ├─ Simple component?
  │   └─ YES → Route to object template ✓
  └─ Complex component?
      └─ YES → Complexity Router (decomposition) ✓
```

**Visual Reference:** [ROUTER-FLOW-DIAGRAM.md](ROUTER-FLOW-DIAGRAM.md)

---

## INTERPRETATION EXAMPLES

### Example 1: Button Detection

```
My interpretation:

This looks like a PRIMARY BUTTON.

Based on what I see:
- Prominent placement at bottom of form
- Bright blue background (primary color)
- White text saying "Save Profile"
- Located after all form fields

I think this "Save Profile Button":
- Saves the form data to the database
- Updates the user's profile information
- Shows loading state during save
- Navigates to profile view on success

Does this match your intent?
```

---

### Example 2: Text Detection

```
✓ TEXT ELEMENT DETECTED

I see horizontal line pairs in the sketch - this is text content.

Quick Detection:
- 3 line pairs → 3 lines of text
- Routing to text analysis for detailed specification...

→ Loading text-specific instructions...

Text Analysis from Sketch:
- 3 lines of text (3 horizontal bar groups)
- Line thickness: 2px → ~20-24px font size
- Line spacing: 2px between lines → ~1.4 line-height
- Alignment: Left
- Content capacity: ~150-180 characters (50-60 per line)
```

---

### Example 3: Complex Component

```
🔍 Complex Component Detected

I see this "Booking Calendar" has multiple states and interactions.

Complexity Indicators I Found:
- Time-based interactions (selecting dates)
- Multiple states (available, booked, selected, disabled)
- Business rules (booking validation, date constraints)
- Cross-component sync (updates booking summary)

To keep this manageable, I'll help you separate:
1. Page Context - Where it appears, size, position
2. Visual Design - How each state looks (for Figma)
3. Functional Logic - How it behaves, business rules

Shall we decompose this component?
```

---

## KEY PRINCIPLES

**Trust-the-Agent Approach:**
- Agent interprets, user confirms
- Not procedural checkbox selection
- Demonstrates intelligence and reasoning

**Text Detection Priority:**
- Always check for text first
- Horizontal line pairs = text content
- Prevents misclassification

**Complexity Routing:**
- Simple components stay in page
- Complex components get decomposed
- Enables modular architecture

**Context-Aware:**
- Understands form flow
- Recognizes UI patterns
- Applies common sense

---

## INTEGRATION

### Within Page Specification Workflow

**Called from:** `page-specification/steps-c/4c-03-document-section.md`

**Flow:**
1. Designer working on section specification
2. Agent encounters object in sketch
3. Loads object router
4. Detects type and routes
5. Completes specification
6. Returns to section documentation

---

### With Modular Architecture

**Simple components:**
- Documented inline in page specification
- No separate component file needed

**Complex components:**
- Routed through Complexity Router
- Creates feature folder structure
- Enables three-tier architecture
- See: `modular-architecture/` workflow

---

## COMPLEXITY ROUTER

**[COMPLEXITY-ROUTER.md](COMPLEXITY-ROUTER.md)**

Provides decomposition coaching for complex components.

**Features:**
- Detects complexity indicators
- Guides three-tier separation:
  - Page context (where it appears)
  - Visual design (how it looks)
  - Functional logic (how it behaves)
- Creates feature folder structure
- Maintains modular architecture

**Use when:** Component has multiple states, business rules, or complex interactions

---

## TROUBLESHOOTING

### "Agent misidentified the object"

**Solution:** User provides clarification at confirmation step
- Choice 2: "Close but let me clarify"
- Choice 3: "No, it's actually something different"

Agent adjusts interpretation and proceeds.

---

### "Text not detected"

**Check:** Are there horizontal line PAIRS?
- Single lines = decorative elements
- Line pairs = text markers

**Reference:** [TEXT-DETECTION-PRIORITY.md](TEXT-DETECTION-PRIORITY.md)

---

### "Component seems complex but agent didn't route to decomposition"

**Solution:** Agent may have classified as simple
- User can request decomposition manually
- Or continue with inline documentation if preferred

**Note:** Complexity routing is a suggestion, not mandatory

---

## FILES REFERENCE

### Router Files

- **[object-router.md](object-router.md)** - Main routing logic
- **[COMPLEXITY-ROUTER.md](COMPLEXITY-ROUTER.md)** - Complexity assessment and coaching
- **[ROUTER-FLOW-DIAGRAM.md](ROUTER-FLOW-DIAGRAM.md)** - Visual flow documentation
- **[TEXT-DETECTION-PRIORITY.md](TEXT-DETECTION-PRIORITY.md)** - Text detection rules

### Object Templates

All templates in [templates/](templates/) folder:
- button.md
- heading-text.md
- text-input.md
- image.md
- link.md
- [Additional types referenced but not yet created]

---

## NOTES

**This is routing infrastructure** - not a user-facing workflow.

**Used automatically** within page specification process when encountering objects in sketches.

**Enables:**
- Consistent object specification
- Intelligent type detection
- Proper complexity routing
- Modular architecture support

---

_Object Type Router - Intelligent detection, proper routing_
