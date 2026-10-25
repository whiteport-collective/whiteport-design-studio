# Research A: Editing Craft for Viska (AI media agent, DaVinci Resolve Studio)

Research date: 2026-10-25. Written for the Whiteport Design Studio "Viska" agent.

## 0. How to read this document

- Every claim carries a source URL. Where I add my own synthesis or a number that no source gives, it is tagged **[Inference]**. Where sources conflict or are weak, it is tagged **[Uncertain]**.
- **Source quality varies a lot.** The strongest sources are Walter Murch (book via secondary summaries, plus a direct interview), the Cutting et al. shot-length study, EBU R95, platform documentation (TikTok, Meta via Socialync), Frame.io, PremiumBeat and No Film School. Much of the per-format guidance on the web comes from production-company and tool-vendor blogs (CapCut, invideo, Splice, Capsule, and others), which share a common framework but are marketing-adjacent. I treat their numbers as practitioner starting points, not standards.
- Genre-specific average shot lengths (ASL) for corporate formats are **not documented in any research I found**. The ASL figures in section 1 are labeled as inference and should be calibrated by Viska against reference films the client approves.

---

## 1. Foundations that apply to every production

### 1.1 Murch's Rule of Six (the priority stack for any cut)
Walter Murch (*In the Blink of an Eye*) ranks what a cut must satisfy, with weights:
1. Emotion, 51%
2. Story, 23%
3. Rhythm, 10%
4. Eye trace, 7%
5. Two-dimensional plane of the screen (screen direction, axis), 5%
6. Three-dimensional space (spatial continuity), 4%

Sources: https://cloud.wikis.utexas.edu/wiki/spaces/rtf318/pages/80022510/Murch+s+Rule+of+Six , https://artlist.io/blog/eye-trace-and-rule-of-six-editing/ . The percentages come from secondary summaries of the book; I did not check them against the book itself **[Uncertain on exact wording, consistent across sources]**.

- The ideal cut satisfies all six. When it cannot, give them up **from the bottom**: emotion is worth more than the other five combined, and if the emotion is right it masks other faults. https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch
- **Agent rule:** for each candidate cut point, score emotion first. Do not pick a cut because it is "on the beat" (rhythm, 10%) if another frame lands the emotional beat better.

### 1.2 Where exactly to cut: the blink and the decisive moment
- Murch noticed his cuts kept landing where Gene Hackman blinked. He treats the cut as a "blink" that separates and punctuates ideas. https://musicbed.com/blog/filmmaking/editing/editing-secrets-from-legendary-editor-walter-murch
- Cut "just before the blink", if the actor is in character. Never cut mid-blink ("looks like how it feels when you get something in your eye"). For a double-take, cut right after the blink. Override the blink rule if the moment calls for it. https://www.provideocoalition.com/aotc-murch-bcpc/
- Murch looks for the "decisive" moment in a shot and chooses iconic frames as cut points (the cut acts like a "flashbulb" that fixes images in memory). He dislikes mindless match-on-action as a default. Same source.
- For corporate interviews, Frame.io advises cutting on the frame just before or after a blink to avoid shifty-looking expressions. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/
- Every Frame a Painting ("How Does an Editor Think and Feel?") argues editing is driven by the eyes, which carry the emotion, and that repeated viewing trains the editor to "feel the moment when the shot wants you to cut". https://www.openculture.com/2016/05/the-alchemy-of-editing-film.html , https://subtraction.com/2016/05/23/how-does-a-film-editor-think-and-feel/amp

### 1.3 Story first, picture second (interview-driven work)
- Build a rough assembly from interviews only, with no B-roll, until the story works as audio alone, like a radio piece or podcast. Then add B-roll. Story and structure come before music, sound design, colour and graphics. https://nofilmschool.com/2015/11/how-cut-short-documentary-films-part-two-building-story-adding-b-roll
- Doc-style workflow: one "selects" timeline of the best soundbites from every interview, then trim over several passes. https://s-films.com/?p=1134
- Version the sequence at every major step so experiments can be reverted. https://nofilmschool.com/2015/11/how-cut-short-documentary-films-part-two-building-story-adding-b-roll
- One video, one proposition. If there are competing messages, make two videos. Cut every theme that does not serve the proposition. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/

### 1.4 Pace: what "normal" looks like
- Hollywood average shot length (ASL) fell from about 10 s in the 1930s–40s to below 4 s after 2000 (160 films, 1935–2010). Shorter shots in recent films also carry more motion per unit of time. https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/
- Secondary reports of Cutting's work give about 2.5 s "today", but that figure is not in the paper itself. https://flowingdata.com/2014/09/22/evolution-of-movies/ **[Uncertain]**
- **[Inference] Starting ASL bands for Viska** (no source gives genre ASLs; calibrate against client-approved references): interview-led doc or testimonial 3–6 s for B-roll, with interview shots held longer while the speaker carries emotion; brand film 2–4 s; event recap 1–2.5 s in the build, 0.5–1.5 s at the peak; social talking-head, a visual change every 2–5 s. More important than the average is **variation**: vary shot length and speed with the music (https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie). Do not stay on one emotional note for more than about 45 s (https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/).

---

## 2. Per production type

Each section covers length, structure, A-roll/B-roll, pacing, music, opening and ending, and common mistakes. A-roll means the primary content, usually interview or presenter. B-roll means supporting visuals.

### 2.1 Event recap / aftermovie

**Length**
- Corporate event recap: most run about a minute or less (Canon). https://www.canon.ca/en/Pro-Inspiration/Five-steps-for-producing-engaging-event-recap-videos
- RainFocus, an events-platform vendor, recommends 2–4 minutes with one song. https://rainfocus.com/blog/15-points-of-a-great-recap-video/
- Festival aftermovies compress about 3 days into 5–20 minutes, plus a 30 s social cut. https://festivalpro.com/festival-management/2103/news/2022/9/29/Get-to-Grips-with-the-Music-Festival-Aftermovie.html
- A practitioner festival editor says keep it as short as possible: leaving viewers wanting more beats boring them. https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie
- **[Inference]** For Swedish SME and B2B events, deliver a 60–90 s master, a 15–30 s 9:16 cut and a 6 s bumper. 60–90 s is also cited as a practical target, and 15–30 s for Reels, in https://beverlyboy.com/filmmaking/how-to-repurpose-event-footage-post-event/ and https://fotoowl.ai/blogs/how-to-turn-event-photos-into-an-instagram-ready-recap-video

**Structure**
- Three acts: beginning, climax, end. Open with a visually interesting hook, but **do not reveal the peak**: no night or fireworks at the start. Build anticipation the way arriving at a festival does. Hold high-energy moments for the climax and save the strongest material for last. https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie
- Corporate variant: tell it chronologically, mixing visuals with brief interviews of organisers and participants. Use text overlays sparingly. Avoid voice-over narration (called clichéd). End with a brand-relevant CTA, such as next year's registration or a hashtag. https://www.canon.ca/en/Pro-Inspiration/Five-steps-for-producing-engaging-event-recap-videos
- Start with something striking and skip long venue establishing shots. Build a storyline that evokes emotion, "not just a series of beautiful images". https://www.eventplanner.co.uk/news/10766_the-art-of-the-perfect-aftermovie.html
- The two sources conflict on establishing shots. Piree wants the venue established (drone or wide) before close-ups; Event Planner says skip lengthy location shots. **[Inference] Resolution:** establish in 1–2 short, striking shots, not a slow tour.

