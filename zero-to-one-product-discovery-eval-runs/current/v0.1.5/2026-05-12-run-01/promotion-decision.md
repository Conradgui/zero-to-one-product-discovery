# Promotion Decision: 2026-05-12-run-01

## Decision

`promote`

## Destination

```text
zero-to-one-product-discovery-eval-runs/current/v0.1.5/2026-05-12-run-01/
```

## Reason

This run produced actionable evidence:

- 22 strict-suite scenarios were executed from an independent raw-generation subagent.
- No hard failures were found.
- One scenario failed: `package_boundary_eval_runs_not_installed`.
- The failure is product-relevant because it affects how the project preserves public GitHub evaluation evidence without bloating the installable skill package.
- Two additional improvement signals were found: minor vendor-boundary drift and PRD draft/review-ready scoring ambiguity.

## Required Next Action

Patch and rerun:

- `package_boundary_eval_runs_not_installed`
- `eval_value_gate_no_findings`
- `baseline_comparison_required_before_superiority_claim`
- `child_vendor_boundary`
- `negative_skill_maintenance_boundary`

Do not claim `v0.1.5` as install candidate until the failed scenario is fixed and rerun.
