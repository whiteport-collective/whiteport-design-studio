---
name: recording
description: Spelar in allt som hörs, och på begäran det som syns, på personens dator, skriver ut det live och grundligt efteråt. Media stannar i personens privata mediamapp; utskriften hamnar i rätt projekt. Använd när personen säger "starta inspelning", vill ha ett samtal, ett möte, en video eller ett webbinarium utskrivet, eller vill att agenten följer det som visas på skärmen.
used_by: [idun, saga, freya, mimir]
version: 1.0
tools: [wds/meeting-live, wds/git]
---

# Inspelning

Ett samtal är värt mest när allt finns kvar: vad som sades, vad som visades och vad som bestämdes. Inspelningen sker på personens egen dator, utan bot i mötet, så den fungerar i alla samtal och på alla plattformar (Meet, Teams, Zoom, Messenger, telefon via datorn) och för allt annat ljud, som videor och webbinarier. Ljudet tolkas på datorn.

Två regler, utan att fråga varje gång (Mårten, 2026-10-17):
- **Media stannar privat.** Ljud, skärmvideo och bilder sparas i personens privata mediamapp och flyttas inte. Personen bestämmer själv senare vad som görs med dem.
- **Utskriften hamnar i projektet.** Den grundliga utskriften arkiveras i mötesarkivet i det projekt samtalet gäller.

Hur det görs står i [meeting-live-toolet](../../tools/meeting-live.md): `local.py --dir` för inspelningen, `refine.py` för den grundliga utskriften och `live.py archive` för arkivet.

## Starta

Personen ska bara behöva säga **"spela in"** (eller "starta inspelning", "livetolka mötet"). Agenten förstår direkt, kopplar upp allt och kontrollerar ljudet själv. Den enda frågan före start är vilken skärm som ska spelas in (Mårten, 2026-10-21).

**Det här är den lokala inspelningen, inte Fireflies.** Gå aldrig med via Fireflies (`/join`, `live.py join`) när personen säger "spela in": den 21 oktober kostade det sex minuter av ett möte. Fireflies används bara när personen uttryckligen säger Fireflies.

**Beslut (Mårten, 2026-10-21): vi går bort från Fireflies.** Fireflies klarar språken dåligt, och den lokala utskriften svarar mycket snabbare. Lokal inspelning är standard. En egen mötesbot för Google Meet ska byggas för de fall där en synlig deltagare behövs.

1. **Fråga vilken skärm**, i ett meddelande med knappar: lista skärmarna som är anslutna (namn, upplösning, vilken som är huvudskärm) plus "ingen skärm". Inget annat i frågan.
2. **Starta direkt** efter svaret: den valda skärmen, datorns ljud och mikrofonen. Bara när personen säger att det är en video eller ett webbinarium: `--no-mic`.
   - **Mediamappen:** `recordings:` i `.wds/me.md`. Mappen får namnet `<datum>_<tid>-inspelning`; titeln kommer med i arkivet efteråt. Saknas `recordings:`: föreslå en plats i personens privata Drive, fråga en gång och skriv svaret i `.wds/me.md`. Det är den enda fråga som får komma före start.
   - Talarna heter `--them "De andra" --me "<personens namn>"` tills vidare. Namnen sätts i arkivet.
   - Kör i bakgrunden och starta bevakningen, enligt toolet.
3. **Kontrollera ljudet själv** inom en minut:
   - Vilka enheter lyssnar inspelningen på (första raderna i utskriften: `Lyssnar: … <- <enhet>`)? Är det de enheter personen faktiskt använder (headset, Bluetooth-hörlurar, högtalare)? Fel enhet: stoppa och starta om med rätt, direkt.
   - Visar statusraden (`== Status 00:15: … ==`, efter 15 sekunder och sedan varje minut) ljudnivå för båda kanalerna, och ligger texten bara några sekunder efter talet? Står det att sekunder hoppades över, säg det: ljudet spelas in ändå.
   - Kommer det repliker från **båda** kanalerna? Tills den första repliken kommit från en kanal: be personen säga något kort, och kontrollera att det dyker upp. Laddas taligenkänningen första gången (några minuter), säg det i en rad; ljudet spelas in ändå.
   - Säg sedan i **en** rad: "Inspelningen är igång: ditt ljud ✓, datorns ljud ✓, skärmen ✓." Eller vad som inte fungerar och vad du gör åt det.
4. **Fråga sedan, i ett meddelande:** vad handlar det om, vilket projekt gäller det, och vilka är med? Svaret styr kommentarerna under mötet och var utskriften arkiveras.

Alla i samtalet vet att det spelas in. Det är lagligt att spela in ett samtal man själv deltar i; i arbetssammanhang säger personen till de andra att en agent läser med, eftersom texten går vidare till en AI-tjänst. Om privata samtal bestämmer personen själv.

## Under inspelningen

**Lång tystnad under en feedbackrunda:** fråga kort om personen är kvar, i stället för att svara på varje statusrad (Mårten, 2026-10-24).

Inspelningen går vidare tills personen säger stopp, också när ingen säger något och när ingen sitter vid datorn: ljudet är lika långt som inspelningen, och datorn hålls vaken. Locket ska vara öppet. Följ samtalet som i [live-meeting](../live-meeting.md): korta rader i chatten bara när någon frågar något eller något behöver sägas nu. Med skärmen igång finns en bild för varje gång skärmen ändrats (`== Bild … ==` i bevakningen). Titta på den när det som sägs hänger på det som visas: en siffra i en presentation, ett dokument, en sajt.

## Stoppa

När personen säger "stoppa":

1. **Stoppa ordentligt** genom att lägga filen `STOP` i inspelningens mapp, så att ljud och video avslutas hela.
2. **Den grundliga utskriften:** kör `refine.py` på mappen. Säg ungefär hur lång tid den tar, och gör den i bakgrunden.
3. **Utskriften till projektet:** avgör vilket projekt samtalet gällde, utifrån vad som sades och vilka som var med. Är det oklart, fråga en gång med ett förslag. Arkivera `final.jsonl` med `live.py archive` i det projektets repo, med en rad i registret som pekar på mediamappen, och committa.
4. **Säg i en rad** var utskriften hamnade och att ljud och video ligger kvar i mediamappen.

**Feedback på eget arbete:** när feedbacken är nedskriven som en lista som personen har sett, behövs inte inspelningen längre. Lägg mappen i papperskorgen i stället för att köra `refine.py` och arkivera (Mårten, 2026-10-24).

Samtal som inte gäller något projekt får ingen utskrift i något repo; den ligger kvar i mediamappen tillsammans med ljudet.

Media hör aldrig hemma i git: ljud och video ligger i Drive, utskrift och sammanfattning i repot.
