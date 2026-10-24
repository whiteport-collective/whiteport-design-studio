---
name: resolve
source: wds
type: script
description: Styr DaVinci Resolve Studio med Python mot Resolves skript-API (projekt, bins, import, tidslinjer, LUT och rendering), och beskriver hur gratisversionen tar emot det agenten förbereder. Utan MCP.
used_by: [media-ingest, video-edit, media-export]
---

# Tool: resolve

**Status (2026-10-23):** Studio köpt. Skript-API:t (Python) kräver Studio från och med 21.1; i gratisversionen körs inga Python-skript, inte ens från Workspace-menyn. Skriptdelen nedan är inte provad än. Allt under Studio prövas första gången det behövs, och det som stämmer skrivs in här.

Resolve 21.1 har också en inbyggd MCP-server (File → Setup AI Assistants). Den används inte: WDS kör inga MCP-servrar i sessioner, och samma åtkomst finns i Python-API:t.

## Ladda ner och installera

Whiteport har en licens för **DaVinci Resolve Studio** (köpt 2026-10-23 på Mårten, bokförd som utlägg i Whiteport AB). Licensnyckeln står i orderbekräftelsen från noreply@blackmagicdesign.com i Mårtens Gmail (ämne "Blackmagic Design Order", 2026-10-23) och ska ligga i Bitwarden; den skrivs aldrig in i en fil. En Studio-nyckel räcker till två datorer; flytta den med Help → Deactivate License på den dator som lämnar.

- **Nedladdningssidan:** https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion (välj *DaVinci Resolve Studio* för Windows eller Mac; ingen inloggning, bara namn och e-post).
- **Från skript**, utan webbläsare: Blackmagics support-API ger senaste versionen och en nedladdningslänk.

```bash
# Senaste versionerna och deras downloadId
curl -s "https://www.blackmagicdesign.com/api/support/us/downloads.json" | python -c "import json,sys;[print(x['name'],x['urls'].get('Windows',[{}])[0].get('downloadId')) for x in json.load(sys.stdin)['downloads'] if x['name'].startswith('DaVinci Resolve Studio')][:3]"

# Registrera och få länken (namn och e-post enligt users/<användare>/user.md)
curl -s -X POST "https://www.blackmagicdesign.com/api/register/us/download/<downloadId>" \
  -H "Content-Type: application/json;charset=UTF-8" -H "User-Agent: Mozilla/5.0" \
  -d '{"firstname":"…","lastname":"…","email":"…","phone":"…","country":"se","city":"…","street":"…","state":"…","product":"DaVinci Resolve Studio"}'
```

Studio 21.1.1 för Windows är en zip på 10,3 GB och lika mycket uppackad: räkna med drygt 21 GB ledigt. Installationsfilen är signerad av Blackmagic Design Pty Ltd (kontrollera med `Get-AuthenticodeSignature`). Installationen kräver administratörsgodkännande; en tyst installation (`/i /q /noreboot`) avbryts när den inte får det, så personen startar den själv.

## Utan Studio: gratisversionen

Agenten förbereder filer som personen öppnar i Resolve:

| Agenten gör | Personen gör i Resolve |
|---|---|
| En tidslinje som FCP 7 XML (`xmeml`) eller EDL, med klippen och markörerna, sparad i projektets arbetsmapp | File → Import → Timeline, välj filen. Media hittas där de ligger. |
| En LUT (`.cube`) för projektets utseende | Lägg den i Resolves LUT-mapp, eller välj den i Color/Photo |
| Ett projekt som `.drp` i `resolve/` | File → Import Project |

