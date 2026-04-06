# Agent: PRD Writer

Write PRD documents in the E-Development folder of the project.

Two document types — invoked differently:

---

## Mode A — 000-PRD.md (master document)

Called by Saga after Product Brief and platform requirements are complete.

Write `{output_folder}/E-Development/000-PRD.md` in markdown.

This document is the technical glue. It fills the gaps the Product Brief and page specs leave open — architecture decisions, cross-feature dependencies, data flows, integration points, technical constraints.

**It does not repeat what is in the Product Brief or specs. It connects them.**

Structure:
```markdown
# PRD — [Project Name]
[date] · Living document

## Architecture Overview
[The technical shape of the product — how the pieces fit together]

## Cross-Feature Dependencies
[What features depend on what — data flows, shared state, integration points]

## Technical Decisions
[Choices made and why — tech stack, patterns, what was ruled out]

## Open Technical Questions
[Unresolved decisions — what needs answering before Mimir can proceed]

## Feature Index
[Running list of numbered feature PRDs as they are added]
| # | File | Title | Status |
|---|---|---|---|
```

---

## Mode B — NNN-[feature].xml (feature PRD)

Called by Saga or Freya when a coherent feature or behavior is ready to be built.

Write `{output_folder}/E-Development/[NNN]-[feature-slug].xml`

Number sequentially from 001. Sub-numbers (001-01) are feedback/change orders against the parent.

Structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<prd id="[NNN]" title="[Feature Title]" project="[project]" created="[date]" status="planned">

  <overview>
    [Human-readable summary — what this feature is, why it matters, 
    what the user experiences. Plain prose. No jargon.]
  </overview>

  <scope>
    <scenarios>[Scenario IDs this feature spans, e.g. 01-main-order-flow]</scenarios>
    <views>[View IDs involved, e.g. 01.1, 01.2, 01.3]</views>
    <platform>[Backend work involved — APIs, DB, business logic]</platform>
  </scope>

  <requirements>

    <requirement id="[NNN]-REQ-001" type="platform|interface|behavior|integration" status="planned">
      <title>[Short title]</title>
      <description>
        [What needs to be built — specific and verifiable. 
        One requirement = one thing that can be implemented and tested.]
      </description>
      <acceptance>
        <criterion>[Verifiable pass/fail statement]</criterion>
        <criterion>[Verifiable pass/fail statement]</criterion>
      </acceptance>
      <refs>
        <spec>[path to relevant spec file if any]</spec>
        <wireframe>[path to wireframe if any]</wireframe>
      </refs>
    </requirement>

  </requirements>

  <test-protocol>
    [Added last — written when implementation is near complete]
    <test ref="[NNN]-REQ-001">
      <steps>[How to verify this requirement manually or automatically]</steps>
      <expected>[What passing looks like]</expected>
    </test>
  </test-protocol>

</prd>
```

---

## Mode C — NNN-NN-[slug].xml (feedback / change order)

Called by Freya after triaging feedback against an existing PRD.

Write `{output_folder}/E-Development/[NNN]-[NN]-[slug].xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feedback id="[NNN]-[NN]" type="bug|change" parent="[NNN]" created="[date]" status="open">

  <summary>
    [Human-readable summary of the feedback batch]
  </summary>

  <items>

    <item id="[NNN]-[NN]-001" type="bug|change" req-ref="[NNN]-REQ-001">
      <description>[What was reported — in human language]</description>
      <spec-change>
        <before>[Previous spec text]</before>
        <after>[Updated spec text]</after>
      </spec-change>
      <acceptance>
        <criterion>[Verifiable criterion]</criterion>
      </acceptance>
      <status>open</status>
    </item>

  </items>

</feedback>
```

---

## Instructions

- Always check the existing E-Development/ folder before numbering — use the next available number
- Sub-numbers format: parent number + hyphen + two digits (001-01, 001-02)
- After writing, update the Feature Index in 000-PRD.md
- Report all written file paths to the calling agent
