# Produktion och template (utkast 2026-10-27)

Mårten, 2026-10-27: stilfångsten handlar om hur en produktion ska göras. Den kopplas till en **produktion**, och varje typ av projekt och stilguide sparas som en **template** som är kopplad till produktionen och kan kopieras.

## Begreppen

| Begrepp | Vad det är | Exempel |
|---|---|---|
| **Produktion** | En film (eller en serie filmer) som görs för en kund: brief, manus, material, klipp, leverans. | "Där vill jag också vara med" för Visitas certifieringswebb |
| **Template** | Hur en sorts produktion görs, färdig att kopiera: produktionstypen (gången, slagen, längden, avstämningarna) och stilguiden (looken, tempot, typen, ljudet, mätt ur förebilder och kundens profil), med reglerna som kommit ur tidigare produktioner. | `eventfilm-varm`, `kundcase-lugn`, `dokumentar-snabb`, `talat-ord` |
| **Stilfångst** | Sättet en stilguide blir till: förebilder mäts ruta för ruta och siffrorna skrivs in i templaten. | Tre reels mäts och blir `dokumentar-snabb` |

## Hur de hänger ihop

```
template  ──kopieras──▶  produktion  ──anteckningar──▶  (lyfts tillbaka på ja)  ──▶  template, ny version
```

1. **En ny produktion börjar med en kopia av en template.** Viska föreslår templaten ur briefen (typ, kanal, kundens profil); personen säger ja eller väljer en annan. Kopian ligger i produktionen, med vilken template och version den kom från.
2. **Produktionen äger sin kopia.** Det som ändras under arbetet (en regel, en siffra, ett typsnitt) ändras i produktionens kopia, med datum och personens ord. Andra produktioner påverkas inte, och en pågående produktion ändras inte när templaten senare ändras.
3. **Det som ska gälla framåt lyfts tillbaka.** Vid leverans visar Viska vilka anteckningar som borde gälla fler produktioner, och de förs in i templaten som en ny version på personens ja.
4. **En ny template görs** genom stilfångst (två eller tre förebilder mäts), eller genom att en lyckad produktion sparas som template ("spara den här som `kundcase-lugn`").

## Var de ligger (förslag)

**Templates finns på två nivåer**, som brand och designsystem i WDS:

| Nivå | Var | Vad |
|---|---|---|
| WDS | `agents/wds/viska/templates/<template>/` | Allmänna produktionstyper och stilar som alla kunder kan använda |
| Kund | `<kundens repo>/brand/templates/<template>/` | Kundens egna, byggda på kundens profil och förebilder; går före WDS-nivån |

**En template:**

```
<template>/
  <template>.md        vad den är för, produktionstypen (gång, slag, längd, avstämningar), när den passar och inte
  stil.md              stilguiden: siffrorna (klipptakt, bildlängder, rörelse, färg, typ, text mot ord, övergångar, ljudnivåer) och reglerna
  film.yaml            skelettet: slagen med roller och längder, spåren, musikens plats, ljudnivåer
  anteckningar.md      regler ur tidigare produktioner: datum, personens ord, regeln, vad som ändrades
  forebilder.md        förebilderna som mättes: titel, länk, längd, datum; klippprotokollen per förebild (aldrig själva filmerna)
  grafik/              grafiken som HyperFrames-komponenter i stilen (kort, namnskylt, slutkort), läser kundens designsystem
  version              t.ex. 3 (2026-10-27)
```

**En produktion** (i projektets repo, mediet på den delade enheten som nu):

```
projects/<projekt>/produktioner/<produktion>/
  <produktion>.md      produktionens själ: brief, krafter, beslut och avstämningar med datum
  template/            kopian av templaten (med `fran.md`: vilken template, vilken version, när)
  film.yaml            manus och klipplista, börjar som templatens skelett
  manus.md, storyboard.html, behov.md, rattigheter.csv
```

## Vad som ändras i Viska

- `film-production`: steg 2 väljer och kopierar templaten; mappen heter `produktioner/` i stället för `film/`.
- Ny skill `style-capture`: förebilder → mätningar → `stil.md`, `forebilder.md` och en provproduktion.
- `film-assembly` och `motion-graphics` läser reglerna ur produktionens kopia av templaten, inte ur sig själva; kontrollerna räknar mot `stil.md`.
- Vid leverans: förslag på vilka anteckningar som lyfts till templaten.
- `talat-ord` (motion-sessionens template) och provfilmens upplägg blir de första templates i den nya formen.

## Öppna frågor

1. Två nivåer (WDS och kund), eller bara en?
2. Mappnamnet `produktioner/` i projektet, eller något annat?
3. Ska produktionstyp och stilguide kunna kombineras fritt (eventfilm × varm stil), eller är en template alltid ett par?
