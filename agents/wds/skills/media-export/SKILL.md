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

## Klipp till kundens mediebank

De värdefulla klippen ur varje inspelning levereras färdiga till kundens mediebank, i två versioner: hela bilden och stående 9:16. Råmaterialet stannar i Drive (Mårten, 2026-10-24).

**Gör mediebanksklippen först, reelen sedan.** De färdiga klippen (urval, följning, färg) är grunden för reels och annat; att göra reelen först betyder att samma arbete görs två gånger.

**Klart betyder:** för varje utvalt klipp en tidslinje i Resolve med båda versionerna, en `.drt` bredvid råklippet (`<klipp>.mediabank-NN.drt`) så att allt om klippet följer med råklippet, och två filer i `export/mediabank/<inspelning>/` med titel, beskrivning och nyckelord inskrivna, och en rad i `export/mediabank/mediabank.csv`.

### Gången

1. **Urvalet** i `<projekt>/resolve/mediabank-urval.json`: klipp, in- och utpunkt (bort med det onödiga), titel, beskrivning, nyckelord. Viska föreslår ur katalogen och utskrifternas scensammanfattningar; personen bestämmer.
2. **Följningen för 9:16:** kartan över klippet, nyckelpunkter för rutans mittpunkt. De blir riktiga nyckelpunkter i Resolve (via FCPXML), som går att flytta i Inspector.
3. **Färgen:** balanserad, med karaktär efter ljuset men utan projektets utseende. Klippet mäts över tiden, och där ljuset skiftar (kök med lysrör, sal med glödljus) delas det i zoner med var sin korrigering och en övertoning emellan. Kök och dagsljus lite sterilt, restaurang tydligt varmt, mörka partier (en dörröppning) uppljusade.
4. **Rendering** i Resolve: hela bilden i full upplösning och 9:16 i 1440x2560 (3:2 ur kameran), HEVC 10 bitar.
5. **Feedback:** personen tittar på filerna och säger vad som ska ändras; Viska öppnar klippets tidslinje (eller `.drt`), rättar och renderar om. Förra renderingen läggs i papperskorgen.

Hur det görs: [resolve](../../tools/resolve.md#mediebanken) (`mediabank.py`) och `looks.py` för färgen.
