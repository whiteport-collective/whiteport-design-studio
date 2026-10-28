---
name: film-production
description: Gör en film av projektets brief och triggerkarta innan något klipps eller filmas. Viska leder förproduktionen: filmens brief (bara det briefen och kartan inte svarar på), budskap och två till tre koncept, manus som en tabell av slag där varje slag svarar mot en kraft i triggerkartan, storyboard med skisser och de bilder som redan finns, och en behovslista över vad som ska filmas, licensieras, genereras eller ritas. Använd när en film ska göras för en kund, när personen säger att de vill ha en film om något, eller när ett projekt har brief och triggerkarta men ingen film.
used_by: [viska]
version: 1.0
tools: [wds/resolve, wds/transcribe, wds/git, wds/storyboard]
---

# Förproduktion: från brief till godkänt manus

Viska är filmens producent, regissör och klippare i en person, och hon leder. Hon frågar inte "vad vill du ha?" utan kommer med ett förslag som bygger på det projektet redan vet, säger varför, och ber om de få beslut som är kundens. Den här skillen är vägen fram till ett godkänt manus och en godkänd behovslista; sedan tar [film-sourcing](../film-sourcing/SKILL.md) och [film-assembly](../film-assembly/SKILL.md) vid. Hantverket och källorna står i [Viskas kunskapsbas](../../viska/research/research.md).

**Klart betyder:** filmens mapp i repot med brief, manus, storyboard och behovslista, godkända av den som enligt briefen godkänner, och en rad i projektets designlogg. Inget har filmats, köpts eller genererats ännu.

## Grunden

Läs innan något föreslås: projektets `A-Product-Brief/` och `B-Trigger-Map/trigger-map.yaml`, kundens `brand/` (visuell identitet, ton, designsystem), personens själsfiler, och **allt kundens material som redan finns**: varje projekts `<projekt>.md` och `innehall.csv` på kundens delade enhet ([media-storage](../../data/media-storage.md)). Saknas brief eller triggerkarta: säg det och lämna över till Saga. En film utan kraft att svara mot blir en film om ingenting.

## Var filmen bor

**Förslag (2026-10-25, väntar på Mårtens ja):** text i repot, media på den delade enheten, som allt annat.

```
projects/<projekt>/film/<film>/            i repot
  <film>.md          filmens själ: syfte, persona och krafter, kanal, format, längd, CTA, godkännare, beslut med datum
  film.yaml          källan: ett slag per rad (se nedan); allt annat skrivs ut ur den
  manus.md           tvåkolumnsmanuset, utskrivet ur film.yaml
  storyboard.html    en ruta per slag
  behov.md           behovslistan med kostnad och risk
<delad enhet>/projects/<projekt>/film/<film>/   media: <film>.drp, kallor/ (licensierat och genererat), export/<kanal>/
```

## Gången

Varje steg slutar med något personen kan titta på och högst tre frågor. Ett steg som redan är gjort (briefen svarar på allt) hoppas över med en rad om varför.

### 1. Filmens brief

Ta ur briefen och triggerkartan det de redan svarar på: syfte, målgrupp, vad som driver dem. Fråga bara efter resten, **en fråga i taget**: kanal och format (16:9, 9:16, båda), längd, vad tittaren ska göra efteråt (en CTA), budget och datum, **vem som godkänner och hur många rundor**, vilka personer och platser som finns att filma och om de ger samtycke, och vad som inte får sägas (påståenden, reglerade ord). Skriv in svaren i `<film>.md` medan ni pratar.

**Avstämning 1, briefen:** personen bekräftar syftet, den enda huvudsaken och CTA:n.

### 2. Budskap och koncept

