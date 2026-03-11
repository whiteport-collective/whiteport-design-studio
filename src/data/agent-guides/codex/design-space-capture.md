# Design Space Capture Guide - Codex

Design Space is shared implementation memory, coordination, and reporting for WDS work.

## Search Before Major Work

Before a major task, search for:

- prior implementation patterns
- component experiences
- client feedback that constrains the work
- previous handoffs or verification results

If nothing useful exists, proceed and capture what is learned.

## Capture During Work

Capture when:

- a spec ambiguity is resolved
- implementation reveals drift between docs and code
- a reusable component pattern proves sound
- a technical constraint changes the implementation path
- a verification result is likely to help future agents

## Recommended Categories

- `methodology`
- `successful_pattern`
- `component_experience`
- `agent_experience`
- `client_feedback`

## Reporting Rule

If a Design Space thread exists for the task:

- post understanding before major implementation when scope is uncertain
- post blockers immediately
- post verification findings when done

## Practical Rule

Do not wait to be asked whether something should be remembered.
If the learning will improve future WDS implementation work, capture it.
