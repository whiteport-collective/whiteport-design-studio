---
name: ffmpeg
source: wds
type: cli
description: Läser av, konverterar, skalar och klipper video, ljud och bilder med ffmpeg och ffprobe.
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
