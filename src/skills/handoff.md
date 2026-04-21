# /handoff — Cross-Agent Handoff

Pass a specific piece of work to another WDS agent. This is NOT a session wrap — it is a targeted transfer of one task or artifact to a different agent.

**Usage:** `/handoff [target-agent]`
**Example:** `/handoff mimir`

> **Handoffs go through Agent Space — never as files on disk.**
> Writing handoff content to arbitrary files is not a handoff. It is untracked state other agents cannot reliably find. Agent Space is the single source of truth for cross-agent communication.

---

<handoff-steps>

  <constraints>
    - Derive everything from the conversation. Do NOT ask questions.
    - Do NOT summarize this session. That is a wrap, not a handoff.
    - Focus only on what the receiving agent needs to start the specific task immediately.
    - The sub-agent handles all Agent Space delivery. You only compile and show.
  </constraints>

  <step id="1-compile">
    Determine:
    - `target_agent` — from the argument. If none: infer from context (strategy work → saga, design → freya, implementation → mimir).
    - `from_agent` — your current agent base name (e.g. freya, saga).
    - `project` — current project repo name.

    Compose the handoff content — what the receiving agent needs to start immediately:

    ```
    ## Task
    [Single specific task being handed off. What it is, what state it's in, what remains.]

    ## Files
    [Relevant file paths and what's in them. Be exact.]

    ## Next
    [Single immediately-actionable next step for the receiving agent.]
    ```

    This is task context, not session history. If the receiving agent doesn't need to know something to do the task, leave it out.
  </step>

  <step id="2-show">
    Print EXACTLY this block:

    ── Handoff to [target_agent] ─────────────────
    Task:    [one-line task description]
    Next:    [the Next line you composed]
    ──────────────────────────────────────────────

    Then proceed immediately to step 3.
  </step>

  <step id="3-subagent">
    Spawn a sub-agent with this exact prompt — substitute the bracketed values:

    ---
    You are a delivery agent. Your only job is to post a handoff to Agent Space and return the token.

    Send this request:

    ```bash
    curl -s -X POST "https://uztngidbpduyodrabokm.supabase.co/functions/v1/agent-messages" \
      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV6dG5naWRicGR1eW9kcmFib2ttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI1MTc3ODksImV4cCI6MjA4ODA5Mzc4OX0.FNnTd5p9Qj3WeD0DxQORmNf2jgaVSZ6FU1EGy0W7MRo" \
      -H "Content-Type: application/json" \
      -d '{
        "action": "send",
        "from_agent": "[from_agent]",
        "to_agent": "[target_agent]",
        "project": "[project]",
        "message_type": "handoff",
        "title": "[one-line task description]",
        "content": "[full handoff content — escaped for JSON]"
      }'
    ```

    If the call succeeds: extract the `id` field. Return ONLY the first 6 characters. Nothing else.

    If the call fails or returns an error: return ONLY this text:
    FAILED: [error message or HTTP status]
    ---

    Wait for the sub-agent response.

    **If sub-agent returns 6 characters:** print EXACTLY this — nothing before, nothing after:
    ```
    /[target_agent] [6chars]
    ```

    **If sub-agent returns FAILED:** stop and warn the user:
    ```
    ⚠️ Agent Space unreachable — handoff not sent.
    Check that Agent Space credentials are active (open Bitwarden → verify Agent Space API key).

    Handoff content (copy if needed):
    [full handoff content]
    ```
    Do NOT write the handoff to a file on disk.
  </step>

</handoff-steps>
