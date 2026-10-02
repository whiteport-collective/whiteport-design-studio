# Incidents

What {Org} does when something goes wrong with AI, including a personal data breach.

Status: default (WDS)
Level: default
Tailor in dialog: step 10

Part of the [framework]({org}-framework.md). Keeps principle Q4. Owner: the incident lead. (NIST AI RMF MANAGE 4.3; ISO/IEC 42001 clause 10.2, nonconformity and corrective action.)

## Roles

| Role | Does |
|---|---|
| **Anyone** | Reports at once to the incident lead. Pulls the kill switch if harm is ongoing. |
| **Incident lead** | Runs the incident: contain, log, coordinate, close. |
| **Privacy contact** | Decides whether personal data is involved and whether the breach must be notified. Keeps the breach log. |
| **Approver** | Decides on notification to the authority and on telling clients and the people affected. |

Contacts: {incident lead, privacy contact, approver: how to reach each}. Supervisory authority: {name, how to notify}.

## First steps, every incident

1. **Stop.** Stop the agent or the flow ([kill switch]({org}-access.md#kill-switch)).
2. **Contain.** Withdraw, correct or block what went out, if you can.
3. **Log.** Open a row in the incident log the same day: what, when found, who knows.
4. **Personal data?** Ask the privacy contact. If yes, the breach clock below has started.
5. **Fix and learn.** Find the cause, fix it, link the principle it touched, and close with an action.

## Procedure per type

| Type | Also do |
|---|---|
| **1. Wrong content sent to a client** | Tell the client, correct it, find why the review gate let it through. |
| **2. Personal data processed without a valid basis** | Stop the processing. Privacy contact assesses whether it is a breach. Add or fix the row in [data]({org}-data.md#records-of-processing). |
| **3. AI output led to wrong advice to a client** | Tell the client what was wrong and what is correct. Check other deliveries built on the same output. |
| **4. Security incident or unauthorized access** (incl. a leaked credential) | Rotate credentials, revoke access, check logs for what was reached. Treat as a breach until shown otherwise. |
| **5. Recording without consent** | Stop and delete the recording or footage unless there is another legal basis. Tell the people recorded. |
| **6. An agent acted outside its authorization** | Tighten its profile. Check what else it did. Review its risk score ([risk]({org}-risk.md#agentic-risk-score)). |

## Personal data breach: the 72-hour clock

GDPR Art. 33 requires notification to the supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware of the breach, unless the breach is unlikely to result in a risk to people's rights and freedoms. Every breach must be documented internally, whether notified or not.

- A notification made later than 72 hours must give the reasons for the delay (Art. 33(1)). If not everything is known, notify in phases (Art. 33(4)).
- A processor that finds a breach tells {Org} without undue delay (Art. 33(2)). Vendor agreements should say so.
- When the breach is likely to result in a high risk to people, they are told too, without undue delay (Art. 34).
- The general Digital Omnibus, COM(2025) 837, proposes 96 hours and notification only of high-risk breaches. It is proposed, not adopted.

For a high-risk AI system under the AI Act, serious incidents have their own reporting duties (Arts. 26(5) and 73). Get legal review.

## Breach log

GDPR Art. 33(5): document every personal data breach, "comprising the facts relating to the personal data breach, its effects and the remedial action taken". Kept by the privacy contact.

| Found (date, time) | What happened | Personal data and people affected (categories, approx. numbers) | Effects | Risk to people (none / risk / high) | Authority notified (when, or why not) | People told (when, or why not) | Remedial action | Closed |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## Incident log

All other incidents and near misses.

| Found | Type | What happened | Principle | Action | Owner (role) | Closed |
|---|---|---|---|---|---|---|
| | | | | | | |
