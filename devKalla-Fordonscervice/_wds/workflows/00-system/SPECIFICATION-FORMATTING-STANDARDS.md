# WDS Specification Formatting Standards

**For:** All WDS Agents (Freya, Saga, Idunn)  
**Purpose:** Ensure consistent, readable, and maintainable specification formatting  
**Version:** 1.0

---

## Core Principle

**Specifications must follow WDS formatting standards for consistency, readability, and maintainability.**

Deviations from these standards make specifications harder to read, maintain, and implement.

---

## Markdown Structure Standards

### Heading Hierarchy

**Rules:**
- Use proper heading levels (H1 → H2 → H3 → H4)
- Never skip heading levels (e.g., H1 → H3)
- Only one H1 per page (the page title)
- Use H2 for major sections
- Use H3 for subsections
- Use H4 for component details

**Correct:**
```markdown
# 1.2 Sign In

## Page Sections

### Navigation Header Section

#### Logo Component
```

**Incorrect:**
```markdown
# 1.2 Sign In

#### Navigation Header Section  ← Skipped H2 and H3

## Logo Component  ← Wrong level
```

---

### Content Translation Format

**Rules:**
- Each language on a separate line
- Use consistent indentation (2 spaces)
- Language code in UPPERCASE
- Colon after language code
- Content in quotes

**Correct:**
```markdown
**Content:**
- EN: "Sign In"
- SE: "Logga In"
- NO: "Logg Inn"
```

**Incorrect:**
```markdown
**Content:** EN: "Sign In", SE: "Logga In", NO: "Logg Inn"  ← All on one line

**Content:**
- en: "Sign In"  ← Lowercase language code
- SE "Logga In"  ← Missing colon
- NO: Logg Inn  ← Missing quotes
```

---

### Area Label Format

**Rules:**
- Always use `**AREA LABEL**:` (all caps, bold)
- Label in backticks
- Follow naming convention: `{page}-{section}-{element}`
- Lowercase with hyphens

**Correct:**
```markdown
**AREA LABEL**: `signin-form-email`
```

**Incorrect:**
```markdown
**Area Label**: signin-form-email  ← Not bold, no backticks
**area label**: `signin-form-email`  ← Not all caps
**AREA LABEL**: `SignIn-Form-Email`  ← CamelCase instead of kebab-case
```

**Note:** Area Labels identify UI locations across sketch, specification, and code. They become both `id` and `aria-label` attributes in HTML implementation.

---

### List Formatting

**Rules:**
- Use `-` for unordered lists (not `*` or `+`)
- Consistent indentation (2 spaces per level)
- Blank line before and after lists
- No blank lines between list items (unless nested)

**Correct:**
```markdown
**Features:**

- Email authentication
- Google SSO
- Password reset
- Remember me option
```

**Incorrect:**
```markdown
**Features:**
* Email authentication  ← Wrong bullet character

+ Google SSO  ← Wrong bullet character

- Password reset

- Remember me option  ← Unnecessary blank lines
```

---

### Code Block Formatting

**Rules:**
- Always specify language for syntax highlighting
- Use triple backticks
- Indent code blocks at same level as surrounding text

**Correct:**
```markdown
**HTML Implementation:**

```html
<form id="signin-form">
  <input type="email" id="email" />
</form>
```
```

**Incorrect:**
```markdown
**HTML Implementation:**

```  ← No language specified
<form id="signin-form">
  <input type="email" id="email" />
</form>
```
```

---

## Content Organization Standards

### Section Order

**Standard page specification order:**

1. Page title (H1)
2. Overview
3. Page Sections
4. Structural Object IDs
5. Components & Object IDs
6. Page States
7. Validation Rules
8. Error Messages
9. Data Requirements
10. Responsive Behavior
11. Interactions & Navigation
12. Accessibility
13. Technical Notes
14. Design References

**Do not rearrange or skip sections without reason.**

---

### Component Specification Format

**Standard component format:**

```markdown
### {Component Name}

**OBJECT ID**: `{page-section-element}`

**Component Type:** {type}

**Purpose:** {What job does this do?}

**Content:**
- EN: "{English text}"
- SE: "{Swedish text}"

**Behavior:** {What happens on interaction}

**States:**
- Default: {description}
- Hover: {description}
- Active: {description}
```

**All components must follow this structure.**

---

## Language & Translation Standards

### Multi-Language Content

**Rules:**
- All product languages must be present
- Languages listed in same order throughout spec
- Each language on separate line
- No inline translations

**Correct:**
```markdown
#### Button Text

**Content:**
- EN: "Continue"
- SE: "Fortsätt"
- NO: "Fortsett"
```

**Incorrect:**
```markdown
#### Button Text

**Content:** "Continue" (EN), "Fortsätt" (SE), "Fortsett" (NO)  ← Inline

**Content:**
- EN: "Continue"
- NO: "Fortsett"  ← Wrong order (SE missing)
```

---

### Specification Language vs Product Languages

**Specification Language:**
- Used for descriptions, instructions, annotations
- Consistent throughout spec

**Product Languages:**
- Used for user-facing content only
- All languages present for each content item

