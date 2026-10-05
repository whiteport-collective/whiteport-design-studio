---
name: agent-space-admin
description: Optional. Installs and administers an organization's Agent Space (backend, skill registry, agent, person and tool records, notices). Idun only.
type: http
used_by: [agent-space-install, user-onboarding, librarian]
---

# Tool: agent-space-admin

Admin calls for Agent Space. The everyday call every agent uses (`session-start` for handoff tokens) is in `agents/wds/tools/agent-space.md`. This tool holds what only Idun does.

Agent Space is optional. If `agent_space_url` is missing from `.wds/me.md`, Agent Space is not used: skip every step that needs this tool and say so in one line.

## Configuration

All keys live in Bitwarden. Never in a file, never in `.env`, never in the repo.

From `.wds/me.md` (local, gitignored):

```
agent_space_url: https://<project>.supabase.co
agent_space_bitwarden: <Bitwarden item with the anon key>
agent_space_admin_bitwarden: <Bitwarden item with the service-role key>   # only for admin writes
agent_space_org: <org id>
agent_space_backend: <path to the backend source: migrations and functions>   # only for install
```

Fetch keys at runtime (needs `BW_SESSION`; if the vault is locked, tell the person: 🔑 run `bw unlock`):

```bash
KEY=$(bw get password "<agent_space_bitwarden>")
ADMIN=$(bw get password "<agent_space_admin_bitwarden>")
URL="<agent_space_url>"; ORG="<agent_space_org>"
```

Use the service-role key only for the writes marked **admin** below, and never print it.

---

## Install the backend (CLI)

Run from the backend source (`agent_space_backend`, by default the `design-space` repo's `database/supabase/`). Needs the Supabase CLI and a logged-in account.

```bash
supabase projects create "<org>-agent-space" --org-id <supabase-org> --region eu-north-1 --db-password "$(bw get password "<db-password-item>")"
supabase link --project-ref <project-ref>
supabase db push                                   # apply all migrations in order
supabase functions deploy session-start
supabase functions deploy agent-messages
supabase functions deploy agent-instructions
supabase functions deploy repo-files
supabase secrets set AGENT_SPACE_ORG_ID=<org> GDPR_REGION=EU
supabase secrets set AUTONOMOUS_MESSAGING=false    # AIVSS Moderate/High until sign-off
supabase projects api-keys --project-ref <project-ref>   # read the anon and service-role keys once
```

Save the two keys as Bitwarden items right away (in the vault app, or `bw get template item` → fill name and password → `bw encode` → `bw create item`). Then put the item names, not the keys, in each person's `.wds/me.md`.

---

## Agents

Register an agent (presence and profile):

```bash
curl -s -X POST "$URL/functions/v1/agent-messages" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"action":"register","org_id":"'"$ORG"'","agent_id":"<agent>","pronouns":"<pronouns>","repo":"<repo>",
       "authorization_profile":{"repos":[…],"apis":[…],"network":"none","data_scope":[…],"autonomy_level":"<level>","escalation_triggers":[…]}}'
```

Read it back with `session-start` (shared agent-space tool) and compare the returned profile with the governance document.

---

## People (admin)

PostgREST upserts with the service-role key. Order matters: person, then user, then membership.

```bash
H=(-H "Authorization: Bearer $ADMIN" -H "apikey: $ADMIN" -H "Content-Type: application/json" -H "Prefer: resolution=merge-duplicates")

curl -s -X POST "$URL/rest/v1/people" "${H[@]}" \
  -d '{"id":"<uuid>","display_name":"<name>","legal_name":"<legal>","primary_email":"<email>","pronouns":"<pronouns>","person_type":"human"}'

curl -s -X POST "$URL/rest/v1/users" "${H[@]}" \
  -d '{"id":"<uuid>","org_id":"'"$ORG"'","person_id":"<uuid>","user_type":"human|agent|service","email":"<email>","display_name":"<name>","role":"owner|admin|member|viewer|agent","status":"active"}'

curl -s -X POST "$URL/rest/v1/user_memberships" "${H[@]}" \
  -d '{"user_id":"<uuid>","org_id":"'"$ORG"'","role":"<role>","status":"active"}'
```

Agent users inherit tool access from a human: set `agent_preferences` to `{"tool_delegate":"<human uuid>","pronouns":"…","icon":"…","domain":"wds|business"}` with a `PATCH "$URL/rest/v1/users?id=eq.<uuid>"`.

Verify: `GET "$URL/rest/v1/users?id=eq.<uuid>"` returns `status: active`, and `GET "$URL/rest/v1/user_memberships?user_id=eq.<uuid>"` returns a row.

---

## Per-person tool logins

The person consents themselves. An agent never does it for them.

```bash
# status, then authorize → send auth_url to the person → status again (must be connected: true)
curl -s -X POST "$URL/functions/v1/tool-oauth" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"action":"status|authorize","org_id":"'"$ORG"'","user_id":"<uuid>","service":"google|github|…"}'
```

---

## Skill registry

List registered and pending skills, grouped by agent:

```bash
curl -s -X POST "$URL/functions/v1/agent-instructions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"action":"list-skills","org_id":"'"$ORG"'","statuses":["registered","pending_review"]}'
```

Set a skill's status (`active`, `flagged`, `disabled`; disabled skills are removed locally at the next sync):

```bash
curl -s -X POST "$URL/functions/v1/agent-instructions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"action":"update-skill-status","org_id":"'"$ORG"'","id":"<skill row id>","status":"active|flagged|disabled"}'
```

---

## Notices

Send a notice from Idun (a new person, a new tool, a governance finding):

```bash
curl -s -X POST "$URL/functions/v1/agent-messages" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"action":"send","org_id":"'"$ORG"'","from_agent":"idun","to_agent":"<agent or *>","message_type":"notification","content":"…"}'
```

Handovers between agents go through wrap in the repo, not through this call.

## Not available

- Other backends (local file database, an organization's own SQL server): no tool yet. Write one with the librarian before installing.
- Row-level security policies and memory-scope rules are part of the backend's migrations; this tool applies them, it doesn't define them.
