---
nextStepFile: './step-02-navigation.md'
---

# Step 1: Validate Page Metadata

## Purpose

Verify that page specification declares platform, page type, viewport, and interaction model inherited from scenario platform strategy.

## Context for Agent

Page Metadata establishes technical context before any design decisions. Without this section, developers don't know if they're building for mobile-first responsive web, native mobile app, desktop application, or other platforms. This affects every implementation decision.

## Key Elements

This step validates presence and completeness of:
- Platform declaration (from Product Brief/Scenario)
- Page type (Full Page, Modal, Drawer, etc.)
- Primary viewport (Mobile-first, Desktop-first, etc.)
- Interaction model (Touch, Mouse/keyboard, etc.)
- Navigation context (Public, Authenticated, etc.)
- Inheritance reference to scenario platform strategy

## Instructions

Check if Page Metadata section exists immediately after page title and frontmatter. Verify all required fields are present and properly inherited from scenario platform strategy.

If Page Metadata section is missing, report as CRITICAL issue. If section exists but fields are incomplete or don't reference scenario inheritance, report as WARNING.

Generate diagnostic report showing:
- What's missing or incomplete
- Where it should be located (after page title)
- Example of correct Page Metadata section
- Why this matters for developers

If issues found, ask user if they want you to add/fix the Page Metadata section.

## Next Step

After validating page metadata, proceed to step-02-navigation.md

## Validation Checklist

```yaml
page_metadata_validated:
  section_exists: [true/false]
  platform_declared: [true/false]
  page_type_specified: [true/false]
  viewport_identified: [true/false]
  interaction_model_documented: [true/false]
  navigation_context_defined: [true/false]
  inherits_from_scenario: [true/false]
  status: [pass/warning/critical]
```
