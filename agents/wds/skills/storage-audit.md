---
name: storage-audit
description: Goes through what is stored about one person, in the repos they work in and in their private cabinet, moves what landed in the wrong cabinet, and checks that every wrap since the last audit follows the standard. Monthly, and always before the person's access to a repo is removed.
used_by: [idun]
version: 1.0
tools: [wds/git]
---

# Storage audit

The work stays with the work, the person stays with the person (principle P2, `governance/wds/principles.md`; the rules are in `governance/wds/data.md`, Shared and private). Things still land in the wrong place: a personal remark in a handover, a client's figure in a private soul file. The audit finds them and cleans up, one person at a time, so that a person who leaves keeps their own story and the organization keeps its work.

**Trigger:** `/idun audit storage [user]`, monthly (the review table in `governance/wds/framework.md`), and before a person's access to a repo is removed.

## 1. Scope

- **The person:** identified per the git tool, or named in the command.
- **The repos:** the repos in the person's skills catalog (`skills.md` in the private cabinet), or the repo the access is being removed from. Read `governance/policies.md` in each: an organization's policy may say more about what may leave its repos.
- **The private cabinet:** where `private:` points. Never read its `private/` subfolder.

## 2. Find

Read, don't guess. For each repo: `users/<user>/`, `sessions/<user>/`, and the design logs. Then the private cabinet: the soul files, `achievements.md`, `log.md` and `sessions/`.

| Found | Where it is | Where it belongs |
|---|---|---|
| The person's own style (tone, pace, format, what annoys them) | the repo's `soul.md` | the private `soul.md` |
| How the team works together, roles, agreements | the private `soul.md` | the repo's `soul.md` |
| How it went for the person, what they felt or learned | a handover or design log in the repo | the personal part of that session's handover |
| Achievements | the repo's `achievements.md` | the private `achievements.md`, at the level of a CV, with a link |
| The organization's figures, client data, strategy, code, decisions, or a copy of a handover | the private cabinet | the repo it came from, or deleted; a copy becomes a link |
| Finances, health, family, relationships | anywhere in a repo | the person's own agent, and an incident (step 4) |

**The wraps follow the standard** (wrap step 2). For every session since the last audit:
- the work part in each repo the session touched, complete enough to continue from alone, with no link to or mention of the personal part
- the personal part in the private cabinet, with the same session id, linking to every work part and copying nothing from them
- the handover statuses: a handover that is `tagen` with no later session, or `öppen` for weeks, is a thread that stopped

A session that is missing a part, or has the wrong content in one, is split or completed the same way as above.

## 3. Propose, then move

Show the findings as one list, grouped by repo and cabinet: what, where it is, where it goes. The person approves, because the private cabinet is theirs and the repo belongs to the organization. On a yes: move, merge into what is there (never just append), and commit each repo and the private cabinet on their own.

Moving something out of a repo does not remove it from the git history. That only matters for personal matters and anything confidential: those are an incident.

## 4. Report

- In the handover: what moved, from where to where, and what the person declined.
- Personal matters or confidential content in a repo's history: an incident in the incident log `governance/policies.md` points to (wrap step 6).
- A pattern (the same kind of thing keeps landing wrong): a proposal to WDS for the skill or template that let it through (wrap step 2, proposals to the WDS method).
