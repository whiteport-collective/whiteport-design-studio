---
name: wrap
source: wds
description: Avsluta en session. Skriver överlämningen (till samma eller en annan agent), jämför sessionen med alla soul-filer och uppdaterar dem i repot och privat, för skill-ändringar till källrepot och katalogen, uppdaterar projektloggen och delar arbetet.
tools: [wds/shared/git]
---

# Wrap: avsluta sessionen

Agentoberoende. Skillen beskriver *vad* som ska göras. Hur git används står i [git-toolet](../tools/git.md).

## 1. Vem, vilken session, till vem

- **Användare:** identifiera enligt git-toolet. Det ger `<användare>`, alltså GitHub-användarnamnet med små bokstäver.
- **Session-id:** `YYYY-MM-DD_HH-MM-<användare>`, med svensk lokaltid vid **sessionens start**. Agenten noterade tiden vid start (se AGENTS.md). Om den inte gjorde det: använd tiden för sessionens första commit, och annars tiden nu.
- **Från:** den agent som var aktiv (saga, freya, mimir, ivonne …), oavsett modell. Utan agent: modellnamnet med små bokstäver och bindestreck, till exempel `claude-opus-5-5`.
- **Till:** vem som ska ta nästa steg. Oftast samma agent, och då är wrapen en överlämning till sig själv. Hör nästa steg till en annan agent blir det den agenten.
- **Vad:** ta reda på vad som ändrats enligt git-toolet. Med det och samtalet framför dig: vilka projekt rördes, vad blev klart och vad återstår?

## 2. Överlämningen

Varje wrap är en överlämning. Mappen är **mottagarens**. Filnamnet är `<session-id>-<från>-<sammandrag>.md`:

- `<session-id>` = `YYYY-MM-DD_HH-MM-<användare>`, alltså tidsstämpel och vem som körde.
- `<från>` = agenten som skrev.
- `<sammandrag>` = vad sessionen gjorde, 3–6 ord, små bokstäver, bindestreck, å/ä → a och ö → o. Exempel: `2026-09-27_13-22-martenangner-ivonne-product-brief-en-karriar-tack.md`.

Filnamnet börjar med tidsstämpeln, så `/<agent> <repo> YYYY-MM-DD_HH-MM` hittar den.


| Mottagare | Sökväg |
|---|---|
| Samma person, samma agent (vanlig wrap) | `sessions/<användare>/<från>/<session-id>-<från>-<sammandrag>.md` |
| Samma person, annan agent | `sessions/<användare>/<till>/<session-id>-<från>-<sammandrag>.md` |
| Känd annan person | `sessions/<person>/<till>/<session-id>-<från>-<sammandrag>.md` |
| Vi vet inte vem som kör | `sessions/all-users/<till>/<session-id>-<från>-<sammandrag>.md` |

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
- **Till en annan agent:** skriv även en kort wrap till dig själv om du har egna trådar kvar, och länka överlämningen därifrån.
- **Status:** mottagaren sätter `status: tagen` och `tagen_av: <session-id>` när hen börjar (se AGENTS.md, sessionsstart). Tog den här sessionen en överlämning: sätt `status: klar` i den filen om uppdraget är gjort.
- **Överlämningar raderas aldrig.** `sessions/all-users/` är neutral och har inget användar-id. Vem som körde framgår av sessionen när den tas (`tagen_av: <session-id>`).
- **Skriva i någon annans mapp:** det enda som är tillåtet är att lägga en *ny* fil i deras `sessions/<person>/<agent>/`.

## 3. Projektloggen: teamets gemensamma tidslinje

För varje projekt som rördes: lägg en rad **överst** i `projects/<projekt>/design-process/_progress/design-log.md`:

```markdown
## YYYY-MM-DD_HH-MM-<användare> (<från> → <till>)
- En till tre punkter om vad som hände i projektet. [Överlämning](../../../../sessions/<användare>/<till>/<fil>.md)
```

## 4. Soul-genomgång: jämför och uppdatera

**Var ligger det privata skåpet?** Platsen står i `private:` i `users/<användare>/user.md`, och en kopia står i `.wds/me.md`. Det kan vara en lokal mapp eller ett repo.
- **Saknas `private:`, eller finns mappen inte på den här datorn:** fråga personen var de privata soul-filerna ska sparas. Föreslå en mapp i ett repo som personen själv äger, eller en lokal mapp, men aldrig projektrepot. Skriv svaret i `private:` i `user.md` och i `.wds/me.md`, och skapa mappen och de filer som behövs.
- **Personen avstår:** skriv bara i repots skåp. Visa i kvittensen vad som skulle ha sparats privat, och fråga igen vid nästa wrap.

Agenten läste soul-filerna vid start ("Step: soul" i `shared-activation.md`). Gå nu igenom hela samtalet och jämför det med vad filerna redan säger. Leta efter allt som är nytt eller har ändrats:

