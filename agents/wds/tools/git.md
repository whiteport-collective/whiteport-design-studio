---
name: git
source: wds
description: Hur agenter använder git. Identifierar användaren, visar vad som ändrats, gör commit och push.
used_by: [agent-space-install, folder-presentation, handoff, install-wds, librarian, live-meeting, org-onboarding, product-brief, project-setup, recording, trigger-map, user-onboarding, wrap, film-production]
---

# Tool: git

Används av skills som behöver veta vem som jobbar, vad som ändrats eller som ska spara arbete.

## Vem är användaren

Användaren identifieras av sitt **GitHub-användarnamn med små bokstäver**. Det är också mappnamnet i `users/`.

0. **Läs `.wds/me.md` i repots rot.** Den är gitignorerad, en per dator, och fältet `user:` är svaret.
   - Saknas den men `~/.wds/me.md` finns i hemmappen: kopiera den till `.wds/me.md` och kontrollera att `.wds/` står i `.gitignore`.
   - Saknas båda: gå vidare till steg 1–3 och skapa sedan `~/.wds/me.md` och `.wds/me.md` med `github`, `user`, `name`, `email` och `private` (sökvägen på den här datorn till personens privata soul-filer, eller tom).
1. Om GitHub CLI finns:
   ```bash
   gh api user --jq .login
   ```
   Gör om svaret till små bokstäver. `MartenAngner` blir `martenangner`.
2. Annars:
   ```bash
   git config user.email
   ```
   Matcha mot `email:` i `users/*/user.md`. Mappnamnet är användaren.
3. Ingen träff: fråga efter GitHub-användarnamnet och kopiera `users/_template/` till `users/<namn>/`. Be personen kontrollera att `git config user.email` är rätt adress.

## Vad har ändrats i sessionen

```bash
git status --short                    # osparat
git log --oneline --since="8 hours"   # sessionens commits
git diff --stat HEAD                  # omfattning
```

## Spara och dela

```bash
git add <sökvägar>
git commit -m "<typ>: <session-id> — <en rad>"
git pull --rebase
git push
```

- `<typ>` är till exempel `wrap`, `brief`, `design` eller `fix`.
- En skill eller ett tool committas alltid för sig: `skill(<namn>): <vad och varför>` eller `tool(<namn>): <vad och varför>`, med bara den filen och dess skript.
- Lägg till specifika sökvägar, inte `git add -A` i blindo. Kolla `git status` först.
- **Räkna med parallella sessioner.** Flera agenter jobbar ofta i samma repo samtidigt, särskilt där det finns en `sessions/`-mapp eller en öppen överlämning. Kolla `git reflog -5` och `git log --oneline -5` efter färska commits från en annan session innan du gör commit.
- **Laga framåt.** Ett eget misstag rättas med en ny commit. Aldrig `reset`, `commit --amend`, kedjor av `revert` eller `checkout -- <fil>` för att ångra: en annan sessions commit eller osparade ändring kan landa sekunder före och försvinna. Fråga innan något kommando som skriver om historik.
- **Om `pull --rebase` krockar:** stanna och visa konflikten för användaren. Lös den inte på egen hand i någon annans filer.
- **Om `push` misslyckas:** säg det rakt ut med felmeddelandet. Påstå aldrig att något är pushat utan att ha sett det gå igenom.
- Kvittera med commit-hash: `git log --oneline -1`.
- **Före en granskning:** gör commit och push innan du ber en annan agent (Codex, en annan session) granska eller ta över. Den läser repot och ser inte det som bara finns lokalt.

## Aldrig

- `git push --force`, `git reset --hard` eller att skriva om historik som redan är pushad
- `reset`, `commit --amend` eller `checkout -- <fil>` i ett repo där en annan session kan vara igång
- Commit av hemligheter som `.env`, nycklar eller lösenord
