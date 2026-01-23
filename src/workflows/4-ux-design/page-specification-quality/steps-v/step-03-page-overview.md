---
nextStepFile: './step-04-page-sections.md'
---

# Step 3: Validate Page Overview

## Purpose

Verify that page specification includes strategic context through page description, User Situation, and Page Purpose sections.

## Context for Agent

Page Overview captures strategic intent (WHY) before implementation details (HOW). This section connects design decisions to user needs and trigger map, providing essential context for developers and stakeholders. Without clear overview, developers don't understand the purpose behind design choices.

## Key Elements

This step validates:
- Page description paragraph (1-2 paragraphs explaining what page does)
- User Situation section (user's context, needs, emotional state)
- Page Purpose section (what job page must accomplish)
- Success criteria or VTC reference
- Emotional context and pain points addressed

## Instructions

Check for page description paragraph immediately after navigation section. Verify "User Situation" and "Page Purpose" sections exist with meaningful content that explains user context and page goals.

If overview sections are missing, report as CRITICAL. If content is too brief or lacks strategic context, report as WARNING.

Generate diagnostic report showing what's missing or insufficient, provide examples of strong overview content, and explain why strategic context matters.

## Next Step

After validating page overview, proceed to step-04-page-sections.md

## Validation Checklist

```yaml
page_overview_validated:
  description_paragraph_present: [true/false]
  user_situation_section_present: [true/false]
  page_purpose_section_present: [true/false]
  emotional_context_included: [true/false]
  success_criteria_defined: [true/false]
  strategic_intent_clear: [true/false]
  status: [pass/warning/critical]
```
