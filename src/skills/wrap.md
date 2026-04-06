# /wrap — Session Wrap Skill

**Invocation:** `/wrap`
**Works for:** any agent (saga, freya, mimir)

---

<wrap-steps>

  <constraints>
    - Derive everything from the conversation. Do NOT ask the user any questions.
    - Your agent_id is your WDS base name: saga, freya, or mimir. Never a project name.
    - No output between steps — only what the steps explicitly say to print.
  </constraints>

  <step id="1-write">
    Write session-wrap.md to the repo root. Silent — no output.

    ```markdown
    ## Learned
    [What will benefit future sessions: decisions with reasons, patterns, non-obvious constraints.
    Skip only if nothing was learned this session.]

    ## Context
    [What was done. State of artifacts. Open threads. Be specific.]

    ## Plan
    [The plan we are in the middle of and the end goal. Where we are, what remains.]

    ## Next
    [Single immediately-actionable next task. Not "continue X" — "do Y in file Z".]

    ## Spec Sync
    [Did anything change that diverges from a written spec/brief/doc? Update it NOW.
    If nothing changed: write "None".]
    ```
  </step>

  <step id="2-show">
    Print EXACTLY this block — nothing before, nothing after:

    ── Handover ──────────────────────────────────
    Next:    [Next — one line]
    Plan:    [Plan — one line]
    Open:    [blocking issues or "None"]
    Learned: [one line or "None"]
    ──────────────────────────────────────────────
  </step>

  <step id="3-publish">
    Run:
    python c:/dev/WDS/design-space/tools/wrap-publish.py \
      --input session-wrap.md \
      --repo [repo-folder-name] \
      --agent [saga|freya|mimir] \
      --user "[git config user.name]"

    No additional output. Let the script print what it prints.
  </step>

  <step id="4-token">
    Parse the UUID from "Handoff posted: {uuid}" in the script output.
    Take the first 6 characters.

    Print EXACTLY this — nothing before, nothing after:

    ```
    /[agent] [6chars]
    ```

    Session complete. Stop.
  </step>

</wrap-steps>
