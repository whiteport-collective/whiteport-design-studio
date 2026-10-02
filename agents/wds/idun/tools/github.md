---
name: github
description: GitHub CLI for setup work. Login, creating repos, and reading members and collaborators for access maps.
type: cli
used_by: [org-onboarding, user-onboarding]
---

# Tool: github

Uses the GitHub CLI (`gh`). Who the user is and how to commit and push is in `agents/wds/shared/tools/git.md`; this tool covers what setup needs on top of that.

## Login

```bash
gh auth status                     # logged in, and as whom
gh auth login                      # browser flow; walk the person through it
gh auth refresh -s admin:org       # if the organization uses SSO or needs org admin
```

Gate for setup: `gh auth status` shows the right account, and a test push works.

## Create a repo

```bash
gh repo create <owner>/<repo> --private --clone
gh repo view <owner>/<repo> --json url --jq .url
```

Private unless the person says otherwise. If the repo exists, don't create it: clone it, or use the local folder.

## Access maps

Members of an organization and their role:

```bash
gh api orgs/<org>/members --paginate --jq '.[].login'
gh api orgs/<org>/memberships/<login> --jq '{user: .user.login, role: .role, state: .state}'
```

Repos and who has access:

```bash
gh repo list <org> --limit 200 --json name,visibility --jq '.[] | "\(.name) \(.visibility)"'
gh api repos/<org>/<repo>/collaborators --paginate --jq '.[] | "\(.login) \(.role_name)"'
```

Last activity for a person (for access reviews):

```bash
gh api users/<login>/events/public --jq '.[0].created_at'
```

## Add a person to a repo

Only after the person and their role are confirmed:

```bash
gh api -X PUT repos/<owner>/<repo>/collaborators/<login> -f permission=push   # pull | triage | push | maintain | admin
```

## Not available

- Changing organization-level roles or billing. The organization owner does that in GitHub.
