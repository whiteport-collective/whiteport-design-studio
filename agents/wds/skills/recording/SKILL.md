---
name: recording
description: Records everything that is heard, and on request what is shown, on the person's computer, and transcribes it live and thoroughly afterwards. Media stays in the person's private media folder; the transcript of an official meeting goes to the right project, cleaned of anything private. Use when the person wants the agent to take part in a meeting or call, in any words ("spela in" [record], "ta del av mötet" [take part in the meeting], "delta i mötet" [join the meeting], "gå med" [join], "join", "lyssna" [listen], "livetolka" [interpret live]), wants a call, a video or a webinar transcribed, or wants the agent to follow what is shown on the screen. Fireflies only when the person says Fireflies.
used_by: [idun, saga, freya, mimir]
version: 1.0
tools: [wds/meeting-live, wds/git]
---

# Recording

A conversation is worth most when everything is kept: what was said, what was shown and what was decided. The recording happens on the person's own computer, with no bot in the meeting, so it works in every call and on every platform (Meet, Teams, Zoom, Messenger, phone through the computer) and for any other sound, such as videos and webinars. The audio is transcribed on the computer.

Two rules, without asking each time (Mårten, 2026-10-17, tightened 2026-11-02):
- **Media stays private.** Audio, screen video and images are too large for git. They are saved in the person's private media folder, locally on the computer or on a network drive such as Google Drive, and are not moved. The person decides later what is done with them.
- **The transcript goes to the project when the meeting was official.** The thorough transcript of a meeting held in the project's name is archived in that project's meeting archive, and anything private is cleaned out first: what was said about things other than the work, before, after and in between. Other conversations are private, and the transcript stays in the media folder.

How it is done is in the [meeting-live tool](../../tools/meeting-live.md): `local.py --dir` for the recording, `refine.py` for the thorough transcript and `live.py archive` for the archive.

## Start

The person should be able to say it in any words: **"spela in"** [record], "ta del av mötet" [take part in the meeting], "delta i mötet" [join the meeting], "gå med i mötet" [join the meeting], "join", "livetolka mötet" [interpret the meeting live]. Anything that means the agent should take part in a conversation is this skill (Mårten, 2026-10-23: "ta del av mötet" went to the Fireflies join and cost the start of the meeting). The agent understands at once, connects everything and checks the audio itself. The only question before the start is which screen to record (Mårten, 2026-10-21).

**This is the local recording, not Fireflies.** Never join through Fireflies (`/join`, `live.py join`) when the person says "spela in" [record]: on 21 October that cost six minutes of a meeting. Fireflies is used only when the person explicitly says Fireflies.

**Decision (Mårten, 2026-10-21): we are moving away from Fireflies.** Fireflies handles the languages poorly, and the local transcription responds much faster. Local recording is the default. A meeting bot of our own for Google Meet is to be built for the cases where a visible participant is needed.

1. **Ask which screen**, in a message with buttons (Mårten 2026-10-23: "snyggt" [neat], keep it that way): list the connected screens (name, resolution, which one is the main screen) plus "no screen". Nothing else in the question. **When the request names the sources** (a screen or "no screen", the microphone, the computer's audio, as in "spela in datorskärmen och datorns mikrofon" [record the computer screen and the computer's microphone]), skip the question and start at once with what was named, the screen matched to the names in `screens:` in `.wds/me.md`. Ask only about a source the request leaves out and the defaults do not cover (Mårten, 2026-11-27: "om jag anger källorna i min beställning då kan du starta direkt" [if I name the sources in my request, you can start at once]).
2. **Start right away** after the answer: the chosen screen, the computer's audio and the microphone. Only when the person says it is a video or a webinar: `--no-mic`.
   - **The media folder:** `recordings:` in `.wds/me.md`. The folder is named `<datum>_<tid>-inspelning` [`<date>_<time>-recording`]; the title is added in the archive afterwards. If `recordings:` is missing: suggest a place in the person's private Drive, ask once and write the answer in `.wds/me.md`. It is the only question allowed before the start.
   - The speakers are named `--them "De andra" --me "<the person's name>"` for now. The names are set in the archive.
   - Run in the background and start the watch, according to the tool.
3. **Check the audio yourself** within a minute:
   - Which devices is the recording listening to (the first lines of the output: `Listening: … <- <device>`, `Lyssnar: … <- <enhet>` in older versions)? Are they the devices the person actually uses (headset, Bluetooth headphones, speakers)? Wrong device: stop and restart with the right one, at once.
   - Does the status line (`== Status 00:15: … ==`, after 15 seconds and then every minute) show the audio level for both channels, and is the text only a few seconds behind the speech? If it says seconds were skipped, say so: the audio is recorded anyway.
   - **Headphones first, always when they are there** (Mårten, 2026-11-10: "Välj alltid dem om det går" [Always choose them if possible]). The computer's audio is taken from the headphones and the microphone from the headset: `--mic "Headset Microphone"`. If there is no headset microphone, the computer's built-in one. Never a microphone in an external device (screen, camera): the screen's microphone recorded silence three times (2026-11-05, 2026-11-10). List the inputs before the start if you are unsure what is there.
   - Are lines coming from **both** channels? Until the first line has come from a channel: **show a random two-digit number** in the chat, ask the person to say it, and check that exactly that number appears in the transcript (Mårten, 2026-11-01 and 2026-11-05). If the speech recognition is loading for the first time (a few minutes), say so in one line; the audio is recorded anyway.
   - Then say in **one** line: "The recording is running: your audio ✓, the computer's audio ✓, the screen ✓." Or what is not working and what you are doing about it.
4. **Then ask, in one message:** what is it about, which project does it concern, and who is taking part? The answer steers the comments during the meeting and where the transcript is archived.

Everyone in the conversation knows it is being recorded. It is legal to record a conversation you take part in yourself; in a work setting the person tells the others that an agent is reading along, since the text goes on to an AI service. The person decides about private conversations.

## During the recording

The recording continues until the person says stop, also when nobody is talking and nobody is at the computer: the audio is as long as the recording, and the computer is kept awake. The lid should be open. Follow the conversation as in [live-meeting](../live-meeting.md): short lines in the chat only when someone asks something or something needs to be said now. The watch wakes the agent for every line; do not answer "I'm following" to each one, write only when there is something to say (2026-10-23: a fifty-minute meeting produced about a hundred such lines). With the screen on, there is an image for every time the screen changed (`== Picture … ==` in the watch). Look at it when what is said depends on what is shown: a figure in a presentation, a document, a site.

## Stop

When the person says "stoppa" [stop]:

1. **Stop properly** by putting the file `STOP` in the recording's folder, so that the audio and video are closed whole.
2. **The thorough transcript:** run `refine.py` on the folder. Say roughly how long it takes, and run it in the background.
3. **The transcript to the project:** decide whether the meeting was official and which project it concerned, from what was said and who took part. If it is unclear, ask once with a suggestion. Clean out what is private, archive `final.jsonl` with `live.py archive` in that project's repo, with a line in the register pointing to the media folder, and commit.
4. **Say in one line** where the transcript went and that the audio and video stay in the media folder.

Conversations that were not official meetings get no transcript in any repo; it stays in the media folder together with the audio.

Media never belongs in git: audio and video live in Drive, transcript and summary in the repo.
