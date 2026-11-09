---
name: wrap
source: wds
description: Avsluta en session. Skriver överlämningen i två delar, projektdelen i repot och den personliga delen i det privata skåpet (till samma eller en annan agent), jämför sessionen med alla soul-filer och uppdaterar dem i repot och privat, för skill-ändringar till källrepot och katalogen, rapporterar incidenter och föreslår G&C-punkter, uppdaterar projektloggen och delar arbetet.
used_by: [idun, saga, freya, mimir]
tools: [wds/git]
---

# Wrap: avsluta sessionen

Agentoberoende. Skillen beskriver *vad* som ska göras. Hur git används står i [git-toolet](../tools/git.md).

**Wrap frågar inte vad som hände.** Agenten var med i samtalet och tar vad som gjordes, vad som återstår och nästa steg ur samtalet och git. De enda frågorna är var sessionerna och det privata skåpet ska ligga, och bara när svaret saknas (steg 1 och 4).

**Arbetet stannar hos arbetet, personen stannar hos personen** (principen P2 i `governance/wds/principles.md`, Mårten 2026-11-01). Allt om arbetet skrivs fritt i repot: beslut, siffror, kunder, kod, vad som är kvar och hur teamet jobbar tillsammans. Allt om personen skrivs fritt i det privata skåpet: hur hen vill jobba, vad hen lärde sig, hur det gick och vad hen levererade. Ingen av delarna behöver censureras, och ingen kopierar från den andra. Det privata länkar till arbetet, så att inget av organisationens följer med en person som stängs av från ett repo.

## 1. Vem, vilken session, till vem

- **Användare:** identifiera enligt git-toolet. Det ger `<användare>`, alltså GitHub-användarnamnet med små bokstäver.
- **Session-id:** `YYYY-MM-DD_HH-MM-<användare>`, med svensk lokaltid vid **sessionens start**. Agenten noterade tiden vid start (se AGENTS.md). Om den inte gjorde det: använd tiden för sessionens första commit, och annars tiden nu.
- **Från:** den agent som var aktiv (saga, freya, mimir, ivonne …), oavsett modell. Utan agent: modellnamnet med små bokstäver och bindestreck, till exempel `claude-opus-5-5`.
- **Till:** vem som ska ta nästa steg. Oftast samma agent, och då är wrapen en överlämning till sig själv. Hör nästa steg till en annan agent blir det den agenten.
- **Vad:** ta reda på vad som ändrats enligt git-toolet. Med det och samtalet framför dig: vilka projekt rördes, vad blev klart och vad återstår?
- **Projektrot:** mappen där projektet bor. Det är repots rot, utom när repot har flera projekt. Då är det projektets egen mapp, till exempel `projects/<projekt>/`, och repots `AGENTS.md` säger vilken. Rörde sessionen inget enskilt projekt: repots rot.
- **Sessionsmapp:** där överlämningarna sparas. Normalt `<projektrot>/sessions/`. Repot kan bestämma annat i `<projektrot>/sessions/README.md`:
  - `sessions: private` betyder att ingen sparar sessioner i repot, vilket passar ett publikt repo som många arbetar i. Varje person väljer själv en plats i sitt privata skåp. Platsen står i skåpets `projects/<repo>.md` på raden `sessions:`, som en länk relativt den filen. Det gäller bara repon vars innehåll redan är publikt; ett repo med en organisations interna material behåller projektdelen i repot.
  - Saknas raden, fråga personen en gång var sessionerna för det här repot ska ligga, och skriv svaret där. Saknas skåpet, eller avstår personen, visas överlämningen bara i chatten och sparas inte.
- **Privat sessionsmapp:** där den personliga delen sparas, `sessions/` i roten av det repo eller den lokala mapp där det privata skåpet (`private:`) ligger.

## 2. Överlämningen, i två delar

Varje wrap är en överlämning i två delar med samma session-id:

