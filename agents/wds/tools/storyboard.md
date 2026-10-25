---
name: storyboard
source: wds
type: script
description: Skriver ut en films storyboard ur film.yaml som en HTML-sida, en ruta per slag: en bildruta ur det klipp som redan finns, eller en blyertsskiss som genereras ur slagets beskrivning. Utan MCP.
used_by: [film-production]
---

# Tool: storyboard

**Status (2026-10-25):** inte byggt. Det här är planen; det som provas skrivs in här.

## Vad det gör

```bash
python agents/wds/tools/storyboard/storyboard.py "projects/<projekt>/film/<film>"
```

1. Läser `film.yaml`. För varje slag med `kalla: finns` tas en bildruta ur det första klippet i `material` vid dess tidkod med [ffmpeg](ffmpeg.md) (`-ss <tc> -frames:v 1`, proxyn om den finns), skalad till 960 bredd.
2. För varje annat slag genereras en **blyertsskiss** ur `bild`: svartvit, grov, ramen och vinkeln synliga, en pil för kamerarörelsen, inga ansiktsdrag, ingen text i bilden. Samma stil i hela filmen genom en referensbild (den första godkända skissen) som skickas med varje anrop.
3. Skriver `storyboard.html` bredvid `film.yaml`: rutorna i manusets ordning, med slagets id, roll, sekunder, bild och ljud under, och kanten färgad efter källan (finns, filma, licensiera, generera, grafik). Skisserna sparas i `storyboard/` och genereras bara om när slagets `bild` har ändrats.

## Bildgenereringen

Googles bildmodell (Gemini, "Nano Banana") via HTTP, med nyckeln ur Bitwarden (`bw get password "<post>"`, posten bestäms när verktyget byggs); aldrig via MCP. Promptmönster:

```
Storyboard panel, pencil sketch on white paper, loose graphite lines, light hatching for shadows, no colour, no text.
Shot: <utsnitt och vinkel>. Subject: <motiv och handling, utan namn>. Camera: <rörelse>, shown as an arrow.
Same drawing style as the reference panel.
```

Skisserna är arbetsmaterial och visas bara för personen och kunden i förproduktionen; de går aldrig in i en film. Ladda inte upp kundens förtroliga material som referens till en tjänst som tränar på uppladdat.

## Animatik

Rutorna läggs i Resolve med slagens längd och en tillfällig speakerröst (`Project.GenerateSpeech`), när tempot behöver visas före inspelningen. Ingår i verktyget när det byggs.
