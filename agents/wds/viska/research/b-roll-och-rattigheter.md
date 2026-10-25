# B-roll for Viska: planning, archive search, stock, music, matching, rights tracking

Research for Whiteport's AI media agent "Viska" (DaVinci Resolve Studio pipeline).
Researched: 2026-10-25. All URLs were accessed on that date.

**How to read this.** Each claim carries its source. Text marked **[Unverified]** comes from secondary sources, or from sources that contradict each other. Text marked **[Recommendation]** is my own synthesis and has no source behind it. This is not legal advice. For high-value client deliverables, such as TV ads or paid campaigns with identifiable people, check the license text and ask a lawyer.

---

## 0. Executive summary

1. **Plan B-roll from the script, not the library.** Work in two columns: audio/A-roll on one side, picture on the other. Score each script segment for how visual it is. Decide whether each beat needs literal or metaphorical cover. Then source it in this order: own archive, then stock, then AI.
2. **The archive is Viska's biggest asset.** innehall.csv can be imported into Resolve as clip metadata, so keywords, ratings and descriptions become searchable and drive Smart Bins. For semantic search, Resolve 21 Studio has IntelliSearch built in. For a Python index Viska controls itself, use open models: SigLIP 2, OpenCLIP or Meta Perception Encoder, with PySceneDetect splitting clips into shots.
3. **Stock licences differ most on what happens after delivery.** Per-asset perpetual licences (Getty/iStock, Adobe Stock, Pond5) are safest for client work. They are transferable or usable by the client, they include indemnity, and commercial content comes with releases. Subscription libraries (Artlist, Storyblocks, Envato Elements) cover projects finished during the subscription. New edits after cancellation are not covered. Free libraries (Pexels, Pixabay, Mixkit, Coverr, Videvo) give you no warranty about releases, so you carry that risk.
4. **Sweden adds one legal constraint.** Under *Lag (1978:800) om namn och bild i reklam*, using an identifiable person in marketing without consent is unlawful. That applies to free stock with no releases and to our own archive shoots.
5. **Music: Epidemic Sound Pro covers client work** (sublicensing). It excludes cinema, TV shows and TV ads, and Content ID clearance depends on connected channels. Musicbed single-song licences are perpetual. Avoid the YouTube Audio Library for client deliverables.
6. **Log the licence for every clip when it is ingested.** Keep a snapshot of the licence page and the version date, since terms change: the Pexels and Pixabay terms changed on 20 Oct 2026. Generate a rights report and music cue sheet from the final timeline.

---

## 1. B-roll planning: from script to shot needs

### 1.1 Terms

- **A-roll** is the primary footage, such as an interview or presenter. **B-roll** is supplementary footage cut in over it. B-roll is used to set scenes, smooth transitions, hide coughs and bad frames, and cover cuts between interview soundbites so you avoid jump cuts. It comes from your own shoots (often a second unit), stock, or archival sources. Source: Adobe, https://www.adobe.com/creativecloud/video/discover/b-roll.html
- Common B-roll types are establishing shots (where and when), cutaways (leaving the main action) and close-ups/inserts. Source: same Adobe page.
- B-roll also builds establishing and insert shots, bridges segments and covers flubbed lines. Source: No Film School, https://nofilmschool.com/2020/01/three-steps-perfect-b-roll

### 1.2 Deriving needs from a script

- **Shot list first.** For scripted work, go through the script and mark possible establishing shots, cutaways and close-ups. For interview documentaries, note which images could go with each line of dialogue. Source: https://www.adobe.com/creativecloud/video/discover/b-roll.html
- **Two-column A/V script.** Picture (B-roll, A-roll, photos, graphics, screen captures) goes in the left column and audio (interview, music, VO, SFX) in the right. Each row is a beat, and the audio runs over the picture. This is standard in documentary, TV news and advertising. Sources: Chicago Media Works paper-edit guide, https://www.chicagomediaworks.com/2instructworks/3editing_doc/3docedit_scriptmpl/3editing_docspaperedit.html ; Boords template, https://boords.com/video-script-template/documentary-template
- **Paper edit / master script.** Copy soundbites with their sequence name and timecode into a master document, and note B-roll filenames or timecodes above each quote. One guide also says to log and rename B-roll *before* this step. Source: StaffMeUp guide, https://blog-stg.staffmeup.com/?p=3310 **[Secondary]**
- **Automated version of the same logic** (Async, a vendor blog): transcribe, segment by *idea* rather than sentence, and score each segment for visual value. Concrete nouns, actions, places and numbers score high. Write an "ideal clip" description for each segment, source the clip, place it at word-level timing, then review it by hand. Source: https://async.com/blog/match-b-roll-to-your-video/ **[Vendor source, but the pipeline matches what Viska already has: transcripts with word timings]**

### 1.3 Literal vs. metaphorical B-roll ("show, don't tell")

