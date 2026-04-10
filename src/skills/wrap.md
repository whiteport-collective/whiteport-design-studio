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

  <step id="0-milestone-check">
    Before writing anything: assess whether this is a natural milestone boundary.

    A milestone boundary is when a discrete unit of work is complete — a feature shipped,
    a spec finalized, a phase closed. NOT mid-task, mid-investigation, or mid-dialog.

    **If NOT at a milestone:** note this as "mid-session" in Context. The Next task should
    be the immediate continuation of interrupted work.

    **If at a milestone:** proceed normally.

    **Call threshold:** If this session has had 15+ tool calls, surface once as part of step 2:
    `Note: session at [N] calls — good time to wrap for fresh context.`
  </step>

  <step id="1-write">
    Write session-wrap.md to the repo root. Silent — no output.

    ```markdown
    ## Learned
    [What will benefit future sessions: decisions with reasons, patterns, non-obvious constraints.
    Skip only if nothing was learned this session.]

    ## Context
    [What was done. State of artifacts. Open threads. Be specific.
    If mid-session (not at milestone): flag it clearly — "Wrapped mid-task: [what was in progress]"]

    ## Plan
    [The overarching plan and end goal. Where we are. What remains.
    If more than one session of work remains: list numbered milestones with status:
      - [DONE] Milestone 1 — description
      - [CURRENT] Milestone 2 — description (~1 session)
      - [ ] Milestone 3 — description (~2 sessions)
    Omit milestone list if this is single-session work.]

    ## Next
    [Single immediately-actionable next task.
    Prefix with model: MODEL:[Haiku|Sonnet|Opus] — task description.
    Model selection = task type × complexity × stakes:
      - Haiku: simple, low-stakes, short — lookups, message checks, summaries
      - Sonnet: moderate complexity — strategy, spec, dialog, UX, config, analysis
      - Opus: any code; OR high-stakes/production work; OR long or complex tasks where reasoning quality matters
    Default to the lightest model that can handle the task. Escalate only when stakes or complexity genuinely justify it — not as a precaution.
    Format: "MODEL:Sonnet — [task]" or "MODEL:Opus — [task]"]

    ## Spec Sync
    [Did anything change that diverges from a written spec/brief/doc? Update it NOW.
    If nothing changed: write "None".]
    ```
  </step>

  <step id="2-show">
    Print EXACTLY this block — nothing before, nothing after:

    ── Handover ──────────────────────────────────
    Next:    [Next line — including MODEL prefix]
    Plan:    [Plan — one line summary or current milestone]
    Open:    [blocking issues or "None"]
    Learned: [one line or "None"]
    ──────────────────────────────────────────────

    [If call threshold reached: print "Note: session at [N] calls — good time to wrap."]
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

    Check the Next line from step 2: does it hand off to a different agent?
    - "Wake Mimir" / "Hand to Mimir" / "/mimir" → target agent is mimir
    - "Wake Freya" / "Hand to Freya" / "/freya" → target agent is freya
    - "Wake Saga" / "Hand to Saga" / "/saga" → target agent is saga
    - No handoff detected → target agent is current agent

    Print EXACTLY this — nothing before, nothing after:

    ```
    /[target-agent] [6chars]
    ```

    Session complete. Stop.
  </step>

</wrap-steps>
