# /handoff — Cross-Agent Handoff

Send a structured handoff to another WDS agent. Does NOT wrap the session — use when passing a specific piece of work to a different agent while the current session continues (or as an explicit cross-agent wrap).

**Usage:** `/handoff [target-agent]`
**Example:** `/handoff mimir`

> **Handoffs go through Agent Space — never as files on disk.**
> Writing handoff content to arbitrary files on the hard drive is not a handoff. It is untracked state that other agents cannot reliably find, and it creates noise in the repo. Agent Space is the single source of truth for cross-agent communication.

---

<handoff-steps>

  <constraints>
    - Derive everything from the conversation. Do NOT ask questions.
    - No output between steps — only what the steps explicitly say to print.
    - This is NOT a session wrap. Do not update presence, do not write session-wrap.md.
    - Handoff MUST be sent to Agent Space. If the curl call fails, warn the user — do not fall back to writing a file.
  </constraints>

  <step id="1-resolve">
    Determine:
    - `from_agent` — your current agent_id (e.g. freya-d660de). If not known, use base name (freya).
    - `target_agent` — from the argument (e.g. mimir). If no argument: infer from conversation context.
      - Working on a brief being handed to design → freya
      - Handing a Work Order to implementation → mimir
      - Handing strategy/brief work → saga
    - `project` — current project repo name (e.g. sharif-webshop).

    Compose the handoff content — what the receiving agent needs to know to start immediately:
    ```
    ## Context
    [What was done. What exists and where. Be specific about file paths and state.]

    ## Next:
    [Single immediately-actionable next task for the receiving agent. Concrete — file, action, criterion.]
    ```

    The `## Next:` line is what the receiving agent's boot flow will surface. Make it precise.
  </step>

  <step id="2-send">
    Run this curl command (silent output, capture response):

    ```bash
    curl -s -X POST "https://uztngidbpduyodrabokm.supabase.co/functions/v1/agent-messages" \
      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV6dG5naWRicGR1eW9kcmFib2ttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI1MTc3ODksImV4cCI6MjA4ODA5Mzc4OX0.FNnTd5p9Qj3WeD0DxQORmNf2jgaVSZ6FU1EGy0W7MRo" \
      -H "Content-Type: application/json" \
      -d '{
        "action": "send",
        "from_agent": "[from_agent]",
        "to_agent": "[target_agent]",
        "project": "[project]",
        "subject": "Handoff from [from_agent]",
        "content": "[handoff content — escaped for JSON]",
        "message_type": "handoff"
      }'
    ```

    Parse the `id` field from the JSON response.
    Take the first 6 characters of the UUID — this is the handoff token.

    **If the curl call fails or returns an error:**
    Stop and warn the user:
    ```
    ⚠️ Agent Space unreachable — handoff not sent.
    The handoff content is ready but could not be delivered.

    To fix: check that Agent Space credentials are active.
    Tip: open Bitwarden and verify the Agent Space API key is present and not expired.

    Handoff content (copy if needed):
    [handoff content]
    ```
    Do NOT write the handoff to a file on disk. Wait for the user to resolve connectivity.
  </step>

  <step id="3-show">
    Print EXACTLY this block — nothing before, nothing after:

    ── Handoff ───────────────────────────────────
    To:      [target_agent]
    Next:    [the ## Next: line you composed]
    Token:   /[target_agent] [6chars]
    ──────────────────────────────────────────────

    Session continues. The receiving agent boots with `/[target_agent] [6chars]`.
  </step>

</handoff-steps>
