---
skill: register
agent: idun
---

# Register to Library Workflow

Takes an existing skill file and registers it in the WDS skill library. Validates, classifies, adds to manifest, and syncs.

---

<workflow id="register">

  <constraints>
    - Never register a file that doesn't parse correctly. Validate first.
    - The original file stays where it is. Registration adds it to the manifest (it may already be in the right location).
    - If the file is outside the WDS repo, copy it to the correct location first.
    - Registration is idempotent — re-registering an existing entry updates it.
    - Always sync after registering. A manifest entry without a sync is incomplete.
  </constraints>

  <step id="1-locate">
    Read the file at the given path.

    Common sources:
    - `~/.claude/commands/` — local Claude commands
    - Project repo `src/skills/` — already in the library structure
    - Any absolute path the user provides

    If the path doesn't exist, ask the user to provide the correct path.
  </step>

  <step id="2-classify">
    Determine what type of artifact this is:

    | Type | How to identify |
    |------|----------------|
    | **skill** | Has frontmatter with `skill:` field, contains `<workflow>` WML |
    | **workflow** | Has `<workflow>` WML but is subordinate to a skill |
    | **agent** (sub-agent) | Defines a stateless specialist, no activation sequence |
    | **reference** | Documentation, guide, template — no WML |
    | **activation** | Boot sequence with `<activation>` XML |
    | **persona** | YAML with `agent.metadata` and `agent.persona` |

    If ambiguous, ask the user.
  </step>

  <step id="3-identify-owner">
    Determine which agent(s) should have access:

    - Named agent (e.g., `saga`) — only that agent gets it
    - `*` (shared) — all agents receive it
    - Multiple agents — register once per agent

    If the file has frontmatter with `agent:` or `agents:`, use that.
    Otherwise ask: "Which agent should own this?"
  </step>

  <step id="4-validate">
    Run the Skill Validator sub-agent (`agents/skill-validator.md`) if available.

    Check:
    - [ ] Frontmatter is valid (name, skill, agent fields)
    - [ ] WML structure is correct (if applicable)
    - [ ] Tools referenced by capability, not implementation
    - [ ] No hardcoded paths or credentials
    - [ ] File is in the correct location for its type

    If validation fails: show findings, ask user to fix or register anyway.
  </step>

  <step id="5-place">
    Ensure the file is in the correct WDS repo location:

    | Type | Location |
    |------|----------|
    | skill | `src/skills/{agent}/SKILL.md` |
    | workflow | `src/skills/{agent}/workflows/{name}.md` |
    | agent | `src/skills/{agent}/agents/{name}.md` |
    | reference | `src/skills/{agent}/references/{name}.md` |
    | activation | `src/skills/{agent}.activation.md` |
    | persona | `src/agents/{agent}.agent.yaml` |

    If the file is already in the right place, skip.
    If it needs to move/copy, show the user and confirm.
  </step>

  <step id="6-manifest">
    Update `src/sync-manifest.json`:

    ```json
    {
      "agent": "{agent-id or *}",
      "type": "{type}",
      "file": "{relative-path}",
      "channel": "stable",
      "changelog": "{one-line description}"
    }
    ```

    Check for duplicates first — if the file is already in the manifest, update the entry.
  </step>

  <step id="7-sync">
    Push to Agent Space:

    ```bash
    node tools/sync-from-manifest.js --agent {agent}
    ```

    Verify the instruction bundle was updated. Report the new compiled size.

    "Registered {type} '{name}' for {agent}. Synced to Agent Space ({N} chars compiled)."
  </step>

</workflow>
