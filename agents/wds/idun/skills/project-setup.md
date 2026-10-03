---
name: project-setup
description: Starts a new WDS project for a client. A short project intake, the project folder in the right repo, where the code lives, and a handover to Saga so the product brief starts from the intake.
agent: idun
version: 1.0
tools: [wds/shared/git, wds/shared/sync, wds/idun/github]
---

# Project Setup

Takes a new project from "we want to build X" to a project folder Saga can start in. Any client can run it, in any WDS repo. It is the project-level step of setup: qualification decides the scope, org onboarding builds the workspace, and this skill adds one project to it.

| Situation | Path |
|---|---|
| No WDS workspace yet | `skills/qualification.md`, then `skills/org-onboarding.md`. Org onboarding runs this skill for each project in its step 3. |
| A workspace exists, a new project | This skill directly (`/idun project`) |
| The project folder already exists | Show it and its status. Nothing is created. |

The layout follows `agents/wds/shared/data/repo-structure.md`: one project is one folder under `projects/`, a complete WDS structure of its own, and projects never share folders. What several projects share lives in `shared/<org>/`.

---

<workflow id="project-setup">

  <constraints>
    - One question per message. Skip any question the qualification summary or the handover already answered.
    - Confirm the summary before writing anything. No folders, repos or files before the person says yes.
    - Check before writing: if a file exists, read it and update it. Never overwrite.
    - The WDS agents are installed with the sync tool, never copied by hand. A real sync writes into other repos, so it runs only after the person's yes.
    - No credentials in any file. Name who has access and the password manager item, never the value.
    - The intake is shared and professional: it travels in the repo and can be read by the client. Commercial terms and private notes stay out of it.
    - Commit and push after each step that writes (git tool).
  </constraints>

  <step id="1-scan">
    Read, don't ask:
    - Is this a WDS repo: `AGENTS.md` naming the WDS agents, `agents/wds/` installed, `projects/`?
    - Which projects exist (`projects/*/design-process/_progress/wds-project-outline.yaml`), and the organization (`shared/<org>/org-profile.md`)?
    - Is there a qualification summary or an open handover to Idun with a project in `## Nästa`?

    No WDS workspace: route to `skills/qualification.md` and stop here.
  </step>

  <step id="2-intake">
    Ask, one at a time, only what is still unknown:

    **Required**
    1. **Client:** the organization's full name, and who commissions the project.
    2. **Project name and slug:** the slug is short, lowercase, with hyphens (`acme-webshop`). It becomes the folder name.
    3. **What is being built:** website, web app, mobile app, e-commerce, a service, or something else.
    4. **Why:** the problem it solves or the goal, in one or two sentences.
    5. **Known constraints:** an existing brand (logo, colours, tone of voice), a platform that is already decided, accessibility or legal requirements.
    6. **Languages:** which languages the product needs.

    **Optional, when relevant**
    - A deadline or a milestone.
    - Reference or competitor sites the client likes.
    - Integrations or technical requirements already known.

    Then confirm:

    ```
    Client:       [organization] (commissioner: [role or name])
    Project:      [name] → projects/[slug]/
    Building:     [type]
    Goal:         [one sentence]
    Constraints:  [list, or "none stated"]
    Languages:    [list]
    Milestone:    [date and what, or —]

    Ready to set this up?
    ```

    If the person corrects anything: adjust and confirm again.
  </step>

  <step id="3-repo-and-code">
    Decide where the project lives and where its code lives. Use the two setups in `repo-structure.md`:

    | Setup | When | The project folder | The code |
    |---|---|---|---|
    | **Shared** | A department or business repo with several projects, where someone else owns the code | `projects/[slug]/` in the business repo | Its own code repo |
    | **Combined** | A team that designs and builds, or a smaller project | `projects/[slug]/` in the same repo | A folder such as `app/` or `src/` |

    - **The repo:** the current WDS repo, unless the person wants a new one. A new repo is created with the GitHub tool, private unless the person says otherwise, and cloned under the dev root the person uses. A new repo also needs the workspace: run `skills/org-onboarding.md` step 3 for it first.
    - **The code:** ask only if it isn't clear. Record it once, in `code:` in the project outline (step 4), so Mimir knows where to build. Not decided yet: write `code: undecided`.
  </step>

  <step id="4-create">
    Show the file tree, then write after a yes. Templates: `references/workspace-templates.md`.

    1. `projects/[slug]/design-process/` with `A-Product-Brief/` … `E-Development/` as the WDS agents expect them.
    2. `projects/[slug]/design-process/_progress/wds-project-outline.yaml`: project, repo, org, scope, created, `output_folder`, `code:`, the phases (qualification and onboarding as they stand, the rest `pending`), governance as it stands in the repo, and the team.
    3. `projects/[slug]/design-process/_progress/00-design-log.md`, first line: `YYYY-MM-DD · idun · Project set up from the intake. Next: /saga.`
    4. A row in the project table in `AGENTS.md`: name, folder, status.
    5. Material the project shares with others (brand, tone, contacts) goes to `shared/<org>/`, not into the project. Point to what is already there.
    6. If `agents/wds/` is missing: install it with the sync tool, after the person's yes ("Installing in a project" in `agents/wds/README.md`).

    Commit: `projects: [slug] set up`, then push.

    **Gate:** `/saga` starts in the repo and finds the project.
  </step>

  <step id="5-handover">
    The product brief is Saga's. Hand over with the intake, so she starts from it and does not ask again.

    Write the handover with wrap (`agents/wds/shared/skills/wrap.md`) to Saga: `sessions/<user>/saga/`, or `sessions/all-users/saga/` if someone else on the team will run her. Put the confirmed intake under `## Gjort` and, under `## Nästa`: "Product brief for [project] in dialog with [commissioner]: goals, audience, scope, tone of voice, competitive context and success criteria, starting from the intake."

    Say:

    > [Project] is set up in `projects/[slug]/`. Next: run `/saga [repo] [timestamp]` and she starts the product brief from the intake.

    End with the resume command from the wrap.
  </step>

</workflow>

---

## Quality rules

- **One project, one folder.** Never two projects in one `design-process/`, never a project outside `projects/` unless `AGENTS.md` says the repo has a single project at its root.
- **The intake is the source of truth** for the product brief's starting point. Saga confirms and deepens it; she does not repeat it.
- **Code location is recorded once.** Mimir reads it from the project outline.
- **WDS needs nothing else.** No installer, no external task system and no backend. Agent Space, if the client uses it, is optional and comes from qualification.
