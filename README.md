# Whiteport Design Studio (WDS)

**Strategic design methodology for creating products users love, powered by AI agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
**v1.0.0** — Install by prompt · Slash commands · Agent Space · Org config

---

## Install

Open a Claude session and type:

```
Install whiteport-design-studio from GitHub for me
```

Claude fetches `install.md` from this repo and sets everything up. No terminal. No npm. Done in under a minute.

```
✓ Whiteport Design Studio installed
  Version: 1.0.0
  Location: ~/.claude/wds/
  Commands: /saga  /freya  /mimir  /sync
```

---

## What is WDS?

WDS is a structured design methodology that guides you from product idea to developer-ready specification — using AI agents as collaborators. Each agent owns a phase. They hand off to each other automatically. You stay in the design conversation.

- **Strategic foundation** — Connect every design decision to business goals and user psychology
- **Trigger mapping** — Understand the psychological forces that drive user behavior
- **UX scenarios** — Scenario-first design: understand the journey before drawing anything
- **Design Loop** — Eight-step per-page cycle from spec to implemented and token-extracted
- **Agent coordination** — Agents hand off through `_progress/` files and Agent Space session tokens

---

## Agents

| Agent | Slash command | Role |
|-------|--------------|------|
| **Saga** | `/saga` | Strategic analyst — Product Brief, Trigger Map |
| **Freya** | `/freya` | UX designer — Scenarios, Design Loop, design specs |
| **Mimir** | `/mimir` | Builder — Implements from Freya's specs |

Start with `/saga` on a new project.

---

## Skills and Tools

```
src/
├── skills/
│   ├── saga/           # Strategic analyst
│   ├── freya/          # UX designer
│   ├── mimir/          # Builder
│   └── feedback/       # Feedback collector
└── tools/
    ├── wireframe/       # Layout rules (rendering-agnostic)
    ├── rendering/       # Excalidraw, Pencil, NanoBanana
    ├── sync/            # WDS update tool
    ├── git/             # Git helpers
    ├── persona-page/    # Persona document generator
    ├── prd-writer/      # PRD writer
    ├── prd-workflow/    # PRD workflow
    └── session/         # wrap and start
```

**Skills** are user-triggered agents with an activation loop. **Tools** are utility nodes — no activation loop, called as needed. Both are markdown files; the distinction is organizational.

---

## Design Phases

| Phase | Agent | Output |
|-------|-------|--------|
| 1. Product Brief | Saga | `A-Product-Brief/` |
| 2. Trigger Map | Saga | `B-Trigger-Map/` |
| 3. UX Scenarios | Freya | `C-UX-Scenarios/` |
| 4. UX Design | Freya | `D-UX-Design/` |
| 5. Development | Mimir | — |

---

## Configuration

WDS stores settings in `~/.claude/wds-config.yaml` — outside the git clone, survives updates, user-editable.

```yaml
sync-source: https://github.com/whiteport-collective/whiteport-design-studio
branch: main

agent-space:
  url: https://uztngidbpduyodrabokm.supabase.co
  anon-key: <shared-wds-anon-key>
  agents:
    saga: saga
    freya: freya
    mimir: mimir
```

**Agent Space** is the session handoff system — agents wrap a session, publish a token, and the next agent resumes from exactly where it left off.

---

## Org Install

Distribute WDS across a team with a single command. Host your own `wds-config.yaml` and pass the URL at install time:

```
Install whiteport-design-studio from GitHub, use org config from https://your-org.com/wds-config.yaml
```

Every employee gets your org's Agent Space and sync source automatically. The anon key is read-only — safe to host publicly.

See [docs/getting-started/installation.md](docs/getting-started/installation.md) for the full config schema.

---

## Updates

WDS agents sync automatically on startup. To update manually:

```
/sync
```

---

## Supported Design Tools

| Tool | What it does |
|------|-------------|
| **Excalidraw** | Wireframing |
| **Pencil (Penpot)** | UI design via MCP |
| **NanoBanana** | AI image generation |
| **html.to.design** | HTML prototype → Figma |

---

## Agent Compatibility

WDS skill files are markdown — any capable AI agent can read and follow them. The sync tool uses standard git commands. Session state lives in `_progress/` files that any agent can read and write.

The activation patterns (subagent spawning, Agent Space tokens) are currently optimized for Claude Code. Adapters for other runtimes are possible — the file-based coordination layer works regardless of which agent is running.

---

## Learning Material

Full course in [docs/learn/](docs/learn/):

- **Module 02** — Installation & setup
- **Module 04** — Product Brief
- **Module 06** — Trigger Mapping
- **Module 08** — UX Scenarios
- **Module 19** — Agent coordination and session handoffs

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

---

Built by [Whiteport Collective](https://github.com/whiteport-collective)
