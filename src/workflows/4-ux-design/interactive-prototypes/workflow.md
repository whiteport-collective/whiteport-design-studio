---
name: Interactive Prototypes
description: Create production-ready interactive prototypes using phased section-by-section implementation
web_bundle: true
---

# Interactive Prototypes Workflow

**Goal:** Build self-contained, production-ready interactive prototypes from UX specifications

**Your Role:** Implementation facilitator guiding section-by-section prototype development with approval gates

---

## OVERVIEW

This workflow creates interactive prototypes using:
- ✅ Tailwind CSS (no separate CSS files)
- ✅ Vanilla JavaScript (components in shared folders)
- ✅ Section-by-section implementation (approval gates)
- ✅ Just-in-time story files (created as needed)
- ✅ Demo data auto-loading

**Note:** We use "scenario step" instead of "page" - a step can be a full page, modal, overlay, state change, or any UI change requiring a new sketch.

---

## WHEN TO USE

Use this workflow when:
- ✅ Page specifications are complete and approved
- ✅ Ready to build working interactive prototypes
- ✅ Need production-ready HTML/CSS/JS implementations
- ✅ Want iterative development with approval gates

Skip this workflow when:
- ❌ Specifications not complete yet
- ❌ Still in sketching or wireframe phase
- ❌ Using different prototyping tools (Figma, Adobe XD)
- ❌ Building final production code (this is prototype stage)

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
- [INTERACTIVE-PROTOTYPES-GUIDE.md](guides/INTERACTIVE-PROTOTYPES-GUIDE.md) - Overview and methodology
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

This workflow creates **prototypes**, not final production code. The code is production-ready quality but intended for:
- Stakeholder demos
- User testing
- Design validation
- Developer handoff reference

Final production code will be built in development phase using proper frameworks and architecture.

---

_Interactive Prototypes - Section-by-section implementation with approval gates_
