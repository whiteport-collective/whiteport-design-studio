---
name: agent-space
source: wds
description: Agent Space (Supabase) for realtime agent presence, messages and handoff tokens. Optional — WDS works without it.
---

# Agent Space

Agent Space is used only for realtime: registering presence and resuming from an 8-character handoff token. Project memory lives in the repo, not here.

## Configuration

Never write the key in a skill or tool file. Resolve it in this order:

1. Environment variable `WDS_AGENT_SPACE_KEY`
2. `agent_space_key:` in `.wds/me.md` (local, gitignored, one per machine)

Base URL: `WDS_AGENT_SPACE_URL`, or `agent_space_url:` in `.wds/me.md`.

If neither is set: Agent Space is not configured. Skip every Agent Space step silently and continue.

## session-start

```bash
curl -s -X POST "$WDS_AGENT_SPACE_URL/functions/v1/session-start" \
  -H "Authorization: Bearer $WDS_AGENT_SPACE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"<agent>","org_id":"<org>","repo":"<current-repo-folder-name>","project":"<current-repo-folder-name>","register":true}'
```

The response contains `messages[]`. To resume a handoff token: find the first message whose `id` starts with the token and read its `## Next` line.
