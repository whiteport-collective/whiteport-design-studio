# Research C: AI-generated video in client productions (for Viska)

Research date: **2026-10-25**. Web research only. Every claim has a source, and each fact is dated where the source gives a date. This market changes week to week, so check prices and model lists again before quoting them to a client.

**Reliability legend**
- **[1st]** = vendor's own documentation or a legal primary source.
- **[2nd]** = law-firm, press or reputable secondary source.
- **[3rd]** = aggregator, SEO or vendor-competitor blog. Treat as an indication only.
- **UNVERIFIED** = I could not confirm it against a primary source.

---

## 0. Key takeaways (TL;DR)

1. **Higgsfield is an aggregator with its own tools on top.** It is a web studio plus a separate pay-per-second developer API (launched 2026-09-16) that resells about 50 third-party models (Seedance, Kling, Wan, MiniMax, Veo, Grok, LTX, PixVerse) and adds its own layers (Cinema Studio camera control, Soul and Soul ID characters, DoP, upscaler).
   - You own the output and may use it commercially.
   - **IP indemnity and a no-training guarantee come only on Enterprise.**
   - The company carries reputational baggage from 2026 controversies.
2. **Sora is gone.** OpenAI shut the app on 2026-04-26 and the API on 2026-09-24. Do not plan around it.
3. **Google:** Veo 3.1 preview models in the Gemini API were shut down on 2026-10-22, and Google now pushes **Gemini Omni Flash**. GA Veo 3.1 lives on in the **Gemini Enterprise Agent Platform** (the former Vertex AI): 24 fps, up to 4K, C2PA support. Google lists Veo among its **indemnified** services (April 2026 archive).
4. **Runway is now also an aggregator.** Its API sells Gen-4.5, Aleph 2.0, Kling, Veo, Seedance, Wan, MiniMax, Grok, Magnific upscaling, SDR-to-HDR and more, priced per second.
5. **Adobe Firefly Video** is still the "commercially safe" option, but indemnity requires an enterprise entitlement and excludes partner models and beta features. Its native video model looks technically behind (1080p, about 5 s clips, per 2025 data).
6. **EU AI Act Article 50 has applied since 2026-08-02. It was not delayed by the Digital Omnibus.**
   - A "deep fake" is AI content that resembles existing **persons, objects, places, entities or events** and would falsely appear authentic. The Commission's July 2026 Guidelines explicitly count *AI marketing that makes products look different from reality* as a deepfake.
   - For a tourism client, a realistic AI shot of a real place must be labelled.
   - Advertising rarely qualifies for the lighter "artistic" regime.
7. **Craft rule of thumb.** AI works for people-free establishing shots, abstract metaphors, impossible camera moves, stylised product beauty shots and transitions. It fails on faces and hands, text and logos, physics, multi-person action and anything that has to be truthful (testimonial, documentary, real staff, real locations).
   - Use **image-to-video from your own approved stills** to keep the look consistent.
   - Grade the clip to match a hero shot, add shared grain, conform the frame rate, and log provenance.

---

## 1. Higgsfield

### 1.1 What it is
- An AI video and image platform that aggregates third-party models alongside its own engine. Bloomberg and Variety (2026-10-23) describe a hub tapping about 35 third-party video models, with Nvidia and TCV joining a Series B extension. Per the same coverage, the August 2026 Series B was led by DST Global and raised USD 400M at a USD 5.4B valuation. [2nd]
  - https://www.bloomberg.com/news/articles/2026-10-23/nvidia-tcv-invest-in-ai-video-startup-higgsfield-in-series-b-extension
  - https://variety.com/2026/digital/news/nvidia-tcv-invest-generative-ai-startup-higgsfield-1236929624/
  - https://www.tipranks.com/news/nvidia-and-tcv-back-ai-video-startup-higgsfield-as-users-top-40-million
- Model counts vary by source ("15+", "20+", "35", "50+ via API"), so treat the count as fluid.

### 1.2 Models available (as of Oct 2026)
- **Higgsfield's own roundup (credit costs "as of October 20, 2026") [1st, marketing]** lists:
  - Seedance 2.5 (up to 30 s, joint audio, up to 50 references, Region Edit)
  - Veo 3.1 / Veo 3.1 Lite (1080p, 4–8 s, native audio)
  - WAN 3.0 (1080p, up to 30 s)
  - Kling 3.0 (4K, up to 15 s, audio)
  - MiniMax Hailuo 2.3 (1080p)
  - Cinema Studio 4.0 (its own; 1080p, up to 30 s)
  - HappyHorse (1080p, 3–15 s)
  - Grok Imagine 1.5 (1080p, 1–15 s, lip-sync)
  - Gemini Omni Flash 1.1 (4K, 3–10 s)
  - FLUX.3 Video (4K, up to 20 s)
  - The same page states that Sora 2 is retired and not offered. Seedance 2.5 requires Plus or higher.
  - https://higgsfield.ai/blog/5-Best-AI-Video-Models-2026-Tested-Compared
