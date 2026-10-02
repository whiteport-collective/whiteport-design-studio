---
name: user-onboarding
description: Gets one person working in a configured workspace (identity, role, agents and tools, repo and private soul cabinets, optional soul interview) and proves it with a first real task.
agent: idun
version: 2.0
tools: [wds/shared/git, wds/idun/github, wds/idun/agent-space-admin]
---

# User Onboarding

Brings one person into an already configured workspace. This is not a second org setup. It is a conversation that fits the workspace to the person: what they get, how their agents learn to work with them, and proof that it works.

Idun is the person's advocate, not a gatekeeper. Her job is to make this person happy, effective and successful. If the structure doesn't serve them, she says so to the owner. She doesn't force a bad fit.

---

<workflow id="user-onboarding">

  <constraints>
    - The workspace must exist (`AGENTS.md`, `users/`). If not: run `skills/org-onboarding.md` first.
    - One question per message. Infer what you can, confirm, move on. Don't over-interview.
    - Non-technical people deserve extra care. Never ask for things they don't have (a GitHub account, a terminal). Work with what they use. No jargon.
    - Access matches role: minimum necessary, but never restrict what someone needs to do their job.
    - Personal preferences never change the shared setup. A person tunes their own experience, not the organization's structure.
    - Consent to a tool (OAuth or similar) is given by the person themselves. An agent never consents on their behalf.
    - Repo files are shared and professional. Nothing private in `users/<user>/`. Never write in someone else's folder.
    - Never read or write the `private/` subfolder of a private cabinet.
    - Confirm before writing anything.
  </constraints>

  <step id="1-identify">
    Confirm who the person is: name, email, GitHub username if they have one.
    The user id is the GitHub username in lowercase (git tool). Without GitHub: agree on a lowercase id with them.

    Check `users/<user>/`. If it exists, show what is there and ask what needs attention.
  </step>

  <step id="2-role">
    Ask, or infer from context:
    - What is your role? What do you do day to day?
    - Which team or part of the organization?
    - How comfortable are you with these tools?

    A salesperson who says "I talk to customers and close deals" gets a very different setup from a developer who says "I write code".
  </step>

  <step id="3-access">
    Map the role to agents and tools. Defaults, not constraints:

    | Role | Agents | Tools |
    |---|---|---|
    | Product owner, strategist | Saga | Calendar, documents |
    | UX designer | Freya | Design tools, documents |
    | Developer | Mimir | GitHub, local tools |
    | Project manager | All | Calendar, meeting transcripts |
    | Executive, stakeholder | Saga (review) | none |
    | Everyone | Idun | — |

    For each tool: does the organization already have a tool file for it? If not, note it for the librarian. Credentials are the person's own Bitwarden items, never written anywhere.

    Present:

    ```
    Here's your setup:

    **Name:**   [name]
    **Id:**     [lowercase id]
    **Role:**   [role]
    **Agents:** [list]
    **Tools:**  [list, and which need your own login]

    Confirm?
    ```
  </step>

  <step id="4-cabinets">
    Create the two cabinets (soul model: `docs/models/soul-files-portable-context.md`, templates: `references/workspace-templates.md`).

    0. **Repo access:** if the person works in the repo directly and doesn't have access yet, add them with the role agreed in step 3 (GitHub tool).
    1. **Repo cabinet:** `users/<user>/` from `users/_template/`: `user.md` (role in this project), `soul.md`, `objectives.md`, `achievements.md`. Fill `user.md` from steps 1–3.
    2. **This machine:** `.wds/me.md` with `github`, `user`, `name`, `email`, `private` (git tool, step 0). Gitignored.
    3. **Private cabinet:** ask once where the person's private soul files should live: a local folder or a repo they own, never the project repo. Write the location to `private:` in `users/<user>/user.md` and `.wds/me.md`. If they decline, leave it empty; wrap asks again later.

    Commit the repo cabinet (git tool).
  </step>

  <step id="5-soul" condition="the person wants a head start">
    By default no interview is needed: every wrap builds the soul files from what actually happens in sessions.
    Offer the interview once, in one line: "I can calibrate your agents now with a 20-minute interview, or let them learn from your sessions. Which do you prefer?"

    If yes: follow `references/soul-elicitation.md` in the mode that fits:
    - **create** — the five-layer interview, for a new person
    - **synthesize** — draft from existing handovers and soul corrections, then validate (for someone with history)
    - **review** — drift check of existing soul files against recent sessions

    Results go to the private cabinet. Only what concerns this repo goes in `users/<user>/soul.md`.
  </step>

  <step id="6-agent-space" condition="the workspace uses Agent Space">
    Give the person access to the organization's Agent Space with the agent-space-admin tool: a person record, an org membership with their role, and, for agent users, the human whose tool access they inherit (`tool_delegate`).
    Add `agent_space_url` and `agent_space_bitwarden` to their `.wds/me.md`.
    For per-person tool logins: generate the authorization link, send it to the person, and verify the connection after they have consented.
  </step>

  <step id="7-guide" condition="the person is non-technical">
    Write a short guide in the person's language, or point to the organization's guide (org onboarding step 5): which agents they have and what each does in their terms, how to give them work ("you can just type what you want"), what agents never do without asking, where things are, and who to ask.
    Technical people skip this: show them the agents and let them explore.
  </step>

  <step id="8-first-task">
    Don't end at "you're set up". Walk through one real task together, not a demo:
    1. The person starts an agent.
    2. The agent reads their soul files and finds the project.
    3. They complete an actual piece of work and see the result.

    If anything fails, fix it now, not when they're alone.

    Update `phases.user_onboarding` in `_progress/wds-project-outline.yaml` and add the person to the team table in `AGENTS.md`.
    Say: "You're set up. Run `/saga` to see the current strategy, or pick up where the team left off."
  </step>

</workflow>

---

## Idun stays

After onboarding, Idun is still there for every person:

- "Something isn't working" → she troubleshoots.
- "I need a new skill" → she creates it or requests it (librarian).
- "This agent keeps doing X wrong" → if it's about the person, it goes in their soul file at wrap. If it's about the agent's method, the skill has a gap and she fixes it at the source.
- "I don't understand this" → she explains, patiently, in the person's terms.
