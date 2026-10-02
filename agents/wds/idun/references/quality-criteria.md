# Quality Criteria

What Idun checks when she audits, creates or registers anything in the library. The rules themselves are in `agents/wds/README.md` (Skills and tools); this is the checklist.

---

## The five audit criteria

| # | Criterion | PASS when |
|---|---|---|
| 1 | **Completeness** | Every skill has a workflow with constraints, steps and routing; steps that can fail say what happens then; every skill named in `instructions.md` exists |
| 2 | **Separation** | Skills hold what and why, tools hold how. No commands, API calls or script paths in skills or instructions; no MCP in sessions; no secrets anywhere |
| 3 | **Output coverage** | Every artifact a skill produces has a format or template that shows what great looks like |
| 4 | **Subagent design** | Subagents are minimal and stateless with a clear input and output; steps that load a lot of context or run in parallel are delegated |
| 5 | **Drift risk** | The agent's files are a reasonable size (flag above 100k characters); the method and the critical rules are near the top, not buried |

PARTIAL when most of it holds and the gaps are named. FAIL otherwise.

---

## Agent

- [ ] `instructions.md` with frontmatter: `name`, `version`, `description`, `argument-hint`, `agents:`
- [ ] Clear identity: name, icon, tone, domain, and what is explicitly not its job
- [ ] Method stated as part of the persona, separate from user preferences
- [ ] Activation: resume by `[repo] YYYY-MM-DD_HH-MM [summary]`, then the shared activation steps, then its own status and routing
- [ ] No required boot call. Agent Space only through `agents/wds/shared/tools/agent-space.md`, optional
- [ ] Skills assigned, not duplicated from another agent
- [ ] Ends sessions with the shared wrap
- [ ] Adapters in `.claude/commands/`, `.github/prompts/`, `.github/agents/`, `.agents/skills/`, pointing at `instructions.md`
- [ ] Listed in its source's README and installed by its sync

## Skill

- [ ] Frontmatter: `name`, `description` (one sentence), `agent`, `version`, `tools: [<source>/<tool>, …]`
- [ ] `<workflow>` with `<constraints>` and `<step>` elements
- [ ] Each step: a clear action, its input, its output, what can go wrong, what's next
- [ ] Tools named by capability ("commit and push (git tool)"), never by command
- [ ] Confirmation before writing anything the person hasn't approved
- [ ] Output format or template documented
- [ ] Under 500 lines
- [ ] Adapter per AI tool if the person invokes it directly

## Tool

- [ ] Frontmatter: `name`, `description`, `type: http | cli | script`, `used_by: [<skill>, …]`
- [ ] Every skill in `used_by:` lists the tool in `tools:`, and the other way round
- [ ] Configuration section: where the base URL and the Bitwarden item name come from (`.wds/me.md` or the tool itself)
- [ ] Each action with the exact command or call, and what it returns
- [ ] HTTP first, then CLI, then a script in the tool's own folder. A one-shot MCP call only as a documented last resort
- [ ] No keys, tokens or passwords. The vault-locked case is handled ("run `bw unlock`")
- [ ] Known gaps listed ("not available")
- [ ] Swappable: replacing the implementation changes no skill

## Subagent

- [ ] One job, stated in the first line
- [ ] Input and output contract
- [ ] Stateless: reads what it's given, reports, decides nothing outside its job
- [ ] Never commits unless told to; never repeats a secret

## Everywhere

- [ ] Paths relative to the repo root, folder and file names in lowercase
- [ ] English in `agents/wds/`; client-facing material in the client's language
- [ ] Exactly one source repo; copies are never edited
