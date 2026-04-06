---
skill: prd
agents: [saga, freya]
---

# PRD Workflow

Creates and maintains product requirement documents in `E-Development/`.

The PRD folder is the machine's memory of what was agreed. Users never need to open it — agents read it, write it, update it, and brief Mimir/Codex from it.

---

<workflow id="prd">

  <constraints>
    - 000-PRD.md is written once by Saga and updated as the project evolves. Never rewritten from scratch.
    - Feature PRDs (NNN.xml) are numbered sequentially. Never renumber.
    - Feedback files (NNN-NN.xml) are sub-numbered against their parent. Each feedback batch = one file.
    - The spec is always updated BEFORE the PRD is updated. PRD reflects confirmed spec changes only.
    - Test protocols are added last — when implementation is near complete.
  </constraints>

  <!-- ═══════════════════════════════════════════
       ROUTE
  ═══════════════════════════════════════════ -->

  <step id="route">
    Determine which mode to run:

    | Trigger | Mode |
    |---|---|
    | Saga, after Product Brief + Platform Requirements complete | A — write 000-PRD.md |
    | Feature ready to build (Saga or Freya) | B — write feature PRD |
    | Feedback triaged and spec updated (Freya) | C — write feedback file |
    | Test protocol needed | D — add test-protocol to existing PRD |
  </step>

  <!-- ═══════════════════════════════════════════
       MODE A — Master PRD
  ═══════════════════════════════════════════ -->

  <step id="mode-a">
    Read:
    - `A-Product-Brief/` — all documents
    - `A-Product-Brief/04-platform-requirements.md` (or equivalent)
    - `B-Trigger-Map/` — for user and business context
    - `C-UX-Scenarios/00-ux-scenarios.md` — for feature scope

    Identify:
    - What architecture decisions have been made
    - What cross-feature dependencies exist
    - What is technically unresolved
    - What the feature build order should be

    Invoke `agents/prd-writer.md` Mode A.

    After writing: confirm with the calling agent.
    "000-PRD.md written. [N] open technical questions identified. Ready to number first feature PRD."
  </step>

  <!-- ═══════════════════════════════════════════
       MODE B — Feature PRD
  ═══════════════════════════════════════════ -->

  <step id="mode-b">
    Determine what the feature covers:
    - Which scenarios and views are involved
    - What platform work is required (APIs, DB, business logic)
    - What interface work is required (specs, wireframes)
    - What crosses screen boundaries (transitions, shared state)

    Check `E-Development/` for next available number.

    Write requirements at the right granularity:
    - One requirement = one thing that can be implemented AND tested independently
    - Platform requirements first, then interface requirements
    - Leave test-protocol empty — added later

    Invoke `agents/prd-writer.md` Mode B.

    Update Feature Index in 000-PRD.md.

    "Feature PRD [NNN]-[slug].xml written. [N] platform requirements, [N] interface requirements."
  </step>

  <!-- ═══════════════════════════════════════════
       MODE C — Feedback File
  ═══════════════════════════════════════════ -->

  <step id="mode-c">
    Prerequisite: specs already updated (feedback.md workflow completed first).

    For each feedback item:
    - Map to parent PRD requirement ID
    - Record before/after spec text
    - Write verifiable acceptance criterion

    Invoke `agents/prd-writer.md` Mode C.

    Post work order to Design Space pointing to the feedback file.

    "[NNN]-[NN]-[slug].xml written. [N] items. Mimir brief ready."
  </step>

  <!-- ═══════════════════════════════════════════
       MODE D — Test Protocol
  ═══════════════════════════════════════════ -->

  <step id="mode-d">
    Read the feature PRD.
    For each requirement: write test steps and expected outcome.
    Update the <test-protocol> section of the existing PRD file.

    "Test protocol added to [NNN]-[slug].xml. [N] tests covering [N] requirements. Ready for Idun."
  </step>

</workflow>
