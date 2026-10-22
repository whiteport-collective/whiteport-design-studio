---
name: video-edit
description: Klipper video utifrån det som sägs. Viska skriver ut talet, föreslår klipp (bort med tystnad, omtagningar och felsägningar, eller det personen vill behålla) och lämnar en tidslinje som öppnas i DaVinci Resolve. Använd när personen vill klippa ett tal, en intervju eller ett föredrag, eller säger "klipp ihop", "ta bort pauserna" eller "gör en kort version".
used_by: [viska]
version: 1.0
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
