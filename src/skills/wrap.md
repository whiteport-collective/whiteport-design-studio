# /wrap — Session Wrap Skill

**Invocation:** `/wrap`
**Works for:** any agent (saga, freya, mimir)

---

<wrap-steps>

  <constraints>
    - Derive everything from the conversation. Do NOT ask the user any questions.
    - Your agent_id is your WDS base name: saga, freya, or mimir. Never a project name.
    - Show substance to user BEFORE spawning subagent — user must see what is being saved.
    - The subagent handles all mechanical execution. You only compile and show.
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

  <step id="1-compile">
    Compile the session substance internally. Do NOT write to disk. Do NOT output anything.

    Compose these four fields:

    **learned:** What will benefit future sessions: decisions with reasons, patterns,
    non-obvious constraints. "None" if nothing was learned.

    **context:** What was done. State of artifacts. Open threads. Be specific.
    If mid-session: "Wrapped mid-task: [what was in progress]"

    **plan:** The overarching plan and end goal. Where we are. What remains.
    If multi-session: list numbered milestones with status:
      - [DONE] Milestone 1 — description
      - [CURRENT] Milestone 2 — description (~1 session)
      - [ ] Milestone 3 — description (~2 sessions)
    Omit milestone list if single-session work.

    **next:** Single immediately-actionable next task.
    Prefix with model: MODEL:[Haiku|Sonnet|Opus] — task description.
    Model selection = task type × complexity × stakes:
      - Haiku: simple, low-stakes, short — lookups, summaries
      - Sonnet: moderate complexity — strategy, spec, dialog, UX, config, analysis
      - Opus: any code; OR high-stakes/production work; OR long or complex tasks
    Default to lightest model that can handle the task.

    **spec_sync:** Did anything change that diverges from a written spec/brief/doc?
    "None" if nothing changed.
  </step>

  <step id="2-show">
    Print EXACTLY this block to the user — nothing before, nothing after:

    ── Handover ──────────────────────────────────
    Next:    [next — including MODEL prefix]
    Plan:    [plan — one line summary or current milestone]
    Open:    [blocking issues or "None"]
    Learned: [learned — one line or "None"]
    ──────────────────────────────────────────────

    [If call threshold reached: print "Note: session at [N] calls — good time to wrap."]

    Wait for no input. Proceed immediately to step 3.
  </step>

  <step id="3-subagent">
    Spawn a subagent using the Agent tool with this exact prompt —
    substitute the bracketed values from step 1:

    ---
    You are a wrap executor. Your only job is to save a session wrap file.
    Follow these steps exactly. No interpretation. No additions.

    **Session data:**
    - agent_id: [saga|freya|mimir]
    - learned: [learned]
    - context: [context]
    - plan: [plan]
    - next: [next]
    - spec_sync: [spec_sync]

    **Step A — Ensure progress folder exists:**
    Create `progress/` in the project root if it doesn't exist.

    **Step B — Write state file:**
    Write `progress/[agent_id].md` with this exact content:

    ```
    ## Wrapped
    [current date and time]

    ## Context
    [context]

    ## Plan
    [plan]

    ## Next
    [next]

    ## Learned
    [learned]

    ## Spec Sync
    [spec_sync]
    ```

    **Step C — Confirm:**
    Return ONLY: `Saved to progress/[agent_id].md`
    ---

    Print whatever the subagent returns. Session complete. Stop.
  </step>

</wrap-steps>
