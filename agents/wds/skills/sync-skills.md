---
name: sync-skills
source: wds
description: Synkar skills, agenter och policy mellan WDS-repot, personens privata repo, projektrepona och datorns .claude-mapp. Körs efter en ändring i en skill, efter byte av dator och när något saknas.
tools: [wds/sync]
---

# Sync skills: samma version överallt

Varje skill har exakt ett källrepo. Synken ser till att alla platser där den används har den senaste versionen:

| Från | Till | Vad |
|---|---|---|
| WDS-repot | varje WDS-repo på datorn | `agents/wds/`, adaptrarna (`.claude/commands/`, `.github/`, `.agents/skills/`) och `governance/wds/` där governance är uppsatt |
| en organisations källrepo | organisationens andra repon | `governance/<org>/` |
| WDS-repot och personens privata repo | datorns `~/.claude/commands/` | pekare till agenterna och skillsen, så att `/saga`, `/idun` och personens egna kommandon fungerar i alla repon |

Vilka källor som gäller för personen står i personens katalog, `skills.json` i det privata skåpet. Idun skapar den vid installationen.

**Användning:** `/sync-skills`, `/sync-skills dry-run` (visa bara) eller `/sync-skills no-pull` (hoppa över git pull).

## 1. Fråga först

En riktig synk skriver i andra repon än det sessionen arbetar i. Kör den därför bara när personen har sagt ja, eller efter en torrkörning som personen har sett. Okända flaggor startar aldrig en synk.

## 2. Kör

Kör synken enligt [sync-toolet](../tools/sync.md).

## 3. Kvittens

Sammanfatta kort:
- antal skills per källa
- repon som uppdaterades, och repon som hoppades över, med skäl
- **lokalt ändrade** kommandon: de har redigerats direkt i `~/.claude/commands/` och sparats undan. Erbjud att flytta ändringen till källrepot.
- **krockar:** samma kommando från flera källor. Föreslå vilken källa som ska äga det.
- governance: vad som speglades, och om en konfliktkontroll behövs

Påminn om att nya kommandon syns i nästa session.
