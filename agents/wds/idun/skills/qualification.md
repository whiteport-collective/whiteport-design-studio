---
name: qualification
description: Turns an opening conversation into a confirmed setup scope (project, people, governance depth, Agent Space or not) before anything is written.
agent: idun
version: 1.0
tools: []
---

# Qualification

The front door. It should feel like a conversation, not an intake form. Idun's judgment decides which questions are needed, what scope the answers imply, and when enough is known to summarize. A solo project stays light. An organization gets more depth only when real signals call for it.

The confirmed summary is the source of truth for everything after it. Org onboarding acts on it without reopening discovery.

---

<workflow id="qualification">

  <constraints>
    - One question per message. If an answer already covers an upcoming question, skip that question.
    - Infer scope silently. Never offer Solo / Team / Enterprise as a menu.
    - Do not ask which WDS agents to install. Saga, Freya, Mimir and Idun are all included. Custom agents are a later librarian task.
    - Do not ask about governance without an organization signal. Do not ask about integrations below team scope.
    - Agent Space is optional. Never assume it, never assume a backend. WDS works from the repo alone.
    - Write nothing, create nothing, configure nothing before the summary is confirmed.
    - The summary stays in the conversation. If the session ends first, it goes into the wrap handover.
  </constraints>

  <step id="1-open">
    Ask:

    > Tell me: what are you building, and who's involved?

    That one answer usually reveals the project type, the scale and the team. Let it drive what comes next.
  </step>

  <step id="2-infer-scope">
    Read the signals. Do not show this table.

    | Signal | Scope |
    |---|---|
    | "just me", "solo", "personal project", "trying it out" | Solo |
    | "small team", "2–3 people", "startup", a partner or two | Team |
    | "company", "department", "employees", "clients", several repos | Organization |
    | "compliance", "regulated", "GDPR", "audit", public sector, personal data at scale | Organization + governance |
    | "pilot", "proof of concept" | Solo or team. Keep it light |

    If the person is only exploring WDS in a single repo, that is fine. Keep it to the solo path.
  </step>

  <step id="3-follow-up">
    Ask only what is still unknown, one question at a time, in this order:

    1. **Project name and repo.** Is there a repo already, or should one be created? One project or several in it?
    2. *(Team+)* **People.** "Who else is on the team? Names and roles."
    3. *(Organization)* **The organization.** "What does the organization do, and who are its customers?" Enough for an org profile, no more.
    4. *(Organization)* **Governance.** "Do you need an AI governance framework? It covers acceptable use, data handling and who decides what. The lean version takes about 20 minutes." If no: move on immediately.
    5. *(Team+)* **Realtime.** Only if several people or machines need live presence, messages or handoff tokens between sessions: "Do you want Agent Space for live coordination, or is the repo enough?" The repo is enough for most teams. If they want it, ask where it should run: 1 person on 1 machine (local), several machines (cloud), or an existing company standard. Never assume a vendor.
    6. *(Team+)* **Integrations.** "Which tools should the agents work with? Email, calendar, GitHub, meeting transcripts, a CMS?" These become tool files later. Note them, don't configure them.

    Stop when you know: project, repo, people, scope, governance yes/no, Agent Space yes/no.
  </step>

  <step id="4-summary">
    Present:

    ```
    Here's what I'll set up:

    **Project:**      [name] — [one line]
    **Repo:**         [existing path / new repo name]
    **Scope:**        [solo / team / organization]
    **People:**       [names and roles, or "just you"]
    **Organization:** [name, or —]
    **Governance:**   [none / lean / standard / full suite]
    **Agent Space:**  [not used / wanted: where]
    **Integrations:** [list, or "none for now"]

    Ready to proceed?
    ```

    Governance depth: lean for 1–2 people, standard for 3–10, full suite (`governance-report`) for 10+ or regulated work. Say which and why in one line if it isn't obvious.

    If the person corrects anything: adjust and confirm again.
  </step>

  <step id="5-route">
    On confirmation, update `phases.qualification: done` once the outline exists, and continue:

    | Situation | Next |
    |---|---|
    | No workspace yet, or a partial one | `skills/org-onboarding.md` with the summary |
    | Workspace exists, a new person | `skills/user-onboarding.md` |
    | Workspace exists, a new project | `skills/project-setup.md` with the summary |
    | Full governance suite chosen | Org onboarding first, then `skills/governance-report.md` |

    If the session ends before onboarding: wrap with the summary under `## Nästa`, to Idun.
  </step>

</workflow>
