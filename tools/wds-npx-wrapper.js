#!/usr/bin/env node

/**
 * WDS CLI - Direct execution wrapper for npx
 * Ensures proper execution when run via npx from npm registry.
 */

const { execSync } = require('node:child_process');
const path = require('node:path');
const fs = require('node:fs');

// Check if we're running in an npx temporary directory
const isNpxExecution = __dirname.includes('_npx') || __dirname.includes('.npm');

if (isNpxExecution) {
  // Running via npx - spawn child process to preserve user's working directory
  const args = process.argv.slice(2);
  const cliPath = path.join(__dirname, 'cli', 'wds-cli.js');

  if (!fs.existsSync(cliPath)) {
    console.error('Error: Could not find wds-cli.js at', cliPath);
    console.error('Current directory:', __dirname);
    process.exit(1);
  }

  try {
    execSync(`node "${cliPath}" ${args.join(' ')}`, {
      stdio: 'inherit',
      cwd: process.cwd(),
    });
  } catch (error) {
    process.exit(error.status || 1);
  }
} else {
  // Local execution - use require
  require('./cli/wds-cli.js');
}
