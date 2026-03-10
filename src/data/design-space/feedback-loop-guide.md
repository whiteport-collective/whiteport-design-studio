# Design Feedback Loop Guide

**Purpose:** Teach the Design Space the designer's taste through linked before/after pairs.

**Philosophy:** The feedback loop is a learning process, not a complaint log. Focus on **what works, how we improved, and what the better solution looks like**. The "before" state is just context — the "after" state is the knowledge. A database of solutions is valuable. A database of complaints is not.

**Exceptions:** Usability testing findings and client feedback are captured as-is — including confusion, failure, and frustration. These are diagnostic data, not complaints. A user struggling at a password field is a measurement, not a grievance. The positivity principle applies to agent-designer feedback (the feedback loop), not to raw user research data.

---

## The Learning Process

When the designer requests a change to your work, you are witnessing a **preference signal** — an opportunity to learn what great design looks like for this designer. Capture the improvement.

### Flow

```
Freya creates design
    ↓
Designer reviews → suggests improvement
    ↓
CAPTURE BEFORE (semantic + visual, pattern_type: "rejected")
    ↓
ASK: "What would make this better?"
    ↓
Designer explains (or Freya infers from the direction)
    ↓
Freya applies the improvement
    ↓
CAPTURE AFTER (semantic + visual, pattern_type: "approved")
    ↓
SAVE LINKED PAIR (capture_feedback_pair)
    ↓
Confirm: "Learned: [X approach] works better than [Y] because [reasoning]"
```

---

## When to Trigger

The feedback loop activates when the designer:
- Suggests a direction: "make it more..." or "try something different"
- Refines the design: "move this here" or "use a different color"
- Approves with refinement: "yes, but..." or "almost, just..."
- Redirects the approach: "let's go a different direction with..."

The loop does NOT trigger for:
- Technical corrections ("fix the typo")
- Requirements clarifications ("actually, there should be 4 items, not 3")
- Questions ("what if we added...?" — wait for a decision)

---

## Pattern Types

| Type | When | Example |
|------|------|---------|
| `rejected` | The starting point before improvement | "The centered layout with large heading" |
| `approved` | The improved version (the real knowledge) | "Left-aligned layout with smaller, lighter heading" |
| `delta` | Refinement, not a full redesign | "Same layout, but increased padding by 20px" |
| `conditional` | Works in specific contexts | "Dark hero works for agency sites, not for e-commerce" |

---

## The WHY Question

Ask naturally. Don't interrogate. Vary your phrasing:

### Forward-looking
- "What would make this feel right?"
- "What are you going for?"
- "What does the better version look like?"

### Specific
- "Is it the [layout / color / spacing / hierarchy] we should improve?"
- "Should it be more [open / minimal / bold / warm / structured]?"
- "What part works already — what should we build on?"

### Outcome-oriented
- "What feeling should this create?"
- "When you imagine this done right, what do you see?"

### When the designer gives a direction without explanation
Infer and confirm: "Got it — [X approach] works better here because [your inference]. Right?"

