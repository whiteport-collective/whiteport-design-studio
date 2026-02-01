---
nextStepFile: './step-03-page-overview.md'
---

# Step 2: Validate Navigation Structure

## Purpose

Verify that page specification has proper navigation structure with H3 header, dual "Next Step" links, embedded sketch, and H1 page title.

## Context for Agent

Navigation structure provides immediate context for where the page fits in the user journey. Consistent navigation enables automated tooling, cross-linking, and ensures designers can quickly navigate between related pages. Embedded sketch gives visual reference without leaving the document.

## Key Elements

This step validates:
- H3 header with page number and name
- "Next Step" link before sketch (pointing to next page)
- Embedded sketch image with proper path
- "Next Step" link after sketch (same as first link)
- H1 page title matching H3
- Correct relative paths to adjacent pages
- Page number consistency across all elements

## Instructions

Check navigation section at top of document. Verify H3 and H1 headers match and include correct page numbers. Confirm dual "Next Step" links exist (before and after sketch) and point to correct adjacent pages using relative paths.

Verify embedded sketch image exists and path is correct (typically `Sketches/[page-number]-[page-name]_[viewport].jpg`).

If navigation structure is missing or incomplete, report as CRITICAL. If links are broken or paths incorrect, report as WARNING.

Generate diagnostic report showing what's missing, incorrect paths, and provide example of correct navigation structure.

## Next Step

After validating navigation structure, proceed to step-03-page-overview.md

## Validation Checklist

```yaml
navigation_validated:
  h3_header_present: [true/false]
  h1_header_present: [true/false]
  headers_match: [true/false]
  page_numbers_consistent: [true/false]
  next_step_before_sketch: [true/false]
  next_step_after_sketch: [true/false]
  links_match: [true/false]
  sketch_embedded: [true/false]
  paths_valid: [true/false]
  status: [pass/warning/critical]
```
