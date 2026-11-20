---
name: live-meeting
source: wds
description: The agent takes part in a meeting in progress through Fireflies, documents and fact-checks while it runs, and archives the whole meeting afterwards. Use when a meeting is to be documented live, or when a recorded meeting is to be archived.
used_by: [idun, saga, freya, mimir]
version: 1.0
tools: [wds/meeting-live, wds/git]
---

# Live meeting: in the meeting, not afterwards

A long meeting becomes useful only once it is documented, and a claim is worth most while it can still be asked about. The agent listens to the whole meeting, writes the note while the meeting runs and checks facts along the way. The person can keep their eyes on the meeting and read the note when it suits them.

**Usage:** `/live-meeting`, or `/live-meeting <project>` when the note is to go to a particular project.

<workflow id="live-meeting">

  <constraints>
    - The agent only takes part in conversations where everyone knows they are being recorded or transcribed. With Fireflies the bot is visible; the local transcription is not, so there the person says it. Private conversations are never transcribed, and if a conversation turns to something private the agent stops the transcription at once.
    - Everything runs locally according to the [meeting-live tool](../tools/meeting-live.md). No server, no MCP.
    - **All material is kept.** After the meeting the whole transcript is archived in the repo's meeting archive (`communication/meetings/`, or where `AGENTS.md` says), and the note goes into the project. A meeting that is not archived cannot be used later, in an agreement, a disagreement or an audit. In a public repo only the note is archived.
    - The person is sitting in a meeting. The chat gets only short lines: answers to questions and contradictions that matter now. Everything else goes in the note.
    - Keep apart what was said and what is true. A claim that could not be checked is stated as a claim, never as fact.
  </constraints>

  <step id="1-join">
    Join the latest meeting in progress according to the tool: `join` in the background, then the watch.
    If Bitwarden is locked or no meeting is running: one line on what the person should do, according to the tool's error table.

    **Check the language in the first minute.** If the text is gibberish or in the wrong language, Fireflies has the wrong language setting. Say so at once, start the tool's local fallback and ask the person to change the language in Fireflies. Every minute in the wrong language is lost.

    Decide where the note goes:
    - where the repo's `AGENTS.md` says meetings are documented, otherwise
    - in the project's input folder for the phase the meeting feeds, `projects/<project>/<phase>/input/<date>-<title>.md`.
    If the project is unclear: ask once, with a suggestion.
  </step>

  <step id="2-catch-up">
    Read what has already been said (`transcript`). Create the note with the headings below and fill in what is there.
    Write one line in the chat: that the agent has joined, where the note is, and the meeting so far in one sentence.
  </step>

  <step id="3-follow">
    For each batch of new lines:

    1. **Update the note** right away, under the right heading:

       | Heading | Content |
       |---|---|
       | Participants | name and role, as soon as they are clear |
       | Decisions | what was decided and by whom |
       | Actions | who does what, and when |
       | Claims | the claim, who made it, time in the meeting, status and source |
       | Open questions | what was left unanswered |
       | Course of the meeting | one short line per section of the meeting, with the time |

    2. **Fact-check** claims that matter for decisions: figures, dates, names, claims about companies and people, technical and legal claims. Search the repo first (brief, earlier meetings, `communication/`, `people/`, `timeline.md` at the level they apply to), then the web. The status is *confirmed*, *contradicted* or *not verified*, always with a source.
    3. **Speak up in the chat** only when a claim is contradicted by a source and it affects what is being discussed, or when someone in the meeting addresses a question to the agent. One or two lines.
    4. **When the watch runs out,** start it again with the same command. Nothing is lost.
    5. **If the connection drops,** the join handles it itself and fills the gap. If the process dies, continue in the same file with `join --continue`, at once.
  </step>

  <step id="4-close">
    When the watch shows that the meeting has ended:

    1. **Archive the whole meeting** with the tool's `archive`, with every file that belongs to the meeting: several connections, a new recording in the right language and the local fallback. Fireflies' finished transcript can take a few minutes; wait for it unless the person needs the archive right away.
    2. Finish the note: a summary at the top, with the three most important decisions and all actions. Link it in the register's summary column.
    3. Check the claims still marked *not verified* one last time.
    4. **Actions and open questions** become tasks and questions where the project keeps them, with a link to the meeting. Whatever the agent can do, it starts on (`agents/wds/data/session.md`, Drive the work to delivery).
    5. Add a line about the meeting to the project's design log, with a link to the note.
    6. Commit and push the archive, the register, the note and the log (the git tool).
    7. Show the summary in the chat and ask whether anything should go on to another agent. That is done with wrap or handoff.
  </step>

</workflow>
