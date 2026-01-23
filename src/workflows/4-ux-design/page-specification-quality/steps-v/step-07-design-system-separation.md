---
nextStepFile: './step-08-final-validation.md'
---

# Step 7: Validate Design System Separation & Unnecessary Information

## Purpose

Verify that page specification focuses on strategic design intent without CSS implementation details, and contains no unnecessary information like code snippets, version control notes, or duplicate content.

## Context for Agent

Page specs focus on WHAT/WHY (strategic), not HOW (implementation). Design System is the single source of truth for styling. Mixing CSS details into page specs causes maintenance nightmares when styles change. Unnecessary information clutters specs and confuses developers about what's actually required.

## Key Elements - Design System Separation

This step validates NO presence of:
- CSS classes, hex codes, or color values
- Font sizes, padding, margins, or layout measurements
- Styling implementation details
- Component references properly link to Design System
- Color/typography references use Design System tokens

## Key Elements - Unnecessary Information

This step validates NO presence of:
- Implementation code snippets (HTML, CSS, JavaScript)
- Developer instructions or technical setup steps
- Version control information (commit messages, PR notes)
- Internal project management notes
- Duplicate content across sections
- Outdated/deprecated information
- Design iteration history

## Instructions

Scan entire document for CSS implementation details (hex codes like #FF5733, pixel values like 16px, CSS classes like .button-primary, font specifications like font-size: 14px). Report each occurrence with line numbers.

Check for code snippets in fenced code blocks, developer setup instructions, git commit references, duplicate sketches or content, and outdated notes.

If CSS details found, report as CRITICAL. If unnecessary information found, report as WARNING.

Generate diagnostic report showing all violations with line numbers, explain why each is problematic, and provide recommendations for where information should live instead (Design System for styling, separate docs for setup, etc.).

## Next Step

After validating design system separation, proceed to step-08-final-validation.md

## Validation Checklist

```yaml
design_system_separation_validated:
  no_css_classes: [true/false]
  no_hex_codes: [true/false]
  no_pixel_values: [true/false]
  no_styling_details: [true/false]
  component_references_present: [true/false]
  design_system_tokens_used: [true/false]
  no_code_snippets: [true/false]
  no_version_control_info: [true/false]
  no_duplicate_content: [true/false]
  no_outdated_information: [true/false]
  status: [pass/warning/critical]
```