- **Projektdelen** i repot: allt om arbetet, så fullständigt att vem som helst kan fortsätta från den ensam. Den nämner aldrig att det finns en personlig del och länkar aldrig dit.
- **Den personliga delen** i den privata sessionsmappen (steg 1): det som bara rör personen, och en länk till varje projektdel. Den kopierar inget ur projektdelen.

Testet för varje rad: behöver någon annan det här för att fortsätta? Då hör det till projektdelen. Finns inget privat skåp skrivs bara projektdelen.

### Projektdelen

Mappen är **mottagarens**. Filnamnet är `<session-id>-<från>-<sammandrag>.md`:

- `<session-id>` = `YYYY-MM-DD_HH-MM-<användare>`, alltså tidsstämpel och vem som körde.
- `<från>` = agenten som skrev.
- `<sammandrag>` = vad sessionen gjorde, 3–6 ord, små bokstäver, bindestreck, å/ä → a och ö → o. Exempel: `2026-09-27_13-22-martenangner-ivonne-product-brief-en-karriar-tack.md`.

Filnamnet börjar med tidsstämpeln och slutar med sammandraget. Återupptagningskommandot (steg 9) hittar filen på tidsstämpeln och visar sammandraget, så att man ser vad överlämningen handlar om innan man kör den.

| Mottagare | Sökväg |
|---|---|
| Samma person, samma agent (vanlig wrap) | `<sessionsmapp>/<användare>/<från>/<session-id>-<från>-<sammandrag>.md` |
| Samma person, annan agent | `<sessionsmapp>/<användare>/<till>/<session-id>-<från>-<sammandrag>.md` |
| Känd annan person | `<sessionsmapp>/<person>/<till>/<session-id>-<från>-<sammandrag>.md` |
| Vi vet inte vem som kör | `<sessionsmapp>/all-users/<till>/<session-id>-<från>-<sammandrag>.md` |
| Förslag till WDS-metoden (steg 4 och 6) | Idun hos den som förvaltar WDS, se nedan |

**Förslag till WDS-metoden** gäller agenterna, deras skills och tools och WDS standardpolicy. De ändras bara i WDS källrepo, whiteport-design-studio, och Mårten Angner godkänner. Förslaget blir en egen överlämning till Idun, som samlar in förslagen från alla kunders wraps och för dem vidare till källrepot:
- **Den som förvaltar WDS kör wrapen:** i den egna sessionsmappen för WDS källrepo, `<sessionsmapp>/<användare>/idun/`. Källrepots `sessions/README.md` avgör var mappen ligger; säger den `sessions: private` är det personens privata sessionsmapp för whiteport-design-studio.
- **Någon annan kör wrapen:** i WDS källrepo `sessions/all-users/idun/` om repot sparar sessioner och agenten får skriva där. Annars i det här repots `<sessionsmapp>/all-users/idun/`, där Idun hämtar den när hon går igenom kundens repon.
- Skriv bara det som tål att läsas av alla i projektet: bristen, vad som hände och förslaget, med länk till incidenten om det finns en.

```markdown
---
session: YYYY-MM-DD_HH-MM-<användare>
start: YYYY-MM-DDTHH:MM+02:00
slut: YYYY-MM-DDTHH:MM+02:00
user: <användare>
från: <agent eller modell>
till: <agent eller modell>
model: <modell-id>
tool: <claude|copilot|codex|...>
projects: [<projekt>, ...]
repos: [<repo>, ...]
status: öppen
tagen_av:
---

## Gjort
- ...

## Kvar
- ...

## Nästa
Konkreta steg i ordning för mottagaren.

## Filer
- [relativ/sökväg](../../../relativ/sökväg)
```

