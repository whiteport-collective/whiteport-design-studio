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

Lärdom från första försöket: mycket varmt material (glödlampor) blev gräddgult när värme lades ovanpå utjämningen. Håll värmen låg och låt nästan vita ytor dras mot neutralt (`clean`).
