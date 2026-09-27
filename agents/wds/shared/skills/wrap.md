---
name: wrap
source: wds
description: Avsluta en session. Skriver överlämningen (till samma eller en annan agent), uppdaterar soul, achievements och objectives samt projektloggen, och delar arbetet.
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

Varje wrap är en överlämning. Mappen är **mottagarens**, filnamnet slutar med **avsändaren**:

| Mottagare | Sökväg |
|---|---|
| Samma person, samma agent (vanlig wrap) | `sessions/<användare>/<från>/YYYY-MM-DD_HH-MM-<från>.md` |
| Samma person, annan agent | `sessions/<användare>/<till>/YYYY-MM-DD_HH-MM-<från>.md` |
| Känd annan person | `sessions/<person>/<till>/YYYY-MM-DD_HH-MM-<från>.md` |
| Vi vet inte vem som kör | `sessions/all-users/<till>/YYYY-MM-DD_HH-MM-<från>.md` |

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

## 4. Användarfilerna

I `users/<användare>/`. Varje punkt ska ha datum. **Skriv inget privat**, eftersom filerna är delade med teamet. Ändra aldrig i någon annans mapp. Rör bara de filer där något nytt faktiskt hänt.

| Vad som hände | Fil | Rubrik |
|---|---|---|
| Personen rättade agenten: vad som var fel, hur det ska vara | `soul.md` | Rättelser |
| Personen uppskattade eller avvisade något | `soul.md` | Uppskattat / avvisat |
| Något blev klart och levererat | `achievements.md` | överst, med länk till överlämningen |
| Ett mål tillkom, ändrades eller nåddes | `objectives.md` | uppdatera listan |
| Rollen i projektet ändrades | `user.md` | Roll |

Något som gäller personen **överallt**, inte bara i det här repot, hör hemma i personens privata soul-fil (`private:` i `user.md`). Föreslå det för personen i stället för att skriva det här.

## 5. Dela

Spara och dela överlämningen, projektloggarna och användarfilerna enligt git-toolet. Commit-meddelandet ska vara `wrap: <session-id> — <en rad>`.

## 6. Andra repon och personlig logg

- **Andra repon i samma session:** skriv en överlämning med **samma session-id** i deras `sessions/<användare>/<till>/`, eller kör deras egen wrap. Varje repo får bara sin egen del. Tack vare samma id kan man hitta sessionen i alla repon.
- **Privat logg:** om `user.md` har `private:` och repot finns på datorn, lägg en rad där med session-id, repo och länk. Dela där också.

## 7. Kvittens

Visa användaren:
- session-id, mottagare och sökväg till överlämningen
- vad som lades till i användarfilerna, eller "inget nytt"
- commit-hash och att push gick igenom
