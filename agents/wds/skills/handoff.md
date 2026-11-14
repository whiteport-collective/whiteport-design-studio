---
name: handoff
source: wds
description: Hand a bounded task to another agent or person in the middle of a session. The same handover file and resume command as wrap, but the session goes on.
used_by: [idun, saga, freya, mimir]
tools: [wds/git]
---

# Handoff: hand over a task

A handoff is a handover without a wrap. It hands **one** task to someone else, and the session goes on. Everything else follows [wrap](wrap.md), so the recipient takes a handoff the same way as a wrap: with the resume command.

**Usage:** `/handoff <to> [person]`, for example `/handoff mimir` or `/handoff wera camilla`.

Ask nothing. Take everything from the conversation.

## 1. Who, which session, to whom

As [wrap step 1](wrap.md#1-who-which-session-to-whom): user, session id, from, project root and sessions folder.

- **To:** the agent in the argument. Missing: strategy → saga, design → freya, build → mimir.
- **Person:** the same person by default. Another person when the argument says so, and `all-users` when we don't know who runs it.

## 2. The handover

The same filename, folder and format as [wrap step 2](wrap.md#the-project-part), with `status: open`. `<summary>` describes the task, not the session. The words in the file are the English ones in [i18n.yaml](../data/i18n.yaml).

The content concerns the task alone:

- **Done:** what is already finished of the task, and the decisions it rests on.
- **Left:** what remains.
- **Next:** concrete steps in order, so the recipient can start at once.
- **Files:** relative links to everything the recipient needs.

If the task came from the session file's `## In progress`, note there that it was handed over, with a link.

## 3. Share

Save and share only the handover file per the git tool. The commit message is `handoff: <session-id> → <to> — <one line>`. Soul files, project log and skills are left to wrap.

## 4. Receipt

Show the recipient and the path. End with the resume command as its own code block, in the same format as [wrap step 9](wrap.md#9-receipt):

````
```
/<to> <repo> YYYY-MM-DD_HH-MM <summary>
```
````

Then continue the session where it was.
