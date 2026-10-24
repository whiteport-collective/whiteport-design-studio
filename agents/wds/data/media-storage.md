# Media: var bilder och video bor

**Bestämt (Mårten, 2026-10-22, strukturen ändrad 2026-10-24).** Gäller alla agenter som hanterar foto, video och ljud från ett projekt. Viska äger flödet.

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
  kameror.md                           kameraregistret: serienummer → person och kamera (se nedan)
  projects/
    <startdatum>-<projekt>/            samma namn som projects/ i repot
      <projekt>.md                     projektets själ: mål, leveranser, personerna, platserna, schemat, det bästa
      logg.md                          vem som gjorde vad med materialet, människor och agenter, nyaste först
      inkorg/                          nytt material läggs här (eller kommer från en ansluten kamera), Viska sorterar och tömmer
      <datum>-<plats>/                 en inspelning = en dag på en plats
        <datum>-<plats>.md             inspelningens anteckningar: plats, tid, ljus, vilka, kameror, klocka
        <datum>-<plats>.drp            Resolve-dokumentet för inspelningen: godtagbara foton och rimliga klipp, med stjärnor
        innehall.csv                   en rad per fil: vad den visar, personer, nyckelord, teknik, konst, betyg, bortval
        ingest.csv                     en rad per fil: när, varifrån, tagen, kamera, sha256
        <person>/                      vem som fotade: marten, camilla
          <kamera>/                    vilken kamera: lumix-s9, iphone-15
            P1000708.MP4               originalen, foto och video blandat, kamerans egna namn
            P1000708.RW2, P1000708.JPG
            P1000708/                  allt som görs av en fil, bara när något görs (se nedan)
      mediabank/                       färdiga filer för kundens mediebank
        <datum>-<plats>/               alla kameror och fotografer tillsammans
        mediabank.csv                  en rad per fil: titel, beskrivning, nyckelord, fotograf, inspelning, original
      export/<kanal>/                  versioner för en viss kanal (webb, tryck, videoheader), gjorda av mediebankens filer
