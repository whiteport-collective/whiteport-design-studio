---
name: meeting-live
source: wds
type: script
description: Records and transcribes what is heard (and shown) on the computer locally with Whisper, live and thoroughly afterwards, and archives the meeting. Fireflies only when the person explicitly asks for it. Everything runs on the computer, without a server and without MCP. The scripts are in meeting-live/.
used_by: [live-meeting, recording]
---

# Tool: meeting-live

**Local recording is the default (Mårten, 2026-10-21).** Fireflies handles the languages poorly, and the local transcription responds much faster. Use `local.py` (the section [Local transcription](#local-transcription-without-a-bot-default)), `refine.py` and `live.py archive`. The Fireflies parts (`join`, `watch` against Fireflies, the fetch in `archive`) are used only when the person explicitly says Fireflies. A meeting bot of our own for Google Meet is to be built for the cases where a visible participant is needed.

## Fireflies (only on explicit request)

Fireflies realtime goes straight to a jsonl file on the computer. The agent watches the file and gets new lines about every 30 seconds.

```
Fireflies (socket.io) → live.py join (in the background) → .wds/live/<time>-<title>.jsonl → live.py watch → the agent
```

The stream and the watch are two processes. The watch can be restarted at any time without losing the meeting, and it continues where it stopped (`<file>.seen`).

## Configuration

**New computer:** run `powershell -ExecutionPolicy Bypass -File agents/wds/tools/meeting-live/setup.ps1` (with `-Preload` to also download and convert the models for the thorough transcription). It installs Python if it is missing, the packages, ffmpeg and, with Intel graphics, OpenVINO, and checks that the screens are found. Can be run again.

| What | Where |
|---|---|
| Fireflies language | **Multi-Language on all meetings** (Mårten, 2026-10-17), in the Fireflies settings: several languages in the same meeting, beta. The language cannot be set in the calendar invitation. |
| The Fireflies key | The Bitwarden item `Fireflies API Key`, the password field. Fetched at run time, never written to file. |
| Python packages | `python -m pip install "python-socketio[client]"` (once per computer). The local recording: `pyaudiowpatch faster-whisper numpy pillow`, and `ffmpeg` in PATH for the screen video (`winget install Gyan.FFmpeg`). The graphics card: see below. |
| The meeting file | `.wds/live/` in the repo root, working material during the meeting. `.wds/` is gitignored. |
| The meeting archive | `communication/meetings/` at the level it concerns (the repo root for a client), with the index `communication/meetings.md`. The repo's `AGENTS.md` can name another place. |

The script: `agents/wds/tools/meeting-live/live.py`. In a repo without `agents/wds/` the path in the WDS repo is used.

## Actions

### Meetings in progress

```bash
FIREFLIES_API_KEY="$(bw get password 'Fireflies API Key')" python agents/wds/tools/meeting-live/live.py list
```

### Join (in the background)

The latest meeting in progress, or a specific one with `--id <id>`. Run with Bash `run_in_background`, since the process lives as long as the meeting:

```bash
FIREFLIES_API_KEY="$(bw get password 'Fireflies API Key')" python agents/wds/tools/meeting-live/live.py join --number 1
```

The output starts with `Connected to "<title>"` and `File: <path>`. The meeting's earlier lines are written first, so that the agent catches up.

**The join keeps itself alive.** If the connection to Fireflies drops and does not come back within 20 seconds, the join builds a new one in the same file and fills the gap from Fireflies' saved transcript. The watch shows `== The connection dropped, reconnecting ==` and `== Gap filled with N lines from Fireflies ==`. No line is written twice.

**If the process has died,** continue in the same file instead of starting a new one:

```bash
FIREFLIES_API_KEY="$(bw get password 'Fireflies API Key')" python agents/wds/tools/meeting-live/live.py join --continue .wds/live/<file>.jsonl
```

### Watch

**Claude Code:** Monitor with the command below and `timeout_ms: 1800000`. Each output is a batch of new lines. When the watch runs out after 30 minutes it is started again with the same command.

```bash
python agents/wds/tools/meeting-live/live.py watch .wds/live/<file>.jsonl --every 10
```

The watch prints `== MEETING OVER: <reason> ==` and exits when Fireflies stops recording, and `== ERROR: … ==` if something goes wrong.

**Copilot and Codex** have no watch that wakes them. Read new lines with `transcript` when the person asks, or between each answer.

### The whole meeting as text

```bash
python agents/wds/tools/meeting-live/live.py transcript .wds/live/<file>.jsonl
```

### Local transcription, without a bot (default)

Listens to the computer's audio out, that is what the person hears, and the microphone, and transcribes locally with Whisper when the speaker pauses, in the same format. The audio never leaves the computer. No bot joins the meeting, so it works whoever sent the invitation and on any platform. With `--no-mic` only the computer's audio: videos, webinars, podcasts.

**The others should know about it.** A bot is visible in the meeting; the local transcription is not. Use it only when everyone in the conversation knows it is being transcribed, and never in private conversations that are not about work. If a conversation turns to something else, stop the transcription.

Whisper sometimes makes up text in noise and short sounds (".", "000", `<|nospeech|>`, invented words). That is filtered out with the model's own measures of whether it was speech and how sure the words are; in the test all 32 real utterances were kept. Windows. Swedish uses KB-Whisper, which is downloaded the first time (a few minutes). Run in the background and watch the file with `watch` as usual:

```bash
python agents/wds/tools/meeting-live/local.py .wds/live/<time>-local.jsonl --them "<the others>" --me "<the person>" --lang sv
```

`--lang auto` detects the language for each piece, for meetings that switch languages.

Measured 2026-10-17 on Mårten's computer (8 cores, no graphics card acceleration) with a Swedish voice message of 131 seconds:

| Model | Time against real time | Swedish |
|---|---|---|
| `KBLab/kb-whisper-small` (`--lang sv`, default) | 0.17 | Best: names and words right |
| `small` (`--lang auto`) | 0.18 | Detects Swedish, but more errors |
| `medium` (`--lang auto`) | 0.49 | No better than KB-Whisper; with two audio sources close to real time |

The figures apply to long pieces. **Each piece costs at least about 2 seconds**, since Whisper always computes on 30 seconds of audio: 2 s of audio takes 2.4 s, 8 s takes 2.7 s and 28 s takes 4.1 s (measured 2026-10-21). Many short pieces, like "ja" and "mm" in the microphone, therefore eat the most time.

**Delay:** the audio is cut at pauses (0.5 s) and after 8 seconds at the latest (`--pause`, `--max`). Measured 2026-10-21 with four minutes of a real meeting through the speakers, with `--screen`: the first line 13 seconds after the start (the model is loaded before), then text **8 seconds after the start of the utterance** (median), 12 for 90 % and at most 15. Counted from when the speaker stopped, that is 3–4 seconds. The speakers are only told apart as "the others" and "me".

```bash
python agents/wds/tools/meeting-live/local.py .wds/live/<time>-<title>.jsonl --no-mic --them "<the video>"
```

**The recording and the transcription run separately.** The audio is always written to file and never lost, however far behind the transcription is. The transcription runs in its own thread:

- What is waiting for transcription **is merged per speaker**, up to 25 seconds per piece, so that the transcription catches up by itself.
- **Echo is filtered out live.** If the speakers are heard in the microphone, the microphone's sound level follows the computer's audio up and down; such pieces are not transcribed as "me". In the test with the computer's speakers 28 of 67 echo pieces were filtered out, and in the Visita meeting (headphones) only 1 of 59 real ones. With headphones there is no echo. `refine.py` removes the echo from its transcript afterwards.
- If the transcription is still more than `--max-lag` seconds (30) behind the speech, **it skips** the piece. The audio is still there, and the thorough transcription takes it.

**The status line.** After 10 seconds and then every minute a line is written to the transcript, which the watch shows:

```
== Status 05:15: De andra -20 dB, Mårten -46 dB · text 3 s behind the speech · 8 s echo from the speakers in the microphone ==
```

The sound level per channel shows that sound is coming in (0 dB is full, below -60 more or less silent, -90 or `no sound` when nothing is playing). Speech from the meeting is around -20 dB in the computer's audio; the microphone around -45 when the person is quiet. With the status line after 10 seconds the agent can say "your audio ✓, the computer's audio ✓" without waiting for a line: the computer's audio only shows when something is playing, so ask the person to say something or play something short if that channel is silent. "text N s behind the speech" is how far behind the transcription is. If it says that seconds were skipped, the computer cannot keep up. `audio blocks dropped` means that the sound card had to wait for the program and dropped a piece (about 0.1 s per block); a few per minute is harmless. Read the status line instead of the file sizes: Drive for desktop does not show new sizes until the file is closed.

**Windows must not throttle the process.** A process started by an agent in the background, while a video meeting has the foreground, can be throttled by Windows (EcoQoS). `local.py` turns that off for itself, and the screen video runs at a lower priority than the transcription.

**The computer must cope with the meeting too.** Whisper gets three of four cores (`--threads 3`): as fast as four, and one core is left for the audio, the video and the meeting app. With all four the playback in the speakers stuttered during a test. Measured 2026-10-21 with 90 seconds of meeting audio in the speakers (processor on average):

| What runs | Processor | Dropped |
|---|---|---|
| Only the playback | 17 % | – |
| Recording and live transcription | 43 % | no audio blocks |
| Plus screen video (`--screen`) | 49 % | 1 microphone block |

So the screen video costs little: 5 frames per second take a third of a core, and most of it is the screen capture itself (2736×1824), not the encoding. Hardware encoding (`h264_qsv`) saved only a fifth and is not used; 2 frames per second halves the cost if that should be needed.

### Recording: audio, screen and thorough transcription afterwards

Everything in one folder: the live transcript, the audio per channel and, with `--screen`, the screen as video and a picture when the screen changes. The skill [recording](../skills/recording/SKILL.md) describes the flow.

```bash
python agents/wds/tools/meeting-live/local.py --list-screens
python agents/wds/tools/meeting-live/local.py --dir "<the recording's folder>" [--monitor <n>] --them "<the others>" --me "<the person>"
```

**Choosing a screen.** `--list-screens` lists the connected screens in real pixels, for example `1. Surface Panel (\\.\DISPLAY1): 2736x1824 (main screen), position 0,0`. Use it when the skill asks which screen to record. `--monitor <n>` records only that screen, both video and pictures (and turns on `--screen`). `--screen` without `--monitor` takes all screens as one picture. No screen: neither `--screen` nor `--monitor`.

**Only part of the screen** (Mårten, 2026-10-31: a smaller film): `--region left,top,width,height` as fractions of the screen, for example `--monitor 2 --region 0,0,0.5,0.5` for the top left quarter. Applies to both video and pictures.

**Choosing a microphone:** `--mic <part of the name>`, for example `--mic Surface`, otherwise the Windows default microphone. If the status line shows -90 dB for the microphone it is silent or turned off: switch (2026-10-31: the camera microphone in the screen gave no sound).

| File | Content |
|---|---|
| `transcript.jsonl` | The live transcript, with a line `{"event": "frame", "file": …}` for each new picture and a status line every minute |
| `them.wav`, `me.wav` | The audio per channel, 16 kHz. As long as the recording: silence is filled in by the clock, also when nobody says anything. The time in the file is the same as `start` in the transcript and the time in the pictures' names |
| `screen.mp4` | The screen, 5 frames per second, 1080 p (`--screen` or `--monitor`) |
| `frames/<mm-ss>.jpg` | A picture when the screen has changed, checked every five seconds (`--screen`) |

- **Stop** by putting a file named `STOP` in the folder. Then audio and video are finished properly; a process that is killed hard leaves them broken.
- **The computer is kept awake** during the recording, so it continues when nobody touches the computer. If the lid is closed, Windows follows the setting for the lid.
- **The thorough transcription** afterwards: a larger model, all the audio in one pass, a more thorough search, and the echo from the speakers removed by comparing the channels. It writes `final.jsonl`, which `archive` takes:

```bash
python agents/wds/tools/meeting-live/refine.py "<the recording's folder>" [--model KBLab/kb-whisper-medium]
```

KB-Whisper medium is downloaded the first time (about 1.5 GB). Without graphics card acceleration it takes about half the conversation's length per channel.

#### The graphics card (Intel graphics via OpenVINO)

**NVIDIA cards (2026-10-23, not tried yet):** `local.py` and `refine.py --device auto` use faster-whisper on CUDA (float16) when an NVIDIA card is present, before the Intel graphics. `setup.ps1` installs cuBLAS and cuDNN 9 as pip packages. Check on the first computer with an NVIDIA card that `ctranslate2.get_cuda_device_count()` is greater than zero; if the DLL files are not found, put `site-packages/nvidia/*/bin` in PATH.

`refine.py --device auto` (default) uses the Intel graphics when present, otherwise the processor. `--device gpu` or `--device cpu` forces one of them; `--first <seconds>` and `--out <file>` are for measuring without overwriting `final.jsonl`.

| What | Where |
|---|---|
| Packages | `openvino-genai`, and for the conversion, once, `optimum-intel[openvino]` |
| Models | `~/.venvs/models/<model>-ov` (fp16, for example `kb-whisper-small-ov` from 2026-10-14) is used first, otherwise `<model>-int8-ov`, which `refine.py` converts by itself the first time |
| Compiled kernels | `cache/` in the model folder (`CACHE_DIR`), so that the next start takes a few seconds |
| Media files with times per word | [meeting-live/ov_transcribe.py](meeting-live/ov_transcribe.py): videos and audio files, the whole file in one call, with `<id>.words.json` |

The speech detection (VAD) is still done by faster-whisper, and only the speech is sent to the graphics card, in pieces of at most 28 seconds. A meeting recording has long silent parts filled with zeros, and in them Whisper otherwise makes up text. `ov_transcribe.py` sends the whole file, which works for videos without such silence.

Measured on Mårten's computer (Intel Iris Xe):

| Model and device | Audio | Time against real time |
|---|---|---|
| KB-Whisper small, fp16, the graphics card (2026-10-14) | Three YouTube videos, 18–33 min | 8.0–8.9x |
| KB-Whisper medium, int8, the graphics card (2026-10-23) | Five minutes of a meeting, the others' channel | 3.7x, while the processor was running another transcription at the same time |
| KB-Whisper medium, int8, the graphics card (2026-10-23) | The same five minutes, the microphone (mostly silence) | 11.1x |
| KB-Whisper medium, int8, the processor | Meetings | about 2x |

**Lesson (2026-10-23):** The OpenVINO path was built 2026-10-14 but lived only in a temporary work folder and in `~/.venvs`, and was therefore rebuilt nine days later. Code that works goes into this repo the same day. It first prints how much of each audio file has sound (`them.wav: 19:13 long, sound in 4:39 of it`); if that is much less than the recording's length, audio has been lost. `final.jsonl` gets the recording's end time and length, so that `archive` writes the right time in the header and the length in the index.

#### Lessons from the Visita meeting 2026-10-21

The first real meeting with `--screen` (19 minutes, Teams) gave only the first 4.5 minutes. The causes, now fixed:

1. **The transcription and the recording ran in the same loop.** During the meeting the transcription took about three times longer than the audio (Teams, the screen video and many short pieces from the microphone). While the loop was transcribing, the audio stayed in memory, and at the stop it was thrown away: 15 minutes of audio were never written to file. The live transcript therefore came about once a minute and fell further and further behind. It could not be noticed during the meeting.
2. **The model was loaded after the audio had started recording,** so the first 25 seconds of audio landed before the clock's start: negative times at the beginning. After that the time was calculated from the clock minus the audio that was waiting, and became wrong when audio was missing.
3. **`final.jsonl` had no end time,** so `archive` wrote "11:08–11:08" and left the length empty.

The rest of that meeting cannot be recovered: the audio after about 4:40 was never written to disk, and the screen video has no audio.

### Archive

After the meeting: the whole meeting to the repo's meeting archive, merged from all the files that belong to the meeting (several connections, a new recording in the right language, the local fallback). The final transcript is fetched from Fireflies when there is one, since it is cleaner than the live transcript; otherwise the live transcript is used.

```bash
FIREFLIES_API_KEY="$(bw get password 'Fireflies API Key')" python agents/wds/tools/meeting-live/live.py archive .wds/live/<file>.jsonl [<file>.jsonl …] --out communication/meetings --lang sv --title "<the meeting's name>"
```

`--media <the media folder>` writes where the audio and video are in the transcript's header and in the index. It writes `communication/meetings/<date>-<title>.md` and adds a row to `communication/meetings.md` (date, meeting, length, Fireflies id, transcript, summary). The summary column is filled in when the summary is written. `--out` is the folder, and the index sits beside it with the folder's name. If `--out` ends in `.md` it is the transcript's file name, and the index belongs to the file's folder. Fireflies' final transcript can take a few minutes after the meeting; `--no-fetch` archives the live transcript straight away. `--lang sv` writes the archive's labels in Swedish (`--lang en`, the default, in English).

### Finish

Stop the background process. The join writes an end line by itself when the meeting is no longer in progress in Fireflies (checked every minute).

## File format

One line per event, in order:

```json
{"event": "joined", "title": "…", "meeting_id": "…", "participants": ["…"], "at": "…"}
{"n": 1, "start": 3.2, "speaker": "Anna", "text": "…", "seed": true}
{"n": 2, "start": 61.0, "speaker": "Mårten", "text": "…", "id": "<chunk_id>"}
{"event": "reconnecting", "at": "…"}
{"event": "filled", "count": 4, "at": "…"}
{"event": "ended", "reason": "…", "at": "…"}
```

`seed: true` are lines from before the connection, `fill: true` lines that filled a gap. `start` is seconds from the start of the meeting.

The local transcript also has status lines and the length in the end line:

```json
{"event": "status", "start": 75.1, "levels": {"De andra": -20, "Mårten": -45}, "lag": 3, "skipped": 0, "echo": 8}
{"event": "ended", "reason": "stopped", "at": "…", "duration": 253.4}
```

`reason` is free text for people to read. Files from before 2026-11-14 have Swedish reasons (`stoppad`, `grundlig utskrift`, `avbrutet`); nothing parses it.

## Errors

| What happens | Say and do |
|---|---|
| Bitwarden is locked | "Unlock Bitwarden: `bw unlock`, and paste BW_SESSION." Pass it in the environment per command, never save it. |
| `No meetings in progress` | "Fireflies is not recording right now. Start the recording, and I will join in 30 seconds." |
| `auth failed` | The key is wrong or has expired. Check the Bitwarden item. |
| `The package is missing` | Install `python-socketio[client]` and join again. |
| The background process exits unexpectedly | Read its output and continue in the same file with `join --continue <file>`. |
| The status line shows `no sound` or below -60 dB for a channel | Wrong device or a muted microphone. Stop and start again with the right device. |
| The status line shows that seconds were skipped | The computer cannot keep up with transcribing live. The audio is recorded anyway; the thorough transcription takes it. Headphones instead of speakers reduce the work. |
| The text is incomprehensible or in the wrong language | Fireflies has the wrong language setting. Say so straight away, start the local fallback, and ask the person to change the language in Fireflies (that gives a new meeting id; join that too). `archive` includes all the parts. |

The delay from speech to file is a few seconds (Fireflies' speech recognition), plus the watch's interval.

## Not available

**The agent cannot speak in the meeting.** There are two ways if it is needed, so that it does not have to be investigated again:

| Way | How | Fits |
|---|---|---|
| Virtual audio cable | Text to speech to a virtual microphone: VB-Cable and VoiceMeeter (Windows), BlackHole and Loopback (Mac). The person chooses the cable as microphone, and the agent speaks in the person's place. Cheap but fragile. | Own use |
| Our own meeting bot for Google Meet | To be built (decision 2026-10-21): joins as a visible participant with its own microphone. Replaces the idea of a bought meeting bot (Recall.ai, Meetstream.ai). | When a visible participant is needed |

The audio cable is enough for own use until the Meet bot exists.
