# Spec Challenge Checklist

Before writing code, challenge the handoff against this checklist.

## Scope

- What exactly is being built or changed?
- What is explicitly out of scope?
- Is the task a new page, shared component update, content migration, or behavior fix?

## Source Files

- Which page spec governs this work?
- Which shared design-system specs apply?
- Which existing implementation files are expected to change?

## Content Completeness

- Is all copy final in every required locale?
- Are SEO, structured data, and heading requirements final?
- Are any values placeholders rather than approved content?

## Asset Readiness

- Are final images, icons, and logos available?
- Are alt texts and filenames specified?
- Are generated assets approved or still provisional?

## Behavior

- Are interactive states fully defined?
- Are dynamic rules complete, including edge cases?
- Is responsive behavior explicit for mobile, tablet, and desktop?

## Reuse vs New Build

- Can existing shared components satisfy the spec?
- If not, what specifically is missing?
- Does the change belong in a shared component or only this page?

## Implementation Drift

- Does the current code already differ from the spec?
- Is that intentional, accidental, or unresolved?
- Should code move toward the spec, or should the spec be updated?

## Validation

- What proves the task is done?
- Build only?
- Visual parity?
- Localization parity?
- SEO/schema parity?

If any answer above is unknown and it materially affects implementation, ask before coding.
