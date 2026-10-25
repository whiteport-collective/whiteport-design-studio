# Viskas kunskapsbas: film från brief till leverans

Utredd 2026-10-25 på Mårtens uppdrag: "läsa på och förstå all kunskap som finns på nätet om hur vi redigerar olika typer av produktioner, mixar in B-roll från vårt eget arkiv, royaltyfria klipp och AI-genererade sekvenser". Fyra utredningar, var och en med källa på varje påstående. Det egna resonemanget är märkt **[Inference]**, **[Recommendation]** eller **[Unverified]**, och svaga källor **[Uncertain]** eller **[vendor]**. Rapporterna är på engelska, eftersom källorna är det; skillsen som bygger på dem är på svenska.

| Rapport | Vad den svarar på | Används av |
|---|---|---|
| [klipphantverk.md](klipphantverk.md) | Murchs prioritetsordning, åtta produktionstyper (eventfilm, varumärkesfilm, kundcase, intervju, talking head, lansering, rekrytering, 9:16), klippens och övergångarnas ordförråd med när och när inte, dramatik och rytm, ljud, bildsäkra ytor, 27 tecken på AI-slop och tio regler som går att kontrollera på en tidslinje | [film-assembly](../../skills/film-assembly/SKILL.md), [film-production](../../skills/film-production/SKILL.md) |
| [fran-brief-till-film.md](fran-brief-till-film.md) | Kedjan brief → budskap → koncept → manus (tvåkolumns) → bildlista → behovslista → pappersklipp → grov-, finklipp och låsning; triggerkartan som "forces of progress"; intervjufrågor ur krafterna; vad Resolve 21.1:s API, FCPXML, OTIO, Fusion och OGraf klarar; vad agenten beslutar själv och vad den frågar om | [film-production](../../skills/film-production/SKILL.md), [film-assembly](../../skills/film-assembly/SKILL.md), [resolve](../../tools/resolve.md) |
| [b-roll-och-rattigheter.md](b-roll-och-rattigheter.md) | B-roll ur manus, sök i eget arkiv (också semantiskt), arkivbolagens licenser för kunduppdrag i Sverige, musik och ljudeffekter, att få arkivbilder att se egna ut, rättighetsloggen | [film-sourcing](../../skills/film-sourcing/SKILL.md) |
| [ai-video.md](ai-video.md) | Higgsfield och de andra generatorerna (läget 2026-10-25), vad AI-klipp duger till och inte, bild-till-video ur egna stillbilder, matchning i Resolve, AI-förordningens artikel 50, lagen om namn och bild i reklam, avtal, ursprungslogg per klipp | [film-sourcing](../../skills/film-sourcing/SKILL.md) |

## Färskvara

Generatorer, priser och licensvillkor ändras månad för månad (Sora stängde 2026-09-24, Veo 3.1:s förhandsmodeller 2026-10-22, Pexels och Pixabay bytte villkor 2026-10-20). Kontrollera det som gäller innan pengar läggs eller något levereras, och skriv in det nya här med datum. Rättsfrågorna (AI-märkning, samtycke, avtalsklausuler) ska granskas av en svensk jurist innan de används i ett kundavtal.

## Det som inte är provat

Allt om Resolve 21.1:s nya anrop (`AddTransition`, `SetSpeed`, `SetFades`, `GetTranscription`, `CreateSubtitlesFromAudio`, `NormalizeAudioLevel`, titlar med Text+ och OGraf) kommer ur Blackmagics egna filer på datorn, inte ur egna prov. Det som provas skrivs in i [resolve](../../tools/resolve.md).
