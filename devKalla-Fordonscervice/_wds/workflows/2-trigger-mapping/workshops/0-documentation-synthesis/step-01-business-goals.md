# Documentation Synthesis - Step 1: Business Goals

<critical>Frame as validation: "Your material suggests X, is this correct?"</critical>
<critical>Fill gaps through conversation if documentation incomplete</critical>

<step>

<action>Analyze documentation for vision and objectives</action>

<check if="clear_vision_found">
  <output>**Vision Statement**
  
Your documentation suggests this vision:

> {{extracted_vision}}

Is this the aspirational goal you're working toward?</output>

  <ask>Does this capture your vision, or should we refine it?</ask>
  
  <action>Refine based on feedback</action>
  <template-output>vision_statement</template-output>
</check>

<check if="vague_vision_found">
  <output>**Vision Statement**
  
I found some aspirational language in your documentation. It seems like your vision is:

> {{interpreted_vision}}

But this isn't explicitly stated. Is this accurate?</output>

  <ask>Should we use this, or define a clearer vision statement?</ask>
  
  <action>Refine or create vision statement</action>
  <template-output>vision_statement</template-output>
</check>

<check if="no_vision_found">
  <output>**Vision Statement**
  
I don't see an explicit vision statement in your documentation. However, based on your objectives and plans, the **implied vision** seems to be:

> {{inferred_vision}}

This is reverse-engineered from what you're trying to achieve.</output>

  <ask>Does this capture your aspirational goal? Or should we define it differently?</ask>
  
  <action>Create vision statement through conversation</action>
  <template-output>vision_statement</template-output>
</check>

<output>---

**Strategic Objectives**</output>

<check if="smart_objectives_found">
  <output>Your documentation includes these measurable objectives:

{{#each extracted_objectives}}
**Objective {{@index + 1}}:** {{this.statement}}
- Metric: {{this.metric}}
- Target: {{this.target}}
- Timeline: {{this.timeline}}
{{/each}}

These look SMART (Specific, Measurable, Achievable, Relevant, Time-bound).</output>

  <ask>Are these the right strategic objectives? Any adjustments?</ask>
  
  <template-output>objectives</template-output>
</check>

<check if="vague_goals_found">
  <output>Your documentation mentions these goals:

{{#each extracted_goals}}
- "{{this.original}}"
{{/each}}

These aren't fully SMART yet. Let me help sharpen them:

{{#each extracted_goals}}
**From documentation:** "{{this.original}}"
**Suggested SMART version:** {{this.smart_version}}
{{/each}}</output>

  <ask>Do these SMART versions capture what you need to measure?</ask>
  
  <action>Refine objectives based on feedback</action>
  <template-output>objectives</template-output>
</check>

<check if="no_objectives_found">
  <output>I don't see measurable objectives in your documentation. 

Based on your vision and plans, what would indicate you're succeeding?</output>

  <ask>What metrics would prove you're achieving your vision?

Think about:
- User metrics (adoption, engagement, retention)
- Business metrics (revenue, growth, market share)
- Quality metrics (satisfaction, referrals, reviews)</ask>
  
  <action>Create objectives through conversation using SMART method</action>
  <template-output>objectives</template-output>
</check>

<output>**Workshop 1 Complete!** ✅

**Vision:**
{{vision_statement}}

**Strategic Objectives:**
{{#each objectives}}
{{@index + 1}}. {{this.statement}}
{{/each}}

Next, we'll identify who can help you achieve these goals.</output>

</step>
