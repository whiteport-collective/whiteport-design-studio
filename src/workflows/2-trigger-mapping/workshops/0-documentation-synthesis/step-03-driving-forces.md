# Documentation Synthesis - Step 3: Driving Forces

<critical>Frame as validation: "Your material suggests X, is this correct?"</critical>
<critical>Documentation often focuses on positive wants - probe for negative drivers</critical>

<step>

<action>For each persona, analyze documentation for psychological drivers</action>

<output>**Mapping Psychological Drivers**

For each persona, we need to understand BOTH sides of motivation:
- **Positive drivers** (what they want to achieve)
- **Negative drivers** (what they fear or want to avoid)

Remember: Negative drivers are often more powerful (loss aversion principle).</output>

{{#each personas}}

<output>---

**{{this.name}}**</output>

<check if="positive_drivers_found">
  <output>**Positive Drivers (What they want)**

Your documentation suggests {{this.name}} wants to:

{{#each this.extracted_positive}}
- {{this}}
{{/each}}</output>

  <ask>Do these capture what {{this.name}} is trying to achieve? Anything missing?</ask>
  
  <action>Refine positive drivers based on feedback</action>
</check>

<check if="vague_positive_drivers">
  <output>**Positive Drivers (What they want)**

Your documentation mentions general needs like:
{{#each this.vague_wants}}
- "{{this}}"
{{/each}}

These are too vague. Let's make them specific to the **usage context**.</output>

  <ask>When {{this.name}} uses your product, what specific outcomes do they want?

Not general life goals, but what they want to accomplish **in this usage context**.</ask>
  
  <action>Create specific usage-context positive drivers</action>
</check>

<check if="no_positive_drivers_found">
  <output>**Positive Drivers (What they want)**

Your documentation doesn't explicitly state what {{this.name}} wants to achieve.</output>

  <ask>When {{this.name}} uses your product, what are they trying to accomplish? What positive outcomes do they seek?</ask>
  
  <action>Define positive drivers through conversation</action>
</check>

<check if="negative_drivers_found">
  <output>**Negative Drivers (What they fear/avoid)**

Your research identifies these fears and frustrations:

{{#each this.extracted_negative}}
- {{this}}
{{/each}}</output>

  <ask>Do these capture what {{this.name}} wants to avoid? Any other fears or frustrations?</ask>
  
  <action>Refine negative drivers based on feedback</action>
</check>

<check if="pain_points_but_not_drivers">
  <output>**Negative Drivers (What they fear/avoid)**

Your documentation mentions pain points:
{{#each this.pain_points}}
- {{this}}
{{/each}}

Let's frame these as **psychological drivers** - what they fear or want to avoid.</output>

  <ask>Based on these pain points, what does {{this.name}} fear? What are they trying to avoid?

Think about:
- Fear of embarrassment or looking unprofessional
- Fear of wasting time or money
- Fear of making wrong decisions
- Frustration with current solutions
- Anxiety about outcomes</ask>
  
  <action>Transform pain points into negative drivers</action>
</check>

<check if="no_negative_drivers_found">
  <output>**Negative Drivers (What they fear/avoid)**

Your documentation focuses on what users want, but doesn't mention fears or frustrations.

This is common - but negative drivers are often MORE powerful than positive ones!</output>

  <ask>What does {{this.name}} fear or want to avoid in this context?

Think about the flip side of their positive wants:
- If they want to look professional, they fear looking unprofessional
- If they want to save time, they fear wasting time
- If they want to make good decisions, they fear making wrong ones

What are {{this.name}}'s fears and frustrations?</ask>
  
  <action>Define negative drivers through conversation</action>
</check>

<template-output>{{this.name}}_driving_forces</template-output>

{{/each}}

<output>**Workshop 3 Complete!** ✅

**Driving Forces Mapped:**
{{#each personas}}
- **{{this.name}}**: {{this.positive_count}} positive drivers, {{this.negative_count}} negative drivers
{{/each}}

Next, we'll prioritize which groups and drivers matter most.</output>

</step>
