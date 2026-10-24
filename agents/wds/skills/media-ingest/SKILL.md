---
name: media-ingest
description: Viskas start och mottagning. Tittar i projektens inkorgar och efter anslutna kameror, tar reda på projektet (läser projektfilen eller frågar), registrerar nya kameror och kontrollerar deras metadata, och sorterar allt kontrollerat in i <datum>-<plats>/<person>/<kamera>/ i kundens delade Google-enhet. Använd när Viska aktiveras, när personen ansluter en kamera eller ett kort, laddar upp material eller säger "ta in bilderna".
used_by: [viska]
version: 2.0
tools: [wds/media-copy, wds/media-worker, wds/exiftool, wds/resolve]
---

# Ta in media

Första steget i Viskas flöde för en fotografering: in, sortera, bedöma och leverera till mediebanken (Mårten, 2026-10-24). Personen ska inte behöva tänka på mappar: Viska tar reda på vad som är nytt, sorterar på egen hand och rapporterar. Strukturen står i [media-storage](../../data/media-storage.md). Nästa steg är [media-catalog](../media-catalog/SKILL.md).

**Klart betyder:** inkorgen är tom och kortet orört, varje fil ligger i `<datum>-<plats>/<person>/<kamera>/` med en rad i inspelningens `ingest.csv` (sha256), varje videoklipp har en proxy i mappen bredvid sig, och personen har fått en kort rapport.

## När Viska aktiveras

1. **Titta efter nytt:** projektens `inkorg/` på de delade enheterna och anslutna kameror och kort (en enhet med `DCIM/`).
2. **Projektet:**
   - Finns projektet redan, med inkorg och `<projekt>.md`: läs projektfilen (mål, leveranser, personer, platser, schema) och börja.
   - Ny material utan projekt (en kamera med bilder som just tagits): **fråga först**, en fråga i taget, tills Viska vet vilket projekt det är, för vem, varför, vilka som var med och var. Skapa projektet i Drive (och i repot) med `<projekt>.md` och mapparna, och börja sedan.
   - Inget nytt: fråga vad som ska göras.
3. **Kör flödet** på det nya, steg för steg, och rapportera kort i chatten när varje steg är klart. Varje steg ger en rad i projektets `logg.md`.

## Var materialet hör hemma

- **Datum och plats:** filernas tidsstämplar mot projektets schema. Passen och tidsluckorna säger när personen bytte plats. En inspelning är en dag på en plats, med ett kort namn (`2026-10-22-linnesalen`). Är platsen okänd, använd schemat för den tiden och nämn det i rapporten.
- **Person och kamera:** ur [kameraregistret](../../data/media-storage.md) på kamerans serienummer (`SerialNumber`). En kamera som inte finns där: se nedan. Telefoner skriver inget serienummer; personen avgörs av vem som lämnade materialet.
- **Klockan:** jämför ett ögonblick två kameror fångat (ett tal, en gruppbild). Skiljer det mer än en minut: skriv det i inspelningens anteckningar och rapporten. Originalens tid ändras aldrig.
- **Krockar** (samma filnamn, annat innehåll, samma kamera): den krockande omgången läggs i en undermapp efter kortets mapp (`101_pana`). Filnamnen ändras aldrig.

## En ny kamera

En kamera som inte finns i registret registreras en gång (Mårten, 2026-10-24):

1. **Fråga vems kameran är** och vad den ska heta i mapparna (`lumix-s9`, `iphone-15`).
2. **Kontrollera kamerans metadata** i de nya filerna ([exiftool](../../tools/exiftool.md)):
   - fotograf och upphovsrätt (`Artist`, `Copyright`): satta, och till rätt person?
   - klockan och tidszonen: stämmer tiden i filerna med när de togs (kopieringen, schemat, en annan kamera)?
   - ägaren och serienumret (`OwnerName`, `SerialNumber`), där kameran har dem.
3. **Påminn personen** om det som saknas eller är fel, och var i kamerans meny det ställs in (Lumix S9: Inställningar → Upphovsrättsinformation; Klockinställning och Tidszon). Originalen ändras inte i efterhand; rätt fotograf och upphovsrätt skrivs in i filerna som levereras till mediebanken.
4. **Skriv in kameran** i `kameror.md`: serienummer, märke och modell, person, namn, och datumet då metadata kontrollerades.

## Gången

1. Läs av det nya (`scan` i [media-copy](../../tools/media-copy.md)) och bestäm inspelningar, personer och kameror enligt ovan.
2. Torrkör varje del (inspelning × person × kamera) och kontrollera planen: rätt antal, inga oväntade krockar.
3. **Från ett kort: kopiera, aldrig flytta.** Kortet används inte för något arbete, och det formateras inte förrän kopian syns och stämmer i Drive. Från inkorgen: flytta.
4. Kontrollera varje fil mot sha256 och skriv `ingest.csv`.
5. **Proxy** för varje videoklipp i mappen bredvid klippet ([media-worker](../../tools/media-worker.md)).
6. Rapportera: inspelningar, antal per person, kamera och typ, nya kameror och deras metadata, klockskillnader, krockar, det som var en gissning.

## Rätta

Om något hamnat fel flyttas det till rätt plats, med samma tool, och flytten loggas. Säg till om filen redan används i ett Resolve-dokument, eftersom den då måste länkas om.
