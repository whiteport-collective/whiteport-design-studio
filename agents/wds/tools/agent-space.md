---
name: agent-space
source: wds
description: Agent Space (Supabase) for realtime agent presence, messages and handoff tokens. Optional — WDS works without it.
---

# Agent Space

Agent Space is used only for realtime: registering presence and resuming from an 8-character handoff token. Project memory lives in the repo, not here.

## Configuration

All keys live in Bitwarden. Never write a key in a file, never read it from `.env`.

1. The base URL and the Bitwarden item name come from `.wds/me.md` (local, gitignored, one per machine):
   ```
   agent_space_url: https://<project>.supabase.co
   agent_space_bitwarden: <name of the Bitwarden item>
   ```
2. Fetch the key at runtime: `bw get password "<agent_space_bitwarden>"` (needs `BW_SESSION`).
   If the vault is locked, tell the user: 🔑 run `bw unlock`. Do not look for the key anywhere else.
3. If `agent_space_url` is missing, Agent Space is not configured. Skip every Agent Space step silently and continue.

## session-start

```bash
KEY=$(bw get password "<agent_space_bitwarden>")
curl -s -X POST "<agent_space_url>/functions/v1/session-start" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"<agent>","org_id":"<org>","repo":"<current-repo-folder-name>","project":"<current-repo-folder-name>","register":true}'
```

The response contains `messages[]`. To resume a handoff token: find the first message whose `id` starts with the token and read its `## Next` line.
