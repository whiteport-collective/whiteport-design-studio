---
nextStepFile: './step-05-section-order.md'
---

# Step 4: Validate Page Sections

## Purpose

Verify that page specification has properly structured Page Sections with Object IDs, component references, and behavior specifications.

## Context for Agent

Page Sections define the actual UI components and their behavior. Object IDs enable traceability from spec → code → Figma. Component references ensure design system consistency. Behavior specs reduce developer guesswork. This is the core implementation guidance section.

## Key Elements

This step validates:
- "## Page Sections" header present
- Section Objects (H3) with clear purpose statements
- Component specs (H4) with Object IDs in format `OBJECT ID: object-name`
- Design system component references
- Content specifications for each component
- Behavior specifications (interactions, states, validation)
- Proper hierarchy (H3 for sections, H4 for components)
- **Responsive behavior documentation** (if page metadata declares responsive platform)

## Instructions

Check for "## Page Sections" header. Verify all sections use H3 headers with purpose statements. Confirm all components use H4 headers with Object IDs in correct format.

Validate that components reference design system (links to component docs), specify content clearly, and document behavior/interactions.

**Platform-Specific Validation:**
If Page Metadata declares **Responsive Web Application** or **Primary Viewport: Mobile-first/Desktop-first**, check that responsive behavior is documented for key components (layout changes, navigation patterns, content reflow, viewport-specific interactions).

If Page Sections missing, report as CRITICAL. If Object IDs missing or malformed, report as CRITICAL. If component references or behavior specs missing, report as WARNING. If responsive platform declared but no responsive behavior documented, report as WARNING.

Generate diagnostic report showing missing Object IDs, incorrect formatting, missing component references, missing responsive documentation, and provide examples of correct structure.

## Next Step

After validating page sections, proceed to step-05-section-order.md

## Validation Checklist

```yaml
page_sections_validated:
  page_sections_header_present: [true/false]
  sections_use_h3: [true/false]
  components_use_h4: [true/false]
  all_components_have_object_ids: [true/false]
  object_id_format_correct: [true/false]
  design_system_references_present: [true/false]
  content_specified: [true/false]
  behavior_documented: [true/false]
  responsive_behavior_documented: [true/false/not_applicable]
  status: [pass/warning/critical]
```
