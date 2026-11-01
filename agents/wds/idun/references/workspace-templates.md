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
│   ├── _template/                user.md soul.md objectives.md
│   └── <user>/
├── sessions/                     Handovers. Folder = receiving agent.
│   ├── <user>/<agent>/
│   └── all-users/<agent>/
├── governance/
│   ├── policies.md               The policy files in reading order. Owned by this repo.
│   ├── wds/                      The WDS default. Synced, read-only (has .source).
│   ├── <org>/                    The org's policy. Edited only in its source repo; a copy elsewhere (has .source).
│   └── <project>/                Optional tightenings for this repo.
├── org-profile.md                Shared across projects, at the level it serves (see below)
├── brand/                        The brand. Exists once.
│   ├── visual-identity/          Visual direction, mark, moodboard, assets
│   ├── tone-of-voice.md          What we believe, how we sound, the words
│   └── design-system/            Tokens and the components more than one project uses
├── people/<person>/              The people the work involves
├── communication/                Meetings, mail and chats
├── contacts.md
├── timeline.md
├── projects/<project>/           The WDS folders directly in the project, no design-process/ level
│   ├── A-Product-Brief/ … E-Development/
│   └── _progress/
│       ├── wds-project-outline.yaml
│       └── 00-design-log.md
└── .wds/me.md                    Who sits at this machine. Gitignored, one per machine.
```

A single-project repo may keep its `output_folder` at the root instead of under `projects/`, for example `design-process/`. `AGENTS.md` says which. Under `projects/` a project never gets a `design-process/` subfolder.

The shared material (org profile to timeline) lives at the level it serves. Here that is the root, because the repo serves one organization. In an agency repo with several clients it goes in the client's folder (`<client>/brand/` and so on), next to that client's projects. A `shared/` folder is a last resort. See `agents/wds/data/repo-structure.md`.

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
2. Find out who you work with: read `.wds/me.md` (if missing, follow `agents/wds/tools/git.md`), then the soul files in `users/<user>/` and in the private cabinet that `private:` points to, and let them shape the work.
3. Read `governance/policies.md` and follow the policy files in that order: the WDS default, then the organization's, then this repo's (see "Which policy applies" in `agents/wds/data/session.md`).
4. Read the latest handover to you in `sessions/<user>/<agent>/` and open ones in `sessions/all-users/<agent>/`.
5. Work inside one project folder at a time.

The full start is in `agents/wds/data/session.md`.

## During the session

When the person corrects you or states a preference, follow it at once, and write what will last in the file where it belongs (`agents/wds/data/session.md`, During the session).

## At session end

Run wrap: `agents/wds/skills/wrap.md`.

## Agents

| Agent | Source | Role | Command |
|---|---|---|---|
| Idun | wds | Setup, onboarding, governance, skill library | `/idun` |
| Saga | wds | Strategy: product brief, trigger map | `/saga` |
| Freya | wds | UX: scenarios, design, specs | `/freya` |
| Mimir | wds | Build: tech audit, PRD, code | `/mimir` |

## Rules

- One project = one folder under `projects/`, each a separate WDS structure. `output_folder` is `projects/<project>/`, with the WDS folders directly inside it.
- What several projects share lives at the level it serves, here the root: `brand/`, `people/`, `communication/`, `contacts.md`, `timeline.md`, `org-profile.md`. Never copied into projects. A `shared/` folder is a last resort.
- The brand is `brand/visual-identity/`, `brand/tone-of-voice.md` and `brand/design-system/` (tokens and shared components). Each project's `D-Design-System/` holds only the components that project alone uses; when a second project needs one, it moves up to `brand/design-system/`. A token is changed only in `brand/design-system/`.
- Each project's `02-content-language.md` and `03-visual-direction.md` point to `brand/` and add only what is the project's own.
- One folder per source in `agents/`. WDS agents are synced from whiteport-design-studio and never edited here.
- Policy lives in `governance/`, one folder per source: `wds/`, `<org>/` and, optionally, `<project>/`. A folder with a `.source` file is a synced copy and is read-only; edit it in its source repo. `governance/policies.md` lists the files in reading order.
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
- `soul.md` — how we work together in this repo: roles, agreements, conventions with the team and the agents
- `objectives.md` — what the person wants to achieve here

The person's own working style and what they have delivered live in their private cabinet, which travels with them. Nothing here points to it except the `private:` line.

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
# First: how we work together in this repo

Shared file. The agreements for working with First here, with the team and the agents. Follow it.
The person's own style (tone, pace, format) lives in their private soul file. If they conflict, this one wins.

## Agreements

## Corrections

Date, what the agent did wrong in this repo and how it should be.
```

## users/_template/objectives.md

```markdown
# First: goals in this project

Shared file. What the person wants to achieve here. Agents prioritize by it.
```

---

## _progress/wds-project-outline.yaml

```yaml
project: <name>
repo: <folder>
org: <org, or empty>
scope: solo | team | organization
created: YYYY-MM-DD
output_folder: projects/<project>
code: <folder in this repo, such as app/ | another repo | undecided>
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

Created at the first wrap, or in user onboarding when the person names a location. Files: `user.md` (with a Facts section: addresses, companies and their numbers, homes, ways to reach the person), `soul.md`, `identity.md`, `objectives.md`, `heartbeat.md`, `log.md`, `people/` (below), and optionally `skills.md` + `skills.json` (the skills catalog).

**`people/`: the people in the person's life.** So that "Camilla at Some" is enough for any agent to know who she is and what has happened. `people/README.md` is the register, read at every session start: one line per person with the name, what the person calls them, the relationship and a link. `people/<firstname-lastname>.md` holds who they are, where their contact details live (the person's address book, for example Google Contacts; never a copy, so details are kept up to date in one place), the shared history with dates and sources (links to mail, handovers, documents), and what is ongoing. Colleagues, clients, partners, family and friends all belong here, with what the person wants every agent to know. Health, money and the sensitive side of a relationship stay in `private/`. A `private/` subfolder may exist; work agents never read or write it. See `docs/models/soul-files-portable-context.md`.
