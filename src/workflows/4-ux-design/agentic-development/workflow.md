---
name: Agentic Development
description: AI-assisted development for non-technical designers using Agent Dialogs and structured collaboration
web_bundle: true
---

# Agentic Development Workflow

**Goal:** Enable non-technical designers to build production-ready code through structured AI collaboration

**Your Role:** Implementation partner guiding step-by-step development with clear feedback protocols and approval gates

---

## OVERVIEW

Agentic Development is about **how** you work with AI — not **what** you build.

Use this workflow to build a prototype, extend a production app, create a new feature, or anything else. The AI handles implementation while you focus on what to build and how it should behave.

This workflow enables:
- ✅ Direct implementation from specifications
- ✅ Step-by-step development with approval gates
- ✅ Clear feedback protocol with timing guidance
- ✅ Agent Dialog structure for context and handoff
- ✅ Dynamic planning that adapts as we learn

**Note:** We use "scenario step" instead of "page" - a step can be a full page, modal, overlay, state change, or any UI change requiring a new sketch.

---

## WHEN TO USE

Use this workflow when:
- ✅ Page specifications are complete and approved
- ✅ Ready to build working implementations
- ✅ Working with AI to develop production-ready code
- ✅ Want iterative development with approval gates
- ✅ Need structured collaboration with clear feedback handling

Skip this workflow when:
- ❌ Specifications not complete yet
- ❌ Still in sketching or wireframe phase
- ❌ Simple one-file changes that don't need documentation
- ❌ Pure exploration where the path is unclear

---

## USER FEEDBACK PROTOCOL

During development, the designer provides feedback. **CRITICAL: Never implement feedback without first classifying it and stating when it should be addressed.**

### Feedback Types

| Type | What It Is | When to Address |
|------|------------|-----------------|
| **Bug/Issue** | Something broken, error, not working | Now — fix immediately, iterate until resolved |
| **Quick Adjustment** | Small tweak, change X to Y | Now — implement immediately |
| **Addition** | New requirement that fits current dialog | Later step — add to plan |
| **Change Request** | Outside current dialog scope | Future session — document in Change Requests |

### The 2-Minute Rule (GTD)

**If a fix takes less than 2 minutes, do it immediately.**

From David Allen's "Getting Things Done": planning overhead should not exceed task complexity. See [GTD Model](../../../docs/models/gtd-getting-things-done.md).

| Situation | Action |
|-----------|--------|
| Missing condition check | Fix now, log as sub-step |
| Wrong variable name | Fix now, log as sub-step |
| Needs new component | Add to plan |
| Architectural change | Add to plan |

**Pattern:** Do the fix → Log as sub-step (e.g., 20a-1) → Continue main task

### Response Flow

**When user reports something:**

1. **CLASSIFY** — What type of feedback is this?
2. **TIMING** — When should it be addressed?
3. **DOCUMENT** — For bugs, add to plan BEFORE fixing
4. **CONFIRM** — For additions and change requests, confirm before proceeding
5. **EXECUTE** — Implement or document as appropriate

### Bug/Issue (Document First, Then Fix)

**User says:** "This is broken" / "Error occurred" / "Not working"

**Agent response:**
```
This is a bug — [brief description of issue].
Let's call it 10A and let me add it to the plan, then fix it.
```

**Required sequence:**
1. **Identify** — Understand and describe the bug clearly
2. **Document** — Add to dialog plan as sub-step (e.g., 21a, 21b)
3. **Execute** — Fix and iterate until resolved
4. **Log** — Record resolution in progress log

**If user reports multiple issues at once:**
1. Identify and list each issue separately
2. Add ALL to the plan first
3. Then work through them one by one

**Why document first:** Bugs discovered during implementation are valuable context. Recording them ensures traceability, prevents forgotten fixes, and creates a clear record for handoff.

**Example:**
```
User: "The drawer appears behind the overlay and the reassign doesn't work"

Agent: "I see two issues:
        1. Drawer z-index (appears behind overlay)
        2. Reassign not working

        Let me add both to the plan as 21a and 21b, then fix them."
```

### Quick Adjustment (Fix Now)

**User says:** "Change X to Y" / "Make this button go here" / "Use different color"

**Agent response:**
```
Quick adjustment — I'll implement this now.
```

Then implement the change.

### Addition (Add to Plan)

**User says:** "We should also add X" / "Don't forget to handle Y"

**Agent response:**
```
This is an addition that fits the current dialog.
I'll add it to Step {N} for later. Confirm?
```

Then add to the appropriate step or To Do section in the dialog file.

### Change Request (Document for Later)

**User says:** "The profile button should go to /family" / "We need a settings page"

**Agent response:**
```
This is outside the current dialog scope.
It doesn't block {feature name}.

I'll add it to Change Requests for a future session. Confirm?
```

