# Documentation Synthesis - Step 5: Gap Analysis & Validation

<critical>Identify what's strong vs. weak in documentation</critical>
<critical>Validate strategic alignment between docs and plans</critical>

<step>

<output>**Gap Analysis & Validation**

Let me analyze what we've built from your documentation...</output>

<action>Compare original documentation to synthesized Trigger Map:
- What was clear and strong?
- What was vague or missing?
- What did we fill through conversation?
- Are there contradictions or misalignments?
</action>

<output>**Documentation Strengths:**

{{#each strengths}}
✅ {{this.area}}: {{this.description}}
{{/each}}</output>

<check if="gaps_identified">
  <output>**Gaps Identified:**

{{#each gaps}}
⚠️ **{{this.area}}**: {{this.gap}}
   - Impact: {{this.impact}}
   - What we did: {{this.how_filled}}
{{/each}}</output>
</check>

<check if="critical_gaps">
  <output>**Critical Gaps:**

{{#each critical_gaps}}
❌ **{{this.area}}**: {{this.gap}}
   - **Impact:** {{this.impact}}
   - **Recommendation:** {{this.recommendation}}
{{/each}}</output>

  <ask>These gaps could affect your strategy. Would you like to:

a. **Address now** - Fill these gaps through focused conversation
b. **Note for later** - Document as areas for future research
c. **Accept as-is** - Work with what we have

Which approach?</ask>

  <check if="address_now">
    <action>Run targeted mini-workshops for critical gaps</action>
  </check>

  <check if="note_for_later">
    <action>Document gaps in handover notes</action>
  </check>
</check>

<output>---

**Strategic Alignment Check**</output>

<action>Reverse engineer: Does the plan match the vision?
- Compare stated vision to implied vision from plans
- Check if objectives align with vision
- Verify target groups serve objectives
- Validate features address drivers
</action>

<output>**Consistency Check:**

Your documentation says you want:
> {{vision_statement}}

Your plan/features suggest:
> {{plan_implications}}</output>

<check if="alignment_good">
  <output>✅ **Strong alignment** - Your plans effectively support your vision.

The Trigger Map reveals a coherent strategy where:
- Objectives measure progress toward vision
- Target groups drive objectives through their usage
- Driving forces are addressed by planned approach</output>
</check>

<check if="alignment_issues">
  <output>⚠️ **Potential misalignment detected:**

{{#each misalignments}}
**Issue {{@index + 1}}:** {{this.issue}}
- **Documentation says:** {{this.doc_says}}
- **Plan implies:** {{this.plan_implies}}
- **Recommendation:** {{this.recommendation}}
{{/each}}</output>

  <ask>These misalignments could indicate:
- Vision and plan aren't fully aligned
- Documentation is outdated
- Hidden assumptions need surfacing

Should we address these before finalizing the Trigger Map?</ask>

  <action>Discuss and resolve misalignments</action>
</check>

<output>---

**What You've Accomplished**

From your documentation, we've created:

✅ **Clear Vision**: {{vision_statement}}
✅ **{{objective_count}} Strategic Objectives**: Measurable and SMART
✅ **{{group_count}} Prioritized Target Groups**: Behavioral profiles with psychological depth
✅ **{{driver_count}} Driving Forces**: Both positive and negative
✅ **Strategic Focus**: {{focus_statement}}
✅ **Gap Analysis**: {{gap_count}} areas identified for future research

**What you now have:**
- Single-slide strategic reference (instead of {{page_count}} pages)
- Clear priorities for design decisions
- Psychological insights organized and actionable
- Gaps identified for future research
- Validated strategic alignment

**What you can do with this:**
- Reference it in daily design work
- Share it in AI chats for context (much better than pasting extensive docs)
- Use it for team alignment
- Guide feature prioritization
- Validate design decisions</output>

<ask>Ready to proceed to documentation generation and handover?</ask>

<template-output>gap_analysis</template-output>
<template-output>alignment_check</template-output>

</step>
