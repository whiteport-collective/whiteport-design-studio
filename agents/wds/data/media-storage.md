# Media: var bilder och video bor

**Bestämt (Mårten, 2026-10-22).** Gäller alla agenter som hanterar foto, video och ljud från ett projekt. Viska äger flödet.

## Principen

**En mediafil flyttar inte när den väl är sparad.** Den byter varken mapp eller namn, så att varje projekt som länkar till den hittar den, hos alla, så länge den finns. Allt annat i det här dokumentet följer av det.

- Det som inte ändras är **sökvägen under mediaroten**. Roten får bytas: från den delade enheten i Google Drive till en arkivdisk när Drive rensas. Strukturen under roten följer med oförändrad.
- Därför bestäms mapp och namn **när materialet kommer in**. Personen lägger allt i projektets `inkorg/`, och Viska sorterar det själv ([media-ingest](../skills/media-ingest/SKILL.md)). Att sortera bilder efter innehåll gör man i redigeringsprogrammet, aldrig i mapparna.
- **En fil som hamnat fel flyttas till rätt plats** (Mårten, 2026-10-22). Helst innan redigeringen börjar, eftersom en fil som ett projekt redan använder blir offline och måste länkas om. Varje flytt loggas.
- **Original rörs aldrig.** Redigeringar och exporter är nya filer i egna mappar.
- Media hör aldrig hemma i git. Repot har utskrifter, manus och beslut; mediet ligger i Drive.

## Var

Kundens **delade enhet** i Google Drive, en per kund (till exempel *Visita Kommunikation*). På en delad enhet ägs filerna av enheten, inte av en person: de finns kvar för kunden om någon slutar, och hela projektet kan delas med ett klick. Personliga inspelningar (möten, samtal) ligger i stället i personens privata mediamapp, se [recording](../skills/recording/SKILL.md).

```
<delad enhet>/
  projects/
    <startdatum>-<projekt>/            samma namn som projects/ i repot
      <datum>-<plats>/                 en inspelning = en dag på en plats
        ingest.csv                     en rad per fil: när, varifrån, tagen, kamera, sha256
        original/
          <person>-<kamera>/           en mapp per källa: marten-lumix-s9, johanna-iphone
        export/
          <kanal>/                     webb, sociala-medier, tryck, videoheader …
      inkorg/                          personen lägger allt här, Viska sorterar och tömmer
      resolve/                         projektfiler (.drp) som andra öppnar
```

- **Projektmappen** finns i Drive bara när projektet har media. Namnet är exakt projektets mapp i repot, med startdatum först ([repo-structure](repo-structure.md#projektens-namn)). Allt på den delade enheten är media, så inspelningarna ligger direkt i projektmappen, utan en mellannivå `media/` (Mårten, 2026-10-22). Datummapparna listas först, `inkorg/` och `resolve/` sist.
- **En inspelning är en dag på en plats.** Fotar man två platser samma dag blir det två inspelningsmappar, uppdelade efter filernas tidsstämplar.
- **En undermapp per källa** i `original/`. Varje kamera och varje person som lämnar material får sin egen. Det håller isär filnamn som annars krockar (Lumix numrerar `P1000001` och framåt och kan börja om).
- **I `original/` ligger allt som det kom ur kameran:** foto och video blandat, kamerans egna filnamn. Inget redigeras eller döps om här.
- Alla namn med små bokstäver och bindestreck, utan mellanslag och å, ä, ö. De ska fungera i skript, i Resolve och på alla datorer.

## Arbeta och dela

- **Lokalt:** Google Drive för datorn (`G:\Shared drives\…` i Windows). Markera projektmappen *tillgänglig offline* medan den redigeras, så att video inte strömmas. När projektet är klart tas den bort lokalt men ligger kvar i Drive.
- **Redigeringsprogrammet pekar på filerna där de ligger**, det kopierar dem inte. I DaVinci Resolve blir källmapparna bins och album, och färgsättning, betyg och urval görs där.
- **Dela ett Resolve-projekt:** exportera projektet som `.drp` till `resolve/` (eller använd ett gemensamt projektbibliotek i Blackmagic Cloud). Var och en sätter **Path Mapping** i projektinställningarna till sin egen sökväg till den delade enhetens rot, och Resolve översätter länkarna. Villkoret är att allt projektet använder ligger under projektmappen i Drive; en fil från skrivbordet blir offline hos de andra.

## Arkivera

När Drive behöver rensas kopieras projektmappen till en arkivdisk med samma struktur, kontrolleras mot checksummor och tas sedan bort från Drive. Roten är det enda som byts. En annan process än redigeringen, och den görs bara på personens ja.

## Öppet

- Path Mapping med Google Drive för datorn är inte provat än. Prova med två personer innan ett projekt hänger på det.
- Arkiveringen saknar ännu en skill och ett tool.
