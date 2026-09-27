---
skill: feedback
agent: freya
---

# Feedback Workflow

Processes design feedback through the specification before anything is implemented.
Feedback never goes directly to code — it goes to the spec first.

---

<workflow id="feedback">

  <constraints>
    - Never suggest implementation changes directly from feedback language.
    - The spec is the source of truth. Changes must land in the spec before Mimir is briefed.
    - Mimir receives a spec delta and acceptance criteria — not the original feedback.
    - If feedback cannot be mapped to a spec change, it is not actionable yet. Resolve it first.
    - One feedback session can affect multiple pages — handle each page separately.
  </constraints>

  <!-- ═══════════════════════════════════════════
       RECEIVE
  ═══════════════════════════════════════════ -->

  <step id="receive">
    Accept feedback in any form:
    - Free text from user or stakeholder
    - Screenshot with annotations
    - Browser review findings
    - Recorded session notes
    - List of issues

    Do not act yet. Read it all first.

    Ask if anything is unclear:
    "Before I analyse this — is there anything here that needs more context?"

    Wait for answer, then → go to <step id="analyse">
  </step>

  <!-- ═══════════════════════════════════════════
       ANALYSE
       Map feedback to spec implications
  ═══════════════════════════════════════════ -->

  <step id="analyse">
    For each piece of feedback:

    1. Identify which page(s) it affects
    2. Read the current spec for that page: `{output_folder}/D-UX-Design/[page-slug].md`
    3. Determine what type of feedback it is:

    | Type | What it means |
    |---|---|
    | Content gap | Something is missing from the spec — needs to be added |
    | Content conflict | Spec says one thing, implementation/feedback says another |
    | Behavior change | An interaction or state needs to change |
    | Structure change | Layout, hierarchy, or flow needs to change |
    | Out of scope | Feedback asks for something not in the current spec — new work |
    | Unclear | Cannot be mapped to a spec change without more information |

    4. For unclear feedback: ask one focused question to resolve it before continuing.
       "This feedback about [X] — are you saying [interpretation A] or [interpretation B]?"

    Present the analysis:
    "Here's what I'm reading in this feedback:

    [Page name]:
    - [feedback item] → [type]: [what needs to change in the spec]
    - [feedback item] → [type]: [what needs to change in the spec]

    [If out of scope items:]
    Out of scope (new work, not a spec change): [list]

    Does this match your intent?"

    Wait for confirmation. Adjust if needed.
    → go to <step id="spec-update">
  </step>

  <!-- ═══════════════════════════════════════════
       SPEC UPDATE
       Propose and confirm changes to the spec
  ═══════════════════════════════════════════ -->

  <step id="spec-update">
    For each confirmed spec change, propose the exact edit:

    "For [Page name], I'll make these changes to the spec:

    **[Section]:**
    Before: [current spec text]
    After:  [proposed spec text]

    [Repeat per change]

    Approve these changes?"

    Wait for explicit approval. Do not update the spec until approved.

    Once approved — invoke `agents/spec-writer.md` in update mode:
    Update the spec file with the approved changes only. Do not rewrite sections that were not changed.

    Confirm: "Spec updated. [N] changes applied to [page-slug].md."

    → go to <step id="mimir-brief">
  </step>

  <!-- ═══════════════════════════════════════════
       MIMIR BRIEF
       Write a work order for Mimir — spec delta, not feedback
  ═══════════════════════════════════════════ -->

  <step id="mimir-brief">
    Invoke `agents/mimir-brief.md` with:
    - The original feedback (for context only)
    - The spec changes that were approved and applied
    - The affected pages and their current specs
    - Acceptance criteria derived from the spec changes

    The work order Mimir receives describes what the spec now says — not what anyone felt.

    When the work order is written:
    "Mimir brief ready at: `{output_folder}/D-UX-Design/mimir-briefs/[brief-slug].md`

    Run /mimir to implement. Mimir will work from the updated spec."

    → go to <step id="close">
  </step>

  <!-- ═══════════════════════════════════════════
       CLOSE
  ═══════════════════════════════════════════ -->

  <step id="close">
    Update `_progress/00-design-log.md`:
    - Log: feedback received, spec updated, Mimir brief written
    - Current: awaiting Mimir implementation (or mark as done if user is implementing manually)

    If out-of-scope items were identified:
    "These items were out of scope for this feedback round — they'd require new spec work:
    [list]
    Want to add them to the design backlog?"
  </step>

</workflow>
