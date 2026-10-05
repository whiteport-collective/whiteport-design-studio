# Repostrukturen: mappar med en ägare

**Status: riktning (2026-10-03).** Prövas i visita-kommunikation. Det som står under Öppet är inte bestämt.

## Mönstret

Roten består av mappar som går att droppa in. Varje toppmapp är en *sorts* sak, och varje undermapp har *en ägare*.

| Toppmapp | Undermapp = ägare | Exempel |
|---|---|---|
| `agents/` | källan | `agents/wds/`, `agents/web247/`, `agents/martenangner/` |
| `governance/` | källan för policyn | `governance/wds/`, `governance/visita/` |
| `projects/` | projektet | `projects/enkarriartack/` |
| `users/` | personen | `users/martenangner/` |
| `sessions/` | personen och agenten | `sessions/martenangner/saga/` |

Tre regler:

1. **En mapp har en ägare.** Den byts ut som en helhet och kan droppas in i ett annat repo.
2. **Synken kopierar mappar, inte filer.** Den äger en synkad mapp helt och får därför också ta bort det som försvunnit i källan.
3. **Man läser genom en platt vy**, inte genom mappträdet: `AGENTS.md`, policylistan i `governance/` och planens vyer. Lagringen följer ägaren, och vyn visar allt längs den dimension man behöver.

## En källa inne i `agents/`

Varje källa har samma form, oavsett om det är WDS, en organisation eller en person:

```
agents/<källa>/
├── <agent>/      en mapp per agent: instructions.md, references/, subagents/
├── skills/       alla källans skills
├── tools/        alla källans tools
└── data/         gemensamt underlag och mallar
```

- **Alla agenter kan använda alla skills**, från alla källor i repot. `used_by:` i en skill säger vilka agenter som brukar köra den. Det är en beskrivning, inte en behörighet.
- En källa utan agenter är ett rent skillbibliotek.
- Exempel: `agents/wds/` (Idun, Saga, Freya, Mimir), `agents/visita/` (Vinka och Visitas skills), `agents/martenangner/` (Ivonne och Mårtens egna skills).

## Märkning

- **Understreck bara för arbetsmaterial** i ett projekt, som `_progress/` bredvid `A-Product-Brief/`. Det betyder "maskineri, inte leverans".
- **Inga understreck på toppmapparna.** De är innehåll som människor öppnar varje dag, och `_` säger "rör inte". Astro och Jekyll hoppar dessutom över `_`-mappar.
- **En synkad kopia märks med en fil i mappen**, inte med mappnamnet. Samma mapp är källa i ett repo och kopia i ett annat, och sökvägarna måste vara desamma överallt. Filen heter `.source` och anger `source: <repo>@<sha>`, för både `agents/wds/` och `governance/`. `.wds-sync` betyder bara att repot vill ha WDS.
- **Ingen gemensam `_wds/`.** Kundens projekt, policy och användare är inte WDS:s, och bara det som WDS äger ligger i WDS-mappar.

## Governance

```
governance/
├── policies.md      den platta listan: alla policyer i läsordning
├── wds/             WDS standardpolicy, synkad och skrivskyddad
├── <org>/           organisationens policy, källan i ett repo, speglas till organisationens andra repon
└── <projekt>/       skärpningar som bara gäller ett repo, vid behov
```

- En synkad mapp är en spegel av källan och har en fil `.source` (`source: <repo>@<sha>`). Den ändras aldrig på plats. Se [sync-toolet](../tools/sync.md#governance-policy).
- Där Idun inte har satt upp governance finns ingen `governance/`-mapp.

- Säger två nivåer olika gäller den strängare. En lägre nivå får skärpa men aldrig mildra en högre.
- Agenter rapporterar incidenter och föreslår nya punkter vid varje wrap ([wrap steg 6](../skills/wrap.md#6-gc-incidenter-och-förslag)). De får skärpa men aldrig mildra eller vidga sitt eget mandat.

## Uppgifter

Uppgifterna följer sin ägare. Ingen toppmapp för todos.

| Ägare | Plats |
|---|---|
| Projektet | `projects/<projekt>/_progress/plan.md` |
| Personen | `users/<användare>/`, eller personens privata skåp |

En persons lista är en vy, inte en egen fil: personens egna uppgifter plus alla planers uppgifter där personen står som ansvarig. GTD-kontexterna (@phone, @computer) är ett filter på var uppgiften görs. Formatet prövas fritt i Visita innan det blir standard.

## Två uppsättningar

| Uppsättning | När | Exempel |
|---|---|---|
| **Delad:** verksamhetens repo plus kodrepon | en avdelning med flera projekt, där koden ägs av någon annan | en kommunikationsavdelning och byrån som bygger sajten |
| **Samlad:** WDS och kod i samma repo | ett team som både designar och bygger, eller ett mindre projekt | en webbyrås eget repo |

- **Delad:** hela avdelningen delar ett repo för WDS och agentiskt arbete. Alla ser vad som händer, material delas i stället för att kopieras, och silos uppstår inte. G&C-policyerna gör det säkert genom att styra hur agenterna hanterar andras material.
- **Samlad:** samma rotmappar, och koden ligger i en egen mapp som `app/` eller `src/`.
- I båda fallen anger projektet på ett ställe var koden ligger, så att Mimir vet var han ska bygga.

## Öppet

- Ska personens uppgifter bara ligga i det privata skåpet, eller också i `users/<användare>/` i varje repo?
- Vilken uppsättning ska WDS rekommendera en ny kund?
- Var anger projektet kodens plats: i `AGENTS.md`, i produktbriefen eller i en egen fil?
