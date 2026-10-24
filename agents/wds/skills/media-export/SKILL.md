---
name: media-export
description: Gör färdiga filer av det personen har godkänt: kundens mediebank (grönflaggade bilder som JPG, färdiga klipp som MP4 i hela bilden och 9:16) och filer för varje kanal (webb, sociala medier, tryck, videoheader), med rätt storlek, format och metadata. Använd när personen säger "exportera", "gör webbversioner", "gör klipp till Instagram" eller ett format behövs till en publicering.
used_by: [viska]
version: 1.0
tools: [wds/ffmpeg, wds/exiftool, wds/resolve]
---

# Exportera media

Redigeringen gör personen i Resolve: urval, färgsättning, beskärning, klipp. Viska tar det därifrån och gör en fil per kanal och format, så att den som publicerar bara behöver välja.

**Klart betyder:** varje fil som ska ut finns i `<projekt>/export/<kanal>/` med ett namn som säger vad den är, i rätt storlek och format för kanalen, med upphov och utan plats om den ska publiceras, och personen har fått en lista.

## Underlaget

- **Foton:** Resolve exporterar de redigerade bilderna i full storlek (JPEG eller TIFF) till `<projekt>/export/master/`. RAW går aldrig direkt till en kanal.
- **Video:** Resolve renderar tidslinjen i full kvalitet till `<projekt>/export/master/`. Viska gör kanalversionerna av den.
- **Kanalernas krav** står i projektet (produktbriefen eller en plan i `_progress/`). Saknas de: använd standarden i [ffmpeg-toolet](../../tools/ffmpeg.md) och skriv i rapporten vad som valdes, så att det kan stämmas av med den som publicerar.

## Namn

`<inspelning>-<ämne>-<kanal>-<löpnummer>.<ext>`, till exempel `2026-10-22-linnesalen-gruppbild-webb-01.jpg`. Små bokstäver, bindestreck. Exporter skrivs aldrig över utan personens ja; en ny version får ett nytt löpnummer.

## Metadata

Upphov och kund läggs på varje export ([exiftool](../../tools/exiftool.md)). GPS tas bort från allt som publiceras. Bilder på personer publiceras bara enligt det som gäller i projektet (samtycke, policyn i `governance/`); är det oklart, säg det i rapporten.

## Kundens mediebank

Sista steget i flödet för en fotografering. Det personen godkänt levereras färdigt till projektets mediebank, där det används till sociala medier och vad som helst (Mårten, 2026-10-24). Råmaterialet stannar i Drive. På sikt byggs en mediebank på kundens intranät; tills dess är det en mapp per projekt.

**Klart betyder:** varje grönflaggad bild och varje färdigt klipp ligger i `<projekt>/mediabank/<datum>-<plats>/`, med titel, beskrivning, nyckelord, fotograf och upphovsrätt inskrivna, och har en rad i `<projekt>/mediabank/mediabank.csv`.

- **Bilderna:** de som personen gett grön flagga i inspelningens Resolve-dokument, exporterade ur Resolve med sin färg som **JPG i full upplösning**.
- **Klippen:** varje färdigt klipp ur sitt eget dokument ([video-edit](../video-edit/SKILL.md)), både hela bilden och 9:16, som **MP4 (H.264) i full upplösning** (Mårten, 2026-10-24).
- **En mapp per inspelning**, alla kameror och fotografer tillsammans: den som letar tänker på tillfället, inte på kameran.
- **Namnen** säger inspelningen, motivet och originalet: `2026-10-22-linnesalen_servitris-bar-forratten_P1000708.mp4`, `..._9x16.mp4`, `2026-10-22-linnesalen_gruppbild_P1000604.jpg`. Små bokstäver och bindestreck.
- **Metadata** i varje fil ([exiftool](../../tools/exiftool.md)): titel, beskrivning, nyckelord, fotograf och upphovsrätt ur kameraregistret (rätt även om kameran var felinställd), inspelning, originalets namn. Personer namnges bara om projektet säger att de får det.
- **`mediabank.csv`:** en rad per fil, så att det går att söka och filtrera innan det finns en riktig mediebank.
- **En ny version** av en fil ersätter den förra, som läggs i papperskorgen; den skrivs aldrig över.

Hur det görs: [resolve](../../tools/resolve.md#mediebanken) och [exiftool](../../tools/exiftool.md).
