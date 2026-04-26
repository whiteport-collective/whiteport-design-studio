---
name: scenario-conversation-pattern
description: How to walk through UX Scenarios conversationally — naming screens, pushing for specificity, confirming steps, keeping the emotional arc alive.
---

# Scenario Conversation Pattern

Loaded during scenario walkthroughs. One screen at a time, always forward.

---

## The walking pattern

For each screen in the flow:

1. **Name it** — give the screen a clear, specific name ("Booking Confirmation", not "Page 3")
2. **Describe it** — what does the user SEE when they land here? The dominant element, not a full inventory
3. **State the action** — what does the user DO? (clicks, fills, reads, decides, waits)
4. **Name what comes next** — the next screen or decision point
5. **Confirm** — "Does this feel right, or does something happen differently here?"

Always wait for the answer before moving to the next screen.

---

## Push for specificity

Vague steps create vague designs. Push when you get generic answers:

- "What does [Name] actually see when they land here?" — not "a form" but the headline, the CTA, the dominant visual
- "What's the most important thing on this screen for [Name]?" — forces prioritization
- "Is the path obvious, or could [Name] get lost here?" — reveals navigation decisions
- "What is [Name] feeling at this moment?" — keeps the emotional arc alive
- "What could go wrong here that we want to protect [Name] from?" — surfaces edge cases early

---

## Keeping the emotional arc

The persona arrived with an emotional state (from Usage Context). The scenario should show that state shifting as they move through the product toward their goal.

Name the emotional shift as you walk: "At this point [Name] is still nervous — the confirmation page needs to resolve that."

The final screen should show the persona reaching their primary positive driving force goal. The emotional arc is complete when the persona feels what they were moving toward.

---

## Branching

Scenarios are sunshine paths — no branching within a scenario.

If a branch comes up:
- Take the primary path (the happy path where everything works)
- Note the branch: "We'll design the error/edge case separately — out of scope for this scenario"
- Don't design for failures yet. One linear flow first.

If a branch is so important the user keeps returning to it: finish the primary scenario, then open a second scenario for the alternative flow.

---

## Confirmation pattern

Before calling Scenario Writer, summarize the complete screen list:

```
[Scenario title] — [Archetype name]
1. [Screen name] — [one-line description]
2. [Screen name] — [one-line description]
...
[N]. [Screen name] — ✓ [how the goal is achieved]

Does this capture the flow correctly?
```

Wait for explicit confirmation. Adjust if needed. Then call the writer.

---

## Signs the scenario is working

- Each screen has a specific name that a developer could use as a route name
- The emotional arc is visible from first screen to last
- The flow follows logic — each screen is reachable from the previous one
- The final screen connects to the persona's primary positive driving force

## Signs the scenario needs more work

- Screen names are generic ("Dashboard", "Results", "Page")
- Steps are skipped — the user arrives somewhere without a clear path
- The flow doesn't connect to what the persona was moving toward
- More than ~15 screens in one scenario — consider splitting
