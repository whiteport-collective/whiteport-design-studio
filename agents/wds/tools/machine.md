---
name: machine
description: Installs and checks the programs WDS needs on a person's computer (git, GitHub CLI, Python, VS Code, Claude Code), on Windows and Mac.
type: cli
used_by: [install-wds]
---

# Tool: machine

Install only after the person's yes, one program at a time, and check it afterwards.

## Check what is there

```bash
git --version
gh --version
python --version        # Mac: python3 --version. Must be 3.10 or newer (the skill sync needs it)
code --version          # VS Code, optional
```

On a Mac, `python3` is often Apple's own `/usr/bin/python3` (3.9), even after `brew install python`. Homebrew's Python only wins when Homebrew comes first in PATH, which needs this line in `~/.zprofile` (ask first, check that it is not already there, and open a new terminal afterwards):

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
```

`which python3` should then show `/opt/homebrew/bin/python3`.

## Install

| Program | Windows (winget) | Mac (Homebrew) |
|---|---|---|
| Git | `winget install --id Git.Git -e` | `brew install git` |
| GitHub CLI | `winget install --id GitHub.cli -e` | `brew install gh` |
| Python | `winget install --id Python.Python.3.12 -e` | `brew install python` |
| VS Code | `winget install --id Microsoft.VisualStudioCode -e` | `brew install --cask visual-studio-code` |

On a Mac without Homebrew, ask before installing it (`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`).
After an install on Windows, a new terminal may be needed before the program is found.

## The dev root

The folder where all repos live, one folder per owner: `<dev_root>/<owner>/<repo>`.

- Windows: `C:/dev`
- Mac and Linux: `~/dev`

## Identity for git

```bash
git config --global user.name "<Name>"
git config --global user.email "<email>"
```
