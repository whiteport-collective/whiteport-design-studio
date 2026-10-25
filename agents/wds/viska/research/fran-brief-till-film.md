# Research D: from brief to finished film (pre-production practice, asset gap analysis, automated assembly in DaVinci Resolve 21, and how a leading agent decides)

Prepared for Viska (WDS media agent), 2026-10-25.

## How to read the confidence marks

| Mark | Meaning |
|---|---|
| **[BMD-doc]** | Stated in Blackmagic's own documentation installed with Resolve Studio 21.1.1 on this machine: `%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.md` (dated 31 Aug 2026), `CHANGELOG.md` (1 Sep 2026), `DaVinciResolveScript.pyi` (the official type stubs), `Developer\Fusion Templates\README.txt`, `Developer\OGraf HTML Templates\` (changelog 30 Sep 2026), or the reference manual `C:\Program Files\Blackmagic Design\DaVinci Resolve\Documents\DaVinci Resolve.pdf` (4351 pages, page numbers given). |
| **[Fusion-doc]** | Blackmagic's *Fusion 8 Scripting Guide* (2016). It is still the official Fusion scripting reference, but it predates Resolve's Edit/Fusion integration. |
| **[Tested]** | Already tried by Viska and written down in `agents/wds/tools/resolve.md`. |
| **[User report]** | Forum posts, reviews or blogs. Not checked by us. |
| **[Unverified]** | My inference or an open question that has to be tested. |

Sections 1, 2 and 4 rely on practitioner sources: production-company blogs, tool vendors and course material. They describe common conventions, not formal standards. Most of these sources are vendor content.

---

## Key findings in brief

1. **resolve.md is partly out of date.** Resolve 21.1 added `TimelineItem.AddTransition`, `SetSpeed` (constant speed, freeze frame), `SetFades`, multicam creation and SmartSwitch, `Timeline.AutoAlignClips`, `NormalizeAudioLevel`, and `MediaPoolItem.GetTranscription` with word timing and speaker. All are in Blackmagic's changelog and type stubs [BMD-doc], but none has been tested yet. Some things are still impossible from the API: keyframes on Edit-page Inspector properties, variable speed ramps, and applying an Animated Subtitle template. Those still need FCPXML import or Fusion.
2. **Keyframes have two scripted routes.** One is FCPXML import [Tested for position, BMD-doc for opacity, position, scale and rotation]. The other is Fusion: `Tool.Input = comp.BezierSpline()`, then `Tool.Input[frame] = value` [Fusion-doc], reached through `TimelineItem.GetFusionCompByIndex` [BMD-doc].
3. **Two kinds of brand title template are scriptable:** Fusion `.setting` macros (Text+ inputs set with `SetInput`) and the new **OGraf HTML/CSS/JS titles** (21.1). OGraf takes brand fonts and colours directly from web code. It allows at most 20 parameters [BMD-doc].
4. **The AI features divide in two.** Scriptable: transcription, subtitles from audio, SmartSwitch, Smart Reframe, Magic Mask, stabilisation, voice isolation, dialogue leveler, scene-cut detection, IntelliSearch, Slate ID, speech generation and motion deblur [BMD-doc]. UI-only (absent from the API): IntelliScript, Animated Subtitles, AI Audio Assistant, Music Editor and Music Remixer [BMD-doc, by absence].
5. **The craft order is: brief, then message strategy, then concept and treatment, then script, then shot list and gap list, then shoot or source, then paper edit or radio edit, then rough cut, fine cut and picture lock.** Each arrow is a natural client checkpoint. The Trigger Map maps cleanly onto Jobs-to-be-Done "forces of progress". That mapping gives Viska a principled way to turn scored forces into hooks, beats and proof points.

---

## 1. Pre-production practice: from brief to shot list

### 1.1 The chain of documents

| Stage | Document | What it fixes | Typical client checkpoint |
|---|---|---|---|
| Brief | Creative or video brief | Objective, audience, single message, call to action, channels, format, length, budget, deadline, approvers | **Brief sign-off** |
| Strategy | Message house: a roof message, 3 to 4 pillars, proof points | What must be said, and the evidence for it | Usually signed off together with the brief or the concept |
| Concept | 1 to 3 concept routes, each a one-paragraph idea plus references or a mood board | The creative idea and its tone | **Concept choice** |
| Treatment | Prose summary that "reads like a story", with tone, look and structure | The agreed vision written down, before the script is written | **Treatment sign-off** (often merged with the concept) |
| Script (manus) | Two-column AV script: video on the left, audio on the right, one row per beat or line | Exactly what is seen and heard | **Script sign-off** (the costliest one to skip) |
| Visualisation | Storyboard (still panels) or animatic (panels with timing and scratch audio) | Framing, pacing, flow | Optional; standard for ads and complex shoots |
| Breakdown | Shot list (shot size, angle, movement, lens, location, people, props), ordered by location or setup, not by story | Logistics, budget and schedule | Internal, or shared for information |
| Schedule | Production schedule and call sheets | Who, where, when | Internal; the client confirms access, locations and people |

Sources: Videomaker on planning a video ad and on shot lists; StudioBinder on shot list versus storyboard; Evergreen's two-column A/V script wiki; Sailfin on pre-production. Two practitioner points are worth keeping:

- A Hollywood script leaves room for interpretation. An A/V script "should be a 1:1 description of exactly what the viewer will see and hear" (Evergreen helpwiki).
- Shot lists are ordered for shooting efficiency, because "script order is very rarely the most efficient shooting order" (Videomaker). Many corporate pieces skip the formal script and go straight to an interview plan plus a shot list.

**Two-column AV script.** Left column: shot description with shot size (WS/MS/CU), on-screen text and graphics, and the source of the material. Right column: voice-over or synced dialogue, music cues and sound effects, one row per beat so that sound and picture stay aligned. Used in advertising, corporate, documentary and training films. For Viska, each row is a natural data record. Suggested fields: `beat_id`, `force_ids` (from the Trigger Map), `video`, `audio`, `on_screen_text`, `duration_s`, `source` (existing, shoot, license, generate), `asset_refs`, `status`. One file then yields the script document, the shot list, the gap list and later the timeline markers.

**Storyboard versus animatic.** An animatic is the storyboard panels cut together with durations, simple camera moves and scratch audio. Agencies use it to sell pacing to the client before committing money to a shoot (LTX and Morphic glossaries; vendor sources). For Viska an animatic is cheap: still frames (generated or existing) plus generated speech, assembled in Resolve. It works as a "pre-rough-cut" checkpoint.

### 1.2 What a good video brief contains, and what the producer asks

