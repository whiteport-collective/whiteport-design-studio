---
skill: user-onboarding
agent: idun
---

# User Onboarding Workflow

Adds a new user to Agent Space and connects them to the tools they need. Handles identity creation, org membership, OAuth consent flows, and verification.

---

<workflow id="user-onboarding">

  <constraints>
    - Every user MUST exist in `people` table before `users` table.
    - Every user MUST have a `user_memberships` entry for their org.
    - OAuth consent MUST be completed by the actual human — agents cannot consent on behalf of users.
    - User IDs follow the pattern: `00000000-0000-0000-0000-00000000NNNN` for seed users.
    - Agent users (type: `agent`) do NOT need OAuth — they access tools via the human user's credentials or service accounts.
  </constraints>

  <step id="1-collect-identity">
    Gather user information:

    - **Display name**: how they appear in Agent Space
    - **Legal name**: for contracts/compliance
    - **Email**: primary email (used for OAuth and notifications)
    - **Pronouns**: respected in all agent communication
    - **Person type**: `human` or `organization`
    - **Org**: which organization (e.g., `whiteport`)
    - **Role**: `owner`, `admin`, `member`, `viewer`, `agent`
    - **User type**: `human`, `service`, or `agent`
  </step>

  <step id="2-create-identity">
    Create the user via migration or direct SQL:

    ```sql
    -- 1. Person record
    INSERT INTO people (id, display_name, legal_name, primary_email, pronouns, person_type)
    VALUES ('{uuid}', '{name}', '{legal}', '{email}', '{pronouns}', '{type}')
    ON CONFLICT (id) DO UPDATE SET display_name = EXCLUDED.display_name;

    -- 2. User record
    INSERT INTO users (id, org_id, person_id, user_type, email, display_name, role, status)
    VALUES ('{uuid}', '{org}', '{uuid}', '{user_type}', '{email}', '{name}', '{role}', 'active')
    ON CONFLICT (id) DO UPDATE SET role = EXCLUDED.role, status = EXCLUDED.status;

    -- 3. Org membership
    INSERT INTO user_memberships (user_id, org_id, role, status)
    VALUES ('{uuid}', '{org}', '{role}', 'active')
    ON CONFLICT (user_id, org_id) DO UPDATE SET role = EXCLUDED.role;
    ```
  </step>

  <step id="3-connect-tools" condition="user_type === 'human'">
    For each tool the user needs:

    1. **Check tool status**: Is the tool active for this org?
       ```bash
       curl -X POST {url}/functions/v1/tool-oauth \
         -d '{"action":"status","org_id":"{org}","user_id":"{uuid}","service":"{service}"}'
       ```

    2. **Generate authorize URL**:
       ```bash
       curl -X POST {url}/functions/v1/tool-oauth \
         -d '{"action":"authorize","org_id":"{org}","user_id":"{uuid}","service":"{service}"}'
       ```

    3. **User completes consent**: Send them the `auth_url`. They must open it in their browser and consent.

    4. **Verify connection**:
       ```bash
       curl -X POST {url}/functions/v1/tool-oauth \
         -d '{"action":"status","org_id":"{org}","user_id":"{uuid}","service":"{service}"}'
       ```
       Must return `connected: true`.

    Repeat for each service (google, github, slack, etc.).
  </step>

  <step id="4-agent-access" condition="user_type === 'agent'">
    Agents inherit ALL tool access from their human delegate. No per-agent tool lists.

    Set `tool_delegate` to the human whose credentials the agent uses:
    ```sql
    UPDATE users SET agent_preferences = jsonb_build_object(
      'tool_delegate', '{human_user_id}',
      'pronouns', '{pronouns}',
      'icon', '{icon}',
      'domain', '{domain}'  -- 'wds' for product agents, 'business' for ops agents
    ) WHERE id = '{agent_uuid}';
    ```

    Access model:
    - Agent can use any tool the delegate human has connected
    - Skills define domain expertise, not tool permissions
    - A human can ask any agent to use any tool by name (override)
    - The human's connected services are the ceiling
  </step>

  <step id="5-verify">
    Verify the user is fully set up:

    1. **Identity**: `SELECT * FROM users WHERE id = '{uuid}'` — status = 'active'
    2. **Membership**: `SELECT * FROM user_memberships WHERE user_id = '{uuid}'` — exists
    3. **Credentials**: For each required tool, check `user_vault` — status = 'active'
    4. **Tool test**: Make one real API call through each connected tool

    Report: "{name} is set up in {org}. Connected tools: {list}. Ready."
  </step>

  <step id="6-announce">
    Broadcast to Agent Space:

    ```json
    {
      "action": "send",
      "from_agent": "idun",
      "to_agent": "*",
      "message_type": "notification",
      "content": "New user: {name} ({role}) joined {org}. Connected tools: {list}."
    }
    ```
  </step>

</workflow>
