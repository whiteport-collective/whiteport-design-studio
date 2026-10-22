---
name: media-catalog
description: Gör materialet sökbart. Viska tittar på varje bild och skriver vad den visar, skriver ut varje videoklipp, och för projektets och inspelningens anteckningar och logg bredvid mediet. Körs direkt efter media-ingest, och när personen säger "katalogisera", "vad finns i materialet" eller letar efter en viss bild eller ett citat.
used_by: [viska]
version: 1.0
tools: [wds/transcribe, wds/exiftool, wds/ffmpeg]
---

# Katalogisera media

Materialet är bara värt något om det går att hitta. Viska skriver kunskapen om varje projekt och varje inspelning som vanlig text bredvid mediet, i den form som [media-storage](../../data/media-storage.md#kunskapen-om-materialet) beskriver: `README.md` och `logg.md` i projektet, `README.md`, `innehall.csv` och `transkript/` i varje inspelning.

**Klart betyder:** varje fil i inspelningen har en rad i `innehall.csv` med en beskrivning man kan söka på, varje videoklipp med tal har en `.srt`, inspelningens `README.md` säger vad som hände och vad som finns, projektets `README.md` och `logg.md` är uppdaterade, och personen har fått de bästa bilderna och klippen i några rader.

## Bilderna

- **Titta på en förhandsbild,** inte på originalet: JPEG-filen från kameran, eller förhandsbilden inuti RAW-filen ([exiftool](../../tools/exiftool.md)), nerskalad ([ffmpeg](../../tools/ffmpeg.md)) i en arbetsmapp utanför Drive. Är en RAW och en JPEG samma bild (samma grundnamn), beskriv den en gång och låt båda raderna ha samma text.
- **Beskrivningen** är en mening på projektets språk om det man söker på: vad som händer, vilka, var, stämningen. "Långbord i dämpat ljus, gästerna skålar, Skagenröra i förgrunden." Inte tekniska data; de finns i filen.
- **Nyckelord:** de som projektet använder (talare, gruppbild, miljö, mat, detalj, stämning …) så att de går att filtrera på.
- **Bedömningen, teknisk och konstnärlig,** var för sig 1–5 med en kort kommentar. Tekniken: skärpa på motivet, rörelseoskärpa, exponering, brus, vitbalans, gärna med ett råd för nästa gång, eftersom fotografen lär sig av det. Det konstnärliga: komposition, ljus, ögonblicket, uttrycket, om bilden berättar något och bär projektets känsla.
- **Betyg** 1–5 för hur användbar bilden är för uppdraget, sammanvägt. 5 och `favorit` sparas för de bästa, några procent. Betyget är ett förslag; personens eget betyg i Resolve gäller.
- **Bortval med skäl.** Ingen bild tas bort. En bild som inte duger får `forslag: bort` och ett `varfor` (oskarp, dubblett av en bättre, slutna ögon, misstag). Raderna med `bort` är den fullständiga listan över bortvalda bilder och varför, och ett bortval ångras genom att ändra raden. Personen går igenom förslagen i ett granskningsblad med bilderna och förslagen förvalda, och en knapp som skickar valen tillbaka till chatten.
- **Personer:** bara namn på dem projektets `README.md` känner igen. Övriga beskrivs.
- Många bilder delas upp på flera parallella agenter, en del var, som skriver sina rader till var sin fil som slås ihop. Varje agent får projektets `README.md` så att beskrivningarna blir enhetliga.

## Videoklippen

- **Utskriften:** [transcribe](../../tools/transcribe.md) på källmappen till inspelningens `transkript/`, i bakgrunden.
- **Raden i `innehall.csv`:** vad klippet visar (en blick på en stillbild ur början och mitten) och vad som sägs i en mening, med de viktigaste citaten i nyckelorden.

## Anteckningarna

- **Inspelningens `README.md`:** plats och tid ur `ingest.csv` och schemat, vad som hände i ordning, ljuset, källorna, klockskillnad, favoriterna med filnamn, och det som saknas för uppdraget (till exempel "ingen gruppbild").
- **Projektets `README.md`:** skapas första gången från projektet i repot (`00-index.md`, briefen) och fylls på: uppdraget, personerna, en rad per inspelning, de bästa bilderna och citaten.
- **`logg.md`:** en rad per gång: `2026-10-22 · viska (martenangner) · Katalog: 2026-10-21-middag, 380 filer, 41 klipp utskrivna`. Överlämningen skrivs som vanligt i repot vid wrap.