### When the designer can't articulate
That's fine. Capture the improvement: "Improved from [A] to [B] — designer's intuitive direction. The result [describe what's better about it]."

---

## Capture Format

### Before State
Describe the design you proposed:
- **Layout:** structure, alignment, spacing
- **Visual:** colors, typography weight/size, contrast
- **Components:** which elements, their arrangement
- **Feeling:** the intended mood/tone

### Reasoning
The designer's explanation (verbatim if possible) or your inference.

### After State
Describe what was chosen instead:
- Same categories as before
- Note specifically WHAT changed (the delta)

### Example

```
capture_feedback_pair({
  before_description: "Hero section with centered H1 at 48px bold Rubik,
    navy background, full-width with no max-width constraint.
    Large hero felt authoritative but heavy.",
  after_description: "Hero section with centered H1 at 36px light (300) Rubik,
    navy background, max-width 800px. Lighter weight creates elegance
    and breathing room. Same authority, less weight.",
  reasoning: "Bold headings feel corporate and generic. Light weight at
    large sizes is distinctive — Whiteport's identity is confident calm,
    not loud authority.",
  pattern_type_before: "rejected",
  pattern_type_after: "approved",
  project: "whiteport",
  topics: ["typography", "heading-weight", "brand-voice", "elegance"],
  components: ["hero-banner", "heading-h1"]
})
```

---

## Red Flag Pre-Check

**Before presenting ANY new design to the designer:**

```
search_preference_patterns({
  description: "[describe what you're about to show]",
  image_base64: "[screenshot if available]",
  project: "current-project",
  designer: "marten"
})
```

### If matches found:

1. Read the rejected pattern and its approved alternative
2. Adjust your design to align with the known preference
3. Present the adjusted version
4. Mention it: "I adjusted the [aspect] — you've previously preferred [X] over [Y]."

### If no matches:

Proceed normally. The design passes the taste check.

---

## Quality Bar

### Good Feedback Pair
- Before and after are specific (exact values, not vague descriptions)
- Reasoning focuses on **what makes the improvement better** — not what was "wrong"
- Topics and components are tagged for future searchability
- The pair tells a solution story: "Started here → improved to this → because this approach works better for [reason]"

### Bad Feedback Pair
- Framed as complaints ("designer hated this", "this was ugly")
- Vague descriptions ("changed the layout")
- No reasoning about why the new version is better
- Missing tags (unfindable in future searches)

---

## Over Time

As feedback pairs accumulate, the agent develops taste:

**Cold start (0-10 pairs):** Individual solutions. "Light headings work better than bold for this brand."

**Accumulation (10-50 pairs):** Design principles emerge. "Understated elegance works across typography, spacing, and color. Open, breathing layouts outperform dense ones."

**Taste profile (50+ pairs):** The agent anticipates what works. "Based on 47 improvements, the lighter option with more whitespace will work best here."

**Design DNA (100+ pairs):** The Design Space becomes a design sensibility. New agents start with good taste from day one.

---

## Visual Annotation Feedback

The designer can give feedback by **drawing directly on selected elements** — combining element selection with freehand annotation. This bridges the gap between verbal feedback and visual intent.

### How It Works

```
Designer views live page or screenshot
    ↓
Click element to select it (Agentation-style — captures CSS selector, component path)
    ↓
Draw/sketch on the selected element (freehand strokes, arrows, circles, crosses)
    ↓
Agent receives: element identity + annotation image + optional verbal note
    ↓
Agent interprets the combined signal (what element + what the drawing means)
    ↓
Normal feedback loop continues (capture before → apply → capture after)
```

### Annotation Signals

Interpret drawings as design intent:

| Drawing | Likely Intent |
|---------|---------------|
| Circle around element | "Focus here" — this element needs attention |
| X / cross-out | "Remove this" or "this doesn't work" |
| Arrow pointing | "Move this" in the arrow direction |
| Squiggly line / scribble | "This area feels wrong" — ask for clarification |
| Sketch of a shape | "Replace with something like this" |
| Underline | "Emphasize this" or "this text matters" |
| Lines connecting elements | "These should relate" or "align these" |

When the drawing is ambiguous, confirm: "I see you marked [element] with [description]. Are you saying [interpretation]?"

### Element Selection Data

When an element is selected, capture:
- **CSS selector** — exact DOM path for programmatic reference
- **Component name** — if identifiable from source code
- **Visual context** — surrounding elements and layout position
- **Annotation image** — the freehand drawing overlaid on the element

### Integration with Agentation

Agentation provides the click-to-select foundation. The drawing layer extends it:

1. **Agentation** selects the element → structured data (selector, file path, component hierarchy)
2. **Drawing overlay** captures visual intent → annotation image
3. **Combined** → Freya receives precise element + visual feedback in one signal

### Capture Format for Annotated Feedback

```
capture_feedback_pair({
  before_description: "[element] as currently designed: [description]",
  before_image_base64: "[screenshot of element before change]",
  after_description: "[element] after applying annotation feedback: [description]",
  after_image_base64: "[screenshot after change]",
  reasoning: "Designer drew [annotation type] on [element]. Interpreted as: [intent]. Applied: [change].",
  annotation_type: "circle|cross|arrow|sketch|scribble|underline|connection",
  element_selector: "[CSS selector from Agentation]",
  component: "[component name if identified]",
  pattern_type_before: "rejected",
  pattern_type_after: "approved",
  project: "...",
  topics: ["visual-annotation", "..."],
  components: ["..."]
})
```

### When Drawing Feedback Is Most Useful

- **Spatial feedback** — "move this here" is faster drawn than described
- **Proportion feedback** — "make this bigger" with a sketch showing how much
- **Relationship feedback** — arrows showing what connects to what
- **Deletion feedback** — crossing out unwanted elements
- **Layout feedback** — rough sketch of desired arrangement

---

_The feedback loop captures solutions, not complaints. Every "before" is just the setup for a better "after."_
