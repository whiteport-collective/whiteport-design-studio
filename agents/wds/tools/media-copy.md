---
name: media-copy
source: wds
type: script
description: Läser av ett minneskort eller en inkorg, känner igen kamerorna mot kameraregistret, kontrollerar kamerornas metadata och kopierar eller flyttar media till <datum>-<plats>/<person>/<kamera>/, kontrollerat med sha256 och utan att något skrivs över. Skriptet ligger i media-copy/.
used_by: [media-ingest]
---

# Tool: media-copy

Skriptet: `agents/wds/tools/media-copy/media_copy.py`. I ett repo utan `agents/wds/` används sökvägen i WDS-repot. Kräver Python 3. Läser tidpunkt och kamera med [exiftool](exiftool.md) om det finns, annars filens ändringstid.

## Läs av kortet

```bash
python agents/wds/tools/media-copy/media_copy.py scan "E:/"
```

Visar antal filer per typ, vilka kameror, och passen: en rad per sammanhängande period, med ny rad efter mer än 45 minuters uppehåll. Passen är underlaget för att dela upp dagen på platser.

## Kamerorna

```bash
python agents/wds/tools/media-copy/media_copy.py cameras "E:/" "G:/Shared drives/<enhet>/kameror.md"
python agents/wds/tools/media-copy/media_copy.py check "E:/" --photographer "Mårten Angner"
python agents/wds/tools/media-copy/media_copy.py register "G:/Shared drives/<enhet>/kameror.md" --serial WJ6CB002321 --make Panasonic --model DC-S9 --person marten --name lumix-s9
```

- `cameras` visar varje kamera i källan (märke, modell, serienummer, antal filer, tidsspann) och vem den tillhör enligt registret, eller `OKÄND`. Kod 3 om någon saknas.
- `check` visar kamerans metadata och vad som saknas eller är fel: fotograf (`Artist`), upphovsrätt (`Copyright`), ägare (`OwnerName`), serienummer, tidszon (`OffsetTimeOriginal`) och klockan (tider i framtiden, eller ett år före 2015). Kod 4 när något behöver ställas in i kameran. Provat 2026-10-24: Mårtens Lumix S9 saknade fotograf och upphovsrätt.
- `register` lägger till eller uppdaterar en kamera i `kameror.md` (en tabell: serienummer, märke, modell, person, kamera, kontrollerad, anteckning). En telefon registreras utan serienummer och känns igen på modell.

## Sortera en inspelning

```bash
python agents/wds/tools/media-copy/media_copy.py sort "E:/" "G:/Shared drives/<enhet>/projects/<projekt>" 2026-10-22-linnesalen "G:/Shared drives/<enhet>/kameror.md" --from "2026-10-22 11:30" --to "2026-10-22 15:00"
```

Kopierar varje kamera i tidsramen till `<projekt>/<datum>-<plats>/<person>/<kamera>/`, med person och kamera ur registret. Torrkörning utan `--apply`; `--move` från en inkorg. Kameror som saknas i registret hoppas över (kod 3).

## Kopiera

```bash
# Torrkörning: visar vad som kopieras, vad som redan finns och vad som krockar
python agents/wds/tools/media-copy/media_copy.py copy "E:/" "G:/Shared drives/<enhet>/projects/<projekt>/<datum>-<plats>/<person>/<kamera>" --from "2026-10-22 11:30" --to "2026-10-22 15:00"

# Samma kommando med --apply kopierar
python agents/wds/tools/media-copy/media_copy.py copy … --apply
```

- `--from` och `--to` (lokal tid, `YYYY-MM-DD HH:MM`) väljer en del av kortet. Utan dem kopieras allt.
- `--model "<Model>"` eller `--serial <nr>` väljer en kamera. Används när flera kameror ligger i samma inkorg (`sort` gör det själv).
- `--move` flyttar från en **inkorg** i stället för att kopiera: på samma enhet döps filen bara om, annars kopieras den, kontrolleras och tas bort ur inkorgen. Filer som redan finns med samma innehåll tas bort ur inkorgen. **Aldrig mot ett minneskort.**
- Varje fil kopieras till `<namn>.part`, kontrolleras mot källans sha256 och döps sedan om. En avbruten körning lämnar bara `.part`-filer, som kan tas bort, och körs om.
- **Finns redan med samma innehåll:** hoppas över. Samma kort kan köras flera gånger.
- **Krock** (samma namn, annat innehåll, eller två filer med samma namn på kortet): kopieras inte. Skriptet slutar med kod 2 och listar dem. Agenten frågar personen; skriptet gissar aldrig.
- **Loggen:** en rad per kopierad fil i `<inspelning>/ingest.csv`: när, sökväg under inspelningen, källa, tagen, kamera, storlek, sha256. Checksummorna används igen när mappen arkiveras.
- Utan `--move` läser skriptet bara från källan och tar aldrig bort något där.

## Rätta en fil som hamnat fel

En fil som hamnat i fel inspelning eller källa flyttas med samma skript, från den felaktiga mappen till den rätta, med `--move` och en tidsram eller kamera som väljer just de filerna. Flytten loggas i den nya inspelningens `ingest.csv`. Flytta helst innan redigeringen har börjat: en fil som ett Resolve-projekt redan använder blir offline och måste länkas om.

| Kod | Betyder |
|---|---|
| 0 | Klart, eller torrkörning utan krockar |
| 1 | En kopia stämde inte med originalet. Inget mer kopierades. |
| 2 | Krockar finns |
| 3 | En kamera saknas i registret |
| 4 | Kamerans metadata behöver ställas in (`check`) |
