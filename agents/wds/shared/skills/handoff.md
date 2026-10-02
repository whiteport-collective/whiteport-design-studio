---
name: handoff
source: wds
description: Lämna över en avgränsad uppgift till en annan agent eller person mitt i sessionen. Samma överlämningsfil och återupptagningskommando som wrap, men sessionen fortsätter.
tools: [wds/shared/git]
---

# Handoff: lämna över en uppgift

En handoff är en överlämning utan wrap. Den lämnar **en** uppgift till någon annan, och sessionen fortsätter. Allt annat följer [wrap](wrap.md), så att mottagaren tar en handoff på samma sätt som en wrap: med återupptagningskommandot.

**Användning:** `/handoff <till> [person]`, till exempel `/handoff mimir` eller `/handoff wera camilla`.

Fråga ingenting. Ta allt ur samtalet.

## 1. Vem, vilken session, till vem

Som [wrap steg 1](wrap.md#1-vem-vilken-session-till-vem): användare, session-id, från, projektrot och sessionsmapp.

- **Till:** agenten i argumentet. Saknas det: strategi → saga, design → freya, bygge → mimir.
- **Person:** samma person som standard. En annan person om argumentet säger det, och `all-users` om vi inte vet vem som kör.

## 2. Överlämningen

Samma filnamn, mapp och format som [wrap steg 2](wrap.md#2-överlämningen), med `status: öppen`. `<sammandrag>` beskriver uppgiften, inte sessionen.

Innehållet gäller bara uppgiften:

- **Gjort:** det som redan är klart av uppgiften, och de beslut den vilar på.
- **Kvar:** det som återstår.
- **Nästa:** konkreta steg i ordning, så att mottagaren kan börja direkt.
- **Filer:** relativa länkar till allt mottagaren behöver.

## 3. Dela

Spara och dela bara överlämningsfilen enligt git-toolet. Commit-meddelandet är `handoff: <session-id> → <till> — <en rad>`. Soul-filer, projektlogg och skills lämnas till wrap.

## 4. Kvittens

Visa mottagare och sökväg. Avsluta med återupptagningskommandot som ett eget kodblock, i samma format som [wrap steg 8](wrap.md#8-kvittens):

````
```
/<till> <repo> YYYY-MM-DD_HH-MM <sammandrag>
```
````

Fortsätt sedan sessionen där den var.
