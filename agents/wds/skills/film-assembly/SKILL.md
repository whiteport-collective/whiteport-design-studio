---
name: film-assembly
description: Bygger filmen i DaVinci Resolve Studio ur det godkända manuset: radioklippet av det som sägs, B-roll som täcker och visar, musiken kartlagd och klippt till sitt slut, övergångar bara där de betyder något, dramatik med kontrast och tystnad, grafik i kundens profil, en färg och ett korn över allt material, och ljudet nivåsatt. Kontrollerar tidslinjen mot hantverksreglerna innan personen ser den, och leder versionerna genom grovklipp, finklipp och låsning. Använd när manus och material finns och filmen ska klippas, eller när en version ska göras om efter feedback.
used_by: [viska]
version: 1.0
tools: [wds/resolve, wds/transcribe, wds/ffmpeg, wds/hyperframes]
---

# Bygga filmen i Resolve

Underlaget är filmens godkända `film.yaml` och `manus.md` ([film-production](../film-production/SKILL.md)), materialet i kundens arkiv och det [film-sourcing](../film-sourcing/SKILL.md) har hämtat. Hantverket är [klipphantverk](../../viska/research/klipphantverk.md), med källor; här står reglerna Viska klipper efter. Hur Resolve styrs står i [resolve](../../tools/resolve.md).

**Klart betyder:** filmens Resolve-dokument `<film>.drp` med tidslinjen för versionen (`<film>-grov-1`, `<film>-fin-2`, `<film>-last`), kontrollen körd och godkänd, en rad i projektets logg, och personen har fått versionen med högst tre öppna frågor.

## Prioritetsordningen

Varje klipp väljs efter Walter Murchs ordning: **känsla** först, sedan berättelse, rytm, blickens väg, bildens riktning och rummet. Kan ett klipp inte uppfylla allt, ge upp underifrån. Ett klipp på takten är aldrig skäl nog om en annan ruta bär känslan bättre. Klipp strax före en blinkning, aldrig mitt i.

## Gången

### 1. Radioklippet

Berättelsen byggs först **med ljud enbart**: det som sägs, i manusets ordning, tills det fungerar som radio. Bild, musik, färg och grafik kommer efter.

