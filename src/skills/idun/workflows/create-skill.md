---
skill: create-skill
agent: idun
---

# Create Skill Workflow

Walks through creating a new skill from scratch. Dialog-driven — Idun asks questions, proposes structure, writes files, registers in the library.

---

<workflow id="create-skill">

  <constraints>
    - One question at a time. Do not dump a questionnaire.
    - Propose the structure before writing any files. User confirms before execution.
    - Every skill MUST have a workflow file with WML (`<workflow>`, `<constraints>`, `<step>`).
    - Tools MUST be referenced by abstract capability, not implementation name.
    - If the skill produces output, it needs a template or at least a format description.
    - Register in sync manifest after files are written — never before.
  </constraints>

  <step id="1-intent">
    Ask: "What should this skill accomplish? Who uses it?"

    Capture:
    - **Purpose**: one sentence describing what the skill does
    - **Owner agent**: which agent will have this skill (saga, freya, mimir, idun, *, etc.)
    - **User**: who triggers it (human, another agent, automated)

    If the user already described the skill in their message, extract instead of asking.
  </step>

  <step id="2-triggers">
    Ask: "How is this skill activated?"

    Options:
    - Slash command (`/agent skill-name`)
    - Condition (agent detects a situation)
    - Handoff (another agent delegates)
    - Manual (user asks in conversation)

    Capture the trigger pattern and any arguments.
  </step>

  <step id="3-workflow-design">
    Design the workflow steps. For each step:
    - What does the agent do?
    - What input does it need?
    - What output does it produce?
    - What can go wrong? (exception handling)
    - What happens next? (routing)

    Present the proposed workflow as a numbered list:

    "Here's the workflow I'd write:
    1. {step} — {what happens}
    2. {step} — {what happens}
    ...
    Constraints: {list}

    Look right?"

    Wait for confirmation or adjustments.
  </step>

  <step id="4-tools">
    Identify which abstract capabilities this skill needs:
    - File read/write
    - Web search/fetch
    - Browser interaction
    - Database access
    - Agent Space messaging
    - Sub-agent spawning
    - External API (toolbox)

    List them in the workflow constraints. Do NOT name specific MCP tools — use capabilities.
  </step>

  <step id="5-templates">
    If the skill produces structured output:
    - Define the output format (markdown template, JSON schema, etc.)
    - Show an example of what great output looks like

    If the skill is purely conversational (no artifact), note that explicitly.
  </step>

  <step id="6-sub-agents">
    Evaluate: would any step benefit from a sub-agent?

    Use a sub-agent when:
    - A step requires loading large context that would bloat the main workflow
    - A step is parallelizable (multiple independent analyses)
    - A step is reusable across other workflows

    If yes, create the sub-agent file(s) in `agents/` alongside the workflow.
    If no, note it and move on.
  </step>

  <step id="7-write">
    Write the skill files:

    1. **Workflow file**: `src/skills/{agent}/workflows/{skill-name}.md`
       - Frontmatter: `skill: {name}`, `agent: {agent}`
       - WML: `<workflow>` with `<constraints>` and numbered `<step>` elements
       - Each step has clear input, action, output, and exception handling

    2. **Sub-agent files** (if any): `src/skills/{agent}/agents/{sub-agent}.md`

    3. **Template files** (if any): `src/skills/{agent}/references/{template}.md`

    Show the user what was written: file paths and a brief summary of each.
  </step>

  <step id="8-register">
    Register the new skill:

    1. Update `src/sync-manifest.json` — add entries for all new files
    2. Update the agent's SKILL.md — add the new skill to the skills list
    3. Run `node tools/sync-from-manifest.js` to compile and push to Agent Space
    4. Verify: confirm the instruction bundle was updated

    Report: "Skill '{name}' created and registered. {N} files written. Synced to Agent Space."
  </step>

</workflow>
