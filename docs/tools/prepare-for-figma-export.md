# Prepare for Figma Export: ID Injection Workflow

**Version**: 1.0  
**Last Updated**: January 21, 2026  
**Purpose**: Temporarily add OBJECT IDs to HTML for Figma MCP export  
**Direction**: Code → Figma (with temporary ID injection)

---

## Overview

This workflow enables exporting code to Figma via the html.to.design MCP server **without permanently adding IDs to production code**. The agent temporarily injects OBJECT IDs from specifications during export, then removes them afterward.

### The Problem This Solves

- ✅ **Production code stays clean** - No unnecessary IDs cluttering components
- ✅ **Figma layers get proper names** - OBJECT IDs from specifications used for layer naming
- ✅ **Specification mapping maintained** - Clear connection between specs, code, and Figma
- ✅ **Accessibility preserved** - No misuse of `aria-label` for layer naming
- ✅ **Flexible workflow** - Works for early prototypes and production code

### When to Use This Workflow

Use this workflow when:
- Exporting early prototypes that don't have IDs yet
- Exporting from browser preview for quick design review
- Sending production code to Figma without modifying source files
- Testing visual iterations in Figma before committing to code changes

---

## Choosing Your Export Method

There are **two methods** for exporting to Figma, each with different capabilities:

| Feature | **Method 1: MCP Server** | **Method 2: Browser Extension** |
|---------|-------------------------|--------------------------------|
| **Automation** | ✅ Fully automated | ⚠️ Manual capture required |
| **File Modification** | ✅ No files modified | ⚠️ Temporary aria-labels added to source |
| **Multiple Viewports** | ❌ One viewport at a time | ✅ Mobile, tablet, desktop simultaneously |
| **Responsive Testing** | ❌ Limited | ✅ True responsive capture |
| **Speed** | ✅ Instant | ⚠️ Requires browser interaction |
| **Safety** | ✅ Zero risk (no file changes) | ⚠️ Must remember to remove aria-labels |
| **Best For** | Quick single-page exports | Responsive design documentation |

### Recommendation

**Use MCP Server (Method 1) when:**
- You need a quick export for design review
- You're exporting a single viewport
- You want zero risk of modifying source files

**Use Browser Extension (Method 2) when:**
- You need multiple viewport captures (mobile/tablet/desktop)
- You're documenting responsive behavior
- You want to see how design adapts across breakpoints

---

## Core Principle: Temporary aria-label Injection

**The Strategy:**
1. **Read** the component code (without aria-labels)
2. **Load** OBJECT IDs from specification
3. **Generate** temporary HTML with `aria-label` attributes matching OBJECT IDs
4. **Export** to Figma via MCP (one page at a time)
5. **Discard** temporary HTML (never save to files)

**Result:** Figma layers get named from `aria-label` values, production code stays clean.

**Why aria-label for Figma?**
- The html.to.design MCP server uses `aria-label` attributes to name Figma layers
- These are temporary - only added during export, never saved to source files
- Production code keeps proper accessibility practices (aria-labels only where needed)

---

## Phase 1: Identify Export Target

### Step 1.1: Determine What to Export

**User Request Examples:**
- "Export the sign-in page to Figma"
- "Send the CTA button states to Figma for design review"
- "I want to iterate on the hero section spacing in Figma"

**Extract:**
- Component/page name
- File path (if provided)
- Purpose (design review, state documentation, visual iteration)

---

### Step 1.2: Locate Source Code

**Search Strategy:**
```
1. Check if user provided file path
2. Search in components/ directory
3. Search in app/ directory
4. Search in docs/ for prototypes
```

**Decision Point:**
- ✅ Source found → **Continue to Phase 2**
- ❌ Source not found → **Ask user for clarification**

---

## Phase 2: Load Specification OBJECT IDs

### Step 2.1: Search for Specification

**Search Locations (priority order):**
1. `docs/C-Scenarios/` - Scenario specifications
2. `docs/D-Design-System/` - Component specifications
3. Project root - Any related markdown files

**Search Method:**
```
Use grep_search or find_by_name to locate:
- Files containing component/page name
- Files with "OBJECT ID" references
- Specification markdown files
```

---

### Step 2.2: Extract OBJECT IDs

**What to Extract:**
```markdown
From specification file:

#### Hero Section CTA Button
**OBJECT ID**: `start-hero-cta`
**CSS Class**: `.btn-cta-primary`

Extract:
- OBJECT ID: start-hero-cta
- Component: Hero Section CTA Button
- CSS Class: btn-cta-primary
```