- **Changelog highlights [1st]** (https://higgsfield.ai/creator-hub/changelog):
  - 2026-10-22: Content Factory (topic to finished clip, 15 s–5 min)
  - 2026-10-21: **Kling 4.0** (3–30 s, up to 10 keyframes and 15 references, 720p/1080p on Higgsfield)
  - 2026-10-19: Genjutsu Lite; 3D Angles (re-shoot a photo or video from new camera angles)
  - 2026-10-15: FLUX 3 Video Upscaler update
  - 2026-10-06: Nano Banana 2.1 (images, 4K, 14 references); Ad Multiplier
  - 2026-10-02: AI Influencer
  - 2026-09-30: Genjutsu Restyle (restyle a video while keeping its motion and camera)
  - 2026-09-22: Seedance 2.5 **Draft Mode** (cheap 480p preview, then a 1080p render)
  - 2026-09-16: **Higgsfield API**
  - 2026-09-04: 3D Jutsu
  - 2026-09-01: Genjutsu (swap objects, locations, products or characters in a video)
  - 2026-08-27: **FLUX 3 Video Upscaler** (1080p, 2K or 4K; Precise or Creative)
  - 2026-08-21: **Blender plugin**
  - 2026-08-11: **Cinema Studio 4.0** (up to 30 s, up to 50 references, 30+ camera-movement presets, forward and backward extend)
  - 2026-08-03: Seedance 2.5
- **Kling 4.0 specs elsewhere:** Kuaishou launched it around 2026-10-15. Bernama reports up to 30 s, up to 4K with stereo sound, and 10-bit HDR "pending". [2nd] Its own API was "coming soon" according to fal.ai and Muapi. [3rd]
  - https://www.bernama.com/tv/news.php?id=2622573
  - https://fal.ai/learn/tools/what-is-kling-4-0

### 1.3 Features relevant to Viska
- **Camera control:** Cinema Studio offers presets plus virtual lens, focal length and movement settings. A Higgsfield FAQ claims Cinema Studio camera control works across models (Seedance, Veo 3.1, Kling 3.0, WAN). [1st, marketing; specific lens and body list UNVERIFIED]
  - https://geo.higgsfield.ai/task/blog/what-is-higgsfield-ai-complete-guide-cinematic-creative-studio
- **Character consistency:** Soul ID builds a reusable "digital double" from 20+ photos. A "Reference Anchor" workflow approves a hero still first, then animates it. [1st, marketing]
  - https://higgsfield.ai/blog/best-ai-video-consistent-characters
  - https://workingnotworking.com/higgsfield-ai-cinema-studio-marketing-platform/
  - Do **not** use Soul ID on real people without written consent (see §4).
- **Image-to-video, keyframes and references** are available on most hosted models (Seedance 2.5 up to 50 references; Kling 4.0 up to 10 keyframes).
- **Upscaling:** FLUX 3 Video Upscaler goes to 2K or 4K (changelog above).
- **Video editing (v2v):** Genjutsu, Genjutsu Restyle and Seedance Region Edit.

### 1.4 API (programmatic use), Help Center page published 2026-09-16, modified 2026-09-24 [1st]
Source: https://higgsfield.ai/creator-hub/help-center/integrations/what-is-the-higgsfield-api

- **Endpoints:**
  - Base URL: `https://api.higgsfield.ai`
  - Console: `https://open.higgsfield.ai`
  - Docs: `https://docs.higgsfield.ai/docs`
  - SDKs: Python and TypeScript, or plain REST.
- **Request flow:** Requests are asynchronous (request ID, then polling or a webhook). A **cost-estimate endpoint** returns the price before you run a request.
- **Billing:**
  - USD prepaid balance. Minimum top-up $5. Funds expire after one year.
  - Video is billed **per second of output**, images per image.
  - Failed generations are refunded.
- **Limits and storage:**
  - Each key gets 20 concurrent requests.
  - **Outputs are kept for at least 7 days and may then be deleted**, so download them immediately.
- **Catalogue:**
  - Video families: Seedance, Kling, Wan, MiniMax, PixVerse, LTX, Grok.
  - Own models: Soul 2, Soul Cinema, DoP, Marketing Studio Image.
  - The API catalogue **differs from the web lineup.** Veo is not listed for the API on this page.
- **Credits:** Plan credits and "Unlimited" access do **not** apply to the API. **MCP and CLI** connect to the web account and spend plan credits; the API uses its own balance.
- **Observed costs** from a MindStudio test (2026-09-18) [3rd]: about $0.60 for a Kling 3.0 clip, about $1.10 for MiniMax, about $3.23 for Seedance 2.5 with audio, and $0.20–1.60 for video-only clips.
  - https://www.mindstudio.ai/blog/higgsfield-api-pricing-pay-per-use/

### 1.5 Web plans and credits
- Sources disagree.
  - Most 2026 guides list Free (no credits); Starter $19 / 270 credits; Plus $47 per month billed annually or $59 monthly / 1,200 credits; Ultra $99 per month billed annually or $129 monthly / 3,000 credits. [3rd]
    - https://creatify.ai/blog/higgsfield-pricing-(2026)-plans-and-what-you-ll-actually-pay
    - https://www.krea.ai/blog/higgsfield-pricing-explained-2026-unlimited-credits-and-real-monthly-costs
  - An older Higgsfield-hosted page (2026-04-21) shows $15 / $39 / $99.
  - The pricing page itself (https://higgsfield.ai/pricing) renders client-side and could not be read. **UNVERIFIED. Check it live.**
- Subscription credits do not roll over. Packs and auto-refill credits reportedly expire after 90 days. [3rd]
- For Viska, the **API (pay per second, cost estimate first) is the right integration.** Web plans only make sense for manual exploration.

### 1.6 Terms: ownership, commercial use, training (Terms revised 2026-07-25, effective 2026-08-27) [1st]
Sources:
- https://higgsfield.ai/creator-hub/help-center/account-and-privacy/who-owns-my-generations-and-can-i-use-them-commercially (published 2026-08-02, modified 2026-09-12)
- https://higgsfield.ai/blog/terms-of-use-privacy-policy-update

Ownership and commercial use:
- Higgsfield claims no ownership of inputs or outputs (ToU §4.2 and §4.4).
- There is **no restriction on commercial use**, including ads and client work, and no credit to Higgsfield is required.
- Commercial rights are not tied to a plan, but **free plans watermark outputs.** Paid plans give watermark-free downloads.

Enterprise-only protections. Both of these matter for client work:
- **Legal IP indemnification.**
- **Exclusion of customer content from model training.**
- On all other plans Higgsfield **may train on your content** (§4.4). Deleting content stops future use, but content already trained into a model cannot be removed.
- **Consequence:** do not upload unreleased client product images, staff photos or confidential stills on a non-Enterprise account without the client's consent.

Prohibitions:
- You may not use outputs to train other AI models (§5.1(iii), §5.2(iv)).
- You must ensure no infringement of copyright, trademark or **likeness** (§5.1(ii)(b)).
- You may **not upload images of another person without their permission** (§5.3).
- The help page is silent on the pass-through terms of third-party models. **Open question:** whether Seedance or Kling licence terms impose extra limits when used through Higgsfield. Ask Higgsfield in writing.

### 1.7 Max resolution, frame rate and length
- Resolution and length depend on the model:
  - Natively up to 4K (Kling 3.0/4.0, Gemini Omni Flash 1.1, FLUX.3 Video). Most other models top out at 1080p.
  - Up to 30 s per generation (Seedance 2.5, WAN 3.0, Kling 4.0, Cinema Studio 4.0).
  - Longer pieces come from extend or multi-shot features. OpenAI's customer story claims Higgsfield went "from 1 minute to over 10" minutes using OpenAI models. [1st OpenAI, could not open it (403); summary via search]
    - https://openai.com/index/higgsfield-longer-videos-voice/
- **Frame rate is not stated** in the Higgsfield sources. Check the metadata of each downloaded file. Many models output 24 fps, but this is UNVERIFIED per model.

### 1.8 Reputation risk (2026)
- Controversies reported in 2026:
  - Marketing that boasted about replacing creative jobs (The Register, 2026-02-06)
  - Racist and sexist promotional material, which the co-founder admitted came from "failures in internal processes"
  - Billing and "unlimited" complaints (about $1.35M refunded)
  - Allegations of celebrity deepfake promos (unproven)
  - Undisclosed creator promotions in August 2026
- Sources:
  - https://www.theregister.com/2026/02/06/higgsfield_ai_job_loss/
  - https://timesca.com/kazakh-startup-higgsfield-ai-from-unicorn-to-racism-and-sexism-scandal/
  - https://gritdaily.com/kazakh-startup-higgsfield-criticism/
- **Implication:** Higgsfield is fine as a back-end tool. Avoid naming it in client-facing credits unless the client is comfortable with it, and prefer Enterprise terms for serious client work.

---

## 2. The other leading generators (status 2026-10-25)

| Generator | Current model(s) | Strengths | API and price indication | Commercial terms and indemnity | Output |
|---|---|---|---|---|---|
| **Google Veo / Omni** | Veo 3.1 (GA `veo-3.1-generate-001`, released 2025-11-17); Veo 3.1 Fast; Veo 3.1 Lite (preview); **Gemini Omni Flash / 1.1** (2026-07 / 2026-08) | Outdoor, atmospheric and light/weather realism; native audio; reference images; first/last frame; extend | Gemini API: Veo 3.1 preview **shut down 2026-10-22**, migrate to Omni Flash or GA Veo on the Gemini Enterprise Agent Platform. Indicative rates: Veo 3.1 about $0.40/s at 720p/1080p and $0.60/s at 4K; Fast $0.10–0.30/s; Omni Flash 1.1 about $0.03–0.30/s [3rd] | Veo is on Google Cloud's **Generative AI Indemnified Services** list (archive 2026-04-22). Indemnity typically covers GA, not preview, models [UNVERIFIED detail]. C2PA Content Credentials supported | **24 fps**, 720p/1080p/4K (4K on Standard only), 16:9 or 9:16, 4/6/8 s per clip, up to 4 outputs per prompt. **Region on model page: us-central1 only**, which matters for EU data handling |
| **OpenAI Sora** | **Discontinued** | – | App and web closed 2026-04-26; API closed 2026-09-24; no successor named | – | – |
| **Runway** | Gen-4.5 (2026-02-10), **Aleph 2.0** (v2v editing, 2026-06-02), Gen-4 Turbo, Act-Two, plus resold Kling 3.0/O3, Veo 3.1, Seedance 2.x, WAN 3.0, MiniMax H3, Grok, Omni Flash, Magnific upscaler, Ruby SDR-to-HDR, frame-rate enhance | Editing existing footage with Aleph; a broad one-key catalogue | Official per-second rates: Gen-4.5 $0.12/s; Aleph 2.0 $0.28/s; Gen-4 Turbo $0.05/s; Kling 3.0 4K $0.43/s; Magnific Video Upscaler from $0.007/frame | Commercial use allowed on paid tiers. Enterprise Terms (updated 2026-06-01) put responsibility for outputs on the customer. **Indemnity not confirmed.** Consumer tiers reportedly allow training on inputs and outputs | Varies by model |
| **Kling (Kuaishou)** | Kling 3.0 / O3 (on APIs), **Kling 4.0** (2026-10-15) | Character-driven multi-shot; 4K; long 30 s takes; up to 10 keyframes and 15 references | Kling 3.0 on Runway from $0.09–0.43/s; Kling 4.0 API "coming soon" [3rd] | Terms updated 2026-04-21. Free tier non-commercial and watermarked; paid tiers commercial. Broad licence back to Kling on inputs and outputs. **No indemnity found** | Up to 4K; 3–30 s |
| **Luma Ray** | **Ray3.2** (June 2026) | **Native 16-bit HDR and EXR export in ACES2065-1**, aimed at Resolve and Nuke compositing; Modify Video v2 (v2v, up to 20 s); up to 16 keyframes | Python and TS SDK; Build (usage-based) and Scale (SLA) tiers; about $1.20 per 5 s at 1080p SDR [3rd]; HDR costs more; Ray3.2 rates "may change before GA" | Paid plans (Plus and up) allow commercial use and remove the watermark; free tier non-commercial. Indemnity not stated | 1080p max via API; HDR and EXR |
| **Pika** | Pika 2.5 | Stylised, social short-form | "API Club" $10/mo gateway to 70+ models (launched Aug 2026) [2nd press] | Commercial use and no watermark only on Pro and Fancy [3rd] | – |
| **MiniMax Hailuo** | **H3 / Hailuo 3.0** (2026-07-31), H3 Max | Strong text-to-video and image-to-video rankings on LMArena; 2K; references | Runway resells it from $0.05–0.10/s | Reported open weights under a community licence [3rd, UNVERIFIED] | Up to 2K (2560×1440), 24 fps, up to 15 s (extendable to about 30 s) [3rd] |
| **Seedance (ByteDance)** | **Seedance 2.5** (around 2026-07/08), 2.0, Fast, Mini | Multi-shot narrative, up to 50 references, region edit, draft mode | BytePlus ModelArk is token-billed (about $10.70 per million tokens; reference only); Runway from $0.20/s; regions are ap-southeast-1 (some models also eu-west-1) | **IP risk flag:** in Feb 2026 Disney, Paramount, WBD, Netflix, Sony and the MPA sent cease-and-desist letters over Seedance 2.0 outputs of protected characters and likenesses. ByteDance pledged stronger safeguards | 480p–1080p (some sources say 4K), up to 30 s |
| **Adobe Firefly Video** | Firefly Video Model (GA at MAX London 2025) plus partner models in the Firefly app (Veo, Kling, Runway and others) | Positioned as "commercially safe" (trained on licensed and public-domain content); Premiere **Generative Extend** | Generative credits; enterprise contracts | **IP indemnity only with the right enterprise entitlement** (a new contracting event); **partner-model outputs and beta features are carved out** of the indemnity | 1080p, about 5 s clips, 16:9 / 9:16 / 1:1 (2025 data; a 4K model was announced "coming soon", status UNVERIFIED). Adobe MAX 2026 is 10–12 Nov 2026 in Miami Beach, so new announcements are likely |

### Sources for §2

**Google**
- Gemini API video page: Omni Flash; Veo 3.1 preview shutdown 2026-10-22 [1st]. https://ai.google.dev/gemini-api/docs/video
- Vertex / Agent Platform Veo 3.1 model page: GA, 24 fps, resolutions, C2PA, us-central1 [1st]. https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-1-generate
- Indemnified services (archived 2026-04-22) [1st]. https://cloud.google.com/archive/terms/generative-ai-indemnified-services-20260422
  - The page contents were truncated in my fetch. Search snippets show Veo listed under the "Gemini Enterprise Agent Platform API (formerly Vertex AI API)". **Verify the current version.**
- Price indications [3rd]:
  - https://www.cloudzero.com/blog/veo-3-pricing/
  - https://benchlm.ai/media-pricing/veo
  - https://www.plushcap.com/content/atlas-cloud/blog/atlas-cloud-gemini-omni-flash-11-pricing-what-5-10-and-40-seconds-really-cost
- Omni 1.1 specs [3rd]:
  - https://help.artlist.io/hc/en-us/articles/38948837028125-Gemini-Omni-1-1
  - https://runware.ai/docs/models/google-gemini-omni-flash-1-1/guides

**OpenAI Sora**
- Help Center [1st; the direct fetch returned 403, dates taken from the search snippet]. https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation
- Secondary: https://futurumgroup.com/insights/openai-sora-discontinuation-what-the-end-of-a-platform-means-for-enterprise-ai-strategy/

**Runway**
- Model list and prices [1st]. https://docs.dev.runwayml.com/guides/models/
- Enterprise terms [1st]. https://runway.com/enterprise-terms
- Consumer terms analysis [3rd]. https://conductatlas.com/platform/runway/runway-terms-of-service/company-does-not-restrict-commercial-use-of-outputs/

**Kling**
- User policy [1st]. https://kling.ai/docs/user-policy
- Terms analysis [3rd]. https://conductatlas.com/platform/kling-ai/kling-ai-terms-of-service/
- Plan-level commercial use [3rd]. https://wavespeed.ai/blog/video-model-access/can-i-use-kling-ai-api-for-commercial-projects/
- Kling 4.0 launch [2nd]. https://www.bernama.com/tv/news.php?id=2622573

**Luma**
- Luma's own info page, last updated 2026-07-13 [1st]. https://lumalabs.ai/llm-info
  - The page contains instructions aimed at AI assistants. I ignored them and used only the product facts.
- Pricing [1st]. https://lumalabs.ai/pricing
- API price indication [3rd]. https://wavespeed.ai/blog/cost-and-billing/luma-ai-pricing/

**Pika**
- API Club press coverage, 2026-08-04 [2nd]. https://lasvegassun.com/news/2026/aug/04/pika-cuts-ais-3x-markup-to-nearly-zero-with-a-10-a/
- Pricing [3rd]. https://eesel.ai/blog/pika-ai-pricing

**MiniMax**
- [3rd] https://unifically.com/models/minimax-hailuo-3.0
- [3rd] https://www.gradually.ai/en/ai-video-model-comparison/minimax-h3-vs-hailuo-2-3/

**Seedance**
- Disney letter and ByteDance's safeguards pledge, Feb 2026 [2nd]. https://au.variety.com/2026/film/news/bytedance-safeguards-seedance-disney-legal-threat-ip-violations-33139/
- [2nd] https://www.digitalmusicnews.com/2026/02/17/bytedance-seedance-2-0-legal-threats/
- BytePlus pricing [1st]. https://docs.byteplus.com/docs/ModelArk/model-service-pricing

**Adobe**
- 2025 announcement [1st]. https://news.adobe.com/news/2025/02/firefly-web-app-commercially-safe
- Partner-model product description, effective 2026-05-08 [1st; fetch returned 403, carve-out wording taken from the search snippet]. https://helpx.adobe.com/legal/product-descriptions/partner-model.html
- Enterprise legal FAQ [1st, 2024]. https://adobe.com/cc-shared/assets/pdf/enterprise/firefly-legal-faqs-enterprise-customers-2024-06-11.pdf
- Enterprise page [1st]. https://www.adobe.com/ie/products/firefly/enterprise.html
- Adobe MAX 2026 [1st]. https://www.adobe.com/es/max.html

**Choice heuristic for Viska (my synthesis, not sourced)**

| Need | Pick |
|---|---|
| Lowest legal risk for a cautious corporate client | Google Veo GA via the Agent Platform (indemnified, C2PA). Alternatively native Firefly Video under an Adobe enterprise contract |
| HDR or VFX-grade plates for Resolve | Luma Ray3.2 (EXR, ACES) |
| Editing or restyling real footage | Runway Aleph 2.0, or Higgsfield Genjutsu |
| Long multi-shot sequences with many references | Seedance 2.5 or Kling 4.0, via the Higgsfield or Runway API (mind the IP flag on Seedance) |
| Broad experimentation behind one key | Higgsfield API or Runway API |

---

## 3. Craft: AI shots inside real productions

### 3.1 What works and what fails
Practitioner consensus, mostly from vendor and creator blogs, so read it as guidance rather than proof.

**Works:**
- People-free **establishing shots** and environments
- **Abstract or metaphor visuals** (data, growth, connection)
- Product close-ups and **hero shots without people**
- Stylised motion graphics
- Impossible or expensive camera moves (macro fly-throughs, orbit, crane, drone-like pull-backs)
- Transitions and match cuts
- Sources:
  - https://www.aifire.co/p/generate-professional-ai-b-roll-footage-2026-blueprint
  - https://marketsplash.com/best-ai-video-generators/
  - https://www.opus.pro/blog/best-ai-b-roll-generators-short-form-video

**Fails, or needs heavy review:**
- Multiple people interacting, and two-person direction (models ignore it)
- Faces and hands over time
- Legible **text, signage and logos** (they garble; add real logos and text in Resolve or Fusion instead)
- **Physics** (liquids, cloth, collisions)
- **Consistency across shots** (product shape and location drift)
- **Real, recognisable places** (they will be wrong, and they trigger AI Act deepfake labelling, see §4)
- Anything that "looks generated", which undermines credibility
- Sources: same as above, plus https://hackernoon.com/color-mismatch-is-why-your-ai-generated-video-looks-fake-next-to-real-footage

**Brand and IP:**
- Never prompt with third-party trademarks or protected characters. The Seedance cease-and-desist letters (Feb 2026) show the risk.
- CMS (2026-05-28) recommends internal rules banning others' trademarks and protected works in prompts, plus human review before publishing. https://cms.law/en/swe/legal-updates/ai-in-advertising-key-aspects-for-advertisers-in-sweden

### 3.2 Image-to-video from your own stills (the main consistency lever)
- **Two-stage workflow:**
  1. Generate or choose a still (ideally a frame grab or photo from the real shoot, or a brand-approved image).
  2. Animate it.
- Runway treats the image as the first frame, so the prompt should describe **motion only, not the image again.** Restating the image reduces motion.
- Phrase prompts positively ("static camera" rather than "no camera movement").
- Sources:
  - https://help.runwayml.com/hc/en-us/articles/39789879462419 [1st]
  - https://www.atlabs.ai/blog/how-to-prompt-with-runway-gen-4-image-to-video-a-comprehensive-guide [3rd]
  - https://runware.ai/docs/models/runway-gen-4-5/guides/directing-motion [3rd]
- **First and last frame:** Veo 3.1 supports it, and so do MiniMax H3 Max and Kling 2.5. Use it for **transitions between two real shots.**
- **References:** Veo asset images; Seedance up to 50; Kling up to 15. Use them to lock product, wardrobe and palette.
- **Legal caveat on uploads:**
  - Do not upload photos of real people without consent (Higgsfield ToU §5.3; Swedish name and image law, §4.4).
  - Do not upload confidential client material to tiers that train on inputs.

### 3.3 Prompting camera language
- **Structure:** subject and action → setting → **camera (shot size, angle, movement, lens)** → lighting and atmosphere → style → technical details. Explicitly state camera movement, otherwise models default to static or a simple pan.
- **Vocabulary that works:**
  - Moves: dolly in/out, truck, pedestal, crane up, orbit, tracking shot, push-in, whip pan, rack focus, dolly zoom, Dutch angle
  - Lens: "35 mm", "85 mm shallow depth of field", "macro"
  - Light: golden hour, overcast soft light, practicals
- Sources [3rd]:
  - https://www.leonardo.ai/news/mastering-prompts-for-veo-3
  - https://dhl.veed.io/learn/veo-3-1-prompts
  - https://eastondev.com/blog/en/posts/ai/20251204-veo3-camera-control/
- With Higgsfield Cinema Studio, use its camera and lens presets instead of free text where possible, for more predictable results.

### 3.4 Matching AI clips to real footage in DaVinci Resolve Studio
- **Resolution:**
  - Generate at the highest native resolution affordable: 1080p minimum; 4K on Veo Standard, Kling 3.0/4.0 4K or Omni 1.1.
  - Otherwise **upscale before grading**, because upscaling changes texture and shifts the grade.
  - Upscaler options:
    - Topaz (subscription only since late 2025; Starlight models; Astra for creative upscaling) [3rd]
    - FLUX 3 Video Upscaler on Higgsfield
    - Magnific Video Upscaler on the Runway API
    - Resolve Studio's Super Scale (established Resolve Studio feature, not re-verified for v21)
  - Sources:
    - https://www.myarchitectai.com/blog/topaz-ai-pricing
    - https://www.capterra.com/p/10043466/Topaz-Video/
- **Frame rate:**
  - Veo outputs **24 fps** [1st]. MiniMax H3 is reported at 24 fps [3rd]. Others vary, so check each file.
  - For a 25p Swedish timeline, a silent B-roll clip can be conformed 24→25 (a 4% speed-up), or retimed with Optical Flow or Speed Warp.
  - Runway also sells "Enhance Frame Rate" ($0.01 per 2 s) [1st].
  - (Conform advice is standard post practice, not from a cited source.)
- **Colour:**
  - AI clips have **no log curve or camera metadata**, and each generation renders warm or cool differently.
  - Correct every AI clip to a **hero reference shot on the scopes** (black point, white balance), then apply the creative grade. Apply LUTs last.
  - For HDR or ACES pipelines, Luma Ray3.2 EXR output in ACES2065-1 avoids SDR clipping.
  - Source: https://hackernoon.com/color-mismatch-is-why-your-ai-generated-video-looks-fake-next-to-real-footage
- **Texture:**
  - AI output tends to be **over-sharp and "plasticky".** Soften slightly, **never add sharpening**, then add **one shared grain layer** across AI and real footage to unify them. [3rd]
  - Add motion blur where AI motion is too crisp. Resolve 21 adds AI Motion Deblur and UltraSharpen; use them in the other direction for the real footage only as needed.
  - Sources:
    - https://invideo.io/faq/how-do-you-add-film-grain-blur-and-color-grading-to-ai/
    - https://www.cgchannel.com/2026/06/blackmagic-design-releases-davinci-resolve-21-0/
- **Resolve 21 (stable, June 2026) and 21.1** [2nd]:
  - New AI tools: IntelliSearch (find clips by object or person), CineFocus, Motion Deblur, UltraSharpen, Face Age Transformer, Speech Generator, and Magic Mask "Render in Place".
  - 21.1 reportedly adds "AI assistant integration" (detail UNVERIFIED; the Phoronix page returned 403). This is potentially relevant for Viska's agent control of Resolve.
  - Sources:
    - https://www.cgchannel.com/2026/06/blackmagic-design-releases-davinci-resolve-21-0/
    - https://phoronix.com/news/DaVinci-Resolve-21.1
- **C2PA in Resolve:** I found **no evidence** that Resolve reads or writes C2PA Content Credentials. **UNVERIFIED.** Assume metadata from generators is stripped on export, and keep provenance in our own log (§5).

---

## 4. Ethics and law for client work (EU and Sweden)

### 4.1 EU AI Act Article 50: transparency
- **Dates:**
  - Article 50 has applied since **2 August 2026**.
  - The Digital Omnibus (Regulation (EU) 2026/1744, in force 2026-07-27) postponed high-risk obligations (Annex III to 2027-12-02; Annex I to 2028-08-02) but **did not postpone Article 50.**
  - Only Art. 50(2) machine-readable marking gets a grace period: until **2 December 2026**, for generative systems placed on the market before 2026-08-02.
  - Watermark-detection interoperability is due by 2027-02-02.
  - Sources:
    - https://www.morganlewis.com/blogs/sourcingatmorganlewis/2026/08/eu-ai-acts-transparency-rules-what-went-into-effect-on-2-august (2026-08-12) [2nd]
    - https://www.joneswalker.com/en/insights/blogs/ai-law-blog/yes-august-2-still-matters-the-eu-approved-a-high-risk-ai-delay-but-most-trans.html [2nd]
    - https://www.faegredrinker.com/en/insights/publications/2026/7/eu-ai-act-commission-confirms-transparency-code-of-practice-as-adequate-and-publishes-final-version-of-its-guidelines-on-transparency-obligations (2026-07-30) [2nd]
- **Who must do what:**
  - **Providers** (Google, Runway, Higgsfield and so on) must mark outputs in machine-readable form (Art. 50(2)).
  - **Deployers** (Whiteport and the client, as professional users) must **disclose deepfakes** (Art. 50(4)).
  - The disclosure must be clear and distinguishable, given **at the latest at the first exposure**, and accessible (Art. 50(5)).
  - Source: https://artificialintelligenceact.eu/article/50/ [1st text]
- **Definition (Art. 3(60)):** a deep fake is AI-generated or manipulated image, audio or video content that resembles existing **persons, objects, places, entities or events** and would falsely appear authentic or truthful.
  - Source: https://artificialintelligenceact.eu/article/3/
  - **So a realistic AI shot of a real tourist destination, or of a real product shown differently from reality, is in scope. A clearly fictional or abstract visual is not.**
- **Commission Guidelines on Article 50 (final, 2026-07-20) and Code of Practice on marking and labelling (final 2026-06-10, judged adequate):**
  - Deepfake status is assessed case by case against what the audience expects.
  - **AI marketing that makes products look different from reality, digital replicas of real people, and de-aging all count as deepfakes.**
  - Advertising *can* be "creative", but most advertising examples **do not** qualify for the reduced "evidently artistic" regime.
  - A **visible label at first exposure** is required. The Commission's standard **EU icon** satisfies it, and metadata alone is not enough.
  - Posting on the open internet can trigger the duty.
  - Content generated before 2026-08-02 does not need retroactive labels.
  - The informative character prevails in mixed content.
  - Fines go up to €15M or 3% of global turnover.
  - Sources:
    - Faegre Drinker (above)
    - https://www.stephensonharwood.com/post/102nfqh/eu-ai-act-update-european-commission-adopts-guidelines-on-article-50-transparency-obligations/ (2026-08-03) [2nd]
    - https://digital-strategy.ec.europa.eu/en/news/commission-publishes-code-practice-marking-and-labelling-ai-generated-content [1st]
    - https://www.jonesday.com/en/insights/2026/06/european-commission-publishes-final-code-of-practice-on-marking-and-labelling-aigenerated-content [2nd]
- **Practical reading for Viska (synthesis, not legal advice):**
  - **Must label:** realistic AI imagery of real places, real people, real products shown unrealistically, or invented "real-looking" events.
  - **Probably no label needed:** clearly abstract, animated or fantastical visuals, and minor assistive edits such as cleanup, upscaling or colour.
  - When unsure, label: the EU icon or an "AI-generated footage" super, plus an end-card note.
  - Contracts should state who (agency or client) applies the label (Stephenson Harwood recommends contract review).
- **AI literacy (Art. 4)** has applied since 2025-02-02. Staff using these tools need adequate training (CMS, above).

### 4.2 Platform labels
- **YouTube** [1st]: https://support.google.com/youtube/answer/14328491
  - Creators must disclose realistic altered or synthetic content: real people doing things they didn't, **altered footage of real events or places**, realistic scenes that never happened, and AI music as the main focus.
  - Not required: unrealistic or animated content, colour, effects, upscaling, and AI help with scripts or thumbnails.
  - YouTube **auto-labels content carrying C2PA**, and creators cannot remove that label.
  - Disclosure does not reduce reach or monetization.
- **Meta (Facebook and Instagram)** [3rd, verify in Meta's Transparency Center]:
  - The "AI info" label is applied automatically for Meta's own generative ad tools and when **C2PA or IPTC metadata** indicates AI. Otherwise the advertiser uses a manual disclosure control.
  - Undisclosed photorealistic AI people or political content risks rejection.
  - Sources:
    - https://www.cinerads.com/blog/ai-ad-disclosure-requirements
    - https://coinis.com/blog/meta-ai-content-labeling-facebook-instagram-ads-2026
- **TikTok** [1st newsroom]:
  - The AIGC label is required for fully generated or significantly edited realistic content.
  - TikTok reads C2PA and adds **invisible watermarks** to AI content made with its own tools and to uploads carrying C2PA. It reports more than 1.3B videos labelled.
  - Ad-specific visible-label rules come from secondary sources only.
  - Sources:
    - https://newsroom.tiktok.com/more-ways-to-spot-shape-and-understand-ai-content?lang=en (2025-11-19)
    - https://newsroom.tiktok.com/tiktok-ssa-shares-more-ways-to-spot-shape-and-understand-ai-generated-content?lang=en-ZA (2026-03-10)
- **LinkedIn** [1st]: https://www.linkedin.com/help/linkedin/answer/a6282984
  - Shows a **C2PA "CR" icon** on images and video with Content Credentials. Clicking it shows whether AI was used, the app or device, the issuer and the date.
  - LinkedIn admits it cannot label all AI content.
  - Background: https://fortune.com/2024/11/26/linkedin-content-credentials-labeling-challenges-c2pa

### 4.3 C2PA Content Credentials
- C2PA is a signed, tamper-evident record of origin and edits. It proves the declared history is intact, **not that the content is true.** The manifest can be embedded in the file or kept as a sidecar.
  - https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html [1st]
  - Deployment guidance (2026-07): https://c2pa.org/wp-content/uploads/sites/33/2026/07/Content-Credentials-Deployment-Guidance.pdf
- Veo on the Agent Platform supports C2PA [1st, model page above]. Google has a content-credentials page: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/content-credentials
- **Problem:** NLE re-encoding usually strips generator credentials, and Resolve support for C2PA is unconfirmed. Platforms auto-label C2PA content (YouTube, Meta, LinkedIn, TikTok).
- **Choose deliberately:**
  - **Either** keep provenance and accept the platform labels. This is honest and AI Act-aligned.
  - **Or** apply our own visible label and keep the provenance log internally.
  - Never strip credentials *to hide* AI use from content that requires a label.

### 4.4 Sweden: likeness, marketing law, copyright
- **Name and image in advertising (Lag (1978:800) om namn och bild i reklam)** [1st]: https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/lag-1978800-om-namn-och-bild-i-reklam_sfs-1978-800/
  - §1: using a person's name, **image** or another clear reference to them in marketing **without consent** is prohibited.
  - §2: fines for intentional or grossly negligent breaches.
  - §3: reasonable compensation plus damages.
  - §4: materials can be ordered destroyed.
  - An AI likeness that is clearly recognisable as a real person very likely counts as such a "clear reference". This is my reading; no AI-specific case law was found. **Consent per campaign:** consent for one campaign may not cover the next.
    - https://lawline.se/answers/2218 [3rd]
- **Marketing Practices Act (2008:486):**
  - Marketing must be true and not misleading (s. 10), and the agency and the client are liable alike (s. 23).
  - Reklamombudsmannen, matter 2503-36 (2025-08-13): **"AI is not an excuse"** for misleading content.
  - Patent and Market Court, PMT 13029-25 (2026-04-01): AI chatbot answers count as marketing.
  - An AI shot that misrepresents a hotel, a destination or a product is therefore a marketing-law risk as well as an AI Act issue.
  - Source: CMS (2026-05-28, updated 2026-08-11), https://cms.law/en/swe/legal-updates/ai-in-advertising-key-aspects-for-advertisers-in-sweden [2nd]
- **Denmark (neighbour, a trend signal):** a copyright-based right over one's own face and voice against realistic digital imitations has been re-introduced, with a target date of 2027-01-01. It is **not in force** as of October 2026.
  - https://eprs.europarl.europa.eu/contents/publications/EPRS/2026/01/EPRS_ATA(2026)782611.html
  - https://intellectual-property-helpdesk.ec.europa.eu/news-events/news/denmarks-proposed-copyright-rules-deepfakes-2026-06-01_en
- **Copyright in AI output:**
  - **EU and Sweden:** protection requires human creative input ("the author's own intellectual creation", CJEU originality standard; Swedish Copyright Act 1 kap. 1 §).
    - The **Prague Municipal Court (2024)** denied copyright to a text-to-image output and treated the prompt as at most a "theme".
    - No CJEU ruling on AI output was found as of October 2026.
    - Sources:
      - https://www.twobirds.com/en/insights/2024/czech-republic/czech-court-denies-copyright-protection-of-ai-generated-work-in-first-ever-ruling
      - https://lup.lub.lu.se/student-papers/search/publication/9218678 (student thesis, low weight)
  - **US:** the Supreme Court denied cert in *Thaler v. Perlmutter* (2026-03-02), so the human-authorship requirement stands. The Copyright Office (Jan 2025) says prompts alone are insufficient.
    - https://www.mayerbrown.com/en/insights/publications/2026/03/supreme-court-denies-review-in-ai-authorship-case
  - **Practical consequence:**
    - Raw AI shots are probably **not protected**, so competitors could reuse them. The edit, grade, composite and overall film, as human creative work, are protected.
    - Don't promise clients "exclusive copyright" in AI clips. Promise contractual rights to the deliverable instead.
    - Vendors "assigning ownership" (Higgsfield, Runway, Kling) cannot create copyright where the law does not grant it.

### 4.5 When NOT to use AI
- **Testimonials, documentary, case studies, "behind the scenes", news-like content:** use real footage only. The informative character prevails under the AI Act Guidelines, and marketing law requires truth.
- **Real staff and real customers:** no synthetic doubles, de-aging or voice clones without explicit written, campaign-specific consent (Lag 1978:800, Higgsfield §5.3, the AI Act deepfake definition). Even with consent, a label is needed.
- **Tourism clients' real locations:** don't generate "the" Visby, Kiruna or the client's hotel. Use real footage or licensed stock. Use AI only for clearly non-specific, stylised or metaphorical inserts (weather, light, abstract textures), or label clearly.
- **Product truth:** never show product features, sizes, results or colours that differ from reality. The Guidelines name this explicitly as a deepfake, and it is also misleading marketing.
- **Third-party IP:** no logos, characters, artists' styles by name, or real celebrities.
- **Industry benchmark:** Netflix's generative AI guidance for partners (Aug 2025) says outputs must not replicate copyrighted works or unowned likenesses, tools must not train on production data, and AI material stays out of final deliverables without approval. Talent likeness needs consent and written approval. [2nd]
  - https://www.cined.com/netflix-publishes-generative-ai-guidelines-for-content-production/
  - https://ymcinema.com/2025/08/27/netflix-generative-ai-guidelines-filmmakers/

### 4.6 What to put in client agreements (synthesis)
1. **AI-use disclosure and approval:** list planned AI shots per production. The client approves each AI shot in the offline edit.
2. **Allocation of AI Act duties:** state who applies the Art. 50(4) labels, in which channels, and in what form (EU icon, super, description text), and who keeps the records.
3. **Tool list and terms:**
   - Name the generators used.
   - Commit to **enterprise or no-training tiers** for client-confidential inputs, or get the client's consent to standard tiers.
   - Note where data is processed (for example Veo in us-central1; BytePlus in ap-southeast-1).
4. **IP warranties scaled to reality:**
   - Warrant the human-made parts and the licensed stock.
   - For AI shots, warrant only "generated with [tool] under its commercial terms; no third-party marks or likenesses prompted".
   - Pass through any vendor indemnity (Google Veo GA, Adobe enterprise Firefly). Cap liability.
   - State that copyright in raw AI output may not exist.
5. **Likeness:** written, campaign-specific and time-limited consent for any real person used as a reference, with withdrawal and takedown terms.
6. **Provenance deliverable:** the client receives a provenance log (§5) and, if wanted, C2PA-signed masters.
7. **Truth clause:** no AI depiction of real products, places or people that misrepresents reality, with client sign-off on factual accuracy.
8. **Retention:** generator outputs on Higgsfield's API are deleted after about 7 days, so the agency archives the masters and logs.

---

## 5. Recommended agent workflow for Viska

```
1. DECIDE NEED
2. CHOOSE GENERATOR
3. PROMPT FROM CONTEXT
4. GENERATE VARIANTS
5. REVIEW
6. GRADE TO MATCH
7. LABEL AND LOG PROVENANCE
```

**1. Decide need (gate)**
- Answer these questions:
  - What does the shot have to communicate (from the script or storyboard and the trigger map)?
  - Can real footage or licensed stock do it as well? If yes, use that.
  - Is the shot **truth-bearing** (testimonial, documentary, real staff, real place, product feature)? If yes, **stop: no AI.**
  - Does it depict a real person, place, object or event realistically? If yes, mark it **"label required"** and get client approval.
- Output: a shot card with purpose, duration, framing, mood, AI-allowed (yes/no), label-required (yes/no) and the client approval status.

**2. Choose generator (rules table)**

| Requirement | Generator |
|---|---|
| Low legal risk, indemnity wanted | Veo 3.1 GA (Agent Platform) or Firefly enterprise |
| HDR or EXR plate | Luma Ray3.2 |
| Restyle or edit real footage | Runway Aleph 2.0 or Higgsfield Genjutsu |
| Long multi-shot, many references | Kling 4.0 or Seedance 2.5 (avoid IP-adjacent prompts) |
| Cheap ideation | Seedance 2.5 Draft (480p), Veo Lite, Omni Flash 360p/720p, Grok Lite |
| Default single-key access | Higgsfield API (cost-estimate endpoint first) or Runway API |

- Re-check the model list monthly. Sora's exit and the Veo preview shutdown show how fast models disappear.

**3. Prompt from brand and trigger-map context**
- Inputs: brand palette, light and mood words, approved reference stills (preferably frames from the actual shoot), the shot card, and the camera grammar of the surrounding real shots (lens, height, movement speed).
- Template: `[subject + action], [setting], [shot size / angle], [camera move + speed], [lens], [lighting/time], [palette/style], [texture: natural film grain, slight motion blur], [duration], [aspect]`.
- For image-to-video, describe motion only.
- Banned-terms filter: brand names, logos, celebrity and artist names, real place names (unless the shot is approved and labelled).

**4. Generate variants**
- Run 3–6 variants per shot at draft resolution or with fast models. Record the seed where the API exposes one.
- Use first/last-frame mode for transitions between real shots.
- Re-render only the selected variant at full resolution. Download immediately (Higgsfield keeps files at least 7 days only).

**5. Review (human in the loop)**
- Automated checks: frame-by-frame scan for faces and hands, text and logos, physics glitches, flicker, and drift from the reference.
- Human checks: brand fit, truthfulness, likeness or IP resemblance, and "does it look generated next to the real shots?"
- The client approves AI shots explicitly.

**6. Grade to match (Resolve Studio)**
- Order: conform the frame rate (to 25p or 24p) → upscale (Super Scale, Topaz, FLUX or Magnific) → soften the over-sharpness → match black point and white balance to the hero shot on scopes → creative grade → shared grain and halation across AI and real footage → add motion blur if needed → final LUT.
- Composite real logos and text in Fusion instead of generating them.

**7. Label and log provenance**
- Apply labels per the shot card (EU icon or super, platform AI toggles).
- Write one provenance record per AI clip. Store it with the project and export it to the client.

```yaml
clip_id: VSK-2026-031-AI-004
project: <client/production>
purpose: establishing / metaphor / transition
generator: higgsfield-api | runway-api | vertex-veo
model: veo-3.1-generate-001        # exact model id + version
endpoint_or_plan: API pay-per-second | Enterprise
date_generated: 2026-10-25T14:03Z
prompt: "<full text>"
negative_or_settings: {resolution: 1080p, fps: 24, duration_s: 6, aspect: 16:9, audio: off}
seed: 123456 | n/a
reference_inputs: [still_017.png (own photo, client-approved), ...]
variants_generated: 4
selected_variant: 2
cost_usd: 2.40
license_terms: "Higgsfield ToU 2026-08-27 §4.4 commercial OK; no indemnity (non-Enterprise)"
indemnified: false
c2pa_present_in_source: true | false | unknown
post_processing: [conform 24->25, Topaz upscale 4K, grade, grain]
real_person_or_place_depicted: none | <name + consent ref>
ai_act_label_required: true | false
label_applied: "EU AI icon + 'AI-generated footage' super, 2 s"
reviewer: <name>, approved_by_client: <name/date>
```

---

## 6. Open questions and uncertainties
- **Higgsfield:** the live pricing page could not be read. The pass-through of upstream model licences (Seedance, Kling) is undocumented. The frame rate of each model's output is not published. Enterprise pricing is unknown.
- **Google:** the full current indemnified-services list could not be read (truncated). Whether Gemini Omni Flash is indemnified is unknown. EU-region availability of Veo is apparently us-central1 only, which should be verified for GDPR.
- **Adobe:** current 2026 specs of the native Firefly Video model, and the exact list of partner models that are indemnified (a forum claim says some Google and OpenAI models are covered; unverified). New announcements are likely at MAX on 10–12 Nov 2026.
- **Kling 4.0 API:** not confirmed live. **Seedance 2.5:** the official ByteDance spec page was not found; the specs come from aggregators.
- **Resolve 21.1:** the "AI assistant integration" details are unverified (page blocked). C2PA support in Resolve is unverified.
- **Legal:** this is research, not legal advice. Have a Swedish IP or marketing lawyer review the agreement template (§4.6) and the labelling policy before first use.
