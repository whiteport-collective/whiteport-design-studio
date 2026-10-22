---
name: meeting-live
source: wds
type: script
description: Spelar in och skriver ut det som hörs (och visas) på datorn lokalt med Whisper, live och grundligt efteråt, och arkiverar mötet. Fireflies bara när personen uttryckligen ber om det. Allt körs på datorn, utan server och utan MCP. Skripten ligger i meeting-live/.
used_by: [live-meeting, recording, video-edit]
---

# Tool: meeting-live

**Lokal inspelning är standard (Mårten, 2026-10-21).** Fireflies klarar språken dåligt, och den lokala utskriften svarar mycket snabbare. Använd `local.py` (avsnittet [Lokal utskrift](#lokal-utskrift-utan-bot-standard)), `refine.py` och `live.py archive`. Fireflies-delarna (`join`, `watch` mot Fireflies, hämtningen i `archive`) används bara när personen uttryckligen säger Fireflies. En egen mötesbot för Google Meet ska byggas för de fall där en synlig deltagare behövs.

## Fireflies (bara på uttrycklig begäran)

Fireflies realtid går direkt till en jsonl-fil på datorn. Agenten bevakar filen och får nya repliker ungefär var 30:e sekund.

```
Fireflies (socket.io) → live.py join (i bakgrunden) → .wds/live/<tid>-<titel>.jsonl → live.py watch → agenten
```

Strömmen och bevakningen är två processer. Bevakningen kan startas om när som helst utan att mötet tappas, och den fortsätter där den slutade (`<fil>.seen`).

## Konfiguration

| Vad | Var |
|---|---|
| Fireflies språk | **Multi-Language på alla möten** (Mårten, 2026-10-17), i Fireflies inställningar: flera språk i samma möte, beta. Språket går inte att sätta i kalenderinbjudan. |
| Fireflies-nyckeln | Bitwarden-posten `Fireflies API Key`, lösenordsfältet. Hämtas vid körning, skrivs aldrig till fil. |
| Python-paket | `python -m pip install "python-socketio[client]"` (en gång per dator). Den lokala reserven: `pyaudiowpatch faster-whisper numpy`. |
| Mötesfilen | `.wds/live/` i repots rot, arbetsmaterial under mötet. `.wds/` är gitignorerad. |
| Mötesarkivet | `communication/meetings/` på den nivå det gäller (repots rot för en kund), med registret `communication/meetings.md`. Repots `AGENTS.md` kan ange en annan plats. |

Skriptet: `agents/wds/tools/meeting-live/live.py`. I ett repo utan `agents/wds/` används sökvägen i WDS-repot.

## Åtgärder

### Pågående möten

```bash
FIREFLIES_API_KEY="$(bw get password 'Fireflies API Key')" python agents/wds/tools/meeting-live/live.py list
```

### Gå med (i bakgrunden)

Det senaste pågående mötet, eller ett visst med `--id <id>`. Kör med Bash `run_in_background`, eftersom processen lever lika länge som mötet:

```bash
FIREFLIES_API_KEY="$(bw get password 'Fireflies API Key')" python agents/wds/tools/meeting-live/live.py join --number 1
```

Utskriften börjar med `Ansluten till "<titel>"` och `Fil: <sökväg>`. Mötets tidigare repliker skrivs in först, så att agenten kommer ikapp.

**Joinen håller sig vid liv.** Faller anslutningen till Fireflies och kommer inte tillbaka inom 20 sekunder, bygger joinen en ny i samma fil och fyller luckan ur Fireflies sparade transkript. Bevakningen visar `== Anslutningen föll, ansluter igen ==` och `== Luckan fylld med N repliker ==`. Ingen replik skrivs två gånger.

**Har processen dött,** fortsätt i samma fil i stället för att starta en ny:

```bash
FIREFLIES_API_KEY="$(bw get password 'Fireflies API Key')" python agents/wds/tools/meeting-live/live.py join --continue .wds/live/<fil>.jsonl
```

### Bevaka

**Claude Code:** Monitor med kommandot nedan och `timeout_ms: 1800000`. Varje utskrift är en klump nya repliker. När bevakningen löper ut efter 30 minuter startas den igen med samma kommando.

```bash
python agents/wds/tools/meeting-live/live.py watch .wds/live/<fil>.jsonl --every 10
```

Bevakningen skriver ut `== MÖTET ÄR SLUT: <skäl> ==` och avslutas när Fireflies slutar spela in, och `== FEL: … ==` om något går fel.

**Copilot och Codex** har ingen bevakning som väcker dem. Läs nya rader med `transcript` när personen frågar, eller mellan varje svar.

### Hela mötet som text

```bash
python agents/wds/tools/meeting-live/live.py transcript .wds/live/<fil>.jsonl
```

### Lokal utskrift, utan bot (standard)

Lyssnar på datorns ljud ut, alltså det personen hör, och mikrofonen, och skriver ut lokalt med Whisper när talaren pausar, i samma format. Ljudet lämnar aldrig datorn. Ingen bot går med i mötet, så det fungerar oavsett vem som bjudit in och på vilken plattform. Med `--no-mic` bara datorns ljud: videor, webbinarier, poddar.

**De andra ska veta om det.** En bot syns i mötet; den lokala utskriften syns inte. Använd den bara när alla i samtalet vet att det skrivs ut, och aldrig i privata samtal som inte gäller arbetet. Börjar ett samtal handla om något annat, stoppa utskriften.

Whisper hittar ibland på text i brus och korta ljud (".", "000", `<|nospeech|>`, påhittade ord). Sådant sorteras bort med modellens egna mått på om det var tal och hur säkra orden är; i provet behölls alla 32 riktiga yttranden. Windows. Svenska använder KB-Whisper, som laddas ned första gången (några minuter). Kör i bakgrunden och bevaka filen med `watch` som vanligt:

```bash
python agents/wds/tools/meeting-live/local.py .wds/live/<tid>-lokal.jsonl --them "<de andra>" --me "<personen>" --lang sv
```

`--lang auto` upptäcker språket för varje bit, för möten som byter språk.

Uppmätt 2026-10-17 på Mårtens dator (8 kärnor, ingen grafikkort-acceleration) med ett svenskt röstmeddelande på 131 sekunder:

| Modell | Tid mot realtid | Svenska |
|---|---|---|
| `KBLab/kb-whisper-small` (`--lang sv`, standard) | 0,17 | Bäst: namn och ord rätt |
| `small` (`--lang auto`) | 0,18 | Upptäcker svenska, men fler fel |
| `medium` (`--lang auto`) | 0,49 | Inte bättre än KB-Whisper; med två ljudkällor nära realtid |

Siffrorna gäller långa bitar. **Varje bit kostar minst ungefär 2 sekunder**, eftersom Whisper alltid räknar på 30 sekunder ljud: 2 s ljud tar 2,4 s, 8 s tar 2,7 s och 28 s tar 4,1 s (mätt 2026-10-21). Många korta bitar, som "ja" och "mm" i mikrofonen, äter därför mest tid.

**Fördröjning:** ljudet klipps vid pauser (0,5 s) och senast efter 8 sekunder (`--pause`, `--max`). Mätt 2026-10-21 med fyra minuter av ett riktigt möte genom högtalarna, med `--screen`: första repliken 13 sekunder efter start (modellen laddas före), sedan text **8 sekunder efter yttrandets början** (median), 12 för 90 % och högst 15. Räknat från när talaren slutat är det 3–4 sekunder. Talarna skiljs bara åt som "de andra" och "jag".

```bash
python agents/wds/tools/meeting-live/local.py .wds/live/<tid>-<titel>.jsonl --no-mic --them "<videon>"
```

**Inspelningen och utskriften går var för sig.** Ljudet skrivs alltid till fil och tappas aldrig, hur långt efter utskriften än ligger. Utskriften går i en egen tråd:

- Det som väntar på utskrift **slås ihop per talare**, upp till 25 sekunder per bit, så att utskriften kommer ikapp av sig själv.
- **Eko sorteras bort live.** Hörs högtalarna i mikrofonen följer mikrofonens ljudnivå datorns ljud upp och ner; sådana bitar skrivs inte ut som "jag". I provet med datorns högtalare sorterades 28 av 67 ekobitar bort, och i Visita-mötet (hörlurar) bara 1 av 59 riktiga. Med hörlurar finns inget eko. `refine.py` tar bort ekot efteråt ur sin utskrift.
- Ligger utskriften ändå mer än `--max-lag` sekunder (30) efter talet **hoppar den över** biten. Ljudet finns kvar, och den grundliga utskriften tar den.

**Statusraden.** Efter 10 sekunder och sedan varje minut skrivs en rad i utskriften, som bevakningen visar:

```
== Status 05:15: De andra -20 dB, Mårten -46 dB · text 3 s efter talet · 8 s eko från högtalarna i mikrofonen ==
```

Ljudnivån per kanal visar att ljud kommer in (0 dB är fullt, under -60 i stort sett tyst, -90 eller `inget ljud` när inget spelas). Tal från mötet ligger runt -20 dB i datorns ljud; mikrofonen runt -45 när personen är tyst. Med statusraden efter 10 sekunder kan agenten säga "ditt ljud ✓, datorns ljud ✓" utan att vänta på en replik: datorns ljud syns bara när något spelas, så be personen säga något eller spela upp något kort om den kanalen är tyst. "text N s efter talet" är hur långt efter utskriften ligger. Står det att sekunder hoppades över hinner datorn inte med. `ljudblock tappade` betyder att ljudkortet fick vänta på programmet och tappade en bit (cirka 0,1 s per block); enstaka per minut är ofarligt. Läs statusraden i stället för filstorlekarna: Drive för skrivbordet visar inte nya storlekar förrän filen stängts.

**Windows får inte strypa processen.** En process som startats av en agent i bakgrunden, medan ett videomöte har förgrunden, kan strypas av Windows (EcoQoS). `local.py` stänger av det för sig själv, och skärmvideon körs med lägre prioritet än utskriften.

**Datorn ska orka med mötet också.** Whisper får tre av fyra kärnor (`--threads 3`): lika snabbt som fyra, och en kärna blir kvar till ljudet, videon och mötesappen. Med alla fyra hackade uppspelningen i högtalarna under ett prov. Uppmätt 2026-10-21 med 90 sekunder mötesljud i högtalarna (processorn i snitt):

| Vad som körs | Processor | Tappat |
|---|---|---|
| Bara uppspelningen | 17 % | – |
| Inspelning och liveutskrift | 43 % | inga ljudblock |
| Dessutom skärmvideo (`--screen`) | 49 % | 1 mikrofonblock |

Skärmvideon kostar alltså lite: 5 bilder per sekund tar en tredjedel av en kärna, och det mesta är själva skärmfångsten (2736×1824), inte kodningen. Hårdvarukodning (`h264_qsv`) sparade bara en femtedel och används inte; 2 bilder per sekund halverar kostnaden om det skulle behövas.

### Inspelning: ljud, skärm och grundlig utskrift efteråt

Allt i en mapp: utskriften live, ljudet per kanal och, med `--screen`, skärmen som video och en bild när skärmen ändras. Skillen [recording](../skills/recording/SKILL.md) beskriver flödet.

```bash
python agents/wds/tools/meeting-live/local.py --list-screens
python agents/wds/tools/meeting-live/local.py --dir "<inspelningens mapp>" [--monitor <n>] --them "<de andra>" --me "<personen>"
```

**Välja skärm.** `--list-screens` listar de anslutna skärmarna i riktiga bildpunkter, till exempel `1. Surface Panel (\\.\DISPLAY1): 2736x1824 (huvudskärm), position 0,0`. Använd det när skillen frågar vilken skärm som ska spelas in. `--monitor <n>` spelar in bara den skärmen, både video och bilder (och slår på `--screen`). `--screen` utan `--monitor` tar alla skärmar som en bild. Ingen skärm: varken `--screen` eller `--monitor`.

| Fil | Innehåll |
|---|---|
| `transcript.jsonl` | Liveutskriften, med en rad `{"event": "frame", "file": …}` för varje ny bild och en statusrad varje minut |
| `them.wav`, `me.wav` | Ljudet per kanal, 16 kHz. Lika långt som inspelningen: tystnad fylls i efter klockan, också när ingen säger något. Tiden i filen är samma som `start` i utskriften och tiden i bildernas namn |
| `screen.mp4` | Skärmen, 5 bilder per sekund, 1080 p (`--screen` eller `--monitor`) |
| `frames/<mm-ss>.jpg` | En bild när skärmen har ändrats, kontrollerat var femte sekund (`--screen`) |

- **Stoppa** genom att lägga en fil som heter `STOP` i mappen. Då avslutas ljud och video ordentligt; en process som avbryts hårt lämnar dem trasiga.
- **Datorn hålls vaken** under inspelningen, så den fortsätter när ingen rör datorn. Stängs locket följer Windows inställningen för locket.
- **Den grundliga utskriften** efteråt: större modell, hela ljudet i ett svep, grundligare sökning, och ekot från högtalarna borttaget genom att kanalerna jämförs. Den skriver `final.jsonl`, som `archive` tar:

```bash
python agents/wds/tools/meeting-live/refine.py "<inspelningens mapp>" [--model KBLab/kb-whisper-medium]
```

KB-Whisper medium laddas ned första gången (cirka 1,5 GB). Utan grafikkort-acceleration tar den ungefär halva samtalets längd per kanal. Den skriver först hur mycket av varje ljudfil som har ljud (`them.wav: 19:13 lång, ljud i 4:39 av den`); är det mycket mindre än inspelningens längd har ljud tappats. `final.jsonl` får inspelningens sluttid och längd, så att `archive` skriver rätt tid i huvudet och längden i registret.

#### Lärdomar från Visita-mötet 2026-10-21

Det första riktiga mötet med `--screen` (19 minuter, Teams) gav bara de första 4,5 minuterna. Orsakerna, som nu är åtgärdade:

1. **Utskriften och inspelningen gick i samma slinga.** Under mötet tog utskriften ungefär tre gånger längre tid än ljudet (Teams, skärmvideon och många korta bitar från mikrofonen). Medan slingan skrev ut låg ljudet kvar i minnet, och vid stopp kastades det: 15 minuter ljud skrevs aldrig till fil. Liveutskriften kom därför ungefär en gång i minuten och hamnade allt längre efter. Det gick inte att upptäcka under mötet.
2. **Modellen laddades efter att ljudet börjat spelas in,** så de första 25 sekundernas ljud hamnade före klockans start: negativa tider i början. Efter det räknades tiden ut från klockan minus det ljud som väntade, och blev fel när ljud saknades.
3. **`final.jsonl` hade ingen sluttid,** så `archive` skrev "11:08–11:08" och lämnade längden tom.

Resten av det mötet går inte att få fram: ljudet efter ungefär 4:40 skrevs aldrig till disk, och skärmvideon har inget ljud.

### Arkivera

Efter mötet: hela mötet till repots mötesarkiv, sammanfogat från alla filer som hör till mötet (flera anslutningar, en ny inspelning på rätt språk, den lokala reserven). Det färdiga transkriptet hämtas från Fireflies när det finns, eftersom det är renare än liveutskriften; annars används liveutskriften.

```bash
FIREFLIES_API_KEY="$(bw get password 'Fireflies API Key')" python agents/wds/tools/meeting-live/live.py archive .wds/live/<fil>.jsonl [<fil>.jsonl …] --out communication/meetings --lang sv --title "<mötets namn>"
```

`--media <mediamappen>` skriver var ljud och video ligger i utskriftens huvud och i registret. Det skriver `communication/meetings/<datum>-<titel>.md` och lägger till en rad i `communication/meetings.md` (datum, möte, längd, Fireflies-id, transkript, sammanfattning). Sammanfattningskolumnen fylls i när sammanfattningen är skriven. Fireflies färdiga transkript kan dröja några minuter efter mötet; `--no-fetch` arkiverar liveutskriften direkt.

### Avsluta

Stoppa bakgrundsprocessen. Joinen skriver själv en slutrad när mötet inte längre pågår i Fireflies (kontrolleras varje minut).

## Filformat

En rad per händelse, i ordning:

```json
{"event": "joined", "title": "…", "meeting_id": "…", "participants": ["…"], "at": "…"}
{"n": 1, "start": 3.2, "speaker": "Anna", "text": "…", "seed": true}
{"n": 2, "start": 61.0, "speaker": "Mårten", "text": "…", "id": "<chunk_id>"}
{"event": "reconnecting", "at": "…"}
{"event": "filled", "count": 4, "at": "…"}
{"event": "ended", "reason": "…", "at": "…"}
```

`seed: true` är repliker från före anslutningen, `fill: true` repliker som fyllde en lucka. `start` är sekunder från mötets början.

Den lokala utskriften har också statusrader och längden i slutraden:

```json
{"event": "status", "start": 75.1, "levels": {"De andra": -20, "Mårten": -45}, "lag": 3, "skipped": 0, "echo": 8}
{"event": "ended", "reason": "stoppad", "at": "…", "duration": 253.4}
```

## Fel

| Vad som händer | Säg och gör |
|---|---|
| Bitwarden är låst | "Lås upp Bitwarden: `bw unlock`, och klistra in BW_SESSION." Skicka den i miljön per kommando, spara den aldrig. |
| `Inga pågående möten` | "Fireflies spelar inte in just nu. Starta inspelningen, så går jag med om 30 sekunder." |
| `auth failed` | Nyckeln är fel eller har gått ut. Kontrollera Bitwarden-posten. |
| `Paketet saknas` | Installera `python-socketio[client]` och gå med igen. |
| Bakgrundsprocessen avslutas oväntat | Läs dess utskrift och fortsätt i samma fil med `join --continue <fil>`. |
| Statusraden visar `inget ljud` eller under -60 dB för en kanal | Fel enhet eller avstängd mikrofon. Stoppa och starta om med rätt enhet. |
| Statusraden visar att sekunder hoppades över | Datorn hinner inte skriva ut live. Ljudet spelas in ändå; den grundliga utskriften tar det. Hörlurar i stället för högtalare minskar arbetet. |
| Texten är obegriplig eller på fel språk | Fireflies har fel språkinställning. Säg det direkt, starta den lokala reserven, och be personen byta språk i Fireflies (det ger ett nytt mötes-id; gå med i det också). `archive` tar med alla delarna. |

Fördröjningen från tal till fil är några sekunder (Fireflies taligenkänning), plus bevakningens intervall.

## Inte tillgängligt

**Agenten kan inte tala i mötet.** Två vägar finns om det behövs, så att det inte behöver utredas igen:

| Väg | Hur | Passar |
|---|---|---|
| Virtuell ljudkabel | Text till tal till en virtuell mikrofon: VB-Cable och VoiceMeeter (Windows), BlackHole och Loopback (Mac). Personen väljer kabeln som mikrofon, och agenten talar i personens plats. Billigt men ömtåligt. | Eget bruk |
| Egen mötesbot för Google Meet | Ska byggas (beslut 2026-10-21): går med som synlig deltagare med egen mikrofon. Ersätter tanken på en köpt mötesbot (Recall.ai, Meetstream.ai). | När en synlig deltagare behövs |

Ljudkabeln räcker för eget bruk tills Meet-boten finns.
