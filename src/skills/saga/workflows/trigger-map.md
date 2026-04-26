---
skill: trigger-map
agent: saga
prerequisite: "{output_folder}/A-Product-Brief/product-brief.md"
output_folder: "{output_folder}/B-Trigger-Map"
---

# Trigger Map Workflow

Maps the business goals and target users from the Product Brief into a four-layer strategic document:
Business Goals → Product/Solution → Target Groups → Driving Forces.

The output is a set of documents that Freya uses to build UX Scenarios.

---

<workflow id="trigger-map">

  <constraints>
    - One question at a time. Always wait for the answer.
    - Reflect back what you heard before asking the next question.
    - Archetype names must be alliterative (e.g., Harriet the Hairdresser, Viktor the Videographer).
    - Do not invent psychology — only use what emerged from the conversation.
    - Subagents write the documents — do not write them inline.
    - Write each document as soon as its workshop is confirmed complete, before continuing.
    - Update design log at each checkpoint.
  </constraints>

  <!-- ═══════════════════════════════════════════
       INIT
  ═══════════════════════════════════════════ -->

  <step id="init">
    Load:
    - `{output_folder}/A-Product-Brief/product-brief.md` — extract business goals and target user sections
    - `_progress/00-design-log.md` — check Current for in-progress work
    - `references/trigger-mapping.md`

    IF prerequisite missing:
      "I need the Product Brief before I can map triggers. Run /PB first."
      Stop.

    IF Current table has a trigger-map task in progress:
      → resume at the step recorded in Current

    Extract from Product Brief:
    - User behavioral profiles (target groups section)
    - Business context and value proposition
    - Any goals or objectives already stated

    Brief to user:
    "I've read the Product Brief. I can see [N] user profiles to work with: [names/labels].
    I'll run five workshops to build the Trigger Map — starting with your business goals,
    then mapping each user group. Let's begin."

    → go to <step id="goals-workshop">
  </step>

  <!-- ═══════════════════════════════════════════
       WORKSHOP 1 — BUSINESS GOALS
  ═══════════════════════════════════════════ -->

  <step id="goals-workshop">
    Goal: Reach a shared understanding of 3 visionary goals,
    each with 3 SMART objectives. Goals are directional and durable.
    Objectives are measurable and time-bound.

    Start from what the Product Brief already says about goals.
    One question at a time. Reflect before asking the next.

    <sequence>

      <phase id="vision">
        Opening: "What does winning look like for this business — not in numbers, but as a vision?
        If everything goes right, what is this company known for?"
        Synthesize: 1–2 visionary statements.
        Confirm before continuing.
      </phase>

      <phase id="goals">
        For each of 3 goals (primary outcome first, then the two prerequisites that enable it):
        "What has to be true for [vision] to happen? What goal, if achieved, makes it inevitable?"
        Synthesize: goal name and one-sentence aspiration.
        Confirm each goal before moving to the next.
      </phase>

      <phase id="objectives">
        For each confirmed goal:
        "How will you know you've achieved [goal name]? What would you measure?"
        Synthesize: 3 SMART objectives per goal (specific, measurable, time-bound).
        Confirm before writing.
      </phase>

    </sequence>

    Checkpoint:
    "I have three goals with objectives. Let me write that up."

    <subagent ref="agents/goals-writer.md">
      <input>
        - Vision statements
        - 3 goals with names and one-sentence aspirations
        - 3 SMART objectives per goal
        - Product Brief source reference
      </input>
      <output>`{output_folder}/B-Trigger-Map/01-business-goals.md`</output>
    </subagent>

    "Business goals written. Now let's map the people who will make this happen."

    Update design log: goals-workshop complete.

    → go to <step id="persona-workshops">
  </step>

  <!-- ═══════════════════════════════════════════
       WORKSHOPS 2–4 — PERSONAS + DRIVING FORCES
       One persona at a time. Write after each confirmation.
  ═══════════════════════════════════════════ -->

  <step id="persona-workshops">
    Work through each user profile from the Product Brief, one at a time.
    Priority order: highest strategic value first.

    For each persona, run the full sequence below before calling the persona writer.

    <persona-sequence>

      <phase id="name">
        Propose an alliterative archetype name that captures the essence:
        "For [profile label], I'm thinking [Name the Noun] — [one-line characterization].
        Does that feel right, or would you describe them differently?"
        Confirm or adjust before continuing.
      </phase>

      <phase id="profile">
        Goal: Who this person is — life context, background, psychological makeup.
        Opening: "Tell me about [Name]'s world. Who are they, and what's their relationship to [the problem space]?"
        Follow up on: what they value, what defines their self-image, what they're proud of,
        what they're quietly struggling with.
        Synthesize: background, psychological profile, internal emotional state.
        Confirm before continuing.
      </phase>

      <phase id="driving-forces">
        Goal: The deep motivations — what they are moving toward and moving away from.

        Positive forces:
        "What does [Name] actually want to achieve? What would make them feel like they've won?"
        Synthesize: 3–5 positive forces, WHAT + WHY + WHEN pattern.

        Negative forces:
        "What is [Name] most afraid of, or most frustrated by, in this space?"
        Synthesize: 3–5 negative forces, WHAT + WHY + WHEN pattern.

        Score each force: Frequency + Intensity + Fit (1–5 each, total /15).
        Confirm forces and scores before continuing.
      </phase>

      <phase id="usage-context">
        Goal: How, when, and in what state [Name] actually uses the product.
        Opening: "Walk me through how [Name] finds and uses this product.
        What brings them there, and what are they feeling when they arrive?"
        Synthesize: discovery path, emotional state on arrival, behavior pattern, decision criteria.
        Confirm before writing.
      </phase>

      <phase id="goal-connection">
        For each confirmed business goal from Workshop 1:
        Identify how this persona serves that goal — specifically.
        If not already clear from earlier phases: "How does [Name] connect to [Goal name]?"
        Synthesize: one sentence per relevant goal.
      </phase>

      Checkpoint after each persona:
      "[Name] mapped. Let me write that up before we continue."

      <subagent ref="agents/persona-writer.md">
        <input>
          - Archetype name and priority number (02 = primary, 03 = secondary, etc.)
          - Profile: background, psychological profile, internal state
          - Driving forces: positive and negative, WHAT + WHY + WHEN, FIA scores
          - Usage context: discovery path, emotional state, behavior, decision criteria
          - Business goal connections
        </input>
        <output>`{output_folder}/B-Trigger-Map/{NN}-persona-{firstname}-the-{archetype}.md`</output>
      </subagent>

      "Written. Shall we continue to [next persona]?"

    </persona-sequence>

    Update design log: persona-workshops complete.

    → go to <step id="poster-generate">
  </step>

  <!-- ═══════════════════════════════════════════
       GENERATE POSTER
  ═══════════════════════════════════════════ -->

  <step id="poster-generate">
    "All [N] personas mapped. Let me build the Trigger Map poster."

    <subagent ref="agents/trigger-writer.md">
      <input>
        - Business goals from 01-business-goals.md
        - All persona files: names, priorities, top driving forces, business goal connections
        - Product name and one-line description
      </input>
      <output>`{output_folder}/B-Trigger-Map/00-trigger-map.md`</output>
    </subagent>

    Update design log: poster complete.

    → go to <step id="feature-impact-generate">
  </step>

  <!-- ═══════════════════════════════════════════
       GENERATE FEATURE IMPACT
       Saga runs this autonomously — no user questions needed.
  ═══════════════════════════════════════════ -->

  <step id="feature-impact-generate">
    "One more thing — I'll derive the Feature Impact Analysis from the driving forces.
    This tells us which features have the highest strategic leverage. Give me a moment."

    <subagent ref="agents/feature-impact-writer.md">
      <input>
        - All persona files with driving forces and FIA scores
        - Business goals for context
        - Product description for fit scoring
      </input>
      <output>`{output_folder}/B-Trigger-Map/feature-impact.md`</output>
    </subagent>

    → go to <step id="review">
  </step>

  <!-- ═══════════════════════════════════════════
       REVIEW & CLOSE
  ═══════════════════════════════════════════ -->

  <step id="review">
    Present the Feature Impact summary:
    "Feature Impact Analysis written. Here are the top priorities:

    [List top 5–7 features by weighted score, one line each]

    Review the full analysis in `feature-impact.md`. Let me know if anything needs adjusting —
    especially if I've named a feature wrong or missed something important."

    Wait for feedback. If adjustments: update documents and re-confirm.

    Update `_progress/00-design-log.md`:
    - Move current task to Log
    - Set Current to empty
    - Mark Trigger Map as complete in phase status

    Print:
    "Trigger Map complete.

    Deliverables in `B-Trigger-Map/`:
    - `00-trigger-map.md` — four-layer poster
    - `01-business-goals.md` — goals + objectives
    - `NN-persona-*.md` — persona profiles with driving forces
    - `feature-impact.md` — prioritized feature list

    Freya can now build UX Scenarios from this foundation. Run /freya when ready."
  </step>

</workflow>
