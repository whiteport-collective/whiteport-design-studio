# Workspace Templates

What a WDS workspace contains and the starting content of each file. Used by org onboarding (step 3) and user onboarding (step 4). Write client-facing files in the organization's language; the structure stays the same. All folder and file names in lowercase.

---

## Tree

```
<repo>/
├── AGENTS.md                     All rules. Agent-neutral.
├── CLAUDE.md                     Adapter → AGENTS.md
├── .github/copilot-instructions.md   Adapter → AGENTS.md (if the team uses Copilot)
├── .gitignore                    includes .wds/
├── agents/
│   ├── wds/                      Installed by the sync. Never edited here.
│   └── <org>/                    The organization's own agents, skills and tools (if any)
├── users/
│   ├── README.md
│   ├── _template/                user.md soul.md objectives.md achievements.md
│   └── <user>/
├── sessions/                     Handovers. Folder = receiving agent.
│   ├── <user>/<agent>/
│   └── all-users/<agent>/
├── shared/<org>/                 Shared across projects: org profile, brand, contacts, governance
├── projects/<project>/design-process/
│   ├── A-Product-Brief/ … E-Development/
│   └── _progress/
│       ├── wds-project-outline.yaml
│       └── 00-design-log.md
└── .wds/me.md                    Who sits at this machine. Gitignored, one per machine.
```

A single-project repo may keep its `output_folder` at the root instead of under `projects/`. `AGENTS.md` says which.

---

## AGENTS.md

```markdown
# <Repo name> — instructions for all AI agents

Applies to every agent in this repo: Claude, Copilot, Codex and others.
Agent-specific files (`CLAUDE.md`, `.github/copilot-instructions.md`, `.claude/`, `.github/prompts/`) are thin adapters that point here. Never put content in them.

<One paragraph: what this repo is, for whom.>
Team: **<Name>** (<role>), **<Name>** (<role>).
Language: <language for client-facing material>. All folder and file names in lowercase.

---

## At session start

1. Note the start time (`YYYY-MM-DD_HH-MM`, local time). The session id is `YYYY-MM-DD_HH-MM-<user>`.
2. Find out who you work with: read `.wds/me.md`. If missing, follow `agents/wds/shared/tools/git.md`.
3. Read the latest handover to you in `sessions/<user>/<agent>/` and open ones in `sessions/all-users/<agent>/`.
4. Work inside one project folder at a time.

## At session end

Run wrap: `agents/wds/shared/skills/wrap.md`.

## Agents

| Agent | Source | Role | Command |
|---|---|---|---|
| Idun | wds | Setup, onboarding, governance, skill library | `/idun` |
| Saga | wds | Strategy: product brief, trigger map | `/saga` |
| Freya | wds | UX: scenarios, design, specs | `/freya` |
| Mimir | wds | Build: tech audit, PRD, code | `/mimir` |

## Rules

- One project = one folder under `projects/`, each a separate WDS structure. `output_folder` is `projects/<project>/design-process/`.
- What several projects share lives in `shared/<org>/`, never copied into projects.
- One folder per source in `agents/`. WDS agents are synced from whiteport-design-studio and never edited here.
- Everything in the repo is shared and professional. Private matters go in each person's private cabinet.
- No credentials in the repo. Name who has access and the Bitwarden item, never the value.
- Commit and push after each finished step.

## Projects

| Project | Folder | Status |
|---|---|---|
| <name> | `projects/<project>/` | <status> |
```

## CLAUDE.md

```markdown
@AGENTS.md
```

## .gitignore

```
# Local identity per machine — never synced
.wds/
```

To opt the repo in to `/sync-skills` before it has any other WDS marker, create an empty `agents/wds/.wds-sync`.

---

## .wds/me.md (per machine, gitignored)

```markdown
github: <GitHubUsername>
user: <githubusername in lowercase>
name: <Full Name>
email: <email>
private: <path on this machine to the private cabinet, or empty>
agent_space_url:        # optional, only if the workspace uses Agent Space
agent_space_bitwarden:  # optional, the Bitwarden item that holds the key
```

---

## users/README.md

```markdown
# users

One folder per person, named after the GitHub username in lowercase. Shared and professional: the team, partners and the client may read it.

- `user.md` — role in this project, and `private:` (where the person's private cabinet is)
- `soul.md` — how agents work with the person in this repo, built from their corrections
- `objectives.md` — what the person wants to achieve here
- `achievements.md` — what has been delivered, newest first

New person: the agent creates the folder from `_template/` on the first session. Wrap fills it in.
Never write in someone else's folder.
```

## users/_template/user.md

```markdown
---
github: GitHubUsername
name: First Last
email: name@example.com
private:
---

# First Last: who in this project

Shared file. Describes only the role in this repo.

## Role

## Collaboration
```

## users/_template/soul.md

```markdown
# First: how agents work with them in this repo

Shared file. The behavioral contract, built from the person's own corrections. Follow it.
Complements the person's private soul file. If they conflict, this one wins.

## How they want agents to work

## Corrections

Date, what the agent did wrong and how it should be.

## Appreciated / rejected
```

## users/_template/objectives.md

```markdown
# First: goals in this project

Shared file. What the person wants to achieve here. Agents prioritize by it.
```

## users/_template/achievements.md

```markdown
# First: delivered in this project

Shared file. What actually got done, with date and link. Wrap adds rows, newest first.
```

---

## _progress/wds-project-outline.yaml

```yaml
project: <name>
repo: <folder>
org: <org, or empty>
scope: solo | team | organization
created: YYYY-MM-DD
output_folder: projects/<project>/design-process
agents: [idun, saga, freya, mimir]
agent_space: none | <where it runs>
phases:
  qualification: done
  org_onboarding: done
  user_onboarding: done | pending | not_needed
  product_brief: pending
  trigger_map: pending
  ux_scenarios: pending
  ux_design: pending
  development: pending
governance: none | lean | standard | full | in_progress | approved
team: [<user>, …]
```

## _progress/00-design-log.md

```markdown
# Design log — <project>

The team's shared timeline. Newest first. One line per event: date, who, what.

- YYYY-MM-DD · idun · Workspace set up from the confirmed qualification. Next: /saga.
```

---

## Private cabinet (the person's own, never the project repo)

Created at the first wrap, or in user onboarding when the person names a location. Files: `user.md`, `soul.md`, `identity.md`, `objectives.md`, `heartbeat.md`, `log.md`, and optionally `skills.md` + `skills.json` (the skills catalog). A `private/` subfolder may exist; work agents never read or write it. See `docs/models/soul-files-portable-context.md`.
