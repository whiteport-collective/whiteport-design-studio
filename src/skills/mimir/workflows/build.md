---
skill: build
agent: mimir
---

# Build Workflow

Implements a PRD one requirement at a time. Every requirement gets its own commit and browser verification before the next one starts. Freya is notified only when every requirement passes.

---

<workflow id="build">

  <constraints>
    - Never implement without a PRD. If no PRD exists, stop and invoke prd.md first.
    - One requirement at a time. Do not batch.
    - Every requirement must pass browser verification before marking done.
    - Do not notify Freya until all requirements in the PRD are verified.
    - If a requirement fails verification twice, flag as blocked and surface to user.
  </constraints>

  <step id="1-read-prd">
    Read the feature PRD (`E-Development/NNN-[feature].xml`) completely.

    Read `E-Development/000-tech-audit.md` for architecture context.
    Read `E-Development/000-PRD.md` for cross-feature dependencies.

    Identify:
    - Total number of requirements
    - Build order (platform requirements first, then interface)
    - Any cross-feature dependencies that must be resolved first
    - Open technical questions that block any requirement

    If open questions exist: surface them to the user before starting.
  </step>

  <step id="2-plan">
    Present the build plan to the user:

    "Ready to build [feature name]. [N] requirements in this order:
    1. [REQ-001] — [title]
    2. [REQ-002] — [title]
    ...

    Estimated sequence: platform first, then interface.
    Start?"

    Wait for confirmation.
  </step>

  <step id="3-build-loop">
    For each requirement in order:

    <sub-step id="3a-implement">
      Implement the requirement.
      Write focused, minimal code — exactly what the requirement specifies.
      No extras, no refactoring of unrelated code.
    </sub-step>

    <sub-step id="3b-commit">
      Commit with message: `[NNN-REQ-NNN] [requirement title]`
    </sub-step>

    <sub-step id="3c-verify">
      Invoke `agents/browser-verifier.md` with:
      - The acceptance criteria from the PRD requirement
      - The URL/path to verify
      - Any specific states to test (empty, error, success, etc.)

      The verifier opens the browser, tests the criterion, returns: PASS or FAIL with details.
    </sub-step>

    <sub-step id="3d-route">
      IF PASS:
        Mark requirement done in state file.
        Report: "✓ [REQ-NNN] [title] — verified"
        Continue to next requirement.

      IF FAIL:
        Fix the issue. Re-commit. Re-invoke browser-verifier.
        IF FAIL again:
          Flag as blocked: "✗ [REQ-NNN] [title] — blocked: [verifier finding]"
          Surface to user. Wait for guidance before continuing.
    </sub-step>
  </step>

  <step id="4-complete">
    All requirements verified. Update PRD status to `implemented`.
    Update `_progress/mimir-state.md`.

    Notify Freya:
    "WO-[NNN] [feature] — all [N] requirements implemented and browser-verified.
    Spec refs: [list]
    Ready for your review."

    Post work order update to Design Space if applicable.
  </step>

</workflow>