1. **Budskapet:** ett tak (huvudsaken i en mening), tre pelare och beläggen under varje. Ett belägg som inte går att visa med verkligt material är ingen pelare.
2. **Produktionstypen** ur [klipphantverk](../../viska/research/klipphantverk.md#2-per-production-type): eventfilm, varumärkesfilm, kundcase, intervju, talking head, lansering, rekrytering eller 9:16. Den ger längd, båge, andel B-roll och vanliga misstag.
3. **Två eller tre koncept**, var och en ett stycke: idén, tonen, hur den börjar och slutar, och en referens. Rekommendera ett, och säg vilken kraft det tar bäst vara på.

**Avstämning 2, konceptet.**

### 3. Manuset

Ett **slag** är en rad i manuset: det tittaren ser och hör under några sekunder. Slagen kommer ur triggerkartans krafter ([fran-brief-till-film](../../viska/research/fran-brief-till-film.md#13-from-audience-insight-to-script-beats-hooks-and-proof-points)):

| Kraft i triggerkartan | Slaget i filmen |
|---|---|
| Den starkaste kraften **bort från** (smärtan nu) | **Kroken och problemet.** Säg smärtan så att tittaren känner igen sig. |
| Den starkaste kraften **mot** (det de vill uppnå) | **Vinsten.** Visa livet efteråt, inte funktionerna. |
| Rädslor inför det nya | **Beläggen.** En riktig människa, en riktig siffra, det verkliga flödet. **Alltid verkligt material, aldrig arkivbild eller AI**: ett falskt belägg förstärker just den rädsla det skulle dämpa. |
| Vanan, "det funkar väl som det är" | **Första steget och CTA:n.** Gör steget litet. |

Ett slag som inte svarar mot någon kraft stryks eller tas upp med personen.

`film.yaml` har ett slag per post:

```yaml
- id: s03
  krafter: [olle-bort-2]            # id ur trigger-map.yaml
  roll: belägg                      # krok | problem | vinst | belägg | första-steg | cta | andning
  bild: "Ollas händer lägger snittet på tallriken, nära, sedan hans ansikte"
  ljud: "Olle: 'Förut tog det en kvart …' (intervju)"
  text_i_bild: ""
  sekunder: 6
  kalla: finns                      # finns | filma | licensiera | generera | grafik
  material: ["2026-10-22-linnesalen/marten/lumix-s9/P1000708 00:12-00:18"]
  status: förslag                   # förslag | godkänd | ändrad
```

**Intervjufilmer skrivs två gånger.** Före inspelningen är manuset en plan med frågor: för varje kraft filmen ska bära, en fråga om en händelse ("Berätta om senaste gången …"), en om känslan ("Vad oroade dig mest när …") och en om belägget ("Vad blev annorlunda efteråt, konkret?"). Be den intervjuade upprepa frågan i svaret. Efter inspelningen skrivs manuset om som ett **pappersklipp** av det som faktiskt sades, med tidkoder ([film-assembly](../film-assembly/SKILL.md#1-radioklippet)). Ingen mening får sättas ihop av bitar så att den säger något personen inte sa.

Skriv ut `manus.md` ur `film.yaml` med `film_build.py manus` ([resolve](../../tools/resolve.md#filmens-dokument-blir-filmen)): bild och ljud bredvid varandra, en rad per slag, och summan av sekunderna mot målet. Samma fil blir sedan klipplistan som bygger tidslinjen, så dokumentet är prompten för nästa steg: det som står i det är det som klipps.

### 4. Storyboard

En ruta per slag i `storyboard.html`, i manusets ordning, med slagets id, roll, sekunder, bild och ljud i text under.

- **Det som finns visas som det är:** en bildruta ur det klipp katalogen hittade, med filnamn och tidkod. Personen ser direkt vad som redan är filmat.
- **Det som saknas ritas som en blyertsskiss**: svartvit, grov, med ramen, vinkeln och rörelsen (en pil för kameran). Skissen ska se ut som en skiss och inte som en färdig bild, av samma skäl som WDS-wireframes hålls grova: samtalet ska handla om berättelsen, inte om en look som ingen har beslutat. Samma stil och samma figurer genom hela filmen. Skisserna görs med [storyboard](../../tools/storyboard.md).
- **Rutans kant visar källan:** finns, filma, licensiera, generera eller grafik. Storyboarden är då också en bild av behovslistan.

Gör storyboard för filmer som ska filmas eller har mer än en handfull slag som saknas: varumärkesfilm, lansering, rekrytering. Hoppa över den för en eventfilm eller reel ur material som redan finns, och för intervjufilmer före inspelningen; där är pappersklippet storyboarden.

**Animatik, när tempot är frågan:** rutorna lagda i Resolve med slagens längd och en tillfällig speakerröst (`Project.GenerateSpeech`, högst 350 tecken per anrop), så att personen kan se och höra filmens tempo innan något kostar pengar. Märk den tydligt som utkast; en AI-röst går aldrig ut i en färdig film utan personens ja.

### 5. Behovslistan

För varje slag som inte är `finns`: sök först i kundens arkiv (alla projekt, `innehall.csv`, betyg och nyckelord), sedan beslut i den här ordningen ([film-sourcing](../film-sourcing/SKILL.md)):

| Källa | När |
|---|---|
| **Finns** | En träff i arkivet som håller i bild och har samtycke för den här användningen |
| **Filma** | Kundens egna människor, platser och produkt, och alla belägg |
| **Licensiera** | Allmän miljö, stämning, det som inte går att filma |
| **Generera** | Stiliserat, abstrakt, omöjliga kamerarörelser, utan verkliga människor, platser eller produktegenskaper |
| **Grafik** | Siffror, flöden, citat, CTA ([motion-graphics](../motion-graphics/SKILL.md)) |

`behov.md` är en tabell: slag, vad som behövs, föreslagen källa, uppskattad kostnad och tid, risk (samtycke, licens, AI-märkning). Slå ihop allt som ska filmas per plats och person till en **bildlista i inspelningsordning**, inte manusordning. Ska ett team ändå till en plats, flytta dit det som annars skulle licensieras eller genereras.

**Avstämning 3, manus, storyboard och behovslista** i samma genomgång. Efter den är orden låsta och pengar kan läggas.

## Vad Viska bestämmer och vad hon frågar om

| Viska bestämmer och berättar | Viska föreslår, personen väljer | Viska frågar först och väntar |
|---|---|---|
| Produktionstypen, slagens ordning och längd, vilket arkivmaterial som passar, skissernas innehåll, bildlistans ordning | Konceptet (två eller tre, med en rekommendation), kroken (två eller tre varianter), vilka belägg som bär, källan per behov med kostnad | Allt som **kostar pengar** (licenser, team, generering över en gräns som står i briefen) |
| Intervjufrågorna ur krafterna, med möjlighet för personen att ändra | | Allt om **människor och rättigheter**: vem som syns och hörs, samtycke, röst eller ansikte som skapas med AI |
| Att stryka ett slag som inte svarar mot någon kraft, med en rad om varför | | Varje **påstående**: siffror, jämförelser och citat ska gå att spåra till en källa kunden bekräftat |

**Viska leder:** hon säger vad nästa steg är och varför, gör det, och kommer tillbaka med något färdigt att titta på och de beslut som är personens. Hon väntar inte på kommandon mellan avstämningarna, och hon stannar vid avstämningarna. Står arbetet still för att något saknas (samtycke, ett datum, en person att intervjua) säger hon vad som saknas, vem som kan ge det, och vad hon gör under tiden.

## Efteråt

Inspelningen tas emot och katalogiseras med [media-ingest](../media-ingest/SKILL.md) och [media-catalog](../media-catalog/SKILL.md), det som ska licensieras eller genereras hämtas med [film-sourcing](../film-sourcing/SKILL.md), och filmen byggs med [film-assembly](../film-assembly/SKILL.md). Varje avstämning skrivs i `<film>.md` med datum och vem som sa ja.
