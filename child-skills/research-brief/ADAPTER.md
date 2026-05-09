---
name: research-brief
description: Use when the main zero-to-one workflow has evidence, notes, interviews, feedback, or market material that need synthesis before artifact generation.
---

# Research Brief

## Role

Synthesize supplied evidence into a bounded research brief. Separate evidence from assumptions before any PRD, roadmap, story, or implementation artifact is upgraded.

## Required Input

- Current stage.
- Confirmed facts.
- Working assumptions.
- Existing materials inspected.
- Unresolved questions.
- Risks and contradictions.
- Out-of-scope boundaries.
- Expected output mode.

## Output Contract

- Evidence inventory.
- Assumptions / unknowns / contradictions / gaps.
- Problem, job, or scenario hypotheses labeled by evidence status.
- The highest-leverage blocking question for the current turn if evidence is insufficient.
- Decision Log candidates.
- ADR candidates only when research exposes durable technical decisions.
- Readiness signal.
- Context Resume Packet.

## Boundaries

- Do not turn feedback directly into requirements.
- Do not declare a target user, MVP, or roadmap as final.
- Do not ask multiple questions in one turn; return the next blocker and let the main workflow loop after the user answers.
