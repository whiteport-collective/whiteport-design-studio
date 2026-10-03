# agents/wds — Whiteport Design Studio

WDS agents, agent-neutral. Works with Claude, Copilot, Codex and others. All paths are relative to the root of the repo the agents are installed in, so `agents/wds/...` resolves the same in this repo and in a project repo that has a copy.

```
agents/wds/
├── saga/      Strategic analyst — Product Brief, Trigger Map
├── freya/     UX designer — scenarios, UX design, specs
├── mimir/     Implementation — tech audit, PRD, build
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

**Roles:** Saga, Freya and Mimir build and analyse. Content and communication agents belong to the project (for example `agents/visita/vinka/`), not to WDS.

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

## Installing in a project

`/sync-skills` copies `agents/wds/` into every WDS-enabled repo on the machine, so all of them run the latest agents. It also writes the adapters from [shared/adapters/](shared/adapters/) into the repo root: `.claude/commands/`, `.github/prompts/`, `.github/agents/` and `.agents/skills/` for Saga, Freya, Mimir and wrap. They only point at `agents/wds/<agent>/instructions.md`, so the same files work in Claude Code, the Claude app on mobile, Copilot and Codex. There are no mobile versions. Edit here, never in the copy.

How a WDS repo is laid out, folders with one owner each, is described in [shared/data/repo-structure.md](shared/data/repo-structure.md).

## Secrets

No keys in these files. All keys live in Bitwarden and are fetched at runtime (`bw get password "<item>"`). Agent Space is optional — see [shared/tools/agent-space.md](shared/tools/agent-space.md).
