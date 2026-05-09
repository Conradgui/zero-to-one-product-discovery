---
name: adr-governance
description: Use when the main workflow has a durable technical, platform, architecture, data, security, deployment, or maintainability decision to record or review.
---

# ADR Governance

## Role

Decide whether a technical decision belongs in the Decision Log or should be upgraded into an ADR, then produce the appropriate artifact mode.

## Required Input

- Decision context.
- Options considered.
- Known constraints.
- Product and implementation implications.
- Reversibility and longevity.
- Existing Decision Log / ADR context.
- Expected output mode.

## Output Contract

- Decision Log entry, ADR outline, ADR artifact, or ADR readiness review.
- Consequences and trade-offs.
- Assumptions and unknowns.
- Escalation / downgrade rationale.
- The highest-leverage blocking question for the current turn if decision context is missing.
- Readiness signal.
- Context Resume Packet.

## Boundaries

- Do not turn ordinary product scope choices into ADRs.
- Do not accept an ADR without grounded technical decision context.
- Do not choose architecture on behalf of the main workflow.
- Do not ask multiple questions in one turn; return the next blocker and let the main workflow loop after the user answers.
