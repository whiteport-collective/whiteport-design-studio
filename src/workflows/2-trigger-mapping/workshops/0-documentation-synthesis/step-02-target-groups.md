# Documentation Synthesis - Step 2: Target Groups

<critical>Frame as validation: "Your material suggests X, is this correct?"</critical>
<critical>Documentation may have demographics but need behavioral depth</critical>

<step>

<action>Analyze documentation for target groups and user research</action>

<check if="target_groups_found">
  <output>**Target Groups**
  
Your documentation identifies these user groups:

{{#each extracted_groups}}
**{{@index + 1}}. {{this.name}}**
{{this.description}}

Key characteristics from your docs:
{{#each this.characteristics}}
- {{this}}
{{/each}}
{{/each}}

I found {{group_count}} groups total.</output>

  <ask>Are these the right groups? Should we focus on the top 3-4 most critical for your objectives?</ask>
  
  <action>Help prioritize to 3-4 groups maximum</action>
  <template-output>target_groups</template-output>
</check>

<check if="demographic_only_groups">
  <output>**Target Groups**
  
Your documentation mentions these users:

{{#each extracted_groups}}
- {{this.name}}: {{this.demographic_description}}
{{/each}}

However, these are mostly demographic descriptions. For Trigger Mapping, we need **behavioral** profiles.</output>

  <ask>For each group, what's their **context and situation** when using your product? What are they trying to accomplish?</ask>
  
  <action>Transform demographic descriptions into behavioral profiles through conversation</action>
  <template-output>target_groups</template-output>
</check>

<check if="no_target_groups_found">
  <output>**Target Groups**
  
I don't see clear target group definitions in your documentation. 

Based on the context and objectives, these groups might be relevant:
{{#each inferred_groups}}
- **{{this.name}}**: {{this.reasoning}}
{{/each}}</output>

  <ask>Who are the 3-4 key user groups whose product usage will drive your objectives?

Remember the core question: WHO out there in the world will make sure, with their use of the product, that you achieve your goals?</ask>
  
  <action>Define target groups through conversation</action>
  <template-output>target_groups</template-output>
</check>

<output>---

**Creating Detailed Personas**

Now let's add psychological depth to each group...</output>

<action>For each target group, check documentation for:
- Context and situation
- Goals and aspirations
- Frustrations and fears
- Behavioral patterns
- User quotes or interview insights
</action>

<check if="deep_personas_found">
  <output>Your research provides good psychological depth. Here are the personas:

{{#each personas}}
**{{this.name}}**

{{this.description}}

**Context:** {{this.context}}
**Goals:** {{this.goals}}
**Frustrations:** {{this.frustrations}}
{{#if this.quote}}**Quote from research:** "{{this.quote}}"{{/if}}
{{/each}}</output>

  <ask>Do these capture the psychological depth we need? Any refinements?</ask>
  
  <template-output>personas</template-output>
</check>

<check if="shallow_personas_found">
  <output>Your documentation has basic user descriptions, but we need more psychological depth.

{{#each personas}}
**{{this.name}}**

From your docs: {{this.basic_description}}

To make this actionable, we need to understand:
{{/each}}</output>

  <ask>For each persona:
- What's their **context** when using your product?
- What are they trying to **accomplish** (usage goals)?
- What **frustrates** them in this context?
- What do they **fear** or want to avoid?</ask>
  
  <action>Build psychological depth through conversation</action>
  <template-output>personas</template-output>
</check>

<check if="interview_quotes_available">
  <output>I found some great quotes from your user interviews:

{{#each quotes}}
"{{this.quote}}" - {{this.source}}
{{/each}}

These reveal real psychology. Let me incorporate these into the personas...</output>
  
  <action>Use quotes to enrich persona descriptions</action>
</check>

<output>**Workshop 2 Complete!** ✅

**Target Groups (Prioritized):**
{{#each prioritized_groups}}
{{@index + 1}}. {{this.name}}
{{/each}}

Next, we'll map what drives each group psychologically.</output>

</step>
