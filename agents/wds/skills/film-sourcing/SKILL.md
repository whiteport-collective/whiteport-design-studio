---
name: film-sourcing
description: Hämtar det som behovslistan säger saknas, i ordningen eget arkiv, arkivbilder med licens, AI-genererat, och loggar källa och rättighet för varje klipp. Väljer B-roll som visar det som sägs, håller belägg verkliga, följer licensvillkor, lagen om namn och bild i reklam och AI-förordningens märkning, och matchar allt mot det egna materialet. Använd när ett godkänt manus har slag som ska licensieras eller genereras, när en film behöver B-roll eller musik, eller när någon frågar om ett klipp får användas.
used_by: [viska]
version: 1.0
tools: [wds/resolve, wds/ffmpeg, wds/exiftool]
---

# B-roll, arkivbilder och AI-klipp

B-rollen visar det som sägs. Den hämtas ur manuset, inte ur biblioteket: varje slag i `film.yaml` säger vad bilden ska visa och varför ([film-production](../film-production/SKILL.md)). Källorna och villkoren står i [b-roll-och-rattigheter](../../viska/research/b-roll-och-rattigheter.md) och [ai-video](../../viska/research/ai-video.md); de är färskvara, så kontrollera dem innan pengar läggs.

**Klart betyder:** varje slag med källa `licensiera` eller `generera` har ett godkänt klipp under projektets `kallor/` på den delade enheten, en rad i filmens `rattigheter.csv` och, för AI-klipp, ett ursprungskort. Inget har köpts utan personens ja.

## Ordningen

1. **Eget arkiv.** Kundens alla projekt på den delade enheten: `innehall.csv` (beskrivning, nyckelord, betyg), utskrifterna och klippens `.md`. Det egna är alltid bäst, eftersom det visar kundens riktiga människor och platser. Kontrollera samtycket: den som filmades för ett internt evenemang är inte därmed med på en annons.
2. **Arkivbilder med licens** för allmän miljö och stämning.
3. **AI-genererat** för det stiliserade och abstrakta, när varken arkiv eller arkivbilder räcker.

**Belägg är alltid verkliga.** Ett slag med rollen `belägg` (en kund som berättar, en siffra, produkten i bruk) får aldrig vara arkivbild eller AI.

## B-roll som ser vald ut

- **Visa det specifika**, inte tapeten: kundens händer, rum och produkt. Handslag, glödlampor, schackbräden och mynttorn är klichéer som inte säger något.
- **En följd, inte tre lösa klipp:** när ett slag behöver flera bilder, ta vid, nära och människan ur samma inspelning eller samma fotograf, så att ljus och optik hänger ihop.
- **Börja på ordet** som motiverar bilden, och låt den stå två till fem sekunder (snabbare i 9:16).
- **Nära eller långt ifrån:** en arkivbild ska antingen se ut som samma plats och samma dag som det egna materialet, eller tydligt vara något annat. Det som nästan stämmer ser ut som ett misstag.
- Svenska detaljer: årstid, kläder, bilar, skyltar, eluttag och pengar ska stämma. Inga synliga varumärken.

## Arkivbilder

| Nivå | Bolag | För |
|---|---|---|
| Säkrast | Getty/iStock, Adobe Stock, Pond5 | Evig licens per klipp, ansvarsförsäkring, samtycke för igenkännbara personer. Annonser, tv, allt med människor. |
| Bra om abonnemanget sköts | Storyblocks Business, Artlist, Envato Elements | Täcker det som publiceras under abonnemanget. En ny version efter uppsägning kräver ny licens, och licensen ligger hos Whiteport, inte kunden. |
| Med försiktighet | Pexels, Pixabay, Mixkit (bara Free License), Coverr, Videvo | Allmänna miljöer utan igenkännbara personer. Inga garantier om samtycke. Aldrig Mixkit "Restricted" eller Videvo "Editorial". |

- **Aldrig "editorial only"** i en kommersiell film.
- **Igenkännbara personer i marknadsföring kräver samtycke** (lag 1978:800 om namn och bild i reklam). Gratisarkiv utan modellsamtycke håller inte där.
- **Ladda bara ner det som valts**, efter personens ja till listan. Inga massnedladdningar (Pixabay förbjuder det), och ladda aldrig upp arkivbilder till en AI-tjänst i molnet; flera bolag förbjuder det.
- Föredra 25 eller 50 bilder per sekund och platta (log) källor.

## Musik och ljudeffekter

- **Standard:** Epidemic Sound Pro för webb och sociala medier: kunden får publicera på sina kanaler, och offentligt framförande ingår. Tv-reklam och bio kräver Enterprise eller en låtlicens (Musicbed).
- **Före leverans:** lägg kundens YouTube- och Meta-kanaler i musiktjänstens lista över godkända kanaler, annars kommer Content ID-anspråk.
- Undvik YouTubes ljudbibliotek i kunduppdrag. Ljudeffekter: Epidemic eller Artlist, eller Freesound med CC0.
- Spelas filmen på ett evenemang behöver arrangören STIM-licens för STIM-musik. Säg till kunden vilka spår som är direktlicensierade.

## AI-genererat

### Får det vara AI?

Fråga i den här ordningen, och skriv svaret på slagets ursprungskort:

1. Vad ska bilden säga? Kan eget material eller en arkivbild säga det lika bra? Då blir det det.
2. **Bär bilden sanning?** Kundcase, dokumentärt, riktig personal, kundens riktiga plats, en produktegenskap. **Då aldrig AI.**
3. Liknar den en verklig person, plats, sak eller händelse så att den kan tas för äkta? Då **ska den märkas** (AI-förordningen artikel 50, gäller sedan 2026-08-02; reklam räknas sällan som konstnärlig), och kunden godkänner den uttryckligen.

