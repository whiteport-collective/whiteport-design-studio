const path = require('node:path');
const fs = require('fs-extra');
const { BaseIdeSetup } = require('./_base-ide');

/**
 * Codex IDE setup handler for WDS
 *
 * Installs:
 * - .codex/prompts/wds/<agent>.md  — agent launchers
 * - .codex/<guide>.md              — implementation context guides
 */
class CodexSetup extends BaseIdeSetup {
  constructor() {
    super('codex', 'Codex', false);
    this.configDir = '.codex/prompts/wds';
  }

  async setup(projectDir, wdsDir, options = {}) {
    const targetDir = path.join(projectDir, this.configDir);
    await this.ensureDir(targetDir);

    // Install agent launchers
    const agents = await this.getAgents(wdsDir);
    if (agents.length === 0) throw new Error('No agents found in WDS installation');

    for (const agent of agents) {
      const launcher = this.formatAgentLauncher(agent.name, agent.path);
      const content = this.processContent(launcher, agent.metadata);
      await this.writeFile(path.join(targetDir, `${agent.slug}.md`), content);
    }

    // Install implementation context guides
    const guidesInstalled = await this.installGuides(projectDir, wdsDir);

    return { success: true, agents: agents.length, guides: guidesInstalled };
  }

  async installGuides(projectDir, wdsDir) {
    const templatesDir = path.join(wdsDir, 'src', 'workflows', '0-project-setup', 'templates', 'codex-workspace');
    const targetDir = path.join(projectDir, '.codex');
    let installed = 0;

    if (!(await fs.pathExists(templatesDir))) return installed;

    const files = await fs.readdir(templatesDir);
    for (const file of files) {
      if (!file.endsWith('.template.md')) continue;

      const src = path.join(templatesDir, file);
      const destName = file.replace('.template', '');
      const dest = path.join(targetDir, destName);

      // Don't overwrite project-specific files the user may have customized
      if ((destName === 'project-context.md' || destName === 'design-space.md') && (await fs.pathExists(dest))) continue;

      await fs.copy(src, dest);
      installed++;
    }

    return installed;
  }

  processContent(content, metadata = {}) {
    return `---
name: ${metadata.name || 'WDS Agent'}
description: ${metadata.description || 'Agent'}
---

${content}`;
  }

  async detect(projectDir) {
    return await this.exists(path.join(projectDir, '.codex'));
  }
}

module.exports = { CodexSetup };
