---
nextStepFile: './step-07-design-system-separation.md'
---

# Step 6: Validate Object Registry

## Purpose

Verify that page specification includes complete Object Registry with 100% coverage of all Object IDs defined in Page Sections.

## Context for Agent

Object Registry is the single source of truth for all page elements. It enables automated testing (test by Object ID), facilitates content updates and translations, supports Figma export workflows (aria-label mapping), and ensures complete traceability from spec to code to design.

## Key Elements

This step validates:
- "## Object Registry" header present
- Introduction paragraph explaining registry purpose
- Master Object List table(s) with all Object IDs
- 100% coverage (every Object ID from Page Sections appears in registry)
- Proper table formatting (Object ID | Type | Description)
- No orphaned Object IDs (IDs in registry but not in Page Sections)
- Consistent naming conventions

## Instructions

Check for "## Object Registry" header. Verify introduction paragraph exists. Extract all Object IDs from Page Sections and compare against Object Registry table(s).

Calculate coverage percentage. Identify missing Object IDs (in sections but not in registry) and orphaned Object IDs (in registry but not in sections).

If Object Registry section is missing, report as CRITICAL. If coverage is below 100%, report as CRITICAL. If table formatting is incorrect, report as WARNING.

Generate diagnostic report showing coverage percentage, missing Object IDs, orphaned Object IDs, and provide example of correct registry format.

## Next Step

After validating object registry, proceed to step-07-design-system-separation.md

## Validation Checklist

```yaml
object_registry_validated:
  registry_section_present: [true/false]
  introduction_paragraph_present: [true/false]
  table_properly_formatted: [true/false]
  coverage_percentage: [0-100]
  all_object_ids_registered: [true/false]
  no_orphaned_ids: [true/false]
  naming_conventions_consistent: [true/false]
  status: [pass/warning/critical]
```
