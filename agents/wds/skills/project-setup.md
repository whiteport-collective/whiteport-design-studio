---
name: project-setup
description: Starts a new WDS project. A short project intake, the project folder in the right repo, and where the code lives. Use when work starts on something that has no project yet; the agent that starts the work creates it, not Idun.
used_by: [saga, freya, mimir, viska]
version: 1.0
tools: [wds/git, wds/sync, wds/github]
---

# Project Setup

Takes a new project from "we want to build X" to a project folder the work can start in. **The agent that starts the work creates the project itself** (Mårten, 2026-10-27): Saga for a product brief, Viska for a film, Freya or Mimir when that is where it begins. Idun sets up the repo and installs; she does not create projects.

| Situation | Path |
|---|---|
| No WDS workspace yet | Idun sets up the repo first (`qualification.md`, then `org-onboarding.md`); then this skill |
| A workspace exists, a new project | This skill directly, run by the agent that starts the work |
| The project folder already exists | Show it and its status. Nothing is created. |

The layout follows `agents/wds/data/repo-structure.md`: one project is one folder under `projects/`, a complete WDS structure of its own, and projects never share folders. What several projects share lives at the level it serves: the repo root (`brand/`, `people/`, `communication/`, `contacts.md`, `timeline.md`, `org-profile.md`), or the client's folder in an agency repo. `shared/` is a last resort.

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
    - Which projects exist (`projects/*/_progress/wds-project-outline.yaml`, or `projects/*/design-process/_progress/` in older repos), and the organization (`org-profile.md` at the root or in the client's folder; older repos: `shared/<org>/org-profile.md`)?
    - Is there a qualification summary or an open handover with a project in `## Nästa`?

    No WDS workspace: say in one line that Idun sets up the repo first (`/idun`), and stop here.
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

    - **The repo:** the current WDS repo, unless the person wants a new one. A new repo is created with the GitHub tool, private unless the person says otherwise, and cloned under the dev root the person uses. A new repo also needs the workspace, which Idun sets up (`org-onboarding.md` step 3) before the project is created.
    - **The code:** ask only if it isn't clear. Record it once, in `code:` in the project outline (step 4), so Mimir knows where to build. Not decided yet: write `code: undecided`.
  </step>

  <step id="4-create">
    Show the file tree, then write after a yes. Templates: `../idun/references/workspace-templates.md`.

    1. `projects/[slug]/` with `A-Product-Brief/` … `E-Development/` directly inside it, as the WDS agents expect them. No `design-process/` level in between.
    2. `projects/[slug]/_progress/wds-project-outline.yaml`: project, repo, org, scope, created, `output_folder`, `code:`, the phases (qualification and onboarding as they stand, the rest `pending`), governance as it stands in the repo, and the team.
    3. `projects/[slug]/_progress/00-design-log.md`, first line: `YYYY-MM-DD · <agent> · Project set up from the intake. Next: <the first step>.`
    4. A row in the project table in `AGENTS.md`: name, folder, status.
    5. Material the project shares with others (the brand, people, communication, contacts, timeline) stays at the level it serves, not in the project. Point to what is already there. The project's `D-Design-System/` holds only the components it alone uses; the tokens and shared components are in `brand/design-system/`. `A-Product-Brief/02-content-language.md` points to `brand/tone-of-voice.md` and `03-visual-direction.md` to `brand/visual-identity/`.
    6. If `agents/wds/` is missing: install it with the sync tool, after the person's yes ("Installing in a project" in `agents/wds/README.md`).

    Commit: `projects: [slug] set up`, then push.

    **Gate:** the agents start in the repo and find the project.
  </step>

  <step id="5-start">
    Go straight on with the work the project was created for, starting from the intake, so the person does not answer the same questions again. When that work belongs to another agent (usually the product brief, which is Saga's), hand over with wrap (`agents/wds/skills/wrap.md`) to that agent: the confirmed intake under `## Gjort`, the first step under `## Nästa`, and the resume command at the end.
  </step>

</workflow>

---

## Quality rules

- **One project, one folder.** Never two projects in one project folder, never a `design-process/` subfolder under `projects/<project>/`, never a project outside `projects/` unless `AGENTS.md` says the repo has a single project at its root.
- **The intake is the source of truth** for the product brief's starting point. Saga confirms and deepens it; she does not repeat it.
- **Code location is recorded once.** Mimir reads it from the project outline.
- **WDS needs nothing else.** No installer, no external task system and no backend. Agent Space, if the client uses it, is optional and comes from qualification.