The brief templates (Wedio, Content Snare's 29-question intake, Dream Engine, Venture Videos, Sparkol's 16 questions, MnDOT's public-sector video style guide) agree on these items:

- **Purpose and outcome.** What the video must achieve, made specific: "to inform" is too vague. Which KPI does it move?
- **Audience.** Who watches, and where they are in the customer journey.
- **One or two core messages.** More than that dilutes the film.
- **Call to action.** What the viewer should do next.
- **Channels and format.** Where the video runs, its aspect ratios and length, sound-off viewing, captions.
- **Shelf life.** How long the video must stay relevant, and whether it should be easy to update (MnDOT).
- **Brand assets.** Logo, fonts, colours, tone of voice, references the client likes and dislikes.
- **Budget range, deadlines and approvers.** Who signs off, and how many revision rounds. Content Snare notes that asking about approvers up front limits scope creep.
- **Practicalities** (producer questions from the same sources): locations and access, who can appear on camera and whether they will sign releases, existing footage and photos, music preferences, legal and compliance constraints (claims, regulated wording), language versions.

**Mapping to WDS.** The Product Brief and Trigger Map already answer purpose, audience and motivation. Viska's own intake should only ask what they do not answer: channel, format, length, CTA, budget, deadline, approvers, people and locations available, existing material, and legal constraints.

### 1.3 From audience insight to script beats, hooks and proof points

**Jobs-to-be-Done "forces of progress"** (jobstobedone.org, "The Four Forces"). A person switches when **push** (pain in the current situation) plus **pull** (attraction of the better life) outweigh **anxiety** (fear of the new) plus **habit** (comfort of the old). Teams tend to over-invest in pull and ignore anxiety and habit, which often kill the decision.

**The Trigger Map maps directly onto this:**

| Trigger Map element | JTBD force | Role in the film |
|---|---|---|
| Driving force **away from** (pain, fear in the current state) | Push | **Hook and problem beat.** Name the specific pain so the viewer feels seen. |
| Driving force **toward** (desired outcome) | Pull | **Vision or payoff beat.** Show the better life, not the feature list. |
| Fears about the solution (often among the away-from forces) | Anxiety | **Proof beats.** Testimonials, numbers, guarantees, "how it works", a real face. |
| Status quo, "it works well enough" | Habit | **Ease or "first step" beat, and the CTA.** Make the first step small. |

This mapping is my synthesis [Unverified as an industry standard]. The JTBD sources do not discuss video.

**Standard short-form structure** (Lemonlight, Celtx and others): **hook, problem, solution, proof, CTA**, with a single message and the viewer as the hero ("the product is the helper"). Three guidelines from the same sources:

- The hook must earn the next few seconds, because viewers scroll, skip or mute almost at once.
- Proof must match the claim, since irrelevant proof hurts.
- One CTA only.

Writing guidance: write for the ear (contractions, short sentences); draft several hooks and test one change at a time.

**Message house** (Smart Insights, Benjamin Ball, Umbrex): one roof message, 3 to 4 pillars, and proof points under each pillar. Proof points must agree with source documents, so the film never makes claims that conflict with policy or regulatory wording (MangoApps). Smart Insights recommends keeping long evidence lists in a separate document.

**Proposed Viska rule** [Unverified, design proposal]:

1. Pick the primary persona and the top 2 to 3 forces by score (Frequency + Intensity + Fit).
2. The highest-scoring away-from force becomes the hook.
3. The highest-scoring toward-force becomes the payoff.
4. Each proof beat must name the force it answers and the evidence it uses, where the evidence comes from the brief or from interviews.
5. A beat that serves no force is cut, or flagged for the client.

This gives the same traceability the Trigger Map gives Freya.

### 1.4 Interview-based films: question design and "writing in the edit"

**Question design** (Rev, Videomaker, LibreTexts *Documentary Culture* ch. 12, Premiumbeat, Lot1 substack):

- Ask open questions. Yes/no questions give unusable answers. "How" questions yield process and structure; "why" questions yield emotion.
- Ask the subject to **restate the question in the answer**, because the interviewer is cut out. Explain this before the shoot and remind them during it.
- Start with easy, less important questions and narrow toward the important ones.
- After a good answer, a plain restatement ("so that changed everything") often draws a better soundbite. Overused, it becomes leading.
- Prompts such as "What happened next?" and "What makes you say that?".

**For Viska** [Unverified, design proposal]: derive the questions from the Trigger Map. For each target force, ask one story question ("Tell me about the last time…"), one feeling question ("What worried you most when…"), and one proof question ("What changed afterwards, concretely?"). That way the interview is designed to yield the hook, the payoff and the proof bites the script needs.

**Writing the film in the edit:**

- **Paper edit** (Reduct, NYFA, Convert Audio to Text). Transcribe, timecode each paragraph, select more than you need, and arrange the quotes into a beginning, middle and end on paper. Each quote references its source clip and timecode, with notes on B-roll and music. Everyone can review and comment on it before the editor opens the NLE.
- **Radio edit** (No Film School, Lynda/LinkedIn Learning, Todd Boruff, CreativeLive/Ed Kashi). Build the story from interview audio only, so that it "sounds right, as though it were going to play on the radio". Then cover jump cuts with B-roll. "If the audio version of the story isn't engaging, no amount of visual polish will make it interesting." Some editors prefer to start from the visuals (the Lynda instructor). Audio-first is the dominant documentary practice but not a rule.

**Viska can automate both**:

1. `MediaPoolItem.TranscribeAudio(useSpeakerDetection=True)` and then `GetTranscription()`. The result has segments with word-level start and end timecodes and the speaker [BMD-doc, added in 21.1; untested].
2. Viska selects quotes against the script beats and forces, and writes the paper edit as a document for the client.
3. Viska builds the radio edit with `AppendToTimeline([{mediaPoolItem, startFrame, endFrame, mediaType: 2, trackIndex, recordFrame}])`.
4. B-roll is placed on V2 above it.

Practitioner warning (Primal Video, testing the Resolve 21.1 MCP route): Resolve's own transcription skipped speech, leaving false starts in the cut. A word-timestamped external transcript (Deepgram) gave a cleaner result [User report].

---

## 2. Gap analysis and asset audit

### 2.1 Inventory practice

The sources here are mostly vendor blogs (AdPipe, Dream Engine, Remedy Films). The consistent points:

- Existing footage goes unused because it cannot be found: bad file names and no tags. "When finding footage takes longer than shooting new footage, teams stop looking" (AdPipe).
- An audit means cataloguing what exists, organising it by content type, making it searchable, and recording **rights and clearance per asset**, so that every reused clip is cleared for the intended use (AdPipe).
- A shoot that duplicates owned material is "money spent twice". New shoots should be planned modularly (wide, medium and close coverage, isolated elements) so they feed future edits.

Viska already has most of this. `media-catalog` and `innehall.csv` hold descriptions, keywords, ratings and favourites [Tested]. Resolve 21 adds **IntelliSearch**, a content and face search, scriptable through `AnalyzeForIntellisearch(identifyFaces, isBetterMode)` [BMD-doc]. It also adds **Slate ID**, which reads clapperboards into metadata, and **Audio Classification**, which tags audio by category [BMD-doc].

### 2.2 The gap list: decide per beat whether to use, shoot, license or generate

For each script row, compare the required shot with the catalogue. A suggested decision order [Unverified, synthesis of the sources below]:

| Option | Use when | Cost | Main risks |
|---|---|---|---|
| **Use existing** | A catalogue hit matches the beat, the quality is good enough, and rights and releases cover this use | Lowest | Release scope (people filmed for an internal event, now in an advert); outdated look, brand or staff |
| **Shoot** | Real people, places or product of the client are central to proof or authenticity (testimonials, "this is us") | Highest per shot; batch by location | Schedule, weather, access, releases, reshoots. Confirm reshoots at the rough cut, while they are still feasible (Frame.io). |
| **License stock** | Generic context: cityscapes, abstract and mood shots, things impossible to shoot | Medium | Royalty-free licences often exclude broadcast or festivals. Editorial-only clips may not be used in ads. Identifiable people or property need releases. Check platform scope. (Bridgeman, Dissolve, Getty, Motion Elements) |
| **Generate (AI)** | Illustrative, stylised or abstract visuals, backgrounds, animatic frames, temporary voice-over | Low money, some time | **EU AI Act Art. 50(4), applies from 2 Aug 2026:** the deployer (brand or agency) must visibly disclose a deepfake, meaning content resembling real persons, objects, places or events. Generic stylised visuals likely fall outside. The Commission guidance is non-binding. Fines up to EUR 15 million or 3 % of turnover. Other law still applies: IP, personality rights, advertising and consumer law. Never generate fake testimonials or "real customer" proof. (SRD Rechtsanwälte, Lewis Silkin, Makeinfluence, Stibbe) |
| **Graphic or motion design** | Data, numbers, process explanations, quotes | Low to medium (templated) | Accuracy of claims. Brand consistency. |

**Risk rule for proof beats** [Unverified, design proposal]: proof beats that answer **anxiety** must be real (filmed people, real numbers, real product). They may never be stock or AI, because a fake proof undermines exactly the force it should reduce. Stock and AI are for context and pull imagery.

**Budget trade-off.** A shoot day is the expensive, fixed unit. So group every "shoot" row by location and person, and promote a stock or AI row to "shoot" when the crew is on that location anyway. Present the client with the gap list as a table of beat, need, proposed source, cost and risk. That table is the natural **gap-list sign-off** before money is spent.

---

## 3. Automated assembly in DaVinci Resolve Studio 20/21

Baseline: Resolve Studio 21.1.1. Since 21.1 the Python API requires Studio [BMD-doc README, CHANGELOG; Tested in resolve.md]. 21.1 ships its own interpreter, `C:\Program Files\Blackmagic Design\DaVinci Resolve\ResolvePython\ResolvePython.exe` (Python 3.14). With it, `import DaVinciResolveScript` works without the environment variables that resolve.md sets; pip is not supported [BMD-doc README]. A headless mode exists (`-nogui`) [BMD-doc]. 21.1 also deprecates overloaded signatures. Use the dict forms (`AppendToTimeline([{...}])`, `SetProperties({...})`, `SetMetadata({...})`, `ImportMedia([{"FilePath":…}])`) [BMD-doc README]. resolve.md still uses `SetProperty` and `AddItemListToMediaPool(path)`, which now count as deprecated calling conventions.

### 3.1 What the Python API can do (21.1)

All entries are [BMD-doc] (type stubs, README, CHANGELOG) unless marked otherwise.

**Project and media**
- Create, load, import and export projects (`.drp`); cloud projects.
- `MediaPool.ImportMedia`, `AddSubFolder`, `MoveClips`, `RelinkClips`.
- `LinkProxyMedia` [Tested], `LinkFullResolutionMedia`.
- Metadata and third-party metadata, clip colour, flags, markers with `customData`.
- `AutoSyncAudio` (waveform or timecode).
- `CreateMulticamClip` (21.1).
- `ImportFolderFromFile` (`.drb`).

**Timelines**
- `CreateEmptyTimeline`, `CreateTimelineFromClips(name, [{mediaPoolItem, startFrame, endFrame, recordFrame}])`.
- `AppendToTimeline([{mediaPoolItem, startFrame, endFrame, mediaType 1=video/2=audio, trackIndex, recordFrame}])`: in/out points, a track and a record position per clip [BMD-doc; audio-only append Tested].
- `ImportTimelineFromFile(path, {timelineName, importSourceClips, sourceClipsPath, sourceClipsFolders})` for AAF, EDL, XML, FCPXML, DRT, ADL and OTIO [BMD-doc; FCPXML 1.9 and FCP7 XML Tested].
- `Timeline.ImportIntoTimeline` (AAF options).
- `DuplicateTimeline`.
- `Export` to AAF, DRT, EDL, FCP 7 XML, FCPXML 1.8/1.9/1.10, OTIO, ALE, CSV/TAB, HDR and Dolby Vision metadata. FCPXML 1.3 to 1.7 export has been dropped.

**Tracks**
- `AddTrack("video"|"audio"|"subtitle", subType)`, `DeleteTrack`, `SetTrackName`, `SetTrackEnable`, `SetTrackLock`.

**Items**
- `GetItemListInTrack`, `DeleteClips(items, rippleDelete)`, `SetClipsLinked`, `SetClipEnabled`.
- Takes (`AddTake`, `SelectTakeByIndex`, `FinalizeTake`).
- `CreateCompoundClip`, `CreateFusionClip`.

**Static properties: `SetProperties` (all-or-nothing, validated)**
- Pan, Tilt, ZoomX/Y, Rotation, Anchor, Pitch/Yaw, Flip.
- Crop and softness, Opacity, CompositeMode.
- DynamicZoomEnabled and DynamicZoomEase. Ken Burns from start and end rectangles is only partly scriptable: the start and end rectangles themselves are not exposed [Unverified].
- Lens distortion; retime process and motion estimation; scaling.
- Audio volume, pan and pitch.
- Voice isolation amount and Dialogue Leveler (active timeline only).

**New in 21.1**
- `TimelineItem.AddTransition({type: e.g. "Cross Dissolve", category: "simple"|"fusion"|"ofx"|"audio", position: "start"|"end", alignment: "left"|"center"|"right", duration: frames})`. This means **transitions are now scriptable** [BMD-doc; also reported by Newsshooter's 21.1 coverage; untested here].
- `SetSpeed({Percentage, PitchCorrection, StretchKeyframesToFit, RippleTimeline})`: constant speed, and `0.0` gives a freeze frame. Variable ramps are not covered.
- `SetFades({FadeIn, FadeOut})` in frames: video and audio fade handles.
- `PerformMulticamSmartSwitch(settings)`, `FlattenMulticam`, `Timeline.AutoAlignClips`.
- `Timeline.NormalizeAudioLevel(items, {normalizationMode, targetLevel, targetLoudness})`, for example −14 or −16 LUFS for web.
- `MediaPoolItem.GetTranscription()`: word-level timing and speaker.
- Render presets, quick export, and audio render codecs.

**Generators and titles**
- `InsertGeneratorIntoTimeline`, `InsertFusionGeneratorIntoTimeline`, `InsertOFXGeneratorIntoTimeline`, `InsertTitleIntoTimeline`, `InsertFusionTitleIntoTimeline(name)`, `InsertFusionCompositionIntoTimeline`.
- These insert at the playhead. Position first with `SetCurrentTimecode("01:00:10:00")`, which takes a timecode string, not a frame number [User report, Blackmagic forum].
- Which track receives the insert is not documented [Unverified, test it].

**Fusion**
- `AddFusionComp`, `ImportFusionComp(path)`, `ExportFusionComp`, `GetFusionCompByIndex` and `GetFusionCompByName`, which return a Fusion composition object for full Fusion scripting (3.3).

**Colour**
- `SetCDL` [Tested]; LUT on a node [Tested] (`SetLUT` is listed as deprecated on TimelineItem, and node graph calls replace it).
- `ApplyGradeFromDRX`, `CopyGrades`, colour groups, versions, `ExportLUT`.

**AI on clips**
- `SmartReframe()` (Smart Reframe) [Tested; slow modal].
- `CreateMagicMask("F"|"B"|"BI")` and `RegenerateMagicMask`.
- `Stabilize()`.
- `Timeline.DetectSceneCuts()`.
- `Timeline.CreateSubtitlesFromAudio({language incl. AUTO_CAPTION_SWEDISH, captionPreset, charsPerLine, lineBreak, gap})`.
- `TranscribeAudio(useSpeakerDetection)`, `PerformAudioClassification`, `AnalyzeForIntellisearch`, `AnalyzeForSlate`.
- `RemoveMotionBlur`.
- `Project.GenerateSpeech({TextInput ≤ 350 chars, VoiceModel, CustomVoiceFile, Speed, Pitch, AddToTimeline, AudioTrack})`, which is useful for temp voice-over and animatics.
- Several of these need models from the Extras Download Manager, and calls return False otherwise [BMD-doc].

**Render**
- `SetRenderSettings`, `AddRenderJob`, `StartRendering(jobId)`, status calls [Tested].
- Render settings can export subtitles (`ExportSubtitle`, `SubtitleFormat`).

**Still not possible from the API** [BMD-doc, by absence from the type stubs]:

- **Keyframes on Edit-page Inspector properties.** `SetKeyframeMode` only toggles the Colour page mode. Dynamic Zoom is a two-state animation, not free keyframes.
- **Variable speed ramps.**
- **Audio automation curves.**
- **Applying an Animated Subtitle template or a track style.**
- **IntelliScript.**
- **AI Audio Assistant.**
- **Music Editor and Music Remixer.**

### 3.2 What needs FCPXML or OTIO import, and what survives

**Resolve's own manual**, chapter 22 "Importing and Conforming Timelines", pp. 468–472 [BMD-doc], covers effects that are converted on import of FCP 7 XML, FCP X XML (FCPXML), AAF and EDL:

- **Video transitions.** Supported from FCP 7 and FCP X XML: ten types, among them Cross Dissolve, Additive Dissolve, Dip to Color Dissolve, Edge, Center, Clock and Venetian wipes, and Cross, Diamond and Oval iris. EDL gives Cross Dissolve only.
- **Opacity, position, scale and rotation** from FCP X, Premiere or FCP7 XML. "If these settings have been keyframed, the animation will appear in DaVinci Resolve." [BMD-doc; position keyframes Tested in resolve.md as `adjust-transform` with `keyframeAnimation`. Note: the value is a percentage of frame height.]
- **Ken Burns** from FCP X becomes animated Dynamic Zoom.
- **Speed.** Linear and variable speed effects from XML (FCP X XML also carries frame-blend or optical-flow choice and Bezier speed transitions). Converted as one speed keyframe per frame. EDL gives linear speed only. Freeze frames are listed as AAF-only in the table; the PDF table layout is garbled in extraction, so test it [Unverified].
- **Compound clips** from FCP X and nested sequences from FCP7 become compound clips. FCP X multicam and synchronised clips also become compound clips.
- **Eight composite modes** from XML.
- **Colour.** Only FCP X XML colour-board data imports, as primary corrections.
- **Text.** FCP X and FCP7 text generators import as **basic Text generators**, with "some, but not all, formatting". So branded titles should not come in through FCPXML. Insert Fusion or OGraf titles by script instead.
- **Stills** (TIF, JPG, PNG, DPX, TGA, DNG) longer than one frame come in as ordinary clips.
- **Unsupported effects** are not shown, but are preserved for round-trip export.

**FCPXML versions.** The manual does not list import versions. The API exports 1.8, 1.9 and 1.10 [BMD-doc]. Viska's `mediabank.py` writes `fcpxml version="1.9"` and it imported correctly in 21.1.1 [Tested]. The `.fcpxmld` bundle (a folder with Info.fcpxml, which FCP writes for 1.10 and later) is reported not to import; use a flat `.fcpxml` file [User report, Larry Jordan]. Import of 1.11 and later is **unknown, so test it**. Recommendation: write 1.9 or 1.10.

**Known FCPXML import quirk** [Tested]: imported Cross Dissolves become their own items on the track (`GetMediaPoolItem()` returns None). Filter them out before per-clip operations. Import fails while Resolve is rendering.

**OTIO** [BMD-doc, manual pp. 526–527 and 4160]:
- Resolve imports and exports `.otio` (timeline only) and `.otioz` (timeline plus media bundle).
- OTIO's own feature matrix shows that the format carries tracks, markers, nesting, **transitions, linear speed effects**, CDL and image sequences. It does **not** carry "fancy" (variable) speed or audio/video effects (OpenTimelineIO docs).
- Neither Blackmagic nor the OTIO documentation says which OTIO features Resolve maps on import. Transforms and keyframes have no standard OTIO schema [Unverified, test it].

**Conclusion for Viska:**
1. Build the cut in Python: AppendToTimeline with in/out points, then AddTransition, SetSpeed, SetFades, SetProperties.
2. Use **FCPXML only where keyframes or speed ramps are needed**: Ken Burns or pan, animated scale and opacity, variable speed.
3. Use **Fusion or OGraf for titles and graphics**.
4. Use OTIO for exchange with other tools, not as the primary build path.

### 3.3 Brand titles and graphics

**A. Fusion title templates (`.setting` macros)** [BMD-doc, Developer/Fusion Templates/README.txt]:
- Install under `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Templates\Edit\Titles\` (per user) or `C:\ProgramData\...\Fusion\Templates\Edit\Titles\` (all users). They can be bundled as `.drfx` (a zip with an `Edit/Titles/...` hierarchy). A PNG of the same name serves as the icon.
- A title is a generator macro built on **Text+** or Text3D. Expose StyledText, Font, Style, Size and the colour controls in the Macro Editor so they show in the Edit Inspector.
- Use the **Anim Curves** modifier, not fixed keyframes, so the animation stretches to the clip length.
- Bundled assets such as a logo PNG or a LUT are referenced with the `Setting:` path map (for example `Setting:logo.png`).
- Restart Resolve after adding templates.

So Viska can generate one `.setting` per brand (a text file in Lua-table syntax) with the client's font, colours and logo. It installs the file, then calls `timeline.InsertFusionTitleIntoTimeline("<template name>")` and fills the text by script.

**Setting Text+ by script:**

```python
item = timeline.InsertFusionTitleIntoTimeline("Text+")      # or a brand template name
comp = item.GetFusionCompByIndex(1)                          # [BMD-doc]
tool = comp.GetToolList(False, "TextPlus")[1]                # [Fusion-doc] GetToolList(selected, type); Python returns a dict, 1-based
comp.Lock()                                                  # [Fusion-doc] batch mode while editing
tool.SetInput("StyledText", "Rubrik")                        # [Fusion-doc] SetInput(id, value[, time])
tool.SetInput("Font", "Inter"); tool.SetInput("Style", "Bold")
tool.SetInput("Red1", 0.95); tool.SetInput("Green1", 0.4); tool.SetInput("Blue1", 0.1)   # colour as separate float inputs [Unverified input IDs]
comp.Unlock()
```

- The community has converged on this route. A StoryToolkitAI GitHub issue shows `InsertFusionTitleIntoTimeline("Text+")` plus setting `StyledText`. A Blackmagic forum moderator gave the same path in June 2025 but said it was untested [User report]. Not yet tested by Viska.
- The tool's script ID is `TextPlus` [User report].
- Per the Fusion guide, `SetInput` handles only simple data types (numbers and strings). That is why colours are set as separate float channels [Fusion-doc].
- In a macro, the inputs are usually exposed on the macro group. Address them by the published names, or find the inner Text+ tool. Test both [Unverified].

**Keyframed motion through Fusion** [Fusion-doc]:

```python
tool.Size = comp.BezierSpline()
tool.Size[0] = 0.5
tool.Size[24] = 1.0
```

Point inputs such as `Center` use `comp.Path()`. `comp.AddTool("Transform")` adds tools. This is the scripted way to get real keyframes, such as a Ken Burns move on a stills clip turned into a Fusion clip with `Timeline.CreateFusionClip([item])`, without FCPXML. It is untested in Resolve 21 [Unverified].

**B. OGraf HTML titles (21.0/21.1)** [BMD-doc, Developer/OGraf HTML Templates]:
- OGraf is the EBU open standard for HTML, CSS and JavaScript broadcast graphics. Resolve shows OGraf graphics as **Titles in the Edit page**, rendered through Fusion's OGrafLoader (Chromium Embedded Framework on Windows).
- The manifest `.ograf.json` must set `supportsNonRealTime: true`.
- The JavaScript web component must implement `goToTime()` deterministically: no timers, no `Math.random` without a seed, all state computed from the timestamp.
- At most **20 parameters**; a colour counts as one.
- Parameters appear as native Inspector controls.
- 21.1 added scheduled play, stop and custom actions, and delivery of Inspector values and **keyframes** as `updateAction` events.
- Fonts must be bundled; preload them with `document.fonts.load` before frame 0.
- A linter (`Scripts/lint-ograf.py`) and a `.drfx` packager ship with Resolve.
- Install to `%APPDATA%\...\Fusion\Templates\Edit\Titles\OGraf\`.

**Why this matters for WDS:** Freya's design tokens (CSS) and brand fonts can drive titles, lower thirds and end cards directly, with no translation to Fusion. Freya and Viska could share one brand graphics package. Whether the OGraf parameters can be set by script after insertion (as Fusion inputs on the OGrafLoader tool) is **not documented** [Unverified]. If they cannot, Viska writes one template per text variant, or bakes the text in as parameter defaults.

**C. Lottie** playback also exists in 21.1 (WebKit or CEF rendering, Media Storage previews) [BMD-doc OGraf CHANGELOG]. Its details are outside this research.

### 3.4 AI features: what they do and whether they are scriptable

| Feature (version) | What it does | Scriptable? |
|---|---|---|
| **IntelliScript** (20, Studio) | Transcribes the selected clips and builds a timeline from a `.txt` or Final Draft `.fdx` script of **spoken text only**, with full stops after sentences. Best take on V1, alternative takes on higher tracks, disabled. Picks the "best" take by dialogue match only, with no use of good-take metadata. Tolerates ad-libs. (Manual p. 1003.) Users report empty timelines with `.odt` input, clips left untrimmed in a beta, and only about 20 % use of the wanted sentences. | **No** [BMD-doc, absent from the API]. Viska can do the same itself: `GetTranscription()` word timing plus its own matching against the AV script, then `AppendToTimeline` with in/out points. That also lets it rank takes by the Trigger Map, which IntelliScript cannot. |
| **AI Animated Subtitles** (20, Studio) | Fusion title templates in Titles → Animated (Lollipop, Rotate, Slide In, Statement, Word Highlight), dragged onto a **subtitle track header**. Word timing comes from the transcription engine. Custom Fusion templates are possible. (Manual p. 1240; Larry Jordan.) | **Partly.** `CreateSubtitlesFromAudio` (including Swedish) and render-time subtitle export are scriptable. Applying the animated template to the track is **not** [BMD-doc, by absence]. Options: a manual one-click step by the person; per-phrase `InsertFusionTitleIntoTimeline` driven by word timings; or an OGraf caption template. |
| **AI Multicam SmartSwitch** (20, Studio) | Picks angles from speaker detection and lip movement, plus wide-shot rules (minimum edit duration, change delay, wide-angle frequency, wide shot for intro, outro and silence). (Manual p. 1045.) | **Yes, from 21.1**: `PerformMulticamSmartSwitch(SmartSwitchSettings)`, `CreateMulticamClip`, `FlattenMulticam` [BMD-doc]. |
| **AI Audio Assistant** (20, Studio) | Timeline → AI Tools → Audio Assistant. Organises and colour-codes tracks, evens dialogue, sets faders for music, effects and dialogue against a chosen delivery standard. Can be undone. (Manual pp. 781, 1123, 3969.) | **No** [BMD-doc, by absence]. A partial substitute: `NormalizeAudioLevel` with a loudness target (21.1), voice isolation and dialogue-leveler properties, `ApplyFairlightPresetToCurrentTimeline` (20.2.2). |
| **Smart Reframe** (Studio) | Reframes for another aspect ratio: Auto, Pan only or Tilt only. | **Yes**: `TimelineItem.SmartReframe()`, `GetSmartReframeStatus()` [BMD-doc; Tested: about 0.7 fps on a Surface Pro 7, modal]. |
| **Magic Mask** (Studio) | AI person or object mask on the Colour page. | **Partly**: `CreateMagicMask("F"/"B"/"BI")` and `RegenerateMagicMask` exist [BMD-doc]. Choosing what to mask (strokes) is not exposed [Unverified]. |
| **Voice Isolation, Dialogue Leveler** (Studio) | Removes noise from dialogue; levels speech. | **Yes**: track level (`Timeline.SetVoiceIsolationState`) and clip level (`TimelineItem` properties) [BMD-doc]. |
| **Music Remixer** (Studio) | Splits music into stems (voice, drums, bass, other) as a Track FX. | **No** [BMD-doc, by absence]. |
| **Music Editor** (20/21) | Extends or shortens music to the edit length without time-stretching; 21.1 keeps more content and avoids repetition. | **No** [BMD-doc, by absence]. Viska places music by script and asks for this one UI step, or cuts the music itself on the bar grid. |
| **IntelliSearch, Slate ID, Audio Classification** (21) | Content and face search; reading slates; audio categories. | **Yes** [BMD-doc]. |
| **AI Speech Generator** (21) | Text to speech, including a custom voice file. | **Yes**: `Project.GenerateSpeech`, at most 350 characters per call [BMD-doc]. Useful for scratch voice-over in animatics. Final voice-over with a cloned real voice raises consent and AI Act questions. |
| **Detect Scene Cuts** | Splits flattened footage at its cuts. | **Yes** [BMD-doc]. |
| **AI Assistants / MCP** (21.1) | File → Setup AI Assistants registers a built-in MCP server with Claude Desktop, Claude Code and others. Example uses: render presets, timeline breakdowns, renaming, markers to CSV, LUT on node 2, settings checks, reframing to 9:16. Scripts it creates "share the same access permissions" as the assistant. (Manual pp. 4317–4318.) | Not used, by WDS rule (resolve.md). Reviewers do not say whether it exposes more than the Python API. Primal Video's hands-on test reached a good rough cut, timed titles and branded variants [User report]. |

---

## 4. Patterns for an agent that leads

### 4.1 How the human roles divide the decisions

Sources: Dream Engine, Casual Films, Skillman, Frame.io.

- **Producer.** Owns brief, budget, schedule and client contact, "delivered on brief, on budget and on time". In corporate work the producer also proposes creative solutions and references.
- **Director.** Owns the creative vision and its execution on set. In corporate work the director is often also the camera operator.
- **Editor.** Shapes the story in post. The director works closely with the editor through the rough cut. In client work the producer's cut is usually final; directors rarely have the last word unless they also produce (Frame.io).

Viska holds all three roles. It should therefore **separate its own hats explicitly** in what it presents:

- As producer: "this costs X, risk Y".
- As director: "this is the idea and why it serves force F".
- As editor: "this is the cut; these three choices are open".

### 4.2 Client checkpoints

Combined from Frame.io, Dropbox, Tribe Pictures, UBC and Fast.io:

| # | Checkpoint | Client approves | Feedback focus | What gets harder to change after it |
|---|---|---|---|---|
| 1 | **Brief sign-off** | Objective, audience (persona and forces), single message, CTA, channels and format, budget, deadline, **named approvers and number of rounds** | Is this the right problem? | Everything |
| 2 | **Concept or treatment** | One route, tone, references | Does this feel like us? | Tone, format |
| 3 | **Script sign-off (AV script) plus gap list** | Every line of voice-over and on-screen text, proof points and claims, use/shoot/license/generate choices, cost | Words, claims, legal | Words, shoot plan, spend |
| 4 | (Optional) **Animatic or paper edit** | Pacing, order of quotes | Story flow | Structure |
| 5 | **Rough cut** | Structure, story, pacing, "does it meet the brief?", no polish | Narrative only. Confirm any reshoots now. | Structure |
| 6 | **Fine cut** | Graphics and titles, brand details, music, colour direction, mix, legal and compliance | Details | Picture |
| 7 | **Picture lock, then final delivery** | Only that the requested changes were made; who gives final sign-off | Not a reopening | Everything; changes after lock cost money (Frame.io) |

**Practices worth building in:**
- Two or three reviewers with real authority.
- **Consolidate feedback into one list before revising.**
- Name versions by stage (`rough-r1`, `fine-r2`).
- Say what kind of feedback each round wants.
- Show inexperienced clients a more polished cut rather than a raw one (Frame.io).

Viska's existing reel versioning (v4…v7) and the green-flag approval in `media-catalog` fit this model.

### 4.3 What the agent decides itself and what it asks

Anthropic's "Building effective agents" says agents work independently and pause "for human feedback at checkpoints or when encountering blockers". They should get "ground truth from the environment at each step", with stopping conditions. A generator and evaluator loop ("evaluator-optimizer") suits work with clear criteria, such as checking a cut against the script and the forces. The secondary agent-pattern sources (agentpatterns.ai, Rework, handsonai) converge on gates before irreversible, costly or ambiguous steps, with the number of gates matched to the stakes.

**Proposed split for Viska** [Unverified, design proposal]:

| Viska decides (and reports) | Viska proposes; the person chooses | Viska must ask (blocking) |
|---|---|---|
| Craft execution within an approved script: shot choice among equivalent takes, trims, pacing within ±10 % of target length, B-roll coverage, transition types from the brand palette, colour balance (LUT per clip), loudness target, subtitle line breaks | Concept routes (2–3, with a recommendation), the hook among 2–3 drafted variants, music track, which interview bites carry proof, use/shoot/license/generate per gap with cost and risk | Anything that **spends money** (stock licences, crew, paid generation above a threshold) |
| Catalogue, proxies, bins, transcription, paper-edit draft, radio-edit assembly, technical QC (offline media, black frames, loudness, safe areas) | Interview question list (from the forces) | Anything **public or irreversible**: publishing, sending to the client's audience, deleting originals |
| Versioning, render presets, export structure | Cuts at each checkpoint, with 1–3 open questions, not "what do you think?" | **Claims and proof:** every number, testimonial and comparative claim must be traceable to a source the client confirmed |
| Flagging conflicts (a beat serving no force; a proof beat sourced from stock or AI) | | **People and rights:** appearing on camera, releases, use of a person's voice or likeness (including AI voice), any AI content that resembles real people, places or events (Art. 50 disclosure) |
| | | Changes after **picture lock**, and anything outside the signed brief (scope change) |

**Leading behaviour, in WDS style.** At each phase Viska states what it will do next and why (tied to persona and force), does it, and returns with a finished artefact plus the few decisions that are genuinely the client's. It does not wait for commands between checkpoints. It stops at the gates in the right-hand column.

---

## 5. Implications and next steps for Viska and resolve.md

1. **Update resolve.md** (not done here; this is research only):
   - Transitions (`AddTransition`), constant speed and freeze frames (`SetSpeed`), and fades (`SetFades`) are scriptable in 21.1.
   - Keyframes and variable speed are still not; use FCPXML or Fusion BezierSpline for those.
   - Switch to the non-deprecated dict calls.
   - Note the bundled `ResolvePython.exe`.
2. **Test these, in order of value:**
   - `AddTransition` (simple Cross Dissolve, then a Fusion transition)
   - `InsertFusionTitleIntoTimeline` and setting Text+ `StyledText`, `Font` and colour
   - an OGraf brand lower third
   - `GetTranscription` word timing on Swedish speech
   - `CreateSubtitlesFromAudio(AUTO_CAPTION_SWEDISH)`
   - `NormalizeAudioLevel` to −14 LUFS
   - FCPXML 1.10 and 1.11 import
   - OTIO import with transitions and speed
3. **Data model:** one `script.yaml` (or CSV) with one row per beat and fields for Trigger Map force IDs and source type. It renders the AV script, shot list, gap list, paper edit and timeline markers (`AddMarker` with `customData` = beat ID), mirroring how trigger-map.yaml is rendered.
4. **Brand package:** Fusion `.setting` and/or OGraf templates generated from `brand/visual-identity` and `brand/design-system`, installed per user, and listed in a tool file.

---

## Sources

### Blackmagic Design (primary)
- Local, installed with Resolve Studio 21.1.1: `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.md`, `CHANGELOG.md`, `DaVinciResolveScript.pyi`, `Examples\2_compositions_from_timeline_clips.py`
- Local: `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Fusion Templates\README.txt`
- Local: `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\OGraf HTML Templates\README.txt`, `CHANGELOG.md`, `Documentation\02-Resolve-Integration.md`, `05-Properties-and-Controls.md`, `07-Troubleshooting.md`, `09-Template-Authoring-Guide.md`
- Local: *DaVinci Resolve Reference Manual* `C:\Program Files\Blackmagic Design\DaVinci Resolve\Documents\DaVinci Resolve.pdf`: ch. 22 Importing and Conforming Timelines (pp. 468–472, 526–527); ch. 47 Text Based Editing, IntelliScript (p. 1003); Multicam SmartSwitch (p. 1045); ch. 59 Subtitles, AI Animated Subtitles (p. 1240); Audio Assistant (pp. 781, 1123, 3969); Exporting to OTIO (p. 4160); ch. 201 Using DaVinci Resolve with AI Assistants (pp. 4317–4318)
- Fusion 8 Scripting Guide: https://documents.blackmagicdesign.com/UserManuals/Fusion8_Scripting_Guide.pdf
- Earlier Viska findings: `C:\dev\WDS\whiteport-design-studio-viska\agents\wds\tools\resolve.md`, `agents\wds\tools\resolve\mediabank.py`

### Resolve 20/21 coverage and user reports
- Newsshooter, DaVinci Resolve 21.1: https://www.newsshooter.com/2026/09/07/blackmagic-design-davinci-resolve-21-1/
- ProVideo Coalition, "DaVinci Resolve 21.1 is a huge update": https://www.provideocoalition.com/davinci-resolve-21-1-is-a-huge-update/
- Digital Production, "Resolve 21.1 adds MCP and finally gets presets": https://digitalproduction.com/2026/09/08/resolve-21-1-adds-mcp-and-finally-gets-presets/
- YMCinema, Resolve 21.1 MCP: https://ymcinema.com/2026/09/17/davinci-resolve-21-1-mcp-ai-assistants-control-edit/
- Primal Video, "I Let AI Edit My Video in DaVinci Resolve": https://primalvideo.com/guides/davinci-resolve-ai-assistance/
- No Film School, Resolve 21.1: https://nofilmschool.com/davinci-resolve-update-21-1
- iClarified, Resolve 20 features: https://www.iclarified.com/96951/blackmagic-design-unveils-davinci-resolve-20-with-over-100-new-features-and-ai-tools-video
- ProVideo Coalition, Resolve 20 (IntelliScript): https://www.provideocoalition.com/blackmagic-introduces-davinci-resolve-20/
- CineD, Resolve 20 beta: https://cined.com/davinci-resolve-20-released-in-public-beta-with-ai-powered-features
- Blackmagic forum, IntelliScript issues: https://forum.blackmagicdesign.com/viewtopic.php?p=1147887, https://forum.blackmagicdesign.com/viewtopic.php?p=1138565
- Larry Jordan, animated captions in Resolve 20: https://larryjordan.com/articles/create-animated-captions-using-davinci-resolve-20/
- Larry Jordan, round-tripping FCP and Resolve: https://larryjordan.com/articles/round-tripping-projects-between-final-cut-pro-and-davinci-resolve/
- StoryToolkitAI issue #14 (Text+ via script): https://github.com/octimot/StoryToolkitAI/issues/14
- Blackmagic forum, editing Text+ text by script: https://forum.blackmagicdesign.com/viewtopic.php?p=1156041
- Blackmagic forum, InsertTitleIntoTimeline: https://forum.blackmagicdesign.com/viewtopic.php?p=774612
- Blackmagic forum, SetCurrentTimecode: https://forum.blackmagicdesign.com/viewtopic.php?p=813120
- Blackmagic forum, StyledText keyframes: https://forum.blackmagicdesign.com/viewtopic.php?p=251800
- OpenTimelineIO feature matrix: https://opentimelineio.readthedocs.io/en/latest/tutorials/feature-matrix.html

### Pre-production, scripting, interviews and editing
- Videomaker, planning a commercial: https://www.videomaker.com/planning-a-commercial/
- Videomaker, shot lists: https://www.videomaker.com/how-to/planning/organization/how-to-make-an-awesome-shot-list-for-your-film-or-video-project/
- StudioBinder, shot list versus storyboard: https://www.studiobinder.com/blog/shot-list-vs-storyboard/
- Evergreen, A/V two-column script and shot list: https://helpwiki.evergreen.edu/wiki/index.php/A/V_Two_Column_Script_and_Shot_List
- Sailfin, video pre-production: https://www.sailfinproductions.com/what-is-video-pre-production
- Scr8 AV two-column template: https://templates.openoffice.org/de/node/2957.html
- LTX, animatic: https://ltx.io/glossary/animatic
- Wedio, video creative brief template: https://www.wedio.com/en/templates/video-creative-brief-template
- Content Snare, video production questionnaire: https://contentsnare.com/form-templates/video-production-questionnaire/
- Dream Engine, video production brief: https://www.dreamengine.com.au/tips-and-resources/how-to-create-a-great-video-production-brief/
- Venture Videos, video brief: https://venturevideos.com/insight/how-to-write-a-video-brief
- Sparkol, 16 brief questions: https://blog.sparkol.com/16-questions-to-answer-when-giving-a-brief-to-a-video-agency
- MnDOT, video style guide: https://www.mndot.org/metro/pdf/videostyleguide.pdf
- Lemonlight, marketing video script: https://www.lemonlight.com/blog/marketing-video-script/
- JTBD, the four forces: https://jobstobedone.org/the-four-forces/
- Smart Insights, message houses: https://www.smartinsights.com/online-brand-strategy/brand-positioning/message-houses-a-technique-to-improve-the-clarity-of-your-core-brand-messages/
- Benjamin Ball, message house: https://benjaminball.com/blog/what-is-a-message-house/
- MangoApps, message house template: https://www.mangoapps.com/templates/sites/message-house-key-message-framework
- Rev, documentary interview questions: https://www.rev.com/blog/documentary-interview-questions-how-to-ask-good-questions-for-a-documentary-interview
- Videomaker, documentary interview questions: https://www.videomaker.com/article/c06/19014-how-to-ask-great-documentary-interview-questions
- LibreTexts, Preparing Questions: https://human.libretexts.org/Bookshelves/Theater_Film_and_Storytelling/Documentary_Culture/12%3A_Directing_Interviews/12.01%3A_Preparing_Questions
- Premiumbeat, questions during documentary interviews: https://www.premiumbeat.com/blog/developing-questions-during-documentary-interviews/
- Lot1, interviewing for documentaries: https://lot1.substack.com/p/interviewing-for-documentaries-pt
- Reduct, paper edits: https://reduct.video/blog/paper-edits-for-documentary-filmmakers
- NYFA, editing interviews for documentary: https://www.nyfa.edu/student-resources/how-to-edit-an-interview-for-a-documentary/
- No Film School, cutting short documentaries, part 2: https://nofilmschool.com/2015/11/how-cut-short-documentary-films-part-two-building-story-adding-b-roll
- Todd Boruff, interview editing process: https://toddboruff.substack.com/p/my-interview-editing-process
- Lynda, assembling B-roll (radio edit): https://www.lynda.com/Premiere-Pro-tutorials/Assembling-B-roll-shots/105388/112753-4.html

### Assets, rights and AI
- AdPipe, building a brand footage library: https://www.adpipe.com/resources/build-brand-footage-library-repurposing
- AdPipe, unused footage: https://www.adpipe.com/resources/unused-video-footage-creative-waste
- Bridgeman, video licence types: https://www.bridgemanimages.com/en/news/licensing-video-footage-for-film-advertising-and-social-media/16817
- Dissolve, licensing 101: https://communication.dissolve.com/tips/the-language-of-licensing
- Getty, using files: https://www.gettyimages.in/faq/working-files
- Motion Elements, stock licensing: https://www.motionelements.com/blog/articles/what-you-need-to-know-about-stock-media-licensing
- SRD Rechtsanwälte, deepfake labelling under the AI Act: https://www.srd-rechtsanwaelte.de/en/blog/deepfake-labelling-under-the-ai-act-what-the-new-eu-guidance-clarifies
- Lewis Silkin, AI labelling for advertising deployers: https://www.lewissilkin.com/insights/2026/07/31/the-new-ai-labelling-rules-for-deployers-in-the-advertising-supply-chain
- Makeinfluence, Art. 50 for marketing: https://www.makeinfluence.com/en/academy/eu-ai-act-article-50-labeling-duty-for-ai-generated-marketing-content
- Stibbe, deepfake transparency: https://www.stibbe.com/publications-and-insights/deep-fakes-real-transparency-labelling-deep-fakes-and-ai-generated-public

### Roles, approvals and agent patterns
- Frame.io Workflow Guide, editing stages: https://workflow.frame.io/guide/editing-stages
- Dropbox, creative review for video: https://www.dropbox.com/en_GB/resources/creative-review-video-projects
- Tribe Pictures, post-production: https://tribepictures.com/the-video-production-process-part-3-post-production/
- Premiumbeat, three stages of editing corporate video: https://www.premiumbeat.com/blog/3-stages-editing-corporate-video/
- Fast.io, video review and approval: https://www.fast.io/resources/video-review-and-approval.md
- Dream Engine, production crew roles: https://dreamengine.com.au/news/understanding-roles-production-crew
- Casual Films, roles in video production: https://www.casualfilms.com/blog/what-are-the-roles-in-video-production
- Anthropic, Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Agent Patterns, human-in-the-loop checkpoints: https://agentpatterns.ai/loop-engineering/human-in-the-loop-checkpoints/
