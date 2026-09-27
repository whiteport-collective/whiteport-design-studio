---
skill: ux-design
agent: freya
prerequisites:
  - "{output_folder}/C-UX-Scenarios/00-ux-scenarios.md"
output_folder: "{output_folder}/D-UX-Design"
---

# UX Design Workflow

Transforms UX Scenarios into development-ready page specifications through the Design Loop. One loop per page — discuss, spec, wireframe, approve, implement, extract.

---

<workflow id="ux-design">

  <constraints>
    - The Design Loop runs once per page. Steps execute in sequence.
    - Spec Writer generates spec files — do not write specs inline.
    - Wireframes use Excalidraw by default. PNG export required for approval.
    - The approval gate (step 4) is a hard stop — do not proceed without user confirmation.
    - Token Extractor runs after browser review, not before.
    - Update Design Loop Status table in design log after each loop step.
  </constraints>

  <!-- ═══════════════════════════════════════════
       INIT — Adaptive Dashboard
  ═══════════════════════════════════════════ -->

  <step id="init">
    Load:
    - `_progress/00-design-log.md` — Current table + Design Loop Status table
    - All scenario files from `{output_folder}/C-UX-Scenarios/`
    - `references/ux-design-workflow.md`

    Build page inventory from scenarios.
    Read Design Loop Status table — get current status per page.

    IF Current table has a ux-design task:
      Show status and resume:
      "Welcome back. We were working on [page]. Design Loop Status: [step N — step name]."
      → jump to the step recorded for that page

    ELSE:
      Show dashboard and ask where to start.

    <dashboard>
      Print:

      ✨ [Project Name] — Design Status

      [For each scenario:]
      [Scenario name] ([archetype])
        [Page 1]    [status]
        [Page 2]    [status]
        ...

      Legend: ○ not started · S specced · W wireframed · ✓ approved · B built · R reviewed · T tokens
    </dashboard>

    Ask: "Which page do you want to design first?"
    → go to <step id="design-loop">
  </step>

  <!-- ═══════════════════════════════════════════
       DESIGN LOOP
       Runs once per page — repeat for each page
  ═══════════════════════════════════════════ -->

  <step id="design-loop">

    <loop-step id="1-discuss">
      Load `references/specification-quality.md` and `references/strategic-design.md`.

      Open the conversation about this page:
      "Let's talk about [Page name]. In the scenario, [User name] arrives here [after/when] [context from scenario].

      What's the most important thing this page needs to do for them?"

      Explore through conversation:
      - What does the user need to accomplish here?
      - What content / data / actions does the page contain?
      - What emotional state is the user in when they arrive?
      - What should they feel when they leave?
      - Any edge cases or states (empty, loading, error)?

      When the discussion feels complete:
      "I think I have a solid picture of this page. Ready to write the spec?"
      Wait for confirmation.

      Update Design Loop Status: [page] → S (speccing)
    </loop-step>

    <loop-step id="2-spec">
      <subagent ref="agents/spec-writer.md">
        <input>
          - Page name and scenario context
          - Discussion output: purpose, content, actions, emotional arc, edge cases
          - Project context: product brief, trigger map archetype for this flow
        </input>
        <output>
          `{output_folder}/D-UX-Design/[page-slug].md`
        </output>
      </subagent>

      "Spec written. Read through it — does it capture the page correctly?"
      Wait for feedback. Adjust if needed.

      Update Design Loop Status: [page] → S✓ (spec approved)
    </loop-step>

    <loop-step id="3-wireframe">
      Load `references/ux-design-workflow.md` wireframe section.

      "I'll now create the wireframe for [Page name]."

      Invoke `agents/wireframe.md` with the page spec.

      When the wireframe agent reports back, present the description it returns.

      Update Design Loop Status: [page] → W (wireframed)
    </loop-step>

    <loop-step id="4-approve">
      Hard stop. Do not proceed without explicit user approval.

      "Does this wireframe work? Approve to move to implementation, or tell me what to change."

      <gate>
        IF approved: → loop-step 5 (update spec)
        IF changes requested: → loop-step 3 (iterate wireframe), then return here
      </gate>

      Update Design Loop Status: [page] → ✓ (approved)
    </loop-step>

    <loop-step id="5-update-spec">
      Update the spec to reflect the approved wireframe exactly.
      Any decisions made during wireframing that changed the spec must be reconciled now.

      "Spec updated to match approved wireframe."

      Update Design Loop Status: [page] → ✓S (spec synced)
    </loop-step>

    <loop-step id="6-implement">
      Hand off to development. Options:
      - If Mimir is available: invoke `/mimir` with the spec and wireframe
      - If developer: "Implementation-ready. See [page-slug].md + wireframes/[page-slug].png"

      Update Design Loop Status: [page] → B (building)

      When implementation confirmed complete by user:
      Update Design Loop Status: [page] → B✓ (built)
    </loop-step>

    <loop-step id="7-browser-review">
      Invoke `agents/design-reviewer.md` with the built page URL, spec, and approved wireframe.

      Present the review report. If issues found: discuss severity and fix priority with the user.
      If critical issues: resolve before marking reviewed.

      Update Design Loop Status: [page] → R (reviewed)
    </loop-step>

    <loop-step id="8-extract-tokens">
      Load `references/design-system.md`.

      <subagent ref="agents/token-extractor.md">
        <input>
          - Implemented page
          - Existing token registry (if any)
          - Page spec
        </input>
        <output>
          Identified tokens: colors, typography, spacing, component patterns
          New tokens not yet in registry
          Updated token registry
        </output>
      </subagent>

      "Tokens extracted from [Page name]:
      [N] new tokens added to registry.
      [List any significant new patterns identified]"

      Update Design Loop Status: [page] → T (tokens extracted)
    </loop-step>

    <!-- Page complete. Offer next step. -->

    <transition>
      Print:
      "✓ [Page name] — complete

      Next options:
      → [Next page in current scenario] (continue this flow)
      → [First page of next scenario] (start next scenario)
      → Choose a different page"

      Wait for user choice. Loop back to <step id="design-loop"> for chosen page.
    </transition>

  </step>

  <!-- ═══════════════════════════════════════════
       ALL PAGES COMPLETE
  ═══════════════════════════════════════════ -->

  <step id="complete">
    When all pages across all scenarios are at T (tokens extracted):

    Update `_progress/00-design-log.md`:
    - Mark UX Design as complete in phase status

    Print:
    "UX Design complete.
    ✓ [N] pages designed and reviewed
    ✓ Design tokens extracted

    Mimir can build from the specs in D-UX-Design/."
  </step>

</workflow>
