# Installation

WDS installs through Claude. One prompt, and Idun, the WDS setup agent, guides you the rest of the way.

---

## Start

Open **Claude Code**, in the Claude desktop app or in VS Code, and type:

```
Install whiteport-design-studio from GitHub
```

In Swedish: `Installera WDS från whiteport-design-studio på GitHub`.

Claude reads [`install.md`](../../install.md) in the WDS repo, becomes Idun and starts the conversation. The plain Claude chat app cannot install programs or clone repos, so use Claude Code.

---

## What Idun does

Installing WDS means getting you into your repos. The agents, their commands and the policy already live in every WDS repo, so nothing is copied into Claude by hand.

1. **Your Claude account.** Checks that you use your own account and that training on your chats is off.
2. **Programs.** Git, GitHub CLI and Python, and VS Code if you want it. She asks before installing anything.
3. **WDS.** Clones whiteport-design-studio into your dev folder (`C:/dev` or `~/dev`).
4. **GitHub.** You log in in the browser. Idun never asks for a password.
5. **Your personal repo.** A private repo that you own, for your soul files, your skill catalog and your own skills and agents. They follow you across projects and computers. If you prefer, a local folder works too.
6. **Your repos.** Accepts the invitations you expect, finds your WDS repos and clones them.
7. **The skill sync.** Keeps WDS, your personal repo, your project repos and Claude's commands in step. After the first sync, `/idun`, `/saga`, `/freya`, `/mimir`, `/wrap` and `/sync-skills` work everywhere.
8. **A first task.** Shows where your projects stand and hands you over to the right agent.

The full workflow: [agents/wds/idun/skills/install-wds.md](../../agents/wds/idun/skills/install-wds.md).

---

## Keeping WDS updated

Agents check for WDS updates at the start of every session and tell you when there are any. Then run:

```
/sync-skills
```

Run it also after changing a skill and on a new computer. How it works: [agents/wds/shared/tools/sync.md](../../agents/wds/shared/tools/sync.md).

---

## Next Steps

- [Quick Start](quick-start.md) — First 5 minutes with WDS
- [About WDS](about-wds.md) — Understand the method
- [Learn WDS](../learn/00-course-overview.md) — Full course

---

[← Back to Getting Started](getting-started-overview.md)