1. Utskrift med ordtider: [transcribe](../../tools/transcribe.md) `--words` (KB-Whisper, bäst på svenska), eller Resolves `TranscribeAudio` och `GetTranscription` när de är provade.
2. **Pappersklippet:** citaten valda mot manusets slag och krafter, med klipp och tidkoder, i `film.yaml`. Ta fler än som behövs.
3. Lägg dem på A1 med `AppendToTimeline` (in- och utpunkt per citat), marginal kvar i andningen. Tvätta "eh" och felstarter som i [video-edit](../video-edit/SKILL.md#den-tvättade-versionen).
4. **Ingen mening sätts ihop av bitar** så att den säger något personen inte sa. Varje omkastning skrivs upp för godkännande.

### 2. Bilden

- **V1:** det personen säger i bild, där ansiktet bär något (början, känslan, belägget).
- **V2:** B-roll över allt annat. Varje skarv i talet täcks av B-roll, en inzoomning på minst 20 % eller Smooth Cut (högst fyra rutor). Ett hopp i en varumärkesfilm eller ett kundcase syns aldrig; i en talking head för sociala medier är hoppet en del av genren.
- B-roll börjar på ordet som motiverar den, står två till fem sekunder, och kommer som följder (vid, nära, människan) ur samma inspelning.
- **Kontrast driver:** högt och tyst, snabbt och långsamt, vid och nära. Korta bilderna mot höjdpunkten, låt den sedan stå. Visa aldrig höjdpunkten i början.

### 3. Övergångarna

**Rakt klipp är grunden.** Allt annat måste ha ett skäl i det som syns eller hörs.

| Grepp | När | Inte |
|---|---|---|
| J-klipp (ljudet före bilden) och L-klipp (ljudet efter) | Vid **varje** byte av plats eller scen, 6–24 rutor | När det blir oklart vem som talar |
| Matchklipp (form, rörelse, ljud) | Mellan platser, tider eller idéer | Mer än ett per minut |
| Klipp i rörelse | Mitt i rörelsen, samma fart och riktning | Slentrianmässigt |
| Kontrastklipp (smash) | Tyst eller lugnt, sedan högt på ett musikslag | Två gånger i samma film |
| Övertoning | Tid som går, ett inre tillstånd, något som ska lugna | Som standard mellan klipp |
| Tona till svart eller vitt | Ett kapitel slutar | Mellan scener nära i tid och rum |
| Fartramp, piska, maskad övergång | Bara med material filmat för det (50 eller 100 bilder per sekund, piskan i kameran, något som faktiskt passerar bilden) | Digital piska mellan stillastående bilder, ljusläckor ur arkiv, 3D-, snurr- och sidvändningseffekter |

En familj av grepp per film, högst två stiliserade övergångar per minut. Övergångar sätts med `TimelineItem.AddTransition` (Resolve 21.1, inte provat än) eller i FCPXML; fartkurvor och nyckelpunkter med FCPXML eller Fusion ([resolve](../../tools/resolve.md)).

### 4. Musiken och dramatiken

1. **Kartlägg låten** först med markörer: intro, uppbyggnad, topp, nedtrappning, slut. Lägg filmens akter på delarna: början på intro, stegringen på uppbyggnaden, höjdpunkten på toppen, CTA:n på slutet.
2. **Tre till fem hårda synkar per minut** (toppen, accenter). Övriga klipp faller på känsla och rörelse, gärna i frasernas glapp, två till sex rutor före eller efter slaget. Mer än halva klippen på takten blir musikvideo.
3. **Klipp musiken** på taktstrecken så att den slutar på sista rutan. Tona aldrig ut den.
4. **Tystnad:** en till tre sekunder utan musik strax före eller under den viktigaste repliken. Rumstonen fortsätter; digital tystnad låter som ett fel. I 9:16 högst en och en halv sekund.
5. Ljudeffekter bara där något rör sig eller filmen byter del. Svischen varieras, en stegring per akt och den slutar exakt på slaget. I företagsfilm hellre verkliga ljud (en dörr, ett papper, platsen) än trailereffekter.

### 5. Grafiken

Titlar, namnskyltar, siffror och slutskylt i kundens profil, med [motion-graphics](../motion-graphics/SKILL.md) och dess templates. Grafiken landar på ordet och visar idén, den upprepar inte orden. Namnskylt en gång per person, fullt namn och roll, stavat mot listan i briefen, lika länge som det tar att läsa den två gånger (minst 2,5 sekunder). All text inom de säkra ytorna: 5 % in från kanten i 16:9; i 9:16 inom x 120–888, y 288–1248 (1080x1920), undertexter runt y 1000–1248.

### 6. Färgen

Ett utseende för hela filmen, så att eget material, arkivbilder och AI-klipp ser ut som en film:

1. **Ingångsfärgrymd per klipp** (kamerans log för vårt material, Rec.709 för de flesta arkivbilder), inte en extra omvandling ovanpå.
2. **Rätta före du färgsätter:** exponering och vitbalans mot en huvudbild på skopen, klippets ljuszoner som i [video-edit](../video-edit/SKILL.md) och [looks](../../tools/resolve.md#färgsättning-med-lut-per-klipp).
3. **Ett kreativt utseende** och **ett korn över allt**, på tidslinjenivå. Det gemensamma kornet är det starkaste greppet för blandat material.
4. **Bildfrekvens:** tidslinjen i 25 bilder per sekund för svenska kunder; allt konverteras vid import.

### 7. Ljudet

Rumston under varje skarv i talet. Högst fem samtidiga lager (tal, musik, miljö, en eller två effekter). Musiken duckar under tal och lyfter i montage. Dialogen nivåsätts till ungefär −14 LUFS för webb och sociala medier (`NormalizeAudioLevel` i 21.1, inte provat än). Stockklippens eget ljud byts mot egen rumston eller musik.

### 8. Kontrollen

Innan personen ser en version kör Viska tidslinjen mot reglerna ([klipphantverk, avsnitt 7](../../viska/research/klipphantverk.md#7-machine-checkable-rules-for-viska-proposal-inference-unless-cited)), och rättar eller redovisar det som fastnar:

1. Högst två övergångar som inte är raka klipp per minut, en familj av grepp.
2. Bildlängden varierar (variationskoefficient över 0,3), höjdpunkten är snabbare än början, och slutet får stå.
3. Högst halva klippen på takten, utom i toppen av en eventfilm eller reel.
4. Varje skarv i talet är täckt, inget klipp mitt i en blinkning, rumstonen hel.
5. Minst hälften av bytena av plats eller scen är J- eller L-klipp.
6. Ljudnivån, ducking, musiken slutar med bilden, högst fem lager.
7. All text inom säkra ytor, namnskyltar länge nog och rättstavade, varje person namngiven en gång.
8. Första rutan är inte en logotyp; kroken syns inom tre sekunder i 9:16 och sex i 16:9, och första rutan säger något utan ljud.
9. En bildfrekvens, ett utseende, ett korn, AI-klipp märkta och granskade mot listan över AI-tecken.
10. Inga hopsatta citat; omkastningar på listan för godkännande.

Titta sedan på kontaktark ur varje slag och beskriv varje bild i en mening innan du bedömer den. Det som ser ut som AI-slop ([klipphantverk, avsnitt 6](../../viska/research/klipphantverk.md#6-ai-slop--amateur-checklist-with-fixes)) går inte ut.

## Versionerna och avstämningarna

| Version | Personen tar ställning till | Inte |
|---|---|---|
| **Grovklipp** (`-grov-N`) | Berättelsen, ordningen, tempot: håller den mot briefen? Behövs något filmas om, sägs det nu. | Färg, grafik, ljudmix |
| **Finklipp** (`-fin-N`) | Grafik och namn, musiken, färgens riktning, mixen, påståenden och juridik | Ny berättelse |
| **Låst** (`-last`) | Att ändringarna är gjorda, och vem som ger slutligt ja | Nya önskemål; de är en ny beställning |

- **Feedback samlas till en lista** innan något görs om. Personen sätter gärna markörer med text i Resolve; Viska läser dem med api:t, visar listan som en plan och gör sedan nästa version. Varje rättelse som gäller fler filmer skrivs in i templaten eller kundens profil.
- Förra versionen ligger kvar som egen tidslinje.
- **Vid låsning:** rättighetsrapporten och musiklistan ([film-sourcing](../film-sourcing/SKILL.md#rättighetsloggen)), exporterna per kanal ([media-export](../media-export/SKILL.md)), och projektet exporterat som `.drp`.

Viska klipper själv allt inom det godkända manuset (bildval, längder, B-roll, övergångar ur filmens familj, färgbalans, ljudnivå, radbrytningar) och redovisar det. Hon frågar om det som ändrar vad filmen säger, kostar pengar, rör människors medverkan eller kommer efter låsning.
