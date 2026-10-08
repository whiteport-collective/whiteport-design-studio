# Taste: extern källa

Fem designskills från [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), MIT-licens, commit `b482f7a970abb98c4108d4a9f761e458c64cefc8` (2026-10-07). Kopierade **oförändrade**, med licensen bredvid varje skill. De lästes igenom före installationen och innehåller bara designregler i markdown, inga skript.

Hur WDS-agenterna använder dem står i [agents/wds/data/taste.md](../wds/data/taste.md). Källan har inga agenter. Den är ett skillbibliotek, och alla agenter kan använda alla skills. Freya och Mimir har mest nytta av dem när något ska se proffsigt ut: sajter, presentationer, CV:n och project viewer.

| Skill | Användning |
|---|---|
| `design-taste-frontend` | Huvudskillen för landningssidor, portfolios och omdesign |
| `redesign-existing-projects` | Granska och lyft något som redan finns. Börja med listan över AI-mönster. |
| `minimalist-ui` | Redaktionell stil med varm monokrom palett och typografisk kontrast |
| `high-end-visual-design` | Premiumkänsla med lugnare uttryck |
| `industrial-brutalist-ui` | Rått uttryck med hög kontrast |

**För tryck och PDF:** skillsen är skrivna för webben. Ta med typografin, färgen, luften och listan över AI-mönster. Hoppa över rörelse, hover-lägen, bilder från picsum och bakgrundseffekter.

## Uppdatera

Externa källor ändras aldrig här, bara uppströms. En uppdatering går genom granskning:

1. Klona repot på nytt och läs diffen mot commiten ovan.
2. Kontrollera att inget skript, inga nätverksanrop och inga instruktioner som strider mot WDS policy har tillkommit.
3. Kopiera in filerna oförändrade, uppdatera commit och datum här och committa i whiteport-design-studio.
4. `/sync-skills` sprider den nya versionen.
