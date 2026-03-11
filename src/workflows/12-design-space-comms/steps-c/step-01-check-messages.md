# Step 1: Check Messages

## Purpose
Check the agent's inbox for unread messages and display them in chat for the human to follow.

## Procedure

1. Call `check_agent_messages` (or HTTP POST to `agent-messages` with `action: "check"`)
   - Use configured `AGENT_ID`
   - Include broadcast messages (`include_broadcast: true`)
   - Filter by current project if set

2. If messages found:
   - Display in chat using the agent's dialog format (named after the current agent)
   - Show sender → recipient with `[from → to]` arrows
   - Group by thread if multiple messages in same thread
   - Highlight urgent messages first
   - Ask user: "Would you like me to respond to any of these?"

3. If no messages:
   - Report: "No unread messages."
   - Show connection status (realtime vs polling)

4. If connection fails:
   - Report the error to the user: "Could not check messages: {error}"
   - Suggest: "Please check the network connection or restart the session."

## Output Format

Name the dialog block after the current agent so the human always knows whose perspective they're seeing:

```
--- {AGENT_NAME}'s DESIGN SPACE ---

[saga → freya] "What color palette should we use for the dashboard?"
  5 min ago | thread: abc-123 | urgent/question

[dev-agent → Space] "Homepage build complete. Ready for review."
  2 hours ago | thread: def-456 | notification

---
Connection: realtime (live) | {count} unread
```

**Format rules:**
- `[sender → recipient]` — use "Space" when no specific recipient (broadcast)
- Content in quotes, single line preview
- Relative timestamp + thread ID + message type
- The human sees the full dialog and decides what to act on
