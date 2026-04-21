# /handoff — Cross-Agent Handoff

Pass a specific piece of work to another WDS agent. This is NOT a session wrap — it is a targeted transfer of one task or artifact to a different agent.

**Usage:** `/handoff [target-agent]`
**Example:** `/handoff mimir`

---

<handoff-steps>

  <constraints>
    - Derive everything from the conversation. Do NOT ask questions.
    - Do NOT summarize this session. That is a wrap, not a handoff.
    - Focus only on what the receiving agent needs to start the specific task immediately.
    - Handoff is written to `progress/[target_agent].md` — the receiving agent picks it up via `/start`.
  </constraints>

  <step id="1-compile">
    Determine:
    - `target_agent` — from the argument. If none: infer from context (strategy → saga, design → freya, implementation → mimir).
    - `from_agent` — your current agent base name.
    - `project` — current project repo name.

    Compose the handoff content — what the receiving agent needs to start immediately:

    ```
    ## Task
    [Single specific task being handed off. What it is, what state it's in, what remains.]

    ## Files
    [Full absolute paths to every relevant file. The receiving agent should never have to search for them.]

    ## Next
    [Single immediately-actionable next step for the receiving agent.]
    ```

    This is task context, not session history. Always include full absolute file paths — never just filenames. If the receiving agent doesn't need something to do the task, leave it out.
  </step>

  <step id="2-show">
    Print EXACTLY this block:

    ── Handoff to [target_agent] ─────────────────
    Task:    [one-line task description]
    Next:    [the Next line you composed]
    ──────────────────────────────────────────────

    Then proceed immediately to step 3.
  </step>

  <step id="3-write">
    Spawn a sub-agent with this exact prompt — substitute the bracketed values:

    ---
    You are a file writer. Your only job is to write a handoff file.

    **Step A — Ensure progress folder exists:**
    Create `progress/` in the project root if it doesn't exist.

    **Step B — Write handoff file:**
    Write `progress/[target_agent].md` with this exact content:

    ```
    ## Wrapped
    [current date and time]

    ## Context
    [task content from step 1]

    ## Next
    [next line from step 1]

    ## Learned
    None

    ## Spec Sync
    None
    ```

    **Step C — Confirm:**
    Return ONLY: `Saved to progress/[target_agent].md`
    ---

    Print whatever the sub-agent returns. Session continues.
  </step>

</handoff-steps>
