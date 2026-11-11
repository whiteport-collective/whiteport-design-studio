---
name: bitwarden
source: wds
description: Get a secret (API key, token, password) into Bitwarden, rotate it, use it in a command, or handle a leak, without the agent or the chat ever seeing it. Use whenever a key is created, rotated, needed by a script, or has leaked.
used_by: [idun, saga, freya, mimir]
tools: [whiteport-agent-space/bitwarden]
version: 1.0
---

# Bitwarden: secrets without seeing them

Every secret the agents depend on lives in Bitwarden, and nowhere else. The agent prepares everything and runs the tool; the person does only what only they can do: create the secret at the source, copy it, and type the master password in the tool's own window. A secret that passes through the chat, a terminal prompt or a file is burned and replaced. Four secrets got out that way in two days (a GitHub token in Telegram, a bot token and a Bitwarden session key in the chat, an API key pasted at a terminal prompt, 2026-11-10 to 11), and this skill exists so it stops.

How the commands work is in the tool: `C:/dev/WDS/whiteport-agent-space/tools/auth/bitwarden/tool.md`.

## When

| Situation | What to do |
|---|---|
| A service gives a new key or token | **New** |
| A key expires, is replaced, or got out | **Rotate** |
| A script or agent needs a secret | **Use** |
| A secret shows up in the chat, a terminal, a log or a message | **Leak**, at once |

## New

1. Name the item `<Service> <kind> <machine or agent>`, for example `Anthropic API key Lighthouse`. One item per consumer, so that each can be rotated and revoked on its own.
2. Write the notes before the person does anything: what the secret is for, which scripts and agents use it, where it was created (the URL), and when it expires.
3. Tell the person exactly where to click at the source, and which settings to choose. Read the source's form first, in the browser, so the instructions match what they see. Prefer an explicit expiry of at most a year over "never", and over a short default that silently breaks an agent (Console offers 30 days).
4. The person copies the value. They paste it nowhere.
5. Start the tool's `new` with `-Window` and a `-Pattern` for the service. The person types the master password in that window.
6. Read the exit code. On 0, move on to whatever needed the secret.

## Rotate

1. Make the new secret at the source and copy it (as in New).
2. `set` with `-Window` puts it in the existing item. The old value stays in the item's password history.
3. Update every consumer listed in the item's notes, and verify that each one works.
4. Revoke the old secret at the source. Not before step 3, unless it leaked.

## Use

- A command that needs a secret gets it through the tool's `run`, as an environment variable for that run only.
- A script that needs a secret in the middle of other work reads it from the item itself, with the same unlocking as the tool. It never takes the secret as an argument or from a prompt.
- Never fall back to `.env`, `~/.bw-session`, a config file in a repo, or an environment variable that other programs inherit (OpenClaw's Claude CLI fallback inherits `ANTHROPIC_API_KEY` and would bill the API).

## Leak

1. **Say it at once**, in one line, without repeating the value.
2. **Burn it:** revoke at the source and make a new one (Rotate). A Bitwarden session key is burned with `lock`.
3. Do not try to scrub it from everywhere first. Revoking makes every copy worthless; clean-up of history and clipboard comes after, and only where the person agrees.
4. Report it under G&C at wrap (wrap step 6): where it showed up, that it is revoked, who knows. Never the value.

## Never

- Ask for a secret or the master password in the chat.
- Read, print or log a value, or read the clipboard yourself.
- Ask the person to paste into the Claude app's embedded terminal. Hidden prompts there don't take paste reliably, which is why the tool opens its own window.

## Done

The item exists with its notes, every consumer works and has been checked, the old secret is revoked, and any leak is reported.
