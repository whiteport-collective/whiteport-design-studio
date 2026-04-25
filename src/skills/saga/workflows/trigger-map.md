---
skill: trigger-map
agent: saga
prerequisite: "{output_folder}/A-Product-Brief/product-brief.md"
output_folder: "{output_folder}/B-Trigger-Map"
---

# Trigger Map Workflow

Transforms the Product Brief's target users into psychological profiles — driving forces, trigger points, and behavioral archetypes that Freya uses to build scenarios.

---

<workflow id="trigger-map">

  <constraints>
    - One question at a time. Always wait for the answer.
    - Archetype names must be alliterative (e.g., Harriet the Hairdresser, Marcus the Manager).
    - Do not invent psychology — derive it from what the user tells you. Synthesize, don't fabricate.
    - Trigger Writer generates the document — do not write it inline.
    - Update design log at each checkpoint.
  </constraints>

  <!-- ═══════════════════════════════════════════
       INIT
  ═══════════════════════════════════════════ -->

  <step id="init">
    Load:
    - `{output_folder}/A-Product-Brief/product-brief.md` — extract target users section
    - `_progress/00-design-log.md` — check Current for in-progress work
    - `references/trigger-mapping.md`

    IF prerequisite missing:
      "I need the Product Brief before I can map triggers. Run /PB first."
      Stop.

    IF Current table has a trigger-map task:
      → jump to the step recorded in Current

    Extract from Product Brief:
    - User behavioral profiles (2-3 from target-users section)
    - Business goals and value proposition
    - Product concept and core use case

    Brief context to user:
    "I've read the Product Brief. I can see [N] user profiles to work with: [names/labels]. Let me map the psychology behind each one."

    → go to <step id="archetype-workshop">
  </step>

  <!-- ═══════════════════════════════════════════
       ARCHETYPE WORKSHOP
       One archetype at a time — conversational deep dive
  ═══════════════════════════════════════════ -->

  <step id="archetype-workshop">
    For each user profile from the Product Brief, run the archetype sequence.
    Do all archetypes before generating.

    <archetype-sequence>

      <phase id="name">
        Propose an alliterative archetype name that captures the essence:
        "For [profile label], I'm thinking [Name the Noun] — someone who [one-line characterization]. Does that feel right, or would you describe them differently?"
        Confirm or adjust before continuing.
      </phase>

      <phase id="situation">
        Goal: Current life situation — what are they actually dealing with day to day?
        Opening: "Walk me through [Name]'s week. What's their world like right now?"
        Synthesize: current situation, responsibilities, pressures
      </phase>

      <phase id="driving-forces">
        Goal: The deep motivations — what are they moving toward, what are they moving away from?
        Opening: "What does [Name] actually want out of life — and what are they most afraid of?"
        Synthesize: primary drive (toward), primary avoidance (away from), underlying need
      </phase>

      <phase id="trigger-points">
        Goal: The specific moments when [Name] would reach for a solution like this.
        Opening: "What has to happen in [Name]'s day for them to think 'I need something better than what I have'?"
        Synthesize: trigger events (3-5), emotional state at trigger, decision context
      </phase>

      <phase id="objections">
        Goal: What would stop them from adopting — skepticism, switching cost, competing solutions.
        Opening: "What would make [Name] hesitate, or decide this isn't for them?"
        Synthesize: primary objections, trust barriers, competing behaviors
      </phase>

      <phase id="success-moment">
        Goal: What does winning look like for this archetype?
        Opening: "After using this product for six months, what has changed for [Name]? What do they tell a friend?"
        Synthesize: success state, emotional outcome, word-of-mouth trigger
      </phase>

      Checkpoint after each archetype:
      "That's [Name] mapped. Shall I continue to [next archetype], or is there more to add here?"

    </archetype-sequence>

    → go to <step id="connection-map">
  </step>

  <!-- ═══════════════════════════════════════════
       CONNECTION MAP
       Connect archetypes to product features
  ═══════════════════════════════════════════ -->

  <step id="connection-map">
    For each trigger point across all archetypes:
    - Map to the product feature or moment that responds to it
    - Note which triggers are shared across archetypes (high-priority signals)
    - Identify any triggers that have no product response (gap signals)

    Present gaps if found:
    "I notice [N] trigger points that don't have a clear product response yet: [list]. Worth flagging for Freya."

    → go to <step id="generate">
  </step>

  <!-- ═══════════════════════════════════════════
       GENERATE
  ═══════════════════════════════════════════ -->

  <step id="generate">
    Confirm with user:
    "I have all [N] archetypes mapped. Ready to write the Trigger Map?"

    Wait for confirmation.

    <subagent ref="agents/trigger-writer.md">
      <input>
        - All archetype data (name, situation, driving forces, trigger points, objections, success moment)
        - Connection map (trigger → feature mappings, gaps)
        - Product Brief context (business goals, value proposition)
      </input>
      <output>
        `{output_folder}/B-Trigger-Map/00-trigger-map.md`
      </output>
    </subagent>

    → go to <step id="review">
  </step>

  <!-- ═══════════════════════════════════════════
       REVIEW & CLOSE
  ═══════════════════════════════════════════ -->

  <step id="review">
    Present result:
    "Trigger Map written. Read through it and let me know if anything needs adjusting."

    Wait for feedback. If adjustments: update document, re-confirm.

    Update `_progress/00-design-log.md`:
    - Move current task to Log
    - Set Current to empty
    - Mark Trigger Map as complete in phase status

    Ask: "Want me to generate persona pages for each archetype? They give Freya a quick reference when designing."

    IF yes:
      Invoke `../shared/agents/persona-page.md` for each archetype.
      Output to `{output_folder}/B-Trigger-Map/` with naming: `NN-persona-[firstname]-the-[archetype].md` (numbered by priority, starting at 02).
      "Persona pages written to B-Trigger-Map/."

    Print:
    "Trigger Map complete. Freya can now build scenarios from this — run /freya when ready."
  </step>

</workflow>
