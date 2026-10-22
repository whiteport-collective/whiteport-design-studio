---
name: media-export
description: Gör färdiga filer för varje kanal (webb, sociala medier, tryck, videoheader) av det personen har redigerat, med rätt storlek, format och metadata, i inspelningens export/. Använd när personen säger "exportera", "gör webbversioner", "gör klipp till Instagram" eller ett format behövs till en publicering.
used_by: [viska]
version: 1.0
tools: [wds/ffmpeg, wds/exiftool, wds/resolve]
---

# Exportera media

Redigeringen gör personen i Resolve: urval, färgsättning, beskärning, klipp. Viska tar det därifrån och gör en fil per kanal och format, så att den som publicerar bara behöver välja.

**Klart betyder:** varje fil som ska ut finns i `export/<kanal>/` med ett namn som säger vad den är, i rätt storlek och format för kanalen, med upphov och utan plats om den ska publiceras, och personen har fått en lista.

## Underlaget

- **Foton:** Resolve exporterar de redigerade bilderna i full storlek (JPEG eller TIFF) till `export/master/`. RAW går aldrig direkt till en kanal.
- **Video:** Resolve renderar tidslinjen i full kvalitet till `export/master/`. Viska gör kanalversionerna av den.
- **Kanalernas krav** står i projektet (produktbriefen eller en plan i `_progress/`). Saknas de: använd standarden i [ffmpeg-toolet](../../tools/ffmpeg.md) och skriv i rapporten vad som valdes, så att det kan stämmas av med den som publicerar.

## Namn

`<inspelning>-<ämne>-<kanal>-<löpnummer>.<ext>`, till exempel `2026-10-22-linnesalen-gruppbild-webb-01.jpg`. Små bokstäver, bindestreck. Exporter skrivs aldrig över utan personens ja; en ny version får ett nytt löpnummer.

## Metadata

Upphov och kund läggs på varje export ([exiftool](../../tools/exiftool.md)). GPS tas bort från allt som publiceras. Bilder på personer publiceras bara enligt det som gäller i projektet (samtycke, policyn i `governance/`); är det oklart, säg det i rapporten.