**Create ID Mapping:**
```javascript
{
  "start-hero-cta": {
    "cssClass": "btn-cta-primary",
    "selector": "button.btn-cta-primary",
    "type": "button"
  },
  "start-hero-headline": {
    "cssClass": "hero-headline",
    "selector": "h1.hero-headline",
    "type": "heading"
  }
}
```

---

### Step 2.3: Handle Missing Specifications

**If no specification found:**

**Option A: Generate IDs from Code Structure**
```
Analyze component structure:
- Extract CSS class names
- Identify semantic elements
- Generate OBJECT IDs following project convention

Pattern: {page}-{section}-{element}
Example: start-hero-cta, start-hero-headline
```

**Option B: Ask User for Guidance**
```
⚠️ No specification found for {component-name}

I can:
1. Generate temporary IDs based on code structure
2. Create a specification first (recommended)
3. Use CSS class names as IDs

Which approach would you prefer?
```

---

## Phase 3: Generate Temporary HTML with IDs

### Step 3.1: Read Source Code

**For React/TSX Components:**
```tsx
// Original component (no IDs)
export function LandingHero() {
  return (
    <section className="hero-section">
      <div className="hero-content">
        <h1 className="hero-headline">
          Every walk. on time. Every time.
        </h1>
        <button className="btn-cta-primary">
          Start Planning
        </button>
      </div>
    </section>
  )
}
```

---

### Step 3.2: Map OBJECT IDs to Elements

**Mapping Strategy:**
```
Match by CSS class:
  .hero-section → aria-label="start-hero-section"
  .hero-content → aria-label="start-hero-content"
  .hero-headline → aria-label="start-hero-headline"
  .btn-cta-primary → aria-label="start-hero-cta"

Match by semantic element + context:
  <section> in hero → aria-label="start-hero-section"
  <h1> in hero → aria-label="start-hero-headline"
  <button> with CTA class → aria-label="start-hero-cta"
```

---

### Step 3.3: Generate HTML with Injected aria-labels

**Transformation:**
```html
<!-- Generated HTML for Figma export -->
<section aria-label="start-hero-section" class="hero-section">
  <div aria-label="start-hero-content" class="hero-content">
    <h1 aria-label="start-hero-headline" class="hero-headline">
      Every walk. on time. Every time.
    </h1>
    <button aria-label="start-hero-cta" class="btn-cta-primary">
      Start Planning
    </button>
  </div>
</section>
```

**Key Points:**
- ✅ aria-label attributes added to semantic elements (temporary, for Figma layer naming)
- ✅ Original classes preserved
- ✅ Structure unchanged
- ✅ Content matches source exactly

---

### Step 3.4: Add Inline Styles for Figma Compatibility

**Style Requirements:**
```html
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&display=swap');
  
  /* Convert CSS variables to hex values */
  .hero-section {
    background: linear-gradient(180deg, #FFA100 0%, #FF2714 100%);
    padding: 60px 20px;
    font-family: 'Fredoka', sans-serif;
  }
  
  .hero-headline {
    font-size: 48px;
    font-weight: 600;
    color: #FEF3CF;
    line-height: 1.2;
  }
  
  .btn-cta-primary {
    background: linear-gradient(to bottom, #FFA100, #FF2714);
    color: #FEF3CF;
    padding: 13px 25px 16px;
    border-radius: 16px;
    font-size: 18px;
    font-weight: 500;
    border: 1px solid #FFA100;
  }
</style>
```

**Style Conversion Rules:**
- CSS variables → Hex colors
- rem/em → px values
- Google Fonts only
- Inline or `<style>` block

**Note:** Styles use class selectors. The `aria-label` attributes are only for Figma layer naming, not for styling.

---

## Phase 4: Export to Figma

### Step 4.1: Verify MCP Connection

**Check:**
```
Is mcp1_import-html tool available?
- ✅ Yes → Continue to export
- ❌ No → Guide user through setup (see figma-mcp.md)
```

---

### Step 4.2: Execute Export

**MCP Call:**
```javascript
mcp1_import-html({
  name: "Landing Hero - Start Page",
  html: `
    <div aria-label="start-hero-export">
      <style>
        /* Figma-compatible styles */
      </style>
      
      <!-- HTML with aria-label attributes matching OBJECT IDs -->
      <section aria-label="start-hero-section" class="hero-section">
        ...
      </section>
    </div>
  `
})
```

**Expected Response:**
```json
{
  "node": {
    "id": "3:150",
    "name": "Landing Hero - Start Page by html.to.design...",
    "type": "SECTION"
  }
}
```

---

### Step 4.3: Verify Export Success

