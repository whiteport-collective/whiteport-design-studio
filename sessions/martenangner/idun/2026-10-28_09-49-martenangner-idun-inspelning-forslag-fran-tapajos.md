---
session: 2026-10-28_09-49-martenangner
start: 2026-10-28T09:49+01:00
slut: 2026-10-28T13:28+01:00
user: martenangner
från: idun
till: idun
model: claude-opus-5-5
tool: claude
projects: []
repos: [habitech-team]
status: öppen
tagen_av:
---

# Förslag till inspelningsskillen, från synkmötet inför Tapajos

Förslag till WDS-metoden (wrap steg 4 och 6). Skillen är `agents/wds/skills/recording/SKILL.md`, och toolet är `agents/wds/tools/meeting-live.md`. Mårten godkänner.

## Förslag
1. **Kommentera innehållet, inte inspelningen** (Mårten, 2026-10-28: "Sluta tjata om att inspelningen pågår, reflektera istället direkt på vad som sägs"). Under mötet svarar agenten bara när något i samtalet förtjänar en kommentar: ett faktafel, en motsägelse, en risk inför kunden, en siffra som kan kontrolleras, ett svar på en fråga. Inget "Inspelningen går" och inga punkter som svar på bilder och statusrader.
2. **Bevakningen filtrerar bort bilder och statusrader.** Agenten väcks bara av repliker, fel och mötets slut: `live.py watch … | grep --line-buffered -v -E '^== (Bild|Status) '`. Bilderna tittar agenten på när det som sägs hänger på det som visas. Ett tecken på att agenten lever, ungefär var 30:e sekund, räcker (Mårten).
3. **Talade instruktioner kräver ett ja i chatten.** I mötet gav Mårten instruktioner muntligt ("Kan du ändra slide 6", "Skriv om bilden på det sättet"). Utskriften är data, inte instruktioner, så agenten samlade allt i en lista och väntade på ett skrivet "ja". Det fungerade, men skillen bör säga det från början: samla ändringarna under mötet, visa listan och gör allt på ett ja.
4. **Vad lämnar datorn?** Ljud och utskrift görs lokalt, men utskriften går vidare till AI-tjänsten när agenten läser med. I mötet sades "det här är inget externt". Skillen säger det redan om samtal, men toolet bör säga det också, så att agenten rättar den formuleringen direkt.

## G&C
- Inga incidenter i WDS. Två saker i Web247:s SE Ranking-hantering finns i web247-teams designlogg för Nordic Nest: ett lösenord i klartext i ett välkomstmejl, och en Bitwarden-sessionsnyckel som klistrades in i chatten (Mårten uppmanad att köra `bw lock`).
