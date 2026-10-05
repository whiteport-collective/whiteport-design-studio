# agents/wds — Whiteport Design Studio

WDS agents, agent-neutral. Works with Claude, Copilot, Codex and others. All paths are relative to the root of the repo the agents are installed in, so `agents/wds/...` resolves the same in this repo and in a project repo that has a copy.

```
agents/wds/
├── saga/      Strategic analyst — Product Brief, Trigger Map
├── freya/     UX designer — scenarios, UX design, specs
├── mimir/     Implementation — tech audit, PRD, build
├── idun/      Setup and governance — qualification, onboarding, governance suite, skill library
│   └── templates/              governance/: the WDS default policy (framework, principles, tools, data, risk, agents, access, incidents, transparency) · policies.md: the reading list
└── shared/    What no single agent owns
    ├── skills/   wrap, start, handoff, feedback, prd-workflow, design-delivery
    ├── tools/    git, agent-space, memory, sync, wireframe, rendering …
    └── data/     shared activation, agent contracts, glossary, design system, presentations
```

Each agent folder:

| Path | What |
|---|---|
| `instructions.md` | WHO: identity, tone, activation, routing |
| `skills/` | WHAT: workflows (product-brief, trigger-map, ux-design …) |
| `subagents/` | Focused writers and reviewers the agent delegates to |
| `references/` | Method guides loaded when a step needs them |
| `templates/` | Default documents the agent copies into a repo and tailors (Idun: `templates/governance/`, the default policy, and `templates/policies.md`) |
| `tools/` | HOW: commands and API calls only this agent uses (shared ones live in `shared/tools/`) |

**Roles:** Idun installs WDS and gets people started, looks after WDS at each client (structure, sync, governance and compliance, and the conversations about the process) and keeps the WDS method and the skill library. Saga, Freya and Mimir build and analyse. Content and communication agents belong to the project (for example `agents/visita/vinka/`), not to WDS.

## Skills and tools

This principle applies to every skill in every project and initiative, not only WDS.

| | Skill | Tool |
|---|---|---|
| **Holds** | **What and why:** the purpose, the workflow, the judgment, when and for whom | **How:** the commands, API calls and scripts that do the work in practice |
| **Links to** | its tools in the frontmatter: `tools: [<source>/<tool>, …]` | the skills that use it: `used_by: [<skill>, …]` |
| **Changes when** | the strategy or the method changes | the technology changes |

- **One skill can have several tools for the same task.** Posting on a channel can go through an API, a scheduling service or the browser. The skill picks, and the tools do the work.
- **One tool can serve several skills.** It is written once and referenced everywhere.
- **Commands never live in a skill.** An API call, a CLI command or a script path always goes in the tool.
- **No MCP servers in sessions.** A tool uses, in this order: HTTP, a CLI, or a script in the tool's own folder. As a last resort it starts an MCP-only server for a single call and exits.
- **Every skill and tool has exactly one source repo.** Local copies are never edited.
- **Applied as you go.** When a session touches a skill or tool, the agent checks that `tools:` and `used_by:` match and fixes them (wrap step 5).

```markdown
---                                   ---
name: <skill>                         name: <tool>
description: One sentence.            description: One sentence.
tools: [<source>/<tool>]              type: http | cli | script
---                                   used_by: [<skill>, <skill>]
                                      ---
```

## Installing

On a new computer the person says "install whiteport-design-studio from GitHub" in Claude Code. Claude reads [install.md](../../install.md) and becomes Idun, who runs [idun/skills/install-wds.md](idun/skills/install-wds.md): programs, GitHub, a personal repo, the person's repos and the sync.

## Installing in a project

`/sync-skills` ([shared/skills/sync-skills.md](shared/skills/sync-skills.md), script in [shared/tools/sync/](shared/tools/sync/)) reads the person's own catalog, `skills.json` in their private cabinet. It copies `agents/wds/` into every WDS-enabled repo on the machine, so all of them run the latest agents. It also writes the adapters from [shared/adapters/](shared/adapters/) into the repo root: `.claude/commands/`, `.github/prompts/`, `.github/agents/` and `.agents/skills/` for Idun, Saga, Freya, Mimir, wrap, handoff and sync-skills. They only point at `agents/wds/<agent>/instructions.md`, so the same files work in Claude Code, the Claude app on mobile, Copilot and Codex. There are no mobile versions. Edit here, never in the copy.

## Governance policy

A repo where governance is set up has a folder `governance/` at its root, with one folder per source:

| Folder | What | Edited where |
|---|---|---|
| `governance/wds/` | The WDS default, a copy of `idun/templates/governance/` with the same file names | Never. Synced, read-only. |
| `governance/<org>/` | The organization's policy, possibly localized (`governance/visita/ramverk.md`) | Only in the organization's one source repo; its other repos get a copy |
| `governance/<project>/` | Optional tightenings for one repo | Here |
| `governance/policies.md` | The policy files in reading order: wds, then org, then project | Here. Idun creates it at setup. |

A synced folder is a mirror of its source, and its `.source` file (`source: <repo>@<sha>`) shows the version. A folder with `.source` is never edited. Precedence: WDS default < organization < project. A lower level may tighten a rule, never loosen it, and the stricter rule wins. Every agent reads `governance/policies.md` at session start and follows the files in that order ([shared/data/shared-activation.md](shared/data/shared-activation.md), Step: governance). A repo without `governance/` has no governance set up, and agents continue without it. How the copies are made: [shared/tools/sync.md](shared/tools/sync.md). How Idun tailors the policy: [idun/skills/governance-report.md](idun/skills/governance-report.md).

How a WDS repo is laid out, folders with one owner each, is described in [shared/data/repo-structure.md](shared/data/repo-structure.md).

## Secrets

No keys in these files. All keys live in Bitwarden and are fetched at runtime (`bw get password "<item>"`). Agent Space is optional — see [shared/tools/agent-space.md](shared/tools/agent-space.md).
