---
skill: tech-audit
agent: mimir
---

# Tech Audit Workflow

Produces `E-Development/000-tech-audit.md` — a living document describing what is already built. Written once, updated as the project evolves. Every PRD is written on top of it.

---

<workflow id="tech-audit">

  <constraints>
    - Read the codebase structurally — directory trees, key files, package.json, config files. Do not deep-read every source file.
    - Do not make assumptions about what exists. Only document what you can confirm.
    - The audit is descriptive, not prescriptive. No recommendations, no opinions. Just what is there.
    - Flag anything unclear as an open question — do not guess.
  </constraints>

  <step id="1-invoke-auditor">
    Invoke `agents/tech-auditor.md` with the project repo path.

    The auditor does the structural scan and returns structured findings.
    Mimir reviews and confirms before writing the document.
  </step>

  <step id="2-review">
    Present findings to the user in plain language:

    "Here's what I found in the codebase. Let me know if anything looks wrong or missing before I write the audit document."

    Show:
    - Stack summary (framework, language, key dependencies)
    - Architecture (monorepo / single app / backend+frontend split)
    - Key features already built (derived from route/module structure)
    - Data models identified (DB schemas, types, interfaces)
    - Key integrations (APIs, services, third-party)
    - Open questions (anything unclear from structure alone)

    Wait for confirmation or corrections.
  </step>

  <step id="3-write">
    Write `{output_folder}/E-Development/000-tech-audit.md`:

    ```markdown
    # Tech Audit — [Project Name]
    [date] · Living document — update when architecture changes

    ## Stack
    [Framework, language, key libraries, versions]

    ## Architecture
    [How the codebase is structured — monorepo, services, key folders]

    ## Features Built
    | Feature | Location | Notes |
    |---|---|---|
    [Derived from route/module structure]

    ## Data Models
    [Key entities, their fields, relationships — from schema/type files]

    ## Integrations
    [External APIs, services, auth providers, payment, etc.]

    ## Open Questions
    [Anything that needs clarification before writing PRDs]
    ```

    Confirm: "Tech audit written. [N] features documented, [N] open questions flagged."
  </step>

  <step id="4-route">
    After audit is written:
    - If Work Orders exist in E-Development/: go to PRD workflow
    - If no Work Orders: "Tech audit complete. No work orders yet — wake Freya to design and hand off."
  </step>

</workflow>
