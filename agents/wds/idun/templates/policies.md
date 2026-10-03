# Policies

The policies for this repo, in the order they are read. Agents read this list at every session start and follow the files in this order: the principles every time, the other files when the task touches their area. A lower level may tighten a rule, never loosen it. When two levels say different things, the stricter one wins, unless the difference is recorded with a reason in {Org}'s [framework]({org}/framework.md#differences-from-the-wds-default).

This file is owned by this repo. Idun creates it at setup and updates it when a policy folder is added or removed. The folders it lists are owned by their sources: a folder with a `.source` file is a synced copy and is never edited here.

## 1. WDS default (`wds/`, synced from WDS)

- [Principles](wds/principles.md)
- [Framework](wds/framework.md) · [Tools](wds/tools.md) · [Data](wds/data.md) · [Risk](wds/risk.md) · [Agents](wds/agents.md) · [Access](wds/access.md) · [Incidents](wds/incidents.md) · [Transparency](wds/transparency.md)

## 2. {Org} (`{org}/`, {source: "the source is in this repo" | "synced from {org-source-repo}"})

- [Principles]({org}/principles.md)
- [Framework]({org}/framework.md) · [Tools]({org}/tools.md) · [Data]({org}/data.md) · [Risk]({org}/risk.md) · [Agents]({org}/agents.md) · [Access]({org}/access.md) · [Incidents]({org}/incidents.md) · [Transparency]({org}/transparency.md)

**Incident log:** [{org}/incidents.md]({org}/incidents.md), in the source repo. Wrap step 6 writes incidents there. In a repo with a copy, the incident is written in the source repo, or handed over to its owner.

## 3. Project (`{project}/`, this repo)

No project tightenings yet.

<!--
Template notes (remove when filled):
- Use the organization's own file names when its policy is localized (for example `visita/ramverk.md`, `visita/incidenter.md`), and write this file in the organization's language.
- No organization policy yet: drop section 2. The WDS default then applies alone. `wds/` is a read-only copy, so there is no incident log to write to: wrap step 6 puts findings under `## G&C` in the handover until the organization has its own policy.
- A project tightening is a folder `governance/<project>/` with one file per area it tightens. Each file names the rule it tightens.
-->
