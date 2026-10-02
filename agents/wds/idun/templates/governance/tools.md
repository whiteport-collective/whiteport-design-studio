# Tools and vendors

Which AI tools {Org} uses, for what, on which data, and what each vendor does with that data.

Status: default (WDS)
Level: default
Tailor in dialog: step 4 (tools and uses), step 11 (vendor due diligence)

Part of the [framework]({org}-framework.md). Keeps principle P4. (NIST AI RMF GOVERN 6.1; ISO/IEC 42001 Annex A.10, third-party and customer relationships.)

## Permitted uses

With an approved tool, on {Org}'s account, within the tool's approved data tier ([data]({org}-data.md#classification)) and through the review gate ([agents]({org}-agents.md#the-review-gate)):

- drafting, editing, translating and summarizing
- research and analysis
- code, tests and documentation
- design, images and media, with disclosure where [transparency]({org}-transparency.md) requires it
- agent work within the agent's authorization profile

## Prohibited uses

- Personal or free accounts for {Org}'s work. They usually lack a data processing agreement and may train on the input.
- Credentials of any kind in a prompt, a chat or a file given to a tool (S2).
- Restricted data in any AI tool, unless the approver has approved that tool and that use, and a DPIA is done where one is required.
- Decisions with legal or similarly significant effects on a person made solely by AI (GDPR Art. 22).
- Any practice prohibited by the AI Act (Art. 5), for example inferring the emotions of people at work or in education, except for medical or safety reasons (Art. 5(1)(f)).
- Content {Org} has no right to use, and content made to deceive.

## Adding a tool

1. The person who wants it fills in a row in both tables below with the status *trial*.
2. On trial, a tool gets public data only.
3. The access owner completes the vendor due diligence. The approver approves or rejects.
4. Approved: the status becomes *approved* with its highest data tier. Rejected: *prohibited*, with the reason.

A new tool triggers a review ([framework]({org}-framework.md#review)).

## Tools in use

| Tool | Vendor | Used for | Type (core / agentic / task-specific) | Highest data tier | Account (org plan) | Owner (role) | Status |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

*Agentic* means the tool takes actions on its own: it writes, sends, deploys or calls other systems. Every agentic tool also has a row in the roster in [agents]({org}-agents.md#roster) and in the integrations table in [access]({org}-access.md#integrations).

## Vendor due diligence

| Vendor | Service | Data location | Trains on our data | Data processing agreement (GDPR Art. 28) | Transfer basis (Chapter V) | Retention | Risk (low / medium / high) | Actions |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

Defaults (recommendations):
- Business or enterprise plans, with training on our data switched off.
- A data processing agreement with every vendor that processes personal data for us (GDPR Art. 28).
- Re-check each vendor quarterly and whenever its terms change.

## Transfers outside the EU/EEA

Any tool or contractor outside the EU/EEA that receives personal data triggers the GDPR Chapter V transfer rules (Arts. 44–49). Record the basis for each one in the table above: an adequacy decision (Art. 45) or appropriate safeguards such as standard contractual clauses (Art. 46).

For US processors, the EU–US Data Privacy Framework covers only certified organizations. The General Court upheld it on 3 September 2025 (T-553/23, Latombe), and an appeal (C-703/25 P) is pending at the Court of Justice, so note a fallback such as SCCs.
