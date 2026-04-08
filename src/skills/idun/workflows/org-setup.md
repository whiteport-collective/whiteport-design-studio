---
skill: org-setup
agent: idun
---

# Org Setup Workflow

Sets up a new organization in the WDS ecosystem. This is the master onboarding workflow — every external client follows this sequence. Individual steps reference other workflows (user-onboarding, tool-onboarding) but this workflow controls the order and gates.

---

<workflow id="org-setup">

  <constraints>
    - Follow the phases in order. Each phase informs the next.
    - Do NOT skip ahead to infrastructure before governance is defined.
    - Do NOT register agents before the org-agent-space repo exists.
    - Adapt governance depth to the org's size and complexity — lean for small teams, full for enterprises.
    - Guide the user through git setup if they are not familiar with it.
    - The user types `meta:` to give process feedback — edit this workflow or related files immediately when that happens.
  </constraints>

  <step id="1-understand-business">
    Understand the organization before touching any systems.

    Gather:
    - **What does the org do?** (industry, services, clients)
    - **Who are the people?** (partners, employees, roles, technical skill levels)
    - **How does money flow?** (revenue model, invoicing, settlements)
    - **What is the current workflow?** (tools, processes, pain points)
    - **What should agents handle?** (automation goals, what humans do today that agents could do)
    - **What is the org's relationship to Whiteport?** (client, partner, internal)

    Deliverable: Business profile written to `{org}-agent-space/org-profile.md`

    Gate: User confirms the profile is accurate before proceeding.
  </step>

  <step id="2-connect-infrastructure">
    Before creating repos or deploying anything, ensure the agent session has the credentials it needs.

    1. **GitHub CLI (`gh`)** — required for creating repos, PRs, issues, project boards
       - Run `gh auth login` — walk the user through the browser flow
       - Verify: `gh auth status` shows the correct org
       - If the org uses SSO: `gh auth refresh -s admin:org` may be needed

    2. **Git identity** — verify `git config user.name` and `git config user.email` are set
       - If user is new to git: walk through install, config, SSH key setup

    3. **Supabase CLI** (if deploying edge functions later)
       - `npx supabase login` or confirm access token in env
       - Can be deferred to step 5 if not needed yet

    4. **Other tool credentials** — check what the org needs (hosting APIs, email, etc.)
       - Document in `.env` or credential manager
       - Never commit secrets to repos

    Gate: `gh auth status` succeeds for the org. `git push` works.
  </step>

  <step id="3-create-org-and-repo">
    Create the org's home:

    1. **Create `{org}-agent-space` repo** on GitHub:
       ```bash
       gh repo create {github-org}/{org}-agent-space --private --clone
       ```
       - If user is new to git: walk them through install, config, SSH key, first commit
       - Structure:
         ```
         {org}-agent-space/
         ├── org-profile.md          ← From step 1
         ├── finance/                ← Org-level financials (agreements, monthly settlements)
         ├── ai-governance/          ← From step 4
         ├── access-audit/           ← People and repo access maps
         └── README.md               ← What this repo is and who owns it
         ```

    2. **Move org-level files** from work repo to agent-space repo:
       - Finance (agreements, monthly settlements) → `{org}-agent-space/finance/`
       - Org profile → `{org}-agent-space/org-profile.md`
       - Keep client work, analysis data, and scripts in the work repo

    3. **Register org in Whiteport Agent Space** as a client (not as an org — the org gets its own space)

    Gate: Repo exists, user can push to it.
  </step>

  <step id="4-governance-framework">
    Create the governance framework in `{org}-agent-space/ai-governance/`.

    Scale governance to the org:

    **Lean (2 partners, no employees, simple business):**
    - 00-introduction.md — What AI agents do here, who is responsible
    - 01-data-handling.md — What data agents access, where it goes, client confidentiality
    - 02-agent-authorization.md — Which agents exist, what they can do, who approves changes
    - 03-access-control.md — Who has access to what (people + agents)
    - 04-agent-asset-organization.md — How we structure agents, skills, tools, templates — and why

    **04 is always included at every scale.** It captures the org's chosen catalog structure,
    the reasoning behind it, and ownership boundaries. A solo dev gets "flat, one person, no layers."
    An enterprise gets "by region → department, inherited governance." Idun writes this from the
    onboarding dialog — it is not a template, it is a document she produces from conversation.

    **Standard (small team, 3-10 people):**
    - Add: 04-incident-response.md, 05-vendor-management.md

    **Enterprise (10+ people, external stakeholders):**
    - Full 12-doc framework (see WDS-E governance template)

    Also create:
    - `access-audit/people-access-map.md` — Every person, their role, what they can access
    - `access-audit/repo-access-map.md` — Every repo, who has access

    Deliverable: Governance docs committed to {org}-agent-space repo.
    Gate: At least one non-technical stakeholder has read and approved the introduction doc.
  </step>

  <step id="5-install-agents-and-skills">
    Install the agent roster, skills, users, and templates in the org's work repo.

    1. **Define agent roster** — which agents does this org need?
       - Map business needs (from step 1) to agent capabilities
       - Reuse existing WDS agents where possible
       - Create org-specific agents only when needed

    2. **Register people** — run user-onboarding workflow for each person
       - Owners/admins first, then members
       - Non-technical users get a simple guide, not a SQL walkthrough

    3. **Install skills** — use the micro skill / workflow skill pattern:

       **Micro skills** — domain knowledge, reusable across workflows:
       - Small, focused, one concept each (e.g., `seo-title-optimization`, `seo-heading-structure`)
       - Platform-agnostic — describe WHAT to do, not HOW on a specific system
       - Referenced by workflow skills, never executed directly by users
       - Live in the work repo under `_bmad/{org}/skills/micro/`

       **Workflow skills** — CMS/platform-specific, user-facing:
       - Reference micro skills for domain knowledge
       - Add platform mechanics, APIs, sub-agents for implementation
       - Each platform gets its own skill (e.g., `seo-optimize-wordpress`, `seo-optimize-joomla`)
       - Live as slash commands in `.claude/commands/`

       **Business skills** — org-specific operations:
       - Invoicing, settlement, pipeline tracking, etc.
       - Also live as slash commands

       Register all skills in Agent Space

    4. **Create templates** — for recurring outputs:
       - Invoices, reports, client communication, etc.
       - Templates live in the work repo, registered in Agent Space

    5. **Write onboarding guide for non-technical users** — how to interact with agents:
       - What agents exist and what they do
       - How to give them work (slash commands, natural language)
       - How to check on progress
       - Who to ask when something goes wrong

    Deliverable: Agents operational in the work repo, all people registered, skills assigned.
    Gate: Each agent boots successfully and can perform its primary task.
  </step>

  <step id="6-implement-agent-space">
    Set up Agent Space infrastructure for the org.

    1. **Database** — create or configure Supabase project (or selected database):
       - Run migrations for Agent Space tables
       - Configure Row Level Security for the org
       - Set up edge functions (session-start, messaging, etc.)

    2. **Connect to work repo** — ensure agents in the work repo boot against this org's Agent Space:
       - Update agent YAML files with correct Supabase URL and anon key
       - Test session-start from the work repo
       - Verify skill loading from Agent Space

    3. **Connect tools** — run tool-onboarding for each tool the org needs:
       - Email, calendar, hosting APIs, etc.
       - OAuth flows for human users
       - Agent delegation for agent users

    4. **End-to-end test** — verify the full loop:
       - Agent boots → loads skills → performs task → captures knowledge → sends message
       - Non-technical user can trigger an agent and get a result

    Deliverable: Agent Space operational, all agents connected, verified end-to-end.
    Gate: A real task (not a test) completes successfully through the agent pipeline.
  </step>

</workflow>