- Håll den kort. Den ska kunna läsas på en minut. `projects: []` om sessionen inte rörde något specifikt projekt.
- **Gjort betyder levererat.** Under `## Gjort` står bara det som mottagaren faktiskt har fått: publicerat på live och kontrollerat i webbläsaren, skickat eller godkänt. Det som bara finns lokalt, i ett utkast eller i en databas som ingen ser, hör till `## Kvar` och märks "bara lokalt, inte live" med vad som stoppar det. Ett uppdrag med sådant kvar får inte `status: klar`.
- **Till en annan agent:** skriv även en kort wrap till dig själv om du har egna trådar kvar, och länka överlämningen därifrån.
- **Status:** mottagaren sätter `status: tagen` och `tagen_av: <session-id>` när hen börjar (se AGENTS.md, sessionsstart). Tog den här sessionen en överlämning: sätt `status: klar` i den filen om uppdraget är gjort.
- **Överlämningar raderas aldrig.** `sessions/all-users/` är neutral och har inget användar-id. Vem som körde framgår av sessionen när den tas (`tagen_av: <session-id>`).
- **Skriva i någon annans mapp:** det enda som är tillåtet är att lägga en *ny* fil i deras `sessions/<person>/<agent>/`.

### Den personliga delen

I `<privat sessionsmapp>/<användare>/<till>/`, med samma filnamn som projektdelen. Rörde sessionen flera repon får den ett sammandrag för hela sessionen. En personlig del per session, hur många repon den än rörde.

```markdown
---
session: YYYY-MM-DD_HH-MM-<användare>
user: <användare>
från: <agent eller modell>
till: <agent eller modell>
del: personlig
repos: [<repo>, ...]
status: öppen
tagen_av:
---

## Projektdelar
- <repo>: `sessions/<användare>/<till>/<filnamn>.md`

## För dig
Hur det gick, vad som skavde, vad du lärde dig, hur du lät och vad som gav energi. Fritt och utan censur, men aldrig organisationens information.

## Nästa
Bara det som är ditt, utöver projektdelarnas Nästa: trådar i andra repon, sådant du själv vill göra.
```

- **Vad som får stå:** kundens och projektets namn, vad som levererades, hur det kändes och vad du lärde dig. **Inte:** siffror, kunddata, strategi, kod, beslut eller kopior ur projektdelen (`governance/wds/data.md`, Shared and private).
- **Ekonomi, hälsa och familj** går fortfarande till personens egen agent (steg 4), inte hit.
- Ingenting nytt för personen: skriv ändå delen med länkarna, så att sessionen finns i personens historia.

## 3. Projektloggen: teamets gemensamma tidslinje

För varje projekt som rördes: lägg en post i projektets designlogg. Den ligger i projektroten, eller i mappen ovanför sessionsmappen när sessionerna sparas privat. Ta den som finns av `_progress/00-design-log.md`, `design-process/_progress/00-design-log.md`, `00-design-log.md` och `design-log.md`. Har loggen en `## Log`-rubrik läggs posten överst under den, annars överst i filen, med samma rubriknivå som posterna som redan finns. Saknas loggen: hoppa över steget.

```markdown
### YYYY-MM-DD_HH-MM-<användare> (<från> → <till>)
- En till tre punkter om vad som hände i projektet. [Överlämning](<relativ sökväg till överlämningen>)
```

**Mappresentationerna.** För varje WDS-mapp i projektet som sessionen ändrade (`A-Product-Brief/` till `E-Development/`): uppdatera mappens `presentation.md` så att den visar mappen som den står efter sessionen, rendera den och ta med den i commiten. Hur och vad: [folder-presentation](folder-presentation/SKILL.md). Har mappen ingen presentation än men fick sitt första riktiga innehåll: skapa den.

## 4. Soul-genomgång: jämför och uppdatera

