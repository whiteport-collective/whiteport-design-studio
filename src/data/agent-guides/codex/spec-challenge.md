# Codex - Spec Challenge Checklist

Before coding, challenge the task against these questions.

## Scope

- What exactly is being built or changed?
- What is explicitly out of scope?
- Is this a new page, shared component update, content migration, or behavior fix?

## Source Truth

- Which page spec governs this work?
- Which shared design-system specs apply?
- Which implementation files are expected to change?

## Content Completeness

- Is all copy final in every required locale?
- Are SEO and schema requirements final?
- Are any values placeholders rather than approved content?

## Assets

- Are final images, icons, and logos available?
- Are alt texts and filenames specified?
- Are generated assets approved or still provisional?

## Behavior

- Are responsive rules explicit for mobile, tablet, and desktop?
- Are dynamic states and edge cases defined?
- Are time- or data-based rules complete?

## Reuse

- Can an existing shared component satisfy the requirement?
- If not, what exactly is missing?
- Does the requested behavior belong in a shared component or only this page?

## Drift Check

- Does current code already differ from the spec?
- Is that intentional, accidental, or unresolved?
- Should code move toward the spec, or should the spec be updated?

## Validation

- What proves the work is done?
- Build only?
- Visual parity?
- Localization parity?
- SEO parity?
- Schema parity?

If any answer above is unknown and it materially affects implementation, ask before coding.
