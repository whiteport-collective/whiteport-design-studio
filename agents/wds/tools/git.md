---
name: git
source: wds
description: How agents use git. Identifies the user, shows what changed, commits and pushes.
used_by: [agent-space-install, folder-presentation, handoff, install-wds, librarian, live-meeting, org-onboarding, product-brief, project-setup, recording, storage-audit, trigger-map, user-onboarding, wrap]
---

# Tool: git

Used by skills that need to know who is working, what changed, or that save work.

## Who the user is

The user is identified by their **GitHub username in lowercase**. It is also the folder name in `users/`.

0. **Read `.wds/me.md` at the repo root.** It is gitignored, one per computer, and the `user:` field is the answer.
   - Missing, but `~/.wds/me.md` exists in the home folder: copy it to `.wds/me.md` and check that `.wds/` is in `.gitignore`.
   - Both missing: go on to steps 1 to 3, then create `~/.wds/me.md` and `.wds/me.md` with `github`, `user`, `name`, `email`, `language` (the code the person reads in, see [i18n.yaml](../data/i18n.yaml)) and `private` (the path on this computer to the person's private soul files, or empty).
1. If the GitHub CLI is there:
   ```bash
   gh api user --jq .login
   ```
   Make the answer lowercase. `MartenAngner` becomes `martenangner`.
2. Otherwise:
   ```bash
   git config user.email
   ```
   Match against `email:` in `users/*/user.md`. The folder name is the user.
3. No match: ask for the GitHub username and copy `users/_template/` to `users/<name>/`. Ask the person to check that `git config user.email` is the right address.

## What changed in the session

```bash
git status --short                    # unsaved
git log --oneline --since="8 hours"   # the session's commits
git diff --stat HEAD                  # extent
```

## Save and share

```bash
git add <paths>
git commit -m "<type>: <session-id> — <one line>"
git pull --rebase
git push
```

- `<type>` is for example `wrap`, `brief`, `design` or `fix`.
- A skill or a tool is always committed on its own: `skill(<name>): <what and why>` or `tool(<name>): <what and why>`, with only that file and its scripts.
- Add specific paths, never `git add -A` blindly. Check `git status` first.
- **Expect parallel sessions.** Several agents often work in the same repo at once, especially where there is a `sessions/` folder or an open handover. Check `git reflog -5` and `git log --oneline -5` for fresh commits from another session before committing.
- **Fix forward.** Your own mistake is corrected with a new commit. Never `reset`, `commit --amend`, chains of `revert` or `checkout -- <file>` to undo: another session's commit or unsaved change may land seconds before and be lost. Ask before any command that rewrites history.
- **If `pull --rebase` conflicts:** stop and show the conflict to the user. Never resolve it on your own in someone else's files.
- **If `push` fails:** say so plainly with the error message. Never claim something is pushed without having seen it go through.
- Confirm with the commit hash: `git log --oneline -1`.
- **Before a review:** commit and push before asking another agent (Codex, another session) to review or take over. It reads the repo and cannot see what exists only locally.

## Never

- `git push --force`, `git reset --hard` or rewriting history that is already pushed
- `reset`, `commit --amend` or `checkout -- <file>` in a repo where another session may be running
- Committing secrets such as `.env`, keys or passwords
