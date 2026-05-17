# Promotion Decision

Run ID: `2026-05-18-targeted-rerun-01`

Tested version: `v0.1.7`

Decision: `promote`

## Rationale

This run is valuable project evidence because it verifies the targeted Windows closeout fixes from `v0.1.7` and finds concrete follow-up issues.

Closed findings:

- Windows Codex loaded `v0.1.7`.
- Maintenance negative control stayed review-only and did not mutate installed files.
- Portfolio side-project trigger no longer exposed `superpowers:*` or host-specific helper skills.

Remaining findings:

- Multi-turn PRD draft behavior still promotes candidate target-user positioning too strongly before explicit user acceptance.
- README packaging docs should directly list `dist/` in the install zip exclusion rule.
- Evaluation package wording should distinguish “run-01 follow-up patch applied” from “patch verification rerun still needed”.
- `evals.json` version metadata can be confused with package version.

## Claim Boundary

Supported:

- `v0.1.7` closes the maintenance mutation and helper-skill visibility regressions in the tested Windows scenarios.
- `v0.1.7` packaging docs are mostly visible in Windows, including PowerShell packaging commands.

Unsupported:

- Install-candidate status.
- Release-grade validation.
- Baseline superiority.
- Fully closed user-gate drift for PRD draft generation.

## Required Follow-Up

Prepare a small follow-up patch before the next install-candidate attempt:

1. Directly list `dist/` in README packaging exclusions.
2. Clarify evaluation-package Next Evidence wording.
3. Clarify evals metadata as strict-suite version vs current package version.
4. Tighten PRD draft rules so candidate target users and MVP scope remain labeled as assumptions until accepted.
