---
nextStepFile: './step-06-object-registry.md'
---

# Step 5: Validate Section Order & Structure

## Purpose

Verify that page specification sections appear in standard WDS order with all required sections present and no duplicate or redundant sections.

## Context for Agent

Consistent section order makes specifications predictable and scannable. Developers and stakeholders know exactly where to find information. Standard order also enables automated tooling and ensures nothing is forgotten.

## Key Elements

This step validates:
- Sections appear in standard WDS order
- All required sections are present
- Optional sections are appropriately placed
- No duplicate sections
- No redundant or orphaned content

## Standard Section Order

1. Page Metadata
2. Navigation (H3 + Next Step + Sketch + Next Step + H1)
3. Page description paragraph
4. User Situation
5. Page Purpose
6. Page Sections
7. Object Registry
8. Reference Materials (optional)
9. Technical Notes (optional)
10. Development Checklist (optional)

## Instructions

Scan document structure and compare against standard section order. Identify sections that are out of order, missing required sections, or duplicate sections.

If required sections are missing, report as CRITICAL. If sections are out of order or duplicated, report as WARNING.

Generate diagnostic report showing current section order vs expected order, missing sections, and duplicates. Provide recommendation for correct ordering.

## Next Step

After validating section order, proceed to step-06-object-registry.md

## Validation Checklist

```yaml
section_order_validated:
  follows_standard_order: [true/false]
  all_required_sections_present: [true/false]
  no_duplicate_sections: [true/false]
  no_orphaned_content: [true/false]
  optional_sections_appropriate: [true/false]
  status: [pass/warning/critical]
```
