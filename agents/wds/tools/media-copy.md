---
name: media-copy
source: wds
type: script
description: Läser av ett minneskort eller en inkorg och kopierar eller flyttar media till en inspelningsmapp, kontrollerat med sha256 och utan att något skrivs över. Skriptet ligger i media-copy/.
used_by: [media-ingest]
---

# Tool: media-copy

Skriptet: `agents/wds/tools/media-copy/media_copy.py`. I ett repo utan `agents/wds/` används sökvägen i WDS-repot. Kräver Python 3. Läser tidpunkt och kamera med [exiftool](exiftool.md) om det finns, annars filens ändringstid.

## Läs av kortet

```bash
python agents/wds/tools/media-copy/media_copy.py scan "E:/"
```

Visar antal filer per typ, vilka kameror, och passen: en rad per sammanhängande period, med ny rad efter mer än 45 minuters uppehåll. Passen är underlaget för att dela upp dagen på platser.

## Kopiera

```bash
# Torrkörning: visar vad som kopieras, vad som redan finns och vad som krockar
python agents/wds/tools/media-copy/media_copy.py copy "E:/" "G:/Shared drives/<enhet>/projects/<projekt>/media/<datum>-<plats>/original/<person>-<kamera>" --from "2026-10-22 11:30" --to "2026-10-22 15:00"

# Samma kommando med --apply kopierar
python agents/wds/tools/media-copy/media_copy.py copy … --apply
```

- `--from` och `--to` (lokal tid, `YYYY-MM-DD HH:MM`) väljer en del av kortet. Utan dem kopieras allt.
- `--model "<Model>"` väljer en kamera, med namnet som `scan` visar (till exempel `DC-S9`). Används när flera kameror ligger i samma inkorg.
- `--move` flyttar från en **inkorg** i stället för att kopiera: på samma enhet döps filen bara om, annars kopieras den, kontrolleras och tas bort ur inkorgen. Filer som redan finns med samma innehåll tas bort ur inkorgen. **Aldrig mot ett minneskort.**
- Varje fil kopieras till `<namn>.part`, kontrolleras mot källans sha256 och döps sedan om. En avbruten körning lämnar bara `.part`-filer, som kan tas bort, och körs om.
- **Finns redan med samma innehåll:** hoppas över. Samma kort kan köras flera gånger.
- **Krock** (samma namn, annat innehåll, eller två filer med samma namn på kortet): kopieras inte. Skriptet slutar med kod 2 och listar dem. Agenten frågar personen; skriptet gissar aldrig.
- **Loggen:** en rad per kopierad fil i `<inspelning>/ingest.csv`: när, sökväg under inspelningen, källa, tagen, kamera, storlek, sha256. Checksummorna används igen när mappen arkiveras.
- Utan `--move` läser skriptet bara från källan och tar aldrig bort något där.

## Rätta en fil som hamnat fel

En fil som hamnat i fel inspelning eller källa flyttas med samma skript, från den felaktiga mappen till den rätta, med `--move` och en tidsram eller kamera som väljer just de filerna. Flytten loggas i den nya inspelningens `ingest.csv`. Flytta helst innan redigeringen har börjat: en fil som ett Resolve-projekt redan använder blir offline och måste länkas om.

| Kod | Betyder |
|---|---|
| 0 | Klart, eller torrkörning utan krockar |
| 1 | En kopia stämde inte med originalet. Inget mer kopierades. |
| 2 | Krockar finns |
