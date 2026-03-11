# Design Space Interaction Principles

Design Space is shared implementation memory, task routing, presence, and reporting for WDS work.

## Core Behavior

Codex should use Design Space in four ways:

1. Search before starting major work.
2. Capture insights during implementation, not only at the end.
3. Report progress or blockers in the assigned thread when one exists.
4. Preserve reusable engineering knowledge for future agents.

## Search Before Build

Before a major task, search for:

- prior implementation patterns
- client feedback that constrains the work
- component experiences
- previous handoffs or verification results

If nothing useful exists, proceed and capture what is learned.

## Capture During Work

Capture when:

- a spec ambiguity is resolved
- code reveals a mismatch between docs and implementation
- a shared component pattern proves reusable
- a constraint blocks a naive implementation path
- an implementation decision will matter on future pages

## Project Customization

Add:

- project tag
- client name
- default topics
- thread reporting expectations
- local Design Space file references
