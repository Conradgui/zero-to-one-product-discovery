# v0.1.7 Targeted Windows Rerun Summary

Run ID: `2026-05-18-targeted-rerun-01`

## Purpose

This run verified whether the `v0.1.7` closeout patch addressed the issues found in the first Windows clean-install relay run.

## Result

| Metric | Result |
|---|---:|
| Targeted scenarios | 5 |
| Passed | 4 |
| Partial | 1 |
| Failed | 0 |
| Hard failures | 0 |
| Average score | 89 |
| Install candidate | false |

Interpretation: `v0.1.7` improved the Windows behavior and closed two important regressions, but it is still not an install candidate because user-gate drift remains partially open.

## What Passed

- Windows Codex confirmed the installed and loaded skill was `v0.1.7`.
- Maintenance review stayed review-only and did not mutate installed files.
- Portfolio side-project trigger entered Diagnostic Start without exposing `superpowers:*` or other host-specific helper skills.
- Packaging docs were visible enough to show PowerShell packaging and most package-boundary exclusions.

## Remaining Issues

1. User-gate drift is improved but not fully closed.
   The E2E PRD Draft did not become final and did not enter Roadmap or Implementation Plan, but it still wrote “first version focuses on career-switching programming learners” too strongly before explicit user acceptance.

2. Packaging docs should directly list `dist/`.
   README mentions the repo root contains `dist/`, but the install zip exclusion list should explicitly say not to include `dist/`.

3. Evaluation status wording needs cleanup.
   `evaluation-package.md` still says “Patch and rerun findings from run-01,” even though `v0.1.7` already applies the patch. It should now say “verify v0.1.7 follow-up patches.”

4. Eval metadata can be misunderstood.
   `evals.json` has `"version": "0.1.5"` because it represents the strict-suite version, but readers can misread it as the current package version.

## Recommendation

Promote this run as valuable evidence, then create a small follow-up patch. Do not mark `v0.1.7` as install candidate.

The next patch should focus on documentation clarity and a stronger PRD draft rule:

- candidate target users, MVP scope, and positioning must remain explicitly labeled as assumptions or options until accepted by the user;
- PRD Draft sections must not present suggested positioning as confirmed fact.

## Evidence Files

- `raw.md`
- `scored-report.json`
- `value-review.json`
- `promotion-decision.md`
