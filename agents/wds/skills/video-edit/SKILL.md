---
name: video-edit
description: Gör de godkända videoklippen färdiga, ett i taget: varje klipp får ett eget Resolve-dokument med klippets namn, en vågrät tidslinje per utvalt ögonblick (klippt, färgsatt i ljuszoner) och en stående 9:16 med den vågräta inbäddad och följd. Tal och intervjuer får en tvättad version utan pauser och utfyllnadsord. Reels klipps ihop av de färdiga klippen. Använd när klipp är godkända (grön flagga), när personen vill ha en stående version, en tvättad version av ett tal, en reel eller highlights.
used_by: [viska]
version: 2.0
tools: [wds/ffmpeg, wds/transcribe, wds/media-worker, wds/resolve]
---

# Klippa video

Tredje steget i flödet, efter [media-ingest](../media-ingest/SKILL.md) och [media-catalog](../media-catalog/SKILL.md). De klipp personen godkänt (grön flagga i inspelningens Resolve-dokument) görs färdiga **ett i taget**, som klippet med servitrisen och tallriken (Mårten, 2026-10-24). Sedan går de till mediebanken ([media-export](../media-export/SKILL.md)).

**Klart betyder:** för varje godkänt klipp ett Resolve-dokument med klippets namn, sparat som `<klipp>/<klipp>.drp` i mappen bredvid klippet, med de vågräta och stående tidslinjerna färdiga; tal och intervjuer har en tvättad version i samma mapp; och personen har fått en rad per klipp i chatten och i loggen.

## Klippets dokument

**Ett Resolve-dokument per klipp, med klippets namn** (`P1000708`), och bara det klippet i sig. Flera ögonblick ur samma klipp blir flera tidslinjer i samma dokument (Mårten, 2026-10-24).

| Tidslinje | Vad |
|---|---|
| `P1000708-01` | det utvalda ögonblicket i hela bilden: in- och utpunkt (bort med det onödiga), färgen i ljuszoner |
| `P1000708-01 9x16` | stående 1440x2560 med tidslinjen `P1000708-01` **inbäddad** (nästlad), i mitten, så att den fyller rutan i full höjd, och följd med nyckelpunkter |

1. **Ögonblicket:** in- och utpunkt ur klippets beskrivning (`<klipp>/<klipp>.md`). Börja när det händer, sluta när det är gjort (tallriken står på bordet).
2. **Färgen:** balanserad med ljusets karaktär. Klippet mäts över tiden; där ljuset skiftar (kök med lysrör, sal med glödljus, en mörk dörröppning) delas det i zoner med var sin korrigering och en övertoning emellan, så att färgen glider utan hopp. Kök och dagsljus lite sterilt, restaurang tydligt varmt, mörka partier uppljusade.
3. **Den stående versionen** ställs upp först: en ny 9:16-tidslinje med den vågräta tidslinjen inbäddad, i mitten. Rutan är alltid fylld, **aldrig svart** någonstans. Sedan följningen: nyckelpunkter som håller det viktiga (personen, tallriken) i bild och glider mjukt mellan varandra; rutan går aldrig utanför bilden. Där motivet blir litet zoomar den in något. Ändras den vågräta versionen följer den stående med, utan att göras om.
4. **Kontrollera** bilder genom hela klippet, i båda versionerna, innan klippet lämnas: fylld ruta, motivet i bild, färgen jämn över zonerna.
5. **Spara** dokumentet som `<klipp>/<klipp>.drp`. Feedback rättas i klippets dokument.

Det som Resolve kan justera (rotation, fast zoom, position, färg) görs i Resolve och renderas aldrig om; bara det Resolve inte kan göra från skript renderas med ffmpeg ([resolve](../../tools/resolve.md), [ffmpeg](../../tools/ffmpeg.md)).

## Den tvättade versionen

