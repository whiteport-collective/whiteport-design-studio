# Page Specification Quality Workflow - Automated Execution

**Purpose:** Ensure every page specification follows WDS standards with complete structure, Object IDs, and traceability.

**For Freya (AI Agent):** This file provides automated workflow execution instructions.

---

## Automated Workflow Execution

<action>Load and execute: workflow.md</action>

This will initialize the BMAD v6 micro-step workflow architecture and guide you through all 8 validation steps sequentially.

---

## Workflow Architecture

This workflow follows **BMAD v6 step-file architecture**:

- **8 Sequential Steps** - Each step is a self-contained validation check
- **Just-In-Time Loading** - Only current step in memory
- **Diagnostic Reporting** - Identify issues, suggest fixes, let designer decide
- **State Tracking** - Track validation progress through steps

---

## Reference Documentation

- **workflow.md** - Main entry point and workflow architecture
- **quality-guide.md** - Overview reference of all checks and why they matter
- **steps-v/** - Individual validation step files (step-01 through step-08)
