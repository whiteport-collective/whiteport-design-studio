# Whiteport Design Studio — instructions for all AI agents

Applies to every agent working in this repo: Claude, Copilot, Codex and others. Tool-specific files (`CLAUDE.md`, `.github/copilot-instructions.md`) are thin adapters that point here.

## What this repo is

The source of the WDS agents: **Saga** (strategy), **Freya** (UX design) and **Mimir** (build). They live in [agents/wds/](agents/wds/README.md). Project repos get a copy through `/sync-skills`; changes are made here, never in a copy.

WDS is its own framework, inspired by BMad. It is open to other frameworks: another source is simply another folder under `agents/<source>/`.

## Rules

- **All folder and file names in lowercase.**
- **Skill = what, tool = how, instructions = who.** Commands and API calls belong in a tool, never in a skill or instructions file.
- **No secrets in any file.** All keys live in Bitwarden and are fetched at runtime with `bw get password "<item>"`. Files may name the Bitwarden item, never the value.
- **Paths are relative to the repo root** (`agents/wds/shared/...`), so they work unchanged in project repos.
- **Memory lives in the project repo** (`sessions/<user>/<agent>/`, `users/<user>/`, `design-process/_progress/`). Every wrap is a handover — to the same agent or another one. Agent Space is only for realtime and is optional.

## Proposed: projects/ instead of docs/

Tested in visita-kommunikation (2026-09-27): every project lives in `projects/<project>/design-process/` as a **completely separate WDS folder structure** (A-Product-Brief … E-Development, `_progress/`). One repo can then hold several WDS projects, and each one keeps its own design log. Shared material (brand, tone, contacts) goes in `shared/<org>/`, never inside a project.

This works better than the single `docs/` output folder. Proposal: make `projects/<project>/design-process/` the default `output_folder`, and have agents resolve it from the project repo's `AGENTS.md`.

## Legacy, pending removal

`src/module.yaml`, `src/module-help.csv`, `src/agents/*.agent.yaml`, `tools/cli/`, `_wds/` and the schema tests belong to the old BMad installer. `src/workflows/` (the long step files) is still referenced as source material and will be migrated into agent skills phase by phase.