**A/B ratio**
- Mostly B-roll, with short quotes ("keep any quotes short and memorable"). https://rainfocus.com/blog/15-points-of-a-great-recap-video/
- **[Inference]** About 80–95% B-roll. Interview bites of 3–8 s, used as anchors, not exposition.

**Pacing and music**
- Pick tracks with dynamics, changes and tempo shifts so the picture can follow. Line up movement (jumps, DJ actions, pyro) with musical changes. Avoid mechanical on/off-beat cutting. https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie
- Place key scenes at the song's high points. https://rainfocus.com/blog/15-points-of-a-great-recap-video/
- Keep camera movement in every shot. If footage is static, add digital push-ins (shoot 4K for a 1080 timeline). Shoot slow motion at 100 fps or more. https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie
- Keep visuals consistent: similar colours, shapes, lines and textures. Capture smiles and laughter, VIPs and behind-the-scenes. https://rainfocus.com/blog/15-points-of-a-great-recap-video/
- Lay crowd audio under the music, either recorded on camera or from a library. https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie

**Ending**
- The strongest material goes last, visually distinct from the climax. Then the logo or CTA. https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie , https://rainfocus.com/blog/15-points-of-a-great-recap-video/
- End the music with the picture rather than fading it out. https://wistia.com/blog/9-video-production-faux-pas-to-avoid

**Amateur mistakes**
- Climax too early, no sense of place, static footage, too long, explicit storylines. https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie
- Spelling errors in names and on-screen text, and uncleared music rights. https://rainfocus.com/blog/15-points-of-a-great-recap-video/
- A tourism or folk-event angle favours warm, human edits (faces, hands, crafts) over pure hype, and credits contributors. https://www.ticketfairy.com/blog/2025/08/25/the-festival-after-movie-that-feels-like-home-editing-and-rights/

### 2.2 Brand / company film

**Length**
- A flagship film is usually 2–5 minutes, with short social cut-downs. https://blaremedia.net/what-is-a-brand-film/
- Another production company says 3–10+ minutes. https://akshonmedia.com/services/brand-films/
- BBH Labs argues against long manifestos ("just strategy set to a mood film") and wants brand ads as short as possible. https://www.bbh-labs.com/forget-manifestos-brand-ads-should-be-as-short-as-possible
- **[Inference]** For SMEs: a 90–150 s hero film plus a 30 s and a 15 s cut-down.

**Purpose and structure**
- A brand film answers "why should I trust you" rather than "why buy today". https://blaremedia.net/what-is-a-brand-film/
- Use a three-part arc: attention-grabbing opening, body, closing CTA. Open on the problem the company solves, not on the company itself. https://www.peppercontent.io/blog/a-beginners-guide-to-structuring-a-strong-corporate-video
- Hook that hints at the main message; save the strongest theme for last; place objections before the theme that answers them, with the biggest objection near the end; show the improved "after" life, but add obstacles and contrast so it is not flat. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/

**A/B ratio**
- Viewers tire of long talking heads, so B-roll carries much of the load. https://s-films.com/?p=1134
- Try a B-roll-led cut, with voice carrying the story. Use props, stock or simple animated icons for abstract points. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/
- **[Inference]** 60–80% B-roll on screen. Interview audio runs much longer than interview picture.

**Tone**
- Corporate work suits a "more conservative approach with images that underline the spoken words". Documentaries can use dramatic contrast. https://artlist.io/blog/?p=6387
- Play against expectations where the brand allows, such as a serious subject delivered with humour or an unexpected audio/visual pairing. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/

**Music**
- Supports, never overpowers; clean audio is the priority. https://www.finchley.co.uk/finchley-learning/videography-editors-guide-to-editing-corporate-videos
- Do not score wall-to-wall: silence is valid. https://www.premiumbeat.com/blog/how-to-edit-a-film-to-music-without-it-becoming-a-music-video

**Amateur mistakes**
- Several messages in one film, one emotional tone held too long, visible jump cuts and verbal clutter, no clear CTA. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/

### 2.3 Customer testimonial / case video

**Length**
- Under about 2 minutes. https://levitatemedia.com/learn/video-testimonial-script
- **[Inference]** 60–120 s master, 20–40 s social cut built around the single best result line.

**Structure**
- Problem, then solution, then result, sometimes plus a recommendation. https://testimonial.to/resources/video-testimonial-script-examples , https://capsule.video/blog/video-testimonial-tips
- **Problem:** what it cost the customer (time, difficulty, not knowing how to fix it), so the viewer recognises themselves. https://capsule.video/blog/video-testimonial-tips
- **Result:** specific numbers ("saved 15 hours a week" beats "it's great"). https://testimonial.to/resources/customer-video-testimonials
- **Ending:** a short endorsement inviting others. https://boast.io/?p=26439

**Authenticity**
- Use prepared questions, never scripted lines. Non-actors should not "act". https://testimonial.to/resources/video-testimonial-questions , https://wistia.com/blog/9-video-production-faux-pas-to-avoid
- Reorder lines if needed, but never change the speaker's meaning. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/
- Ethical limit: "frankenbites" (stitching words into statements never made) are a recognised manipulation in factual editing. https://yorkspace.library.yorku.ca/xmlui/handle/10315/38136
- **[Inference] Hard rule for Viska:** no sentence may be assembled from fragments that changes or strengthens what the customer actually said. Any reorder must be logged for client approval.

**A/B ratio**
- **[Inference]** About 40–60% interview on screen. More interview than in a brand film, because the face is the proof. Cover every internal edit with B-roll of the customer's real workplace or product in use, or with a punch-in.

**Covering edits**
- Punch in about 40–50% for emphasis, keeping the eyes aligned across the cut. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/
- In Resolve, Smooth Cut (optical flow, 2–4 frames) hides small pauses where head position barely changes. https://www.premiumbeat.com/blog/easier-interview-editing-with-davinci-resolves-smooth-cut-transition , https://www.rippletraining.com/?p=11828 , https://forum.blackmagicdesign.com/viewtopic.php?p=556033

**Opening**
- The problem section must "pop from frame one". https://capsule.video/blog/video-testimonial-tips
- **[Inference]** A cold open on the strongest result or emotion line also works, before returning to the problem.

### 2.4 Interview / mini-documentary

**Structure**
- Basic three acts, built audio-first (section 1.3). https://nofilmschool.com/2015/11/how-cut-short-documentary-films-part-two-building-story-adding-b-roll

**B-roll prompts**
- Can visuals illustrate key moments? Can a B-roll sequence replace interview ("Showing can be far more powerful than telling")? Can B-roll draw parallels between people or places? Can it foreshadow a later reveal? Can it create transitions between key moments? Same source.

**Scope**
- A short-form micro-doc should not try to cover a whole company history: one story only. https://www.capcut.com/create/micro-documentary-short-form-video

**Rhythm**
- Too fast confuses, too slow loses interest. Keep the interview on 1–2 tracks and B-roll on separate tracks. https://artlist.io/blog/?p=6387
- Documentary can use narrative contrast and point of view. Same source.

