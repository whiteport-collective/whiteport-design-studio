---
name: git
version: "1.0.0"
description: Whiteport git standard — conventional commits, branch naming, AI attribution, frequency rules. Use when committing, branching, or handing off code.
agents: [saga, freya, mimir]
---

# Git — Whiteport Standard

All agents follow this when committing, branching, and handing off.

---

## Commits

**Format:** Conventional Commits

```
<type>(<scope>): <short description>

[body — optional]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

| Type | When |
|------|------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `bump` | Version number update |
| `docs` | Documentation only |
| `chore` | Maintenance, config, tooling |
| `refactor` | Restructure, no behavior change |

- One logical change per commit
- Imperative mood: "add webhook handler" not "added"
- Always `Co-Authored-By` when Claude wrote or co-wrote — use actual model name

---

## Branches

`<agent>/<short-description>` — e.g. `codex/refactor-storefront`, `idun/sysadmin-skill`

- Lowercase, hyphens only
- Short-lived — merge or delete after work is done
- Never commit directly to `main` for anything non-trivial

---

## Never

- `--no-verify` — fix the hook instead
- `--force` push to `main`
- `git add .` or `git add -A` — stage specific files
- Amend published commits

---

## Frequency

Commit after each discrete, complete change — not batched at session end.