```

- **Projektmappen** finns i Drive bara när projektet har media. Namnet är exakt projektets mapp i repot, med startdatum först ([repo-structure](repo-structure.md#projektens-namn)). Inspelningarna ligger direkt i projektmappen; `inkorg/` och `mediabank/` sist.
- **En inspelning är en dag på en plats.** Fotar man två platser samma dag blir det två inspelningsmappar, uppdelade efter filernas tidsstämplar och projektets schema.
- **Person och kamera, alltid två nivåer** (Mårten, 2026-10-24): `<person>/<kamera>/`, också när någon bara har en kamera. Det håller isär filnamn som annars krockar (Lumix numrerar `P1000001` och framåt och kan börja om) och fungerar när en person har flera kameror. Vem och vilken kamera avgörs av kameraregistret.
- **Ingen `original/`-mapp** (Mårten, 2026-10-24): allt som ligger direkt i kameramappen är original, som det kom ur kameran. Inget redigeras eller döps om där.
- **En mapp bredvid en fil, med samma namn, när något görs av den** (Mårten, 2026-10-24). `P1000708/` bredvid `P1000708.MP4` (och bredvid `P1000708.RW2`/`.JPG`, som delar namn). Ett foto som bara bedömts får ingen mapp; ett videoklipp som skrivits ut får det. I mappen:

  | Fil | Vad |
  |---|---|
  | `P1000708.md` | beskrivningen: vad klippet visar, scener med tider, personer, citat, bedömning, förslag |
  | `P1000708.srt`, `P1000708.words.json` | utskriften med tider, och tid per ord |
  | `P1000708.proxy.mov` | lätt kopia för redigeringen (1080, H.264) |
  | `P1000708.cube` | utjämningen av färgen (ljuszoner: `P1000708.ljus-N.cube`) |
  | `P1000708-tvattad.mp4`, `.srt`, `.csv` | tvättad version av tal och intervjuer, med tidkodskarta åt båda hållen |
  | `P1000708.drp` | klippets Resolve-dokument: en vågrät tidslinje per utvalt ögonblick och en stående 9:16 med den vågräta inbäddad |

- **Kameraregistret** (`<delad enhet>/kameror.md`): en rad per kamera med serienummer (`SerialNumber` i metadata), märke och modell, person, kamerans namn i mapparna, och när metadata senast kontrollerades. En ny kamera registreras en gång; Viska frågar vem den tillhör och kontrollerar att kamerans metadata är rätt ([media-ingest](../skills/media-ingest/SKILL.md#en-ny-kamera)). Telefoner skriver inget serienummer; de skiljs åt på modell och person.
- Alla namn med små bokstäver och bindestreck, utan mellanslag och å, ä, ö. De ska fungera i skript, i Resolve och på alla datorer.

## Kunskapen om materialet

**Bestämt (Mårten, 2026-10-22).** Varje projekt och varje inspelning bär sin egen kunskap, som vanlig text bredvid mediet. Huvudfilen i en mapp heter som mappen (`<mapp>.md`), aldrig `README.md`: ett repo har bara en README (Mårten, 2026-10-22). Den följer med när mappen delas eller arkiveras, och den gör materialet sökbart långt efteråt ("gruppbilden där alla skrattar", "klippet där chefen säger certifiering"). Formen följer praxis i foto- och filmvärlden, och det WDS lärt sig om själ och logg. Viska skriver den med [media-catalog](../skills/media-catalog/SKILL.md) direkt efter importen.

| Fil | Praxis den bygger på | Innehåll |
|---|---|---|
| `<projekt>.md` i projektet | WDS soul, produktionens anteckningar | Uppdraget i några rader, personerna som syns (namn, roll, hur man känner igen dem), inspelningarna med en rad var, favoriterna, länk till projektet i repot. Det Viska lär sig om projektet skrivs in här direkt. |
| `logg.md` i projektet | WDS designlogg, DIT-loggen | En rad per händelse, nyaste först: datum, vem (person eller agent), vad (import, katalog, redigering, export, flytt). Överlämningarna, var arbetet står och vad som är nästa steg, ligger i repots `sessions/` som vanligt; loggen pekar dit. |
| `<datum>-<plats>.md` i inspelningen | Fotografens anteckningar, kamerarapporten | Plats, tid, vad som hände, ljuset, vilka som var med, källorna och deras inställningar, klockskillnad mellan kameror, det som saknas. |
| `innehall.csv` | Loggning i film, IPTC-fälten i foto, urval med flaggor | En rad per fil: `fil, tagen, beskrivning, nyckelord, teknik, teknik_kommentar, konst, konst_kommentar, betyg, favorit, forslag, varfor`. Beskrivning och nyckelord på projektets språk. Betyg 1–5 som i Resolve och Lightroom. `forslag: bort` med `varfor` är listan över bortvalda filer; ingen fil raderas. |
| `<klipp>/<klipp>.md` och `.srt` | Loggning i film, undertexter som sidofil | Beskrivningen med scener och tider, och det som sägs med tider (SubRip) och tid per ord (`.words.json`), i mappen med samma namn bredvid klippet, så att allt följer med klippet (Mårten, 2026-10-24). Resolve läser `.srt` som undertextspår. Originalet rörs inte. |

- **Originalen rörs fortfarande inte.** Kunskapen ligger i egna filer, aldrig inskriven i originalen. På exporter skrivs beskrivning, nyckelord och upphov in i filen ([exiftool](../tools/exiftool.md)), så att de följer med ut.
- **Personer:** namn bara på dem som är med i projektet eller har gett sitt samtycke. Andra beskrivs ("en lärare vid fönsterbordet"). Följ projektets policy i `governance/`.
- **Sökbart:** allt är text i Drive, så Drives sökning hittar det, och agenterna söker med vanliga verktyg i `G:\`.

## Arbeta och dela

- **Bearbetningen görs lokalt, Drive är transporten** (Mårten, 2026-10-22). Nytt material läses från kortet eller en lokal inkorg (arbetsmappen på datorn; på Surface Pro 7 `E:\DaVinci Resolve Cacherbete\<projekt>\`), och all analys, utskrift och tvätt skrivs först dit. När arbetet är klart flyttas resultatet in i projektmappen på den delade enheten i en omgång, kontrollerat. Då spelar det ingen roll om Drive strömmar eller har filerna offline, och inget laddas upp och ner medan agenten arbetar. Sökvägen under projektmappen i Drive är fortfarande den som aldrig ändras.
- **Proxyfiler görs vid mottagningen** (Mårten, 2026-10-22): varje videoklipp får en lätt kopia, `<klipp>/<klipp>.proxy.mov`, i mappen bredvid klippet, så att det syns vad som hör ihop och vad varje fil är. 1080 i höjd med bevarat bildformat, H.264. `import_project.py` kopplar proxyn till klippet i Resolve. Klippning och uppspelning går mot proxyn, färgsättning och export mot originalet. Det gör att materialet går att redigera även på en dator utan grafikkort.
- **Redigera:** Google Drive för datorn (`G:\Shared drives\…` i Windows). Markera projektmappen *tillgänglig offline* (högerklick → Offlineåtkomst, kan inte göras av en agent) på datorn där den redigeras, så att video inte strömmas. När projektet är klart tas den bort lokalt men ligger kvar i Drive.
- **Redigeringsprogrammet pekar på filerna där de ligger**, det kopierar dem inte. I DaVinci Resolve blir källmapparna bins och album, och färgsättning, betyg och urval görs där.
- **Dela ett Resolve-projekt:** varje Resolve-dokument sparas också som `.drp` bredvid materialet: inspelningens i inspelningsmappen, klippets i klippets mapp (Mårten, 2026-10-24). Var och en sätter **Path Mapping** i projektinställningarna till sin egen sökväg till den delade enhetens rot, och Resolve översätter länkarna. Villkoret är att allt projektet använder ligger under projektmappen i Drive; en fil från skrivbordet blir offline hos de andra.

## Arkivera

När Drive behöver rensas kopieras projektmappen till en arkivdisk med samma struktur, kontrolleras mot checksummor och tas sedan bort från Drive. Roten är det enda som byts. En annan process än redigeringen, och den görs bara på personens ja.

## Öppet

- Studiebesöket 2026-10-21 (Visita) ligger i den förra strukturen (`original/<person>-<kamera>/`, `resolve/`, `export/`). Det flyttas till den nya bara på Mårtens ja, eftersom Resolve-projekten då måste länkas om.

- Path Mapping med Google Drive för datorn är inte provat än. Prova med två personer innan ett projekt hänger på det.
- Arkiveringen saknar ännu en skill och ett tool.