Valda klipp där någon pratar, presenterar eller intervjuas får en version utan "hmm", "eh", utfyllnadsord, felstarter och långa pauser (Mårten, 2026-10-22). Den görs **bara med ffmpeg på datorn**, utan Resolve (Mårten, 2026-10-24), och läggs i klippets mapp; råfilen rörs aldrig.

- `<klipp>/<klipp>-tvattad.mp4` och `.srt`, och **klipplistan** `<klipp>-tvattad.csv`: en rad per borttagen bit med `start_ra, slut_ra, ord, varfor` och en rad per behållen bit med `start_ra, slut_ra, start_tvattad, slut_tvattad`. Det är kartan mellan råfilens tidkoder och den tvättade versionens, åt båda hållen, så att utskriften finns med båda.
- Viska klipper med marginal (en bit av andningen kvar) så att skarvarna inte låter hackiga, kontrollerar med `worker.py check` ([media-worker](../../tools/media-worker.md)), och säger i rapporten hur mycket som togs bort (antal och sekunder).

## Reel för sociala medier

En reel är ögonblicken från ett evenemang, i 9:16, med musik under och klippljudet av. Den klipps ihop av de färdiga klippen i mediebanken, inte från råmaterialet (Mårten, 2026-10-24). Byggd och provad på Visitas studiebesök (v1–v7, Mårten, 2026-10-23 och 24).

**Klart betyder:** en ny tidslinje `reel-9x16-vN` i Resolve, klippen var för sig i en egen bin, och en rad i projektets logg. Personen granskar i Resolve; ingen förhandsvisning i webbläsaren.

### Vad som gör den bra

- **Människorna och ögonblicken**, aldrig tomrummet mellan dem eller ett tomt bord. Välj ögonblick ur utskrifterna (skratt, repliker) och ur katalogen, inte på måfå.
- **Hjältarna i bild**, de andra inte: den som berättar eller gör något. Någon som bara går förbi klipps bort eller ramas ut.
- **Kändisen får två klipp**, talarna som betyder något för kunden är med, och en vinkel där publiken och rummet syns.
- **Ungefär 5 sekunder per klipp.** Ett klipp med en resa (en tallrik från passet till bordet) får vara längre med en fartkurva: normal fart i början, snabbt under färden, normal när det viktiga händer, och klippet slutar när det är gjort.
- **Egen följning i varje klipp**, ingen Smart Reframe: läs kartan och sätt nyckelpunkter som glider mjukt mellan varandra. Personen i centrum, rak i bilden.
- **Gruppbilderna rör sig:** panorering över raden, eller inzoomning nära mot den som står i mitten.
- **Kronologiskt**, mjuka övertoningar (0,3 s), musik under och uttoning till svart på slutet.

### Gången

1. **Klipplistan** med ögonblicken, i ordning, och en karta över varje klipp. Nyckelpunkter efter kartan.
2. **Rendera bara det Resolve inte kan** (Mårten, 2026-10-24): följning, fartkurvor och rörliga stillbilder renderas med [ffmpeg](../../tools/ffmpeg.md#omformatering-till-916-och-reel); rotation, fast zoom, position och färgjustering sätts på klippet i [Resolve](../../tools/resolve.md#reel-i-resolve), där personen kan ändra dem. Ett klipp renderas aldrig om för något som går att justera i Resolve.
3. **Kontrollera** en bild ur varje del, och bild för bild i klipp med fartkurva, innan versionen lämnas.
4. **Ny version i Resolve:** klippen i `<projekt>/resolve/reel-vN-klipp/`, en ny tidslinje, en rad i loggen. Den förra versionen ligger kvar.
5. **Feedback:** personen tittar i Resolve och pratar, gärna med [inspelning](../recording/SKILL.md) av skärm och ljud. Varje punkt skrivs ner direkt, och listan visas som en plan innan nästa version görs. Vid lång tystnad: fråga om personen är kvar. När listan är skriven läggs inspelningen i papperskorgen.
