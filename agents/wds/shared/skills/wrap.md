---
name: wrap
source: wds
description: Avsluta en session. Skriver sessionssammanfattningen, uppdaterar soul, achievements och objectives samt projektloggen, och delar arbetet.
tools: [wds/shared/git]
---

# Wrap: avsluta sessionen

Agentoberoende. Skillen beskriver *vad* som ska göras. Hur git används står i [git-toolet](../tools/git.md).

## 1. Vem, vilken session, vilken mapp

- **Användare:** identifiera enligt git-toolet. Det ger `<användare>`, alltså GitHub-användarnamnet med små bokstäver.
- **Session-id:** `YYYY-MM-DD_HH-MM-<användare>`, med svensk lokaltid vid **sessionens start**. Agenten noterade tiden vid start (se AGENTS.md). Om den inte gjorde det: använd tiden för sessionens första commit, och annars tiden nu.
- **Mapp:** om en agentpersonlighet var aktiv (saga, freya, mimir, ivonne …) blir det `<personlighet>`. Annars blir det modellnamnet med små bokstäver och bindestreck, till exempel `claude-opus-5-5`. Personligheten gäller oavsett vilken modell som kördes.
- **Vad:** ta reda på vad som ändrats enligt git-toolet. Med det och samtalet framför dig: vilka projekt rördes, vad blev klart och vad återstår?

## 2. Sessionssammanfattning

Skriv `users/<användare>/sessions/<mapp>/YYYY-MM-DD_HH-MM-<mapp>-summary.md`:

```markdown
---
session: YYYY-MM-DD_HH-MM-<användare>
start: YYYY-MM-DDTHH:MM+02:00
slut: YYYY-MM-DDTHH:MM+02:00
user: <användare>
agent: <personlighet eller tom>
model: <modell-id>
tool: <claude|copilot|codex|...>
projects: [<projekt>, ...]
repos: [<repo>, ...]
---

## Gjort
- ...

## Kvar
- ...

## Nästa steg
Konkret första åtgärd för den som tar över, vem det än är.

## Filer
- [relativ/sökväg](../../../../relativ/sökväg)
```

Håll den kort. Den ska kunna läsas på en minut. `projects: []` om sessionen inte rörde något specifikt projekt.

## 3. Överlämning till en agent: när vi inte vet vem som kör

Om nästa steg hör till en viss agent (saga, freya, mimir …) men det inte är självklart vilken person som kör den, skriv en överlämning i `users/_handovers/<agent>/YYYY-MM-DD_HH-MM-<mapp>-till-<agent>.md`:

```markdown
---
från: <session-id>
från_agent: <mapp>
till: <agent>
projekt: <projekt eller tom>
status: öppen
tagen_av:
---

## Uppdrag
En mening: vad agenten ska åstadkomma.

## Läge
Det mottagaren behöver veta: underlag, beslut, vad som finns och saknas. Länka i stället för att upprepa.

## Nästa
Konkreta steg i ordning.
```

- `_handovers` har understreck och kan därför aldrig krocka med ett GitHub-användarnamn.
- Länka överlämningen från sammanfattningen (Nästa steg) och från projektloggen.
- Överlämningar raderas aldrig. Mottagaren ändrar `status` (se AGENTS.md, sessionsstart).
- **Tog sessionen själv en överlämning?** Sätt `status: klar` i den filen om uppdraget är gjort, annars låt den stå som `tagen` och skriv läget i sammanfattningen.

## 4. Projektloggen: teamets gemensamma tidslinje

För varje projekt som rördes: lägg en rad **överst** i `projects/<projekt>/design-process/_progress/design-log.md`:

```markdown
## YYYY-MM-DD_HH-MM-<användare> (<mapp>)
- En till tre punkter om vad som hände i projektet. [Session](../../../../users/<användare>/sessions/<mapp>/<fil>.md)
```

## 5. Användarfilerna

I `users/<användare>/`. Varje punkt ska ha datum. **Skriv inget privat**, eftersom filerna är delade med teamet. Ändra aldrig i någon annans mapp. Rör bara de filer där något nytt faktiskt hänt.

| Vad som hände | Fil | Rubrik |
|---|---|---|
| Personen rättade agenten: vad som var fel, hur det ska vara | `soul.md` | Rättelser |
| Personen uppskattade eller avvisade något | `soul.md` | Uppskattat / avvisat |
| Något blev klart och levererat | `achievements.md` | överst, med länk till sammanfattningen |
| Ett mål tillkom, ändrades eller nåddes | `objectives.md` | uppdatera listan |
| Rollen i projektet ändrades | `user.md` | Roll |

Något som gäller personen **överallt**, inte bara i det här repot, hör hemma i personens privata soul-fil (`private:` i `user.md`). Föreslå det för personen i stället för att skriva det här.

## 6. Dela

Spara och dela sammanfattningen, eventuell överlämning, projektloggarna och användarfilerna enligt git-toolet. Commit-meddelandet ska vara `wrap: <session-id> — <en rad>`.

## 7. Andra repon och personlig logg

- **Andra repon i samma session:** skriv en sammanfattning med **samma session-id** i deras `users/<användare>/sessions/<mapp>/`, eller kör deras egen wrap. Varje repo får bara sin egen del. Tack vare samma id kan man hitta sessionen i alla repon.
- **Privat logg:** om `user.md` har `private:` och repot finns på datorn, lägg en rad där med session-id, repo och länk. Dela där också.

## 8. Kvittens

Visa användaren:
- session-id och sökväg till sammanfattningen
- eventuell överlämning: till vilken agent och sökväg
- vad som lades till i användarfilerna, eller "inget nytt"
- commit-hash och att push gick igenom
