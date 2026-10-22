---
name: video-edit
description: Klipper video utifrån det som sägs. Viska skriver ut talet, föreslår klipp (bort med tystnad, omtagningar och felsägningar, eller det personen vill behålla) och lämnar en tidslinje som öppnas i DaVinci Resolve. Använd när personen vill klippa ett tal, en intervju eller ett föredrag, eller säger "klipp ihop", "ta bort pauserna" eller "gör en kort version".
used_by: [viska]
version: 1.0
tools: [wds/ffmpeg, wds/meeting-live, wds/resolve]
---

# Klippa video

Ersätter det gamla `/edit-video`, som gjorde en tidslinje för Premiere med Deepgram. Nu sker utskriften på datorn med Whisper, och tidslinjen öppnas i Resolve. Viska klipper på orden; bilden, rytmen och färgen bestämmer personen i Resolve.

**Klart betyder:** personen har en tidslinje i Resolve med de godkända klippen och markörer för kapitel, källfilerna ligger kvar orörda i `original/`, och utskriften finns i projektet.

## Gången

1. **Ljudet ut och skrivs ut:** ljudspåret som mono 16 kHz ([ffmpeg](../../tools/ffmpeg.md)), och en utskrift med ordtider med den lokala Whisper som [meeting-live](../../tools/meeting-live.md) använder. Läs hur dess skript tar emot en fil innan det körs första gången, och skriv in det i toolet.
2. **Visa utskriften** med tider, och markera tystnad över en sekund, upprepade meningar (troliga omtagningar), utfyllnadsord och korta felstarter.
3. **Kom överens om klippen.** Snabbstädning (tystnad över två sekunder, utfyllnad, felstarter), personens egna val, eller bästa tagningen bland omtagningarna. Säg vad som tas bort innan tidslinjen skrivs.
4. **Tidslinjen:** FCP 7 XML (`xmeml`) med källans bildfrekvens och upplösning ur `ffprobe`, ett klipp per behållen del, namn som säger vad delen är, och markörer för kapitel. Den sparas i projektets arbetsmapp, inte i `original/`. Med Studio importeras den direkt ([resolve](../../tools/resolve.md)); utan Studio öppnar personen den med File → Import → Timeline.
5. **Utskriften** arkiveras i projektet i repot (manus eller underlag), aldrig mediet.

En ny version av klippen är en ny tidslinje. Den förra ligger kvar.
