# Promotion Decision: 2026-05-14-run-02

Decision: `promote`

Reason: this targeted rerun closes the package-boundary failure and vendor-boundary drift found in `2026-05-12-run-01`. It is valuable because it changes the release-readiness interpretation of the patch, even though it is not a full-suite validation.

Preserve:

- `raw.md`
- `scored-report.json`
- `value-review.json`
- `promotion-decision.md`

Do not claim:

- full 22-scenario suite pass after patch
- install-candidate status
- baseline superiority
- global-install trigger reliability

Next evidence needed:

1. Full strict-suite rerun if the project wants to mark v0.1.5 as install candidate.
2. Baseline-vs-skill A/B run before any superiority claim.
3. Fresh global-install trigger test before public install reliability claims.
