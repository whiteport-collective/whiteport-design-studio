---
skill: catalog
agent: idun
---

# Skill Catalog Workflow

Lists everything in the skill library with status. The inventory of what exists, who owns it, and whether it's current.

---

<workflow id="catalog">

  <constraints>
    - Read from the actual files and manifest — never from memory.
    - Show sync status by comparing manifest to Agent Space.
    - If filtered by agent, still show shared (*) skills that the agent receives.
    - Keep output as tables — scannable, not verbose.
  </constraints>

  <step id="1-gather">
    Read the current state from three sources:

    1. **Manifest**: `src/sync-manifest.json` — what's registered
    2. **Files**: `src/skills/` directory tree — what exists on disk
    3. **Agent Space**: query `agent-instructions` (list-skills action) — what's deployed

    Also read:
    - `src/.sync-state.json` — last sync timestamp and hashes
    - W-A-S `agents/` — org-level configs per agent
  </step>

  <step id="2-compile">
    Build the catalog data:

    **Per agent:**
    - Agent name, domain, icon
    - Skills assigned (from manifest)
    - Workflow files (exist? / missing?)
    - Sub-agents
    - References
    - Compiled instruction size (chars)
    - Last synced to Agent Space (from sync state)
    - Stale? (files changed since last sync)

    **Shared (*):**
    - Skills, workflows, references available to all agents

    **Toolbox:**
    - Registered tools from plugin_catalog
    - Status per org (active/planned/disabled)

    **Users:**
    - From W-A-S `org/users.md` or Agent Space users table
  </step>

  <step id="3-display">
    Output the catalog as tables.

    If no agent filter:

    ```
    ## Agents
    | Agent | Domain | Skills | Workflows | Sub-agents | Size | Synced | Stale? |
    |-------|--------|--------|-----------|------------|------|--------|--------|

    ## Shared Skills
    | Skill | Type | File | Channel |
    |-------|------|------|---------|

    ## Toolbox
    | Tool | Version | Status | Actions |
    |------|---------|--------|---------|

    ## Users
    | Name | Type | Role | Domain | Delegates to |
    |------|------|------|--------|-------------|
    ```

    If filtered by agent name:

    ```
    ## {Agent Name} — {domain}
    | Skill | Type | File | Exists? | In Manifest? | In Agent Space? |
    |-------|------|------|---------|-------------|----------------|

    ## Quality Check
    [Run a quick inline audit: 5 criteria, PASS/FAIL only]
    ```
  </step>

  <step id="4-actions">
    After displaying the catalog, suggest next actions if issues found:

    - Missing workflow files → "Want me to create them?"
    - Stale sync → "Want me to run sync?"
    - Unregistered files on disk → "Want me to register these?"
    - Failed quality checks → "Want me to run a full audit?"

    If everything is clean: "Library is current. {N} agents, {N} skills, {N} tools. All synced."
  </step>

</workflow>