**Example:**
```markdown
## Hero Section

**Purpose:** Convert visitors into users by presenting value proposition  ← Spec language

#### Primary Headline

**OBJECT ID**: `start-hero-headline`

**Content:**  ← Product languages
- EN: "Every walk. on time."
- SE: "Varje promenad. i tid."
```

---

## Formatting Consistency Standards

### Bold & Italic Usage

**Rules:**
- Use `**bold**` for field labels (OBJECT ID, Content, Purpose, etc.)
- Use `*italic*` for emphasis only (sparingly)
- Never use bold for entire paragraphs

**Correct:**
```markdown
**Purpose:** Convert visitors into users

**Content:**
- EN: "Get Started"
```

**Incorrect:**
```markdown
Purpose: Convert visitors into users  ← Not bold

**Convert visitors into users by presenting a compelling value proposition and clear call-to-action that addresses their primary pain points.**  ← Entire paragraph bold
```

---

### Spacing Standards

**Rules:**
- One blank line between sections
- No blank lines between list items (unless nested)
- Two blank lines before major section headings (H2)
- Consistent indentation (2 spaces)

**Correct:**
```markdown
## Page Sections


### Navigation Header

**OBJECT ID**: `signin-header`

**Purpose:** Provide navigation and branding
```

**Incorrect:**
```markdown
## Page Sections
### Navigation Header  ← No blank line

**OBJECT ID**: `signin-header`


**Purpose:** Provide navigation and branding  ← Too many blank lines
```

---

### Link Formatting

**Rules:**
- Use descriptive link text
- Use relative paths for internal links
- Format: `[Link Text](path/to/file.md)`

**Correct:**
```markdown
See [Profile Setup Specification](../1.3-Profile-Setup/1.3-Profile-Setup.md)
```

**Incorrect:**
```markdown
See Profile Setup Specification  ← No link
See [here](../1.3-Profile-Setup/1.3-Profile-Setup.md)  ← Generic link text
See ../1.3-Profile-Setup/1.3-Profile-Setup.md  ← Raw URL
```

---

## Common Formatting Mistakes

### ❌ Mistake 1: Inline Translations

**Wrong:**
```markdown
**Content:** "Sign In" (EN), "Logga In" (SE)
```

**Right:**
```markdown
**Content:**
- EN: "Sign In"
- SE: "Logga In"
```

---

### ❌ Mistake 2: Inconsistent Area Label Format

**Wrong:**
```markdown
❌ Area Label: signin-form-email
❌ **area-label**: `signin-form-email`

✅ **AREA LABEL**: `signin-form-email`
```

**Right:**
```markdown
**OBJECT ID**: `signin-form-email`
```

---

### ❌ Mistake 3: Skipped Heading Levels

**Wrong:**
```markdown
# Page Title

#### Component  ← Skipped H2 and H3
```

**Right:**
```markdown
# Page Title

## Section

### Subsection

#### Component
```

---

### ❌ Mistake 4: Inconsistent List Bullets

**Wrong:**
```markdown
- Item 1
* Item 2
+ Item 3
```

**Right:**
```markdown
- Item 1
- Item 2
- Item 3
```

---

### ❌ Mistake 5: Missing Language Translations

**Wrong:**
```markdown
**Content:**
- EN: "Submit"
← Missing SE translation
```

**Right:**
```markdown
**Content:**
- EN: "Submit"
- SE: "Skicka"
```

---

## Validation Checklist

Before finalizing a specification, check:

**Structure:**
- [ ] Proper heading hierarchy (H1 → H2 → H3 → H4)
- [ ] Sections in standard order
- [ ] Consistent spacing and indentation

**Object IDs:**
- [ ] Format: `**OBJECT ID**: `{id}``
- [ ] Naming convention: `{page}-{section}-{element}`
- [ ] All interactive elements have IDs

**Translations:**
- [ ] Each language on separate line
- [ ] All product languages present
- [ ] Consistent language order
- [ ] Proper formatting with quotes

**Lists:**
- [ ] Use `-` for bullets
- [ ] Consistent indentation
- [ ] Proper spacing

**Links:**
- [ ] Descriptive link text
- [ ] Valid paths
- [ ] Proper markdown format

**Code Blocks:**
- [ ] Language specified
- [ ] Proper indentation
- [ ] Triple backticks

---

## Agent Responsibilities

**When creating specifications:**
1. Follow all formatting standards
2. Use page specification template
3. Maintain consistency throughout
4. Validate before finalizing

**When reviewing specifications:**
1. Check for formatting deviations
2. Identify inconsistencies
3. Recommend corrections
4. Update to match standards

---

## Related Resources

- **Page Specification Template:** `../workflows/4-ux-design/templates/page-specification.template.md`
- **Language Configuration Guide:** `./language-configuration-guide.md`
- **File Naming Conventions:** `./FILE-NAMING-CONVENTIONS.md`
- **Specification Quality Guide:** `../data/agent-guides/freya/specification-quality.md`

---

**Consistent formatting creates professional, maintainable specifications that developers trust.** 📝✨
