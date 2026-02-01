# Step 03b: Generate Secondary Persona Document

**Goal:** Create detailed profile for the SECONDARY target user

---

## Purpose

Create the SECONDARY persona document - the validator who needs to trust the product.

**Focus:** Validation strategy, trust building, evaluation process

---

## Input Required

From trigger map YAML:
- `targetGroups.secondary` section
- Name, role, type, roleInFlywheel
- 6 drivingForces (3 wants, 3 fears)

---

## Template Reference

Use the comprehensive persona document template:
`templates/persona-document-template.md`

This template provides the complete structure for sections 1-13.

---

## File Naming

```
03-[Name]-the-[Role].md
```

**Example:** `03-Marcus-the-Mentor.md`

---

## Key Requirements

**Length:** ~250-375 lines

**Tone:**
- Rich, nuanced, human
- Not "converting" but "creating awesome"
- Natural language, storytelling

**Driving Forces:**
- Each must have **[Product] Answer**
- Show how product addresses each driver
- Be specific and actionable

**Validation:**
- Focus on what builds trust
- Show the evaluation journey
- Address skepticism and concerns

---

## Secondary-Specific Section

**Include:** "Validation Strategy"

Show:
- What they need to see about the product
- Conversion path: Discovery → Evaluation → Adoption → Advocacy
- Focus on validation and trust building
- How product proves its value to them

---

## Example

Reference: `examples/WDS-Presentation/docs/2-trigger-map/03-Lars-the-Leader.md` (SECONDARY - 316 lines)

---

## Output

<output>✅ Secondary persona document created: `03-[Name]-the-[Role].md`</output>

Store as: `03-[Name]-the-[Role].md` in trigger map folder

---

## Next Step

**If Tertiary persona exists:**

<output>Ready for Step 3c: Generate Tertiary Persona</output>

<action>Load and execute: step-03c-generate-tertiary-persona.md</action>

**If NO Tertiary persona:**

<output>Ready for Step 4: Generate Key Insights Document</output>

<action>Load and execute: step-04-generate-key-insights.md</action>

Do NOT skip ahead.
