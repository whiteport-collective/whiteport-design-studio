# Sysadmin — Skill Operations

**Channel:** internal (whiteport only)
**Scope:** Manage WDS skills — sync, manifest, versions. Nothing else.

---

## Commands

| Action | What it does |
|--------|-------------|
| `sync` | Compile and upload all stable skills to Agent Space |
| `sync --agent <name>` | Sync one agent only |
| `sync --dry-run` | Preview what would be synced |
| `sync --channel internal` | Sync whiteport-only skills |
| `add` | Add a new entry to sync-manifest.json |
| `update` | Update an existing manifest entry |
| `bump` | Bump version numbers — manifest, SKILL.md files, or both |
| `status` | Show sync state from .sync-state.json |

---

## sync

Run from `whiteport-design-studio/`:

```bash
DESIGN_SPACE_URL="https://uztngidbpduyodrabokm.supabase.co" \
DESIGN_SPACE_ANON_KEY="<anon-key>" \
node tools/sync-from-manifest.js [--agent <name>] [--dry-run] [--channel internal]
```

Credentials: whiteport anon key (same as in `whiteport-agent-space/sync.js`).

---

## add

Add to `src/sync-manifest.json` → `instructions[]`:

```json
{
  "agent": "<agent|*>",
  "type": "<skill|workflow|agent|reference|persona|activation>",
  "file": "src/skills/<path>.md",
  "channel": "<stable|beta|internal>",
  "changelog": "<one-line description>"
}
```

Use `channel: internal` for whiteport-only skills.
Bump manifest version. Then run sync.

---

## bump

Bump version numbers across three layers:

| Layer | File | When |
|-------|------|------|
| Manifest | `src/sync-manifest.json` → `version` | Any skill change |
| WDS-EC skill | `skills/WDS/.../SKILL.md` → `version:` | When updating a skill in WDS-EC |
| WDS-E agents | `_WDS-E/agents/wds/<agent>/.../SKILL.md` → `version:` | After syncing new skill content |

Minor bump (1.3→1.4) for additions. Patch bump (1.3.0→1.3.1) for changelog-only.

---

## status

Read `src/.sync-state.json` and report last sync timestamp, agents synced, and any files newer than last sync.

---

## Rules

- Always bump manifest version when adding or changing entries.
- Always run sync after manifest changes.
- `channel: internal` = NOT distributed outside whiteport.
- Never edit compiled blobs in Supabase directly — edit source, re-sync.
- WDS-EC (`whiteport-design-studio-enterprise-codebase`) is the canonical source for Codex skills. whiteport-design-studio is the canonical source for saga/freya/mimir/idun.
