---
name: ffmpeg
source: wds
type: cli
description: Läser av, konverterar, skalar och klipper video, ljud och bilder med ffmpeg och ffprobe, och renderar det Resolve inte kan göra från skript: följning med nyckelpunkter till 9:16, fartkurvor, rörliga stillbilder och ihopsättning av en reel.
used_by: [media-catalog, media-export, video-edit]
---

# Tool: ffmpeg

**Installera:** `winget install --id Gyan.FFmpeg -e` (Windows), `brew install ffmpeg` (Mac). Kontrollera med `ffmpeg -version`.

Läser alltid från `original/` eller från en export ur redigeringsprogrammet, och skriver alltid till `export/` eller en arbetsmapp. Aldrig `-y` mot en fil som redan finns i `export/` utan att personen sagt ja.

## Läsa av

```bash
ffprobe -v quiet -print_format json -show_format -show_streams "<fil>"
```

## Video

```bash
# Webb: H.264, högst 1920 bred, snabb start
ffmpeg -i "<in>" -vf "scale='min(1920,iw)':-2" -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "<ut>.mp4"

# Sociala medier, stående 9:16 (1080x1920), beskuret från mitten
ffmpeg -i "<in>" -vf "crop=ih*9/16:ih,scale=1080:1920" -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "<ut>.mp4"

# Videoheader: utan ljud, kort loop, liten fil
ffmpeg -ss <start> -t <sekunder> -i "<in>" -an -vf "scale=1920:-2" -c:v libx264 -crf 24 -preset slow -pix_fmt yuv420p -movflags +faststart "<ut>.mp4"
ffmpeg -ss <start> -t <sekunder> -i "<in>" -an -vf "scale=1920:-2" -c:v libvpx-vp9 -crf 34 -b:v 0 "<ut>.webm"

# Klipp ut en del utan att koda om (snabbt, klipper på närmaste nyckelbild)
ffmpeg -ss <start> -to <slut> -i "<in>" -c copy "<ut>"

# Ljudet till taligenkänning: mono 16 kHz
ffmpeg -i "<in>" -vn -ac 1 -ar 16000 "<ut>.wav"

# En stillbild ur en video
ffmpeg -ss <tid> -i "<in>" -frames:v 1 -q:v 2 "<ut>.jpg"
```

## Bilder

ffmpeg läser JPEG, PNG och TIFF men inte RAW (RW2, DNG). RAW framkallas i redigeringsprogrammet, och ffmpeg gör storlekar av den exporten.

```bash
# Webb: högst 2400 bred, JPEG och WebP
ffmpeg -i "<in>.jpg" -vf "scale='min(2400,iw)':-2" -q:v 3 "<ut>.jpg"
ffmpeg -i "<in>.jpg" -vf "scale='min(2400,iw)':-2" -quality 82 "<ut>.webp"
```

ffmpeg tappar metadata. Kopiera tillbaka den med [exiftool](exiftool.md) efteråt.

## Omformatering till 9:16 och reel

Skript i `agents/wds/tools/ffmpeg/`, för det som Resolve inte kan göra från skript: följning med nyckelpunkter, fartkurvor och rörliga stillbilder. Allt som går att justera i Resolve görs där i stället ([resolve](resolve.md#reel-i-resolve)). Vad som gör en bra reel står i skillen [video-edit](../skills/video-edit/SKILL.md).

```bash
python agents/wds/tools/ffmpeg/framing_sheet.py "<delad enhet>/projects/<projekt>" klipplista.json <arbetsmapp>/framing [--only 5,8]
python agents/wds/tools/ffmpeg/reframe.py "<delad enhet>/projects/<projekt>" klipplista.json <klippmapp> [--only 5,8]
python agents/wds/tools/ffmpeg/reel_assemble.py "<delad enhet>/projects/<projekt>" klipplista.json <klippmapp> <projekt>/export/sociala-medier/<datum>-reel-<namn>-vN.mp4 --music <spår> [--xfade 0.3] [--fade-out 1.2]
```

**Klipplistan** (`<projekt>/resolve/reel-9x16-vN-klipplista.json`) har en del per rad, i ordning. Videoklipp: `rec`, `stem`, `start`, `want` (längd i reelen), `dur` (`want` + övertoningen, utom sista delen) och:

| Nyckel | Vad |
|---|---|
| `"x": 0.5` eller `[0.42, 0.48, 0.52]` | Rutans mittpunkt över bredden; en lista är nyckelpunkter jämnt fördelade i klippet, och rutan glider mellan dem med en mjuk kurva (smoothstep, som Ease In/Out) |
| `"speed": 1.7` | Fast fart |
| `"ramp": [[0,1],[1.2,1],[3,6],[23.5,6],[25.6,1],[27.6,1]]` | Fartkurva (sekunder från `start`, fart), linjär mellan punkterna; klippets längd blir kurvans längd |
| `"resolve": {"RotationAngle": -1.5}` | Sätts i Resolve av `reel_timeline.py`, inte här |
| `"rotate"`, `"eq"` | Rotation och färglyft inbakade, bara för leveranser utan Resolve |

Stillbilder: `"still": "<sökväg under projektet>"`, `"move"`: `pan` (över en gruppbild), `zoom` (mot mitten) eller `push` (nära mot `"focus": [x, y]` med `"zoom": [1.65, 1.85]` och en liten glidning). De sparas som `<klippmapp>/segNN-still-<bild>.mp4`.

**Kartan** (`framing_sheet.py`) visar början, en tredjedel, två tredjedelar och slutet av varje klipp med ett rutnät 1–9; läs var ansiktena och handlingen är och sätt `"x"`. **`reframe.py`** beskär, skalar, lägger på klippets LUT (`<projekt>/resolve/lut/<inspelning>/<klipp>.cube`) och sparar `segNN-<klipp>.mp4`. **`reel_assemble.py`** sätter ihop delarna med övertoningar, lägger musiken under (in- och uttoning, -14 LUFS) och tonar ut till svart.

**Grafikkretsen (Intel Quick Sync).** Originalen avkodas med grafikkretsen (`-hwaccel d3d11va`) och klippen kodas med `h264_qsv`; LUT och färg läggs efter beskärningen. Mätt 2026-10-24 på Surface Pro 7, två klipp à 5 s ur 4K HEVC: 57 s på processorn med färg på 4K, 36 s med färg efter beskärningen, **17 s** med grafikkretsen och färg efter beskärningen. `WDS_NO_QSV=1` tvingar processorn. `-hwaccel qsv` fungerar inte med filter på processorn: bildrutorna stannar i grafikminnet och `lut3d` når dem inte.
