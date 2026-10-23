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
      <projekt>.md                     projektets själ (samma namn som mappen): vad, för vem, varför, personerna, inspelningarna, det bästa
      logg.md                          vem som gjorde vad med materialet, människor och agenter, nyaste först
      <datum>-<plats>/                 en inspelning = en dag på en plats
        <datum>-<plats>.md             inspelningens anteckningar: plats, tid, ljus, vilka, kamerainställningar, klocka
        innehall.csv                   en rad per fil: vad den visar, personer, nyckelord, betyg, favorit
        ingest.csv                     en rad per fil: när, varifrån, tagen, kamera, sha256
        original/
          <person>-<kamera>/           en mapp per källa: marten-lumix-s9, johanna-iphone
            <klipp>.srt, .words.json   utskriften bredvid varje videoklipp, samma grundnamn
            Proxy/<klipp>.mov          lätt kopia för redigeringen (1080, H.264); Resolve hittar den själv
        klipp/                         tvättade versioner av tal och intervjuer: <klipp>-tvattad.mp4 + .srt + .csv + .xml
        export/
          <kanal>/                     webb, sociala-medier, tryck, videoheader …
      inkorg/                          allt nytt läggs här, Viska sorterar och tömmer
        <person>/                      när flera lämnar material: en mapp var
      resolve/                         projektfiler (.drp) som andra öppnar
