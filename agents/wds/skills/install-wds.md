---
name: install-wds
description: Gets a person from a fresh Claude to working in their WDS repos. Programs, GitHub, a personal repo for their private files, their repos cloned, the skill sync running, and a first task with the right agent.
used_by: [idun]
version: 1.0
tools: [wds/machine, wds/github, wds/git, wds/sync]
---

# Install WDS

Started when someone says "installera WDS" or "install WDS" (see `install.md` at the root of whiteport-design-studio), or with `/idun setup`. The person has Claude and nothing else.

Installing WDS means getting the person into their repos. The agents, the adapters and the policy already live in each WDS repo. What the computer needs is the programs, a login, the person's own repo, and the skill sync that keeps everything in step.

---

<workflow id="install-wds">

  <constraints>
    - One question per message. Plain words. Many people who install WDS have never used a terminal.
    - **Never ask for a password.** Logins happen in the browser. The agent never sees a password, a token or a key.
    - The person consents to everything themselves: installing a program, accepting an invitation, creating a repo. Ask before each.
    - Other repos are asked first (Idun's mandate): a real sync writes in many repos and waits for a yes.
    - Private material never goes into a shared repo.
    - Show progress as a short checklist after each step.
  </constraints>

  <step id="1-account">
    Check that the person works in Claude with their own account. Explain in one line why: everything they do is traced to them, and the organization's policy usually requires it.
    Ask which plan it is. On a personal plan (Pro, Max), ask them to turn off training on their chats in Claude's privacy settings. A Team or Enterprise plan does not train by default.
    Once their organization's repo is cloned (step 7), check the account against its `governance/<org>/` tool policy if there is one.
  </step>

  <step id="2-programs">
    Check git, GitHub CLI and Python with the machine tool. Python runs the skill sync.
    Install what is missing, one at a time, after the person's yes. Offer VS Code if they want to see the files.
    Agree on the dev root (machine tool).
  </step>

  <step id="3-wds">
    Clone whiteport-design-studio into `<dev_root>/whiteport-collective/whiteport-design-studio`. It is public, so no login is needed yet.
    From now on, read Idun and her skills from this clone.
  </step>

  <step id="4-github">
    Does the person have a GitHub account? If not, they create one themselves at github.com, with their work email. Wait.
    Log in with the GitHub tool (browser flow). Check with `gh auth status`.
    Set the git name and email (machine tool). The user id is the GitHub username in lowercase (git tool).
  </step>

  <step id="5-personal-repo">
    Suggest a personal, private repo that the person owns, for everything that is theirs and follows them across projects and computers:

    ```
    <user>-private/
    ├── users/<user>/            the private cabinet
    │   ├── user.md  soul.md  identity.md  objectives.md  heartbeat.md
    │   ├── skills.json          the skill catalog that the sync reads
    │   └── projects/<repo>.md   private notes per repo, and where its sessions are kept
    ├── agents/<user>/           their own agents, skills and tools
    └── sessions/                private sessions, for repos that keep none
    ```

    Explain in two lines: the soul files are how the agents learn to work with them, and own skills and agents live here so that they work in every project. Nothing in it is ever shared with the organization.

    - **Yes:** create it with the GitHub tool (private) and clone it into `<dev_root>/<user>/<user>-private`. Create the folders above with empty files, commit and push.
    - **No:** use a local folder, `~/wds-private/`, with the same structure. Say once that it exists only on this computer and is lost with it.
  </step>

  <step id="6-me">
    Create `~/.wds/me.md`, one per computer, outside every repo:

    ```markdown
    # Who sits at this computer

    user: <user>
    github: <GitHub username>
    name: <Name>
    email: <email>
    private: <path to users/<user>/ in the personal repo, or to ~/wds-private/users/<user>/>
    ```
  </step>

  <step id="7-repos">
    Show pending invitations (GitHub tool). The person accepts the ones they expect.
    List the person's repos and organizations, and mark the WDS repos: those with `agents/wds/` or a design process.
    Clone the WDS repos the person works in, after their yes, into `<dev_root>/<owner>/<repo>`.
    No WDS repo yet: say so. The person may be the first in their organization, and `/idun qualify` sets one up.
  </step>

  <step id="8-catalog">
    Create the skill catalog: copy `agents/wds/tools/sync/catalog-template.json` to `skills.json` in the private cabinet and fill it in:
    - `dev_root` and the paths to the WDS clone and the personal repo
    - `owners`: the person's GitHub username and the organizations they work in
    - the organizations' `governance` entries, if a cloned repo is an organization's policy source
    - no personal repo: remove that source
  </step>

  <step id="9-sync">
    Run the sync as a dry run and show what it would do. After the person's yes, run it for real (`sync-skills`).
    Check that `/idun`, `/saga`, `/freya`, `/mimir`, `/wrap`, `/handoff` and `/sync-skills` exist in `~/.claude/commands/`. They show up in the next session.
    Tell the person when to run `/sync-skills` from now on: after changing a skill, on a new computer, or when an agent says WDS has updates.
  </step>

  <step id="10-person">
    For each WDS repo the person works in, run `user-onboarding.md` from step 2 (role) onward: role, `users/<user>/`, access, and the private cabinet, which already exists.
  </step>

  <step id="11-start">
    Show where things stand in each project: the design log and the person's open tasks in `_progress/plan.md` (the tasks with them as owner), if the project has a plan.
    Agree on a first real task and hand over to the right agent, for example Saga, Freya or the organization's own agent.
    Show how to start next time: open the repo in Claude (or VS Code) and type `/<agent>`.
  </step>

  <step id="12-wrap">
    Wrap the session (`agents/wds/skills/wrap.md`). The handover goes to the agent that takes the first task.
    If anything in the installation was hard or unclear, hand a short note about it to Idun as a method proposal (wrap step 4).
  </step>

</workflow>

---

## Done when

- The person is logged in to GitHub and Claude with their own accounts.
- `~/.wds/me.md` exists, and the private cabinet exists as a repo or a local folder.
- Their WDS repos are cloned, and the sync has run.
- They have started a first task with an agent, in the session or in a handover.
