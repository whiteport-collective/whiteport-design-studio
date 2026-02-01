---
name: Page Specification Quality Workflow
description: Validate WDS page specifications through sequential quality checks
web_bundle: true
---

# Page Specification Quality Workflow

**Goal:** Ensure every WDS page specification meets quality standards with complete structure, Object IDs, and traceability.

**Your Role:** Audit page specifications systematically, diagnose issues, and provide actionable recommendations. Let the designer decide whether to implement fixes.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained validation check that must be followed exactly
- **Just-In-Time Loading**: Only current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Steps must be completed in order, no skipping or optimization allowed
- **Diagnostic Reporting**: Identify issues and suggest fixes, don't automatically rewrite unless asked
- **State Tracking**: Track validation progress through sequential steps

### Step Processing Rules

1. **READ COMPLETELY**: Always read entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If step has a menu with Continue option, only proceed when user selects 'C'
5. **REPORT FINDINGS**: Generate conversational diagnostic reports with line numbers and examples
6. **LOAD NEXT**: When directed, load, read entire file, then execute next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 🎯 **ALWAYS** follow the exact instructions in step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps
- 🔍 **ALWAYS** diagnose and recommend, don't auto-fix unless explicitly asked

---

## WORKFLOW MODES

### Mode 1: New Page Creation ✨
**Use when:** Creating a new page specification from a sketch

**Process:** Run all 8 steps sequentially to build specification correctly from the start.

### Mode 2: Page Update Validation 🔄
**Use when:** Validating changes after sketch updates or content revisions

**Process:** Run relevant steps (typically Steps 4, 6, 8) to validate changes maintain standards.

### Mode 3: Pre-Handoff Quality Audit 🔍
**Use when:** Final quality check before developer handoff

**Process:** Run all 8 steps in validation mode, generate comprehensive quality report.

### Mode 4: Legacy Spec Fix 🛠️
**Use when:** Fixing old specifications that don't follow WDS standards

**Process:** Run all 8 steps, identify all issues, provide prioritized fix recommendations.

---

## INITIALIZATION SEQUENCE

### 1. Determine Workflow Mode

Ask user which mode they need:
- [N] New Page Creation
- [U] Update Validation
- [A] Pre-Handoff Audit
- [L] Legacy Spec Fix

### 2. Load Page Specification

Ask user for the page specification file path to audit.

### 3. First Step Execution

Load, read full file and then execute `steps-v/step-01-page-metadata.md` to begin workflow.

---

## VALIDATION STEPS

```
Step 1: Page Metadata
    ↓
Step 2: Navigation Structure
    ↓
Step 3: Page Overview
    ↓
Step 4: Page Sections & Objects
    ↓
Step 5: Section Order & Structure
    ↓
Step 6: Object Registry
    ↓
Step 7: Design System Separation & Unnecessary Information
    ↓
Step 8: Final Validation
```

---

## OUTPUT FORMAT

Each step generates a diagnostic report following this format:

```markdown
🔍 [Step Name] Audit

**Status:** ✅ PASS / ⚠️ WARNING / ❌ CRITICAL

**Issues Found:**
1. [Issue type] [Description]
   - Location: Line X-Y
   - Current: [what exists now]
   - Should be: [what it should be]
   - Why: [explanation of why this matters]

**Recommendation:**
[Specific actionable fix with examples]

Would you like me to fix this?
```

---

## REFERENCE DOCUMENTATION

- **Quality Guide**: `quality-guide.md` - Overview of all checks and why they matter
- **Page Spec Template**: `../templates/page-specification.template.md`
- **Individual Step Guides**: `step-01-navigation.md` through `step-08-final-validation.md` (legacy, being migrated)

---

**Ready to start? Tell me which mode you need and which page specification to audit.**
