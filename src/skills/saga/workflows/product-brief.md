---
skill: product-brief
agent: saga
output_folder: "{output_folder}/A-Product-Brief"
---

# Product Brief Workflow

Produces the Product Brief document suite through structured discovery conversation.

---

<workflow id="product-brief">

  <constraints>
    - One question at a time. Always wait for the answer before continuing.
    - Never present a list of questions. Never run a form.
    - If the user has existing materials: invoke material-analyzer before discovery.
    - Discovery data is collected in memory throughout — Brief Writer generates all documents at the end.
    - Update design log at each checkpoint.
  </constraints>

  <!-- ═══════════════════════════════════════════
       INIT
  ═══════════════════════════════════════════ -->

  <step id="init">
    Load:
    - `{project-root}/_bmad/wds/config.yaml` — resolve project_name, output_folder, user_name, communication_language, document_output_language
    - `_progress/00-design-log.md` — check Current for in-progress work
    - `_progress/wds-project-outline.yaml` — check existing_materials flag

    IF Current table has a product-brief task:
      → jump to the step recorded in Current
    ELSE IF existing_materials.has_materials is true OR user provides documents:
      → go to <step id="material-analysis">
    ELSE:
      → go to <step id="discovery">
  </step>

  <!-- ═══════════════════════════════════════════
       MATERIAL ANALYSIS (optional path)
  ═══════════════════════════════════════════ -->

  <step id="material-analysis">
    <subagent ref="agents/material-analyzer.md">
      <input>All documents provided by user or referenced in existing_materials</input>
      <output>
        - Confirmed topics: what is already clearly established
        - Gap topics: what needs conversation
        - Extracted data: structured per discovery category
      </output>
    </subagent>

    Present findings briefly:
    "I've reviewed your materials. I have solid data on [confirmed topics]. I still need to explore [gap topics] with you."

    Mark confirmed topics as pre-filled in discovery data.
    → go to <step id="discovery"> (skip confirmed topics, use Confirmation Mode for them)
  </step>

  <!-- ═══════════════════════════════════════════
       DISCOVERY
       9 categories — one conversational thread each
       Confirmed topics → Confirmation Mode (quick verify)
       Gap topics → full discovery conversation
  ═══════════════════════════════════════════ -->

  <step id="discovery">
    Load `references/discovery-conversation.md` before starting.

    Run each category in sequence. For each:
    - Confirmed: state what was found, ask "anything to add or correct?"
    - Gap: open with a single question, listen, reflect, deepen, confirm, document

    <category id="vision">
      Goal: Why does this exist? Purpose, impact, aspiration.
      Opening: "Tell me — why does this product exist? What change does it create in the world?"
      Synthesize: mission statement, vision statement, core purpose
    </category>

    <category id="positioning">
      Goal: Who is it for, what makes it different, what are the alternatives.
      Opening: "Who is this really for — and why would they choose this over what they're doing today?"
      Synthesize: target market, differentiation, competitive positioning
    </category>

    <category id="business-model">
      Goal: How it makes money. B2B vs B2C. Pricing approach.
      Opening: "How does the business make money from this?"
      Synthesize: revenue model, pricing approach, B2B/B2C/hybrid classification
    </category>

    <category id="business-customers">
      Goal: Decision-makers, buyer vs end-user distinction (B2B only).
      Condition: only if business-model is B2B or has enterprise component
      Opening: "Who signs the contract or makes the purchasing decision — and how are they different from the people who use it day-to-day?"
      Synthesize: buyer profile, user profile, procurement path
    </category>

    <category id="target-users">
      Goal: Behavioral profiles, pain points, current workarounds.
      Opening: "Walk me through a typical user. What are they trying to get done, and what gets in their way today?"
      Synthesize: 2-3 user behavioral profiles (not demographics — behaviors and motivations)
    </category>

    <category id="product-concept">
      Goal: The core structural idea. What kind of product is this.
      Opening: "If you had to describe what kind of product this is in one sentence — not what it does, but what it *is* — what would you say?"
      Synthesize: product type, founding concept, core structural principle
    </category>

    <category id="success-criteria">
      Goal: Measurable outcomes, KPIs, timeline.
      Opening: "What does success look like 12 months after launch? What numbers change?"
      Synthesize: primary KPIs, secondary indicators, launch timeline
    </category>

    <category id="competitive-landscape">
      Goal: Real alternatives users have today. Differentiators. Unfair advantage.
      Opening: "What do people use instead of this — not just direct competitors, but any alternative including doing nothing?"
      Synthesize: competitor map, key differentiators, unfair advantage if any
    </category>

    <category id="constraints">
      Goal: Technical, budget, timeline, regulatory parameters.
      Opening: "What are the hard walls — things we absolutely cannot do, or must do, regardless of what would otherwise be ideal?"
      Synthesize: technical constraints, budget range, timeline, regulatory/compliance requirements
    </category>

    → go to <step id="suite-check">
  </step>

  <!-- ═══════════════════════════════════════════
       SUITE CHECK
       Determine which extension documents to produce
  ═══════════════════════════════════════════ -->

  <step id="suite-check">
    Based on what came up in discovery, determine extensions needed:

    <signal check="content-language">
      Triggered by: brand voice, tone, language, SEO keywords, content strategy, multiple languages, copywriting
    </signal>

    <signal check="visual-direction">
      Triggered by: design style, brand aesthetics, visual references, logo, colors, typography, imagery
    </signal>

    IF content-language triggered:
      → run <step id="content-language-discovery"> before writing
    IF visual-direction triggered:
      → run <step id="visual-direction-discovery"> before writing
    ELSE:
      → go to <step id="generate">
  </step>

  <!-- ═══════════════════════════════════════════
       CONTENT & LANGUAGE EXTENSION (optional)
  ═══════════════════════════════════════════ -->

  <step id="content-language-discovery">
    Load `references/content-structure-principles.md` and `references/seo-strategy-guide.md`.

    <category id="brand-personality">
      Goal: How the brand should feel — personality attributes, what it is and is not.
      Opening: "If the brand were a person at a dinner party, how would you describe them?"
    </category>

    <category id="tone-of-voice">
      Goal: How the brand speaks — formal/informal, warm/authoritative, direct/exploratory.
      Load `references/strategic-documentation.md`
      Opening: "Give me an example of a brand that speaks the way you want to speak — and tell me what you like about it."
    </category>

    <category id="language-strategy">
      Goal: Primary language, secondary languages, localization approach.
      Opening: "What languages does the product need to support — and are all markets equal, or is one the primary market?"
    </category>

    <category id="seo-keywords">
      Goal: Core keyword themes, priority topics, search intent.
      Opening: "What would someone type into Google when they're looking for something like this — before they know your brand name?"
    </category>

    <category id="content-structure">
      Goal: How content is organized — navigation logic, content hierarchy, page types.
      Opening: "What are the main content areas of the product or site? What does a user need to find?"
    </category>

    → go to <step id="generate">
  </step>

  <!-- ═══════════════════════════════════════════
       VISUAL DIRECTION EXTENSION (optional)
  ═══════════════════════════════════════════ -->

  <step id="visual-direction-discovery">
    Load `references/inspiration-analysis.md`.

    <category id="visual-references">
      Goal: Concrete visual references — sites, brands, images the user responds to.
      Opening: "Show me or name something that looks the way you want this to feel — doesn't have to be in your industry."
    </category>

    <category id="design-style">
      Goal: Overall aesthetic direction — minimal, bold, editorial, warm, technical, etc.
      Synthesize: style keywords, reference analysis
    </category>

    <category id="color-direction">
      Goal: Color personality — not exact palette, but emotional direction.
      Opening: "What colors feel right for this — and just as importantly, what feels wrong?"
    </category>

    <category id="typography-direction">
      Goal: Type personality — serif/sans, editorial/functional, expressive/neutral.
      Opening: "What does the typography need to say about the brand — and are there fonts you already love or hate?"
    </category>

    <category id="imagery-style">
      Goal: Photo/illustration style, visual metaphors, what to avoid.
      Opening: "What kind of imagery do you imagine — photography, illustration, abstract? What's the mood?"
    </category>

    → go to <step id="generate">
  </step>

  <!-- ═══════════════════════════════════════════
       GENERATE
  ═══════════════════════════════════════════ -->

  <step id="generate">
    Confirm with user before generating:
    "I have everything I need. Ready to write the Product Brief?"

    Wait for confirmation.

    <subagent ref="agents/brief-writer.md">
      <input>All discovery data collected across categories</input>
      <output>
        - `{output_folder}/A-Product-Brief/product-brief.md` (always)
        - `{output_folder}/A-Product-Brief/content-language.md` (if content-language triggered)
        - `{output_folder}/A-Product-Brief/visual-direction.md` (if visual-direction triggered)
      </output>
    </subagent>

    → go to <step id="review">
  </step>

  <!-- ═══════════════════════════════════════════
       REVIEW & CLOSE
  ═══════════════════════════════════════════ -->

  <step id="review">
    Present what was written:
    "Product Brief suite written:
    ✓ product-brief.md
    [✓ content-language.md — if written]
    [✓ visual-direction.md — if written]

    Read through it and let me know if anything needs adjusting."

    Wait for feedback. If adjustments needed: update the relevant document, re-confirm.

    Update `_progress/00-design-log.md`:
    - Move current task to Log
    - Set Current to empty or next task
    - Mark Product Brief as complete in phase status

    Print:
    "Product Brief complete. Ready for Trigger Map when you are — just say /TM."
  </step>

</workflow>
