---
name: transcribe
source: wds
type: script
description: Skriver ut talet i videoklipp och ljudfiler till .srt på datorn med KB-Whisper (faster-whisper), utan server och utan att något skrivs bredvid originalen. Skriptet ligger i transcribe/.
used_by: [media-catalog, video-edit, motion-graphics, film-production, film-assembly]
---

# Tool: transcribe

Skriptet: `agents/wds/tools/transcribe/transcribe.py`. Kräver Python 3, `ffmpeg` ([ffmpeg](ffmpeg.md)) och `python -m pip install faster-whisper` (en gång per dator). Modellen är KBLab:s svenska Whisper, samma som [meeting-live](meeting-live.md) använder; den laddas ner första gången (några minuter).

```bash
# Alla klipp i en källmapp, utskriften bredvid varje klipp
python agents/wds/tools/transcribe/transcribe.py "<inspelning>/original/<källa>" "<inspelning>/original/<källa>" --words

# Ett klipp, med tid per ord för klippning
python agents/wds/tools/transcribe/transcribe.py "<klipp>.mp4" "<arbetsmapp>" --words

# Engelska eller okänt språk
python agents/wds/tools/transcribe/transcribe.py … --lang en
python agents/wds/tools/transcribe/transcribe.py … --lang auto
```

- Kör på processorn. Räkna med ungefär klippets längd i tid för `kb-whisper-medium`; `--model KBLab/kb-whisper-small` går fortare och räcker för att hitta i materialet. Kör i bakgrunden.
- Ett klipp som redan har en `.srt` hoppas över, så en avbruten körning startas bara om. Klipp utan tal får en tom `.srt`.
- `--words` skriver också `<grundnamn>.words.json` (start, slut, ord), som [video-edit](../skills/video-edit/SKILL.md) klipper på.
