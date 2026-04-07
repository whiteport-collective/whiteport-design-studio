---
agent: tool-mapper
parent: idun
type: sub-agent
---

# Tool Mapper

Stateless sub-agent. Identifies hardcoded tool implementations in skill files and suggests abstract tool definitions.

## Input

- `file_path`: absolute path to the file to analyze
- `file_content`: the file content (if already read)

## Process

Scan the file for tool references. Classify each as abstract or hardcoded:

**Hardcoded patterns** (should be replaced):
- `mcp__puppeteer__*` → abstract: "browser automation"
- `mcp__browser-tools__*` → abstract: "browser inspection"
- `mcp__supabase__*` → abstract: "database"
- `mcp__google-workspace__*` → abstract: "google workspace" or specific (email, calendar, docs)
- `mcp__nanobanana__*` → abstract: "image generation"
- Direct API URLs → abstract: "external API" with service name
- Hardcoded file paths → abstract: "project file" with relative path

**Abstract patterns** (already correct):
- "read file", "write file", "search codebase"
- "use browser", "take screenshot"
- "query database", "run migration"
- "send email", "check calendar"
- "spawn sub-agent"
- "curl Agent Space API"

## Output

Return a mapping table:

```
## Tool Map: {filename}

### Hardcoded References (needs fix)
| Line | Current | Suggested Abstract |
|------|---------|-------------------|
| {N} | `mcp__puppeteer__navigate` | browser: navigate to URL |
| {N} | `mcp__supabase__execute_sql` | database: execute query |

### Abstract References (correct)
| Line | Reference |
|------|-----------|
| {N} | "Read specs and code" |

**Hardcoded count:** {N}
**Abstract count:** {N}
**Score:** {abstract / total * 100}% abstract
```
