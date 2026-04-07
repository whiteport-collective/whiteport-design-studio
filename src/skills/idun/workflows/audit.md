---
skill: audit
agent: idun
---

# Skill Audit Workflow

Reviews an agent's complete skill set against WDS quality criteria. Produces a scored audit report with findings and recommended fixes.

---

<workflow id="audit">

  <constraints>
    - Read the actual files — never audit from memory or assumptions.
    - Score each criterion honestly. A pass is only when the standard is fully met.
    - The audit is diagnostic, not punitive. Findings are opportunities, not failures.
    - Do not fix anything during the audit. Document only.
    - If auditing "all", process one agent at a time. Complete each before starting the next.
  </constraints>

  <step id="1-select-target">
    Determine audit target from the argument:
    - Named agent (e.g., "saga") → audit that agent only
    - "all" → audit every agent in the skill library

    Locate the agent's files:
    - WDS repo: `src/skills/{agent}/SKILL.md`
    - W-A-S repo: `agents/{namespace}/{agent}/` (instructions.md, tools.md, skills.md)
    - Sync manifest: `src/sync-manifest.json`
    - Compiled instructions in Agent Space (via session-start)

    If files are missing, note it as a finding — don't abort.
  </step>

  <step id="2-scan">
    For the target agent, read and evaluate:

    **SKILL.md** (the skill definition):
    - Does every skill have a workflow file that exists?
    - Are triggers documented?
    - Are deliverables clear?

    **Workflow files** (each workflow/*.md):
    - Has `<workflow>` with `<constraints>` and `<step>` elements?
    - Every step that can fail has exception handling?
    - Steps have clear routing (what happens next)?

    **Sub-agents** (agents/*.md):
    - Are they minimal and stateless?
    - Do they have clear input/output contracts?

    **Tools** (tools.md in W-A-S):
    - Are tools referenced by abstract capability or hardcoded to implementation?
    - Does the agent have the right tools for its skills?

    **Compiled size**:
    - Count total characters across all files for this agent
    - Flag if > 100k chars (drift risk — instructions buried deep)

    **Sync status**:
    - Is the agent in sync-manifest.json?
    - Is the compiled instruction in Agent Space current?
  </step>

  <step id="3-score">
    Score against the five quality criteria:

    | # | Criterion | Score | Notes |
    |---|-----------|-------|-------|
    | 1 | **Completeness** — WML with constraints, routing, exception handling | PASS / PARTIAL / FAIL | |
    | 2 | **Tool abstraction** — capability-based, not implementation-hardcoded | PASS / PARTIAL / FAIL | |
    | 3 | **Template coverage** — output types have templates | PASS / PARTIAL / FAIL | |
    | 4 | **Sub-agent design** — minimal, stateless, context-efficient | PASS / PARTIAL / FAIL | |
    | 5 | **Drift risk** — compiled size reasonable, critical instructions not buried | PASS / PARTIAL / FAIL | |

    Overall: count of PASS / PARTIAL / FAIL
  </step>

  <step id="4-report">
    Write the audit report to `_progress/skill-audit-{agent}.md`:

    ```markdown
    # Skill Audit — {Agent Name}
    {date} · Auditor: Idun

    ## Summary
    {Overall score} — {one-line assessment}

    ## Scores
    | Criterion | Score | Detail |
    |-----------|-------|--------|
    [from step 3]

    ## Findings
    ### {Finding title}
    **Severity:** high / medium / low
    **What:** {description}
    **Where:** {file path + line if applicable}
    **Fix:** {recommended action}

    [repeat for each finding]

    ## Recommendations
    [Prioritized list — what to fix first]
    ```

    Present summary to user: "{Agent} scored {X}/5 PASS. {N} findings, {N} high-severity. Full report at _progress/skill-audit-{agent}.md"
  </step>

  <step id="5-next">
    If auditing "all": move to next agent, repeat from step 2.

    When all agents are done, write a summary comparison:
    ```
    | Agent | Score | Highest-severity finding |
    |-------|-------|--------------------------|
    ```

    Ask: "Want me to fix any of these findings now?"
  </step>

</workflow>
