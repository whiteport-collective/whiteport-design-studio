# Installation

WDS installs via Claude. One prompt, no manual steps.

---

## Personal Install

Open a Claude session and type:

```
Install whiteport-design-studio from GitHub for me
```

Claude fetches `install.md` from the WDS GitHub repo and follows the steps automatically. When done you'll see:

```
✓ Whiteport Design Studio installed
  Version: 1.0.0
  Location: ~/.claude/wds/
  Commands: /saga  /freya  /mimir  /sync
```

---

## What the Installer Does

1. Detects your home directory
2. Checks for an existing WDS installation (offers upgrade or clean install)
3. Clones the WDS repo to `~/.claude/wds/`
4. Writes `~/.claude/wds-config.yaml` with default settings
5. Creates slash command files in `~/.claude/commands/`

---

## Configuration — `wds-config.yaml`

WDS stores its configuration at `~/.claude/wds-config.yaml`. You can edit this file at any time — it survives updates because it lives outside the git clone.

**Default config:**

```yaml
sync-source: https://github.com/whiteport-collective/whiteport-design-studio
branch: main
```

**`sync-source`** — where WDS updates are pulled from. Change this if your org forks WDS.

---

## Org Install

If you're distributing WDS across a team with a custom fork, host your own `wds-config.yaml` and pass the URL during install:

```
Install whiteport-design-studio from GitHub, use org config from https://your-org.com/wds-config.yaml
```

Claude fetches your config file and writes it as `~/.claude/wds-config.yaml` instead of the defaults. Every employee points to your fork automatically.

**Example org config:**

```yaml
sync-source: https://github.com/your-org/wds-fork
branch: main
```

---

## Keeping WDS Updated

WDS agents sync automatically on startup. You can also sync manually at any time:

```
/sync
```

Or ask directly: `sync WDS` / `update WDS` / `check for updates`.

---

## Troubleshooting

**"WDS not installed"** — The sync tool can't find `~/.claude/wds/`. Run the install prompt above.

**Old installation found** — If you had a pre-1.0 WDS install, the installer will ask if you want to remove it before proceeding. Say yes.

**Token not resolving on resume** — If `/saga [token]` reports no match, the handoff message may have been sent before the Agent Space routing fix. Start a fresh session with `/saga` and pick up from `progress/saga.md` in your project folder.

---

## Next Steps

- [Quick Start](quick-start.md) — First 5 minutes with WDS
- [About WDS](about-wds.md) — Understand the method
- [Learn WDS](../learn/00-course-overview.md) — Full course

---

[← Back to Getting Started](getting-started-overview.md)
