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

## Installing in a project

`/sync-skills` copies `agents/wds/` into each project repo that has an `agents/wds/` folder. The project's adapters (`.claude/commands/`, `.github/prompts/`, `.github/agents/`, `.agents/skills/`) point at `agents/wds/<agent>/instructions.md`. Edit here, never in the copy.

## Secrets

No keys in these files. Agent Space is optional — see [shared/tools/agent-space.md](shared/tools/agent-space.md).