**Var ligger det privata skåpet?** Platsen står i `private:` i `users/<användare>/user.md`, och en kopia står i `.wds/me.md`. Det kan vara en lokal mapp eller ett repo.
- **Saknas `private:`, eller finns mappen inte på den här datorn:** fråga personen var de privata soul-filerna ska sparas. Föreslå en mapp i ett repo som personen själv äger, eller en lokal mapp, men aldrig projektrepot. Skriv svaret i `private:` i `user.md` och i `.wds/me.md`, och skapa mappen och de filer som behövs.
- **Personen avstår:** skriv bara i repots skåp. Visa i kvittensen vad som skulle ha sparats privat, och fråga igen vid nästa wrap.

Agenten läste soul-filerna vid start och skrev in det som skulle bestå redan under sessionen ([session.md](../data/session.md), Start och During the session). Wrap är skyddsnätet: gå igenom hela samtalet, jämför det med vad filerna säger nu och skriv in det som ännu inte står där. Leta efter allt som är nytt eller har ändrats:

- **Fakta om personen:** var hen jobbar, roll, chef och kollegor, kunder, vad som har hänt, adresser, bolag
- **Människor i personens liv:** vem någon är, relationen och vad ni har gjort tillsammans
- **Rättelser** av agenten, och vad personen uppskattade eller avvisade
- **Insikter** om hur personen tänker, beslutar och vad hen värdesätter
- **Mål** som tillkom, ändrades eller nåddes
- Sådant som **levererades**

Varje nyhet sorteras till rätt fil:

| Nytt | Fil | Skåp |
|---|---|---|
| Nuläge: arbetsplats, roll, chef, kollegor, kunder, vad som har hänt | `heartbeat.md` | privat |
| Personens egen stil: hur agenter ska jobba med hen, överallt (ton, tempo, format, vad som irriterar), också när det lärdes i det här repot | `soul.md` | privat |
| Hur vi jobbar tillsammans i det här repot: roller, överenskommelser, arbetssätt i teamet och med agenterna | `soul.md` | repo |
| Vem personen är: värderingar, drivkrafter, sätt att tänka | `identity.md` | privat |
| Professionell profil: kompetens, erfarenhet, arbetssätt | `user.md` | privat |
| Bestående fakta: adresser, bolag med organisationsnummer, hem, kontaktvägar | `user.md`, avsnittet Fakta | privat |
| Människor: kollegor, kunder, partner, familj och vänner. Vem, relationen, historik med datum och källa. Kontaktuppgifter står i personens adressbok (till exempel Google Contacts) och filen hänvisar dit, aldrig en kopia | `people/<namn>.md`, och en rad i `people/README.md` | privat |
| Roll i det här projektet | `user.md` | repo |
| Personliga mål | `objectives.md` | privat |
| Projektets mål och personens mål i projektet | `objectives.md` | repo |
| Levererat, på CV-nivå: vad, för vem och när ("byggde det öppna glaset för Visita"), aldrig hur det gjordes inne hos kunden | `achievements.md` | privat, överst, med länk till projektdelen. Projektets egen tidslinje är designloggen (steg 3) |
| Ekonomi, hälsa och känsliga detaljer om relationer (konflikter, privatliv) | en överlämning till personens privata agent i `sessions/<användare>/<agent>/` i det privata skåpets repo (eller i den lokala mappen) | privat, aldrig i soul-filerna och aldrig i projektrepot |

Repots filer ligger i `users/<användare>/`. De privata ligger där `private:` pekar.

**Regler**
- **Uppdatera och optimera, lägg inte bara till nya rader.** Skriv in det nya där det hör hemma, slå ihop dubbletter, ersätt det som inte längre gäller och stryk det inaktuella. Håll varje fil kort och lätt att läsa. Rättelser och händelser får datum.
- **Agentens metod hör inte hemma i soul.** Rättar personen hur agenten följer sin egen metod, till exempel samtalsguiden eller en mall, är det en brist i agentinstruktionerna. Föreslå en ändring uppströms i stället för att skriva i någons soul. Gäller det WDS-agenterna blir förslaget en överlämning till Idun hos den som förvaltar WDS (steg 2, Förslag till WDS-metoden).
- **Repots filer delas med teamet.** Skriv aldrig något privat där, och ändra aldrig i någon annans mapp.
- **De privata filerna håller aldrig organisationens information.** En lärdom skrivs som personens egen ("vill ha siffran före resonemanget"), inte som kundens sak ("Visitas budget är …").
- **Privata filer skrivs direkt.** Är skåpet ett repo görs commit och push enligt git-toolet. Är det en lokal mapp sparas filerna bara. Kvittensen visar vad som ändrades.
- Rör bara de filer där något nytt faktiskt har hänt. `heartbeat.md` skapas första gången det finns något att skriva.

