# Module 02: Installation & Setup

## Lesson 4: WDS Initialization

**Install WDS and activate your first agent**

---

## What You'll Do

- Install WDS via a single prompt to Claude
- Understand the folder structure
- Activate an agent and start working

**Time:** 5-10 minutes

---

## Step 1: Install WDS

Open a new Claude session (Claude Code, Claude.ai, or any Claude IDE integration) and type exactly:

```
Install whiteport-design-studio from GitHub for me
```

Claude will:
1. Fetch `install.md` from the WDS GitHub repo
2. Clone WDS to `~/.claude/wds/`
3. Write your config to `~/.claude/wds-config.yaml`
4. Create slash command files in `~/.claude/commands/`

When done you'll see:

```
✓ Whiteport Design Studio installed
  Version: 1.0.0
  Location: ~/.claude/wds/
  Commands: /saga  /freya  /mimir  /sync
```

**✅ Checkpoint:** You see the confirmation above with four commands listed.

---

## Step 2: Understand the Structure

WDS installs to your home directory, not your project:

```
~/.claude/
├── wds/                    ← WDS repo (git clone)
│   ├── src/skills/         ← Agent skill files
│   ├── src/tools/          ← Tool skill files
│   └── install.md          ← Version registry
├── wds-config.yaml         ← Your config (sync source, Agent Space)
└── commands/
    ├── saga.md             ← /saga command
    ├── freya.md            ← /freya command
    ├── mimir.md            ← /mimir command
    └── sync.md             ← /sync command
```

Your **project folder** gets a `_progress/` folder created automatically the first time an agent wraps a session.

**Key insight:** WDS lives in `~/.claude/` — one installation, available in every project.

---

## Step 3: Activate an Agent

WDS has three specialized agents activated by slash commands:

| Agent | Command | Role |
|-------|---------|------|
| **Saga** | `/saga` | Business & Product Analyst — Product Brief, Trigger Map |
| **Freya** | `/freya` | UX Designer — Scenarios, Design Loop |
| **Mimir** | `/mimir` | Builder — Implements from specs |

### Start with Saga

For a new project, open a Claude session in your project folder and run:

```
/saga
```

Saga will scan your project for existing WDS work and guide you to the right starting point.

**✅ Checkpoint:** Saga responds and greets you!

---

## Step 4: Configuration (Optional)

WDS stores settings at `~/.claude/wds-config.yaml`. You can edit this at any time:

```yaml
sync-source: https://github.com/whiteport-collective/whiteport-design-studio
branch: main

agent-space:
  url: https://...
  anon-key: ...
  agents:
    saga: saga
    freya: freya
    mimir: mimir
```

**`sync-source`** — where updates are pulled from. Change if your org forks WDS.

**`agent-space`** — the session handoff backend. Agents use this to pass context between conversations via tokens. See [Module 19](../module-19-agent-coordination/module-19-overview.md) for details.

### Org Install

If your team has a shared WDS configuration, your admin will give you a one-line install command:

```
Install whiteport-design-studio from GitHub, use org config from https://your-org.com/wds-config.yaml
```

This replaces the default config with your org's Agent Space and sync source.

---

## Troubleshooting

**Slash commands not working** — Check `~/.claude/commands/` contains `saga.md`, `freya.md`, `mimir.md`, `sync.md`. If missing, re-run the install prompt.

**Old WDS installation found** — The installer will ask if you want to remove it. Say yes to proceed with the fresh install.

**Agent says "WDS not installed"** — Run `/sync` to trigger a check, or re-run the install prompt.

---

## Congratulations!

You've completed Module 02: Installation & Setup!

**What you accomplished:**
- ✅ GitHub account & repository
- ✅ IDE installed
- ✅ Project cloned
- ✅ WDS installed
- ✅ Agent activated

**You're ready to design with WDS!**

---

## What's Next?

- **[Module 03: Alignment & Signoff](../module-03-alignment-signoff/module-03-overview.md)**
- **Ask Saga:** "What should I do next?"

---

*Part of Module 02: Installation & Setup*
*[← Back to Module Overview](module-02-overview.md)*
