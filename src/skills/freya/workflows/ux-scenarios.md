---
skill: ux-scenarios
agent: freya
prerequisites:
  - "{output_folder}/A-Product-Brief/product-brief.md"
  - "{output_folder}/B-Trigger-Map/trigger-map.md"
output_folder: "{output_folder}/C-UX-Scenarios"
---

# UX Scenarios Workflow

Transforms the Trigger Map into UX scenario outlines — linear sunshine paths through the product, one per user archetype, exposing every screen that needs to be designed.

---

<workflow id="ux-scenarios">

  <constraints>
    - Each scenario follows ONE archetype through ONE complete flow — linear, no branching.
    - Sunshine path only: the happy path where everything works as intended.
    - Screens are named and described, not designed. Design happens in Phase 4.
    - Scenario Writer generates the files — do not write scenario content inline.
    - Update design log after each scenario is completed.
  </constraints>

  <!-- ═══════════════════════════════════════════
       INIT
  ═══════════════════════════════════════════ -->

  <step id="init">
    Load:
    - `{output_folder}/A-Product-Brief/product-brief.md`
    - `{output_folder}/B-Trigger-Map/trigger-map.md`
    - `_progress/00-design-log.md`
    - `references/trigger-map-initiation.md`

    IF Current table has a ux-scenarios task:
      → jump to the scenario in progress

    <subagent ref="agents/scenario-analyzer.md">
      <input>Product Brief + Trigger Map</input>
      <output>
        - Site/app type classification
        - Recommended scenario mode (Dialog / Suggest / Dream)
        - Suggested scenario list with archetype mapping
        - Estimated page count
      </output>
    </subagent>

    → go to <step id="scope">
  </step>

  <!-- ═══════════════════════════════════════════
       SCOPE
       Determine how many scenarios, which mode
  ═══════════════════════════════════════════ -->

  <step id="scope">
    Present analyzer output:

    "I've read the brief and trigger map. Here's what I'm thinking:

    [Site/app type] — [estimated page count] pages
    [N] scenarios, one for each archetype:
    [list archetypes and proposed scenario titles]

    Mode: [Dialog/Suggest/Dream] — [one-line reason]"

    <mode-logic>
      Dialog  → large products (100+ pages), present one scenario at a time, discuss scope before each
      Suggest → medium products (20-100 pages), present full list, confirm, then walk through each
      Dream   → simple products (<20 pages), generate all outlines, present for review
    </mode-logic>

    Ask: "Does this feel right? Anything to add or adjust before I start outlining?"

    Wait for confirmation. Adjust if needed.
    → go to <step id="scenario-loop">
  </step>

  <!-- ═══════════════════════════════════════════
       SCENARIO LOOP
       Walk through each scenario one at a time
  ═══════════════════════════════════════════ -->

  <step id="scenario-loop">
    For each scenario (repeat until all are done):

    <scenario-walkthrough>

      <phase id="open">
        Introduce the scenario:
        "[Archetype name] wants to [goal]. Let me walk through what they experience."

        State the entry point:
        "They start at [entry point]. What brought them here was [trigger from Trigger Map]."
      </phase>

      <phase id="walk">
        Load `references/scenario-conversation-pattern.md`.

        Walk screen by screen in conversation. For each screen:
        - Name it: "[Page name]"
        - Describe what the user sees and does: "[User action / decision / content encountered]"
        - Name the next screen or decision point
        - Ask: "Does this feel right, or does something happen differently here?"

        Push for specificity:
        - "What does [Name] see when they land here?"
        - "What does [Name] do next — is the path obvious?"
        - "What could go wrong here that we want to design for?"

        Continue until the archetype reaches their success state from the Trigger Map.
      </phase>

      <phase id="confirm">
        Summarize the scenario as a screen list:

        "[Scenario title] — [Archetype name]
        1. [Screen name] — [one-line description]
        2. [Screen name] — [one-line description]
        ...
        [N]. [Screen name] — success state"

        Ask: "Does this capture the flow correctly?"
        Wait for confirmation or adjustments.
      </phase>

      <phase id="write">
        <subagent ref="agents/scenario-writer.md">
          <input>
            - Scenario title and archetype
            - Confirmed screen list with descriptions
            - Entry trigger (from Trigger Map)
            - Success state
          </input>
          <output>
            `{output_folder}/C-UX-Scenarios/[scenario-slug].md`
          </output>
        </subagent>

        Update design log: mark this scenario as complete.
      </phase>

    </scenario-walkthrough>

    After last scenario → go to <step id="index">
  </step>

  <!-- ═══════════════════════════════════════════
       INDEX
  ═══════════════════════════════════════════ -->

  <step id="index">
    <subagent ref="agents/scenario-writer.md">
      <input>All completed scenario files</input>
      <output>
        `{output_folder}/C-UX-Scenarios/00-ux-scenarios.md`
        — index with: scenario titles, archetypes, page counts, entry points
      </output>
    </subagent>

    → go to <step id="review">
  </step>

  <!-- ═══════════════════════════════════════════
       REVIEW & CLOSE
  ═══════════════════════════════════════════ -->

  <step id="review">
    Print:
    "UX Scenarios complete:
    ✓ [N] scenarios written
    ✓ [total page count] screens identified
    ✓ 00-ux-scenarios.md index created

    Read through them and let me know if any flow needs adjusting."

    Wait for feedback. If adjustments: update relevant scenario file.

    Update `_progress/00-design-log.md`:
    - Move current task to Log
    - Mark UX Scenarios as complete in phase status

    Print:
    "Ready for UX Design — run /UX when you want to start designing pages."
  </step>

</workflow>