**Sound**
- Room tone under every dialogue edit (section 4.3). Use L-cuts to show a listener's reaction. https://vimeo.com/blog/post/guide-to-film-cuts
- **[Inference]** Length 3–8 min for web docs, plus a 60–90 s trailer. ASL is longer than in the other formats; allow holds of 5–10 s on emotional faces and on landscapes.

### 2.5 Talking-head explainer for social

**Hook**
- TikTok says about 90% of ad recall impact is captured in the first 6 s, so land the value proposition early. Faster scene changes help at the start. https://ads.tiktok.com/business/en-CA/blog/creative-best-practices-top-performing-ads
- Instagram's Adam Mosseri: "The first three seconds of a reel are super important". The often-quoted "3 seconds" Facebook IQ figure does not actually appear in that study **[Uncertain]**. https://www.opus.pro/blog/facebook-reels-hook-formulas
- Open with the payoff or product, not a logo animation. https://adadvisor.ai/blog/meta-video-ad-script

**Sound-off**
- Key messages must appear as on-screen text, not only spoken. Test by watching on mute. https://segwise.ai/blog/anatomy-top-performing-video-ad-frame-by-frame
- TikTok counters that 88% of its users say sound is vital, so design for both. https://ads.tiktok.com/business/en-CA/blog/creative-best-practices-top-performing-ads

**Jump cuts**
- Standard in this genre: remove pauses, filler and mistakes to raise words per minute, at a cadence that still feels natural. https://www.gling.ai/blog/ultimate-guide-to-jump-cuts-master-your-video-editing-skills
- Vary the frame with punch-ins or a second angle, or put a graphic over a topic change. https://nofilmschool.com/easy-ways-to-hide-jump-cuts-your-next-video , https://subscribr.ai/youtube-strategy/editing-talking-head-videos-engaging

**Pattern interrupts**
- A new visual, sound, pace or question every 8–12 s, per creator blogs **[Uncertain, vendor sources]**. https://www.gofaceless.ai/blog/optimize-video-engagement-pattern-breaks
- A deliberate pause of 0.5–1 s before a key point works. Silences over about 1.5 s read as a frozen video. https://www.socialync.io/blog/retention-techniques-keep-viewers-watching-2026 **[Uncertain]**

**Length**
- Platforms now allow 3 minutes: Reels went from 90 s to 3 min, and Shorts from 60 s to 3 min. https://www.socialmediatoday.com/news/instagram-officially-expands-reels-length-to-3-minutes/737766/ , https://socialnewsdesk.com/?p=18258
- Ad guidance is 6–15 s for prospecting and 15–30 s for consideration. https://www.stackmatix.com/blog/meta-video-ads
- **[Inference]** For organic explainers: 30–60 s, one idea, hook, then three beats, then CTA.

**Slop warning**
- Template editing (same hook pattern, caption style, pacing and AI voice in every video) is exactly what platforms and viewers now flag as slop. https://www.vozo.ai/blogs/youtube/youtube-ai-slop , https://artlist.io/blog/what-is-ai-slop-and-why-it-matters-for-video-creators/

### 2.6 Product / launch film

**Structure**
- Recurring pattern across 20+ SaaS launch videos: hook, solution, demo, features, CTA. https://contra.com/community/kLiYx05n-perfect-product-video-structure-hook-solution
- The alternatives are a problem-first open or a teaser that withholds the product. https://www.atlabs.ai/blog/25-ai-video-script-templates-for-product-launch-campaigns

**Feature framing and beats**
- "It does X so you can Y". https://www.atlabs.ai/blog/25-ai-video-script-templates-for-product-launch-campaigns
- Each motion beat has one job: reveal, compare, emphasise, transition or close. The first frame should explain the topic without audio, and the last frame says what to do next. https://hera.video/blog/b2b-saas-feature-announcement-video-guide

**Length**
- 30–45 s for a homepage. 12–20 s for 9:16, with one hook and one proof point. https://hera.video/blog/ai-product-launch-video-generator-guide **[vendor numbers]**

**Brand and product timing**
- Show the product on screen: TikTok reports +65% brand affinity and +25% recall. Use CTA cards rather than interrupting content (+45% recall). https://ads.tiktok.com/business/en-CA/blog/creative-best-practices-top-performing-ads
- Branding in the first seconds should be subtle and must not compromise the hook. https://ads.tiktok.com/business/library/Creative_Codes_ENG.pdf

**Editing**
- Speed ramps and match cuts fit product reveals: ramp into a reveal, then hold real time on the product (section 3).
- Use hit-point SFX sparingly (section 4.4).
- **[Inference]** Shot length is short in the hook (under 1 s) and longer on demo shots, so the viewer can read the UI or product.

### 2.7 Recruitment / employer-brand film

**Length**
- Under about 2 minutes, unless the story is compelling. https://www.ere.net/8-tips-for-creating-stellar-employer-branding-videos
- 15–30 s for social, 2–3 min for full showcases. https://vidcruiter.com/video-interviewing/recruitment-videos/
- "Five short ones are better than one long one." https://www.storybox.cloud/en/blog/recruiting-videos-attract-top-talents

**One idea per video**
- Do not try to cover a whole department in 15 s. https://onrec.com/news/how-short-form-video-is-transforming-recruitment-marketing-and-employer-branding

**Authenticity is the brief**
- Ask "Is this us?" throughout. Do not film a snack-filled break room if people bring their own lunch. Prepare employees but do not over-script; let them be themselves. https://www.ere.net/8-tips-for-creating-stellar-employer-branding-videos
- A slightly rough real-employee clip often beats an overproduced one. Employee voices are more credible than management's. https://hudsontalent.com/insight/how-employer-brand-videos-draw-talent/ , https://theundercoverrecruiter.com/employer-brand-video/
- **[Inference] Editing implications:** natural grade, real workplace sound (room tone, ambience) kept audible, unpolished moments and laughter kept, minimal flashy transitions, employees named with lower thirds, and an end card pointing to the careers page.

**Measure**
- Careers-page traffic, time on listings with video, and application quality and time-to-fill. https://vidcruiter.com/video-interviewing/recruitment-videos/

### 2.8 9:16 Reels / Shorts / TikTok (any of the above, adapted)

**Hook**
- Value inside 6 s. Branding subtle early. CTA as a card. https://ads.tiktok.com/business/en-CA/blog/creative-best-practices-top-performing-ads , https://ads.tiktok.com/business/library/Creative_Codes_ENG.pdf

**Safe areas**
- See section 5.3. Keep text and faces out of the bottom 35% and the right-hand button column.

**Text**
- Text overlays increase view time and recall (TikTok, no numbers given). https://ads.tiktok.com/business/en-CA/blog/creative-best-practices-top-performing-ads
- Captions for sound-off viewing. https://segwise.ai/blog/anatomy-top-performing-video-ad-frame-by-frame

