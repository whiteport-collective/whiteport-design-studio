# Template: talat-ord

Ord ur det som sägs, lyfta på kundens kort ovanpå en reel eller ett talat klipp, och ett slut där ett riktigt foto står bredvid avsändaren. Hantverket bakom står i skillen [motion-graphics](../../../skills/motion-graphics/SKILL.md); här står vad den här filmtypen har bestämt. Byggs med [hyperframes](../../../tools/hyperframes.md) (`film.py build`).

**Passar:** en reel eller ett kort klipp där någon förklarar något (kocken om smöret, en talare, en intervju), 10–30 s, stående eller liggande. **Passar inte:** en film utan tal, eller en längre förklaring med kapitel.

## Filerna

| Fil | Vad |
|---|---|
| `index.html` | Filmen: markeringar som `film.py` fyller, rörelsen och rollerna. Inga färger eller typsnitt av egen |
| `template.md` | Den här: beslut, roller, `film.json` och rättelser |

## Looken kommer ur kunden

Templaten läser två filer ur kundens `brand/design-system/`: `tokens.css` (kundens tokens, som allt annat byggs med) och `film.css`, där designsystemet översätts till bild. `film.css` skrivs en gång per kund, av Viska tillsammans med den som äger designsystemet, och ändras där, aldrig i en film. Rollerna:

| Roll | Vad den styr |
|---|---|
| `--film-ground` | Slutets mark |
| `--film-ink` | Text på kortet och på marken |
| `--film-card` | Kortet bakom orden |
| `--film-accent` | Linjen och den förskjutna skuggan, kundens accent: en färgfamilj |
| `--film-accent-ink` | Accenten som text på marken |
| `--film-on-plate` | Text direkt på bild, om en framtida variant behöver den |
| `--film-font`, `--film-heavy`, `--film-text` | Kundens typsnitt, vikten för lyfta ord och för vanlig text |
| `--film-shadow`, `--film-radius`, `--film-line` | Skuggans förskjutning, hörnen och linjens tjocklek |
| `--film-margin`, `--film-size-word`, `--film-size-then`, `--film-size-end`, `--film-logo` | Marginal och storlekar i bildpunkter för formatet |

Typsnitt som inte finns på datorn (Visitas National 2 är licensierat) läggs med `@font-face` i `film.css`, med kundens fil eller `local()`, och faller annars tillbaka på det som står efter i listan.

## `film.json`

```json
{
  "template": "talat-ord",
  "brand": "<repo>/brand/design-system",
  "plate": "plate.mp4", "words": "plate.words.json",
  "fps": 25, "width": 1080, "height": 1920, "duration": 15,
  "cuts": [3.9, 8.9, 12.0],
  "beats": [
    { "ord": "60 grader", "y": 0.60 },
    { "ord": "långsamt", "linje": "långsamt", "sedan": "men under längre tid", "till": 9.5, "y": 0.66 }
  ],
  "end": { "at": 12.0, "photo": "gruppbild.jpg", "focus": "50% 62%", "title": "Studiebesök i Stockholm",
           "sub": "22 oktober 2026", "logo": "visita-logo.svg" },
  "belagt": [ { "text": "22 oktober 2026", "kalla": "inspelningen 2026-10-22-koket" } ]
}
```

- **`ord`** är en fras ur transkriptet, ordagrant; finns den inte stoppar bygget. Rutan landar två bildrutor innan frasens första ord hörs.
- **`linje`** ritar en linje under rutan i exakt den tid ordet tar att säga. **`sedan`** lägger det som sägs efteråt på en lägre rad, ord för ord i talets takt.
- **`till`** är när rutan lämnar bilden; utan den lämnar den med nästa klipp i `cuts`. En sekund över klippet är tillåten när raden behöver läsas klart.
- **`end`** reser kundens mark bakom linjen strax före `at`; fotot ritas fram uppifrån och lever till sista bildrutan. Siffror i slutet måste stå i `belagt` med källa.
- `y` är rutans höjd i bilden (0–1); lägg den under ansiktet och över det som bevisar.

