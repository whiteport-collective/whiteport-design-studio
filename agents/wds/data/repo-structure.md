# The repo structure: folders with one owner

**Status: direction (2026-10-03).** Being tested in visita-kommunikation. What is under Open is not decided.

## The pattern

The root consists of folders that can be dropped in. Each top folder is one *kind* of thing, and each subfolder has *one owner*.

| Top folder | Subfolder = owner | Example |
|---|---|---|
| `agents/` | the source | `agents/wds/`, `agents/web247/`, `agents/martenangner/` |
| `governance/` | the source of the policy | `governance/wds/`, `governance/visita/` |
| `projects/` | the project | `projects/enkarriartack/` |
| `users/` | the person | `users/martenangner/` |
| `sessions/` | the person and the agent | `sessions/martenangner/saga/` |

Next to them lies the content shared between projects, at the level it serves: `brand/`, `people/`, `communication/`, `contacts.md`, `timeline.md`, `org-profile.md`. See [Shared material](#shared-material).

Three rules:

1. **A folder has one owner.** It is replaced as a whole and can be dropped into another repo.
2. **The sync copies folders, not files.** It owns a synced folder completely and may therefore also delete what has disappeared in the source.
3. **You read through a flat view**, not through the folder tree: `AGENTS.md`, the policy list in `governance/` and the plan's views. Storage follows the owner, and the view shows everything along the dimension you need.

## Shared material

**Decided (Mårten, 2026-10-13).** What is shared between projects lives at the level it serves, never inside a project and never in a generic `shared/` folder.

| The repo | The level | Example |
|---|---|---|
| Belongs to one client or organisation | the root | `brand/`, `people/<person>/`, `communication/`, `contacts.md`, `timeline.md`, `org-profile.md` |
| An agency's repo with several clients | the client's folder, next to the client's projects | `<client>/brand/` |

- A folder called `shared/` is a last resort, when nothing else works. Older repos often have `shared/<org>/`. Read what is there and propose moving it to the right level.
- **The brand lives in `brand/`**, once, at the level it serves. It has three parts:

  | Part | What |
  |---|---|
  | `brand/visual-identity/` | The visual direction (`visual-direction.md`), the mark, the moodboard and the assets. Why and how it looks. |
  | `brand/tone-of-voice.md` | What we believe, how we sound, the words and the storytelling principles. For the whole company. |
  | `brand/design-system/` | The tokens (`design-tokens.md`) and the components more than one project uses. |

- `people/`, `communication/`, `contacts.md`, `timeline.md` and `org-profile.md` lie next to `brand/`, not inside it.
- Each project has a thin `D-Design-System/` with only the components that only that project uses. When a second project needs a component, it moves up to `brand/design-system/`. A token is changed only in `brand/design-system/`, never in a project.
- In the product brief, `A-Product-Brief/02-content-language.md` is a short pointer to `brand/tone-of-voice.md` and `03-visual-direction.md` a short pointer to `brand/visual-identity/`, both plus what applies only to the project. If there is no `brand/` when the voice or the visual direction is written the first time, what applies to the whole company is written in `brand/` and what is the project's own in the project file.
- Reference: welqora-analysis, see the rule in its `AGENTS.md`, `brand/README.md` and the root folders `brand/`, `people/`, `communication/` and `timeline.md`.

## A source inside `agents/`

Every source has the same shape, whether it is WDS, an organisation or a person:

```
agents/<source>/
├── <agent>/      one folder per agent: instructions.md, references/, subagents/
├── skills/       all the source's skills
├── tools/        all the source's tools
└── data/         shared material and templates
```

- **All agents can use all skills**, from every source in the repo. `used_by:` in a skill says which agents usually run it. It is a description, not a permission.
- A source without agents is a pure skill library.
- Examples: `agents/wds/` (Idun, Saga, Freya, Mimir), `agents/taste/` (an external design source without agents), `agents/visita/` (Vinka and Visita's skills), `agents/martenangner/` (Ivonne and Mårten's own skills).
- **An external source** is copied unchanged, with its license and `source.md` (origin, commit, review), and is updated only through a reviewed diff.

## Marking

- **Underscores only for working material** in a project, like `_progress/` next to `A-Product-Brief/`. It means "machinery, not delivery".
- **No underscores on the top folders.** They are content people open every day, and `_` says "do not touch". Astro and Jekyll also skip `_` folders.
- **A synced copy is marked with a file in the folder**, not with the folder name. The same folder is the source in one repo and a copy in another, and the paths must be the same everywhere. The file is called `.source` and states `source: <repo>@<sha>`, for both `agents/wds/` and `governance/`. `.wds-sync` only means that the repo wants WDS.
- **No shared `_wds/`.** The client's projects, policy and users are not WDS's, and only what WDS owns lives in WDS folders.

## Governance

```
governance/
├── policies.md      the flat list: all policies in reading order
├── wds/             WDS default policy, synced and read-only
├── <org>/           the organisation's policy, source in one repo, mirrored to the organisation's other repos
└── <project>/       tightenings that apply to one repo only, when needed
```

- A synced folder is a mirror of the source and has a `.source` file (`source: <repo>@<sha>`). It is never changed in place. See [the sync tool](../tools/sync.md#governance-policy).
- Where Idun has not set up governance there is no `governance/` folder.

- When two levels say different things, the stricter one applies. A lower level may tighten but never loosen a higher one.
- Agents report incidents and propose new points at every wrap ([wrap step 6](../skills/wrap.md#6-gc-incidents-and-proposals)). They may tighten but never loosen or widen their own mandate.

## Tasks

Tasks follow their owner. No top folder for todos.

| Owner | Place |
|---|---|
| The project | `projects/<project>/_progress/plan.md` |
| The person | `users/<user>/`, or the person's private cabinet |

A person's list is a view, not a file of its own: the person's own tasks plus every plan's tasks where the person is named as responsible. The GTD contexts (@phone, @computer) are a filter on where the task is done. The format is tried freely in Visita before it becomes the standard.

## Two setups

| Setup | When | Example |
|---|---|---|
| **Split:** the organisation's repo plus code repos | a department with several projects, where someone else owns the code | a communications department and the agency that builds the site |
| **Combined:** WDS and code in the same repo | a team that both designs and builds, or a smaller project | a web agency's own repo |

- **Split:** the whole department shares one repo for WDS and agentic work. Everyone sees what is happening, material is shared instead of copied, and silos do not form. The G&C policies make it safe by governing how the agents handle other people's material.
- **Combined:** the same root folders, and the code lives in its own folder such as `app/` or `src/`.
- In both cases the project states in one place where the code lives, so that Mimir knows where to build.

## Open

- Should the person's tasks live only in the private cabinet, or also in `users/<user>/` in every repo?
- Which setup should WDS recommend to a new client?
- Where does the project state the code's location: in `AGENTS.md`, in the product brief or in a file of its own?
