---
name: agent-space-install
description: Optional. Turns an approved AI governance suite into a running Agent Space whose every permission traces back to a signed governance decision.
used_by: [idun]
version: 0.2
tools: [wds/agent-space-admin, wds/git]
---

# Agent Space Install

Governance defines the rules. This skill builds the infrastructure that enforces them.

**Agent Space is optional.** WDS works fully from the repo: memory, handovers and soul files live there. Agent Space adds realtime: presence, messages between agents, handoff tokens, and, when governance asks for it, an audit trail and enforced authorization profiles. Run this skill only when the organization chose Agent Space and its governance suite (`governance-report.md`) is approved.

Nothing is installed that is not in the governance documents. Agent permissions match `12-agent-governance.md` exactly. Tool connections come from the tool inventory in `11-system-integration-governance.md`. Safety settings follow the AIVSS score in `04-ai-risk-assessment.md`. The result is a configuration that is traceable back to approved decisions.

The numbers refer to the full 12-document set. With the merged default policy, read `governance/<org>/agents.md` for 12, `governance/<org>/access.md` for 11 and `governance/<org>/risk.md` for 04 (mapping table in `governance-report.md`, Default policy).

---

<workflow id="agent-space-install">

  <constraints>
    - Governance is the only source of truth. Nothing is installed on Idun's own judgment about what "should" be there. Every setting cites a document and section.
    - If governance is incomplete, stop. Never infer a missing authorization profile. Surface the gap and wait.
    - Permissions are exact, never rounded up. "Read — project repo" means read, not read-write.
    - Keys live in Bitwarden. Never in `.env`, a settings file or the repo. Files name the Bitwarden item only.
    - No MCP servers in sessions. Approved tools become tool files (HTTP, CLI or script).
    - Project memory stays in the repo. Agent Space holds realtime messages, presence and the audit log, not the project's knowledge.
    - One commit per installation step, so the audit trail shows what was installed when.
    - AIVSS High: no live agent actions before the named pre-deployment approver has signed off.
    - Failing smoke tests block completion. Never call an installation done with failing checks.
  </constraints>

  <step id="0-preflight">
    Verify, in the governance suite's location:

    1. All documents exist and none is still marked in progress.
    2. `00-introduction.md` has a named adoption owner and an approval date.
    3. `04-ai-risk-assessment.md` has an AIVSS Factor_Sum and a risk level (Low / Moderate / High).
    4. `12-agent-governance.md` has an authorization profile for every agent in the planned roster.

    Any failure: stop, show the gap, do not proceed.
  </step>

  <step id="1-read-governance">
    Extract exactly what is listed. Do not infer or expand.

    | Document | Extract |
    |---|---|
    | `00-introduction.md` | Org name, adoption level (current and target), approved agent roster, adoption owner |
    | `04-ai-risk-assessment.md` | Factor_Sum, risk level, the safety settings that follow |
    | `12-agent-governance.md` | Per agent: repo access, API access, network, data scope, autonomy level, escalation triggers, memory scope |
    | `10-access-control-groups-policy.md` | Per person: which agents they can direct, what they can approve, whether they can change profiles |
    | `11-system-integration-governance.md` | Tool inventory: name, provider, auth method, data categories, approved for agent use |
    | `05-incident-response-plan.md` | Escalation contacts |

    Hosting follows the adoption level and the organization's standard: local for a single person on one machine, cloud (EU region) for an operational team, the organization's own platform where the governance suite requires on-premises data. The agent-space-admin tool documents the hosted backend; any other backend needs its tool written first (librarian, create-tool).

    Present the plan and wait:

    ```
    ## Agent Space installation plan

    **Org:**            [name]
    **Adoption level:** L[X] → L[Y]
    **Backend:**        [where it runs, region]
    **AIVSS risk:**     [Low / Moderate / High] — Factor_Sum [X.X]

    **Agents to register:**
    - [agent] — [autonomy level] — [scope]

    **People:**         [N] access records
    **Tools:**          [approved tools] · not yet approved: [list]
    **Safety:**         [summary]

    Ready to install? (y)
    ```
  </step>

  <step id="2-backend">
    Install the backend with the agent-space-admin tool: create the project in the chosen region, apply the schema, deploy the functions, store the keys in Bitwarden.
    Write `agent_space_url` and `agent_space_bitwarden` into each person's `.wds/me.md`, never into the repo.
    Commit the configuration record skeleton: `chore: initialize Agent Space — [backend], [region]`.
  </step>

  <step id="3-agents">
    Register each approved agent with its exact authorization profile from `12-agent-governance.md`: repos, APIs, network, data scope, autonomy level, escalation triggers.
    Read each profile back after writing it and compare.
    One commit per agent: `chore: register [agent] — profile from 12-agent-governance`.
  </step>

  <step id="4-scope">
    Configure what each agent may see in Agent Space:

    | Layer | Who reads | Who writes |
    |---|---|---|
    | Org messages and governance notices | All agents | Idun only |
    | Project messages and work orders, one namespace per project | Agents whose profile lists the project | Same |
    | An agent's own handoff tokens and session notices | That agent | That agent |

    Exceptions only as written in `12-agent-governance.md` (for example Idun reading all agents' notices for coordination, or an orchestration chain sharing context within the chain).
    Isolation to enforce: project namespaces, agent session privacy, client data segregation, org-level write restriction.
    AIVSS Moderate or High: log every read and write with agent, time and namespace.
    Verify with a cross-project read by a test agent. It must be denied. Record the result.
    Commit: `chore: configure Agent Space scope — 12-agent-governance`.
  </step>

  <step id="5-people">
    Create one access record per person in `10-access-control-groups-policy.md`: role, agents they can direct, actions they can approve, whether they can change profiles (principal only).
    Commit: `chore: per-person access — 10-access-control-groups-policy`.
  </step>

  <step id="6-tools">
    For each tool approved for agent use in `11-system-integration-governance.md`: make sure a tool file exists (librarian, create-tool) with its Bitwarden item, its data scope matching the inventory, and the agents permitted to use it.
    A tool in the inventory but not approved for agent use is not configured. List it in the plan as "not yet approved".
    Commit: `chore: tool connections — 11-system-integration-governance`.
  </step>

  <step id="7-safety">
    Apply the AIVSS settings:

    | Risk | Autonomous messages | Escalation | Alerting | Logging |
    |---|---|---|---|---|
    | Low (0–4.0) | On | Standard | Recommended | Standard |
    | Moderate (4.1–7.0) | On | Tightened | Required, to the escalation contacts | All agent actions |
    | High (7.1–10) | Off until the approver signs off | At first uncertainty | Required | Tamper-evident audit trail |

    Commit: `chore: AIVSS safety settings — [level], Factor_Sum [X.X]`.
  </step>

  <step id="8-smoke-test">
    Run and report pass or fail for each:

    | Check | Pass when |
    |---|---|
    | Backend reachable | `session-start` answers for a registered agent |
    | Agents registered | Each profile read back matches the governance document |
    | People | Every named person has a record |
    | Tools | Each approved tool authenticates |
    | Escalation | The contacts from `05-incident-response-plan.md` are configured |
    | Safety | Settings match the risk level |
    | AIVSS High | Autonomous messages are off until sign-off |

    Any failure: stop, show it, fix it, run again.
  </step>

  <step id="9-record">
    Write `agent-space-config.md` next to the governance suite: date, installed by Idun, org, adoption level, backend and region, registered agents (autonomy, scope, source section), number of access records, tools (approved for agents, source section), safety settings, smoke test results, and every place where the configuration differs from the governance defaults, with the reason.
    Commit: `docs: agent-space-config.md — installation record`.
  </step>

  <step id="10-handoff">
    Say:

    > Agent Space is installed and running. Every permission matches what was approved in your governance documents, nothing broader, nothing narrower. Agents registered: [list]. Smoke tests passed. The record is in `agent-space-config.md`.

    Next step by situation: a new deployment → `/saga` for the first discovery; agents already live → `/idun governance` for a gap assessment; orchestration → `/mimir`.
  </step>

</workflow>
