# /social-publish — Publish Social Media Posts via Browser

Schedules and publishes posts to LinkedIn, Facebook, and Instagram using the Chrome DevTools MCP. Reads post content from a markdown post file. Use when publishing or scheduling social media content across platforms.

**Usage:** `/social-publish [path/to/post.md]`

---

<social-publish-steps>

  <constraints>
    - Always use Chrome DevTools MCP (`mcp__plugin_chrome-devtools-mcp_chrome-devtools__*`). Never use Puppeteer — it runs an isolated browser with no login session.
    - UIDs expire after every page interaction. Always take a fresh snapshot before each click.
    - Never reuse a UID from a previous snapshot — the page may have re-rendered.
    - When fill() doesn't work on a field: click() to focus it, use Ctrl+A to select all, then type_text() to replace.
    - If Chrome DevTools MCP fails to connect: delete the LOCK file at `C:\Users\marte\.cache\chrome-devtools-mcp\chrome-profile\Default\LOCK`, then retry.
    - Snapshots are large. Save to file with `filePath` param and grep for relevant UIDs rather than reading the full output.
    - Scheduled posts cannot receive first-comment automation — note it and do it manually after the post goes live.
  </constraints>

  <step id="0-read-post">
    Read the post file. Extract:
    - **LinkedIn text** (under `## LinkedIn → ### Post`)
    - **Facebook text** (under `## Facebook → ### Post`)
    - **Instagram text** (under `## Instagram → ### Post`)
    - **Image filename** (`Bild:` frontmatter field)
    - **Image path** — same folder as the post file
    - **Scheduled datetime** (`Datum:` frontmatter field)
    - **First comment content** for each platform (under `### Första kommentar`)

    Report what was found before proceeding.
  </step>

  ---

  ## Tool: LinkedIn

  <step id="linkedin-1-navigate">
    Navigate to LinkedIn:

    ```
    navigate_page → url: "https://www.linkedin.com/feed/"
    ```

    Take snapshot. Confirm the feed is visible and the user is logged in.
  </step>

  <step id="linkedin-2-open-composer">
    Find and click the post composer. In the snapshot, look for:
    - A button or input labeled **"Start a post"** / **"Starta ett inlägg"**
    - Or the text field at the top of the feed

    Click it to open the full post composer dialog.
  </step>

  <step id="linkedin-3-type-text">
    Take snapshot. Find the **textbox** in the composer dialog (role: `textbox`, multiline).

    Type the LinkedIn post text:
    ```
    type_text → uid: [textbox uid], text: [linkedin_text]
    ```

    Do NOT use fill() — LinkedIn's editor is a contenteditable and fill() will replace without proper rendering. Use type_text() which simulates keystroke-by-keystroke input.
  </step>

  <step id="linkedin-4-upload-image">
    Take snapshot. Find the image attach button — labeled **"Lägg till media"** or the photo/image icon in the composer toolbar.

    Upload the image:
    ```
    upload_file → uid: [image button uid], filePath: [absolute path to image file]
    ```

    Wait for the image preview to appear in the composer. Take snapshot to confirm.
  </step>

  <step id="linkedin-5-open-schedule">
    Take snapshot. Find the **"Nästa"** button (bottom right of composer).

    Click it:
    ```
    click → uid: [Nästa button uid]
    ```

    A scheduling options dialog appears. Take snapshot.

    Find and click the schedule option — labeled **"Schemalägg för senare"** or the clock/calendar icon.
  </step>

  <step id="linkedin-6-set-date">
    Take snapshot. The scheduling dialog shows a calendar and time field.

    To set the date:
    1. Click the date field or the forward arrow to navigate to the target month
    2. Find the target date button — labeled e.g. **"Monday, 27 April 2026"** (aria-label)
    3. Click it:
       ```
       click → uid: [date button uid]
       ```

    Do NOT use fill() on the date text field — the calendar widget does not respond to direct text input.
  </step>

  <step id="linkedin-7-set-time">
    Take snapshot. Find the time input — a combobox or spinbutton labeled with the current time.

    To set time:
    1. Click the time field to focus it
    2. Select all existing value: press Ctrl+A
    3. Type the new time:
       ```
       type_text → text: "07:00"
       ```

    Ctrl+A is required — if you just type, the value appends to the existing time instead of replacing it.

    Take snapshot to confirm the time field shows the correct value.
  </step>

  <step id="linkedin-8-schedule">
    Take snapshot. Find and click **"Schemalägg"** (the confirm schedule button).

    ```
    click → uid: [Schemalägg button uid]
    ```

    A confirmation message appears: **"Inlägget har schemalagts"** (Post has been scheduled).

    Take snapshot to confirm. Update the post file status to `scheduled`.
  </step>

  <step id="linkedin-9-first-comment-note">
    LinkedIn does not allow scheduling a first comment on a scheduled post.

    Note for follow-up:
    ```
    ⚠️ First comment must be added manually after the post goes live.
    Content:
    [first comment text from post file]
    ```
  </step>

  ---

  ## Tool: Facebook Business Suite (Meta)

  Meta Business Suite schedules posts to both Facebook and Instagram in one flow, with per-platform text customization.

  <step id="meta-1-navigate">
    Navigate to the Meta Business Suite post composer:

    ```
    navigate_page → url: "https://business.facebook.com/latest/composer/"
    ```

    Take snapshot. If a popup or dialog appears (e.g. onboarding, notifications), dismiss it:
    - Find a **"Stäng"** / **"Close"** / **"×"** button
    - Click it before proceeding
  </step>

  <step id="meta-2-upload-image">
    Take snapshot. Find the photo/media upload area — a button labeled **"Foto/Video"** or **"Ladda upp"** / **"Upload from desktop"**.

    Upload the image:
    ```
    upload_file → uid: [upload button uid], filePath: [absolute path to image file]
    ```

    Wait for image preview to appear. Take snapshot to confirm only one image is uploaded.

    If the image appears twice (duplicate): find the **"Ta bort"** / **"Remove photo"** button on the second copy and click it.
  </step>

  <step id="meta-3-customize-platforms">
    Take snapshot. Find and enable the toggle **"Anpassa inlägg för varje plattform"** / **"Customize post for each platform"**.

    This reveals separate tabs for Facebook and Instagram. Click it if not already enabled.
  </step>

  <step id="meta-4-facebook-text">
    Take snapshot. The **"Facebook"** tab should be active by default.

    Find the text input area (role: `textbox` or contenteditable). Click it to focus.

    Type the Facebook post text:
    ```
    type_text → uid: [textbox uid], text: [facebook_text]
    ```
  </step>

  <step id="meta-5-instagram-text">
    Take snapshot. Find the **"Instagram"** tab and click it.

    Find the Instagram text input. Click it to focus, then type:
    ```
    type_text → uid: [textbox uid], text: [instagram_text]
    ```
  </step>

  <step id="meta-6-open-schedule">
    Take snapshot. Find the schedule toggle or button — labeled **"Schemalägg"** / **"Set date and time"** or a calendar icon near the publish button.

    Enable it. A date/time row appears for each platform (Facebook and Instagram).
  </step>

  <step id="meta-7-set-date">
    Take snapshot. Find the date field for Facebook (and separately for Instagram if shown independently).

    To set the date:
    1. Click the date input field to open the calendar widget
    2. Navigate to the correct month using the **"Nästa månad"** / forward arrow if needed
    3. Click the target day button in the calendar grid

    Repeat for Instagram if the date fields are independent.

    Do NOT use fill() on date text fields — they do not respond to direct text input. Use the calendar widget clicks only.
  </step>

  <step id="meta-8-set-time">
    Take snapshot. Find the time spinbuttons — typically hour and minute fields (role: `spinbutton`).

    For each field:
    1. Click to focus
    2. Select all with Ctrl+A
    3. Type the value (e.g. "07" for hour, "00" for minutes)

    Confirm the time shows correctly in the snapshot.
  </step>

  <step id="meta-9-schedule">
    Take snapshot. Find and click the **"Schemalägg"** / **"Schedule"** publish button.

    ```
    click → uid: [Schedule button uid]
    ```

    A confirmation popup appears confirming the post is scheduled. Take snapshot to confirm.

    Update the post file status line to:
    ```
    **Status:** scheduled — LinkedIn + FB + IG [day] [date] [time] CEST
    ```
  </step>

  ---

  ## Tool: LinkedIn Messaging

  <step id="linkedin-msg-1-navigate">
    Navigate to LinkedIn messaging:

    ```
    navigate_page → url: "https://www.linkedin.com/messaging/"
    ```

    Take snapshot. The inbox is visible with conversation list on the left.
  </step>

  <step id="linkedin-msg-2-find-conversation">
    In the snapshot, search for the recipient's name in the conversation list.

    Click their conversation to open it:
    ```
    click → uid: [conversation list item uid]
    ```

    Take snapshot to confirm the conversation thread is visible.
  </step>

  <step id="linkedin-msg-3-type-message">
    Take snapshot. Find the compose field — a `textbox` labeled **"Skriv meddelande …"** (multiline, focused).

    Clear any existing content first:
    1. Click the textbox to focus it
    2. Press Ctrl+A to select all
    3. Then type the message:
       ```
       type_text → uid: [textbox uid], text: [message]
       ```

    Take snapshot to confirm the textbox shows the correct message content.
  </step>

  <step id="linkedin-msg-4-send">
    Take snapshot. Find the **"Skicka"** (Send) button — a button near the compose field, separate from the **"Öppna sändalternativ"** dropdown arrow.

    Click it:
    ```
    click → uid: [Skicka button uid]
    ```

    Take snapshot to confirm the message now appears as a new bubble in the conversation thread. The conversation list on the left should show **"Du: [message preview]"** as the latest entry.
  </step>

  ---

  <step id="final-report">
    Report what was published:

    ```
    ── Social Publish ────────────────────────────
    ✓  LinkedIn     — scheduled [datetime]
    ✓  Facebook     — scheduled [datetime]
    ✓  Instagram    — scheduled [datetime]

    ⚠️  First comment (LinkedIn) — add manually after post goes live:
    [first comment content]

    Post file status updated.
    ─────────────────────────────────────────────
    ```
  </step>

</social-publish-steps>
