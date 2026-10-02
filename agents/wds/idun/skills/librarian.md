---
name: librarian
description: Keeps the skill library. Catalogs, audits, creates and registers agents, skills, tools and subagents in their source repos, keeps tools and used_by in step, and syncs the library to every repo that uses it.
agent: idun
version: 2.0
tools: [wds/shared/git, wds/shared/sync, wds/idun/agent-space-admin]
---

# Librarian

Idun owns the agent factory. She creates agents, writes skills and tools, audits what exists, and keeps the library that every agent draws from. She is the reason agents work correctly, and the first to know when they don't.

## The building blocks

| Block | What it is | Lives in |
|---|---|---|
| **Agent** | Who: identity, tone, activation, routing | `agents/<source>/<agent>/instructions.md` |
| **Skill** | What and why: a workflow with purpose and judgment | `agents/<source>/<agent>/skills/` or `agents/<source>/shared/skills/` |
| **Tool** | How: the commands, API calls and scripts | `agents/<source>/<agent>/tools/` or `agents/<source>/shared/tools/` |
| **Subagent** | A focused, stateless specialist an agent delegates to | `agents/<source>/<agent>/subagents/` |
| **Reference** | Method guide or template loaded when a step needs it | `agents/<source>/<agent>/references/` |
| **Adapter** | A thin pointer per AI tool so the agent or skill can be invoked | `.claude/commands/`, `.github/prompts/`, `.github/agents/`, `.agents/skills/` |

The rules are in `agents/wds/README.md` (Skills and tools). The checklists are in `references/quality-criteria.md`.

