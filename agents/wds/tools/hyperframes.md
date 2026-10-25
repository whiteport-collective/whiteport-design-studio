---
name: hyperframes
source: wds
type: cli
description: Renderar rörlig grafik skriven som HTML och GSAP till video med HyperFrames (npx, ingen global installation, ingen MCP), och bygger filmen ur en Viska-template med film.py. Skriptet ligger i hyperframes/.
used_by: [motion-graphics, film-assembly]
---

# Tool: hyperframes

[HyperFrames](https://github.com/heygen-com/hyperframes) (HeyGen, Apache 2.0) renderar en HTML-sida till video genom att stega en pausad GSAP-tidslinje bild för bild i Chrome, så att varje rendering blir likadan. Viska skriver aldrig sidan för hand: [film.py](hyperframes/film.py) bygger den ur en template i `agents/wds/viska/templates/` och kundens `brand/design-system/`. Vad som är bra grafik står i skillen [motion-graphics](../skills/motion-graphics/SKILL.md).

## Installera

Kräver Node 22+, [ffmpeg](ffmpeg.md) och Python 3. Inget installeras globalt: CLI:t körs med `npx` och en låst version, och hämtar Chrome (headless shell) till `~/.cache/puppeteer` första gången. Stäng av telemetrin och skill-installationen i varje skal:

```bash
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1
npx -y hyperframes@0.8.196 doctor          # Node, ffmpeg, Chrome; whisper, Kokoro och Docker behövs inte
```

HyperFrames egna skills (`npx hyperframes skills`, pluginen) installeras inte: de skriver till agentens globala skillmapp, och hantverket finns i motion-graphics. `init` utan `--skip-skills` försöker installera dem; film.py behöver inte `init`.

## Bygga, titta och rendera

```bash
# Bygg filmen ur film.json (se templatens template.md), i en arbetsmapp utanför repot
python agents/wds/tools/hyperframes/film.py build "<klipp>/film.json" "<arbetsmapp>/film"

# Kontrollera (lint, körning, layout, rörelse, kontrast) och titta på bilder
cd "<arbetsmapp>/film"
npx -y hyperframes@0.8.196 check --json 2>/dev/null          # stderr har förloppet, stdout är JSON
npx -y hyperframes@0.8.196 snapshot --at 0.5,1.2,6,9.2,13    # PNG och ett kontaktark i .hyperframes/artifacts/snapshots/

# Rendera för leverans
npx -y hyperframes@0.8.196 render --fps 25 --quality looks --output renders/<namn>.mp4

# Kontaktark av den färdiga filmen: en bild per sekund med verklig tid
python agents/wds/tools/hyperframes/film.py sheet renders/<namn>.mp4 <namn>-kontaktark.jpg
```

- **Förhandsvisning** för personen: `npx -y hyperframes@0.8.196 preview --background --port 3017` och adressen `http://localhost:3017/#project/<mapp>`; stoppa med `preview --stop`. Ändringar personen gör där hamnar i `index.html` i arbetsmappen och förs tillbaka till `film.json` eller templaten för hand.
- **Tid:** 15 s i 1080×1920 tog 53 s på Surface Pro 7 (i7-1165G7, grafikkretsen till Chrome), 2 min 9 s när två renderingar gick samtidigt. Kör i bakgrunden.
- **Ljudet** följer med från bildplattan (`data-has-audio`). Fps sätts till plattans (`--fps 25` för Lumix-materialet).

## Grafiklager med alfakanal till Resolve

`film.py build … --overlay` utelämnar plattan och gör bakgrunden genomskinlig. Slutet (kundens mark) är fortfarande heltäckande.

```bash
npx -y hyperframes@0.8.196 render --fps 25 --format mov --output renders/overlay.mov            # ProRes 4444 med alfa
npx -y hyperframes@0.8.196 render --fps 25 --format webm --output renders/overlay.webm          # VP9 med alfa
npx -y hyperframes@0.8.196 render --fps 25 --format png-sequence --output renders/overlay.png   # RGBA-bilder i en mapp
```

Prövat 2026-10-25 med talat-ord (15 s, 1080×1920, 25 fps) på Surface Pro 7:

| Format | Resultat | Storlek | Tid |
|---|---|---|---|
| `mov` | ProRes 4444 (`ap4h`), `yuva444p12le`: riktig alfakanal. Förstahandsvalet till Resolve | 116 MB | 1 min 5 s |
| `webm` | VP9 med alfa (`ALPHA_MODE=1`); ffmpeg läser alfan bara med `-c:v libvpx-vp9` före `-i` | 2,3 MB | 1 min 1 s |
| `png-sequence` | 375 RGBA-bilder i en mapp; säkrast när ett program inte läser alfa i video | 84 MB | – |

Alla tre lades på plattan med ffmpeg (`overlay=format=auto`) och gav samma bild som filmen renderad med plattan. **Import i Resolve är inte prövad än:** lägg `overlay.mov` på V2 över plattan på V1; Resolve ska känna igen alfan i ProRes 4444 (klippets attribut, Alpha Mode: Straight). Skriv in resultatet här första gången.

## Fallgropar (prövat 2026-10-25)

- **Tidslinjen är global.** Alla GSAP-tider i en sida räknas från filmens början, även för element inne i en `.clip` med `data-start`. En scen som räknade lokalt visade "långsamt" två sekunder för tidigt.
- **Bokstavsavstånd, `width`, `left` och liknande får inte animeras** (`gsap_non_transform_motion`): de hackar när bilderna stegas. Animera `x`, `y`, `scale`, `opacity` och `clip-path`.
- **`clip-path` måste ha samma enheter i start och slut** (`inset(-25% 100% …)` till `inset(-25% -5% …)`); blandade `px` och `%` hoppar direkt till slutläget.
- **Typsnitt i länkade CSS-filer hittas inte.** HyperFrames lägger bara in typsnitt som står i sidans egen `<style>`; ett typsnitt i en `<link>`-ad fil blev Arial i renderingen fast stillbilderna från `snapshot` såg rätt ut. Därför lägger `film.py` in kundens `tokens.css` och `film.css` i sidan. Titta på en beskuren bildruta ur den färdiga filmen, inte bara på `snapshot`.
- **Typsnitt** som inte är inbyggda (Inter, Roboto, Montserrat med flera) behöver `@font-face` med en fil i kundens `film.css`; ett `local()` som inte finns på datorn faller tyst tillbaka. Inbyggda familjer hämtas i fler vikter från Google Fonts och sparas i `~/.cache/hyperframes/fonts`.
- **GSAP** laddas från jsDelivr i en låst version (3.14.2, GreenSocks fria licens); renderingen behöver nätet första gången.
- `nested_structure_needs_subcomposition` är en varning för redigering i HyperFrames Studio, inget fel i filmen.
- ffmpeg på Windows har ingen fontconfig: `drawtext` kraschar utan `fontfile=`, därför letar `film.py sheet` upp ett systemtypsnitt.
