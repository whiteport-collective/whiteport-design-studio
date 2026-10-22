---
name: resolve
source: wds
type: script
description: Styr DaVinci Resolve Studio med Python mot Resolves skript-API (projekt, bins, import, tidslinjer, LUT och rendering), och beskriver hur gratisversionen tar emot det agenten förbereder. Utan MCP.
used_by: [media-ingest, video-edit, media-export]
---

# Tool: resolve

**Status: inte provat (2026-10-22).** Resolve 21.1 är installerat på Mårtens dator i gratisversionen. Skript-API:t kräver Studio från och med 21.1. Allt under Studio prövas första gången det behövs, och det som stämmer skrivs in här.

Resolve 21.1 har också en inbyggd MCP-server (File → Setup AI Assistants). Den används inte: WDS kör inga MCP-servrar i sessioner, och samma åtkomst finns i Python-API:t.

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
