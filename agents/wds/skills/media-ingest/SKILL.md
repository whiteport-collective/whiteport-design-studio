---
name: media-ingest
description: Sorterar foto, video och ljud från projektets inkorg (eller direkt från ett minneskort) in i rätt inspelning och källa i kundens delade Google-enhet, kontrollerat och loggat. Använd när personen har laddat ner material, säger "sortera materialet", "ta in bilderna" eller sätter i ett kort.
used_by: [viska]
version: 1.0
tools: [wds/media-copy, wds/exiftool, wds/resolve]
---

# Ta in media

Personen laddar ner, Viska sorterar. Personen ska inte behöva tänka på mappar: allt läggs i projektets `media/inkorg/`, och Viska gör resten på egen hand och rapporterar efteråt (Mårten, 2026-10-22). Strukturen och principen står i [media-storage](../../data/media-storage.md).

**Klart betyder:** inkorgen är tom, varje fil ligger i `<datum>-<plats>/original/<person>-<kamera>/`, varje fil har en rad i inspelningens `ingest.csv` med sha256, och personen har fått en kort rapport.

## Så avgör Viska

- **Projektet:** det personen säger, annars det enda projektet med en tom eller fylld inkorg. Projektets namn är detsamma som i repot (`projects/<startdatum>-<slug>/`). Finns ingen projektmapp i Drive skapas den, med samma namn som i repot.
- **Datum och plats:** läs av inkorgen (`scan` i [media-copy](../../tools/media-copy.md)). Passen, tidsluckorna och projektets schema (mötesanteckningar, designloggen, kalendern) säger var personen var. En inspelning är en dag på en plats. Platsens namn är kort, med små bokstäver och bindestreck (`2026-10-22-linnesalen`). Är platsen okänd för ett pass, använd det som står i schemat för den tiden, och nämn det i rapporten.
- **Källan:** kameran ur metadata (`Model`, till exempel `DC-S9` → `lumix-s9`) och personen ur `Artist`/`Creator` i metadata, annars den som lämnade materialet. Namnet blir `<person>-<kamera>`, till exempel `marten-lumix-s9`.
- **Klockan:** när flera källor finns i samma inspelning, jämför tiden för ett ögonblick båda fångat (ett tal, en gruppbild). Skiljer det mer än en minut: skriv skillnaden i rapporten och i designloggen. Originalens tid ändras aldrig; skillnaden hanteras i redigeringsprogrammet.
- **Krockar** (samma filnamn, annat innehåll, inom samma källa): lägg den krockande omgången i en undermapp efter kortets mapp, `original/<källa>/<kortmapp>/` (till exempel `101_pana`). Filnamnen ändras aldrig.

## Gången

1. Läs av inkorgen och bestäm inspelningar och källor enligt ovan.
2. Torrkör varje del (inspelning × källa) och kontrollera planen: rätt antal, inga oväntade krockar.
3. Flytta med `--move`. Från ett minneskort kopieras det i stället, och kortet rörs aldrig.
4. När Studio finns: lägg upp projektet i Resolve med en bin per inspelning och källa ([resolve](../../tools/resolve.md)).
5. Rapportera i några rader: inspelningar, antal per källa och typ, eventuell klockskillnad, krockar, och det som var en gissning. Lägg en rad i projektets designlogg (`_progress/00-design-log.md`) i repot och committa.

## Rätta

Om något hamnat fel flyttas det till rätt plats, med samma tool, och flytten loggas. Säg till om filen redan används i ett Resolve-projekt, eftersom den då måste länkas om.
