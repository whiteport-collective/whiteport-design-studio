const path = require('node:path');
const chalk = require('chalk');
const ora = require('ora');
const { Installer } = require('../lib/installer');

const installer = new Installer();

module.exports = {
  command: 'update-skills',
  description: 'Update WDS skills and tools to the latest version (preserves config and IDE setup)',
  options: [],
  action: async () => {
    const projectDir = process.cwd();

    console.log('');
    console.log(chalk.bold('Updating WDS skills and tools...'));
    console.log(chalk.dim(`Project: ${projectDir}`));
    console.log('');

    const spinner = ora('Copying latest skills and tools...').start();
    try {
      const { wdsDir, wdsFolderName } = await installer.updateSkills(projectDir);
      spinner.succeed(`Skills updated in ${wdsFolderName}/`);

      console.log('');
      console.log(chalk.green('✓ Done.'));
      console.log(chalk.dim(`  Skills and tools refreshed from latest WDS source.`));
      console.log(chalk.dim(`  Config, IDE integrations, and project folders unchanged.`));
      console.log('');

      process.exit(0);
    } catch (error) {
      spinner.fail('Update failed');
      console.error(chalk.red(error.message));
      process.exit(1);
    }
  },
};