**Success Indicators:**
- ✅ Node ID returned
- ✅ No error message
- ✅ User confirms layer visible in Figma
- ✅ Layer names match OBJECT IDs (from aria-label attributes)

**Communicate to User:**
```
✅ Successfully exported to Figma!

Export Details:
- Component: Landing Hero
- Figma Node ID: 3:150
- OBJECT IDs used (as aria-labels):
  • start-hero-section
  • start-hero-content
  • start-hero-headline
  • start-hero-cta

The layers in Figma now match your specification OBJECT IDs. 
You can make visual adjustments in Figma and reference these IDs 
when discussing changes.

Note: The aria-label attributes were added temporarily for export 
only - your source code remains unchanged.
```

---

## Phase 5: Post-Export Cleanup

### Step 5.1: Discard Temporary HTML

**Important:**
- ❌ **DO NOT save** the temporary HTML to any file
- ❌ **DO NOT commit** aria-label-injected code to repository
- ✅ **ONLY use** temporary HTML for MCP export (one page at a time)
- ✅ **KEEP** original source code unchanged

**Why:**
- Production code should only have aria-labels for genuine accessibility needs
- Temporary aria-labels are for Figma layer naming only
- Specifications remain the source of truth for OBJECT IDs

---

### Step 5.2: Document Export Metadata (Optional)

**If user wants to track exports:**
```markdown
## Figma Export Log

### Landing Hero - 2026-01-21
- **Source**: components/landing-hero.tsx
- **Figma Node**: 3:150
- **OBJECT IDs** (via aria-label): start-hero-section, start-hero-content, start-hero-headline, start-hero-cta
- **Purpose**: Design review for spacing and gradient adjustments
- **Specification**: docs/C-Scenarios/01-Customer-Onboarding/1.1-Start-Page/1.1-Start-Page.md
```

---

## Workflow Variations

### Variation A: MCP Server Export (Single Viewport)

**Scenario:** Quick export via MCP server, one page at a time

**Process:**
1. User identifies component to export
2. Agent locates source file
3. Agent loads specification OBJECT IDs
4. Agent generates temporary HTML with `aria-label` attributes in memory
5. Agent exports to Figma via MCP
6. Agent discards temporary HTML

**Advantages:**
- ✅ Fully automated
- ✅ No file modifications
- ✅ No manual steps

**Limitations:**
- ❌ One viewport at a time
- ❌ Cannot capture responsive variations simultaneously

---

### Variation B: Browser Extension Export (Multiple Viewports)

**Scenario:** User wants to capture mobile, tablet, and desktop viewports simultaneously using html.to.design browser extension

**Process:**

**Step 1: Add aria-labels to Preview**
```
Agent adds aria-label attributes to source files temporarily:

components/landing-hero.tsx:
<section aria-label="start-hero-section" className="hero-section">
  <h1 aria-label="start-hero-headline" className="hero-headline">
    Every walk. on time. Every time.
  </h1>
  <button aria-label="start-hero-cta" className="btn-cta-primary">
    Start Planning
  </button>
</section>

⚠️ IMPORTANT: These changes are temporary and will be removed after capture
```

**Step 2: User Captures with Browser Extension**
```
Instructions to user:

1. Open preview in browser (http://localhost:3000)
2. Activate html.to.design browser extension
3. Select multiple viewports:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1440px)
4. Click "Capture" in extension
5. Confirm layers appear in Figma with proper OBJECT ID names
6. Notify agent when capture is complete
```

**Step 3: Remove aria-labels from Source**
```
Agent removes temporary aria-label attributes:

components/landing-hero.tsx:
<section className="hero-section">
  <h1 className="hero-headline">
    Every walk. on time. Every time.
  </h1>
  <button className="btn-cta-primary">
    Start Planning
  </button>
</section>

✅ Source code restored to clean state
```

**Advantages:**
- ✅ Multiple viewports captured simultaneously
- ✅ True responsive testing in Figma
- ✅ Layers properly named with OBJECT IDs

**Limitations:**
- ⚠️ Requires temporary file modification
- ⚠️ Manual browser extension interaction
- ⚠️ Must remember to remove aria-labels after capture

**Safety Protocol:**
```
Before removing aria-labels, agent asks:

"Have you completed the Figma capture with the browser extension?
I'll now remove the temporary aria-label attributes from your source files."

Wait for user confirmation before proceeding.
```

---

### Variation C: Export Component States

**Scenario:** Export button with hover, active, disabled states

