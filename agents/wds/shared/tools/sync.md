---
name: sync
type: script
version: "2.0.0"
description: Kör synken av skills, agenter och governance mellan WDS-repot, personens privata repo, projektrepona och datorns .claude-mapp. Skriptet ligger i sync/sync.py.
used_by: [sync-skills, idun]
---

# WDS Sync

Hur synken körs. Vad den är till för och när den körs står i skillen [sync-skills](../skills/sync-skills.md).

## Var allt ligger

| Vad | Var |
|---|---|
| Skriptet | `agents/wds/shared/tools/sync/sync.py` i WDS-repot på datorn |
| Personens katalog | `skills.json` i det privata skåpet, alltså mappen på raden `private:` i `~/.wds/me.md`. Saknas den: `~/.wds/skills.json`. |
| Mall för katalogen | `agents/wds/shared/tools/sync/catalog-template.json` |
| Tillstånd och undansparade lokala ändringar | `~/.claude/.sync-skills-state.json` och `~/.claude/commands-local-edits/` |

Kör alltid skriptet från WDS-repots egen klon, så att den senaste versionen används. Ligger den på standardplatsen är sökvägen `<dev_root>/whiteport-collective/whiteport-design-studio`.

## Köra

```bash
python "<wds-repot>/agents/wds/shared/tools/sync/sync.py"             # full synk
python "<wds-repot>/agents/wds/shared/tools/sync/sync.py" --dry-run   # visa bara
python "<wds-repot>/agents/wds/shared/tools/sync/sync.py" --no-pull   # hoppa över git pull
```

Okända flaggor synkar aldrig. Skriptet visar då hjälpen och avslutar.

## Vad skriptet gör

1. **Sparar undan lokala ändringar.** Kommandon som har redigerats direkt i `~/.claude/commands/` sedan förra synken kopieras till `~/.claude/commands-local-edits/` innan något skrivs över.
2. **Hämtar senaste versionen** (`git pull --ff-only`) av alla källrepon och projektrepon. Repon med osparade ändringar hoppas över.
3. **Kör källorna i katalogens ordning.** Senare källa vinner vid namnkrock.
   - `vendor-agents`: kopierar `agents/wds/` och adaptrarna in i alla WDS-repon, och speglar governance (se nedan). Bara från källans standardbranch utan ändringar, och bara till repon på standardbranchen utan ändringar. Commit och push av bara de filerna.
   - `pointer-skills`: skriver pekare i `~/.claude/commands/`, en fil per agent eller skill, som läser originalet.
   - `capabilities-py`, `agent-space-js`: äldre källtyper som kör källans eget installationsskript.
4. **Rapporterar krockar**, alltså samma kommando från flera källor.

## Katalogen

```json
{
  "dev_root": "C:/dev",
  "sources": [ { "name": "...", "kind": "vendor-agents | pointer-skills | ...", "repo": "...", ... } ],
  "project_discovery": { "max_depth": 2, "markers": [".claude/skills", ".claude/commands"] }
}
```

Mallen visar standardkällorna: WDS-agenterna till alla WDS-repon, WDS-kommandona globalt och personens privata repo sist. En ny källa är en ny post. Varje post har `why`, som förklarar varför källan finns.

## Kvittens

Skriptet skriver ut vad det gjorde per källa, repon som hoppades över med skäl, lokalt ändrade kommandon, krockar och governance-raden. Skillen sammanfattar det för personen.

---

## Governance policy

Keeps the policy folders in `governance/` current in every repo where governance is set up, because an agent often sees only one repo. It touches `governance/` only; how `agents/` is synced does not change.

- **On agent startup** it is a dry run: it lists what would change and writes nothing.
- **On a direct request** it writes, commits and pushes, after the person's yes. A real sync writes into repos other than the one the session works in, so it is never run without asking (principle H1 in the WDS default policy). Unknown or misspelled options never start a real sync.

### Folders

Each folder in `governance/` has one owner (`agents/wds/shared/data/repo-structure.md`). A synced folder is a copy of a whole folder, like `agents/wds/`:

