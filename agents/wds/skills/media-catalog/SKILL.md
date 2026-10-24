---
name: media-catalog
description: Bedömer och gör materialet sökbart. Viska bedömer varje bild tekniskt och konstnärligt, väljer bort de uppenbart dåliga, lägger de godtagbara i inspelningens Resolve-dokument med balanserad färg och 1–5 stjärnor, skriver ut och beskriver varje videoklipp med scener och tider, och lägger de rimliga klippen i Resolve på samma sätt. Personen godkänner med grön flagga. Körs direkt efter media-ingest, och när personen säger "katalogisera", "vad finns i materialet" eller letar efter en viss bild eller ett citat.
used_by: [viska]
version: 2.0
tools: [wds/transcribe, wds/exiftool, wds/ffmpeg, wds/media-worker, wds/resolve]
---

# Katalogisera media

Materialet är bara värt något om det går att hitta. Viska skriver kunskapen om varje projekt och varje inspelning som vanlig text bredvid mediet, i den form som [media-storage](../../data/media-storage.md#kunskapen-om-materialet) beskriver: `<projekt>.md` och `logg.md` i projektet, `<datum>-<plats>.md` och `innehall.csv` i varje inspelning, och utskriften bredvid varje klipp.

**Klart betyder:** varje fil i inspelningen har en rad i `innehall.csv` med en beskrivning man kan söka på; varje videoklipp har en mapp bredvid sig med utskrift och beskrivning; inspelningens Resolve-dokument `<datum>-<plats>` har de godtagbara bilderna och de rimliga klippen med balanserad färg och stjärnor, sparat som `<datum>-<plats>.drp` i inspelningsmappen; anteckningarna och `logg.md` är uppdaterade; och personen har fått de bästa bilderna och klippen i några rader och vet att godkännandet väntar.

**Godkännandet** (Mårten, 2026-10-24): Viska ger stjärnor, personen sätter **grön flagga** i Resolve på det som ska vidare. Bara grönflaggat går till mediebanken ([media-export](../media-export/SKILL.md)) och till klippens egna dokument ([video-edit](../video-edit/SKILL.md)). När personen litar på Viskas förslag kan hon börja behandla sina favoriter på egen hand; tills dess väntar hon på flaggorna.

## Ordningen: bilderna först

**Bilderna katalogiseras först, och videon processas under tiden** (Mårten, 2026-10-22). Bilderna är mindre material och går snabbt att bedöma, och personen kan börja arbeta med dem för hand medan klippen skrivs ut och tvättas. Starta därför utskrift och proxyfiler i bakgrunden ([media-worker](../../tools/media-worker.md) `batch`, ett skript utan AI) i samma stund som materialet är kopierat, och gå sedan direkt till bilderna. Rapportera bilderna när de är klara, utan att vänta på videon.

## Bilderna

- **Titta på en förhandsbild,** inte på originalet: JPEG-filen från kameran, eller förhandsbilden inuti RAW-filen ([exiftool](../../tools/exiftool.md)), nerskalad ([ffmpeg](../../tools/ffmpeg.md)) i en arbetsmapp utanför Drive. Är en RAW och en JPEG samma bild (samma grundnamn), beskriv den en gång och låt båda raderna ha samma text.
- **Beskrivningen** är en mening på projektets språk om det man söker på: vad som händer, vilka, var, stämningen. "Långbord i dämpat ljus, gästerna skålar, Skagenröra i förgrunden." Inte tekniska data; de finns i filen.
- **Nyckelord:** de som projektet använder (talare, gruppbild, miljö, mat, detalj, stämning …) så att de går att filtrera på.
- **Bedömningen, teknisk och konstnärlig,** var för sig 1–5 med en kort kommentar. Tekniken: skärpa på motivet, rörelseoskärpa, exponering, brus, vitbalans, gärna med ett råd för nästa gång, eftersom fotografen lär sig av det. Det konstnärliga: komposition, ljus, ögonblicket, uttrycket, om bilden berättar något och bär projektets känsla.
- **Betyg** 1–5 för hur användbar bilden är för uppdraget, sammanvägt, mot projektets mål och leveranser. 5 sparas för de bästa, några procent. Betyget är ett förslag; personens flagga och betyg i Resolve gäller.
- **Bortval med skäl.** Ingen bild tas bort eller flyttas. En uppenbart dålig bild (oskarp, misstag, dubblett av en bättre, slutna ögon) får `forslag: bort` och ett `varfor` i `innehall.csv` och läggs **inte** i Resolve. Raderna med `bort` är listan över bortvalda bilder och varför; ett bortval ångras genom att ändra raden.
- **Till Resolve:** de godtagbara bilderna läggs i inspelningens Resolve-dokument, RAW när den finns, annars JPEG, med betyget som stjärnor (`SetMetadata("Rating", "1"–"5")`). 5 stjärnor är Viskas favoriter. Bilderna stannar i RAW tills de ska användas; först då exporteras de till ett format som fungerar på en tidslinje, och färgen balanseras med ljusets karaktär (Mårten, 2026-10-24; se [resolve](../../tools/resolve.md#inspelningens-dokument)).
- **Personer:** bara namn på dem projektets `<projekt>.md` känner igen. Övriga beskrivs.
- Många bilder delas upp på flera parallella agenter, en del var, som skriver sina rader till var sin fil som slås ihop. Varje agent får projektets `<projekt>.md` så att beskrivningarna blir enhetliga.

## Videoklippen

- **Alla klipp skrivs ut och beskrivs** (Mårten, 2026-10-24): det är det enda sättet att avgöra vilka delar och vilka klipp som går att använda till något. Utskriften görs i bakgrunden med [transcribe](../../tools/transcribe.md), och allt läggs i mappen bredvid klippet: `<klipp>/<klipp>.srt` och `.words.json`.
- **Beskrivningen** `<klipp>/<klipp>.md`: vad klippet visar, **scenerna med tider** (vad som händer från när till när, vilka, var, kamerarörelsen), citaten, ljuset (skiftar det inom klippet?), teknisk och konstnärlig bedömning, och förslag: vad delen kan användas till (projektets leveranser, mediebanken, en reel) med in- och utpunkt.
- **Raden i `innehall.csv`:** klippet i en mening och de viktigaste citaten i nyckelorden, så att det går att söka på.
- **Till Resolve:** de rimliga klippen läggs i inspelningens Resolve-dokument i en egen bin, med balanserad färg och stjärnor som bilderna, och de föreslagna in- och utpunkterna som markörer. Personen godkänner med grön flagga.
- Den tvättade versionen av tal och intervjuer görs först när ett klipp är valt ([video-edit](../video-edit/SKILL.md#den-tvättade-versionen)).

## Anteckningarna

- **Inspelningens `<datum>-<plats>.md`:** plats och tid ur `ingest.csv` och schemat, vad som hände i ordning, ljuset, källorna, klockskillnad, favoriterna med filnamn, och det som saknas för uppdraget (till exempel "ingen gruppbild").
- **Projektets `<projekt>.md`:** skapas första gången från projektet i repot (`00-index.md`, briefen) och fylls på: uppdraget, personerna, en rad per inspelning, de bästa bilderna och citaten.
- **`logg.md`:** en rad per gång: `2026-10-22 · viska (martenangner) · Katalog: 2026-10-21-middag, 380 filer, 41 klipp utskrivna`. Överlämningen skrivs som vanligt i repot vid wrap.