## 5. Skills: katalogen och källrepona

Skills ligger i repot för det projekt, initiativ eller företag de gäller. Personens katalog (`skills.md` och `skills.json` i det privata skåpet) listar personens egna skills och alla repon personen jobbar i.

- **Nytt projekt:** finns det här repot inte i katalogen, lägg till det med sökväg, GitHub-adress och vad det innehåller. Från och med nu synkas det vid varje wrap.

Resten gäller när sessionen skapade, ändrade, flyttade eller tog bort en skill, ett tool eller ett skript.

- **Inget som fungerar blir kvar i en temporär mapp.** Gå igenom sessionens arbetsmapp (scratchpad, `%TEMP%`, sessionsmappar) och miljöer utanför repona (till exempel `~/.venvs`). Ett skript, en installation eller en inställning som fungerade flyttas till källrepot för det tool det hör till, med sökvägar och mätningar i toolets beskrivning. OpenVINO-utskriften från 2026-10-14 låg bara i en temporär mapp och byggdes om nio dagar senare (2026-10-23).

- **Ändringen ska ligga i källan.** Varje skill har exakt ett källrepo. En ändring som gjordes i en lokal kopia, till exempel `~/.claude/commands`, en adaptermapp eller en synkad `agents/wds/`, flyttas till källrepot. Där görs commit och push. Externa källor ändras uppströms.
- **En commit per skill eller tool.** Varje ändrad skill eller tool får en egen commit med bara den filen och dess skript, aldrig annat arbete. Meddelandet ska vara `skill(<namn>): <vad som ändrades och varför>` eller `tool(<namn>): …`. Då visar `git log -- <fil>` hur skillen har utvecklats.
- **Katalogen uppdateras.** Har personen en skillskatalog i sitt privata skåp (`skills.md`, och `skills.json` om den finns), lägg in nya skills och källor, och ändra raden för det som flyttats eller tagits bort. Skriv över inget. Uppdatera raden där skillen står.
- **Sprid versionen.** Kör synken enligt katalogen, så att alla repon och den här datorn får den nya versionen.
- **Bekräftelse:** synk, en ny rad i katalogen samt commit och push i personens egna repon görs utan att fråga, och kvittensen visar vad som hände. Personen bekräftar bara när ändringen går till ett publikt repo, hamnar i någon annans repo, eller tar bort eller flyttar en skill.
- **Skill och tool hålls isär** enligt `agents/wds/README.md` (Skills and tools). Kontrollera att skillen listar sina tools i `tools:` och att varje tool listar sina skills i `used_by:`. Kommandon som hamnat i en skill flyttas till ett tool.

## 6. G&C: incidenter och förslag

Governance säger *vad* som gäller och varför: principerna, policyerna och vem som beslutar. Compliance är *hur* vi håller oss till dem: rutiner, kontroller, avvikelser och incidenter. Varje session kan visa att ramverket saknar något, och wrap är skyddsnätet som fångar det.

Gå igenom sessionen och leta efter:
- **Incident:** något hände som bryter mot en princip, eller nästan gjorde det. Exempel: ett lösenord som projektet använder finns i en publik databas efter en läcka.
- **Avvikelse:** något i repot eller arbetssättet följer inte en princip just nu.
- **Lucka:** ett fall som ramverket inte täcker, så att agenten fick improvisera.

