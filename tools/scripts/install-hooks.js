#!/usr/bin/env node
/**
 * Install WDS git hooks.
 * Usage: node tools/scripts/install-hooks.js
 */

import { copyFileSync, chmodSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = join(__dirname, '../..');

// Get git hooks dir
let hooksDir;
try {
  hooksDir = execSync('git rev-parse --git-path hooks', { cwd: REPO_ROOT }).toString().trim();
  if (!hooksDir.startsWith('/') && !hooksDir.match(/^[A-Z]:/)) {
    hooksDir = join(REPO_ROOT, hooksDir);
  }
} catch {
  hooksDir = join(REPO_ROOT, '.git/hooks');
}

const hooks = ['post-push'];

for (const hook of hooks) {
  const src = join(__dirname, '../hooks', hook);
  const dest = join(hooksDir, hook);

  if (!existsSync(src)) {
    console.warn(`Hook source not found: ${src}`);
    continue;
  }

  copyFileSync(src, dest);
  chmodSync(dest, 0o755);
  console.log(`Installed: .git/hooks/${hook}`);
}

console.log('\nWDS hooks installed. Skills will auto-sync to Design Space on push.');
