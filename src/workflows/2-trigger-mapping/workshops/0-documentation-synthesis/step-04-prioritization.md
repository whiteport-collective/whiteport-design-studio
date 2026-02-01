# Documentation Synthesis - Step 4: Prioritization

<critical>Documentation rarely includes explicit prioritization</critical>
<critical>Use conversation to determine what matters most</critical>

<step>

<output>**Prioritizing Strategic Elements**

Your documentation gives us the pieces. Now we need to prioritize:
- Which target groups have highest impact on your objectives?
- Which groups are most feasible to reach?
- Which driving forces are most frequent and intense?</output>

<action>Check if documentation includes any prioritization signals:
- Explicit priority statements
- Resource allocation (budget, team focus)
- Timeline emphasis (what's first)
- Frequency of mention
- Depth of research on certain groups
</action>

<check if="priority_signals_found">
  <output>Based on your documentation, I see these priority signals:

{{#each priority_signals}}
- {{this.signal}}: suggests {{this.implication}}
{{/each}}

This suggests the following prioritization:</output>
</check>

<check if="no_priority_signals">
  <output>Your documentation doesn't explicitly prioritize between groups or drivers.

Let's determine priorities together:</output>
</check>

<output>**Target Group Prioritization**

{{#each target_groups}}
**{{@index + 1}}. {{this.name}}**
{{/each}}</output>

<ask>For each group, let's assess:

**Impact on objectives:** If this group succeeds with your product, how much does it drive your objectives? (High/Medium/Low)

**Feasibility:** How easy is it to reach and serve this group? (High/Medium/Low)

Let's start with {{first_group.name}}:
- Impact on objectives?
- Feasibility?</ask>

<action>For each group, gather impact and feasibility ratings</action>
<action>Calculate priority score (Impact × Feasibility)</action>
<action>Rank groups by priority</action>

<output>**Priority Ranking:**

{{#each prioritized_groups}}
{{@index + 1}}. **{{this.name}}** ({{this.priority_level}})
   - Impact on objectives: {{this.impact}}
   - Feasibility: {{this.feasibility}}
   - Reasoning: {{this.reasoning}}
{{/each}}</output>

<ask>Does this prioritization align with your strategic thinking?</ask>

<template-output>prioritized_groups</template-output>

<output>---

**Driving Forces Prioritization**

Now let's identify the top drivers across all groups:</output>

<action>Analyze driving forces for:
- Frequency (how many groups share this driver?)
- Intensity (how strongly do they feel this?)
- Alignment with top-priority groups
</action>

<output>**Top Driving Forces:**

{{#each top_drivers}}
{{@index + 1}}. **{{this.driver}}** ({{this.type}})
   - Affects: {{this.groups_affected}}
   - Intensity: {{this.intensity}}
   - Priority: {{this.priority_level}}
{{/each}}</output>

<ask>Do these feel like the most critical drivers to address?</ask>

<template-output>prioritized_drivers</template-output>

<output>---

**Design Focus Statement**

Based on this prioritization:</output>

<action>Generate focus statement combining:
- Top priority group
- Top 3-5 drivers
- Connection to objectives
</action>

<output>{{focus_statement}}</output>

<ask>Does this capture where design efforts should focus?</ask>

<template-output>focus_statement</template-output>

<output>**Workshop 4 Complete!** ✅

**Strategic Priorities Set:**
- Top group: {{top_group.name}}
- Top drivers: {{top_driver_count}} identified
- Focus statement: Defined

{{#if feature_list_in_docs}}
Your documentation includes a feature list. Would you like to run the optional **Feature Impact workshop** to score features against these priorities?
{{/if}}

{{#if no_feature_list}}
Next, I'll create your comprehensive Trigger Map documentation and handover.
{{/if}}</output>

</step>
