---
name: video-edit
description: Klipper video, utifrån det som sägs och utifrån bilden. Tal och intervjuer klipps på orden; en reel för sociala medier klipps ihop av ögonblicken, i 9:16 med egen följning och musik. Allt lämnas som tidslinje i DaVinci Resolve. Använd när personen vill klippa ett tal, en intervju eller ett föredrag, vill ha en reel eller highlights, eller säger "klipp ihop", "ta bort pauserna" eller "gör en kort version".
used_by: [viska]
version: 1.1
tools: [wds/ffmpeg, wds/transcribe, wds/media-worker, wds/resolve]
---

# Klippa video

Ersätter det gamla `/edit-video`, som gjorde en tidslinje för Premiere med Deepgram. Nu sker utskriften på datorn med Whisper, och tidslinjen öppnas i Resolve. Viska klipper på orden; bilden, rytmen och färgen bestämmer personen i Resolve.

**Klart betyder:** personen har en tidslinje i Resolve med de godkända klippen och markörer för kapitel, källfilerna ligger kvar orörda i `original/`, och utskriften finns i projektet.

## Gången

1. **Utskriften med ordtider:** [transcribe](../../tools/transcribe.md) med `--words`. Finns klippets `.srt` redan bredvid klippet från katalogen, börja med att läsa den.
2. **Visa utskriften** med tider, och markera tystnad över en sekund, upprepade meningar (troliga omtagningar), utfyllnadsord och korta felstarter.
3. **Kom överens om klippen.** Snabbstädning (tystnad över två sekunder, utfyllnad, felstarter), personens egna val, eller bästa tagningen bland omtagningarna. Säg vad som tas bort innan tidslinjen skrivs.
4. **Tidslinjen:** FCP 7 XML (`xmeml`) med källans bildfrekvens och upplösning ur `ffprobe`, ett klipp per behållen del, namn som säger vad delen är, och markörer för kapitel. Den sparas i projektets arbetsmapp, inte i `original/`. Med Studio importeras den direkt ([resolve](../../tools/resolve.md)); utan Studio öppnar personen den med File → Import → Timeline.
5. **Utskriften** ligger bredvid klippet (`<klipp>.srt`). Citat som används i manus eller texter förs in i projektet i repot med en länk dit.

En ny version av klippen är en ny tidslinje. Den förra ligger kvar.

## Den tvättade versionen

För en intervju eller en talande person gör Viska automatiskt en version utan "hmm", "eh", utfyllnadsord, felstarter och långa pauser (Mårten, 2026-10-22). Den är aldrig en ny videofil som ersätter råfilen, utan en tidslinje som pekar in i råfilen, så att allt borttaget går att få tillbaka.

- **Klipplistan** `<klipp>-tvattad.csv` bredvid tidslinjen: en rad per borttagen bit med `start_ra, slut_ra, ord, varfor` (tider i råfilen) och en rad per behållen bit med `start_ra, slut_ra, start_tvattad, slut_tvattad`. Det är kartan mellan råfilens tidkoder och den tvättade versionens, åt båda hållen.
- **En markör för varje borttagen bit** i tidslinjen, vid skarven, med ordet som togs bort i markörens namn. I Resolve syns var varje "hmm" satt.
- **Lägga tillbaka:** råfilen är orörd, så ett borttaget ord kommer tillbaka genom att dra ut skarven i Resolve till tiden i klipplistan, eller genom att Viska skriver en ny tidslinje utan just det bortvalet.
- Viska klipper med marginal (en bit av andningen kvar) så att skarvarna inte låter hackiga, och säger i rapporten hur mycket som togs bort (antal och sekunder).

## Reel för sociala medier

En reel är ögonblicken från ett evenemang, i 9:16, med musik under och klippljudet av. Byggd och provad på Visitas studiebesök (v1–v7, Mårten, 2026-10-23 och 24).

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
