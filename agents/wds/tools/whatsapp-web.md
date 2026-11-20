---
name: whatsapp-web
source: wds
type: script
description: Reads a chat in WhatsApp Web in time order, with text and voice messages, and downloads it as files. Only reads; sends and changes nothing. The script is whatsapp-web/collector.js and runs in the browser tab.
used_by: []
---

# Tool: whatsapp-web

Fetches the whole chat with a contact, so that it can be archived and analysed. WhatsApp's own list of messages is the reference, so that nothing is missing.

**No WDS skill yet.** The archive (merging, transcribing voice messages, a readable version) is for now made by the project's own tool, for example `agents/welqora/tools/kommunikationsarkiv/` [communication archive] in welqora-analysis. The WDS skill for a communication archive is not written yet; when it exists it goes in `used_by:`.

## Prerequisites

- WhatsApp Web is logged in in the person's Chrome, and the agent reaches the tab through the browser tool (`javascript_exec`).
- Chrome allows multiple downloads from web.whatsapp.com.
- The person has said yes to archiving the chat, and the archive follows the project's data and confidentiality policy (`governance/`). The archive goes only into a private repo.

## Actions

Open web.whatsapp.com and the chat with the contact. Then run in the tab, one call at a time. Each call stays under about 38 seconds so that it fits within the browser tool's time limit.

1. **Install:** paste the whole of `whatsapp-web/collector.js`. The answer is `installed`.
2. **Reference:** `await __wa.list('<the contact's name>')` gives the number of messages and the first and last time, from WhatsApp's local storage.
3. **The text:** `await __wa.collect()`, repeated until `missing` is 0.
4. **The voice messages:** `await __wa.voice()`, repeated until `voice` equals `of`. Each voice message is played muted for a moment so that the audio file can be fetched.
5. **Export:** `await __wa.export('<prefix>')` downloads two files to Downloads (Hämtade filer on a Swedish Windows):
   - `<prefix>-messages.jsonl`: one message per line with `n`, `id`, `time`, `t`, `from` (`me` or `them`), `type` and `text`
   - `<prefix>-voice.json`: the voice messages as base64, keyed on the message id

## Limitations

- The message text is encrypted in WhatsApp's storage and is therefore read from the page. The list of ids and times comes from the storage.
- "View once" video cannot be saved. Images, video and documents are downloaded with WhatsApp's own download and saved outside the repo.
- WhatsApp does not load older messages when the script sets the scroll position abruptly, so `collect()` scrolls in steps and may need to be run several times.

## Never

- Send anything in WhatsApp without the person's explicit yes for that particular message.
- Save the export in a public repo.