**WAIT for user confirmation.**

If user confirms → Add to Change Requests section
If user says "do it now" → Treat as quick adjustment and implement

### Anti-Pattern: What NOT to Do

**NEVER do this:**

User: "The profile button should go to /family"
Agent: *immediately edits the file*

**ALWAYS do this:**

User: "The profile button should go to /family"
Agent: "This is outside current scope. I'll add it to Change Requests. Confirm?"
User: "Yes" or "No, do it now"
*then acts accordingly*

### Why This Matters

From experience, skipping the classify-and-timing step leads to:
- Agent implementing things the user didn't want
- User frustration from lack of visibility
- Lost context when user wanted to discuss first
- Scope creep pulling focus from current implementation

The extra seconds to classify and confirm build trust and ensure alignment.

---

## SESSION START PROTOCOL

When starting or resuming a session, **always follow this sequence before implementing anything:**

### 1. Read the Dialog Document

```
Agent: "Let me read the dialog document to understand where we are."
```

Read the dialog file completely to understand:
- What steps are done
- What steps remain
- Any blockers or change requests
- Current context and decisions

### 2. Verify Plan Against Reality

**The plan may be outdated.** Check if:
- Steps marked "To Do" have actually been implemented
- Steps marked "Done" are truly complete
- The numbering is sequential and accurate

```
Agent: "I see steps 11-18 in To Do, but let me check the code..."
Agent: "These are already implemented. Let me update the plan."
```

If the plan is outdated → Update it before proceeding.

### 3. Present Current Status

Summarize for the designer:
- What's done (with step numbers)
- What's remaining (with step numbers)
- Any change requests pending

```
Agent: "Here's where we are:
        Done: Steps 9b, 10, 11-19
        To Do: Steps 20, 21
        Ready to continue?"
```

### 4. Before Implementing a Step

**Always check the specification/sketches first:**

```
Agent: "Before implementing step 20, let me check the sketches..."
Agent: "I see this requires a nested drawer pattern, not inline buttons.
        Should I break this into sub-steps?"
```

This prevents building the wrong thing and wasting effort.

### Why This Matters

