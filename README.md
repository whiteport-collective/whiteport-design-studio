# Whiteport Design Studio (WDS)

**Strategy, projects and alignment — with AI agents that remember, hand over and work in any tool.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

WDS helps a team go from *"we should do something about this"* to a shared, documented understanding of **why**, **for whom** and **what** — before anyone designs a screen or writes a line of code. And when it is time to build, the same agents can do that too.

---

## What WDS is for

Most AI frameworks start with code. WDS starts with the questions that decide whether the code is worth writing:

- **Strategy** — What is the business goal? What does success look like?
- **People** — Who are we building for, and what drives them? (Trigger Mapping)
- **Alignment** — Does everyone — client, team, stakeholders — agree on the same picture?
- **Projects** — Every project keeps its own documented trail, from brief to delivery.

Design and development follow from that foundation. You can stop at a signed-off product brief, go on to UX design, or let the agents build it. **You can also program, if you want to.**

---

## The agents

| Agent | Role | Delivers |
|-------|------|----------|
| **Saga** | Strategic analyst | Product Brief suite, Trigger Map (business goals, personas, driving forces) |
| **Freya** | UX designer | UX scenarios, UX design, specifications |
| **Mimir** | Builder (optional) | Tech audit, PRD, working code |

Start with Saga. She asks one question at a time, reflects before moving on, and writes the documents as you go.

WDS is also a frame for **your own agents**. A project can add a communicator, an SEO specialist or anything else under `agents/<source>/<agent>/` — same structure, same memory, same handovers.

---

## How it works

### The repo is the memory

Nothing lives in a hidden database. Everything an agent knows about the project is a file in the project repo, versioned in git and readable by people:

```
your-project-repo/
├── AGENTS.md                      rules for every agent — the single source
├── agents/
│   ├── wds/                       Saga, Freya, Mimir + shared skills and tools
│   └── <your-source>/<agent>/     your own agents
├── users/<github-username>/       who each person is: role, soul, objectives, achievements
├── sessions/                      handovers — every wrap is one
│   ├── <user>/<agent>/<session-id>-<from>-<summary>.md
│   └── all-users/<agent>/         for whoever runs that agent next
└── projects/<project>/design-process/
    ├── A-Product-Brief/  B-Trigger-Map/  C-UX-Scenarios/  D-Design-System/  E-Development/
    └── _progress/design-log.md    the project's shared timeline
```

### Every session ends with a handover

`/wrap` writes what was done, what is left and what comes next — addressed to the agent that should continue. Usually that is the same agent; sometimes it is the next one in line (Saga hands over to Freya). The session ends with a resume command:

```
/saga visita-kommunikation 2026-09-27_13-22
```

Repo first, then the session's start time. Anyone on the team can paste it — in any tool — and the agent picks up exactly where the last session stopped, or tells you which repo to open if you are in the wrong place.

### One repo, many projects

Each project under `projects/` is a **completely separate WDS structure** with its own design log. Material shared across projects (brand, tone of voice, contacts) goes in `shared/`.

### Agent-neutral

The agents are plain markdown. `AGENTS.md` holds the rules; tool-specific files are thin adapters that point to it:

| Tool | Adapters |
|------|----------|
| Claude Code | `CLAUDE.md` → `AGENTS.md`, `.claude/commands/<agent>.md` |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/prompts/`, `.github/agents/` |
| Codex | reads `AGENTS.md` directly, `.agents/skills/<agent>/SKILL.md` |

A designer in Copilot and a strategist in Claude work in the same repo, with the same agents and the same history.

---

## Get started

1. Copy [`agents/wds/`](agents/wds/) into your project repo.
2. Add an `AGENTS.md` that says who is on the team, where projects live and how sessions start and end. The session start and wrap rules in [agents/wds/shared/](agents/wds/shared/) describe what it needs to cover.
3. Add one adapter per agent for the tools your team uses (see the table above).
4. Open the repo and run `/saga`.

Keep `agents/wds/` untouched in your project and improve it here, upstream — then pull the new version in. Whiteport uses a small sync script that copies `agents/wds/` into every project repo that opts in.

---

## Principles

- **Skill = what, tool = how, instructions = who.** Commands and API calls live in tools, never in workflows.
- **No secrets in files.** Keys live in a password manager (we use Bitwarden) and are fetched at runtime.
- **Lowercase everything.** Folder and file names, always.
- **Ship over perfect.** A signed-off 80% brief beats a perfect one nobody has read.

---

## Status

WDS is being rebuilt as its own framework. Done: the agent-neutral structure in `agents/wds/`, repo-based memory and handovers, timestamp resume. In progress: moving the long step files in `src/workflows/` into agent skills, and removing the old installer (`src/module.yaml`, `tools/cli/`, `*.agent.yaml`).

## Credits

WDS was born as a module for the [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) and is still **inspired by BMad** — thank you to the BMad community. It is now an independent framework, open to connecting with BMad and other agent frameworks as sources under `agents/<source>/`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

---

Built by [Whiteport Collective](https://github.com/whiteport-collective)
