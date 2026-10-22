# Whiteport Design Studio — instructions for all AI agents

Applies to every agent working in this repo: Claude, Copilot, Codex and others. Tool-specific files (`CLAUDE.md`, `.github/copilot-instructions.md`) are thin adapters that point here.

## What this repo is

The source of the WDS agents: **Idun** (setup, governance and the skill library), **Saga** (strategy), **Freya** (UX design), **Mimir** (build) and **Viska** (media: photo and video). They live in [agents/wds/](agents/wds/README.md). Project repos get a copy through `/sync-skills`; changes are made here, never in a copy.

WDS is its own framework, fully independent of BMad. Mårten Angner approves everything at WDS level. It is open to other frameworks: another source is simply another folder under `agents/<source>/`.

## Rules

- **All folder and file names in lowercase.**
- **Skill = what, tool = how, instructions = who.** Commands and API calls belong in a tool, never in a skill or instructions file.
- **No secrets in any file.** All keys live in Bitwarden and are fetched at runtime with `bw get password "<item>"`. Files may name the Bitwarden item, never the value.
- **Paths are relative to the repo root** (`agents/wds/skills/...`), so they work unchanged in project repos.
- **Policy lives in `governance/`**, one folder per source: `governance/wds/` (the default, a copy of `agents/wds/data/templates/governance/`), `governance/<org>/` (the organization's policy, edited only in its source repo) and, optionally, `governance/<project>/` (tightenings). `governance/policies.md` lists the files in reading order, and agents follow it at session start. A folder with a `.source` file is a synced copy and is never edited. Repos where Idun has not set up governance have no `governance/` folder. See [agents/wds/README.md](agents/wds/README.md#governance-policy).
- **Memory lives in the project repo** (`sessions/<user>/<agent>/`, `users/<user>/`, `projects/<project>/_progress/`). Every wrap is a handover — to the same agent or another one. Agent Space is only for realtime and is optional.

## Proposed: projects/ instead of docs/

Tested in visita-kommunikation (2026-09-27): every project lives in `projects/<project>/` as a **completely separate WDS folder structure** (A-Product-Brief … E-Development, `_progress/`). The WDS folders lie directly in the project folder, with no `design-process/` level in between: `projects/` already says what the folder is. One repo can then hold several WDS projects, and each one keeps its own design log. Material shared across projects (brand, people, communication, contacts, timeline, org profile) lives **at the level it serves**, never inside a project: the repo root when the repo belongs to one client or organisation (`brand/`, `people/<person>/`, `communication/`, `contacts.md`, `timeline.md`, `org-profile.md`), the client's folder in an agency repo with several clients (`<client>/brand/`). A `shared/` folder is a last resort, used only when nothing else works (Mårten, 2026-10-13). The brand exists once, in three parts: `brand/visual-identity/` (the visual direction, mark, moodboard, assets), `brand/tone-of-voice.md` (what we believe, how we sound, the words) and `brand/design-system/` (the tokens and the components more than one project uses). Each project keeps a thin `D-Design-System/` with only its own components, and its `02-content-language.md` and `03-visual-direction.md` point to `brand/`.

This works better than the single `docs/` output folder. The wider pattern (folders with one owner: `agents/`, `governance/`, `projects/`, `users/`, `sessions/`, and where tasks live) is in [agents/wds/data/repo-structure.md](agents/wds/data/repo-structure.md). Proposal: make `projects/<project>/` the default `output_folder`, and have agents resolve it from the project repo's `AGENTS.md`.

## Legacy, pending removal

`src/module.yaml`, `src/module-help.csv`, `src/agents/*.agent.yaml`, `tools/cli/`, `_wds/` and the schema tests belong to the old BMad installer. `src/workflows/` (the long step files) is still referenced as source material and will be migrated into agent skills phase by phase.