Tidslinjen refererar till filerna med absolut sökväg under den delade enheten. Hos en annan person översätter Path Mapping (projektinställningarna) roten, se [media-storage](../data/media-storage.md#arbeta-och-dela).

## Med Studio: skript-API:t

Resolve måste vara igång, och Preferences → System → General → External scripting using ska stå på **Local**.

**Miljön, Windows:**

```powershell
$env:RESOLVE_SCRIPT_API = "$env:PROGRAMDATA\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
$env:RESOLVE_SCRIPT_LIB = "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
$env:PYTHONPATH = "$env:PYTHONPATH;$env:RESOLVE_SCRIPT_API\Modules"
```

**Mac:** `RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"`, `RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"`, och `$RESOLVE_SCRIPT_API/Modules` i `PYTHONPATH`.

Dokumentationen för API:t ligger i `$RESOLVE_SCRIPT_API/README.txt` på datorn. Läs den innan ett anrop används första gången, och skriv in det som fungerar här.

**Grunden:**

```python
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
pm = resolve.GetProjectManager()
project = pm.CreateProject("<projekt>") or pm.LoadProject("<projekt>")
mp = project.GetMediaPool()
storage = resolve.GetMediaStorage()

# En bin per inspelning och källa, med filerna där de ligger
root = mp.GetRootFolder()
b = mp.AddSubFolder(root, "2026-10-22-linnesalen marten-lumix-s9")
mp.SetCurrentFolder(b)
storage.AddItemListToMediaPool("<sökväg till original/<källa>>")

# Tidslinje från en XML som agenten har skrivit
mp.ImportTimelineFromFile("<sökväg>.xml")

# Exportera projektet så att andra kan öppna det
pm.ExportProject("<projekt>", "<delad enhet>/projects/<projekt>/resolve/<projekt>.drp")
```

Hur mycket av Photo-sidan (album, RAW-inställningar, export av stillbilder) API:t når är inte känt. Pröva och skriv in det här.

## Regler

- Resolve skriver aldrig över original. Rendering går till `export/<kanal>/`.
- Projektets media ska ligga under projektmappen på den delade enheten. Viska lägger aldrig in en fil från någon annanstans.

## Startfilen: alla bilder och klipp i Resolve utan Studio

```bash
python agents/wds/tools/resolve/timeline_xml.py "<delad enhet>/projects/<projekt>"
```

Skriver `<projekt>/resolve/<projekt>-start.xml` (FCP 7 XML) ur inspelningarnas `innehall.csv`: en tidslinje per inspelning i inspelningsordning (foton som JPEG, 4 s styck, och klipp, utan dem som föreslås bort), en tidslinje med favoriterna och en med de tvättade talen i `klipp/`. Varje fil får en markör med katalogens beskrivning och betyg. Mediet länkas där det ligger, så filen fungerar på varje dator där den delade enheten har samma sökväg; annars Path Mapping.

I Resolve: **File → Import → Timeline**, välj filen. Klippen hamnar i Media Pool och tidslinjerna skapas. Utskrifterna (`<klipp>.srt` bredvid klippet) dras in som undertextspår. RAW-filerna (RW2) läggs in från `original/` när färgsättningen börjar. `--with-rejects` tar med även de bortvalda, `--still` ändrar fotonas längd.

## Lägga in ett projekt med skript (Studio)

```bash
python agents/wds/tools/resolve/import_project.py "<delad enhet>/projects/<projekt>"   # bins, metadata, färger, tidslinjer
python agents/wds/tools/resolve/proxies.py "<delad enhet>/projects/<projekt>"          # proxyfiler och koppling
```

`import_project.py` skapar eller öppnar projektet med mappens namn och lägger in varje inspelning som en bin med `video`, `foto`, `raw` och `tal-tvattade`. Katalogens beskrivning, nyckelord och bedömning blir metadata (Description, Keywords, Comments), favoriter blir gröna och bortval orange, och det blir en tidslinje per inspelning plus en med favoritklippen. Redan importerade filer hoppas över, och `<klipp>.proxy.mov` bredvid ett klipp kopplas som proxy. Provat 2026-10-23 med Resolve Studio 21.1.1 på Surface Pro 7: importen tar flera minuter per inspelning när mediet strömmas från Drive.

`proxies.py` gör proxyfiler för projekt som saknar dem och kopplar dem med `MediaPoolItem.LinkProxyMedia`. Proxyfilen heter `<klipp>.proxy.mov` och ligger bredvid originalet. Nytt material får den redan vid mottagningen (`worker.py batch`).

## Färgsättning med LUT per klipp

```bash
python agents/wds/tools/resolve/looks.py "<delad enhet>/projects/<projekt>" --map "2026-10-22-koket=frisk-varm,*=varm" --preview --apply
```

Två steg bakas ihop till en LUT per klipp i `<projekt>/resolve/lut/<inspelning>/<klipp>.cube`: utjämning (vitbalans och exponering mätta på klippet, helst via proxyn) och ett utseende. `--preview` skriver en före/efter-bild per inspelning, `--apply` lägger LUT:en på nod 1 för varje klipp i tidslinjerna. Mätningar och utseenden sparas i `looks.json`.

| Utseende | För | Känsla |
|---|---|---|
| `varm` | middagar, salar, utomhus | varm och härlig: gyllene ljus, vita dukar förblir vita, lätt lyfta skuggor (Mårten, 2026-10-23) |
| `frisk-varm` | storkök, stål, lysrör | fräscht fast varmt: rena vita kockrockar, varm hud och mat, stål mot varmt i stället för blått, lite mer kontrast |

Resolve tar bara LUT:ar i sin egen LUT-mapp; `--apply` kopierar dit och använder relativ sökväg (provat 2026-10-23, 49 klipp). Lärdom från första försöket: mycket varmt material (glödlampor) blev gräddgult när värme lades ovanpå utjämningen. Håll värmen låg och låt nästan vita ytor dras mot neutralt (`clean`).

## Reel i Resolve

Vad som gör en bra reel och hur versionerna går till står i skillen [video-edit](../skills/video-edit/SKILL.md). Här står hur det görs i Resolve.

**Tidslinjen ur färdiga klipp** (renderade med [ffmpeg](ffmpeg.md#omformatering-till-916-och-reel)):

```bash
python agents/wds/tools/resolve/reel_timeline.py "<delad enhet>/projects/<projekt>" v7
```

Klippen hämtas ur `<projekt>/resolve/reel-<version>-klipp/segNN-*.mp4` (stillbilderna som rörliga klipp), läggs i binen `reel-<version>-klipp` och på tidslinjen `reel-9x16-<version>` i 1080x1920 med `scaleToCrop`, musiken på A1 (`AppendToTimeline` med `mediaType: 2`). Skriptet väntar på att Resolve startat och öppnar projektet med mappens namn.

**Det som går att sätta på ett klipp från skript**, och som därför sätts här i stället för att klippet renderas om (Mårten, 2026-10-24): `"resolve": {...}` på en del i klipplistan sätts med `TimelineItem.SetProperty`:

| Egenskap | Exempel |
|---|---|
| Rotation | `"RotationAngle": -1.5` |
| Fast zoom och position | `"ZoomX": 1.05, "ZoomY": 1.05, "Pan": 20, "Tilt": -10` |
| Färgjustering per klipp | `TimelineItem.SetCDL({...})`, eller i Color |

Nyckelpunkter (rörelse som ändras över tid), fartkurvor och övergångar går inte att skapa från skript. De renderas med ffmpeg.

**Rendering**, mätt 2026-10-24 på Surface Pro 7: tidslinjen reel-9x16-v7 (61 s, 12 färdiga klipp och musik) som H.264 1080x1920 på 34 s:

```python
project.SetCurrentRenderFormatAndCodec("mp4", "H264")
project.SetRenderSettings({"SelectAllFrames": True, "TargetDir": "<mapp>", "CustomName": "<namn>", "FormatWidth": 1080, "FormatHeight": 1920})
job = project.AddRenderJob(); project.StartRendering(job)
while project.IsRenderingInProgress(): time.sleep(1)
project.GetRenderJobStatus(job)   # TimeTakenToRenderInMs
```

**Smart Reframe** (`reel.py`, provat 2026-10-23) används inte längre: agenten följer varje klipp själv. Skriptet finns kvar: Smart Reframe analyserar i en modal ruta, cirka 0,7 bildrutor per sekund på Surface Pro 7, och då svarar API:t `None`; skriptet väntar ut varje analys. `"reframe": false` behåller det breda utsnittet.

```bash
python agents/wds/tools/resolve/reel.py "<delad enhet>/projects/<projekt>" klipplista.json --name reel-9x16-v4 --replace --render "<projekt>/export/sociala-medier"
```

**Resolve på Surface Pro 7.** Grafikminnet räcker inte till Resolve och många videor samtidigt i webbläsaren: tumnaglar och visare blir svarta, och loggen (`%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\logs\ResolveDebug.txt`) visar `CL_OUT_OF_RESOURCES`. Stäng sidor som spelar video, spara projektet (`ProjectManager.SaveProject`), avsluta (`Resolve.Quit`) och starta om. Kontrollera att ingen gammal `Resolve.exe` ligger kvar. Hackar uppspelningen: Playback → Timeline Proxy Resolution → Quarter.

## Mediebanken

```bash
python agents/wds/tools/resolve/mediabank.py "<delad enhet>/projects/<projekt>" [--only P1000708-01] [--replace] [--render] [--out <mapp>]
python agents/wds/tools/resolve/mediabank.py "<delad enhet>/projects/<projekt>" --open P1000708-01
```

Läser `<projekt>/resolve/mediabank-urval.json` (fälten står i skriptets hjälptext). För varje klipp: en FCPXML med båda versionerna i råklippets upplösning, importerad med `MediaPool.ImportTimelineFromFile` till binen `mediabank`, neutral färg per ljuszon på nod 1, `Timeline.Export(..., EXPORT_DRT)` bredvid råklippet och, med `--render`, två renderingsjobb ur samma tidslinje (hela bilden; 9:16 med `FormatWidth` 1440, centrerat utsnitt genom `scaleToCrop`). En tidslinje som redan finns rörs inte utan `--replace`.

Provat 2026-10-24 med P1000708 (30 s, 4K HEVC 10 bitar): båda versionerna renderade på cirka 160 s på Surface Pro 7.

**FCPXML i Resolve 21:** `adjust-transform` med `keyframeAnimation` på `position` blir riktiga nyckelpunkter (Pan); värdet är procent av bildens höjd (`-30` blev `-768` px i 3840x2560). `transition` med Cross Dissolve importeras som egna objekt på spåret: filtrera bort dem (`GetMediaPoolItem()` är `None`) innan LUT:ar läggs på klippen. Importen misslyckas medan Resolve renderar; ett jobb som hängt sig (full disk) kräver omstart av Resolve.

**Ljuszoner** (`looks.light_segments`): log(R/B) och ljushet två gånger per sekund; en ny zon när färgtemperaturen hoppar mer än 0,18 eller när det blir mörkt (under 0,25). Mörka zoner breddas 0,4 s och får starkare exponering. Karaktär per zon (`looks.character`): log(R/B) under 0,15 `steril`, över 0,3 `restaurang`, däremellan `neutral`. `"look"` på ett klipp i urvalet tvingar ett utseende.

**Disken:** renderingar och Drives cache behöver plats på C:. Med under en gigabyte ledigt hänger renderingen på 0 %. Resolves cache, galleri och projektmedia ligger på `E:\DaVinci Resolve Cache\` på Surface Pro 7 (`perfCacheClipsLocation`, `colorGalleryStillsLocation`, `projectMediaLocation`).

## Inspelningens dokument

```bash
python agents/wds/tools/resolve/shoot_document.py "<delad enhet>/projects/<projekt>/<datum>-<plats>" [--limit N] [--replace]
```

Ett Resolve-projekt per inspelning, med inspelningens namn, för personens godkännande ([media-catalog](../skills/media-catalog/SKILL.md)). Underlaget är `innehall.csv`: filer med `forslag: bort` läggs inte in. Binarna `foto` och `video` med en underbin per person och kamera; beskrivning, nyckelord och bedömning som metadata, betyget som stjärnor (`MediaPoolItem.SetMetadata("Rating", "1"–"5")`). Klippen läggs på tidslinjen `video` med en balanserad färg per klipp på nod 1, mätt på proxyn och sparad som `<klipp>/<klipp>.cube`. Projektet exporteras som `<inspelning>/<inspelning>.drp` (`ProjectManager.ExportProject`). Personen godkänner med grön flagga.

**Bilderna stannar i RAW** (Mårten, 2026-10-24): Resolve 21 läser Lumix S9:s RW2 (6000x4000, Still) men visar dem svarta på en tidslinje, så bilderna ligger bara i binen, utan tidslinje och färg. En bild som ska användas på en tidslinje exporteras först till ett format som fungerar där, och då balanseras färgen. Provat 2026-10-24 med fem bilder och tre klipp ur Linnésalen.

## Fotosidan (Photo page) i Resolve 21

Utrett och provat 2026-10-24 med Resolve Studio 21.1.1 på Surface Pro 7 (Blackmagics *DaVinci Resolve 21 New Features Guide*, kapitlet Photo, och erfarna användare).

- **Album:** ett fotoalbum är "en särskild sorts tidslinje" av stillbilder, men i skript-API:t syns det bara som ett objekt av typen `Photo Album` i Media Pool, inte som en tidslinje. API:t kan varken skapa album, lägga bilder i dem eller färgsätta dem. Album skapas i gränssnittet (högerklick i Media Pool → New Photo Album, eller File → New Photo Album) och bilder läggs till med högerklick → Add Photo(s) to Album. Mallprojektet `agents/wds/tools/resolve/mallar/inspelning.drp` (binarna `foto` och `video` och ett tomt album `foton`) importeras av `shoot_document.py` med `ProjectManager.ImportProject(mall, inspelningens namn)`, så att albumet finns från början. Kvar i gränssnittet är att lägga bilderna i albumet: markera dem i binen → högerklick → Add Photo(s) to Album.
- **Färgen sitter på bilden:** "All grades and effects for still images within albums are applied at the source level" och delas mellan alla album i projektet.
- **RAW:** Lumix S9:s RW2 visas och framkallas på fotosidan (stöd från Resolve 21 beta 3), men blir svarta på en vanlig tidslinje. Fliken **RAW** (Panasonic Stills) i Inspector är det rekommenderade stället för exponering och färg: Decode Quality, White Balance, Color Temp (kelvin), Tint, Exposure (steg), Highlights, Shadows, Color Boost m.fl. Konvertering till DNG behövs inte.
- **Stjärnorna** är samma som `MediaPoolItem.SetMetadata("Rating", …)` och syns i albumet.
- **Grafikminnet på Surface Pro 7:** full framkallning av 24 megapixel ger `CL_OUT_OF_RESOURCES` och visaren uppdateras inte. Sätt Decode Quality till Quarter res. per bild (projektinställningen finns inte i API:t); exporten görs i full upplösning. Starta om Resolve om visaren slutar uppdatera; värdena är sparade på bilden.
- **Skärmbilder:** datorns vanliga skärmbildsverktyg ser inte Resolves gränssnitt (det ritas av grafikkortet). Ta skärmbilder med ffmpeg: `ffmpeg -f lavfi -i "ddagrab=output_idx=0:framerate=1,hwdownload,format=bgra" -frames:v 1 -update 1 bild.png`; koordinaterna i klickverktyget är skärmens bildpunkter delat med skalan (2736 → 1344).
- **Skriva värden:** dubbelklicka i fältet, Ctrl+A, skriv värdet, Enter. Trippelklick markerar inte hela fältet och ger fel värden.
- **Auto Balance** (maskininlärning) ändrade inga värden på den här datorn. **Auto tone normalization** i RAW-fliken är inte beskriven någonstans; lämna den på standard (ikryssad).
- **Samma inställning på flera bilder:** markera referensbilden i albumet → Ctrl+C, markera de andra → Edit → Paste Attributes (Alt+V), kryssa ur det som ska vara per bild (Rating, Exposure) → Apply. RAW-inställningar följer bara med mellan filer i samma RAW-format.
- **Recept, restaurang med glödljus** (Linnésalen, Mårten 2026-10-24: "varmare och mysigare", inte blekgrönt): Color Temp 3700 K, Tint +10, Highlights −40, Shadows +25, Color Boost +10, exponeringen mätt per bild på kamerans JPEG (+1,5 till +2,7 steg för bilder ungefär 1,5–2 steg under).
- **Export:** Quick Export på fotosidan (hela albumet eller valda bilder, originalupplösning, med metadata) eller Deliver-sidan; JPEG, PNG, HEIC, TIFF. Bara aktuell version exporteras.

## Stillbilder på en tidslinje: färg per bild och rendering

För bilder som ska levereras färdiga, när kamerans JPEG räcker som underlag (Getinge, 2026-10-24: 14 gruppbilder i starkt orange glödljus).

```bash
python agents/wds/tools/resolve/stills_resolve.py "<delad enhet>/projects/<projekt>" <inspelning> --files P1000307,... [--strength 0.3]
python agents/wds/tools/resolve/render_stills.py "<inspelning> foto" "<inspelning>/export/full=6000x4000:<inspelning>-<kund>-full-{nn}" "<inspelning>/export/epost=2400x1600:<inspelning>-<kund>-epost-{nn}"
```

- `stills_resolve.py` lägger JPEG-bilderna (och RW2 i en egen bin) i projektet med mappens namn, gör tidslinjen `<inspelning> foto` i 6000x4000 och sätter en uppmätt vitbalans som CDL-slope på nod 1 per bild (`TimelineItem.SetCDL`, fungerar på stillbilder). Mätningen: gråvärld på mellantonerna i linjärt ljus, styrka 0,3, ljusheten behålls. 0,3 gav varmt men naturlig hy; 0,4 blev gråaktigt och 0,6 kallt. Finjustera i Color.
- `render_stills.py` renderar en ruta per klipp som JPEG (`SetCurrentRenderFormatAndCodec("jpg", "YUV444_8")`, ett jobb per bild med `MarkIn` = `MarkOut`, valfri storlek). Resolve lägger ett rutnummer på bildsekvenser; skriptet döper om filen efteråt. 28 jobb (14 bilder i två storlekar) tog ett par minuter på MARTEN-SURFACE-. Kör `--formats` för att se vilka format och codecs Resolve erbjuder.
- `Project.ExportCurrentFrameAsStill` är inte pålitlig för kontroll: av 14 bilder sparades 2 när spelhuvudet flyttades i snabb följd. Rendera i stället och gör ett kontaktark av exporterna.
- **Studio eller gratis:** märket nere till vänster säger "DaVinci Resolve Studio 21" eller bara "DaVinci Resolve 21". I gratisversionen ger `scriptapp("Resolve")` `None` och inställningen External scripting finns inte alls; i en ny Studio-installation står den redan på Local. Studio installeras inte över gratisversionen av samma version (installationen hoppar då över huvudprogrammet): avinstallera gratisversionen först (`msiexec /x <produktkod>`), projekten ligger kvar. Installationsguiden körs som administratör, och Windows släpper inte igenom agentens klick dit, så personen klickar igenom den och godkänner licensen.
