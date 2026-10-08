---
name: org-onboarding
description: Turns a confirmed qualification summary into a working WDS workspace, and for organizations into an org profile, a scaled governance set and onboarded people.
used_by: [idun]
version: 2.0
tools: [wds/git, wds/sync, wds/github]
---

# Org Onboarding

Takes Idun from a confirmed scope to a repo where people can start working with Saga, Freya and Mimir. For a solo project that is a few files and a handoff. For an organization it is a sequence of gated phases: understand the business, connect the basics, set up the workspace, scale governance, onboard people, and only then, if wanted, Agent Space.

**Understand before building.** Each phase informs the next. Skipping ahead produces wrong decisions.

---

<workflow id="org-onboarding">

  <constraints>
    - Start only from a confirmed qualification summary. Do not reopen questions it already answered.
    - Follow the phases in order. Each phase ends with a gate the person can see.
    - Scale to context. A solo developer never gets enterprise ceremony. An enterprise never gets a flat folder.
    - Facilitate, don't dictate. Structure principles are guidelines; record the organization's own decision and its reasons.
    - Check before writing: if a file exists, read it and update it. Never overwrite.
    - The WDS agents are installed from their source, never copied by hand or edited in the copy.
    - No keys in any file. Name the Bitwarden item, never the value. No MCP servers in sessions.
    - `meta:` from the person means the process itself is wrong: edit the source skill in whiteport-design-studio, not a local copy, then continue.
    - Commit and push after each phase (git tool).
  </constraints>

  <step id="1-understand-business" condition="scope is team or organization">
    Understand the organization before touching any systems. Gather through conversation, one question at a time:

    - What does the organization do? (industry, services, customers)
    - Who are the people? (partners, employees, roles, technical comfort)
    - What does the current workflow look like? (tools, processes, pain points)
    - What should agents handle? (what people do today that agents could take over)
    - What is its relationship to whoever runs the setup? (client, partner, internal)

    Read the room on depth. A two-person studio needs five sentences. A department needs a page.

    **Deliverable:** `shared/<org>/org-profile.md`, written once the workspace exists in step 3.
    **Gate:** the person confirms the profile is accurate.
  </step>

  <step id="2-connect-basics">
    Make sure the session can do what the setup needs. Use the git tool and the GitHub tool:

    1. Git identity is set (name and email) and matches the person.
    2. GitHub access works for the account or organization that will own the repo.
    3. Anything else the integrations need is noted with its Bitwarden item name. Nothing is stored in files.

    If the person is new to git: be patient and walk them through it. If they're experienced: move fast.

    **Gate:** the person can push to the repo, or to the GitHub account where it will be created.
  </step>

  <step id="3-workspace">
    Set up the WDS workspace. Templates: `../idun/references/workspace-templates.md`.

    1. **Repo.** Use the existing repo, or create one (GitHub tool). Private unless the person says otherwise.
    2. **`AGENTS.md`** with the team, the rules, the project table and the `output_folder`. `CLAUDE.md` points to it.
    3. **Projects.** One folder per project, each a separate WDS structure, made with `project-setup.md`
       (intake, where the code lives, `projects/<project>/` with its front page, outline and design log).
       Run its steps 2–4 for each project. The handover to Saga is written once, in step 8.
    4. **People.** `users/_template/`, `users/README.md`, `sessions/`, and `.wds/` in `.gitignore`.
    5. **Shared org material.** `shared/<org>/` with the org profile from step 1. Org scope only.
    6. **Agents.** Install the WDS agents and their adapters as described in "Installing in a project" in
       `agents/wds/README.md`, using the sync tool. Never copy them by hand.

    Show the file tree before writing. Write after a yes.

    **Gate:** `/saga` starts in the repo and finds the project.
  </step>

  <step id="4-governance" condition="governance was chosen in qualification">
    Scale governance to the organization. Start from the WDS default policy, never from blank pages: create
    `governance/<org>/` from `agents/wds/data/templates/governance/` at the root of the organization's source repo,
    and `governance/policies.md` from `agents/wds/data/templates/policies.md`, as in Step 0 of
    `governance-report.md`. One source repo per organization; its other repos get a read-only copy of
    `governance/<org>/` through the sync tool, and `governance/wds/` is the synced default. A folder with a
    `.source` file is never edited. Register the organization in the sync config (sync tool).
    Then tailor from the conversation: confirm or adjust each default, and list every difference in the
    differences table in `<org>/framework.md`.

    **Always (every scale that has governance):**
    - `<org>/framework.md` — scope, who is responsible, and what AI agents do here
    - `<org>/principles.md` — the default principles, confirmed or adjusted
    - `<org>/incidents.md` — at least the incident log, so wrap step 6 has somewhere to write
    - `governance/policies.md` — the reading order, with the incident log named
    - `<org>/agents.md`, section Skill governance — how agents, skills, tools and templates are organized, who owns what, and why.
      Written from the step 1 conversation. A solo developer gets three lines ("flat, one person, no layers"). A larger org
      gets its department structure and ownership boundaries. The decision and the reasoning are what matter.

    **Lean (1–2 people):** also tailor `<org>/data.md`, `<org>/agents.md` (authorization) and `<org>/access.md`.
    **Standard (3–10 people):** also tailor the rest of `<org>/incidents.md` and `<org>/tools.md`.
    Files that are not tailored stay as copied: the default applies to them until they are. Localized file names
    are fine (`governance/visita/ramverk.md`); `policies.md` lists them.
    **Full suite (10+ people, external stakeholders, regulated):** do not tailor the lean set here. Run `governance-report.md`, which owns the full dialog.

    Also write, for lean and standard:
    - `shared/<org>/access-audit/people-access-map.md` — every person, their role, what they can access
    - `shared/<org>/access-audit/repo-access-map.md` — every repo and who has access (GitHub tool reads the facts)

    **Gate:** the client's principal has read and approved `<org>/framework.md` at an agreed milestone, and its
    `Status:` line says so (`approved v<version> <date>, <role>`). Until then the status is `in progress`.
  </step>

  <step id="5-org-agents" condition="the organization needs its own agents, skills or tools">
    Map the business needs from step 1 to agent capabilities. Reuse the WDS agents first. Create organization agents, skills and tools only when needed, with the librarian (`librarian.md`), in their own source folder `agents/<org>/`, one folder per source. They never go inside `agents/wds/`.

    Write a short onboarding guide for non-technical people in the organization's language: which agents exist and what they do in their terms, how to give them work (commands and plain language), what agents never do without asking, where things are, and who to ask.

    **Gate:** each agent starts and can do its primary task.
  </step>

  <step id="6-people">
    Run `user-onboarding.md` for each person. Owners and admins first, then members.
    For three or more people, spawn setup workers for the file work (`../idun/subagents/setup-worker.md`) and keep the conversations yourself.

    **Gate:** each person can start an agent and complete a real task.
  </step>

  <step id="7-agent-space" condition="Agent Space was chosen in qualification">
    Agent Space comes last, because what it supports must exist first.

    - With the full governance suite: run `agent-space-install.md` once the suite is approved.
    - Without it (presence and handoff tokens only): add `agent_space_url` and `agent_space_bitwarden` to each person's
      `.wds/me.md` as described in `agents/wds/tools/agent-space.md`. Nothing goes in the repo.
  </step>

  <step id="8-handoff">
    Update `_progress/wds-project-outline.yaml` (`org_onboarding: done`, user_onboarding status, governance status) and add a line to the design log.

    Say:

    > All set. Run `/saga` to begin the strategy phase.

    If the session ends here, wrap with the handover to Saga (`sessions/<user>/saga/`), so `/saga <repo> <timestamp>` starts from the confirmed scope and each project's intake (`project-setup.md`, step 5).
  </step>

</workflow>

---

## Quality rules

- **Model first, apply second.** The workspace follows the WDS conventions. The organization is an instance of them, adapted to its context.
- **The agent asset organization is always recorded** (in `<org>/agents.md`, Skill governance) when there is governance. Three lines is fine. The decision must be recorded.
- **The confirmed qualification summary is the source of truth.** Discovery is not reopened.
- **Every phase ends with a clear gate.** The person knows what was done and what's next.
