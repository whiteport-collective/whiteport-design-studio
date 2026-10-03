# Access

Who and what has access to {Org}'s systems, how credentials are kept, what the AI connects to, and how to stop an agent fast.

Status: default (WDS)
Level: default
Tailor in dialog: step 9 (accounts, integrations, kill switch), step 14 (access review cadence)

Part of the [framework](framework.md). Keeps principles S1, S2 and S3. Owner: the access owner.

## Accounts

- Everyone has their own account in every system they work in (S1). No shared logins, no working on someone else's account.
- Every agent acts under an identity that traces to a person: the account of the person who runs it, or its own service account with a named owner.
- Multi-factor authentication on every account that supports it (recommendation).
- Leaving {Org} or changing role: access is removed or changed the same working day (recommendation).
- Access is requested from the access owner, who records it below. The repo names who has access, never the password.

## Least privilege

People and agents get what the task needs, no more (S3). Agents start read-only. Write access is granted per system, for a named purpose, and with an end date where the system allows it (recommendation).

| Group | Members (roles) | Systems | Access |
|---|---|---|---|
| | | | read / write / admin |

Keep a people access map (person, role, what they can access) and a repo access map (repo, who has access) where the organization keeps its shared material, and update them at each access review.

## Credentials

- All passwords, keys and tokens live in {Org}'s password manager: {password manager}. Agents fetch them at runtime.
- A repo, a skill or a tool names the item in the password manager, never the value (S2).
- Secret scanning is switched on for every repo where the platform supports it (recommendation).
- A credential that has been exposed is rotated at once and handled as an incident ([incidents](incidents.md)).

## Integrations

Every system an AI tool or agent reads from or writes to.

| System | What the AI reads | What the AI writes | Authenticated by | Owner (role) | Crosses {Org}'s boundary | How to cut it off |
|---|---|---|---|---|---|---|
| | | | | | | |

Cascade rules (recommendations):
- More than three systems depend on one AI output: add a circuit breaker that stops the chain on an error.
- An AI output would create a financial record: a person approves before the record is created.
- Data crosses {Org}'s boundary: check its integrity at the boundary.
- Outbound data from agents is limited to what the integration needs. Agents do not send Confidential or Restricted data to a system that is not approved for it.

## Kill switch

Anyone who sees an agent cause harm may stop it. The agent owner restarts it after the cause is understood. (NIST AI RMF MANAGE 2.4.)

To stop an agent:
1. Stop its running sessions and scheduled jobs.
2. Revoke or disable its tokens and integration access (table above, last column).
3. Tell the agent owner and the incident lead, and log it ([incidents](incidents.md)).

Test the kill switch before an agent with a Moderate or High risk score goes live, and then quarterly (recommendation).

## Access review

Quarterly, and at every role change or departure (recommendation). The access owner checks every account, group, token and integration against this file, removes what is not needed, and records the deviations in [principles](principles.md#deviations-now).
