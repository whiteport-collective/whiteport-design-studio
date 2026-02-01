# Contributing to Whiteport Design Studio

Thank you for your interest in contributing to WDS.

## Project Overview

Whiteport Design Studio (WDS) is a strategic design methodology that uses AI agents to guide product design, from initial strategy to developer-ready specifications.

The repository contains:
- `src/` - Agent definitions, workflows, data, templates (the WDS module)
- `docs/` - Learning material, method guides, tool guides
- `tools/` - npm installer CLI

## How to Contribute

### Reporting Issues

Open an issue at [github.com/whiteport-collective/whiteport-design-studio/issues](https://github.com/whiteport-collective/whiteport-design-studio/issues).

### Development

1. Fork and clone the repository
2. Install dependencies: `npm install`
3. Test the installer locally: `node tools/cli/wds-cli.js install`
4. Make your changes
5. Submit a pull request

### Areas of Interest

- **Agent improvements** - Better prompts, new workflows, enhanced teaching
- **IDE support** - New IDE configurations in `tools/cli/lib/ide-configs.js`
- **Documentation** - Method guides, tutorials, examples
- **Installer** - CLI improvements, new commands

## Code Style

- Use CommonJS (`require`/`module.exports`) for Node.js compatibility
- Follow existing patterns in the codebase

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
