---
name: sync-skills
source: wds
description: Syncs skills, agents and policy between the WDS repo, the person's private repo, the project repos and the computer's .claude folder. Run after a change to a skill, after changing computers and when something is missing.
used_by: [idun, saga, freya, mimir]
tools: [wds/sync]
---

# Sync skills: the same version everywhere

Every skill has exactly one source repo. The sync makes sure every place that uses it has the latest version:

| From | To | What |
|---|---|---|
| The WDS repo | every WDS repo on the computer | `agents/wds/`, the adapters (`.claude/commands/`, `.github/`, `.agents/skills/`) and `governance/wds/` where governance is set up |
| an organization's source repo | the organization's other repos | `governance/<org>/` |
| The WDS repo and the person's private repo | the computer's `~/.claude/commands/` | pointers to the agents and the skills, so that `/saga`, `/idun` and the person's own commands work in every repo |

Which sources apply to the person is in the person's catalog, `skills.json` in the private cabinet. Idun creates it during installation.

**Usage:** `/sync-skills`, `/sync-skills dry-run` (show only) or `/sync-skills no-pull` (skip git pull).

## 1. Ask first

A real sync writes into repos other than the one the session works in. So run it only when the person has said yes, or after a dry run the person has seen. Unknown flags never start a sync.

## 2. Run

Run the sync as described in the [sync tool](../tools/sync.md).

## 3. Receipt

Summarize briefly:
- the number of skills per source
- the repos that were updated, and the repos that were skipped, with the reason
- **locally edited** commands: they were edited directly in `~/.claude/commands/` and saved aside. Offer to move the change to the source repo.
- **clashes:** the same command from several sources. Suggest which source should own it.
- governance: what was mirrored, and whether a conflict check is needed

Remind the person that new commands show up in the next session.