För varje fynd:
1. **Akut först.** Står en hemlighet öppen eller pågår skada, säg det direkt i sessionen när det upptäcks, inte vid wrap. Människan agerar, till exempel byter lösenordet.
2. **Incidentrapport** i incidentloggen som `governance/policies.md` pekar ut för rätt nivå: organisationens (`governance/<org>/incidents.md`, eller det lokala namnet, till exempel `governance/visita/incidenter.md`) eller projektets. Har organisationens mapp en `.source`-fil är den en kopia: skriv rapporten i källrepot som `.source` anger, och kan agenten inte skriva där blir rapporten en överlämning till policyns ägare. Skriv datum, vad som hände, påverkan, vad som gjordes och vem som vet. **Skriv aldrig själva hemligheten**, bara var den fanns och om den är bytt.
3. **Förslag på ny punkt:** en rutin för hur vi agerar (compliance), eller en ny princip om fallet visar att den saknas (governance). Märk den `förslag`, med datum och länk till incidenten.
4. **Mandatet:** agenten får rapportera, föreslå och skärpa. Den får aldrig själv mildra eller ta bort en princip, eller vidga vad agenter får göra. Det kräver människans uttryckliga ja. Policyns ägare godkänner förslagen. Det gäller Idun också.
5. **WDS standardpolicy** ändras i källan, whiteport-design-studio, aldrig i den synkade kopian `governance/wds/`. Förslaget blir en överlämning till Idun hos den som förvaltar WDS (steg 2, Förslag till WDS-metoden).
6. **Saknas `governance/` eller en incidentlogg** i repot: skriv fyndet under `## G&C` i överlämningen.

Inget fynd: hoppa över steget.

## 7. Dela

Spara och dela projektdelen, projektloggarna och repots användarfiler enligt git-toolet. Den personliga delen och de privata filerna delas i sitt eget repo. Commit-meddelandet ska vara `wrap: <session-id> — <en rad>`.

## 8. Andra repon och personlig logg

- **Andra repon i samma session:** skriv en projektdel med **samma session-id** i deras `<sessionsmapp>/<användare>/<till>/`, eller kör deras egen wrap. Varje repo får bara sin egen del. Den personliga delen länkar till dem alla. Tack vare samma id kan man hitta sessionen i alla repon.
- **Privat logg:** om `private:` pekar på en mapp på den här datorn, lägg en rad överst i `log.md` där: `- <session-id> <repo, …> (<från> → <till>): en rad · <den personliga delens sökväg>`. Skapa filen om den saknas. Är skåpet ett repo delas den där.

## 9. Kvittens

Visa användaren:
- session-id, mottagare och sökvägar till projektdelen eller projektdelarna och till den personliga delen
- båda delarna i sin helhet, så att personen ser att fokus stämmer och att inget av organisationens hamnade i den personliga
- vad som ändrades i soul-filerna, per fil och skåp (repo eller privat), eller "inget nytt"
- den privata överlämningen, om något om ekonomi, hälsa eller familj kom upp
- skills som ändrades: var de ligger nu och att katalogen är uppdaterad
- G&C: incidenter som rapporterades och punkter som föreslogs, eller "inget nytt"
- commit-hash och att push gick igenom

Avsluta med återupptagningskommandot som ett eget kodblock, så att det går att kopiera med ett klick. `<till>` är mottagande agent, `<repo>` är repots mappnamn, tidsstämpeln är sessionens start och `<sammandrag>` är samma ord som i filnamnet, med mellanslag i stället för bindestreck:

````
```
/<till> <repo> YYYY-MM-DD_HH-MM <sammandrag>
```
````

Exempel: `/ivonne martens-documents 2026-09-27_13-22 product brief en karriar tack`. Utan sammandraget vet man inte vad kommandot gäller när det ligger bland andra.