- **Fakta om personen:** var hen jobbar, roll, chef och kollegor, kunder, vad som har hänt
- **Rättelser** av agenten, och vad personen uppskattade eller avvisade
- **Insikter** om hur personen tänker, beslutar och vad hen värdesätter
- **Mål** som tillkom, ändrades eller nåddes
- Sådant som **levererades**

Varje nyhet sorteras till rätt fil:

| Nytt | Fil | Skåp |
|---|---|---|
| Nuläge: arbetsplats, roll, chef, kollegor, kunder, vad som har hänt | `heartbeat.md` | privat |
| Hur agenter ska jobba med personen, överallt | `soul.md` | privat |
| Hur agenter ska jobba med personen, i det här repot | `soul.md` | repo |
| Vem personen är: värderingar, drivkrafter, sätt att tänka | `identity.md` | privat |
| Professionell profil: kompetens, erfarenhet, arbetssätt | `user.md` | privat |
| Roll i det här projektet | `user.md` | repo |
| Mål, personliga eller i projektet | `objectives.md` | privat eller repo |
| Levererat i projektet | `achievements.md` | repo, överst, med länk till överlämningen |
| Ekonomi, hälsa, familj, relationer | en överlämning till personens privata agent i `sessions/<användare>/<agent>/` i det privata skåpets repo (eller i den lokala mappen) | privat, aldrig i soul-filerna och aldrig i projektrepot |

Repots filer ligger i `users/<användare>/`. De privata ligger där `private:` pekar.

**Regler**
- **Uppdatera och optimera, lägg inte bara till nya rader.** Skriv in det nya där det hör hemma, slå ihop dubbletter, ersätt det som inte längre gäller och stryk det inaktuella. Håll varje fil kort och lätt att läsa. Rättelser och händelser får datum.
- **Agentens metod hör inte hemma i soul.** Rättar personen hur agenten följer sin egen metod, till exempel samtalsguiden eller en mall, är det en brist i agentinstruktionerna. Föreslå en ändring uppströms i stället för att skriva i någons soul.
- **Repots filer delas med teamet.** Skriv aldrig något privat där, och ändra aldrig i någon annans mapp.
- **Privata filer skrivs direkt.** Är skåpet ett repo görs commit och push enligt git-toolet. Är det en lokal mapp sparas filerna bara. Kvittensen visar vad som ändrades.
- Rör bara de filer där något nytt faktiskt har hänt. `heartbeat.md` skapas första gången det finns något att skriva.

## 5. Skills: katalogen och källrepona

Gäller när sessionen skapade, ändrade, flyttade eller tog bort en skill, ett tool eller ett skript.

- **Ändringen ska ligga i källan.** Varje skill har exakt ett källrepo. En ändring som gjordes i en lokal kopia, till exempel `~/.claude/commands`, en adaptermapp eller en synkad `agents/wds/`, flyttas till källrepot. Där görs commit och push. Externa källor ändras uppströms.
- **Katalogen uppdateras.** Har personen en skillskatalog i sitt privata skåp (`skills.md`, och `skills.json` om den finns), lägg in nya skills och källor, och ändra raden för det som flyttats eller tagits bort. Skriv över inget. Uppdatera raden där skillen står.
- **Sprid versionen.** Kör synken enligt katalogen, så att alla repon och den här datorn får den nya versionen.

## 6. Dela

Spara och dela överlämningen, projektloggarna och repots användarfiler enligt git-toolet. De privata filerna delas i sitt eget repo. Commit-meddelandet ska vara `wrap: <session-id> — <en rad>`.

## 7. Andra repon och personlig logg

- **Andra repon i samma session:** skriv en överlämning med **samma session-id** i deras `sessions/<användare>/<till>/`, eller kör deras egen wrap. Varje repo får bara sin egen del. Tack vare samma id kan man hitta sessionen i alla repon.
- **Privat logg:** om `private:` pekar på en mapp på den här datorn, lägg en rad överst i `log.md` där: `- <session-id> <repo> (<från> → <till>): en rad · sessions/<användare>/<till>/<fil>.md`. Skapa filen om den saknas. Är skåpet ett repo delas den där.

## 8. Kvittens

Visa användaren:
- session-id, mottagare och sökväg till överlämningen
- vad som ändrades i soul-filerna, per fil och skåp (repo eller privat), eller "inget nytt"
- den privata överlämningen, om något om ekonomi, hälsa eller familj kom upp
- skills som ändrades: var de ligger nu och att katalogen är uppdaterad
- commit-hash och att push gick igenom

Avsluta med återupptagningskommandot som ett eget kodblock, så att det går att kopiera med ett klick. `<till>` är mottagande agent, `<repo>` är repots mappnamn och tidsstämpeln är sessionens start:

````
```
/<till> <repo> YYYY-MM-DD_HH-MM
```
````
