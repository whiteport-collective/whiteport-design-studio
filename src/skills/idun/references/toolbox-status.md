---
skill: toolbox-status
agent: idun
---

# Toolbox Status

Living reference of all registered tools, their status, and connected users.
Updated by Idun after each tool-onboarding or user-onboarding run.

Last updated: 2026-04-07

---

## Infrastructure

| Component | Location | Purpose |
|---|---|---|
| Plugin Catalog | `plugin_catalog` table | Tool registry (slug, version, config schema) |
| Org Installations | `org_plugin_installations` table | Per-org activation + app credentials |
| User Vault | `user_vault` table | Per-user credentials (OAuth tokens, API keys) |
| OAuth Connector | `tool-oauth` edge function | Authorization flows for all OAuth tools |
| OAuth State | `oauth_state` table | In-flight auth flow tracking (10-min TTL) |

---

## Registered Tools

### tool_oauth — OAuth Connector
- **Status:** active
- **Version:** 1
- **Category:** tool
- **Endpoint:** `/functions/v1/tool-oauth`
- **Actions:** authorize, callback, status, revoke
- **Supported services:** google
- **Migration:** 018_user_vault_and_oauth.sql
- **Edge function:** `database/supabase/functions/tool-oauth/index.ts`
- **Org:** whiteport (active)

### tool_gmail — Gmail
- **Status:** active
- **Version:** 2
- **Category:** tool
- **Endpoint:** `/functions/v1/tool-gmail`
- **Actions:** list, read, send, search
- **Auth:** OAuth2 via tool_oauth (service: google)
- **Scopes:** `gmail.modify`
- **Migration:** 017_toolbox_gmail.sql + 018 (vault update)
- **Edge function:** `database/supabase/functions/tool-gmail/index.ts`
- **Org:** whiteport (active)
- **Google Cloud project:** whiteport-media
- **OAuth Client ID:** `576173602489-q2f71vtgufs50a5l9p2a7j7pa1qf57lh`
- **Redirect URI:** `https://uztngidbpduyodrabokm.supabase.co/functions/v1/tool-oauth?action=callback`
- **Credentials backup:** Bitwarden — "Google OAuth — Agent Space (whiteport-media)"

---

## Connected Users

### Whiteport Org

| User | ID | Type | Role | Google OAuth | Tools |
|---|---|---|---|---|---|
| Marten | `00000000-...-000001` | human | owner | connected (2026-04-07) | gmail |

### Agent Access

Agents inherit ALL tool access from their human delegate — no per-agent tool lists.
The human's connected services are the ceiling. Skills define domain expertise, not tool permissions.
A human can ask any agent to use any tool by name.

| Agent | Domain | Delegates to | Default skills |
|---|---|---|---|
| saga | wds | Marten | strategy, product brief, trigger mapping |
| freya | wds | Marten | UX design, scenarios, assets |
| mimir | wds | Marten | implementation, build, PRD |
| idun | wds | Marten | agent factory, skills, tool onboarding |
| ivonne | business | Marten | personal ops, finance, scheduling |

---

### tool_calendar — Google Calendar
- **Status:** active
- **Version:** 1
- **Category:** tool
- **Endpoint:** `/functions/v1/tool-calendar`
- **Actions:** list, get, create, update, free-busy
- **Auth:** OAuth2 via tool_oauth (service: google)
- **Scopes:** `calendar`
- **Migration:** 020_toolbox_calendar.sql
- **Edge function:** `database/supabase/functions/tool-calendar/index.ts`
- **Org:** whiteport (active)
- **Note:** Shares same Google OAuth app as tool_gmail. Calendar API must be enabled in Google Cloud Console.

---

## Planned Tools

| Tool | Service | Auth | Scopes | Status |
|---|---|---|---|---|
| tool_fireflies | fireflies.ai | api_key | transcripts | Webhook exists, search tool pending |
| tool_github | github | oauth2 | repos, issues | Planned |

---

## Onboarding Checklist (for new tools)

1. [ ] Define tool (name, service, auth type, scopes, actions)
2. [ ] Write migration (plugin_catalog + org_plugin_installations)
3. [ ] Write edge function (action router + credential flow)
4. [ ] Configure OAuth (if needed) — provider setup + app credentials
5. [ ] Deploy edge function
6. [ ] Verify end-to-end (status → authorize → status → action)
7. [ ] Register in sync manifest
8. [ ] Update this reference
9. [ ] Commit to both repos
10. [ ] Announce to Agent Space
