# Step 3.5: Generate Signoff Document (Optional)

## Purpose

Offer to create a formal signoff document based on the accepted pitch - contract, service agreement, or internal signoff depending on context.

---

## Context for Agent

**After the pitch is accepted by stakeholders**, you'll offer to create a signoff document to formalize the commitment. This step routes to substeps that handle the document generation process.

**Key Principle**: The pitch got everyone aligned. The signoff document secures the commitment before starting work.

---

## Instructions

Execute the following substeps in sequence to handle signoff document generation:

### Substep 1: Offer Signoff Document

Load, read completely, then execute:
`substeps/04-generate-signoff/20-offer-signoff-document.md`

This substep will:
- Present document type options (contract, service agreement, internal signoff, or skip)
- Gather user's choice
- Route based on selection

### Substep 2: Determine Business Model (if contract/service agreement selected)

If user chose to create a signoff document, load, read completely, then execute:
`substeps/04-generate-signoff/21-determine-business-model.md`

This substep will:
- Ask about business model (fixed price, time & materials, retainer, or hourly)
- Configure sections based on model

### Substeps 3-14: Build Contract Sections (if contract selected)

If user chose contract or service agreement, execute substeps 22-33 in sequence:

1. `substeps/05-build-contract/22-build-section-01-project-overview.md`
2. `substeps/05-build-contract/23-build-section-02-business-model.md`
3. `substeps/05-build-contract/24-build-section-03-scope-of-work.md`
4. `substeps/05-build-contract/25-build-section-04-payment-terms.md`
5. `substeps/05-build-contract/26-build-section-05-timeline.md`
6. `substeps/05-build-contract/27-build-section-06-availability.md`
7. `substeps/05-build-contract/28-build-section-07-confidentiality.md`
8. `substeps/05-build-contract/29-build-section-08-not-to-exceed.md`
9. `substeps/05-build-contract/30-build-section-09-work-initiation.md`
10. `substeps/05-build-contract/31-build-section-10-terms-and-conditions.md`
11. `substeps/05-build-contract/32-build-section-11-approval.md`
12. `substeps/05-build-contract/33-finalize-contract.md`

### Internal Signoff Document (if internal signoff selected)

If user chose internal signoff, execute substeps 34-35:

1. `substeps/06-build-signoff-internal/34-build-internal-signoff.md`
2. `substeps/06-build-signoff-internal/35-finalize-internal-signoff.md`

---

## If User Chooses "Skip"

If user skips signoff document creation:
- Acknowledge: "No problem! The pitch document is ready to share. You can always generate a signoff document later if needed."
- Proceed directly to step-04-present-for-approval.md

---

## Critical Rules

- 🛑 **NEVER** load multiple substeps simultaneously
- 📖 **ALWAYS** read entire substep file before execution
- 🚫 **NEVER** skip substeps or optimize the sequence
- 🎯 **ALWAYS** follow the exact instructions in each substep
- ⏸️ **ALWAYS** halt at menus and wait for user input

---

## Next Step

After signoff document generation is complete (or skipped):
→ `step-04-present-for-approval.md`
