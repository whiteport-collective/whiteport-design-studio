---
skill: tool-onboarding
agent: idun
---

# Tool Onboarding Workflow

Registers a new server-side tool in Agent Space. Covers the full lifecycle: plugin catalog entry, edge function deployment, org activation, OAuth setup (if needed), user authorization, and verification.

---

<workflow id="tool-onboarding">

  <constraints>
    - Every tool MUST be registered in `plugin_catalog` before deployment.
    - Tools that access external APIs on behalf of users MUST use `user_vault` for credentials — never env vars per user.
    - OAuth tools MUST use `tool-oauth` as the connector — do not build custom OAuth per tool.
    - Org-level app credentials (client_id, client_secret) go in `org_plugin_installations.config`.
    - Per-user tokens go in `user_vault`.
    - Every tool MUST have a migration file in `design-space/database/supabase/migrations/`.
    - Every tool MUST have an edge function in `design-space/database/supabase/functions/tool-{name}/`.
    - Tool status MUST be verified end-to-end before marking as active.
  </constraints>

  <step id="1-define">
    Define the tool:

    - **Name**: tool slug (e.g., `tool_gmail`, `tool_calendar`)
    - **Category**: `tool` (in plugin_catalog)
    - **Service**: which external service (e.g., `google`, `github`, `slack`)
    - **Auth type**: `oauth2`, `api_key`, or `service_account`
    - **Scopes**: what permissions does this tool need?
    - **Actions**: what operations does the tool expose? (e.g., `list`, `read`, `send`)
    - **Dependencies**: does it depend on another plugin? (e.g., `tool_oauth`)

    Document in a tool brief before writing any code.
  </step>

  <step id="2-migration">
    Create a migration file: `NNN_toolbox_{name}.sql`

    The migration MUST:
    1. Register in `plugin_catalog` with `config_schema` documenting:
       - `org_config`: what org-level settings are needed
       - `user_credentials`: how user tokens are stored
       - `actions`: list of available actions
       - `endpoint`: the edge function URL path
    2. Activate for the target org in `org_plugin_installations`
    3. Use `ON CONFLICT DO UPDATE` for idempotent re-runs

    Pattern (from tool_gmail):
    ```sql
    INSERT INTO plugin_catalog (plugin_slug, display_name, version, category, config_schema)
    VALUES ('tool_{name}', '{Display Name}', '1', 'tool', '{...}'::jsonb)
    ON CONFLICT (plugin_slug) DO UPDATE SET ...;

    INSERT INTO org_plugin_installations (org_id, plugin_slug, status, activated_at)
    VALUES ('{org_id}', 'tool_{name}', 'active', now())
    ON CONFLICT (org_id, plugin_slug) DO UPDATE SET status = 'active';
    ```
  </step>

  <step id="3-edge-function">
    Create the edge function: `database/supabase/functions/tool-{name}/index.ts`

    The function MUST:
    1. Accept `{ action, org_id, user_id, ...params }` as JSON body
    2. Fetch user credentials from `user_vault` via `getAccessToken()` pattern
    3. Auto-refresh expired tokens using org-level app credentials
    4. Cache refreshed tokens back to `user_vault`
    5. Handle CORS headers
    6. Return structured JSON responses
    7. Include clear error messages when credentials are missing

    Reference implementation: `tool-gmail/index.ts`
  </step>

  <step id="4-oauth-setup" condition="auth_type === 'oauth2'">
    Configure OAuth for the service:

    1. **External provider** (e.g., Google Cloud Console):
       - Enable the required API
       - Create/update OAuth consent screen
       - Create OAuth Web Client credentials
       - Set redirect URI: `https://{supabase-url}/functions/v1/tool-oauth?action=callback`
       - Add required scopes

    2. **Store app credentials** in `org_plugin_installations.config`:
       ```sql
       UPDATE org_plugin_installations
       SET config = config || '{"google_client_id": "...", "google_client_secret": "..."}'::jsonb
       WHERE org_id = '{org_id}' AND plugin_slug = 'tool_{name}';
       ```

    3. **Update tool-oauth SERVICES** if adding a new service provider:
       Add entry to `SERVICES` in `tool-oauth/index.ts` with:
       - `auth_url`: provider's authorization endpoint
       - `token_url`: provider's token exchange endpoint
       - `default_scopes`: scopes this tool needs

    4. **Save credentials to Bitwarden** for disaster recovery.
  </step>

  <step id="5-deploy">
    Deploy the edge function:

    ```bash
    cd design-space/database/supabase
    supabase functions deploy tool-{name} --no-verify-jwt
    ```

    Note: `--no-verify-jwt` is required for tools that receive OAuth callbacks.
    Tools that only accept authenticated agent requests can use `verify_jwt: true`.
  </step>

  <step id="6-verify">
    Verify end-to-end:

    1. **Status check** (should return `connected: false` for new users):
       ```bash
       curl -X POST {supabase-url}/functions/v1/tool-oauth \
         -d '{"action":"status","org_id":"{org}","user_id":"{user}","service":"{service}"}'
       ```

    2. **Authorize** (for OAuth tools):
       ```bash
       curl -X POST {supabase-url}/functions/v1/tool-oauth \
         -d '{"action":"authorize","org_id":"{org}","user_id":"{user}","service":"{service}"}'
       ```
       Open returned `auth_url`, complete consent.

    3. **Status check** (should return `connected: true`):
       Same as step 1.

    4. **Tool action** (test the actual tool):
       ```bash
       curl -X POST {supabase-url}/functions/v1/tool-{name} \
         -d '{"action":"{test-action}","org_id":"{org}","user_id":"{user}"}'
       ```

    ALL four checks must pass before marking the tool as active.
  </step>

  <step id="7-register">
    Register in WDS:

    1. Add entry to `src/sync-manifest.json` (type: `reference`, agent: `*`)
    2. Update toolbox status reference (`src/skills/idun/references/toolbox-status.md`)
    3. Commit to design-space repo (migration + edge function)
    4. Commit to whiteport-design-studio repo (manifest + reference)
    5. Sync to Agent Space so agents discover the tool at next boot
  </step>

  <step id="8-announce">
    Broadcast to Agent Space:

    ```json
    {
      "action": "send",
      "from_agent": "idun",
      "to_agent": "*",
      "message_type": "notification",
      "content": "New tool registered: {tool_name}. Actions: {actions}. Agents can use it via POST to /functions/v1/tool-{name}."
    }
    ```
  </step>

</workflow>
