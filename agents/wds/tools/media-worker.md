---
name: media-worker
source: wds
type: script
description: Gör de långa mediajobben på en dator som alltid är på (utskrift och tvätt av videoklipp i de delade enheterna), och kopierar kort från kameror till projektets inkorg på varje dator. Utan AI och utan server; Drive är kön. Skripten ligger i media-worker/.
used_by: [media-ingest, media-catalog, video-edit]
---

# Tool: media-worker

Två skript, och Google Drive som kö mellan datorerna:

```
kamera → card_watch.py (vilken dator som helst) → <projekt>/inkorg/<person>/
                                                       ↓  Viska sorterar (media-ingest)
                       <projekt>/<datum>-<plats>/original/<person>-<kamera>/
                                                       ↓  worker.py (datorn som alltid är på)
                       transkript/<klipp>.srt + .words.json · klipp/<klipp>-tvattad.xml + .csv · logg.md
```

Kräver Python 3, [ffmpeg](ffmpeg.md), [exiftool](exiftool.md), [transcribe](transcribe.md) (faster-whisper) och Google Drive för datorn med de delade enheterna.

## Mediaarbetaren

```bash
python agents/wds/tools/media-worker/worker.py status            # vad som väntar, per projekt
python agents/wds/tools/media-worker/worker.py run --once        # ett varv
python agents/wds/tools/media-worker/worker.py run               # var femte minut, tills den stoppas
python agents/wds/tools/media-worker/worker.py wash "<klipp>"    # tvätta ett klipp direkt
```

- `--root` är mappen med de delade enheterna, som standard `G:/Shared drives`. Arbetaren går igenom `*/projects/*/<inspelning>/original/`.
- **Utskrift:** varje videoklipp utan `<inspelning>/transkript/<grundnamn>.srt` skrivs ut, med tid per ord.
- **Tvätt, två versioner av varje klipp med tal** (Mårten, 2026-10-22): råfilen i `original/` och en tvättad version utan hummanden, utfyllnadsord och pauser, som ett enda sammanhängande klipp. Den läggs i redigeringen och klipps efter innehåll, utan att tidslinjen fylls av småbitar. Varje klipp med minst 15 ord tvättas automatiskt efter utskriften. Arbetaren skriver i `<inspelning>/klipp/`:
  - `<klipp>-tvattad.mp4`: den tvättade versionen, i råfilens upplösning och bildfrekvens (HEVC 10-bit med Intel Quick Sync, annars libx265, cirka 50 Mbit/s), så att den färgsätts som råfilen.
  - `-tvattad.csv`: tidkodskartan, varje behållen och borttagen bit med tider i råfilen och i den tvättade versionen. Skarvarna ligger på hela bildrutor. Den används för att hitta tillbaka till råfilen.
  - `-tvattad.srt`: undertexten med den tvättade versionens tider.
  - `-tvattad.xml`: samma tvätt som tidslinje mot råfilen (FCP 7 XML: File → Import → Timeline i Resolve), för den som vill dra ut en skarv.
- **Tvätta ett klipp till:** lägg en textfil `<projekt>/jobb/<namn>.tvatta` med klippets sökväg under projektet, till exempel `2026-10-22-linnesalen/original/marten-lumix-s9/P1000400.MP4`. Jobbfilen flyttas sedan till `jobb/klara/`.
- **Vad tvätten tar bort:** hummanden (eh, öh, hmm …), utfyllnadsord (liksom, typ, alltså …), ord som upprepas direkt och pauser över 0,6 s, med 0,15 s luft kvar vid varje skarv. Whisper skriver ofta inte ut hummanden alls, så de försvinner i stället som pauser. Kontrollera alltid den tvättade versionen i Resolve. Allt borttaget står i csv-filen och som en markör i tidslinjen, och kommer tillbaka genom att dra ut skarven.
- **Loggen:** varje klart jobb blir en rad i projektets `logg.md`, `media-worker` som avsändare.
- Inget skrivs i `original/`. Ett avbrutet jobb görs om nästa varv, och ett klart jobb görs aldrig om.

### Installera på datorn som alltid är på

1. Programmen och `python -m pip install faster-whisper`. Kör en utskrift av ett kort klipp en gång, så att modellen laddas ner.
2. Ingen viloläge när laddaren sitter i.
3. En schemalagd aktivitet som startar arbetaren vid inloggning (visa kommandot och få ett ja först):

```powershell
schtasks /Create /TN "WDS media-worker" /SC ONLOGON /RL LIMITED /TR "pythonw C:\dev\WDS\whiteport-design-studio\agents\wds\tools\media-worker\worker.py run"
```

## Kortläsaren

```bash
python agents/wds/tools/media-worker/card_watch.py          # bevakar, kopierar varje kort som ansluts
python agents/wds/tools/media-worker/card_watch.py --once   # kopierar de kort som sitter i nu
```

- Varje dator har `~/.wds/media.json`: `{"person": "<namn>", "inkorg": "<delad enhet>/projects/<projekt>/inkorg"}`. Byt projekt genom att ändra raden.
- Ett kort är en enhet med `DCIM` i roten: ett kort i en kortläsare, eller kameran i läget **PC (Storage)**.
- Kopieringen går genom [media-copy](media-copy.md): kontrollerad med sha256, inget skrivs över, och kortet rörs aldrig. Datorn visar en notis när den är klar. Kortet formateras i kameran först när notisen sagt att allt är kopierat och Drive har synkat.
- Loggen: `~/.wds/card_watch.log`.
- Starta vid inloggning på samma sätt som arbetaren (`card_watch.py` i stället för `worker.py run`).

## Kvar att bygga

- Arbetaren ska väcka Viska (`claude -p`) när en inkorg har legat stilla en stund, så att sorteringen sker utan att någon sitter vid datorn.
- Bevakaren mellan datorerna: status och överlämningar.
