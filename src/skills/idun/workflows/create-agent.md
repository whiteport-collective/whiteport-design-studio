---
skill: create-agent
agent: idun
---

# Create Agent Workflow

Creates a new WDS agent from scratch. Dialog-driven — Idun guides through identity, domain, skills, tools, and activation.

---

<workflow id="create-agent">

  <constraints>
    - One question at a time. Build the agent through conversation.
    - Agent identity MUST include: name, pronouns, icon, tone, domain scope.
    - Every agent MUST have: SKILL.md, activation file, tools.md, instructions.md.
    - Agents MUST be registered in both WDS (sync manifest) and W-A-S (agent folder).
    - Do NOT duplicate skills between agents. Assign existing skills or create new ones.
    - Agent names follow the Norse mythology theme (Saga, Freya, Mimir, Idun, etc.) unless the user specifies otherwise.
    - Create a user record in Agent Space (users table) for the new agent.
  </constraints>

  <step id="1-identity">
    Ask: "What agent do you want to create? Tell me about them."

    Capture through conversation:
    - **Name**: the agent's name (suggest Norse mythology if none given)
    - **Pronouns**: she/her, he/him, they/them
    - **Icon**: emoji that represents the agent
    - **Tone**: how the agent communicates (precise, warm, direct, playful, etc.)
    - **One-liner**: what the agent does in one sentence

    If the user gives a rich description, extract all of the above. Only ask what's missing.
  </step>

  <step id="2-domain">
    Ask: "What is this agent's domain? What competency do they own?"

    Capture:
    - **Domain**: `wds` (product work) or `business` (operations) or new domain
    - **Competency**: what area of expertise (strategy, design, implementation, finance, etc.)
    - **Boundaries**: what is explicitly NOT this agent's job

    Map to existing WDS phases if applicable (1-8).
  </step>

  <step id="3-skills">
    Ask: "What skills does this agent need?"

    Options for each skill:
    - **Assign existing**: pick from the skill library (`/idun catalog`)
    - **Create new**: invoke the create-skill workflow for each new skill
    - **Shared**: assign shared skills (handover-protocol, messaging, work-orders)

    Every agent gets these shared skills by default:
    - agent-space/messaging
    - agent-space/work-orders
    - shared/handover-protocol
  </step>

  <step id="4-tools">
    Based on the domain and skills, determine the tool inventory:

    Write `tools.md` following the delegate access model:
    - **Delegates to**: which human user
    - **Default tools**: tools the agent uses in normal operation
    - **Toolbox**: Agent Space tools available via HTTP
    - **Elevated access**: any special permissions (like Idun's sync authority)
  </step>

  <step id="5-activation">
    Write the activation file (`src/skills/{agent}.activation.md`):

    The activation MUST handle:
    - **Fresh start**: no prior context, full boot
    - **Resume**: handoff token from another session
    - **Boot from Agent Space**: session-start API call

    Follow the pattern from existing activations (saga.activation.md, freya.activation.md).
  </step>

  <step id="6-write-files">
    Create the agent across both repos:

    **WDS repo** (`whiteport-design-studio`):
    - `src/skills/{agent}/SKILL.md` — capabilities, identity, quality criteria
    - `src/skills/{agent}.activation.md` — boot sequence
    - `src/skills/{agent}/workflows/` — one file per skill (if new skills created)
    - `src/agents/{agent}.agent.yaml` — persona definition
    - Update `src/sync-manifest.json` — add all new entries

    **W-A-S repo** (`whiteport-agent-space`):
    - `agents/{namespace}/{agent}/instructions.md` — org-level context
    - `agents/{namespace}/{agent}/tools.md` — tool inventory
    - `agents/{namespace}/{agent}/skills.md` — skill manifest (slug list)

    Show the user a file tree of everything that will be created. Confirm before writing.
  </step>

  <step id="7-register">
    Register the agent in all systems:

    1. **Agent Space user**: Create user record via SQL
       ```sql
       INSERT INTO users (id, org_id, user_type, email, display_name, role, status, agent_preferences)
       VALUES ('{uuid}', '{org}', 'agent', '{agent}@agent.whiteport.com', '{Name}', 'agent', 'active',
         '{"tool_delegate": "{human_uuid}", "pronouns": "{pronouns}", "icon": "{icon}", "domain": "{domain}"}'::jsonb)
       ```

    2. **Sync WDS**: `node tools/sync-from-manifest.js --agent {agent}`
    3. **Sync W-A-S**: `node sync.js --agent {agent}` (from W-A-S repo)
    4. **Verify**: check Agent Space for the new instruction bundles

    Report: "Agent {Name} created. {N} files across 2 repos. Registered in Agent Space. Ready to activate with /{agent}."
  </step>

</workflow>