## Beslut

- **Hörnetiketter och räknare: nej.** Motionmaxxing förbjuder dem, Jamie Fenns regel 4 vill ha dem som orientering. I den här filmtypen tillhör de första sekunderna det som sägs, och 15 sekunder har inga kapitel att räkna. Orienteringen (var, när, avsändaren) står en gång, i slutet bredvid fotot. En siffra visas bara som den sägs, aldrig som en räknare som rullar upp till den.
- **Ord på kort, inte lös text.** Lös vit text försvann mot den gula skärbrädan i provet; kortet håller kontrasten utan glöd eller mörk gradient.
- **En ruta i taget**, högst två i en reel på 15 s, och ingen på bilden som bevisar (snittet).
- **Slutet är kundens mark med ett riktigt foto**, inte ett logotypkort: titeln, datumet och märket bredvid en bild från dagen.

## Provet

Samma brief (Visita, kocken om smöret, 15 s, 9:16) i tre varianter, 2026-10-25. Filmerna, kontaktarken och briefen ligger på Visitas delade enhet i `projects/2026-10-21-studiebesok-stockholm/resolve/motion-prov/`, inte i repot: det här repot är publikt och materialet visar riktiga personer.

| Variant | Vad som syntes |
|---|---|
| Utan skill | Textremsa genom hela filmen plus rubrikrutor ovanpå: två till tre grafiker samtidigt. En räknare rullade 55°, 57°, 60°, alltså värden kocken aldrig sa. Egen rubrik ("Köttet vilar i smör") och en överrubrik i hörnet. Korall bredvid grönt: två färgfamiljer. Visitas skugga och raka hörn fanns med. |
| HyperFrames + motionmaxxing | Återhållsam: ett ord eller en siffra i taget, landar på talet, inget i hörnen, och slutet rör sig till sista bildrutan. Men lös vit text över bild behövde en mörk gradient, "60°" är en omskrivning av "60 grader", och looken blev en generisk Inter-film snarare än Visitas. Kunskapen om tider, kurvor och mätbara grindar är det värdefulla. |
| talat-ord | Samma återhållsamhet, men i Visitas formspråk (vitt kort, grön förskjuten skugga, raka hörn), orden ordagrant ur talet, linjen som ritas i talets takt under "långsamt", och slutet som reser sig bakom linjen i stället för att tona. Byggstoppet för påhittade siffror och fraser som inte sägs. |

Motionmaxxings mätskript på de tre renderingarna: sidkrom (G5) underkänd utan skill (en rad i kanten och ett vänsterställt rubrikblock), godkänd för de två andra. Stillastående slut (G3) 1,8 s utan skill, 1,2 s för de två andra efter rättelsen nedan. talat-ord får ändå G3-anmärkningen att sista "klippet" är 41 % av filmen: slutet kommer med en mark som reser sig, inte ett klipp, och det är med flit.

## Rättelser

Varje rättelse skrivs här med namn och datum och byggs in i `index.html` eller kundens `film.css`, så att nästa film får den.

- 2026-10-25 (prov): bokstavsavstånd animeras inte (HyperFrames hackar på det); en linje under ordet bär tiden i stället.
- 2026-10-25 (prov): klippbanan (`clip-path`) måste ha samma enheter i start och slut, annars hoppar GSAP direkt till slutläget.
- 2026-10-25 (prov): lös vit text under "långsamt" försvann mot den gula skärbrädan; raden ligger nu på kundens kort.
- 2026-10-25 (prov): fotot i slutet planade ut och bilden stod still 1,7 s; nu rör det sig i jämn takt och märket landar sist, så att raden får sina 2 s och bilden står still högst 1,4 s.
- 2026-10-25 (prov): kundens typsnitt blev Arial i renderingen när CSS:en var länkad; `film.py` lägger nu in den i sidan.