**Process:**
1. Load OBJECT IDs from specification
2. Generate HTML for each state:
   ```html
   <div aria-label="button-states-showcase">
     <div class="state-container">
       <div class="state-label">Default</div>
       <button aria-label="btn-cta-primary-default">Start Planning</button>
     </div>
     <div class="state-container">
       <div class="state-label">Hover</div>
       <button aria-label="btn-cta-primary-hover">Start Planning</button>
     </div>
     <!-- More states... -->
   </div>
   ```
3. Export to Figma (one page at a time)
4. Discard temporary HTML

---

### Variation D: Export Early Prototype

**Scenario:** Prototype HTML in docs/ needs design review

**Process:**
1. Read prototype HTML file
2. Check if aria-labels already present
3. If missing, inject aria-labels with OBJECT IDs from specification
4. Export to Figma
5. Optionally: Update prototype file with aria-labels (user decision)

**Decision Point:**
```
The prototype HTML is missing aria-labels for Figma export.

Would you like me to:
1. Add aria-labels temporarily for this export only
2. Add aria-labels permanently to the prototype file
3. Create a specification first, then add aria-labels

Recommendation: Option 2 is best for prototypes since they're 
documentation artifacts, not production code.
```

---

## Best Practices

### DO ✅

- **Always load OBJECT IDs from specifications first**
- **Generate temporary HTML in memory** (never save to files)
- **Preserve original component structure** (only add aria-labels)
- **Export one page at a time** through MCP server
- **Use specification naming conventions** for consistency
- **Communicate clearly** that aria-labels are temporary
- **Verify export success** before discarding HTML
- **Document exports** if tracking is needed

### DON'T ❌

- **Don't modify source files** with temporary aria-labels (except for browser extension method)
- **Don't commit aria-label-injected code** to repository
- **Don't save temporary HTML** (only use for MCP export)
- **Don't skip specification lookup** (always check first)
- **Don't export without aria-labels** (Figma layers will have generic names)
- **Don't use generic aria-labels** (follow specification patterns)

---

## Troubleshooting

### Issue: Figma Layers Have Generic Names

**Cause:** aria-label attributes not properly injected into HTML

**Solution:**
1. Verify OBJECT IDs were loaded from specification
2. Check aria-label injection mapping logic
3. Ensure aria-labels added to correct elements
4. Re-export with corrected HTML

---

### Issue: Specification Not Found

**Cause:** Component doesn't have specification yet

**Solution:**
```
⚠️ No specification found for {component-name}

Options:
1. Create specification first (recommended for production components)
2. Generate temporary IDs from code structure (for quick exports)
3. Use CSS class names as IDs (fallback)

For production components, I recommend creating a specification 
to maintain design-code parity. Would you like me to create one?
```

---

### Issue: aria-label Mapping Unclear

**Cause:** Multiple elements with same class, unclear hierarchy

**Solution:**
1. Analyze component structure more carefully
2. Use parent-child context for OBJECT ID generation
3. Ask user for clarification on ambiguous elements
4. Reference similar components in specifications

---

## Integration with Existing Workflows

### Works With: Figma Export Workshop

This workflow is a **preprocessing step** for the main Figma Export Workshop:

```
Prepare for Figma Export (this workflow)
  ↓ Generates HTML with aria-labels matching OBJECT IDs
Figma Export Workshop (existing)
  ↓ Validates and exports to Figma (one page at a time)
Result: Figma layers with proper OBJECT ID names
```

---

### Works With: Specification-Driven Development

This workflow **reinforces** the specification-first approach:

```
1. Specification created with OBJECT IDs
2. Component implemented (without aria-labels in production)
3. Export to Figma (aria-labels injected from spec, one page at a time)
4. Design iteration in Figma (using OBJECT ID layer names)
5. Changes communicated using OBJECT IDs
6. Code updated based on OBJECT ID references
```

**Result:** Specifications remain source of truth for naming

---

## Summary

This workflow enables **clean, specification-driven Figma exports** without cluttering production code:

- ✅ **Specifications remain source of truth** for OBJECT IDs
- ✅ **Production code stays clean** (no unnecessary aria-labels)
- ✅ **Figma layers properly named** (using OBJECT IDs via aria-labels)
- ✅ **Design-code parity maintained** (shared naming system)
- ✅ **Flexible for any stage** (prototypes, production, previews)
- ✅ **One page at a time** through MCP server (no file saving needed)

**Key Principle:** aria-label attributes are injected temporarily during export, then discarded. The specification-to-Figma connection is maintained without modifying source files.

---

**Related Documentation:**
- [Figma MCP Integration](./figma-mcp.md)
- [html.to.design Tool](./html-to-design.md)
- [WDS Tools Guide](./wds-tools-guide.md)

**Version History:**
- v1.0 (2026-01-21): Initial workflow based on ID injection strategy