**Every skill and tool has exactly one source repo.** Local copies (`~/.claude/commands/`, a project's `agents/wds/`) are never edited. Changes are made at the source and synced out.

---

<workflow id="librarian">

  <constraints>
    - Read the actual files. Never catalog or audit from memory.
    - Work in the source repo. If the current repo holds only a copy, find the source (the skills catalog in the private cabinet, `skills.md`, lists every source) and work there.
    - Propose before writing. Show the file tree and a one-line summary per file. Write after a yes.
    - One question per message when creating something.
    - Commands, API calls and script paths go in a tool, never in a skill or instructions file.
    - No MCP servers in sessions. A tool uses HTTP, a CLI or a script in its own folder, in that order.
    - No keys in any file. Name the Bitwarden item, never the value.
    - All folder and file names in lowercase. Paths relative to the repo root.
    - Commit each skill or tool on its own (git tool: `skill(<name>): …` or `tool(<name>): …`).
    - An audit documents. It fixes nothing until the person asks.
  </constraints>

  <step id="0-route">
    | Argument | Mode |
    |---|---|
    | `catalog [agent]`, or none | catalog |
    | `audit [agent \| all]` | audit |
    | `create-skill` | create-skill |
    | `create-agent` | create-agent |
    | `create-tool [name]` | create-tool |
    | `register [path]` | register |
    | `sync` | sync |
  </step>

  <!-- ═══ CATALOG ═══ -->

  <step id="catalog">
    Read the library from the files: every `agents/<source>/` in the source repo, and the skills catalog (`skills.md`) in the private cabinet if there is one, for the other sources on this machine.

    Show tables, scannable, not verbose:

    ```
    ## Agents
    | Agent | Source | Skills | Subagents | Tools | Adapters |

    ## Shared
    | Skill or tool | Type | Used by |

    ## Tools
    | Tool | Type (http/cli/script) | Used by | Bitwarden item |
    ```

    Filtered by agent: list that agent's skills, tools, subagents and references, whether each file exists, and a quick pass/fail on the quality criteria.

    Flag what is off and offer the fix:
    - a skill's `tools:` doesn't match the tools' `used_by:` → "Want me to fix the links?"
    - a referenced file is missing → "Want me to create it?"
    - an agent without adapters → "Want me to add them?"
    - a copy that differs from its source → "Want me to move the change to the source?"

    If everything is clean: "Library is current. [N] agents, [N] skills, [N] tools."
  </step>

  <!-- ═══ AUDIT ═══ -->

  <step id="audit-1-scan">
    For the target agent (or each agent in turn for `all`, finishing one before the next):

    - `instructions.md`: identity, activation (shared activation, resume by timestamp, no required boot call), routing to every skill.
    - Each skill: run the Skill Validator (`subagents/skill-validator.md`). Run the Tool Mapper (`subagents/tool-mapper.md`) on any skill that contains commands, URLs or MCP names.
    - Each tool: frontmatter, `type`, `used_by`, credentials only by Bitwarden item name.
    - Subagents: minimal, stateless, clear input and output.
    - Size: total characters across the agent's files. Flag above 100k (critical instructions get buried).
    - Adapters: present in all four places, pointing at the right file.
  </step>

  <step id="audit-2-score">
    Score the five criteria from `references/quality-criteria.md` as PASS / PARTIAL / FAIL:
    completeness, separation (skill/tool), output coverage, subagent design, drift risk.
  </step>

  <step id="audit-3-report">
    Report in chat:

    ```
    # Skill audit — [Agent]
    [date] · Auditor: Idun

    ## Summary
    [N]/5 PASS — [one-line assessment]

    ## Scores
    | Criterion | Score | Detail |

    ## Findings
    ### [title]
    **Severity:** high / medium / low
    **Where:** [file and line]
    **Fix:** [recommended action]

    ## Recommendations
    [what to fix first]
    ```

    In a project, save it to `{output_folder}/_progress/skill-audit-<agent>.md`. In a source repo, the findings go into the wrap handover.
    For `all`, end with a comparison table: agent, score, highest-severity finding.
    Ask: "Want me to fix any of these now?"
  </step>

  <step id="audit-4-registry" condition="the organization runs Agent Space with registered skills">
    If the governance suite chose managed or strict skill governance, review the registry too, with the agent-space-admin tool: list registered and pending skills, review each, and set its status.

    - `active` — reviewed and fine
    - `flagged` — needs a change; say what
    - `disabled` — must stop now; it is removed locally at the next sync. Use only when it must stop immediately.

    Promotion from a personal to an org-wide skill happens only after review. Report each decision as:

    ```
    Finding:   what is wrong
    Impact:    why it matters
    Action:    status change, promotion or disable
    Follow-up: who needs to respond next
    ```
  </step>

  <!-- ═══ CREATE-SKILL ═══ -->

  <step id="create-skill-1-intent">
    Ask: "What should this skill accomplish, and who uses it?"
    Capture the purpose in one sentence, the owner agent (or `shared`), the source (`wds`, an org, a person) and who triggers it.
    If the person already described it, extract instead of asking.
  </step>

  <step id="create-skill-2-design">
    Ask how it is triggered: a command, a condition the agent detects, a handoff, or plain conversation.

    Draft the workflow. For each step: what the agent does, what it needs, what it produces, what can go wrong, what happens next.
    Present it as a numbered list with its constraints. "Look right?" Wait.
  </step>

  <step id="create-skill-3-tools">
    List the capabilities it needs. For each one, find the existing tool in the catalog. If none exists, run create-tool for it first.
    The skill names tools in `tools:`; it never contains the commands.

    If it produces an artifact, define the format or a template (a reference). If it is purely conversational, say so.
    Would any step load a lot of context, run in parallel, or be reused elsewhere? Then it becomes a subagent.
  </step>

  <step id="create-skill-4-write">
    Show the files, then write:
    - `agents/<source>/<agent>/skills/<name>.md` with frontmatter `name`, `description`, `agent`, `version: 1.0`, `tools:` and a `<workflow>` with `<constraints>` and `<step>` elements.
    - Subagents and references alongside, if any.
    - Add the skill to the agent's `instructions.md` (skills and routing).
    - Add the skill's name to `used_by:` in each tool it uses.
    - If the person invokes it directly: an adapter in each of `.claude/commands/`, `.github/prompts/` and `.agents/skills/` (for WDS, in `agents/wds/shared/adapters/`).

    Run the Skill Validator on the result. Commit the skill on its own. Then sync.
  </step>

  <!-- ═══ CREATE-AGENT ═══ -->

  <step id="create-agent-1-identity">
    Ask: "What agent do you want to create? Tell me about them."
    Capture name (Norse mythology unless the person wants otherwise), pronouns, icon, tone, a one-line purpose. Ask only what is missing.
  </step>

  <step id="create-agent-2-domain">
    Ask: "What does this agent own, and what is explicitly not its job?"
    Capture the source (WDS agents build and analyse; content and communication agents belong to the project or organization, never to `agents/wds/`), the competency and the boundaries.
  </step>

  <step id="create-agent-3-skills">
    Assign existing skills from the catalog, or create new ones (create-skill). Never duplicate a skill another agent owns: share it instead.
    Every agent uses the shared activation, git and wrap.
  </step>

  <step id="create-agent-4-write">
    Show the tree, then write:
    - `agents/<source>/<agent>/instructions.md` in Saga's format: frontmatter, identity, method, skills with triggers and deliverables, activation (resume by `[repo] YYYY-MM-DD_HH-MM [summary]`, then the shared activation steps, then the agent's own status and routing), subagents, references, tools.
    - `skills/`, `subagents/`, `references/`, `tools/` as needed.
    - Adapters in all four places: `.claude/commands/<agent>.md`, `.github/prompts/<agent>.prompt.md`, `.github/agents/<agent>.agent.md`, `.agents/skills/<agent>/SKILL.md` (for WDS, in `agents/wds/shared/adapters/`).
    - The source's README and its sync configuration, so the agent is installed with the others.

    Commit, sync, and start the agent once to prove activation works.
    Report: "[Name] created. [N] files. Start with /[agent]."
  </step>

  <!-- ═══ CREATE-TOOL ═══ -->

  <step id="create-tool-1-discover">
    Read what exists: the catalog, any tool file with a similar name, commands inside skills that already do this (Tool Mapper), and API docs if the person has them.
  </step>

  <step id="create-tool-2-design">
    Settle the design one topic at a time. Propose a default for each and ask:

    - **Type:** HTTP API, CLI, or a script in the tool's own folder. An MCP-only service gets a one-shot call that starts the server for a single call and exits, as a last resort.
    - **Actions:** which are read-only (safe, autonomous), which write (confirm first, preview, or autonomous with a log).
    - **Auth:** which Bitwarden item holds the key. Per-person logins or one shared org account?
    - **Server-side work:** does it need anything built (a webhook, OAuth on a server, a cache)? If yes, write the spec from `references/tool-build-spec.md` and get it approved. No code before the spec is approved.

    If the API's behavior is unclear, note it as an open question. Never invent behavior.
  </step>

  <step id="create-tool-3-write">
    Write `agents/<source>/<agent>/tools/<name>.md`, or `agents/<source>/shared/tools/<name>.md` if several agents use it:
    frontmatter `name`, `description`, `type`, `used_by`; sections for configuration (Bitwarden item, base URL), each action with the exact command or call, and what is not available.
    Add the tool to `tools:` in each skill that uses it. Commit on its own.

    If there is approved server-side work: hand it to Mimir as a build, with the spec as the work order.
  </step>

  <!-- ═══ REGISTER ═══ -->

  <step id="register">
    Bring a stray skill or tool (a file in `~/.claude/commands/`, a project repo, a pasted text) into its source:

    1. **Read it.** If the path doesn't exist, ask for the right one.
    2. **Classify:** agent instructions, skill, tool, subagent or reference. A file that mixes workflow and commands is split into a skill and a tool.
    3. **Owner and source:** which agent, or shared? Which source repo owns it? Ask if unclear.
    4. **Validate** with the Skill Validator. Strip keys and tokens; replace them with the Bitwarden item name.
    5. **Place** it at the right path in the source, fix `tools:` and `used_by:`, add adapters if it is invoked directly. Show the move and confirm.
    6. **Commit and sync.** The stray copy is overwritten by the sync. Never delete files the person didn't ask to delete.
  </step>

  <!-- ═══ SYNC ═══ -->

  <step id="sync">
    Run the sync tool in direct mode. Report:
    - what was pulled and installed, per source
    - repos that were skipped and why
    - **locally edited copies:** offer to move each change to its source, then sync again
    - **collisions:** the same command from two sources; propose which source should own it

    Remind the person that new skills appear in the next session.
  </step>

</workflow>
