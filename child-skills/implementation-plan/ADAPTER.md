---
name: implementation-plan
description: Use when product direction, planning artifacts, and design direction are confirmed and the main workflow needs decision-complete implementation tasks.
---

# Implementation Plan

## Role

Produce an implementation plan or implementation readiness review from confirmed planning artifacts.

## Required Input

- Confirmed PRD / roadmap / story context.
- Design direction if relevant.
- Technical constraints and known stack.
- Acceptance criteria.
- Verification expectations.
- Non-goals and boundaries.
- Expected output mode.

## Output Contract

- Ordered implementation tasks.
- Acceptance checks per task.
- Verification commands or scenarios.
- Risks, dependencies, and rollback notes when relevant.
- The highest-leverage blocking question for the current turn if planning artifacts are not ready.
- Decision Log / ADR candidates.
- Readiness signal.
- Context Resume Packet.

## Boundaries

- Do not plan implementation from unreviewed product artifacts.
- Do not introduce a stack or architecture unless already chosen.
- Do not skip verification planning.
- Do not ask multiple questions in one turn; return the next blocker and let the main workflow loop after the user answers.
