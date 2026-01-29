# Step 6.3: Create Test Scenario

**Goal:** Define how to validate Design Delivery after implementation

---

## Purpose

Create a Test Scenario file that guides validation testing.

This file documents:
- What to test (test objectives)
- Happy path flows
- Error states to verify
- Edge cases to handle
- Design system validation
- Accessibility testing
- Sign-off criteria

---

## Before You Start

**Ensure you have:**

- ✅ Completed step 6.2 (Design Delivery created)
- ✅ Design Delivery file: `deliveries/DD-XXX-name.yaml`
- ✅ Clear understanding of what needs testing

---

## Instructions

Execute the following substeps in sequence to build the Test Scenario file:

### Substep 1: Initialize Test Scenario File

Load, read completely, then execute:
`substeps/6.3-substeps/01-initialize-test-scenario.md`

This substep will:
- Choose test scenario ID (TS-XXX format)
- Copy template
- Fill out basic metadata
- Define test objectives

### Substep 2: Define Happy Path Tests

Load, read completely, then execute:
`substeps/6.3-substeps/02-define-happy-path.md`

This substep will:
- Define main user flow tests
- Document expected results for each step
- Reference design specifications

### Substep 3: Define Error State Tests

Load, read completely, then execute:
`substeps/6.3-substeps/03-define-error-states.md`

This substep will:
- Define error scenario tests
- Document expected error messages
- Verify error handling

### Substep 4: Define Edge Case Tests

Load, read completely, then execute:
`substeps/6.3-substeps/04-define-edge-cases.md`

This substep will:
- Define unusual scenario tests
- Document expected behavior
- Test boundary conditions

### Substep 5: Define Design System Validation

Load, read completely, then execute:
`substeps/6.3-substeps/05-define-design-validation.md`

This substep will:
- List components to validate
- Define token verification (colors, typography, spacing)
- Check component usage

### Substep 6: Define Accessibility Tests

Load, read completely, then execute:
`substeps/6.3-substeps/06-define-accessibility.md`

This substep will:
- Define screen reader tests
- Define color contrast checks
- Define touch target verification
- Define keyboard navigation tests

### Substep 7: Define Sign-Off Criteria

Load, read completely, then execute:
`substeps/6.3-substeps/07-define-signoff-criteria.md`

This substep will:
- Define what "passing" means
- List must-fix vs. nice-to-fix issues
- Set approval thresholds

---

## Critical Rules

- 🛑 **NEVER** load multiple substeps simultaneously
- 📖 **ALWAYS** read entire substep file before execution
- 🚫 **NEVER** skip substeps or optimize the sequence
- 🎯 **ALWAYS** follow the exact instructions in each substep

---

## Validation

Before proceeding, verify:

- [ ] Test scenario ID matches delivery ID
- [ ] All test types are defined
- [ ] Each test has clear expected results
- [ ] Design system validation is complete
- [ ] Accessibility tests are included
- [ ] Sign-off criteria are clear

---

## Next Step

After Test Scenario file is complete:

<output>✅ Test Scenario file created: `test-scenarios/TS-XXX-name.yaml`</output>

<action>Load and execute: step-6.4-handoff-dialog.md</action>

Do NOT skip ahead.

---

## Success Metrics

✅ Test Scenario file created
✅ All test types defined
✅ Expected results documented
✅ Design system validation included
✅ Accessibility tests included
✅ Sign-off criteria clear

---

**Remember:** Test Scenarios ensure design intent is preserved in implementation. Be comprehensive!
