---
name: motion-graphics
description: Lägger rörlig grafik och B-roll över filmat material så att det ser gjort ut, inte AI-genererat. Grafiken byggs som HTML och renderas med HyperFrames ur en av Viskas templates, med kundens designsystem som look och ordtiderna ur transkriptet som takt. Använd när personen vill ha ord, siffror, en avsändare eller ett slut ovanpå en reel, ett tal eller en intervju, eller ett grafiklager att lägga i Resolve.
used_by: [viska]
version: 1.0
tools: [wds/hyperframes, wds/transcribe, wds/ffmpeg, wds/resolve]
---

# Rörlig grafik

Grafik på film blir AI-slop av samma skäl varje gång: allt tonar in, allt glider upp, tre saker talar samtidigt, en räknare rullar genom värden som ingen har sagt, och looken är verktygets i stället för kundens. Den här skillen är hantverket som håller emot det. Det bakas in i **templates**, inte presets: en template är en filmtyp med reglerna redan inbyggda, som hämtar looken ur kundens designsystem. När personen rättar något rättas templaten eller kundens `film.css`, så att rättelsen gäller i alla filmer efter (Mårten, 2026-10-25).

**Klart betyder:** en renderad film (eller ett grafiklager med alfakanal till Resolve), ett kontaktark som Viska har tittat på bild för bild, filmens `film.json` sparad bredvid klippet och en rad i projektets logg om vad grafiken säger och var det kommer ifrån.

## Hantverket

1. **Grafiken landar på ordet.** Varje ruta och varje ord är på plats två bildrutor innan ordet hörs, med tiderna ur [transcribe](../../tools/transcribe.md) `--words` på den färdiga bildplattan. Whisper kan missa med en tiondels sekund; lyssna på de ord som bär grafiken.
2. **Rita, tona inte.** Linjer ritas fram, rutor dras fram och bort som med en penna, ord slås på hårt och rör sig kort på plats. Opacitet används som på/av, aldrig som en långsam toning.
3. **Lämna över i stället för att övertona.** Grafiken lämnar bilden med klippet eller strax före det, eller följer med över klippet med flit. Slutet kommer genom något som redan finns i bild: linjen blir kanten på kundens mark, som reser sig över sista klippet.
4. **Rytmen är talets.** En linje som ritas tar lika lång tid som ordet den står under. Det som ska läsas står minst en halv sekund plus 0,3 sekunder per ord; filmens sista rad minst två sekunder. Inget fryser i slutet: fotot lever till sista bildrutan.
5. **Återhållsamhet.** Ett eller två ord ur det som sägs, inte en textremsa av allt. Bilden som bevisar något (snittet, tallriken, ansiktet) får stå utan grafik.
6. **En idé per bild.** En grafik i taget. Aldrig rubrik, överrubrik och textremsa samtidigt.
7. **Inga påhittade siffror.** En siffra visas bara om den sägs i talet eller står i `film.json` under `belagt` med källa; bygget stoppar annars. Ingen räknare som rullar genom värden ingen har sagt.
8. **Kundens look, ingen egen.** Färger, typsnitt, hörn och skuggor kommer ur kundens `brand/design-system/` ([taste](../../data/taste.md): projektets design först). Mårtens smak gäller ovanpå: ingen glöd, en färgfamilj, riktiga foton bredvid texten. Lös text direkt på filmat material försvinner mot ljusa ytor; lägg den på kundens kort.

## B-roll under talet

Rösten bär, bilden visar det som sägs. Medan någon pratar om en teknik skär bilden till händerna som gör den, och rösten fortsätter under (J- och L-klipp). B-rollen väljs ur katalogen (`innehall.csv`, taggar och betyg, [media-catalog](../media-catalog/SKILL.md)), inte på måfå, och bildplattan klipps klar i Resolve eller med [ffmpeg](../../tools/ffmpeg.md) innan grafiken görs. Grafiken ändrar aldrig klippningen.

## Hörnetiketter och räknare: krocken

Två källor säger emot varandra. Motionmaxxing förbjuder allt som liknar en webbsida i bild: namn i hörnet, etiketter i spärrade versaler, räknare som "02 / 05", tidskoder. Jamie Fenns regel 4 vill ha dem, som orientering för den som tittar utan ljud och utan sammanhang. Båda har rätt för sin filmtyp, så **varje template avgör** och skriver skälet i sin `template.md`. Ingen regel här gäller över templatens beslut.

- [talat-ord](../../viska/templates/talat-ord/template.md): inga hörnetiketter och inga räknare under filmen. En reel på 15 sekunder har inga kapitel att räkna, och de första sekunderna tillhör det som sägs. Orienteringen (var, när, vem) står en gång, på slutet bredvid fotot, där den hinner läsas.
- En framtida template för en längre förklaring med kapitel kan välja tvärtom: en kapitelrad i kanten, som räknar något verkligt.

## Gången

1. **Bildplattan** färdigklippt, med ljud. Transkribera den med ordtider.
2. **`film.json`** bredvid klippet: template, kundens designsystem, plattan, ordtiderna, klippen, vilka ord som lyfts och slutet. Har kunden inget `film.css`, översätt designsystemet till bild först (rollerna står i templaten) och lägg det i kundens `brand/design-system/`.
3. **Bygg, kontrollera och titta** med [hyperframes](../../tools/hyperframes.md): kontrollen, stillbilder på varje grafiks början och slut, och kontaktarket. Beskriv varje bild i en mening innan du bedömer den.
4. **Rendera** MP4 för leverans, eller grafiklagret med alfakanal när personen klipper vidare i Resolve.
5. **Rättelser** skrivs in i templaten eller kundens `film.css`, med namn och datum, och filmen byggs om.

## Templates

| Template | Vad |
|---|---|
| [talat-ord](../../viska/templates/talat-ord/template.md) | Ord ur talet på kundens kort över en reel, en linje som ritas i talets takt, och ett slut med ett riktigt foto bredvid avsändaren |

## Källor

Prövat 2026-10-25 med samma brief i tre varianter: utan skill, med motionmaxxing och med den här skillens template. Jämförelsen står i [talat-ord](../../viska/templates/talat-ord/template.md#provet). Reglerna är skrivna med egna ord. [HyperFrames](https://github.com/heygen-com/hyperframes) (Apache 2.0) är renderaren. [motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) (Apache 2.0) gav landa-och-lämna-grammatiken och kurvorna. [video-editor-skills](https://github.com/appariciojunior/video-editor-skills) (CC BY-NC 4.0) lästes bara som inspiration; inget är kopierat därifrån. [davinci-resolve-claude-skills](https://github.com/ChaiWithJai/davinci-resolve-claude-skills) (MIT) lästes för Resolve-delen.