**Re-edit, do not just crop**
- **[Inference]** Short-form versions need a faster opening, fewer text lines and visuals that work on mute (https://hera.video/blog/b2b-saas-feature-announcement-video-guide). Reframe every shot for 9:16 (Resolve Smart Reframe, then manual check). Rebuild the hook rather than using the first seconds of the 16:9 master.

**Tourism and hospitality (Visita-type clients)**
- Use ambient destination sound to build a sense of place, with music not overpowering natural sound. Open with wide establishing shots plus ambience. Hotel order: arrival, lobby, room, food and beverage, amenities, local highlights, logo. Mix wide, medium and close shots. Grade naturally and avoid over-editing. Avoid stereotypes. 60–90 s main, 15–30 s social. https://spliceapp.com/blog/destination-arrival-editing-workflow-tips-for-beginners/ , https://spliceapp.com/blog/hotel-arrival-video-edits-for-travel-vlogs/ **[vendor blog, repetitive content]**

---

## 3. Cut and transition vocabulary: when to use and when not

General principle: the default is the straight cut. Every other device must be motivated by story, emotion or rhythm (Murch's ranking, section 1.1). Wistia: avoid stock transitions, because they "tend to look unprofessional and don't add anything", and use a hard cut. https://wistia.com/blog/9-video-production-faux-pas-to-avoid

### Straight (hard) cut
- **Use:** almost always. Professional live production cuts most of the time. https://tfwm.com/?p=7314
- **Avoid:** between two near-identical framings of the same subject (that is a jump cut, see below), or across the 180° line without motivation. That is Murch's 2D-plane criterion (https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch).

### J-cut (audio leads the picture)
- **Use:** to build anticipation for the next image, open a scene with atmosphere before the picture, signal a tonal shift, or bring in a new speaker. https://vimeo.com/blog/post/guide-to-film-cuts
- **Use:** to create urgency. https://www.adobe.com/creativecloud/video/discover/j-cut-and-l-cut
- **Avoid:** when the incoming sound would confuse who is speaking. **[Inference]**

### L-cut (audio carries over the picture)
- **Use:** to extend an emotional beat, show a reaction, carry voice-over or a song through a montage, or hold the last scene's audio a moment longer at the end. https://vimeo.com/blog/post/guide-to-film-cuts
- **Mix:** use both J and L cuts in a scene so the rhythm is not monotonous. https://borisfx.com/blog/l-and-j-cuts-smoother-more-cinematic/
- **Avoid:** in punchy comedy, beat-matched social clips and hard reveals, where a straight cut is better. https://www.capcut.com/create/j-cuts-and-l-cuts-dialogue-edits

### Match cut
- **Graphic:** matches shape, colour or composition (2001's bone to spacecraft; Psycho's drain to eye). Reads as a visual metaphor or a time jump. https://www.soundstripe.com/blogs/how-to-use-match-cuts-in-film-and-video-editing , https://filmdaft.com/?p=36584
- **Action:** carries a movement across the cut (Indy's hat toss). https://www.adobe.com/creativecloud/video/discover/match-cut.html
- **Sound:** a shared or similar sound bridges the shots (kettle steam to train whistle). https://www.soundstripe.com/blogs/how-to-use-match-cuts-in-film-and-video-editing
- **Use:** for transitions between locations, times or ideas in brand films and launches. This is "matching scene transitions" as a craft tool, as analysed in Every Frame a Painting on Edgar Wright. https://www.moviemaker.com/edgar-wright-visual-comedy-video/
- **Avoid:** one per minute is plenty **[Inference]**. Each one should carry meaning, not just be a shape gimmick.

### Cutting on action
- Viewers' eyes follow the motion, so the cut becomes invisible and implies continuous time. Cut mid-movement, not before or after, matching speed and direction. https://en.wikipedia.org/wiki/Cutting_on_action , https://howtofilmschool.com/dictionary/match-on-action/
- Natural attention lapses (a saccade as an object exits the frame) hide cuts. https://era.ed.ac.uk/handle/1842/1076
- **Caveat:** Murch warns against using match-action mindlessly. https://www.provideocoalition.com/aotc-murch-bcpc/

### Cutaway / insert
- A **cutaway** leaves the main action and returns. It hides jump cuts and time skips; in interviews it can be to the interviewer ("noddies") or to B-roll. An **insert** is a close detail inside the scene. https://wikipedia.com/wiki/Cutaway_gag , https://www.tella.com/definition/cutaway
- **Use:** to cover every interview edit. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/
- **Avoid:** literal "wallpaper" B-roll that only repeats the words (say "teamwork", show a handshake). **[Inference]** This matches the slop tell "generic stock footage that doesn't connect to the narration" (https://artlist.io/blog/what-is-ai-slop-and-why-it-matters-for-video-creators/).

### Jump cut
- **Use:** in social talking-heads to raise density. https://www.gling.ai/blog/ultimate-guide-to-jump-cuts-master-your-video-editing-skills
- **Avoid:** in brand films, testimonials and docs, where you plan B-roll instead. https://wistia.com/blog/9-video-production-faux-pas-to-avoid
- A jump cut mainly shows time passing; a smash cut is about contrast. https://www.studiobinder.com/blog/what-is-a-smash-cut-definition/
- **Hide:** with a punch-in of about 40–50% plus eye alignment, a second angle, Smooth Cut, or a graphic. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/ , https://nofilmschool.com/easy-ways-to-hide-jump-cuts-your-next-video

### Smash cut
- An abrupt cut to a sharply contrasting scene. **Use:** for maximum contrast, comedy punchlines (the "Gilligan cut"), shock, or waking from a nightmare. https://en.wikipedia.org/wiki/Smash_cut , https://www.studiobinder.com/blog/what-is-a-smash-cut-definition/
- It depends on surprise. **Avoid:** repeating it. https://filmlifestyle.com/what-is-a-smash-cut/
- **[Inference]** Typical pairing: silence or a quiet shot, then a loud, busy shot on a musical hit.

### Cross-cutting / parallel editing
- Alternates between simultaneous or linked actions to build tension or invite comparison. https://www.soundstripe.com/blogs/parallel-editing-and-cross-cutting , https://www.studiobinder.com/blog/cross-cutting-parallel-editing-definition/
- **Use:** "preparation versus event" (crew setting up while guests arrive; chef cooking while a guest travels to the restaurant) in recaps and tourism films. **[Inference]**
- **Avoid:** more than 2–3 strands in short pieces. **[Inference]**

### Montage
- Short shots that condense time, space and information, often (not necessarily) unified by a music cue. The canonical example is the opening of *Up*. https://en.wikipedia.org/wiki/Montage_(filmmaking) , https://howtofilmschool.com/dictionary/montage/
- Music should swell across montages rather than sit at one flat level. https://www.premiumbeat.com/blog/how-to-edit-a-film-to-music-without-it-becoming-a-music-video

### Whip pan
- **Shoot:** both pans in the same direction and at similar speed, with motion blur to hide the join (slow shutter). A short dissolve can cover brightness or colour mismatches. https://nofilmschool.com/how-to-do-a-whip-pan
- **Avoid:** overusing it, which feels chaotic and gimmicky. Edgar Wright (*Scott Pilgrim*) is the model of motivated use. https://www.clueso.io/glossary/whip-pan , https://beverlyboy.com/film-technology/whip-pans-that-dont-suck-clean-transitions
- **[Inference]** Only use whips shot in camera. Fake digital whips between unrelated static shots are a template tell.

### Speed ramp
- **Use:** to emphasise a key action or reveal, or to build suspense. "You don't just want to speed ramp everything." https://www.premiumbeat.com/blog/wp-json/wp/v2/posts/46125 , https://www.kapwing.com/resources/how-to-use-the-speed-ramp-effect/
- **How:** needs high-frame-rate source (50/100 fps or more), gradual ramps, not too large a speed change. https://www.kapwing.com/resources/how-to-use-the-speed-ramp-effect/
- In Resolve, use Retime curves with Optical Flow or Speed Warp for non-HFR material. https://forum.blackmagicdesign.com/viewtopic.php?p=1141174

### Dip / fade to black (or white)
- Marks the end of a chapter or theme, a storyline switch, or a jump forward in time. **Avoid:** between chronologically close scenes in the same place, which should be cut. https://www.premiumbeat.com/blog/how-when-why-fade-black/
- It pulls viewers out of the story, so use it only where a full stop is wanted. A short fade feels functional; a long one feels reflective. https://www.wevideo.com/blog/fade-black , https://www.nfi.edu/fade-to-black
- **[Inference]** Dip to white reads as a flash, memory or euphoric peak. Use it at most once per film.

### Dissolve / cross-dissolve
- Reads as amateur when used by default. It is a holdover from the stage curtain. Between similarly framed people it can look like one is morphing into the other. https://wistia.com/blog/9-video-production-faux-pas-to-avoid , https://phantommoose.com/2008/06/12/lets-talk-transitions/ , https://tfwm.com/?p=7314
- **Legitimate uses:** passage of time, a dreamlike or inner state, slow reflective sequences. https://www.vegascreativesoftware.com/blog/transition-effects-for-videos/
- A graphic match can be paired with a dissolve. https://www.adobe.com/creativecloud/video/discover/match-cut.html
- A very short dissolve (a few frames) can soften a too-hard cut or hide a whip mismatch. https://nofilmschool.com/how-to-do-a-whip-pan

### Light leaks / film burns
- Seen by many editors as a fad that turns cheesy when overdone. Stock leaks are "easily recognised". https://dvinfo.net/forum/archive/index.php/t-524395.html , https://www.dvinfo.net/forum/archive/index.php/t-508780.html
- If used: subtle, short and motivated (a sunny summer festival, nostalgia), never as a default between every shot. https://www.motionelements.com/blog/articles/mastering-light-leaks-adding-cinematic-magic-to-your-videos , https://nofilmschool.com/2016/03/3-ways-illuminate-your-film-using-light-leaks-premiumbeat

### Masked / object-wipe transitions
- An object or person crosses and fills the frame, and its edge is masked to reveal the next shot. It needs a shot where something enters, fills and exits the frame, with frame-by-frame mask work. https://4kshooters.net/2020/06/05/easy-masking-transition-effect-in-premiere-pro-cc , https://www.premiumbeat.com/blog/create-moving-object-premiere-pro
- **[Inference]** It looks tasteful when the wiping object belongs in the story (a waiter passing in a restaurant film) and the move matches direction and speed into the next shot. It looks cheesy when repeated or when the mask edge chatters. Resolve: Magic Mask or Power Window tracking on the Color or Fusion page.

### Tasteful versus cheesy
- **Tasteful:**
  - Motivated by content: movement, shape or sound already in the footage.
  - Invisible, or meaningful.
  - Consistent within one film.
  - Paired with sound design.
  - Rare.
- **Cheesy:**
  - Preset 3D, spin, page-curl or heart transitions. https://www.dvinfo.net/forum/archive/index.php/t-524395.html
  - Transitions on every cut.
  - A different transition type each time.
  - Stock overlays everyone recognises.
- Synthesised from https://phantommoose.com/2008/06/12/lets-talk-transitions/ , https://wistia.com/blog/9-video-production-faux-pas-to-avoid , https://www.clueso.io/glossary/whip-pan **[Inference: synthesis]**

---

## 4. Dramatic tension and rhythm

### 4.1 Rhythm, the beat and music structure
- **Do not cut to every beat.** It makes the film feel like a music video. Save beat-synced cuts for one or two key moments. Edits a few frames before or after a musical change often feel more organic than landing exactly on it. https://www.premiumbeat.com/blog/how-to-edit-a-film-to-music-without-it-becoming-a-music-video
- Cutting slightly late gives breathing room; slightly early jolts, which suits action. https://eoshd.com/comments/topic/46696-editing **[forum, anecdotal]**
- "If you cut too slavishly to the beat... you are making the music composer the editor and director". https://creativecow.net/?p=1239950 **[forum]**
- Breaking the beat (a hold after a fast run, a delayed cut) creates emphasis and suspense. https://www.capcut.com/create/music-video-pacing-emotional-montage-rhythm
- Follow phrases, drops and energy changes rather than every beat. Dialogue and key action take priority over the musical grid. https://invideo.io/faq/can-ai-automatically-cut-a-video-to-the-beat-of-music/
- **Map the song first:** where it builds, where the main moment lands, where it resolves. A long ambient intro can be dead weight under a fast reel. Phrase gaps often make better cut points than the obvious downbeat. https://spliceapp.com/blog/what-editors-structure-videos-around-soundtracks , https://spliceapp.com/blog/what-video-editors-optimize-drop-timing-edits
- **Music mix:** duck under dialogue, do not leave it at one static "average" level, and swell over montages and bridges. https://www.premiumbeat.com/blog/how-to-edit-a-film-to-music-without-it-becoming-a-music-video
- **End music and picture together.** Edit the track to its natural ending instead of fading out. https://wistia.com/blog/9-video-production-faux-pas-to-avoid
- **[Inference] Agent procedure:**
  1. Mark song sections in Resolve (intro, build, drop or chorus, breakdown, outro) with timeline markers.
  2. Assign story acts to sections: setup to intro, rising to build, peak to drop, resolution or CTA to outro.
  3. Pre-select at most about 3–5 "hard sync" moments per minute (drop, accents) for on-beat cuts or hits.
  4. Elsewhere, let cuts fall on emotion and action, often in phrase gaps, with ±2–6 frame offsets.
  5. Edit the music (cut at bar lines, crossfade within a beat) so the song ends on the last frame.

### 4.2 Silence and breath
- Silence is a legitimate choice. Some great films have little or no music. https://www.premiumbeat.com/blog/how-to-edit-a-film-to-music-without-it-becoming-a-music-video
- Silence hits hardest after dense sound. Real silence is rare: use thinned-out room tone, not digital zero. https://www.krotos.studio/blog/the-power-of-silence-times-when-less-was-more-in-sound-design , https://designingsound.org/2014/06/28/designing-silence/
- Silence can put the viewer inside a character's head (Chion). https://soundgirls.org/silence-as-sound/
- Even with near-silence, faint sound keeps tension alive: one source quotes the *Alien* editor saying the cat-hunt footage was "boring" until faint Foley (rain, chains) was added. **[Uncertain which of these two pages carries the quote]** https://designingsound.org/2014/06/28/designing-silence/ , https://krotos.studio/blog/no-sound-in-sound-design
- **[Inference]** In brand films and testimonials, drop the music for 1–3 s just before or under the key line or result. The contrast makes it land. Keep each pause under about 1.5 s on social. https://www.socialync.io/blog/retention-techniques-keep-viewers-watching-2026

### 4.3 Sound design: room tone, ambience, layers
- **Room tone** fills gaps left by removed coughs, ums and breaths, smooths ambience jumps between takes, and must match the location and level. Record about 1 minute per setup. https://nofilmschool.com/what-is-room-tone , https://www.studiobinder.com/blog/what-is-room-tone , https://www.filmtvsound.com/index.php/sound-design/497-room-tone-vs-background-tracks
- Remove filler, breaths and lip smacks in interviews, and cover the cuts. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/
- **[Inference]** Remove distracting breaths, not all breaths. Fully breathless speech is a cloned-voice tell (https://www.opus.pro/blog/ai-slop-aesthetic-12-tells).
- **Murch, "Dense Clarity – Clear Density":** an audience can track only a limited number of simultaneous sound layers (reported as about 2.5 per sound family, or 5 in total, spread across the "spectrum" from music-like to speech-like). Beyond that it all goes "brown". https://designingsound.org/2009/10/15/walter-murch-special-womb-tone-and-dense-clarityclear-density/ , https://greg.org/archive/2006/06/28/walter-murchs-womb-tone-dense-clarity-clear-density.html **[Uncertain on exact numbers; original at Transom]**
- **[Inference] Rule:** at any moment, no more than about 5 meaningful layers: e.g. dialogue, music, ambience, one or two SFX.

### 4.4 Risers, whooshes, impacts
- A **whoosh** is a short (well under 1 s) sweep that bridges a fast cut. A **riser** is a longer build that must crest exactly on the hit, never early or late. Pair a riser with a faller. Atonal noise risers work in any key; tonal risers suit music landing on a chord. Generic whooshes make different moments feel the same, and muddy impacts clog reveals. https://morphic.com/ai-glossary/riser , https://www.ableton.com/en/blog/learn-how-to-make-high-impact-sounds-for-movies-and-trailers/
- **[Inference] Rules:**
  - SFX are only used where there is visible motion or a structural transition.
  - At most one riser-and-hit per act.
  - Whooshes sit 6–12 dB under dialogue level.
  - Vary samples, and never use the same whoosh twice in a row.
  - In corporate or testimonial pieces, prefer organic transition sounds (a door, a page, wind, the real location) over trailer SFX.

### 4.5 Sound bridges
- A **pre-lap** (the next scene's sound before its picture) is the J-cut principle. A **post-lap** carries sound over the change. Split edit is the umbrella term. Uses: soften cuts, build tension, establish location by ambience before we see it. https://filmdaft.com/what-is-a-sound-bridge-in-film-definition-and-transition-guide/ , https://filmlifestyle.com/what-is-prelap-in-film/
- Sound match cuts are the strongest variant. https://www.soundstripe.com/blogs/how-to-use-match-cuts-in-film-and-video-editing
- **[Inference] Agent rule:** every scene or location change gets a split edit of 6–24 frames (at 25 fps) unless a hard sound contrast (a smash cut) is the intent.

### 4.6 Tension devices summary [Inference: synthesis]
- **Build:** shorten shots progressively, add a riser, cross-cut, use J-cut anticipation, withhold the reveal ("don't reveal the peak", https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie).
- **Release:** a hit on the drop or a smash cut, then a longer hold, an L-cut, and room to breathe.
- **Contrast is the engine:** loud and quiet, fast and slow, wide and close. The *Two Towers* Helm's Deep example shows constant intensity numbs. https://www.krotos.studio/blog/the-power-of-silence-times-when-less-was-more-in-sound-design

---

## 5. Visual consistency, titles and safe areas

### 5.1 Frame rate
- **[Not from these sources; standard knowledge, verify]** Sweden is a 50 Hz / PAL-heritage region. A 25 fps timeline (or 50 fps for sport and slow-motion source) avoids flicker with mains lighting and matches European broadcast.
- 24 fps dropped into a 25 fps timeline looks worst. 30/60 fps on 25 fps is usually acceptable. For broadcast, convert everything to 25 fps first. https://community.adobe.com/questions-729/working-with-25fps-timeline-and-adding-videos-to-timeline-with-mixed-frame-rates-and-dimensions-1380992
- Dropping 30 to 25 fps causes jerky motion; 25 on a 30 fps timeline duplicates frames. Phone footage is often variable or non-integer (29.978…). Check the actual rate. https://forum.shotcut.org/t/30fps-to-25fps/15145
- In Resolve, Optical Flow / Speed Warp retiming of 23.98, 24, 29.97 and 30 fps clips into a 25 fps show gave artifact-free results for one practitioner. https://forum.blackmagicdesign.com/viewtopic.php?p=1141174 **[single user]**
- Frame-rate mismatch is harder to fix than colour mismatch, so pick stock at the project rate. https://soundstripe.com/blogs/make-stock-video-match-shot-video
- **[Inference]** Conforming 24 to 25 fps by speed-up is about 4% faster, and audio pitch shifts unless corrected. Prefer frame-rate conversion for B-roll and keep sync-sound clips at their native speed.

### 5.2 Colour, grain and texture across own footage, stock and AI clips
- **Correct before you grade:** normalise white balance, exposure and contrast with scopes (waveform, vectorscope), then apply one creative grade across all clips. Match to one hero reference frame. https://invideo.io/faq/how-do-you-use-color-grading-to-unify-inconsistent-ai/ **[vendor]**
- Pre-graded stock is harder to match: neutralise it first. Lower resolution rather than upscale. https://soundstripe.com/blogs/make-stock-video-match-shot-video
- **Grain:** apply a uniform grain layer over everything (Resolve Film Grain). This unifies sources. https://beverlyboy.com/film-technology/batch-grain-matching-stock-digital-plates-blend-seamlessly
- **AI clips** tend to be over-sharp and plasticky. One recommendation is a very light blur (0.3–0.6 px), then fine grain at low opacity (8–15%) **[vendor numbers]**. Keep denoise low when upscaling, to avoid waxy skin. Use one colour space (do not mix Rec.709 and HDR exports). https://invideo.io/faq/how-do-you-add-film-grain-blur-and-color-grading-to-ai/ , https://invideo.io/blog/ai-video-post-production-pipeline/
- Colour mismatch is the main reason AI shots look fake next to real footage. https://hackernoon.com/color-mismatch-is-why-your-ai-generated-video-looks-fake-next-to-real-footage
- **AI visual tells to check frame by frame:** flat diffuse lighting in every shot, over-saturated colours, floaty motion without micro-jitter, gibberish text on signs, hand morphs, reflection errors, background people with odd gait, repeating textures. https://www.opus.pro/blog/ai-slop-aesthetic-12-tells
- **[Inference] Rules for Viska:**
  - Match lighting direction and colour temperature across adjacent shots (also https://invideo.io/blog/ai-video-post-production-pipeline/).
  - Add subtle camera shake to AI or locked-off shots only where the surrounding footage is handheld.
  - Never let an AI clip carry identifiable text, hands in close-up, or a real place the client's audience knows. Viewers in Visita-type tourism will spot a fake Swedish landscape.
  - Label AI B-roll in the project log.
- Keep visuals consistent: similar colours, shapes, lines and textures, even when lighting varies. https://rainfocus.com/blog/15-points-of-a-great-recap-video/
- Grade naturally for hospitality and avoid "over-editing". https://spliceapp.com/blog/hotel-arrival-video-edits-for-travel-vlogs/

### 5.3 Titles, lower thirds and safe areas

**Lower thirds (Frame.io)**
- Clean sans-serif matching the brand guide. Strong contrast, using a background plate if needed. Do not cover mouth or face. Keep away from the frame edge and inside title-safe. Leave it on long enough to read every word twice. Animate only if it supports the story; keep it simple. Be consistent across the project. https://blog.frame.io/2017/12/04/create-lower-thirds-titles-that-dont-suck/
- **Duration:** about 3–5 s (HSE Ireland) versus BU's 1–3 s **[conflict]**. Do not stretch one lower third across several shots (Northeastern). Identify each person once, and skip it if they introduce themselves. Full first and last name; short titles; at most 3 lines. https://hse.ie/eng/about/who/communications/digital/video/branding-style-guidelines/lower-thirds , https://www.bu.edu/brand/files/2019/06/bu-video-branding-standards.pdf , https://brand.northeastern.edu/design-and-experiences/design/videography/
- **[Inference]** Apply Frame.io's "read twice" rule as the decider: about 0.25 s per word × 2, with a 2.5 s minimum.
- Proofread every name and title. https://rainfocus.com/blog/15-points-of-a-great-recap-video/
- Have the shoot capture each speaker's full name (spelled out) and title. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/

**16:9 safe areas (EBU R95)**
- Action-safe is 3.5% per side; graphics/title-safe is 5% per side. For 1920×1080 that is about 67/38 px (action) and 96/54 px (graphics). https://tech.ebu.ch/publications/r095 , https://tech.ebu.ch/docs/r/r095.pdf
- The older 5%/10% per-side convention is more conservative. https://en.wikipedia.org/wiki/Safe_area_(television)

**9:16 at 1080×1920** (platforms publish ad-placement numbers only; organic UI may differ, so verify on device):

| Platform | Top | Bottom | Left | Right | Source |
|---|---|---|---|---|---|
| Instagram Reels | 14% (about 269 px) | 35% (672 px) | 6% (about 65 px) | 6% (about 65 px) | Meta, per https://www.socialync.io/tools/safe-zones/instagram-reels |
| TikTok | 240 px | 660 px | 120 px | 120 px, plus a 180 px button column from y≈840 (measured) | https://www.socialync.io/tools/safe-zones |
| YouTube Shorts | 288 px | 672 px | 48 px | 192 px | Google, per https://www.socialync.io/tools/safe-zones/youtube-shorts |

- Other sources give smaller margins: First Pier gives 108/320/60/120 for Reels; Adkit measured a 381 px Shorts bottom. https://www.firstpier.com/resources/instagram-ad-safe-zones , https://adkit.so/tools/safe-zones/youtube **[Uncertain]**
- **[Inference] One universal 9:16 safe box for Viska:** x 120–888, y 288–1248. That is the most conservative combination of the three platforms. Put captions in the band about y 1000–1248, above the bottom UI, not at the very bottom. Keep faces in the upper-middle area.
- **Captions:** the hook must read on mute. Show key messages as on-screen text. https://segwise.ai/blog/anatomy-top-performing-video-ad-frame-by-frame

---

## 6. "AI slop / amateur" checklist with fixes

Each item: **signal**, then the **fix**, with sources. Items without a direct source are synthesis **[Inference]**, built on the cited principles.

**Editing and structure**
1. **Slow logo or intro before content.** Fix: open on the hook, product or payoff. Keep branding subtle until after the hook; logo at the end. https://ads.tiktok.com/business/library/Creative_Codes_ENG.pdf , https://adadvisor.ai/blog/meta-video-ad-script
2. **No single message; several themes competing.** Fix: one proposition per video; split or cut the rest. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/
3. **Peak revealed in the first seconds; flat arc.** Fix: tease without revealing, build, then pay off last. https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie
4. **One emotional tone or one tempo throughout.** Fix: change tone every ≤45 s and vary shot length. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/
5. **Template sameness** (identical hook pattern, caption style, pacing and voice across videos). Fix: design each piece from its own story; vary hook types and caption treatment per client brand. https://www.vozo.ai/blogs/youtube/youtube-ai-slop
6. **Cut on every beat, metronome rhythm.** Fix: sync only key moments; offset others by a few frames; follow phrases. https://www.premiumbeat.com/blog/how-to-edit-a-film-to-music-without-it-becoming-a-music-video
7. **Too long.** Fix: trim ruthlessly; leave them wanting more. https://www.canon.ca/en/Pro-Inspiration/Five-steps-for-producing-engaging-event-recap-videos , https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie

**Cuts and transitions**

8. **Default cross-dissolves or preset transitions on many cuts.** Fix: hard cuts. Keep dissolves for time passing or reflection only, and make every non-cut motivated. https://wistia.com/blog/9-video-production-faux-pas-to-avoid
9. **Mixed transition styles, stock light leaks, digital whip pans between static shots.** Fix: one transition grammar per film, in-camera motion only, at most 1–2 stylised transitions per minute **[Inference]**. https://www.dvinfo.net/forum/archive/index.php/t-508780.html
10. **Visible jump cuts in a brand film or testimonial; mid-blink cuts.** Fix: cover with B-roll, a punch-in or Smooth Cut; cut just before the blink. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/ , https://www.provideocoalition.com/aotc-murch-bcpc/
11. **All straight cuts with audio and picture changing together everywhere** (a "slideshow" feel). Fix: J and L cuts at scene changes, with sound bridges. https://vimeo.com/blog/post/guide-to-film-cuts , https://borisfx.com/blog/l-and-j-cuts-smoother-more-cinematic/
12. **Static shots only.** Fix: favour shots with motion; add subtle push-ins; cut on action. https://robinpiree.com/blog/how-to-make-the-perfect-music-festival-after-movie , https://en.wikipedia.org/wiki/Cutting_on_action

**Content and B-roll**

13. **Generic stock or AI B-roll that does not connect to what is being said.** Fix: B-roll must show the specific client, place and people, or illustrate, parallel or foreshadow. Use stock only for abstract points. https://artlist.io/blog/what-is-ai-slop-and-why-it-matters-for-video-creators/ , https://nofilmschool.com/2015/11/how-cut-short-documentary-films-part-two-building-story-adding-b-roll
14. **Inauthentic or overproduced employer or testimonial content; scripted non-actors.** Fix: "Is this us?"; keep real moments; use questions, not scripts. https://www.ere.net/8-tips-for-creating-stellar-employer-branding-videos , https://wistia.com/blog/9-video-production-faux-pas-to-avoid
15. **Frankenbites, or reordering that changes meaning.** Fix: never change meaning; log reorders for client approval. https://blog.frame.io/2018/12/03/remain-sane-cutting-mundane/ , https://yorkspace.library.yorku.ca/xmlui/handle/10315/38136

**AI visuals**

16. **AI artefacts:** morphing hands, gibberish signage, odd gait, tiling textures, flat lighting, oversaturation, floaty camera. Fix: reject the clip or crop around the artefact; avoid AI for hands, text and known places; grade down saturation; add grain and slight shake. https://www.opus.pro/blog/ai-slop-aesthetic-12-tells , https://invideo.io/faq/how-do-you-add-film-grain-blur-and-color-grading-to-ai/
17. **Mismatched colour, sharpness or grain between sources.** Fix: correct with scopes, match to a hero frame, apply one grade and one grain layer. https://hackernoon.com/color-mismatch-is-why-your-ai-generated-video-looks-fake-next-to-real-footage , https://soundstripe.com/blogs/make-stock-video-match-shot-video
18. **Frame-rate judder** (24p stock in a 25p timeline, VFR phone clips). Fix: conform on import, using optical flow where needed. https://community.adobe.com/questions-729/working-with-25fps-timeline-and-adding-videos-to-timeline-with-mixed-frame-rates-and-dimensions-1380992

**Audio**

19. **TTS voice:** monotone "plateau", no breaths, mouth not closing on b/p for avatars. Fix: a human voice-over, or heavy TTS direction (pauses, emphasis); keep natural breaths; no lip-sync avatars in client work **[Inference]**. https://www.opus.pro/blog/ai-slop-aesthetic-12-tells
20. **Wall-to-wall music at one static level, buried dialogue, music faded out at the end.** Fix: duck under speech, shape levels, allow silence, end music with picture. https://www.premiumbeat.com/blog/how-to-edit-a-film-to-music-without-it-becoming-a-music-video , https://wistia.com/blog/9-video-production-faux-pas-to-avoid
21. **Dead-silent gaps or ambience jumps at dialogue edits.** Fix: room tone under every edit. https://nofilmschool.com/what-is-room-tone
22. **Whoosh on every cut, the same SFX repeated, risers that do not crest on the hit.** Fix: SFX only on motivated transitions; vary them; align the crest to the frame. https://morphic.com/ai-glossary/riser
23. **Too many simultaneous sound layers (mud).** Fix: at most about 5 layers; remove one to add one. https://designingsound.org/2009/10/15/walter-murch-special-womb-tone-and-dense-clarityclear-density/

**Graphics and text**

24. **Random fonts and colours, poor contrast, lower thirds over faces, crowding the edges, overanimated text.** Fix: brand font, plate, title-safe, simple motion, consistent. https://blog.frame.io/2017/12/04/create-lower-thirds-titles-that-dont-suck/
25. **Text or faces under the platform UI in 9:16; just a centre crop of 16:9.** Fix: universal safe box (section 5.3); re-edit for vertical. https://www.socialync.io/tools/safe-zones
26. **Typos or misspelled names.** Fix: a proofreading pass against the client's name list. https://rainfocus.com/blog/15-points-of-a-great-recap-video/
27. **No sound-off readability, or no CTA.** Fix: captions and on-screen key messages; a CTA card at the end. https://segwise.ai/blog/anatomy-top-performing-video-ad-frame-by-frame , https://ads.tiktok.com/business/en-CA/blog/creative-best-practices-top-performing-ads

---

## 7. Machine-checkable rules for Viska (proposal, [Inference] unless cited)

These turn the above into checks an agent can run on a Resolve timeline export (EDL, FCPXML or the Resolve API):

1. **Transition audit:** count non-cut transitions per minute; flag if more than 2. Flag any cross-dissolve shorter than 8 frames that is not marked "soften", and any longer than 1 s that is not marked "time passage". Flag more than one transition type family per film, beyond cut, dissolve and dip. (Section 3.)
2. **Shot-length profile:** compute ASL per act. Flag if the coefficient of variation is under about 0.3 (monotone rhythm). Flag a peak act that is not faster than the setup act. Flag if the final 10% of the film has a shorter ASL than the climax and no hold shot.
3. **Beat-sync ratio:** the share of cuts within ±1 frame of detected beats. Flag above about 50% (music-video feel; PremiumBeat), unless the format is an aftermovie peak or a reel montage.
4. **Interview hygiene:** every interview edit point either has B-roll covering it, a punch-in of 20% or more, or a Smooth Cut of 4 frames or less. No cut lands mid-blink (detect eye closure on the frame). Room tone is continuous under the dialogue tracks.
5. **Split edits:** at least 50% of scene or location changes use J or L cuts.
6. **Audio:** dialogue at about −14 to −16 LUFS integrated for social and web delivery **[Inference; check platform norms]**. Music ducked when speech is present. Music ends within 1 frame of picture end, or on a designed button. At most 5 concurrent active audio layers.
7. **Graphics:** all text inside EBU 5% graphics-safe (16:9) or the universal 9:16 safe box (section 5.3). Lower-third duration at least "read twice" and at least 2.5 s. Each person named once. Spell-check names against the brief.
8. **Opening:** the first frame is not a logo; the value proposition or hook is visible within 3 s on 9:16 and within 6 s at most (TikTok guidance). The first frame communicates without sound.
9. **Consistency:** a single timeline frame rate (25 fps default for Swedish clients). All clips conformed. One grade node tree with a shared grain layer. AI clips flagged in metadata and checked against the AI-tell list (section 6, item 16).
10. **Ethics:** no frankenbites. Any reordered interview statement goes on the approval list for the client and speaker.

---

## 8. Further sources worth reading in full (not fully digested here)
- Walter Murch, *In the Blink of an Eye* (Silman-James, 2nd ed. 2001). Primary source for the Rule of Six and the blink theory.
- Murch, "Dense Clarity – Clear Density" (Transom.org companion). Original wording of the layer limits. https://designingsound.org/2009/10/15/walter-murch-special-womb-tone-and-dense-clarityclear-density/
- Blackmagic Design, free *Editor's Guide to DaVinci Resolve 20* (lessons on cutting interviews, drama, documentary and music videos) and the Fairlight audio guide. https://www.redsharknews.com/blackmagic-davinci-resolve-20-training-guides , https://www.digitalcameraworld.com/photography/video-editing/blackmagic-releases-free-davinci-resolve-20-training-books (download from blackmagicdesign.com/products/davinciresolve/training; I did not verify the direct URL).
- Every Frame a Painting: "How Does an Editor Think and Feel?" and "Edgar Wright – How to Do Visual Comedy" (matching scene transitions, sound-synchronised action). https://en.wikipedia.org/wiki/Every_Frame_a_Painting , https://www.moviemaker.com/edgar-wright-visual-comedy-video/
- Cutting et al. 2011, "Quicker, faster, darker". https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/
- EBU R95 safe areas. https://tech.ebu.ch/publications/r095
- Meta ads guide, Instagram Reels specs (cited via Socialync): facebook.com/business/ads-guide/update/video/instagram-reels
- TikTok Creative Codes. https://ads.tiktok.com/business/library/Creative_Codes_ENG.pdf
- Manfred Becker, *Creating Reality in Factual Television: The Frankenbite and Other Fakes* (Routledge 2020). https://routledge.com/Creating-Reality-in-Factual-Television-The-Frankenbite-and-Other-Fakes/Becker/p/book/9780367481100

## 9. Known gaps
- No authoritative ASL benchmarks for corporate, testimonial or social formats. The numbers in section 1.4 and section 2 are inferred.
- Platform 9:16 safe zones are published for ads only and change with UI updates. Verify on a device before each campaign.
- Several per-format length recommendations come from vendor blogs with commercial interests.
- I did not read the Blackmagic Editor's Guide itself. Resolve-specific procedures (Smooth Cut, Optical Flow, Speed Warp, Magic Mask) are drawn from tutorials and forum posts.
- No Swedish-language or Nordic-specific craft sources were consulted.
