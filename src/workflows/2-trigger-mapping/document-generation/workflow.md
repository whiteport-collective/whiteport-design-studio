---
name: Trigger Map Document Generation
description: Generate comprehensive documentation from trigger map YAML data
web_bundle: true
---

# Trigger Map Document Generation Workflow

**Goal:** Transform trigger map YAML data into comprehensive markdown documentation

**Your Role:** Automated document generator that systematically creates hub, business goals, persona, and insights documents from trigger map data.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file is in memory
- **Sequential Enforcement**: Steps must be completed in order
- **Automated Generation**: No user interaction during document generation
- **Quality Validation**: Final step validates generated documents

### Step Processing Rules

1. **READ COMPLETELY**: Always read entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all sections in order, never deviate
3. **AUTO-PROCEED**: Generate documents without waiting for user input
4. **LOAD NEXT**: When directed, load, read entire file, then execute next step

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 🎯 **ALWAYS** follow the exact instructions in step file
- 🤖 **ALWAYS** auto-proceed through document generation

---

## INITIALIZATION SEQUENCE

### 1. Input Requirement

**Required:** Trigger map YAML file path
- User must provide path to trigger map YAML file
- File must be valid trigger map structure with business goals, platform, target groups, and driving forces

### 2. First Step Execution

Load, read full file and then execute `steps-c/step-01-generate-hub.md` to begin workflow.

---

## OUTPUT

**Generated Documents:**
- Hub document (central navigation for trigger map)
- Business goals documents (one per goal)
- Persona documents (one per target group)
- Key insights document (strategic takeaways)

All documents are cross-linked and follow WDS documentation standards.
