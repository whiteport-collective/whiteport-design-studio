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

WDS stores one setting at `~/.claude/wds-config.yaml`:

```yaml
sync-source: https://github.com/whiteport-collective/whiteport-design-studio
branch: main
```

You only need to edit this if your org forks WDS and wants everyone pulling from the fork instead. In that case your admin will give you a one-line install command that sets this automatically:

```
Install whiteport-design-studio from GitHub, use org config from https://your-org.com/wds-config.yaml
```

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
