# /design-delivery — Deliver WDS Design to BMAD

Hand off completed WDS page specs to the BMAD PRD so coding agents find them automatically.

**Usage:** `/design-delivery` or `/design-delivery [page-name page-name ...]`

---

<design-delivery-steps>

  <constraints>
    - Never overwrite PRD content — only add design references. Existing text is untouched.
    - A page is deliverable when its spec file in D-UX-Design/ is non-empty and not marked Draft.
    - If the PRD has no matching section for a page: report it as unmatched, do not force-insert.
    - Do not ask questions mid-flow. Derive everything from files and arguments.
  </constraints>

  <step id="1-locate-artifacts">
    Find the WDS output folder. Check in order:
    1. `_bmad/wds/` (standard BMAD path)
    2. `_wds/` (legacy path)
    3. `docs/` or `design-process/` (custom root)

    From the output folder, locate:
    - **Spec files:** `{output_folder}/D-UX-Design/*.md` — exclude `00-*` index files
    - **Design log:** `_progress/00-design-log.md` — read Design Loop Status table to know which pages are approved

    Find the BMAD PRD. Check in order:
    1. `_bmad-output/docs/prd.md`
    2. `_bmad-output/prd.md`
    3. `{output_folder}/E-PRD/*.md`

    If no PRD found:
    ```
    ⚠️ No PRD found. Run /mimir to generate the PRD before delivering design.
    ```
    Stop.
  </step>

  <step id="2-inventory">
    Build a delivery inventory:

    For each spec file found:
    - Extract: page name (H1 heading), route (from spec frontmatter or `Route:` line), approval status (from design log)
    - Mark as: ✓ Approved / ⏳ In progress / ○ Not started

    If arguments were given: filter to only the named pages.
    If no arguments: show the full inventory and ask which to deliver:

    ```
    📦 Design Delivery — [Project Name]

    Available specs:
      ✓  [page-name]  ([route])   — approved
      ⏳  [page-name]  ([route])   — in progress
      ○  [page-name]  ([route])   — not started

    Which pages to deliver? (enter names or "all approved")
    ```

    Wait for selection. Then continue with only the selected pages.
  </step>

  <step id="3-match">
    For each selected page, find the matching section in the PRD:

    Match strategy (in order):
    1. Exact route match — PRD section contains the page's route string
    2. Name match — PRD section heading contains the page name (case-insensitive)
    3. Keyword match — PRD section contains 2+ words from the page name

    For each page: record match result (matched section heading + line number, or unmatched).
  </step>

  <step id="4-inject">
    For each matched page:

    Find the first occurrence of this pattern in the matched PRD section:
    - A line starting with `**Design spec:**` → overwrite it
    - If not found → append after the section heading (before the first bullet or paragraph)

    Insert exactly:
    ```
    **Design spec:** `{relative_path_to_spec_file}`
    ```

    Write the updated PRD.
  </step>

  <step id="5-handoff">
    Write a handoff file for Mimir at `_progress/mimir.md` so Mimir knows design is ready.

    Content:
    ```
    ## Wrapped
    [current date and time]

    ## Context
    Design delivery complete. [N] page specs injected into PRD.
    Pages: [comma-separated page names]
    PRD: [path to PRD]

    ## Next
    Run /mimir to plan and execute the build. Design specs are linked in the PRD — follow them.

    ## Learned
    None

    ## Spec Sync
    PRD updated with design spec references.
    ```

    Create `_progress/` if it doesn't exist.
  </step>

  <step id="6-report">
    Print the delivery summary:

    ```
    ── Design Delivery ───────────────────────────
    PRD: [path to PRD]

    Delivered:
      ✓  [page-name] → [PRD section heading]
      ✓  [page-name] → [PRD section heading]

    Unmatched (add manually):
      ⚠️  [page-name] — no PRD section found

    PRD updated. Coding agents will now find design specs automatically.
    ─────────────────────────────────────────────
    ```

    If all pages unmatched: suggest running `/mimir` to regenerate the PRD with WDS awareness.
  </step>

</design-delivery-steps>