AI fungerar för etableringsbilder utan människor, abstrakta bilder för en idé, kamerarörelser som inte går att göra, stiliserade produktbilder och övergångar. Det misslyckas med ansikten och händer, text och logotyper, fysik, flera personer i rörelse och allt som måste vara sant. Generera aldrig en kunds riktiga plats ("hotellet", "Visby"); använd riktigt material eller märk tydligt.

### Gången

1. **Bild-till-video ur egna stillbilder** är bästa sättet att hålla looken: en godkänd bild från inspelningen, och prompten beskriver bara rörelsen.
2. **Prompten** byggs ur slaget, kundens ljus och färger och kamerans språk i klippen runt omkring: `[motiv och handling], [plats], [utsnitt och vinkel], [kamerarörelse och fart], [optik], [ljus och tid], [färg och stil], [textur: naturligt filmkorn, lätt rörelseoskärpa], [längd], [format]`. Inga varumärken, kändisar, konstnärsnamn eller verkliga platsnamn.
3. **Tre till sex varianter** i utkastkvalitet, den valda i full upplösning, och **ladda ner direkt** (Higgsfields api sparar filerna ungefär en vecka).
4. **Granska** bild för bild: ansikten, händer, text, fysik, flimmer. Ser den genererad ut bredvid de riktiga klippen går den inte in.
5. **Matcha** i Resolve: bildfrekvensen till tidslinjens, skala upp, mjuka den överskarpa ytan, svart- och vitpunkt och vitbalans mot huvudbilden på skopen, och samma korn som allt annat ([film-assembly](../film-assembly/SKILL.md#6-färgen)).
6. **Märk och logga** enligt kortet.

**Generatorerna** (läget 2026-10-25, kontrollera varje månad): Higgsfield är en återförsäljare av ett femtiotal modeller med eget api (betalning per sekund, en kostnadsuppskattning före varje körning); ansvarsförsäkring och löfte om att uppladdat inte används för träning finns bara i Enterprise, så **ladda aldrig upp kundens förtroliga material** på de andra nivåerna. Veo 3.1 via Googles plattform har ansvarsförsäkring och C2PA. Runway säljer också många modeller via api. Luma Ray3.2 ger HDR i EXR för färgsättning. Sora finns inte längre. Rådata från en generator har troligen ingen upphovsrätt: lova aldrig kunden ensamrätt till ett AI-klipp.

Ett ursprungskort per AI-klipp, som `kallor/ai/<klipp>.yaml` bredvid klippet:

```yaml
klipp: 2026-10-25-hamnen-gryning-02.mp4
slag: s02
syfte: etablering                 # etablering | idé | övergång | produkt
generator: higgsfield-api
modell: <exakt modell och version>
datum: 2026-10-25T14:03
prompt: "<hela prompten>"
installningar: {upplosning: 1080p, bilder_per_sekund: 24, sekunder: 6, format: "16:9"}
seed: 123456
underlag: ["<egen stillbild, godkänd>"]
varianter: 4
vald: 2
kostnad_usd: 2.40
villkor: "<tjänstens villkor med datum och paragraf>"
ansvarsforsakring: false
efterbehandling: [24->25, uppskalning, färg, korn]
verklig_person_eller_plats: ingen
markning_kravs: false
markning: ""
godkand_av_kund: "<namn, datum>"
```

## Rättighetsloggen

`rattigheter.csv` i filmens mapp i repot, **en rad per användning** av ett klipp som inte är eget. Skriv raden när klippet hämtas, inte efteråt:

`anvandning, film, version, tidslinje, tc_in, tc_ut, kalla (arkiv/ai/musik/ljud), leverantor, leverantorens_id, url, fotograf, sha256, sokvag, licens, licensens_datum, licenskopia, licenstagare (whiteport/kund), order, nedladdad, kanaler (webb/sociala/annons/tv/evenemang), giltig_till, villkor_for_ny_version, endast_redaktionellt, igenkannbara_personer, modellsamtycke, egendomssamtycke, synliga_varumarken, ai, kreditering, kanaler_godkanda_for_musik`

- **Spara en kopia av licenssidan** (pdf) och kvittot i `kallor/<leverantor>/licenser/`; villkoren ändras (Pexels och Pixabay 2026-10-20).
- Skriv `leverantor:id` och licensen i klippets kommentar i Resolve, så att det följer med klippet och syns i smarta bins.
- **Vid låsning** jämförs tidslinjens klipplista med loggen: en rättighetsrapport per leverans och en lista över musiken (titel, upphov, förlag, STIM eller direktlicens, längd). Kunden får båda, med det som inte går att föra över (Artlist-klipp i kundens egna klipp) och villkoren för nya versioner.

## Vad Viska frågar om

Allt som **kostar pengar**, varje **AI-klipp som ska märkas**, varje **igenkännbar person** utan samtycke och varje klipp där licensen är oklar. Resten väljer hon själv och redovisar i behovslistan och rättighetsloggen. Avtalsklausulerna om AI (vilka verktyg, vem märker, vad som garanteras) granskas av jurist innan de används med en kund.

## Verktyg som saknas

Sök och nedladdning via Pexels-, Pixabay- och Adobe Stock-api:erna, generering via Higgsfields eller Runways api, och utskriften av rättighetsrapporten är inte byggda än. Tills de finns söker Viska på webben, personen laddar ner det valda, och Viska skriver loggen.
