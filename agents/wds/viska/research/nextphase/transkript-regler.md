# NextPhase AI transcripts: craft rules for Viska

Source: 8 auto-generated YouTube transcripts in `C:\temp\nextphase\transkript\`. All are paraphrased; each video gets at most one short quote. Read 2026-10-27.

**Before you read: how much concrete data is there?** Not much. These are mostly install-and-promote videos for free skills hosted in a Skool community. The real rules live inside the skill zips, which the videos never show. The transcripts give **no** numbers for caption font size, caption position, safe areas, loudness/LUFS, music ducking, colour space, resolution or bitrate. The only fps figure is 60 fps (one video). Parakeet, Whisper and Wikimedia/public-domain licensing are **never mentioned**. Where a section below says "not covered", the video really is silent on it. The gap is not missing from these notes. To get the real numbers, download the skill zips and read their rule files.

Speaker attribution: most videos are by "Jade(s)" (Jade M). 43WtLf_cAJU says "our school" and "we" and never names the speaker, so it may be Amine Hn or Jason Cooperson. The transcripts don't say which.

---

## 1. zke3bTtvmLo: "How to Make Viral Motion Graphics With AI With 0$ (Turned it into a Skill)"

**1. Workflow / roles**
- Three test videos with more and more setup: (1) one viral one-line prompt plus look notes, (2) adds roles (songwriter, animator, sound designer) and a lyric video synced to a locally generated song, (3) a full "crew" prompt (director, writer, animator, composer, sound designer, render engineer) plus a *story* instead of a task description.
- Render pipeline: Claude writes an HTML page that defines every frame, a headless browser screenshots each frame, and FFmpeg encodes the MP4. HyperFrames supplies a working starting setup, so the agent doesn't rebuild the framework each time.
- Music: the agent generated 12 song versions and checked each one before picking. For lyric sync it transcribes the sung track and maps words to timestamps. Where the transcription heard a different word with the same syllables, it matched words by position.

**2. Numbers / rules**
- 60 fps; a 16 s video = 960 frames. Video 3 has 375 sound effects.
- Sound effects are synthesized in code (whooshes, impacts, a riser into the drop, sparkles). Nothing is downloaded.
- Lyric video: each word appears exactly when it is sung.
- The music model needs a lot of disk space; it ran on a 16 GB MacBook Air.

**3. Style capture**: not covered here. The look comes from prompt text (soft space, palette, a serif font) plus a ban list.

**4. QC loop (the most useful part)**: after each round, grab a frame from the middle of every shot and put them all on one page (a contact sheet). Score each shot 1–10 on story, composition, motion, typography and sync with the music. Write down the three worst problems, fix them, and go again until every shot scores 8 or more.

**5. Blacklist**: explicitly ban the defaults, or the model falls back to them. Banned: centred text, everything fading in, and the colours, fonts and effects from the author's earlier videos. Without music and sound, motion graphics "feel like a PowerPoint".

**6. Tools / costs**: HyperFrames (open source), FFmpeg, ACE-Step 1.5 (local, free music), code-synthesized SFX. Free local voice models are mentioned but not named. Suno and ElevenLabs are named as the paid alternative. Cost is $0 beyond the Claude subscription.

**7. Flags**: the "$0" claim ignores the Claude plan. The author admits the "one prompt" viral claims are really ~10,000-character prompts plus skills. Quote: "the prompt is 10% of the video" (crediting a Twitter article). 375 SFX in about a minute is excessive density for business clients. Treat it as a demo, not a target.

---

## 2. h9ACBGZkKR8: "How to Make Vox-Style Animations in 3 Minutes with Claude Code + Omni"

**1. Workflow / roles**: seven stages, all driven from one style sheet:
1. Research (current news on the topic)
2. Script written for TTS
3. Voice (ElevenLabs)
4. Shot map: every image tied to a stretch of the voiceover
5. Image generation (Nano Banana via the Kie.ai API)
6. Motion: images turned into video clips (a video model, "Omni")
7. Cut, then music on top

Two modes: an **approval gate before image generation** (recommended until the look is locked) or fully autonomous.

**2. Numbers / rules**: landscape for YouTube long-form. Nothing else is measurable.

**3. Style capture**: a style-sheet file (the example is "cyberpunk") holding the palette, fonts and graphic guardrails. To change the look, swap the sheet.

**4. QC**: only the human approval gate. No automated review.

**5. Blacklist**: none.

**6. Tools / costs**: Claude Code, ElevenLabs (free up to ~10 min, then ~$6/month), Nano Banana (said as "$4.8 per image", which is almost certainly a misspeak), a video model at ~$0.10 per second, Kie.ai for API keys. Estimated $30/month for daily shorts and $40 for long-form.

**7. Flags**: API keys are pasted straight into the chat, which is bad practice; use env/vault. Music advice is to search YouTube for "copyright free" tracks with no licence check. Unacceptable for clients. The "passive income" and "no competition" framing is hype. Only the 7-stage order is worth keeping.

---

## 3. E8Qz5fXZIaw: "How To Make Faceless Video $12,000/month (Turned Into A Skill)"

**1. Workflow / roles**
1. Pick a reference format that is already performing. Copy the *format* (pacing, layout, narrator manner), never the story or characters.
2. Make a style sheet.
3. The agent studies the reference: it pulls frames plus the transcript and works out the narrative pattern.
4. The agent writes a new story.
5. Local TTS voice. A second character gets a separate voice with processing (a whisper filtered to sound like a 1990s phone line).
6. Music (local model, or written in code) and SFX written in code (phone ring, knocks, steam).
7. Visuals built in code: 3D sets, figures of about 40 shapes on a skeleton so they can be posed, lighting that follows the sheet.
8. Self-check: screenshot every shot, review, fix, render.
- Once the world is built, a new script re-times every shot to the new voice. That makes sequels mostly a rewrite.

**2. Numbers / rules**
- The horror reference was measured at a **cut every ~3 s**, **one line of yellow captions** and a calm male narrator.
- Hard-hat explainer: 30 s, 5 sets, 18 shots (≈1.7 s per shot), cut to the narration word by word.
- Production time: 3 min of video took ~53 min; 33 s took ~40 min; 30 s took just over an hour.

**3. Style capture (strong)**: a "style sheet" is **one image with six boxes**: fonts; colours with hex codes; characters and props; what the world looks like; how a frame is laid out; rules. Each style has a name ("Lamplit Ink Cartoon", "Red Ghost", "Sunlit Explainer"). The **rules box carries the most weight**, and the rule always wins. Example rules:
- One accent colour is reserved for a single object (the hero's beanie) and appears nowhere else.
- The hero never takes up more than 40% of frame height.
- No readable faces; figures are glowing silhouettes.
- The room is never brighter than the figure.
- Text only exists printed on an object in the scene, never floating over the image.

A style sheet can also be made from several screenshots of a channel you like: the model writes the sheet, then it is rendered once as an image.

**4. QC**: a screenshot-per-shot review before the final render.

**5. Blacklist**: no direct copying of story or characters. YouTube penalizes "mass-produced, repetitive" and inauthentic content.

**6. Tools / costs**: Higgsfield with GPT Image 2.0 (3.5 credits per style sheet, 14 credits in total), Opus 5.5 ("don't go cheap"), a Max plan, free local TTS and a local music model (neither named).

**7. Flags**: the title's income claims are other people's screenshots. The YPP threshold change "Feb 1, 2027" is unverified; check before repeating it. Code-built human figures look bad up close, as the author admits. Useful for Viska: the "style sheet in the client's colours, sold as a recurring service" idea maps directly to Swedish business clients.

---

## 4. vfhuIkbj4as: "Claude Video Editing. Posting is Now on EASY MODE. (Turned It Into A Skill)"

**1. Workflow / roles**: five systems in sequence: (1) news/niche scraper, which first asks who you are, what you do and who you're talking to; (2) word-for-word script writer; (3) editor (separate short-form and long-form editors); (4) cover/thumbnail maker; (5) poster (Blotato). **Nothing publishes without human approval.**

**2. Numbers / rules**
- Script structure: hook in the first seconds → value spread through the whole video, not front-loaded → CTA at the end.
- Short-form editor jobs:
  - cut mistakes, restarts and long pauses
  - cut out the speaker so they sit over the graphics
  - fetch real pages and posts that the speaker mentions
  - word-by-word captions
  - colour grade
  - **25–40 SFX per short**
  - 5 selectable styles
- 30–40 min per short; 2–3 can run in parallel.
- Cover formula: **one word, one scale, one trick**. The text style is identical every time; only the scene changes. The words come from the script. Make 3–4 variants and let a human pick.

**3. Style capture**: the voice is learned from the client's own recordings (calls, videos). Every correction refines it.

**4. QC**: human notes. Every note is saved into the system so the same mistake never happens twice.

**5. Blacklist**: the editor has a **21-rule blacklist**. The examples given: **no emojis** (they read as "vibe-coded"), and **never more than one highlight at the same time**. The script writer has a word blacklist of phrases the person never says.

**6. Tools / costs**: Blotato (subscription; Instagram, TikTok, Facebook), Higgsfield (an AI likeness for covers, paid credits), Opus 5.5.

**7. Flags**: the volume framing (3–7 posts/day) suits creators, not B2B clients. The AI likeness on covers needs consent and disclosure. Recording tips worth passing on to clients: record everything in one session; on a mistake, restart the sentence without stopping; don't use a teleprompter; start at one video a day. Quote: "You don't need every video to be perfect. You just need it to be done." Fine for social, but at odds with client-grade QC.

---

## 5. x0iR9Tl6zZI: "AI Content System Full Walkthrough Costs 0$ (Turned it into a skill)"

**1. Workflow / roles**: one onboarding (niche, audience, tone, goal, asked once and stored), then four parts: (1) find what is trending in the niche right now; (2) a 30-day plan of posts and carousels (hook, body, CTA) drawn in the style sheet or from the client's own photo library; (3) short-video editor (script or free-talk → record → cut pauses, animations, backgrounds, plus screenshots or screen recordings fetched for whatever is mentioned); (4) scheduled posting. The calendar view is reviewed before anything goes out.

**2. Numbers / rules**: none beyond "30 days" and a "2–5 min" setup time.

**3. Style capture**: a style sheet built from Pinterest references or from given colours and fonts, used as fixed guardrails. Alternatively, the client's real photo library (e.g. a roofer's real before/after shots).

**4. QC**: human review of the calendar.

**5. Blacklist**: generic AI or Canva look: the same layouts, fonts and colours as everyone else.

**6. Tools / costs**: Firecrawl (scraping), Higgsfield (credits; "GPT Image 2.5"), Blotato (subscription). Also an option to let Claude control the computer for setup.

**7. Flags**: the title says $0, but the video itself says this one is not $0. Mostly marketing; almost no craft content. "Let Claude control your computer" for installing connectors is a risk. Quote: "Bad prompts make bad carousels". The real point is that the system matters more than the model. Using a client's real photos instead of generated ones is the one sound idea here.

---

## 6. lUqjRmtN7bE: "The New Claude Motion Is Awesome (Scary Good)"

**1. Workflow / roles**: plan the video with Claude in a normal chat until the prompt is solid → build with Claude Code + HyperFrames → preview in the browser and scrub second by second → render the MP4 locally. For photoreal content there are two steps: generate the image with an image model, then animate everything on top in code.

**2. Numbers / rules**: the **four-part motion brief**:
1. Audience, platform and length (e.g. a 20 s Instagram promo for a barber shop).
2. The look: hex codes, fonts, mood.
3. Scene by scene with timecodes ("0–4 s: …").
4. Rules: what it must never do. Examples: **never more than 6 words on screen**; **prices always in the brand colour**.

**Single source of truth**: every word, price and colour sits in one config block at the top of the file. A change (e.g. haircut price $25→$30, a pole recoloured gold) is one line, and timing and motion stay identical.

**3. Style capture**: the "look" and "rules" parts of the brief, the same idea as the style sheet.

**4. QC**: browser preview and scrub before rendering.

**5. Blacklist**: no generated footage or AI people in code-only motion (that is Claude Motion's own limit).

**6. Tools / costs**: Claude Motion (beta, Team/Enterprise only, off by default on Enterprise; exports to Adobe, Descript, HeyGen, Higgsfield, etc.). HyperFrames (free, open source, made by the HeyGen team). ACE-Step 1.5. A cheaper model ("HiQ 5.5", probably Haiku) suggested for saving usage. Higgsfield for product images.

**7. Flags**: the "editable vs. regenerate" argument is correct and the main reason to use code-based motion. Very relevant for clients whose prices and opening hours change. The claim that the $20 plan works is hedged by the author's own warning that usage burns fast.

---

## 7. 43WtLf_cAJU: "How to Make a FREE AI Video Editor & Motion (NO CLAUDE)"

**1. Workflow / roles**: OpenCode (open-source agent CLI) running GLM 5.3 Flash (free) loads the same skill folder ("editor v1") that Claude Code uses. Setup: install Python, FFmpeg, the renderer and a speech-to-text model, plus an optional background-cutout model (~1 GB; the effect puts a large word behind the speaker's head). Then render a **smoke-test video** to prove the install works. Each edit: drop the video in → the agent **shows its plan** → human approves → build → open the result.

**2. Numbers / rules**
- What the skill holds: how often the picture changes, colours, sounds, and rules that must not be broken (no values are given).
- Start with a ~30 s clip, not a 20-minute video.
- Feedback must cite the exact second ("at 0:05, swap this image").
- Ask for a time estimate before the build.

**3. Style capture**: notes are written **into the skill files, not just the session**, so every later edit inherits them.

**4. QC**: the plan-approval step, the smoke test, and human review with timestamped notes.

**5. Blacklist**: not covered.

**6. Tools / costs**: OpenCode (free, open source); GLM 5.3 Flash (~320B parameters, MIT licence, free in OpenCode since Oct 16, but **it runs in the cloud, not locally**); FFmpeg; Python; a local STT model (not named). On Windows, WSL is recommended. Claude plan prices for comparison: Pro $20, Max $100/$200.

**7. Flags**: "$0, no account, fully local" is only partly true. The model call goes to a cloud provider; the provider's no-retention claim needs checking before client footage is sent (GDPR, client confidentiality). Sound advice: **build skills with a strong model, run them with a cheaper one**. The demo engine-explainer was made with the paid Claude editor, not the free one.

---

## 8. VX7_oywIB4g: "How I Fully Automated My Video Editing (Claude Code)"

**1. Workflow / roles**: one editor folder per format (long-form and shorts are kept apart because "they need to learn their own skills"). Give Claude the HyperFrames skill plus catalog and one reference reel. Ask it to describe how that creator edits (motion style, colours, fonts, layout) and save it as a **named style** ("fitness influencer"). Questions from the agent are welcomed. Then record and edit.

**2. Numbers / rules**: target is reproducing **60–70%** of the reference's look. Three of the author's own named styles:
- "motion graphic"
- "prosa": colour grade, clear captions, a transparent overlay of context-matched material fetched online instead of stock filler
- "deep talk": for emotional content

**3. Style capture**: a growing **style library** per style: colours, fonts, B-roll types, layout, writing style, with clickable scene examples. Keep adding references found on social media. The analysis covers B-roll usage, palette, typography and on-screen writing style.

**4. QC**: iterate on the library with the agent. No formal check is described.

**5. Blacklist / AI slop (explicit)**: emojis flying in at random, squares popping up everywhere, stock default colour fonts, and taking the one or two popular tools and only swapping the colour. Quote: "What I can't stand is the sloppy version of it."

**6. Tools / costs**: HyperFrames (HeyGen) with its catalog of styles/blocks, the Claude desktop app → Claude Code.

**7. Flags**: the author admits this is not the best method. Building a style from one named living creator's reel is a likeness/ethics issue for client work; derive styles from several references and the client's brand instead. "If your edits are sloppy, it's probably you" is a fair point (system over tool) but not actionable.

---

## Cross-video gaps (for Viska to fill itself)

- **No caption specs** beyond "word-by-word" and "one line, yellow". Viska must define size, safe area, max chars per line, and a Swedish line-break policy itself.
- **No audio specs**: no loudness target, no ducking, no SFX level relative to the voice. Swedish broadcast and web practice (e.g. −14 LUFS for social, EBU R128 −23 for broadcast) must come from elsewhere.
- **No resolution / aspect / safe-zone numbers** except 60 fps and "landscape for YouTube".
- **No licensing practice.** Several systems "fetch real posts/pages/screenshots online" with no word on rights. ACE-Step/AI music licence terms, Wikimedia attribution and public-domain checks are all absent. Viska needs its own source-and-licence log.
- **No Swedish/multilingual handling.** STT and TTS models are unnamed; Parakeet and Whisper never come up.

---

## Top 25 rules worth adopting

1. Before every render, grab a mid-shot frame from each shot into one contact sheet. (zke3bTtvmLo)
2. Score each shot 1–10 on story, composition, motion, typography and audio sync; fix the 3 worst issues; repeat until every shot is at least 8. (zke3bTtvmLo)
3. Keep an explicit ban list of defaults (centred text, everything fading in, house fonts/colours from earlier jobs) and check every shot against it. (zke3bTtvmLo)
4. Never deliver motion graphics without designed sound; every visual hit needs an audio cue or a deliberate silence. (zke3bTtvmLo)
5. Generate several music candidates and pick by checking fit, not the first output. (zke3bTtvmLo)
6. When syncing text to audio, use word timestamps from STT. If the STT word differs from the script, align by position and syllable count, never by guessing. (zke3bTtvmLo)
7. Run production in a fixed order: research → script → voice → shot map tied to voice timestamps → visuals → motion → cut → music. Don't start visuals before the voice is locked. (h9ACBGZkKR8)
8. Hold a human approval gate before any paid generation until the client's look is signed off. (h9ACBGZkKR8)
9. Store every client style as a named style sheet with six fields: fonts, hex colours, characters/props, world, frame layout, rules. (E8Qz5fXZIaw)
10. Write style rules as checkable absolutes (e.g. "accent colour only on X", "subject ≤ 40% of frame height", "text only on objects in the scene") and let a rule override any creative choice. (E8Qz5fXZIaw)
11. When analysing a reference, measure cut interval, caption lines/colour and narrator manner from extracted frames plus the transcript. Copy the format, never the content or characters. (E8Qz5fXZIaw)
12. Build each project so that a new voiceover re-times every shot automatically: shots keyed to transcript timestamps, not fixed frame numbers. (E8Qz5fXZIaw)
13. Write every brief in four parts: audience/platform/length; look (hex, fonts, mood); scene list with timecodes; never-rules. (lUqjRmtN7bE)
14. Limit on-screen text to at most 6 words at a time unless the style sheet says otherwise. (lUqjRmtN7bE)
15. Always render prices, offers and key numbers in the brand accent colour. (lUqjRmtN7bE)
16. Put all client-editable copy, prices and colours in one config block at the top of the composition, so a change is one line and nothing else moves. (lUqjRmtN7bE)
17. Use code-built motion for text, charts and brand assets; use real or generated photography only as a layer underneath, never AI-generated people in client work without explicit consent. (lUqjRmtN7bE)
18. Scrub the HyperFrames browser preview before every final render. (lUqjRmtN7bE)
19. Show the edit plan and a time estimate and get approval before building. (43WtLf_cAJU)
20. Write every accepted client note into the skill/style file, not only the session, and confirm it was saved. (43WtLf_cAJU)
21. Ask for and record feedback with exact timecodes; reject vague notes and ask for a second mark. (43WtLf_cAJU)
22. Run a short smoke-test render (~30 s) after any setup change before taking on a long job. (43WtLf_cAJU)
23. In talking-head edits, remove fluffs, restarts and long pauses, and never show more than one highlight/emphasis at a time. (vfhuIkbj4as)
24. No emojis, random popping shapes or default "colour fonts"; treat these as automatic QC failures. (VX7_oywIB4g)
25. Keep separate style libraries for long-form and short-form, and replace stock filler with context-matched material only after its source and licence are logged. (VX7_oywIB4g)