- **Literal:** the line names an object or action, and you show it ("I open my laptop at 6am" gets a laptop opening). It is clear but can feel repetitive. **Metaphorical/conceptual:** the line has no physical referent and needs a visual stand-in, such as an empty office at night over a line about burnout. Automated tools struggle with metaphor. The fix is to *name the metaphor in the script* so a search can find it. Source: https://async.com/blog/match-b-roll-to-your-video/
- A shoot checklist can include "potential visual metaphors" alongside locations, angles, texture details and cutaways. Source: https://filmlifestyle.com/how-to-shoot-b-roll-footage/
- For corporate work, one editing guide recommends a conservative approach: images that underline what is being said. Source: Artlist blog, https://artlist.io/blog/how-to-edit-interviews/ **[Secondary]**
- **Clichés to avoid as metaphors:** relay baton, lightbulb, handshake, chessboard (https://www.trueagency.com/truelies/protesting-against-the-cliche); stacked coins, seedling in hands (https://jamesgood.co.uk/blog/for-real-differentiation-ditch-the-clichés). The isolated handshake "doesn't say anything specific about the business" (https://fremont.edu/cliche-images-to-avoid-on-your-website/). The suggested alternative is the real people and the real work. **[These sources are about stills and marketing, applied to video by extension]**

### 1.4 Sequences: wide / medium / close

- **Five-shot method (Michael Rosenblum):** close-up of hands (what), face (who), wide (where), over-the-shoulder (how), and one unusual shot. Sources: Columbia TC lesson, https://www.tc.columbia.edu/digitalfuturesinstitute/media/just-one-thing/lesson-prompts/5-shot-J1T-Lesson-3.docx ; No Film School, https://nofilmschool.com/2020/01/three-steps-perfect-b-roll
- **Wide / Tight / Interesting (Jay P. Morgan):** establish, then detail, then a creative extra shot. Avoid eye level, and add motion (slider, dolly) and depth of field. Source: https://nofilmschool.com/2020/01/three-steps-perfect-b-roll
- A wide/medium/close pattern alternated as the story needs. Source: Adorama, https://www.adorama.com/alc/create-better-videos-shooting-in-sequences ; Videomaker, https://www.videomaker.com/how-to/shooting/composition/this-method-will-leave-you-shooting-b-roll-like-the-pros/
- A sequence will not always be five shots. It may be three, or ten. Source: Baruch course page, https://blogs.baruch.cuny.edu/summermultimedia/?p=257
- **For Viska [Recommendation]:** when a beat needs more than one cutaway, request a *sequence* (wide, then detail, then human element) from the same shoot or the same stock contributor, not three unrelated clips. Shots from one shoot share light, grade and lens, so the sequence looks intentional.

### 1.5 How much B-roll per minute?

**No authoritative per-format ratio was found.** What the sources do give:

| Data point | Value | Source |
|---|---|---|
| Typical cutaway length | ~2–5 s, starting on or just after the motivating word | https://async.com/blog/match-b-roll-to-your-video/ |
| Short-form social B-roll | 2–3 s per clip, fast-paced | https://help.marketscale.com/en/articles/15265917-how-to-add-b-roll-that-makes-every-interview-video-watchable |
| Shooting coverage | 5–10 B-roll clips per interview, several angles | same MarketScale page |
| Hold when shooting | count to ten / 5–10 s / 10–15 s | Adobe (above); Edutopia, https://wpvip.edutopia.org/wp-content/uploads/2022/10/edutopia-stw-maine-project-learning-five-shot-guide-to-video-production-1.pdf ; Baruch (above) |
| Feature-film average shot length | ~12 s (1930) to ~2.5 s (recent, per a Cutting talk); ~4 s in 1985/2005 samples | https://flowingdata.com/2014/09/22/evolution-of-movies/ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/ |

**[Recommendation, not sourced; use as starting defaults and tune per client]:**
- Corporate or interview film, 2–4 min: about 40–60% of runtime covered by B-roll, 6–12 cutaways per minute of 3–6 s each. Show the speaker's face at the start and at key emotional lines.
- Social, 9:16, 15–60 s: 70–90% covered, a cut every 1.5–3 s.
- Case study or brand film with VO: 80–100% covered, with only short A-roll "proof" moments.
- Flag the cut points to cover first: every jump cut left by removed "ehm"s, every list or number, and every named place, product or person.

---

## 2. Searching our own archive (Google Drive plus innehall.csv)

### 2.1 Metadata and tagging practice

- **What logging is:** reviewing footage, noting unusable shots and story-relevant moments, and tagging them with keywords, timecodes and notes. Notes can include shot type, camera angle and audio quality. Sources: https://wpengine.fm.co/filmsupply/how-to-log-footage/ ; https://en.wikipedia.org/wiki/Shot_logging
- **Keyword structure:** subject (adult, child, dog), setting (day, night, winter, office, home), action (jogging, typing). Source: a stock contributor guide, https://intercom.help/contributor-portal-99bac814994e/en/articles/4961704-how-can-i-write-better-keywords-on-my-footage-clips
- **Use one standard.** Keep the same keywords across all footage, rate usability, and mark the best parts with in/out points. Sources: https://www.byteplus.com/en/topic/26511 ; https://wpengine.fm.co/filmsupply/how-to-log-footage/ **[Blogs; no formal controlled vocabulary for this genre was found]**
- **Rights fields belong in the log too.** The IPTC Video Metadata Hub has rights properties: Copyright Owner, Rights Usage Terms (v1.6), Model/Property Release Status and Document, Licensor and Credit Line. Sources: https://iptc.org/std/videometadatahub/userguide/ ; https://iptc.org/download/events/phmdc2016/PhMdC2016-VideoMetadataHub.pdf

**[Recommendation] Columns to add to innehall.csv** (keeping the existing description, keywords, rating and transcript):
`shot_size` (EWS/WS/MS/CU/ECU), `camera_move` (static/pan/tilt/handheld/slider/drone), `subject`, `setting`, `action`, `mood`, `time_of_day`, `season`, `people_identifiable` (y/n), `release_ids`, `release_scope` (client or general), `brands_visible`, `location_name`, `color_space/gamma` (e.g. S-Log3/S-Gamut3.cine, Rec.709), `fps`, `shutter`, `resolution`, `codec`, `metaphor_tags` (e.g. "growth", "calm", "teamwork"), and `best_in`/`best_out` for each file. Use a fixed list of terms for shot_size, camera_move, mood and setting, and keep everything else free-text.

### 2.2 Getting innehall.csv into Resolve

- Resolve can import a CSV through **File > Import Metadata To > Media Pool** and match it to clips. Turning on "ignore file extensions" helps matching, and turning off "match using clip start and end TC" helps when timecode differs. Keywords then become filterable, and metadata can drive Smart Bins. Sources: Pomfort, https://kb.pomfort.com/silverstack/hands-on/creating-dailies/export-to-davinci-resolve/ ; Strada, https://strada-technologies.notion.site/13-Resolve-cca732d5b92c4777aa933f398654ad35 ; Resolve 18.6 manual mirror, https://www.steakunderwater.com/VFXPedia/__man/Resolve18-6/DaVinciResolve18_Manual_files/part544.htm **[Menu names checked only against vendor guides, not Resolve 21]**
- **Resolve scripting (Python):** community references cover `MediaPool.AppendToTimeline()` with dicts of `mediaPoolItem`, `startFrame`, `endFrame` (and `recordFrame` for placement), plus `Timeline.AddMarker(frame, color, name, note, duration)` and `SetClipProperty`. Scripting from outside Resolve needs Studio. Sources: https://github.com/diop/davinci-resolve-api ; https://forum.blackmagicdesign.com/viewtopic.php?p=1131818 ; https://pypi.org/project/dvrctl/0.1.0/ **[Unverified: I could not confirm `MediaPoolItem.SetMetadata` online. Check the README in Resolve's Developer/Scripting folder on the workstation]**

### 2.3 Semantic search over footage

**Built into Resolve: IntelliSearch (Resolve 21, Studio only).** It searches the Media Pool for objects, scenes, faces and spoken dialogue, independent of filenames. It needs a downloaded model: "Faster", or "Better", which is about 6x slower to analyse. Visual hits return whole clips. Transcript hits show where in the clip the phrase is spoken. Results can be saved as dynamic Smart Bins. It only searches media imported into the *open project*; it "is not a media asset manager". Sources: Larry Jordan, https://larryjordan.com/articles/the-power-of-intellisearch-in-davinci-resolve-21/ ; release news, https://www.newsshooter.com/2026/06/02/davinci-resolve-21-final-release/ ; https://nofilmschool.com/davinci-resolve-21 ; Studio-only per https://davinciresolveclub.com/davinci-resolve-21-ai-tools.md **[Swedish dialogue support not confirmed]**
- Resolve 20 also added **IntelliScript**, which builds a timeline from a script by matching it against transcribed clips and puts alternate takes on higher tracks. That is A-roll assembly, not B-roll. Source: https://cined.com/davinci-resolve-20-released-in-public-beta-with-ai-powered-features ; https://tech.yahoo.com/article/davinci-resolve-20s-latest-ai-feature-can-create-an-entire-timeline-based-on-a-script-120009351.html

**Commercial tools:**
- **Jumper** (Witchcraft Software) does local, offline visual and speech search. Premiere and FCP are established. Resolve and Avid are in beta. It runs on Windows and macOS, and pricing is reported at roughly $15/month or $249 lifetime **[unverified]**. Sources: https://www.provideocoalition.com/review-ai-driven-video-search-with-jumper/amp ; https://se.trustpilot.com/review/getjumper.io ; https://topai.tools/t/jumper
- **Twelve Labs (Marengo)** is a cloud video-embedding and search API. Pay-as-you-go indexing is about $0.042/min, plus $0.0015/min/month storage and $4 per 1,000 searches. The free tier gives 600 minutes. Source: https://twelvelabs.io/pricing **[Prices conflict between their own pages]**. Sending client footage to a US cloud raises GDPR/DPA questions. Sending *stock* footage may breach stock terms (see 3.4).
- **Google Vertex AI multimodal embeddings** (`multimodalembedding@001`) put text, image and video into one space, with segment intervals (minimum 4 s) and 1408 dimensions. Sources: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-multimodal-embedding-image-video-text ; https://docs.spring.io/spring-ai/reference/api/embeddings/vertexai-embeddings-multimodal.html

**Open source, usable from Python on Windows:**
- **Shot splitting:** PySceneDetect (`pip install scenedetect[opencv]`, v0.6.6, March 2025). Its content detector finds cuts and its threshold detector finds fades. Pin `<0.7`, since the API is changing. Sources: https://www.scenedetect.com/docs/0.6.4/api.html ; https://pypi.org/project/scenedetect/
- **Embedding models:**
  - CLIP: https://arxiv.org/abs/2103.00020 . OpenCLIP: https://github.com/mlfoundations/open_clip
  - **SigLIP 2** (Feb 2025) is *multilingual* and beats SigLIP at every scale on retrieval. Sizes run 86M to 1B. It matters for Swedish queries. Source: https://huggingface.co/papers/2502.14786
  - **Meta Perception Encoder** (2025) is SOTA-claimed on zero-shot video retrieval. PE-AV (Dec 2025, Apache 2.0) adds *audio* to the shared space. Sources: https://arxiv.org/pdf/2504.13181 ; https://github.com/facebookresearch/perception_models ; https://aihola.com/article/meta-pe-av-audiovisual-encoder **[Benchmarks are company-reported]**
- **Reference projects:**
  - VideoSeek: Windows-first, ONNX + Lance + FFmpeg, text, screenshot or dialogue search. https://github.com/6v17/VideoSeek/wiki
  - video-content-search (OpenCLIP): https://github.com/bwconrad/video-content-search
  - Semantic Eye (CLIP ViT-L-14, skips static frames): https://github.com/GughanS/semantic-eye
  - OpenVINO MobileCLIP notebook: https://docs.openvino.ai/2025/notebooks/mobileclip-video-search-with-output.html
  - AWS walkthrough with OpenCLIP/SigLIP: https://aws.amazon.com/blogs/machine-learning/implement-semantic-video-search-using-open-source-large-vision-models-on-amazon-sagemaker-and-amazon-opensearch-serverless/
  - Maintenance status of these has not been checked.
- **[Recommendation] Viska pipeline:**
  1. Run PySceneDetect on each archive file.
  2. Take 1–3 keyframes per shot.
  3. Embed them with SigLIP 2, which handles Swedish and English text queries.
  4. Store them in a local vector DB (LanceDB or FAISS) keyed by `file_id + shot_in/out`.
  5. Score search hits as a mix of embedding similarity, keyword overlap from innehall.csv and the 1–5 rating, then filter on rights fields (release_scope, people_identifiable).
  6. Use transcript text search separately to find *A-roll*, or B-roll where the subject is talked about.

### 2.4 Transcript → B-roll matching (research and tools)

- **B-Script** (Huber et al., Adobe Research, CHI 2019) is a transcript-based B-roll editor. Its recommender was trained on data from 115 expert editors and suggests *where* to insert B-roll and *what* to show. In a 110-participant study, the transcript interface made insertion easier, and recommendations led to more engaging videos. Sources: https://arxiv.org/abs/1902.11216 ; https://research.adobe.com/publication/b-script-transcript-based-b-roll-video-editing-with-recommendations/
- **Write-A-Video** (Wang et al., SIGGRAPH Asia 2019, ACM TOG 38(6)) builds a montage from themed text in three steps: text editing, visual-semantic shot retrieval, and optimisation under cinematographic rules. Source: https://faculty.runi.ac.il/arik/site/includes/papers/WriteAVideo.pdf
- **LAVE** (U. Toronto) is an LLM agent that turns language into footage retrieval and edit actions, which the user approves. Source: https://www.dgp.toronto.edu/~bryanw/lave/
- **EditDuet** (2025 arXiv) uses Editor and Critic LLM agents that iterate on an NLE timeline. Source: https://arxiv.org/html/2509.10761v1 **[Adjacent work; not specifically about B-roll]**
- A practitioner blog reports that a prompt-only LLM approach to "which sentences need B-roll" did badly. Source: https://motionbox.io/blog/llm-video-editing-workflow **[Anecdotal]**
- **Lesson for Viska [Recommendation]:** follow the B-Script split. Have *placement* (where to cut away) run on rules plus an LLM over the transcript: cover jump cuts, lists, named entities and abstract claims. Have *content* (what to show) run on retrieval. Always add a human approval step, as in LAVE.

---

## 3. Royalty-free stock video for commercial client work (Sweden/EU)

### 3.1 Comparison table

The "terms date" column gives the version date I read. "n/d" means the page showed no date.

| Library | Commercial / client | Attribution | Releases & warranty | Editorial-only clips | After subscription ends | API | Res / formats | Price model | Terms date |
|---|---|---|---|---|---|---|---|---|---|
| **Pexels** | Free, incl. business uses (ads, web, social) | Not required | Contributors *represent* they hold releases. Pexels gives **no warranty** ("AS IS") and the user must check consents | n/a | n/a (no subscription) | Yes, free. 200 req/h, 20k/mo. API use must show a link to Pexels | Up to 4K (4096×2160 in examples), MP4/HLS, `fps` field | Free | ToS updated 20 Oct 2026 |
| **Pixabay** | Free | Not required | Same model as Pexels: uploader represents releases, no warranty, "commercial use will likely require" permissions | n/a | n/a | Yes. 100 req/60 s, cache 24 h, **systematic mass downloads prohibited** | large ≈3840×2160 when available, 1080p for all | Free | ToS updated 20 Oct 2026 |
| **Mixkit** (Envato) | Free License: commercial OK. Restricted License: non-commercial only | Not required | Third-party components (trademarks) need separate permission | n/d | n/a | None found | 4K/HD MP4 | Free | User Terms rev. 2 Oct 2025; licence text **not verified** |
| **Coverr** | Free for commercial and non-commercial use | Not required (website). **API apps must show the Coverr logo** | Coverr holds model releases but **does not provide them**. No releases for brands or property | n/d | n/a | Yes. Demo 50 req/h, production 2,000 req/h. MCP server | **[Unverified]** | Free, plus Coverr+ | n/d. **Prohibits use for AI training/datasets** |
| **Videvo** (Freepik since 2022) | Per clip: Royalty Free vs. Videvo Attribution vs. CC 3.0 vs. **Editorial** | Depends on clip | **[Unverified]** | Yes, some clips are editorial-only | Premium: **[unverified]** | None found | Mixed | Free + premium | Licence page now redirects to Freepik (403). Old guide dated May 2020 |
| **Storyblocks** | Yes. Individual (1 user), Small Business (<50 staff, **agencies excluded**), Business (org, broadcast/OTT/film) | No | Indemnity $20k (Ind./SB), $1M (Business) | Not addressed | **Individual and SB: no perpetual use. Business: perpetual.** Published content stays covered | Yes, partner API (HMAC). Needs end-user and project IDs. Quote-based | 8K/4K/HD on all tiers (May 2026 snapshot) | Subscription. Business "contact sales" | Help article 1 Apr 2026 |
| **Artlist** (Artgrid folded in) | **Pro covers client work.** Project can be transferred to client, "but the License is only yours". Companies >50 staff need Max Business | No | Assets integrated in projects only, not standalone | Not addressed | Published projects stay licensed "forever". **New projects not covered** | Enterprise **music** API only. Footage API not found | Up to 8K. **RAW/LOG is an add-on** (~$18–20/mo) | Subscription (Max ~$39.99/mo annual) | Pro/Business licence effective **15 Feb 2026** |
| **Envato Elements** | Commercial, **one licence per project/end product** | No | Must be integrated or customised, never "as-is" | n/d | Completed end products keep the licence. **No new projects** | No public API found | Mixed. Footage called "dated" in reviews | Subscription | Licence rev. **8 Dec 2025**. Registration rules **conflict** |
| **Adobe Stock** | Standard licence: perpetual, worldwide. **Licence can be transferred to one client/employer** | Editorial: credit required | IP indemnity up to **$10,000**. **Editorial works excluded** | Yes. Newsworthy context only, no ads | Perpetual per asset | **Yes**: search with API key. Licensing needs OAuth + partner programme | HD/4K | Credits/subscription. 4K clips are expensive | Licence page n/d. Additional Terms PDF 15 Sep 2023 |
| **Pond5** | Royalty-free, worldwide, **perpetual**, all media | n/d | Indemnity: $15k individual, $250k business, $1M premium **[tiers conflict across sources]** | Yes. Commercial clearance of editorial clips costs about clip price + $1,500, or + $3,500 with third-party indemnity | Perpetual (pay per clip) | No public API found | Up to 8K/RED collections | Per clip | Help pages n/d (licence page 403) |
| **Getty Images** | RF: perpetual. Client may use it **if named as Licensee**. Up to 10 users per legal entity | Video credit **only if other providers are credited** | Warranty-backed indemnity, no stated cap | Yes. No commercial or advertising use without separate clearance | Perpetual. (Premium Access sharing rights end with the term) | **Yes** (api.gettyimages.com, OAuth) | Up to 4K | Per clip / plans | CLA updated **April 2026** |
| **iStock** | Standard licence covers film/TV, ads, web. Usable by the client you bought it for, if you can bind them | Video: credit "iStock.com/[member]" in end credits where feasible **[as summarised; verify]** | Liability cap **$10k standard / $250k extended** per item | Yes. No commercial use, no releases | Perpetual | Via Getty API | HD/4K, same price | Credits/subscription (Essentials/Signature) | Licence updated **July 2026** (Swedish version) |

Sources for the table:
- Pexels licence https://www.pexels.com/license/ ; ToS https://www.pexels.com/terms-of-service/ ; API https://www.pexels.com/api/documentation/
- Pixabay summary https://pixabay.com/service/license-summary/ ; ToS https://pixabay.com/service/terms/ ; API https://pixabay.com/api/docs/
- Mixkit https://mixkit.co/license/ and https://mixkit.co/terms/
- Coverr https://coverr.co/license ; API https://api.coverr.co/docs/start ; https://coverr.co/developers
- Videvo guide https://www.videvo.net/blog/?p=314 ; Freepik acquisition per https://tecnobits.net/videos-para-youtubers-bancos-de-videos/
- Storyblocks https://www.storyblocks.com/license ; https://intercom.help/storyblocks-9aa34255171d/en/articles/3622218-how-does-licensing-at-storyblocks-work ; API https://documentation.storyblocks.com/view/metadata/SztG3m1i ; pricing snapshot https://pricingsaas.com/companies/storyblocks
- Artlist licence https://help-center.artlist.io/privacy-terms/artlist-license ; RAW/LOG and 8K https://www.cined.com/artgrid-by-artlist-launches-with-raw-log-and-stock-footage-up-to-8k/ ; consolidation and pricing https://photutorial.com/artgrid-review , https://photutorial.com/artlist-pricing ; API https://developer.artlist.io/
- Envato https://help.elements.envato.com/hc/en-us/articles/360000621763-Create-a-new-license ; https://help.elements.envato.com/hc/en-us/articles/360000621483 ; https://help.elements.envato.com/hc/en-us/articles/360000628966-License-Terms (403 for me; revision date via search) ; https://terms.law/ToS-Watchdog/stock-media/envato/ ; reviews https://www.techradar.com/pro/software-services/envato-elements-review
- Adobe https://stock.adobe.com/license-terms ; https://wwwimages2.adobe.com/content/dam/cc/en/legal/servicetou/Stock-Additional-Terms_en_US_20230915.pdf ; API https://developer.adobe.com/stock/docs/
- Pond5 https://www.pond5.com/help/en/articles/10086095-editorial-to-commercial-upgrade ; https://www.pond5.com/help/en/articles/10086101-individual-and-extended-licenses ; https://www.pond5.com/our-licenses
- Getty https://www.gettyimages.com/eula ; https://www.gettyimages.com/faq/licensing ; API https://developer.gettyimages.com/docs/
- iStock https://www.istockphoto.com/legal/license-agreement ; pricing (dated) https://photutorial.com/istock-pricing

### 3.2 Notes that matter for client deliverables

- **Who holds the licence.**
  - Adobe Stock lets you transfer a Standard licence to *one* client. Source: https://stock.adobe.com/license-terms
  - Getty allows use by the client if the client is named as Licensee. Source: https://www.gettyimages.com/eula
  - Artlist: "you can transfer this Project to your clients, though the License is only yours". The client can show the film, but cannot reuse the clip in their own new edits. Source: https://help-center.artlist.io/privacy-terms/artlist-license
- **Re-edits after cancellation.** With Artlist, Envato and Storyblocks (Individual/SB), a *new* cut-down or new version made after the subscription lapses is arguably a new project and **not covered**. Storyblocks Business includes perpetual use. Sources: Artlist licence and Storyblocks licence pages above. **[Recommendation]** Treat client re-versions as new projects, and keep the subscription active as long as the client may order changes. Otherwise buy per-asset licences for hero shots.
- **Storyblocks Small Business explicitly excludes agencies and production companies.** Whiteport should use Individual (1 user) or Business. Source: https://www.storyblocks.com/license
- **Artlist Pro does not cover broadcasters**, who need Max Business or Enterprise. Companies with more than 50 employees need Max Business. Public performance royalties (PRO/collecting society) are not included. Source: https://help-center.artlist.io/privacy-terms/artlist-license
- **Editorial-only clips are a trap for commercial films.** Adobe, Getty, iStock, Pond5 and Videvo all flag them, and they must never appear in marketing. Adobe's indemnity excludes them, and Pond5 charges $1.5k–3.5k+ to clear one. Sources: Adobe Additional Terms 2023, Getty EULA, Pond5 help (above). **[Recommendation]** Viska must filter `editorial == true` out of every commercial search.
- **Free libraries put the risk on you.**
  - Pexels and Pixabay: contributors *represent* they hold releases, but the platforms disclaim responsibility, and "users are responsible for determining whether they need permissions". Sources: https://www.pexels.com/terms-of-service/ ; https://pixabay.com/service/terms/
  - Coverr holds releases but won't hand them over. Source: https://coverr.co/license
  - Neither offers indemnity.
- **Sweden: name and image in advertising.** Lag (1978:800) bans using a person's name or image in marketing without consent. "Bild" covers any image in which the person is identifiable. Penalties include fines, *skäligt vederlag* and damages (including for suffering), and the court can order the material changed or destroyed. Sources: https://lagen.nu/1978:800 ; https://data.riksdagen.se/dokument/sfs-1978-800.html ; https://lawline.se/answers/15674 . Lawline's view is that written consent is needed in practice for marketing (https://www.lawline.se/answers/publicera-bilder-pa-kunder-utan-samtycke) **[a single lawyer's opinion]**.
  - **[Recommendation]** Use free stock with *identifiable people* only where you can obtain the release, or not in ads/marketing at all. Keep free stock to landscapes, textures, hands without faces, crowds without identifiable people, and objects without brands.
- **Sensitive-subject disclaimers.** If a model appears in an unflattering or controversial context (health, crime, debt), Getty and iStock require a note that the image is illustrative and the person is a model. iStock's Swedish example is "Bildbankfoto. Personen på bilden är en modell." Sources: https://www.gettyimages.com/eula ; https://www.istockphoto.com/legal/license-agreement
- **AI-generated stock.** iStock does not offer extended licences or extended indemnity for AI-generated material. Source: https://www.istockphoto.com/legal/license-agreement . **[Recommendation]** Log an `ai_generated` flag for stock too.

### 3.3 Safety ranking for client deliverables [Recommendation, based on the terms above]

1. **Safest:** Getty Images / iStock, Adobe Stock, Pond5. These are perpetual per-asset licences. The client can use them (named licensee or transfer), there is stated indemnity, and commercial (non-editorial) content comes with releases. Use them for hero shots, identifiable people in ads, and TV/OOH.
2. **Good, if you manage the subscription:**
   - **Storyblocks Business**: perpetual, $1M indemnity, broadcast.
   - **Artlist Pro / Max Business**: client work covered, 8K and RAW/LOG.
   - **Envato Elements**: per project. Weakest for footage quality and the clarity of its rules.
   - The risk is re-edits after cancellation, and the licence staying with Whiteport rather than the client.
3. **Use with care:** Pexels, Pixabay, Mixkit (Free License only), Coverr, Videvo (check each clip). Fine for non-identifiable, non-branded generic B-roll. Avoid them for identifiable people in marketing, and never use Mixkit "Restricted" or Videvo "Editorial" clips.

### 3.4 Automation and API constraints for Viska

- **Pexels API:** 200 req/h. You must link to Pexels and should credit videographers in your app. Copying Pexels' core function is not allowed. Source: https://www.pexels.com/api/documentation/
- **Pixabay API:** cache results for 24 h, and *systematic mass downloads are prohibited*. Requests must come from real humans. Source: https://pixabay.com/api/docs/
- **Pexels and Pixabay ToS** ban scraping or data-mining for machine learning. **Coverr** bans use for AI training and datasets. **Getty** bans ML/AI use without authorisation. For creative content, Getty *allows* "internal archiving, searching, indexing, sorting". Uploading Getty content to a third-party AI tool that acquires rights counts as training. Sources: https://www.pexels.com/terms-of-service/ ; https://pixabay.com/service/terms/ ; https://coverr.co/license ; https://www.gettyimages.com/eula
- **[Recommendation]**
  - Have Viska search stock via the APIs and download only the selected clips, triggered by a human approving a shot list.
  - Do not bulk-download libraries.
  - Do not upload licensed stock to cloud embedding services such as Twelve Labs.
  - Local embeddings of clips you have *licensed* are probably "indexing". That is explicitly allowed by Getty, but not explicitly by the others, so it is a grey zone.
- **Programmatic options:**
  - Free: Pexels, Pixabay and Coverr have APIs.
  - Paid: Adobe Stock (licensing needs the affiliate/partner programme), Getty/iStock and the Storyblocks partner API.
  - No public API found: Artlist (music only), Envato, Pond5, Mixkit.

---

## 4. Music and SFX licensing for client work

| Service | Client work | After cancellation | Content ID / social | Exclusions and notes | Terms date |
|---|---|---|---|---|---|
| **Epidemic Sound** (Swedish) | **Pro**: "full sublicensing rights", so clients can publish on *their* channels. Companies >$10M turnover (publishers >$5M) must use Enterprise **[unclear whether this means Whiteport's turnover or the client's]** | Content published during the subscription stays cleared "forever". New content after it ends is claimed | Connect or safelist channels. Pro: 3 channels per platform. Disputes allowed with a valid licence | **Pro excludes cinema, TV shows and TV ads.** Digital ads are included unless you are a major corporation or publisher, or a government entity. The direct licence includes **public performance** (TV, streaming, events). Enterprise has indemnity | Pages n/d. Prices (3rd party, mid-2026): Pro $16.99/mo annual |
| **Artlist** | Pro covers client work and paid ads | Published projects stay licensed. New ones are not | Clearlist: Pro 3 channels per platform, Teams 5, Max Business unlimited. Channels not listed may be claimed, and **lost revenue is not reimbursed**. You may add YouTube project URLs | Broadcasters need Max Business or Enterprise. PRO royalties not included | Effective 15 Feb 2026 |
| **Musicbed** | Per-song licences scoped by project and media | Single-song licence is **perpetual** for that project. **Subscription licences are void if you cancel before the 12-month term ends** | Not documented | Rights-managed style. Broadcast by quote | FAQ n/d |
| **Soundstripe** | Pro plan covers client projects | Projects licensed during the subscription stay licensed permanently. No new uses | Registered channels cleared. For channels *not listed* (e.g. a client's) you generate single-use codes, **which can't be generated after expiry** | A cue sheet may be needed for TV | Help pages n/d |
| **Envato Elements** music | Per project, as for footage | As for footage | **[Not verified]** | | Rev. 8 Dec 2025 |
| **YouTube Audio Library** | Help page addresses only YouTube use and monetisation | n/a | Not claimed via Content ID on YouTube | Use outside YouTube is **not addressed** by Google. CC BY tracks need credit. **Avoid for client deliverables** [Recommendation] | n/d |
| **Freesound** (SFX) | CC0 and CC BY allow commercial use. CC BY-NC does not | n/a | n/a | Filter on CC0. CC BY needs a credit. The legacy Sampling+ licence is retired | n/d |
| **Pixabay music** | Free under the Pixabay licence | n/a | **Some tracks are registered in Content ID by composers.** Claims can come retroactively and need manual dispute | Treat as "may be claimed" | ToS 20 Oct 2026 |

Sources:
- Epidemic: https://www.epidemicsound.com/our-plans/pro-plan/ ; https://www.epidemicsound.com/how-it-works/license-music-legally/ ; https://www.epidemicsound.com/how-it-works/which-plan-is-right-for-you/ ; https://help.epidemicsound.com/hc/en-us/articles/26253712691730-Why-was-a-Content-ID-claim-received-from-Epidemic-Sound ; pricing https://photutorial.com/epidemic-sound-pricing **[3rd party]**
- Artlist: https://help-center.artlist.io/privacy-terms/artlist-license
- Musicbed: https://support.musicbed.com/musicbed-faq/how-long-is-my-license-good-for ; https://www.soundstripe.com/blogs/musicbed-alternatives **[competitor]**
- Soundstripe: https://www.soundstripe.com/knowledge/cancellation/licenses-after-cancellation ; https://www.soundstripe.com/knowledge/licensing-usage/post-subscription-use-0 ; https://www.soundstripe.com/library/pricing
- YouTube: https://support.google.com/youtube/answer/3376882
- Freesound: https://en.wikipedia.org/wiki/Freesound ; https://freesound.org/forum/legal-help-and-attribution-questions/38292
- Pixabay music Content ID: https://hellothematic.com/thematic-vs-pixabay/ **[competitor source]**

**Content ID in general:** Content ID matches audio fingerprints. It does not check your licence before claiming; proof only helps afterwards, in a dispute. Source: https://www.foximusic.com/blog/?p=480 **[vendor blog]**

**Sweden, public performance:** if a client plays the film at an event (launch, fair, conference) with music in it, the *event organiser* needs a STIM licence for STIM repertoire. In 2026, background music at events cost from SEK 368/day for up to 500 visitors. Sources: https://stim.se/en/om-oss/villkor-och-avtal/prices-terms-and-conditions-for-music-licenses/prices-and-special-terms-music-at-events ; https://www.stim.se/en/kund/live-and-performing-arts . Epidemic says its direct licence includes public performance rights for events (https://www.epidemicsound.com/how-it-works/license-music-legally/). Artlist says PRO royalties are *not* included. **[Recommendation]** Tell clients in writing which tracks are "direct licensed / non-PRO" for event use.

**[Recommendation] Music policy for Viska:**
- Default to Epidemic Sound Pro (Swedish, client sublicensing, public performance included) for web and social.
- For TV ads or cinema, quote Epidemic Enterprise, or buy Musicbed single-song licences.
- Before delivery, add the client's YouTube/Meta channels to the safelist/Clearlist, or hand over per-video clearance codes.
- SFX: Epidemic/Artlist SFX, or Freesound CC0 only.

---

## 5. Making stock not look like stock

### 5.1 Selection

- Skip clips you have seen in many other videos, and pick unusual angles, better light and less common scenarios. Download several candidates per beat. Source: https://uppbeat.io/blog/stock-video/kristian-kettner-5-tips-on-using-stock-footage-in-your-content
- Avoid generic office or handshake material that adds nothing. Prefer specific, unusual locations. Sources: https://idearocketanimation.com/21857-stock-video-footage/ ; https://beverlyboy.com/film-technology/dont-be-that-editor-stock-footage-mistakes-that-kill-your-video/
- A stock clip should be "really close" to your own footage or "really far" from it. A clip that is *almost* right reads as a mistake. Source: https://uppbeat.io/blog/stock-video/kristian-kettner-5-tips-on-using-stock-footage-in-your-content
- Pick locations that could plausibly be *the same place* as your footage. Generic spaces adapt, but landmarks don't. Source: https://soundstripe.com/blogs/make-stock-video-match-shot-video
- Avoid static, dull clips; prefer movement and perspective. Source: https://motionarray.com/learn/filmmaking/stock-footage-tips/
- **[Recommendation] Viska selection checklist:**
  - Light direction and time of day match the A-roll.
  - Lens feel matches (wide vs. tele compression, depth of field).
  - Wardrobe, demographics and season fit Sweden. Avoid US sockets, cars, road signs, money and school buses.
  - No visible brands.
  - Camera movement style matches (handheld vs. gimbal).
  - Use one contributor or "collection" per sequence.
  - Prefer log/flat sources.

### 5.2 Colour (Resolve)

- **Colour-managed setup for mixed sources:** DaVinci YRGB Color Managed, timeline DaVinci Wide Gamut Intermediate, output Rec.709 Gamma 2.4 (or 2.2 for desktop viewing). Source: Frame.io, https://blog.frame.io/2023/12/04/color-management-cheat-sheet-davinci-resolve/
- **Set the Input Color Space per clip** (e.g. Rec.709 for most stock, the camera log for our footage). Don't stack a CST on top of a clip that colour management has already interpreted, because that doubles the conversion. If the input space isn't set, Resolve guesses from metadata and often misreads log as Rec.709. Source: Blackmagic forum, https://forum.blackmagicdesign.com/viewtopic.php?p=752388 **[2021 thread]**
- Don't tone-map SDR Rec.709 stock as if it were HDR. iPhone HDR/HLG/Apple Log are different inputs. Source: https://davinciresolveclub.com/iphone-hdr-to-sdr-davinci-resolve/
- No image data is clipped in the input-to-timeline conversion. Source: Resolve 18.6 manual mirror, https://www.steakunderwater.com/VFXPedia/__man/Resolve18-6/DaVinciResolve18_Manual_files/part284.htm
- **Matching workflow:**
  1. Match exposure first on the waveform.
  2. Grab a still of the graded hero shot as a reference.
  3. Match shadows and highlights separately with curves.
  4. Use **Shot Match** (clip-to-clip, fast, medium accuracy) or **Color Match** (needs a colour chart in the shot).
  5. Treat both as starting points.
  - Sources: https://www.4kshooters.net/2016/03/17/more-tips-on-matching-shots-in-davinci-resolve-12 ; Larry Jordan, https://larryjordan.com/articles/how-to-color-match-clips-in-davinci-resolve-20/ ; https://pixflow.net/blog/color-match-cameras-davinci-resolve/
- Ungraded or log stock is easier to match than pre-graded stock. Sources: https://soundstripe.com/blogs/make-stock-video-match-shot-video ; https://uppbeat.io/blog/stock-video/how-to-find-stock-footage-that-matches-your-shooting-style
- Plug-ins: FilmConvert CineMatch for camera matching. Source: https://www.provideocoalition.com/cinematch-from-filmconvert/amp/

### 5.3 Grain and texture

- **Film Look Creator** (ResolveFX, Resolve 19+): grain, halation, blur and vignette in one effect. It imitates film in general, not specific stocks. Sources: https://mixinglight.com/color-grading-tutorials/film-look-creator-resolvefx-overview-workflow ; https://videvo.net/blog/?p=44110
- **Film Grain** ResolveFX (Studio) is procedural grain with type, opacity and composite controls. Source: https://www.premiumbeat.com/blog/master-davinci-resolves-film-grain
- For true *matching*, DVO Regrain RGB has per-channel and per-zone grain controls. Source: https://filmworkz.com/wp-content/uploads/2025/06/DVO-Regrain-RGB-OFX-User-Guide.pdf
- **[Recommendation]** Put **one** grain/texture pass on a timeline-level node or adjustment clip *over everything*: own footage, stock and AI. A shared texture is the strongest single tool for making mixed sources look like one film. If the stock is heavily compressed (8-bit H.264), denoise it lightly before regraining.

### 5.4 Frame rate and shutter

- Match frame rates. Mixing 24/25 fps with 60 fps footage reads as wrong. Conform 50/60 fps stock to the timeline rate, played as slow-motion or frame-dropped. Scale higher-resolution clips down rather than low-resolution clips up. Sources: https://soundstripe.com/blogs/make-stock-video-match-shot-video ; https://uppbeat.io/blog/stock-video/how-to-find-stock-footage-that-matches-your-shooting-style
- **180° rule:** shutter = 1/(2 × fps). At 25 fps that is 1/50. Clips shot with a short shutter (e.g. 1/500 drone or action stock) look stuttery next to 180° footage. Sources: https://www.studiobinder.com/blog/what-is-the-180-degree-shutter-rule/ ; https://blog.kevinlisota.photography/2020/04/understanding-video-frame-rate-and-shutter-speed/ ; the rule's limits: https://provideocoalition.com/the-180-shutter-angle-rule-is-broken
- **[Recommendation]**
  - Sweden is a 25p/50p territory. Set Viska's stock filters to 25/50 fps first. 24 fps clips at 25 play about 4% fast, which is usually acceptable for B-roll with no sync sound. Prefer 50p sources for slow-motion.
  - Pexels returns an `fps` field per file (https://www.pexels.com/api/documentation/), so Viska can filter on it.
  - For short-shutter clips, try Resolve's Motion Blur effect (Studio) **[not verified in sources]**.
- **Audio:** replace stock clip audio with your own room tone or music so it stays consistent. Sources: https://soundstripe.com/blogs/make-stock-video-match-shot-video ; https://beverlyboy.com/film-technology/dont-be-that-editor-stock-footage-mistakes-that-kill-your-video/

---

## 6. Logging and rights tracking (audit trail per delivered film)

### 6.1 What the industry expects

- A clearance log records, per third-party asset: timecode, rights status, usage restrictions (territory, term, platform, credit, fees, renewal triggers) and where the licence or release is filed. Source: https://www.docsie.io/solutions/templates/media-entertainment/rights-clearance-tracker/
- A music cue sheet lists every cue with in/out time in the film, duration, writer, publisher and collecting-society affiliation. Source: https://help.filmhub.com/en/articles/2663801-how-to-add-your-documents
- E&O insurers will not cover a film without a complete clearance package. Most clearance failures come from vague usage terms, missing renewal triggers, or archive sources you can't trace. Sources: https://blog.promise.legal/indie-film-clearance-talent-location-music-releases/ ; https://www.lexplug.com/outlines/clearance-errors-and-omissions-eo-insurance
- Metadata standards for embedding rights:
  - IPTC Video Metadata Hub: Rights Usage Terms, Copyright Owner, Licensor, release status and documents. https://iptc.org/std/videometadatahub/userguide/
  - PLUS License Data Format (XMP `plus:`): licensee, licence start and end dates, media constraints. https://ns.useplus.com/LDF/ldf-XMPReference ; https://exiv2.org/tags-xmp-plus.html
- **Proof of licence by vendor:**
  - Storyblocks: the active plan's licence agreement *is* the proof. There are no per-asset certificates on Individual. Source: https://intercom.help/storyblocks-9aa34255171d/en/articles/3622218-how-does-licensing-at-storyblocks-work
  - Business plans add rights certificates and cue sheets. Source: https://www.storyblocks.com/license
  - Adobe Stock exposes licence history via its API (`/Libraries/1/Member/LicenseHistory`). Source: https://developer.adobe.com/stock/docs/api/
  - Soundstripe Proof of License remains valid for claims later. Source: https://www.soundstripe.com/knowledge/cancellation/licenses-after-cancellation

### 6.2 [Recommendation] Viska rights ledger (one row per clip *use*)

Keep it next to innehall.csv, e.g. `rights-ledger.csv`, or as a sheet per project. Fields:

| Group | Fields |
|---|---|
| Identity | `use_id`, `project_id`, `client`, `deliverable` (master, cut-down, format), `timeline_name`, `record_tc_in/out`, `source_tc_in/out` |
| Source | `source_type` (own / stock / ai / music / sfx), `provider`, `provider_asset_id`, `asset_url`, `contributor`, `file_hash` (sha256), `local_path` |
| Licence | `license_name` (e.g. "Artlist Pro", "Adobe Standard", "Pexels License"), `license_version_date`, `license_snapshot_path` (PDF/HTML of the licence page when downloaded), `licensee` (Whiteport / client), `plan_or_order_id`, `invoice_ref`, `download_date`, `subscription_active_at_publish` |
| Scope | `media` (web/social/paid/TV/OOH/event), `territory`, `term_end` (blank = perpetual), `renewal_trigger` (e.g. "new edit after subscription end = new licence"), `channels_cleared` (Content ID safelist IDs or clearance codes) |
| Risk flags | `editorial_only`, `people_identifiable`, `model_release` (have/none/not needed + doc ref), `property_release`, `brands_visible`, `ai_generated`, `sensitive_use_disclaimer_needed` |
| Attribution | `credit_required` (y/n), `credit_text` |
| Music extras | `title`, `composer`, `publisher`, `pro_affiliation` (STIM/none/direct), `cue_duration` (for the cue sheet) |
| Own footage | `shoot_id`, `release_form_ids`, `release_scope` (this client only / any client / internal), `gdpr_basis` |

**Process:**
1. **At download or generation**, Viska writes the row and saves a licence-page snapshot plus the invoice or receipt. Terms change: the Pexels and Pixabay ToS were updated 20 Oct 2026, and the Artlist licence took effect 15 Feb 2026.
2. **In Resolve**, put `provider:asset_id` and `license_name` into each clip's Comments or Keywords using the CSV metadata import (2.2). The information then travels with the clip, and Smart Bins can show "editorial", "no release" or "AI".
3. **At picture lock**, export the timeline's used-clip list (an EDL, or the edit index as CSV) and join it with the ledger. That produces (a) a rights report per deliverable and (b) a music cue sheet. **[Resolve's export menu names not verified here]**
4. **At delivery**, give the client the rights report and cue sheet. Say what is *not* transferable (e.g. Artlist assets can't be reused in their own edits), and note expiries or conditions, such as "re-edits require an active subscription or new licence".
5. **Archive** the ledger, snapshots and invoices with the project in the shared Drive, for at least as long as the film is in use. **[Retention period is a business/legal decision]**

---

## 7. Open questions and uncertainties

- **Envato Elements:** sources conflict on whether project registration is still needed. The help centre says it is no longer needed, and a Jan 2026 third-party review says it is. I could not read the licence text (403).
- **Mixkit Free / Restricted** and **Videvo** licence texts: I could not read them directly. The Videvo licence URL now redirects to Freepik, which returned 403.
- **Epidemic Pro eligibility:** it is unclear whether the $10M turnover limit applies to Whiteport or to the *client* when sublicensing. Ask Epidemic.
- **Pond5:** indemnity tiers and the current licence text were not read (403). The figures come from help pages.
- **iStock video credit requirement:** taken from a summary of the Swedish licence. Verify the exact clause.
- **Resolve:** IntelliSearch support for Swedish, and whether it is exposed to scripting, is unknown. `MediaPoolItem.SetMetadata` was not verified.
- **Prices** come mostly from 3rd-party aggregators (2026) and change often. Verify before quoting clients.
- **B-roll-per-minute figures** in 1.5 are my heuristics, not sourced norms.
