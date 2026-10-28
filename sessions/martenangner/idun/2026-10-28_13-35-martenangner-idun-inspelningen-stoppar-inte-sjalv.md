---
session: 2026-10-28_13-35-martenangner
start: 2026-10-28T13:35+01:00
slut: 2026-10-28T23:50+01:00
user: martenangner
från: idun
till: idun
model: claude-opus-5-5
tool: claude
projects: []
repos: [habitech-team, whiteport-design-studio]
status: öppen
tagen_av:
---

# Förslag till WDS: inspelningen stoppar inte när mötet är slut

## Vad hände
Kundmötet med Tapajos (habitech-team) slutade 15.24, men inspelningen gick till 22.49 eftersom ingen sa "stoppa". Någon gång efter mötet försvann ljudenheterna. Då skrev `local.py` statusraden "inget ljud" flera gånger i sekunden, i stället för en gång i minuten, och bevakningen fylldes med hundratals rader. Ljudfilerna växte till 1 GB per kanal, varav 7 timmar tystnad. Agenten stoppade inspelningen med `STOP`-filen utan att personen sagt "stoppa", för att skydda mötesljudet mot ett hårt avbrott, och körde `refine.py --first 6600` för att hoppa över tystnaden.

## Förslag
1. **meeting-live (`local.py`):** när en ljudenhet försvinner, skriv en händelse en gång (`== Ljudenheten försvann ==`) och försök koppla upp igen, i stället för en statusrad per varv. Statusraden ska inte gå oftare än en gång i minuten.
2. **meeting-live:** stoppa av sig själv efter till exempel 30 minuter utan tal i någon kanal, med en slutrad som säger varför. Ljudet efter sista repliken behålls.
3. **recording-skillen, Under inspelningen:** när mötet hörs avslutas ("tack för idag", "hej så länge") och ingen säger något på några minuter, fråga personen en gång om inspelningen ska stoppas. Och skriv in när agenten får stoppa själv: när ljudenheterna är borta och mötet är slut, eftersom en hård krasch annars kan förstöra ljudfilerna.

Mårten godkänner.
