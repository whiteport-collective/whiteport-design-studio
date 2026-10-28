# NextPhase AI: genomgång för Viska

Läst 2026-10-27 i Mårtens inloggade Chrome: gruppen [NextPhase AI](https://www.skool.com/nextphase-5790) (Jade M och Amine Hn, gratis, 9 200 medlemmar), klassrummets 22 lektioner, de 11 videorna om video och motion (utskrifter i `transkript/`), och de tre skillpaketen gruppen delar öppet på Google Drive (i `nedladdat/` och `uppackat/`). Inget har installerats eller körts; skillpaketens setup-promptar installerar i `~/.claude/skills` och har inte rörts.

**Licens:** paketen är "shared free by NextPhase … personal or commercial … please don't resell it or repackage it as a paid product". Vi lär oss och skriver våra egna regler och verktyg med egna ord; vi kopierar inte deras kod eller texter in i WDS, som kan säljas. Tredjepartsdelarna de pekar på (HyperFrames Apache 2.0, three.js MIT, GSAP:s gratislicens, OFL-typsnitt, Lucide ISC, whisper.cpp MIT) får vi använda direkt från källan. Robust Video Matting, som Editor V1 frilägger talaren med, är GPL-3.0: använd den bara som separat verktyg, bygg inte in den.

## Vad som finns

| Paket | Vad det är | Värt för Viska |
|---|---|---|
| **EDIT, "The full AI video editing system"** (`ai-video-editor`, 12/10) | Ett långformatsystem för talking head i 16:9 med sju roller: utskrivare, klippare, regissör, motion designer med två hjälpagenter, ljud, kvalitetskontroll, publicering. 30 Python-verktyg, ett grafikbibliotek på HyperFrames och three.js, kort som landar på orden, kapitelkort, ikoner som ritar sig själva, riktiga sidor och skärmar, 3D-logotyper, sju 3D-scener. | **Mest.** Arbetsgången, kontrollerna och reglerna är professionella och passar Viskas talk- och intervjufilmer. |
| **Editor V1 / ZERO** (26/10) | Ett snabbt dokumentärklipp (bilden byter var 0,6–1,5 s) där varje rad får riktigt material ur nätet, färgat och animerat med namngivna grepp uppmätta ruta för ruta ur tre förebilder. | **Metoden** för att mäta en förebild och göra den till en namngiven stil. Själva looken (teal och orange, röda jätteord, klick på varje byte) är fel för de flesta av våra kunder. |
| **Katana Director** (11/10) | En regissörsskill framför Higgsfields Katana: intervju, tre budgetvägar, plan med kostnad per rad, ett tydligt ja, sedan kör Katana själv. | **Kundsamtalet och planen.** Katana kräver Higgsfields MCP, som vi inte använder. |
| **11 videor** | Hur de byggde systemen och vad som gick fel. | Arbetssätt, misstag och några regler; mycket marknadsföring. Se `transkript-regler.md`. |

## Det bästa, i den ordning vi borde ta in det

### 1. Stilfångst: en förebild blir en namngiven template

Detta är kärnan i båda klippskillsen och det som skiljer deras resultat från AI-slop. Man väljer **två eller tre** förebilder man älskar (inte fler), och agenten mäter dem ruta för ruta:

- **Klippen:** skillnad i gråskala mot förra rutan (96x54 px) och avstånd mellan färghistogram; ett klipp där skillnaden är större än max(14, 4 × lokala medianen) eller histogramavståndet över 0,5. Ger klipp per minut, bildlängdernas median och 90-percentil, andel blixtar under 0,17 s.
- **Utseendet:** andel naturlig färg, kall, varm, svartvit, ljus och mörk grund; vinjett; var mättade pixlar ligger i nyans.
- **Typen:** textens storlek i procent av höjden, var den står, hur ord kommer in; textens start mot det talade ordet (de mätte ±1 ruta).
- **Ljudet:** tal och musik skiljs åt (demucs), sedan musikens nivå under talet, ljudhändelser per minut, hur många som landar inom två rutor från ett klipp, tempo.
- **Kontaktark** var 0,5 s över hela filmen och fulla bildrutor kring varje övergång.

Resultatet skrivs som **ett klippprotokoll per förebild** (en rad per bild: tid, längd, vad, kategori, bokstavlig eller bildlig mot vilket ord, rörelse i bilden, färg, text, övergång ruta för ruta, ljud vid klippet) och som **siffror** i stilens dokument, och stilen får ett namn ("använd editor V1"). Råmaterialet (förebildernas rutor och ljud) sparas aldrig, bara mätningarna.

**Två lärdomar ur deras eget arbete:** första versionen blev dålig tills agenten gick tillbaka till förebilderna och mätte djupare, och då hittade den sådant ingen sagt (hälften av bilderna rör sig, varje ny bild börjar oskarp och skärps på ungefär nio rutor, en bild som står i fyra sekunder är ett fel). Och siffrorna blir räcken: regler som går att kontrollera, inte smak.

**För Viska:** en ny skill (arbetsnamn `style-capture`) som gör detta mot en kunds egna förebilder och skriver en template under `viska/templates/`, och ett verktyg för mätningen (ffmpeg, numpy, demucs, våra kontaktark). Den kopplar ihop med det motion-sessionen byggde (`talat-ord`) och med `film-assembly`.

### 2. Anteckningar blir regler, samma dag

Varje kommentar på en version ("rött är för starkt", "jag syns nästan aldrig") skrivs samma dag in som regel med personens ord, datum och vad som ändrades (ett verktyg, en siffra), och gäller sedan alla filmer. En anteckning går före skillen. Kortformatsklipparen har en **svartlista på 21 regler**, varje regel ur ett klipp som underkändes (inga små texter, inga emojis, inga slumpade människor som B-roll, en markering i taget).

**För Viska:** finns som princip (templaten rättas), men saknar formen. Inför `anteckningar.md` per template och per kund: datum, citatet, regeln, vad som ändrades.

### 3. Klippet kontrolleras med örat, och slutfilmen skrivs ut igen

- **Två utskrifter av råfilen:** en vanlig (Whisper slätar ut upprepningar) och en ordagrann som skriver upprepningar två gånger; läs båda.
- **Klipp på vågformen**, aldrig bara på utskriftens tider.
- **Efter klippet:** skriv ut klippets ljud igen och jämför orden som skulle vara med mot orden som hörs; varje skillnad är ett avklippt ord, en omtagning som läckt eller en upprepning som blev kvar tills någon lyssnat på den.
- **Slutfilmen skrivs ut en gång till:** ett ord som musiken eller en effekt dränkte syns där ("Claude did" hördes som "Flaw dead" under en smäll; −4 LU fick "a leak" att bli "illegal").
- **Kontrollera utskriften mot videon minut för minut:** Parakeet tappade en gång 13 sekunder tyst, och allt efter låg fel.
- **Första ordet efter en paus** flyttas till där ljudet börjar; utskrifterna stämplar det 60–220 ms för tidigt.
- **Bilden räknas på antal rutor** och totalen kontrolleras; annars drar den sig tre rutor efter rösten över en lång film.

**För Viska:** `video-edit` tvättar redan tal med ffmpeg. Lägg till den ordagranna utskriften, jämförelsen efter klippet och den sista utskriften av slutfilmen som obligatoriska steg i `film-assembly` och `video-edit`, och ett verktyg som gör jämförelsen.

### 4. Balansen mellan ansiktet och grafiken

Varje ögonblick är **ansikte** (kroken, åsikter, reaktioner, frågor till tittaren, slutsatsen, CTA:n), **båda** (grafiken på 65 % till vänster och ansiktet till höger, eller ansiktet i ett hörn: förklaringar, siffror, jämförelser, listor) eller **grafik** (helbild: det som ska läsas, kapitelkort). Varje läge 20–45 %, ungefär en tredjedel var; ansiktet i bild minst 60 %; aldrig mer än ungefär 12 sekunder utan ansiktet. Ingen grafik på en rad där personen talar *till* tittaren. Grafik görs så att den håller i båda layouterna: viktigt innehåll aldrig i nedre högra 30 × 30 % (där hörnet hamnar), rubrik minst 90 px och brödtext minst 48 px.

**För Viska:** en regel och en kontroll i `film-assembly` för talking head och intervju, som `film_build.py` kan räkna ut ur `film.yaml`.

### 5. Varje grafik betygsätts innan den lämnas

Kontaktark av grafiken, betyg 1–10 på läsbarhet i telefonstorlek, rörelse, komposition, premiumkänsla och riktighet (personens ord, riktiga siffror); rätta de tre sämsta, rendera om; skeppa vid 8 eller mer, högst tre rundor. Bara en rendering i taget (ett lås). Grafiken renderas utan ljud; ljudet läggs i hopbygget.

**För Viska:** in i `motion-graphics` som slutsteg. Låset behövs om flera agenter renderar på Surface Pro 7.

### 6. Bara personens ord och riktiga siffror

Samma regel som vi redan har, men skarpare formulerad: varje ord på ett kort är personens (ur utskriften av det klippta) eller verklig text ur en skärmbild; inga parafraser som lägger till ord; en återspelad terminal visar bara rader verktygen faktiskt skrev, märkt "Real output · replayed"; inga påhittade visningssiffror eller "12K likes" i ett återbyggt gränssnitt. Siffror som bara en källa har märks som en källas påstående. Ett påstående i talet som är fel klipps bort, och personen får se vad som togs bort; det "rättas" aldrig med ord personen inte sa.

### 7. Ljudet

- **Musiken klipps, den duckas inte:** den ligger på en fast nivå under talet och **tystnar helt under poängen** och slår tillbaka på nästa rad. Aldrig en smäll eller ett fall *på* ett kort ord.
- Nivåer: Editor V1 lägger musiken ungefär 5,5 LU under talet (förebilderna 0,8–13,5 dB); EDIT-systemet ungefär 28 dB under för långformat, slutmix −16 LUFS och högst −1 dBTP mätt på den kodade filen.
- **Rösten lyfts, den bearbetas inte:** ingen kompressor, gate, EQ, brusreducering eller loudnorm på rösten; en datorfläkt dras ner högst 8 dB med ett fingeravtryck ur minst 20 s rumston.
- Ett ljud på varje byte, men roterade (fyra varianter av samma klick), annars låter det som en metronom.

**För Viska:** "musiken tystnar under poängen" och slututskriften mot dränkta ord in i `film-assembly`. Klick på varje byte hör till en snabb stil, inte till våra standardfilmer.

### 8. Material ur verkligheten, med rättigheter först

Varje källa går in i planens tabell med licens, och allt oklart märks FLAG; personen bestämmer innan något renderas. Fällor de gått i: sidor bakom Cloudflare ger en "verifiera att du är människa"-sida; NASA:s länkar är http som omdirigerar (en .jpg blev HTML); samtyckesrutor och sidor som laddar vid scroll ger tomma skärmbilder; **titta på varje skärmbild**. Riktiga logotyper hämtas från varumärkets egen fil och ritas aldrig om, och visas bara för att namnge det man pratar om. Välj ögonblicket i ett klipp med en genomsökning på 2–3 bilder per sekund, aldrig mitten av filen.

**För Viska:** stämmer med `film-sourcing` och rättighetsloggen; lägg till fällorna och logotypregeln.

### 9. Kundsamtalet och planen (Katana Director)

- Två frågor i taget, aldrig ett formulär; be om filer i samma andetag som frågan de hör till.
- **Tre budgetvägar** med ett hårt tak: eget material och rörlig grafik (inga generatorkrediter), plus AI-bilder (billigt), plus AI-video (dyrt: 15 s helt genererat kan passera 100 krediter).
- **Planen som tabell:** tid, i bild, text i bild (exakt stavat), hur det görs, kostnad, och summan mot taket. "Kör det, eller ändra något?" Start bara på ett tydligt ja.
- **Kampanj:** samma kropp och slut, tre krokar (smärta, önskan, belägg), två format (9:16 och 4:5); testet är poängen.
- Recept per bransch (tandläkare, byrå, restaurang, konsult, mäklare, e-handel, gym, salong, SaaS, hantverkare) med krokar, vad man ber om och trolig budgetväg.

**För Viska:** budgetvägarna och kostnadskolumnen in i `film-production` (behovslistan har redan kostnad); kampanjmönstret som en egen typ; branschrecepten som referens, översatta till svenska förhållanden.

### 10. Arbetsflödet som håller över flera sessioner

Varje steg lämnar en fil i projektmappen (`keep.json`, `edl.json`, `GRAPHICS.md`, `plan.py`, renderingarna), så att nästa session tar vid där den förra slutade, även när användningsgränsen nås mitt i. Planen visas innan något byggs ("det billigaste ögonblicket att ändra sig"). Kort testrendering först, anteckningar med exakt sekund ("vid sekund 22"), och fråga hur lång tid det tar innan det startar. Två hjälpagenter bygger kort och diagram parallellt med var sin brief och sina rader i prioritetsordning (de längsta sträckorna utan grafik först). Inget publiceras; agenten renderar och stannar.

**För Viska:** samma princip som vår `film.yaml` ("dokumentet är prompten"). Ta in hjälpagentmönstret när grafiken blir många.

## Det vi inte tar in

- **Tempot och looken i Editor V1** som standard: 60–180 bilder i minuten, teal och orange, röda jätteord, klick på allt. Det är en stil för nyhets- och dokumentärreels, inte för en Visita-film. Den kan bli en template bland andra.
- **Katana och Higgsfield via MCP**; regissörsdelen tar vi, utförandet gör vi själva.
- **Musik ur "copyright free"-sökningar på YouTube** och skärmbilder av andras inlägg utan rättighetskontroll.
- **Gratismodellen GLM i OpenCode** för kunduppdrag: modellen körs i molnet, så utskrifter och planer om kundens material lämnar datorn.
- **AI-genererad sång och sångerska** (ACE-Step, lip sync) i kundfilmer; de konstaterar själva att lip sync ser ut som varje AI-avatar.
- Påståendena om "$0" och "en prompt": deras egna videor visar att det tar timmar och många anteckningar.

## Förslag på ordning

1. `style-capture`: skillen och mätverktyget, provat på två eller tre förebilder Mårten väljer, med en första egen template.
2. Kontrollerna i klippet: ordagrann utskrift, jämförelse efter klippet, slututskrift mot dränkta ord (verktyg + rader i `film-assembly` och `video-edit`).
3. Balansregeln och grafikbetyget i `film-assembly` och `motion-graphics`.
4. `anteckningar.md` per template och kund.
5. Kundsamtalet, budgetvägarna och kampanjmönstret i `film-production`, med branschrecept på svenska.

Allt skrivs först här i `C:\temp\nextphase\` och flyttas in hos Viska i visita-kommunikation när den andra datorn är klar.