Sessions can be interrupted. Context can be lost. The dialog document survives — but only if it's kept accurate. This protocol ensures:
- No duplicate work (re-implementing what exists)
- No missed work (skipping what's actually needed)
- Correct understanding of requirements before implementation

---

## EXECUTION PRINCIPLES

### Document Before Acting

**Every decision, action, and problem must be documented in the dialog file BEFORE acting on it.**

This ensures:
- Full traceability of what was decided and why
- Clean handoff if context is lost or session changes
- The dialog document is always the source of truth for progress

### Sketch Fidelity

**Implement code as close to the provided sketches as possible.**

Sketches are intentional design decisions, not loose suggestions. Text sizes, proportions, spacing, and layout choices are made for a reason:

| Element | Approach |
|---------|----------|
| **Text sizes** | Match relative sizes in sketch (headings vs body vs labels) |
| **Proportions** | Preserve ratios between elements |
| **Spacing** | Maintain visual rhythm and whitespace |
| **Layout** | Follow the arrangement precisely |
| **Component style** | Match the visual pattern (pills, cards, buttons) |

**When in doubt:**
1. Ask the designer for clarification
2. Reference the sketch directly in your question
3. Don't assume "close enough" is acceptable

**If constraints make exact matching impossible** (e.g., responsive behavior, platform limitations), document the deviation and explain why.

### Sub-Steps During Execution

While working on a step, you may discover additional tasks needed. Add these as sub-steps:

```markdown
| # | Section | Status | Notes |
|---|---------|--------|-------|
| 14 | Book It Button | ✅ | Complete |
| 14a | Fix button alignment | ✅ | Added during 14 |
| 14b | Add loading state | ✅ | Added during 14 |
| 15 | Cancel Button | 🔄 | In progress |
```

Sub-steps use letter suffixes (14a, 14b) to maintain the parent step's position.

### Dynamic Planning After Step Completion

**After completing each step, review and adjust the plan:**

1. **Review remaining steps** — Are they still accurate?
2. **Shuffle if needed** — Reorder based on what we learned
3. **Add new steps** — If implementation revealed new requirements
4. **Remove steps** — If no longer needed
5. **Update the dialog file** — Document the changes

**Numbering Rules:**
- **Completed steps:** Fixed numbering (never renumber)
- **Future steps:** Dynamic numbering (can change)

Example:
```markdown
### Done
| 9b | Carousel Refactor | ✅ |        ← Fixed, never changes
| 10 | Deep Linking | ✅ |              ← Fixed

### To Do
| 11 | Wire up handlers | 🔲 |         ← Can be renumbered
| 12 | Add poop toggle | 🔲 |          ← Can be removed or moved
| 13 | NEW: Error states | 🔲 |        ← Can be inserted
```

### Handoff Always References Dialog

**Any handoff — to a new session, new agent, or human — MUST reference the dialog document.**

The dialog document is the single source of truth for:
- What has been done
- What decisions were made
- What remains to be done
- Any issues or blockers

Never hand off by describing the task verbally. Always point to the dialog.

### Plan-then-Execute Pattern

**Separate planning from execution into distinct sessions.**

Context windows are finite. Long sessions accumulate noise and risk context loss mid-implementation. The solution: end planning sessions deliberately, start execution sessions fresh.

**Planning Session:**
1. Explore the codebase and requirements
2. Discuss approach with the designer
3. Write the plan to the dialog file
4. End with a clear handoff: *"The plan is documented. Hasta la vista!"*

**Execution Session:**
1. Start fresh (new conversation)
2. Read the product brief for overall context
3. Read the page specification for requirements
4. Read the dialog document to understand the plan and progress
5. Execute the steps one by one

**Why This Works:**
- Fresh context window for execution = maximum working memory
- Dialog document carries all decisions and context forward
- No risk of context loss mid-implementation
- Each session has a clear, focused purpose

**When to Split:**
- After complex exploration or analysis
- When the plan is complete and approved
- When current session is getting long
- Before starting a major implementation phase

**The Dialog is the Bridge:**
```
┌─────────────────────┐    Dialog    ┌─────────────────────┐
│  PLANNING SESSION   │─────File────▶│ EXECUTION SESSION   │
│                     │              │                     │
│ • Explore codebase  │              │ • Fresh context     │
│ • Discuss approach  │              │ • Read brief + spec │
│ • Write plan        │              │ • Read dialog       │
│ • "Hasta la vista!" │              │ • Execute steps     │
└─────────────────────┘              └─────────────────────┘
```

---

## WORKFLOW ARCHITECTURE

This uses **multi-phase architecture** with iterative loops:

### Phase Structure

**Sequential Phases (1-3, 5):** Setup → Analysis → Selection → Finalization

**Iterative Phase (4):** Section implementation loop with 7 micro-tasks

### Critical Rules

- 🎯 **ALWAYS** complete Phase 1 setup before starting
- 📊 **ALWAYS** analyze scenario before selecting views
- 🔁 **ALWAYS** use section-by-section approach (Phase 4 loop)
- ✅ **ALWAYS** get approval before moving to next section
- 📝 **ALWAYS** create story files just-in-time (not upfront)

---

## THE 5 PHASES

### Phase 1: Prototype Setup
**When:** Starting new scenario prototype (one-time per scenario)

**What:** Set up prototype environment and folder structure

**Creates:**
- Prototype folder with complete structure
- Demo data files
- Roadmap document
- All working folders (work/, stories/, shared/, components/, etc.)

**Go to:** [steps-c/1-prototype-setup.md](steps-c/1-prototype-setup.md)

---

### Phase 2: Scenario Analysis
**When:** Setup complete, ready to start building (one-time per scenario)

**What:** Analyze all scenario steps and identify logical views

**Creates:**
- Logical View Map (maps steps to views)
- View identification and relationships

**Go to:** [steps-c/2-scenario-analysis.md](steps-c/2-scenario-analysis.md)

---

### Phase 3: Logical View Selection & Breakdown
**When:** User selects which logical view to build (per view)

**What:** Identify all objects and break view into sections

**Creates:**
- Work file with section breakdown
- Implementation sequence

**Go to:** [steps-c/3-logical-view-breakdown.md](steps-c/3-logical-view-breakdown.md)

---

### Phase 4: Section Story & Implementation Loop
**When:** Ready to build sections (iterative per section)

**What:** For each section - prepare, create story, implement, test, handle feedback, approve

**The 7 Micro-Tasks:**

1. **[4a: Announce & Gather](steps-c/4a-announce-and-gather.md)**
   - Announce section and gather requirements

2. **[4b: Create Story File](steps-c/4b-create-story-file.md)**
   - Create focused story file for this section

3. **[4c: Implement Section](steps-c/4c-implement-section.md)**
   - Implement code following story

4. **[4d: Present for Testing](steps-c/4d-present-for-testing.md)**
   - Present to user with test instructions

5. **[4e: Handle Issue](steps-c/4e-handle-issue.md)**
   - Fix issues if user reports problems (loop back to 4d)

6. **[4f: Handle Improvement](steps-c/4f-handle-improvement.md)**
   - Implement improvements if user suggests (loop back to 4d)

7. **[4g: Section Approved](steps-c/4g-section-approved.md)**
   - Finalize approval and move to next section (back to 4a)

**Flow:** 4a → 4b → 4c → 4d → [4e or 4f if needed, loops to 4d] → 4g → [back to 4a for next section]

**Creates (per section):**
- Story file (just-in-time)
- Incremental updates to view HTML
- Learnings captured

**Key:** One clear task per file → No confusion → Linear execution → Better results!

---

### Phase 5: Finalization
**When:** All sections complete for a logical view (end of view)

**What:** Integration test all states and final approval

**Result:** Production-ready logical view handling all its states

**Go to:** [steps-c/5-finalization.md](steps-c/5-finalization.md)

---

## INITIALIZATION

### Guide References

**Process Guides:**
- [AGENTIC-DEVELOPMENT-GUIDE.md](guides/AGENTIC-DEVELOPMENT-GUIDE.md) - Overview and methodology
- [CREATION-GUIDE.md](guides/CREATION-GUIDE.md) - Technical implementation details
- [PROTOTYPE-INITIATION-DIALOG.md](guides/PROTOTYPE-INITIATION-DIALOG.md) - Conversation scripts
- [PROTOTYPE-ANALYSIS.md](guides/PROTOTYPE-ANALYSIS.md) - Quality standards
- [FILE-INDEX.md](guides/FILE-INDEX.md) - Complete file reference

**Templates:**
- templates/work-file-template.yaml
- templates/story-file-template.md
- templates/page-template.html
- templates/components/dev-mode.*

### First Step Execution

Load, read and execute `steps-c/1-prototype-setup.md` to begin workflow.

---

## OUTPUT

**Per Scenario:**
```
[Scenario-Number]-[Scenario-Name]-Prototype/
├── [View].html files (in root, one per logical view)
├── shared/ (ONE COPY of shared code)
├── components/ (ONE COPY of reusable components)
├── pages/ (page-specific scripts if complex)
├── data/ (demo data JSON files)
├── stories/ (section development files - created just-in-time)
├── work/ (planning files)
└── PROTOTYPE-ROADMAP.md
```

**Result:** Self-contained, production-ready interactive prototypes with:
- Clean HTML using Tailwind CSS
- Vanilla JavaScript components
- Demo data auto-loading
- All states implemented and tested

---

## PROTOTYPE FOLDER STRUCTURE

```
[Scenario-Number]-[Scenario-Name]-Prototype/
├── [Page].html files         ← Logical view HTML files (root)
├── shared/                    ← ONE COPY of shared code
├── components/                ← ONE COPY of reusable components
├── pages/                     ← Page-specific scripts (if complex)
├── data/                      ← Demo data JSON files
├── stories/                   ← Section development files (JIT)
├── work/                      ← Planning files
│   ├── Logical-View-Map.md   ← Maps steps to views
│   └── [View]-Work.yaml      ← Section breakdowns per view
└── PROTOTYPE-ROADMAP.md      ← Overall roadmap
```

---

## ITERATIVE WORKFLOW

**Phase 1-2:** One-time setup and analysis per scenario

**Phase 3:** Repeat for each logical view in scenario

**Phase 4:** Repeat for each section in current view
- Inner loop: Repeat 4d-4e-4f until approved

**Phase 5:** Repeat for each logical view (finalization)

**Pattern:**
```
Setup → Analysis → [View Selection → [Section Loop*] → Finalization]*
```

---

## EXAMPLES

**Typical Scenarios:**

1. **E-commerce Checkout:** 5 views (cart, shipping, payment, review, confirmation)
2. **SaaS Onboarding:** 4 views (signup, profile, preferences, dashboard)
3. **Booking System:** 6 views (search, select, details, confirm, payment, confirmation)

Each view breaks into 3-8 sections depending on complexity.

---

## QUALITY PRINCIPLES

**Section-by-Section Approval:** Never implement entire view at once - break into sections with approval gates

**Just-In-Time Stories:** Create story files only when needed (4b), not upfront

**Incremental Implementation:** Each section builds on previous approved sections

**Demo Data:** Use realistic demo data for testing and validation

**Self-Contained:** Each prototype folder is complete and portable

---

## TROUBLESHOOTING

**Issue:** User feedback requires rework
**Solution:** Use Phase 4e (issues) or 4f (improvements) to handle, then loop back to 4d

**Issue:** Section too complex
**Solution:** Break down further in Phase 3 before starting Phase 4

**Issue:** Logical view unclear
**Solution:** Revisit Phase 2 analysis to refine view mapping

---

## NOTES

This workflow enables **non-technical designers to build with AI** — whether that's:
- A quick prototype for user testing
- New features in an existing production app
- A complete application from scratch

The methodology stays the same:
- Step-by-step with approval gates
- Clear feedback protocol ensures alignment
- Agent Dialogs provide structure and traceability
- AI handles implementation, designer focuses on what and how

---

_Agentic Development - AI-assisted development for non-technical designers_
