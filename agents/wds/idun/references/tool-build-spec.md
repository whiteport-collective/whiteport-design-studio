# Tool Build Spec

Template for a tool that needs something built before it can be used: a server-side function, an OAuth flow, a webhook, a cache. Written by the librarian (create-tool) through dialog, approved by the person, then handed to Mimir as the build's work order. No code is written before the spec is approved.

Most tools don't need this. A tool that calls an existing API or CLI with a key from Bitwarden is just a tool file.

## Design rules

- Resolve the auth model before finalizing. Wrong auth means a full rebuild.
- Every write action has an explicit safety rule: confirm, preview, or autonomous with a log.
- Decide the cache now, never "later". Or decide there is none.
- If the API's behavior is unclear, list it as an open question. Never invent behavior.
- Keys and tokens live in Bitwarden or the backend's secret store. The spec names where, never the value.
- The spec lives next to the tool file: `agents/<source>/tools/<tool>-build-spec.md`.

## Template

```markdown
# Tool build spec: <Tool name>

Status: draft | approved
Tool file: agents/<source>/tools/<tool>.md

## Overview
One paragraph: what the tool does, which service, who uses it.

## Actions
| Action | Inputs | Outputs | Safety (safe / confirm / preview / log) |

## Auth
Type (api key, OAuth per person, shared org account, service account).
Where credentials live (Bitwarden item, backend secret store). How tokens are refreshed.
Who consents, and how (a person always consents for themselves).

## Cache
What is cached, key, limit, pruning, search. Or: none, and why.

## Signals
Events that notify an agent or a person, the format, who receives them. Or: none.

## Usage log
What each action logs (counts, sizes, never content), and why. Cost signals for paid APIs.

## Schema
Sketch of any new tables or stored data.

## Build order
1. …

## Open questions
- …

## References
API docs, an existing tool that follows the same pattern.
```

## After approval

1. Update the tool file with the endpoint and its status.
2. Hand the build to Mimir with this spec as the work order (wrap to `sessions/<user>/mimir/`).
3. When Mimir is done: verify each action end to end before the tool is marked active, then add it to the skills that use it.
