# Step 1: Initialize Dialog

## CONTEXT

This is the first step of the Agent Dialog Workflow. We create the folder structure and main dialog file.

---

## SELECT DIALOG TYPE

<ask>**What type of work is this?**

| Type | Icon | Use When |
|------|------|----------|
| **[A] Prototype Implementation** | 🔧 | Building UI from specifications |
| **[B] Bug Fix** | 🐛 | Fixing issues and defects |
| **[C] Design Exploration** | 🎨 | Exploring visual/UX directions |
| **[D] Capture** | 💾 | Saving ideas for later |
| **[E] Generic** | 📋 | Anything else |

Type:</ask>

<action>
Store dialog_type and select appropriate template:
- A → templates/dialog-types/prototype-implementation.template.md
- B → templates/dialog-types/bug-fix.template.md
- C → templates/dialog-types/design-exploration.template.md
- D → templates/dialog-capture.template.md
- E → templates/dialog.template.md
</action>

---

## GATHER INFORMATION

<ask>**What feature or implementation are we working on?**

Examples:
- "Booking details drawer"
- "User authentication refactor"
- "Calendar scroll fix"

Feature name:</ask>

<action>Store feature_name and generate feature_slug (lowercase, hyphenated)</action>

<ask>**Which specification(s) are relevant?**

Provide the path to the specification file(s) this implementation is based on.

Specification path:</ask>

<action>Store spec_path</action>

<ask>**What agent persona should execute this work?**

Examples:
- "Freya (UX Designer)" — For UI implementation
- "Dev Agent" — For backend work
- "Full Stack" — For end-to-end features

Agent:</ask>

<action>Store agent_name</action>

---

## CREATE FOLDER STRUCTURE

<action>
**Create dialog folder:**

Path: `docs/F-Agent-Dialogs/{date}-{feature_slug}/`

Where:
- `{date}` = Today's date in YYYY-MM-DD format
- `{feature_slug}` = Feature name, lowercase, hyphenated

**Create subfolders:**
- `steps/` — For step instruction files
</action>

---

## CREATE DIALOG FILE

<action>
**Create main dialog file:**

File: `docs/F-Agent-Dialogs/{date}-{feature_slug}/{date}-{feature_slug}-dialog.md`

**Use template from:** `templates/dialog.template.md`

**Fill in:**
- Date: Today's date
- Agent: {agent_name}
- Feature: {feature_name}
- Specification: Link to {spec_path}
- Status: "In Progress"
</action>

---

## GATHER SETUP CONTEXT

<action>
**Read the specification file(s)** to understand:
- What needs to be implemented
- What already exists
- Technical requirements
</action>

<ask>**What's the tech stack for this project?**

Example: "React 19, Next.js 15, TypeScript, Tailwind CSS, Supabase"

Tech stack:</ask>

<action>Store tech_stack</action>

<ask>**What files are relevant to this implementation?**

List the key files that will be modified or referenced.

Relevant files:</ask>

<action>Store relevant_files</action>

<ask>**Are there any existing patterns to follow?**

Describe component structure, styling approach, state management, etc.

Patterns:</ask>

<action>Store patterns</action>

---

## UPDATE DIALOG FILE

<action>
**Fill in Setup Context section:**

- Project Context (tech stack)
- Relevant Files (table)
- Existing Patterns
- Current State (what exists)

**Fill in Purpose:**
- 1-3 sentences describing what this dialog accomplishes
</action>

---

## COMPLETION

<output>
✅ **Dialog initialized!**

**Created:**
- Folder: `docs/F-Agent-Dialogs/{date}-{feature_slug}/`
- Dialog file: `{date}-{feature_slug}-dialog.md`
- Steps folder: `steps/`

**Next:** Proceed to Step 2 to analyze scope and create step breakdown.

[A] Continue to Step 2: Analyze Scope
[B] Review the dialog file first
[C] Add more setup context

Choice:
</output>

---

## ROUTING

<action>
Based on user choice:
- [A] → Load and execute step-02-analyze-scope.md
- [B] → Show the dialog file contents
- [C] → Ask for additional context to add
</action>

---

_Agent Dialog Workflow — Step 1: Initialize Dialog_
