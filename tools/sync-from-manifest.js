#!/usr/bin/env node
/**
 * Sync agent instructions from WDS repo to Design Space.
 * Reads sync-manifest.json, groups files by agent, concatenates them into
 * one compiled instruction document per agent, then upserts to agent_instructions.
 *
 * Usage:
 *   node sync-from-manifest.js                     # sync all stable
 *   node sync-from-manifest.js --channel beta       # sync beta channel
 *   node sync-from-manifest.js --agent saga         # sync one agent
 *   node sync-from-manifest.js --dry-run            # preview only
 *
 * Environment:
 *   DESIGN_SPACE_URL       Supabase project URL
 *   DESIGN_SPACE_ANON_KEY  Supabase anon key
 *   WDS_ROOT               Path to WDS repo (default: auto-detect)
 */

import { readFileSync, existsSync, writeFileSync } from 'fs';
import { join, basename, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createHash } from 'crypto';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = process.env.WDS_ROOT || join(__dirname, '..');

// --- Load env ---
for (const envPath of [join(REPO_ROOT, '.env'), join(__dirname, '../../design-space/.env')]) {
  if (existsSync(envPath)) {
    for (const line of readFileSync(envPath, 'utf8').replace(/\r/g, '').split('\n')) {
      const match = line.match(/^([^#=]+)=(.*)$/);
      if (match && !process.env[match[1].trim()]) {
        process.env[match[1].trim()] = match[2].trim();
      }
    }
  }
}

const SUPABASE_URL = process.env.DESIGN_SPACE_URL;
const SUPABASE_KEY = process.env.DESIGN_SPACE_ANON_KEY;

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('Missing DESIGN_SPACE_URL or DESIGN_SPACE_ANON_KEY');
  process.exit(1);
}

// --- Args ---
const DRY_RUN = process.argv.includes('--dry-run');
const CHANNEL = (() => {
  const idx = process.argv.indexOf('--channel');
  return idx !== -1 ? process.argv[idx + 1] : 'stable';
})();
const AGENT_FILTER = (() => {
  const idx = process.argv.indexOf('--agent');
  return idx !== -1 ? process.argv[idx + 1] : null;
})();

// --- Load manifest ---
const manifestPath = join(REPO_ROOT, 'src/sync-manifest.json');
if (!existsSync(manifestPath)) {
  console.error(`Manifest not found: ${manifestPath}`);
  process.exit(1);
}
const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
console.log(`WDS Instruction Sync v${manifest.version}`);
console.log(`Repo: ${REPO_ROOT}`);
console.log(`Channel: ${CHANNEL}`);
if (AGENT_FILTER) console.log(`Agent filter: ${AGENT_FILTER}`);
console.log();

// --- Filter ---
const filtered = manifest.instructions.filter(i => {
  if (i.channel !== CHANNEL) return false;
  if (AGENT_FILTER && i.agent !== AGENT_FILTER && i.agent !== '*') return false;
  return true;
});

// --- Group by agent (preserving manifest order within each group) ---
const byAgent = new Map();
for (const instr of filtered) {
  if (!byAgent.has(instr.agent)) byAgent.set(instr.agent, []);
  byAgent.get(instr.agent).push(instr);
}

console.log(`${byAgent.size} agent(s) to compile`);
console.log();

// --- Compile and upsert ---
let uploaded = 0;
let skipped = 0;
let failed = 0;
const hashMap = {};

for (const [agentId, instrs] of byAgent) {
  // Collect all readable files for this agent
  const parts = [];
  const names = [];
  for (const instr of instrs) {
    const filePath = join(REPO_ROOT, instr.file);
    if (!existsSync(filePath)) {
      console.warn(`  SKIP (not found): ${instr.file}`);
      skipped++;
      continue;
    }
    const content = readFileSync(filePath, 'utf8');
    parts.push(content);
    names.push(basename(instr.file));
    hashMap[instr.file] = createHash('sha256').update(content).digest('hex').substring(0, 12);
  }

  if (parts.length === 0) continue;

  // Compile into one document
  const compiled = parts.join('\n\n---\n\n');
  const compiledHash = createHash('sha256').update(compiled).digest('hex').substring(0, 12);

  if (DRY_RUN) {
    console.log(`  [${agentId}] ${parts.length} files → ${compiled.length} chars (hash: ${compiledHash})`);
    for (const n of names) console.log(`    · ${n}`);
    continue;
  }

  try {
    // Check for existing row
    const checkUrl = `${SUPABASE_URL}/rest/v1/agent_instructions` +
      `?agent_id=eq.${encodeURIComponent(agentId)}` +
      `&model_target=eq.claude-sonnet-4-6` +
      `&skill_level=eq.wds_default` +
      `&org_id=eq.whiteport` +
      `&client_id=is.null` +
      `&project=is.null` +
      `&repo=is.null` +
      `&select=id,version&limit=1`;

    const checkRes = await fetch(checkUrl, {
      headers: { 'Authorization': `Bearer ${SUPABASE_KEY}`, 'apikey': SUPABASE_KEY },
    });
    const existing = await checkRes.json();
    const existingId = existing?.[0]?.id;

    let res;
    if (existingId) {
      res = await fetch(
        `${SUPABASE_URL}/rest/v1/agent_instructions?id=eq.${existingId}`,
        {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${SUPABASE_KEY}`,
            'apikey': SUPABASE_KEY,
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal',
          },
          body: JSON.stringify({ content: compiled, version: manifest.version }),
        },
      );
    } else {
      res = await fetch(`${SUPABASE_URL}/rest/v1/agent_instructions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${SUPABASE_KEY}`,
          'apikey': SUPABASE_KEY,
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal',
        },
        body: JSON.stringify({
          agent_id: agentId,
          model_target: 'claude-sonnet-4-6',
          skill_level: 'wds_default',
          org_id: 'whiteport',
          content: compiled,
          version: manifest.version,
        }),
      });
    }

    if (res.ok) {
      uploaded++;
      console.log(`  OK [${agentId}] ${parts.length} files compiled (${compiled.length} chars)`);
    } else {
      failed++;
      console.error(`  FAIL [${agentId}]: ${await res.text()}`);
    }
  } catch (err) {
    failed++;
    console.error(`  FAIL [${agentId}]: ${err.message}`);
  }
}

console.log();
console.log(`Done: ${uploaded} compiled+uploaded, ${skipped} files skipped, ${failed} failed`);

// Write sync state
if (!DRY_RUN && failed === 0) {
  const state = {
    synced_at: new Date().toISOString(),
    manifest_version: manifest.version,
    channel: CHANNEL,
    files: hashMap,
  };
  const statePath = join(REPO_ROOT, 'src/.sync-state.json');
  writeFileSync(statePath, JSON.stringify(state, null, 2));
  console.log(`Sync state written to src/.sync-state.json`);
}

if (failed > 0) process.exit(1);
