---
name: exiftool
source: wds
type: cli
description: Läser och skriver metadata i foton och video (tid, kamera, objektiv, plats, upphovsrätt) med ExifTool.
used_by: [media-ingest, media-catalog, media-export, film-sourcing]
---

# Tool: exiftool

**Installera:** `winget install --id OliverBetz.ExifTool -e` (Windows), `brew install exiftool` (Mac). Kontrollera med `exiftool -ver`. Ett nytt skal kan behövas innan kommandot hittas.

## Läsa

```bash
# Tid, kamera och typ för en mapp, som JSON
exiftool -json -q -r -DateTimeOriginal -CreateDate -Model -LensModel -FileType "<mapp>"

# Allt om en fil
exiftool -a -G1 "<fil>"
```

## Förhandsbild ur RAW

En RAW-fil (RW2, DNG) bär en färdig JPEG inuti. Den räcker för att se vad bilden visar, utan att framkalla. Skriv den alltid till en arbetsmapp, aldrig i `original/`.

```bash
exiftool -b -PreviewImage "<fil>.RW2" > "<arbetsmapp>/<fil>.jpg"
# Eller för en hel mapp: <arbetsmapp>/<grundnamn>.jpg
exiftool -b -PreviewImage -w "<arbetsmapp>/%f.jpg" -ext rw2 "<mapp>"
```

## Skriva

**Aldrig i `original/`.** Metadata skrivs bara på exporter, i `export/`.

```bash
# Upphov och beskrivning på en export
exiftool -overwrite_original -Artist="<namn>" -Copyright="© <år> <kund>" -XMP-dc:Description="<text>" "<exportfil>"

# Kopiera metadata från originalet till en export som tappat den (till exempel efter ffmpeg)
exiftool -overwrite_original -TagsFromFile "<original>" -all:all "<exportfil>"

# Ta bort plats ur en export som ska publiceras
exiftool -overwrite_original -gps:all= "<exportfil>"
```

- `-overwrite_original` används bara på exporter, så att ingen `_original`-kopia blir liggande.
- Klockskillnad mellan två kameror redovisas i `ingest.csv` och hanteras i redigeringsprogrammet. Tiden i originalen ändras aldrig.
- **Å, ä, ö från PowerShell:** argumenten går in i Windows teckentabell och blir Latin-1 i filen ("M?rten"). Skriv argumenten till en fil i UTF-8 utan BOM, en per rad, och kör `exiftool -@ <fil>`, med `-charset exif=utf8` i filen (provat 2026-10-24).
