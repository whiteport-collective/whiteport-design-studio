# agents/wds — Whiteport Design Studio

WDS agents, agent-neutral. Works with Claude, Copilot, Codex and others. All paths are relative to the root of the repo the agents are installed in, so `agents/wds/...` resolves the same in this repo and in a project repo that has a copy.

```
agents/wds/
├── idun/      Setup and governance: qualification, onboarding, governance suite, skill library
├── saga/      Strategic analyst: Product Brief, Trigger Map
├── freya/     UX designer: scenarios, UX design, specs
├── mimir/     Implementation: tech audit, PRD, build
├── skills/    every skill: product-brief, trigger-map, ux-design, build, wrap, handoff, feedback, install-wds …
├── tools/     every tool: git, github, machine, sync, wireframe, rendering …
├── data/      shared activation, glossary, repo structure, design system, presentations
│   └── templates/   governance/: the WDS default policy · policies.md: the reading list
└── adapters/  the command files the sync writes into each repo's root
```

**One folder per agent, everything else side by side.** An agent folder holds only the persona:

| Path | What |
|---|---|
| `instructions.md` | WHO: identity, tone, activation, routing |
| `subagents/` | Focused writers and reviewers the agent delegates to |
| `references/` | Method guides loaded when a step needs them |

Skills, tools and data belong to the source, not to an agent. **Every agent can use every skill.** A skill's `used_by:` says which agents usually run it, so an agent knows its core work and the catalog shows who uses what. It is a description, never a permission. A skill without `used_by:` is for anyone. The same layout applies to every source: a project's own source (`agents/<org>/`) has its agents, `skills/`, `tools/` and `data/` the same way, and all of them are available to every agent in the repo.

**Roles:** Idun installs WDS and gets people started, looks after WDS at each client (structure, sync, governance and compliance, and the conversations about the process) and keeps the WDS method and the skill library. Saga, Freya and Mimir build and analyse. Content and communication agents belong to the project (for example `agents/visita/vinka/`), not to WDS.

## Skills and tools

This principle applies to every skill in every project and initiative, not only WDS.

| | Skill | Tool |
|---|---|---|
| **Holds** | **What and why:** the purpose, the workflow, the judgment, when and for whom | **How:** the commands, API calls and scripts that do the work in practice |
| **Links to** | its tools: `tools: [<source>/<tool>, …]`, and the agents that usually run it: `used_by: [<agent>, …]` | the skills that use it: `used_by: [<skill>, …]` |
| **Changes when** | the strategy or the method changes | the technology changes |

- **One skill can have several tools for the same task.** Posting on a channel can go through an API, a scheduling service or the browser. The skill picks, and the tools do the work.
- **One tool can serve several skills.** It is written once and referenced everywhere.
- **Commands never live in a skill.** An API call, a CLI command or a script path always goes in the tool.
- **No MCP servers in sessions.** A tool uses, in this order: HTTP, a CLI, or a script in the tool's own folder. As a last resort it starts an MCP-only server for a single call and exits.
- **Every skill and tool has exactly one source repo.** Local copies are never edited.
- **Visual quality comes from Taste.** Every agent that renders design or writes frontend code follows [data/taste.md](data/taste.md): the project's own design first, Taste for the rest.
- **External sources go through WDS.** A skill library from outside, like [Taste](../taste/source.md), is copied unchanged into its own folder, `agents/<source>/`, with its license and a `source.md` that names the origin, the commit and how it was reviewed. An update is a reviewed diff, never a direct pull. The sync spreads it to every WDS repo like `agents/wds/`.
- **Applied as you go.** When a session touches a skill or tool, the agent checks that `tools:` and `used_by:` match and fixes them (wrap step 5).

```markdown
---                                   ---
name: <skill>                         name: <tool>
description: One sentence.            description: One sentence.
used_by: [<agent>, <agent>]           type: http | cli | script
tools: [<source>/<tool>]              used_by: [<skill>, <skill>]
---                                   ---
```

## Installing

On a new computer the person says "install whiteport-design-studio from GitHub" in Claude Code. Claude reads [install.md](../../install.md) and becomes Idun, who runs [skills/install-wds.md](skills/install-wds.md): programs, GitHub, a personal repo, the person's repos and the sync.

## Installing in a project

`/sync-skills` ([skills/sync-skills.md](skills/sync-skills.md), script in [tools/sync/](tools/sync/)) reads the person's own catalog, `skills.json` in their private cabinet. It copies `agents/wds/` into every WDS-enabled repo on the machine, so all of them run the latest agents. It also writes the adapters from [adapters/](adapters/) into the repo root: `.claude/commands/`, `.github/prompts/`, `.github/agents/` and `.agents/skills/` for Idun, Saga, Freya, Mimir, wrap, handoff and sync-skills. They only point at `agents/wds/<agent>/instructions.md`, so the same files work in Claude Code, the Claude app on mobile, Copilot and Codex. There are no mobile versions. Edit here, never in the copy.

## Governance policy

A repo where governance is set up has a folder `governance/` at its root, with one folder per source:

| Folder | What | Edited where |
|---|---|---|
| `governance/wds/` | The WDS default, a copy of `data/templates/governance/` with the same file names | Never. Synced, read-only. |
| `governance/<org>/` | The organization's policy, possibly localized (`governance/visita/ramverk.md`) | Only in the organization's one source repo; its other repos get a copy |
| `governance/<project>/` | Optional tightenings for one repo | Here |
| `governance/policies.md` | The policy files in reading order: wds, then org, then project | Here. Idun creates it at setup. |

A synced folder is a mirror of its source, and its `.source` file (`source: <repo>@<sha>`) shows the version. A folder with `.source` is never edited. Precedence: WDS default < organization < project. A lower level may tighten a rule, never loosen it, and the stricter rule wins. Every agent reads `governance/policies.md` at session start and follows the files in that order ([data/shared-activation.md](data/shared-activation.md), Step: governance). A repo without `governance/` has no governance set up, and agents continue without it. How the copies are made: [tools/sync.md](tools/sync.md). How Idun tailors the policy: [skills/governance-report.md](skills/governance-report.md).

How a WDS repo is laid out, folders with one owner each, is described in [data/repo-structure.md](data/repo-structure.md).

## Secrets

No keys in these files. All keys live in Bitwarden and are fetched at runtime (`bw get password "<item>"`). Agent Space is optional — see [tools/agent-space.md](tools/agent-space.md).
