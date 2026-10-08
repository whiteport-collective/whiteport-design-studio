# Taste in WDS: visual quality

Every WDS agent that renders design or writes frontend code uses [Taste](../../taste/source.md), the design skills in `agents/taste/skills/`. Taste keeps the output from looking templated or AI-made. It never overrides what the project has decided.

## When

Whenever an agent produces something people will look at:

- high-fidelity design, mockups and prototypes (Freya)
- frontend code: markup, CSS, components, pages (Mimir)
- visual fixes during a feedback round (any agent)
- persona pages, presentations, reports, CVs and other rendered documents (any agent)
- the visual direction of a product brief, as vocabulary for the conversation (Saga)

Not for wireframes. They stay deliberately rough, so that the conversation is about structure, not style.

## Order of authority

1. **The spec and the approved wireframe.** What the page must do and contain.
2. **The project's own design:** the design system, `A-Product-Brief/visual-direction.md` and the client's brand (for example `shared/<org>/`).
3. **Taste** for everything the first two leave open, and as the check against generic patterns.

When Taste disagrees with 1 or 2, the project wins. A Taste rule that seems to fit better is a proposal to the person, not a change made on the agent's own.

## Which skill

| Situation | Taste skill |
|---|---|
| A new landing page, portfolio or site | `design-taste-frontend` (the main one) |
| Improving something that already exists | `redesign-existing-projects`, starting with its list of AI patterns |
| An editorial, calm, document-like expression | `minimalist-ui` |
| A premium, agency-level feel | `high-end-visual-design` |
| A raw, high-contrast, data-dense expression | `industrial-brutalist-ui` |

Read the skill's `SKILL.md` in full before the first render in a session, and take only what fits the brief. Taste's rules are contextual, not a checklist that fires on its own.

**Consistency over variance.** Some Taste skills ask for a new layout every time. In a WDS project, the design system and earlier approved pages win: vary within the system, never away from it.

## Before showing anything

Run the AI-pattern check from `redesign-existing-projects` on the result: generic gradients, default card grids, placeholder imagery, empty hero phrases and the like. Fix what you find, or name it if the project's design asks for it.

## Print and PDF

Taste is written for the web. For print and PDF, take the typography, colour, whitespace and the AI-pattern check. Skip motion, hover states, stock imagery services and background effects.

## Where the files are

`agents/taste/` in the repo you work in. If the repo has no copy yet, read it from whiteport-design-studio and suggest `/sync-skills`.