```

- **Projektmappen** finns i Drive bara när projektet har media. Namnet är exakt projektets mapp i repot, med startdatum först ([repo-structure](repo-structure.md#projektens-namn)). Allt på den delade enheten är media, så inspelningarna ligger direkt i projektmappen, utan en mellannivå `media/` (Mårten, 2026-10-22). Datummapparna listas först, `inkorg/` och `resolve/` sist.
- **En inspelning är en dag på en plats.** Fotar man två platser samma dag blir det två inspelningsmappar, uppdelade efter filernas tidsstämplar.
- **En undermapp per källa** i `original/`. Varje kamera och varje person som lämnar material får sin egen. Det håller isär filnamn som annars krockar (Lumix numrerar `P1000001` och framåt och kan börja om).
- **Fotografen i kameran:** ställ in upphovsrätt eller fotograf i kamerans meny (`Artist`, `Copyright`), så bär varje fil sin fotograf. Telefoner gör inte det, därför en inkorgsmapp per person.
- **I `original/` ligger allt som det kom ur kameran:** foto och video blandat, kamerans egna filnamn. Inget redigeras eller döps om här.
- Alla namn med små bokstäver och bindestreck, utan mellanslag och å, ä, ö. De ska fungera i skript, i Resolve och på alla datorer.

## Kunskapen om materialet

**Bestämt (Mårten, 2026-10-22).** Varje projekt och varje inspelning bär sin egen kunskap, som vanlig text bredvid mediet. Huvudfilen i en mapp heter som mappen (`<mapp>.md`), aldrig `README.md`: ett repo har bara en README (Mårten, 2026-10-22). Den följer med när mappen delas eller arkiveras, och den gör materialet sökbart långt efteråt ("gruppbilden där alla skrattar", "klippet där chefen säger certifiering"). Formen följer praxis i foto- och filmvärlden, och det WDS lärt sig om själ och logg. Viska skriver den med [media-catalog](../skills/media-catalog/SKILL.md) direkt efter importen.

| Fil | Praxis den bygger på | Innehåll |
|---|---|---|
| `<projekt>.md` i projektet | WDS soul, produktionens anteckningar | Uppdraget i några rader, personerna som syns (namn, roll, hur man känner igen dem), inspelningarna med en rad var, favoriterna, länk till projektet i repot. Det Viska lär sig om projektet skrivs in här direkt. |
| `logg.md` i projektet | WDS designlogg, DIT-loggen | En rad per händelse, nyaste först: datum, vem (person eller agent), vad (import, katalog, redigering, export, flytt). Överlämningarna, var arbetet står och vad som är nästa steg, ligger i repots `sessions/` som vanligt; loggen pekar dit. |
| `<datum>-<plats>.md` i inspelningen | Fotografens anteckningar, kamerarapporten | Plats, tid, vad som hände, ljuset, vilka som var med, källorna och deras inställningar, klockskillnad mellan kameror, det som saknas. |
| `innehall.csv` | Loggning i film, IPTC-fälten i foto, urval med flaggor | En rad per fil: `fil, tagen, beskrivning, nyckelord, teknik, teknik_kommentar, konst, konst_kommentar, betyg, favorit, forslag, varfor`. Beskrivning och nyckelord på projektets språk. Betyg 1–5 som i Resolve och Lightroom. `forslag: bort` med `varfor` är listan över bortvalda filer; ingen fil raderas. |
| `<klipp>.srt` bredvid klippet | Undertexter som sidofil | Det som sägs i ett videoklipp, med tider, i SubRip, och `<klipp>.words.json` med tid per ord. Samma grundnamn och samma mapp som klippet, så att utskriften följer med när klippet kopieras eller sorteras om (Mårten, 2026-10-22). Resolve läser `.srt` som undertextspår. Originalet rörs inte; sidofilerna är egna filer. |

- **Originalen rörs fortfarande inte.** Kunskapen ligger i egna filer, aldrig inskriven i originalen. På exporter skrivs beskrivning, nyckelord och upphov in i filen ([exiftool](../tools/exiftool.md)), så att de följer med ut.
- **Personer:** namn bara på dem som är med i projektet eller har gett sitt samtycke. Andra beskrivs ("en lärare vid fönsterbordet"). Följ projektets policy i `governance/`.
- **Sökbart:** allt är text i Drive, så Drives sökning hittar det, och agenterna söker med vanliga verktyg i `G:\`.

## Arbeta och dela

- **Bearbetningen görs lokalt, Drive är transporten** (Mårten, 2026-10-22). Nytt material läses från kortet eller en lokal inkorg (`~/Pictures/wds-arbete/<projekt>/`), och all analys, utskrift och tvätt skrivs först dit. När arbetet är klart flyttas resultatet in i projektmappen på den delade enheten i en omgång, kontrollerat. Då spelar det ingen roll om Drive strömmar eller har filerna offline, och inget laddas upp och ner medan agenten arbetar. Sökvägen under projektmappen i Drive är fortfarande den som aldrig ändras.
- **Proxyfiler görs vid mottagningen** (Mårten, 2026-10-22): varje videoklipp får en lätt kopia i `Proxy/` bredvid originalen, 1080 i höjd med bevarat bildformat, H.264. Det är Blackmagics konvention, så Resolve kopplar proxyn till klippet själv på varje dator. Klippning och uppspelning går mot proxyn, färgsättning och export mot originalet. Det gör att materialet går att redigera även på en dator utan grafikkort.
- **Redigera:** Google Drive för datorn (`G:\Shared drives\…` i Windows). Markera projektmappen *tillgänglig offline* (högerklick → Offlineåtkomst, kan inte göras av en agent) på datorn där den redigeras, så att video inte strömmas. När projektet är klart tas den bort lokalt men ligger kvar i Drive.
- **Redigeringsprogrammet pekar på filerna där de ligger**, det kopierar dem inte. I DaVinci Resolve blir källmapparna bins och album, och färgsättning, betyg och urval görs där.
- **Dela ett Resolve-projekt:** exportera projektet som `.drp` till `resolve/` (eller använd ett gemensamt projektbibliotek i Blackmagic Cloud). Var och en sätter **Path Mapping** i projektinställningarna till sin egen sökväg till den delade enhetens rot, och Resolve översätter länkarna. Villkoret är att allt projektet använder ligger under projektmappen i Drive; en fil från skrivbordet blir offline hos de andra.

## Arkivera

När Drive behöver rensas kopieras projektmappen till en arkivdisk med samma struktur, kontrolleras mot checksummor och tas sedan bort från Drive. Roten är det enda som byts. En annan process än redigeringen, och den görs bara på personens ja.

## Öppet

- Path Mapping med Google Drive för datorn är inte provat än. Prova med två personer innan ett projekt hänger på det.
- Arkiveringen saknar ännu en skill och ett tool.
