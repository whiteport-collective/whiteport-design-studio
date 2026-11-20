# WDS Glossary

Locked terminology for all WDS agents. One definition per term — no synonyms, no aliases.
Agents load this file once at activation. Do not redefine these terms locally.

---

## Phases

| Phase | Name | Owner |
|-------|------|-------|
| 0 | Alignment & Signoff | Saga |
| 1 | Product Brief | Saga |
| 2 | Trigger Mapping | Saga |
| 3 | UX Scenarios | Freya |
| 4 | UX Design | Freya |
| 5 | Agentic Development | Mimir |
| 6 | Asset Generation | Freya |
| 7 | Design System | Freya |
| 8 | Product Evolution | Mimir |

---

## Output Folder Structure

```
{output_folder}/
├── A-Product-Brief/       Phase 1 — strategic foundation
├── B-Trigger-Map/         Phase 2 — user research & personas
├── C-UX-Scenarios/        Phase 3 — journey flows
├── D-UX-Design/           Phase 4 — page specifications & design assets
└── E-Development/         Phase 5 — technical requirements, work orders, code
```

Progress files (machine-local, not committed):
```
progress/
├── [agent].md             Session state per agent
└── project-index.md       Living artifact index, updated on wrap
```

---

## Artifacts

### Strategy (Phase 1)
The suite is numbered in reading order. The numbers are fixed, and a skipped document leaves its number free.
- **Product Brief** — `A-Product-Brief/01-product-brief.md`. Strategic foundation: vision, goals, constraints, target users. Required before any design work.
- **Content Language** — `A-Product-Brief/02-content-language.md`. A short pointer to the tone of voice, plus what only applies to this project: language, SEO, content structure.
- **Visual Direction** — `A-Product-Brief/03-visual-direction.md`. A short pointer to the visual identity, plus what only applies to this project.
- **Brand** — `brand/` at the level it serves (the repo root, or the client's folder). Exists once, in three parts: the visual identity, the tone of voice and the shared design system.
- **Visual Identity** — `brand/visual-identity/`. The visual direction (`visual-direction.md`), mark, moodboard, assets. Why and how it looks.
- **Tone of Voice** — `brand/tone-of-voice.md`. What the company believes, how it sounds, its words and storytelling principles.
- **Shared Design System** — `brand/design-system/`. The tokens (`design-tokens.md`) and the components more than one project uses. A token is changed only here. Each project's thin `D-Design-System/` holds the components only it uses.
- **Platform Requirements** — `A-Product-Brief/04-platform-requirements.md`. Strategic boundaries for what is built: platforms, integrations, constraints, complexity, knowledge gaps. Not a technical spec. Required before the master PRD.

### Research (Phase 2)
- **Trigger Map** — `B-Trigger-Map/00-trigger-map.md`. User psychology mapped to business goals. Required before UX Scenarios.
- **Business Goals** — `B-Trigger-Map/01-business-goals.md`. Measurable outcomes, KPIs.
- **Persona** — `B-Trigger-Map/NN-persona-[firstname]-the-[archetype].md`. Alliterative names required (e.g. Harriet the Hairdresser).
- **Feature Impact** — `B-Trigger-Map/feature-impact.md`. Feature × persona × trigger mapping.

### Design (Phases 3–4)
- **UX Scenarios** — `C-UX-Scenarios/00-ux-scenarios.md`. User journey flows derived from Trigger Map.
- **Page Spec** — `D-UX-Design/[page-name].md`. Per-page specification: layout, content, interactions, acceptance criteria.
- **Design Tokens** — Extracted progressively during Phase 4, not upfront.

### Development (Phase 5)
- **Tech Audit** — `E-Development/000-tech-audit.md`. Living architecture document. Required before any PRD on an existing codebase.
- **Master PRD** — `E-Development/000-PRD.md`. The technical glue: architecture, dependencies, decisions and open questions. Written once after the Product Brief and Platform Requirements, updated as the project evolves. Not the same document as Platform Requirements.
- **Feature PRD** — `E-Development/NNN-[feature].xml`. One per Work Order.
- **Change Order** — `E-Development/NNN-NN-[slug].xml`. Feedback/change against a parent PRD.
- **Work Order** — `E-Development/WO-NNN-[slug].md`. Task written by Freya for Mimir. Contains: objective, scope, files, acceptance criteria.
- **Mimir Brief** — Narrative handoff document from Freya to Mimir when handing off design work.

### Progress (machine-local)
- **Design Log** — `_progress/00-design-log.md`. Project-wide progress, updated each session.
- **Project Outline** — `_progress/wds-project-outline.yaml`. Phase status, project metadata.
- **Session State** — `progress/[agent].md`. Agent-specific session state. Loaded by `/start`, written by `/wrap`.
- **Project Index** — `progress/project-index.md`. Living index of all artifacts, updated by `/wrap`.

---

## Patterns

- **Design Loop** — Freya's per-page cycle: discuss → spec → wireframe → approve → iterate → update spec → implement → browser review → extract tokens.
- **Dream Up Mode** — Three modes for artifact generation: Dialog (collaborative), Suggest (agent proposes), Dream (agent generates fully). Selected at session start.
- **Brownfield** — Project with an existing codebase. Triggers gap-map assessment before new work begins.
- **Greenfield** — Project with no existing codebase. Follows standard phase progression.
- **Gap Map** — Freya's cross-reference of what is designed vs what is built vs what has a Work Order.

---

## Names

- **Agent space** — the realtime layer (presence, messages, handoff tokens) on Supabase that WDS used until November 2026. It is being shut down and archived: handovers and messages are files in git. "Design Space" is its old name.

---

## Model Selection

| Task type | Model |
|-----------|-------|
| Any code, build, deploy, implement | Opus |
| High-stakes / production / compliance | Opus |
| Long or complex multi-step tasks | Opus |
| Strategy, spec, dialog, UX, analysis | Sonnet |
| Simple, low-stakes, short | Haiku |

Default: lightest model that fits. Prefix Next actions with `MODEL:[Haiku|Sonnet|Opus]`.

Sonnet is never recommended for writing code, even small scripts; when Saga or Freya need code, the next step goes to Opus. Codex is OpenAI's agent and never gets a Claude model: give it the strongest current GPT coding model (GPT-5.4 or later as of 2026-04).
