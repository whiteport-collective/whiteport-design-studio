---
# Final step - no nextStepFile
---

# Step 8: Final Validation & Quality Report

## Purpose

Cross-reference all sections, verify sketch coverage, check for broken links, validate naming conventions, and generate comprehensive quality report.

## Context for Agent

Final validation catches inconsistencies before handoff and ensures specification completeness. This step synthesizes findings from all previous steps and provides confidence for developers that the specification is production-ready.

## Key Elements

This step validates:
- Cross-references between sections are consistent
- All sketch elements are documented in Page Sections
- All Object IDs in sections appear in Object Registry
- Internal links are not broken
- Naming conventions are consistent throughout
- Page numbers match across all references
- No orphaned or undocumented elements

## Instructions

Perform final cross-checks across all sections. Verify every element visible in the sketch has corresponding documentation in Page Sections. Confirm all internal links work (navigation links, design system references, etc.).

Check naming consistency (page numbers, Object ID format, component names). Identify any orphaned content or undocumented sketch elements.

Synthesize findings from Steps 1-7 into comprehensive quality report showing overall status, critical issues, warnings, and recommendations.

Generate final quality report with:
- Executive summary (overall status: PASS/NEEDS WORK/CRITICAL ISSUES)
- Issues by category (Critical, Warning, Info)
- Coverage metrics (Object Registry coverage, sketch coverage)
- Recommendations prioritized by impact
- Optional: Offer to add audit stamp to page spec for handoff tracking

## Quality Report Format

```markdown
# Page Specification Quality Report

**Page:** [Page Number] [Page Name]
**Audit Date:** [Date]
**Overall Status:** ✅ PASS / ⚠️ NEEDS WORK / ❌ CRITICAL ISSUES

## Executive Summary
[Brief overview of specification quality]

## Critical Issues (Must Fix Before Handoff)
[List critical issues from all steps]

## Warnings (Should Fix)
[List warnings from all steps]

## Info (Nice to Have)
[List informational items]

## Coverage Metrics
- Object Registry Coverage: X%
- Sketch Coverage: X%
- Design System References: X%

## Recommendations
[Prioritized list of fixes]

## Next Steps
[What to do next based on findings]
```

## Next Step

This is the final step. After generating quality report, ask user if they want to:
- [F] Fix issues (you help implement fixes)
- [S] Add audit stamp to page spec (optional handoff tracking)
- [D] Done (end workflow)

## Validation Checklist

```yaml
final_validation_complete:
  cross_references_consistent: [true/false]
  sketch_coverage_complete: [true/false]
  links_validated: [true/false]
  naming_conventions_consistent: [true/false]
  no_orphaned_content: [true/false]
  quality_report_generated: [true/false]
  overall_status: [pass/needs_work/critical]
```
