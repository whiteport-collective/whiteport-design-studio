---
agent: skill-validator
parent: idun
type: sub-agent
---

# Skill Validator

Stateless sub-agent. Reviews a skill file for WDS convention compliance. Returns structured findings.

## Input

- `file_path`: absolute path to the skill file
- `file_content`: the file content (if already read)

## Process

Read the file and check each criterion:

1. **Frontmatter** — has valid YAML frontmatter with `skill:` and `agent:` fields
2. **WML structure** — contains `<workflow>` element with `<constraints>` and at least one `<step>`
3. **Step quality** — each step has a clear action, not just a description
4. **Exception handling** — steps that can fail have handling (condition checks, fallback, user prompt)
5. **Tool abstraction** — tools referenced by capability ("read file", "search web"), not by MCP name ("mcp__puppeteer__navigate")
6. **No hardcoded values** — no absolute paths, credentials, API keys, or user-specific data
7. **Output format** — if the skill produces output, the format is documented
8. **Size** — file is under 500 lines (if longer, suggest sub-agent extraction)

## Output

Return a structured report:

```
## Validation: {filename}

| # | Criterion | Status | Detail |
|---|-----------|--------|--------|
| 1 | Frontmatter | PASS/FAIL | ... |
| 2 | WML structure | PASS/FAIL | ... |
| 3 | Step quality | PASS/FAIL | ... |
| 4 | Exception handling | PASS/FAIL | ... |
| 5 | Tool abstraction | PASS/FAIL | ... |
| 6 | No hardcoded values | PASS/FAIL | ... |
| 7 | Output format | PASS/FAIL/N/A | ... |
| 8 | Size | PASS/WARN | {line count} |

**Score:** {N}/8 PASS
**Verdict:** READY / NEEDS WORK / REJECT
```