| Folder | Source | Synced to |
|---|---|---|
| `governance/wds/` | `agents/wds/idun/templates/governance/` in whiteport-design-studio, file names kept (`framework.md`, `principles.md` …) | every repo where governance is set up (G1) |
| `governance/<org>/` | `governance/<org>/` in the organization's one source repo. File names may be localized (`governance/visita/ramverk.md`). | the organization's other repos |
| `governance/<project>/` | the repo itself | never synced |
| `governance/policies.md` | the repo itself. Idun creates it at setup. | never synced |

### The rules

- **A copy is a mirror of its source.** The sync replaces the whole folder: changed files are updated, new files are added, and files removed from the source are removed from the copy.
- **`.source` shows the version.** Every synced folder holds `governance/<folder>/.source` with one line:

  ```
  source: <repo>@<sha>
  ```

  `<repo>` is the source repo and `<sha>` the commit the copy was made from.
- **No `.source`, no write.** The sync writes only into a folder that has `.source`, or creates a folder that does not exist yet (with its `.source`). A folder without `.source` is a source or a local folder: the sync leaves it alone and reports it.
- **A copy is never edited.** Agents never change a folder that has `.source`. Changes are made in the source and reach the copies at the next sync. If a copy differs from the version its `.source` names, it has been edited locally: the sync reports it, leaves it, and offers to move the change to the source.
- **No governance folder, no sync.** `governance/wds/` is written only into a repo that already has a `governance/` folder, or that the sync config names as an organization's source or target. Where Idun has not set up governance there is no `governance/` folder, and the sync does not create one.
- **Only reviewed content spreads.** The source is read from its default branch, committed content only, and only when the source repo's checkout is on its default branch and clean. Otherwise nothing is synced from it, and the sync says why.
- **The target must be ready.** Same conditions as the agent sync: the target repo is on its default branch and clean. Skip and report otherwise.
- `governance/policies.md` and `governance/<project>/` are never touched.

### G1 — Find the repos and the sources

Repos are found by folder name under the dev root, as in the resume step of `agents/wds/shared/data/shared-activation.md`. No path is hard-coded: repos are named, and resolved under the dev root.

The organizations come from **the sync config**, the same file that lists the sources of vendor agents to sync. The WDS vendor-agents source has a `governance` list, one entry per organization:

```json
"governance": [
  { "org": "<org>", "governance_source": "<repo>", "repos": ["<repo>", "<repo>"] }
]
```

- `org`: the folder name under `governance/`, lowercase
- `governance_source`: the one repo where `governance/<org>/` is edited
- `repos`: the organization's other repos

**Targets for `governance/wds/`:** every repo that already has a `governance/` folder, plus every `governance_source` and every repo in a `repos` list.
**Targets for `governance/<org>/`:** the repos in its `repos` list, plus every repo whose `governance/<org>/.source` names its `governance_source`, so a repo that has had one sync stays in step even on a machine whose config lacks it.

No `governance` entry: only `governance/wds/` is synced, and only into repos that already have `governance/`.

### G2 — Sync the default

For each target repo except whiteport-design-studio:
1. `governance/wds/` exists without `.source`: skip the repo and report it.
2. Mirror `agents/wds/idun/templates/governance/` into `governance/wds/` as it is. The templates link within their folder, so nothing is rewritten.
3. Write `.source`: `source: whiteport-design-studio@<sha>`.
4. Note whether anything changed (for G4).

### G3 — Sync each organization's policy

For each organization, read the committed `governance/<org>/` in `governance_source`. For each of its targets:
1. `governance/<org>/` exists without `.source`: skip and report. It is a source or a local folder.
2. Mirror the folder, then write `.source`: `source: <governance_source>@<sha>`.

The source repo's own `governance/<org>/` has no `.source` and is never written.

### Commit

Commit only `governance/` paths, then push:

```bash
git -C <repo> add -A -- governance/
git -C <repo> commit -m "governance: synced from <source repo> <short sha>" -- governance/
git -C <repo> push
```

### G4 — Flag a conflict check

If G2 changed `governance/wds/` in a repo that holds an organization's policy, report it, in a dry run too:

> WDS default policy changed. Conflict check due for <org>: run `/idun audit governance` in <governance_source>.

The check itself is Idun's (`agents/wds/idun/skills/librarian.md`, governance-check). The sync never changes an organization's rules.
