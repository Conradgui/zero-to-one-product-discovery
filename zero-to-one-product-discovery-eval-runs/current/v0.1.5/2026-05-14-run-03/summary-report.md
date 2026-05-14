# v0.1.5 Run 03 Summary Report

Run ID: `2026-05-14-run-03`

## Purpose

This run verifies whether the patched `v0.1.5` skill passes the full 22-scenario strict suite after the fixes from `2026-05-12-run-01` and the targeted rerun in `2026-05-14-run-02`.

The run specifically checks that:

- package/eval evidence boundaries remain clear;
- `vendor/` remains a source snapshot and not an active route target;
- PRD output can be a draft without being mislabeled as `final` or `review-ready`;
- multi-agent Controller / Producer / Auditor boundaries hold under pressure;
- user gates, Runtime Workbench limits, and evidence grounding are preserved.

## Evaluation Method

The run follows the project evaluation protocol:

- Protocol: `zero-to-one-product-discovery/evals/claude-code-pressure-test-protocol.md`
- Scenario suite: `zero-to-one-product-discovery/evals/evals.json`
- Rubric: `zero-to-one-product-discovery/evals/eval-rubric-template.md`
- Report schema: `zero-to-one-product-discovery/evals/eval-report.schema.json`
- Value-review schema: `zero-to-one-product-discovery/evals/value-review.schema.json`

Execution used the five-pass process:

1. Raw response generation from `SKILL.md` and `scenarios-lite.json`.
2. Deterministic checks against scenario-specific checks.
3. Rubric grading against the structured scorecard.
4. Evidence Value Review.
5. Promotion decision.

Raw generation was performed by a Codex worker subagent. This is enough for full-suite regression evidence, but it is not a clean installed-skill environment.

## Aggregate Result

| Metric | Result |
|---|---:|
| Scenario count | 22 |
| Passed scenarios | 22 |
| Failed scenarios | 0 |
| Hard failures | 0 |
| Average score | 93.73 |
| Median score | 94 |
| Lowest score | 90 |
| Suite pass | true |
| Install candidate | false |

Interpretation: the patched full strict suite passed. This supports core regression confidence for `v0.1.5`, but it does not justify an install-candidate claim because clean install / natural trigger behavior has not been tested.

## Scenario Results

| Scenario | Category | Risk | Score | Verdict | Hard Failures |
|---|---|---|---:|---|---:|
| `trigger_explicit_zero_idea` | trigger_boundary | medium | 96 | pass | 0 |
| `trigger_implicit_open_source_resume` | trigger_boundary | medium | 95 | pass | 0 |
| `negative_existing_mvp_small_change` | negative_control | high | 94 | pass | 0 |
| `negative_skill_maintenance_boundary` | negative_control | high | 91 | pass | 0 |
| `stage_gate_user_demands_full_artifacts` | stage_gate | critical | 96 | pass | 0 |
| `stage_gate_prd_to_implementation_too_early` | stage_gate | critical | 94 | pass | 0 |
| `evidence_existing_prd_contradictions` | evidence_grounding | high | 95 | pass | 0 |
| `evidence_user_claims_without_proof` | evidence_grounding | high | 94 | pass | 0 |
| `child_prd_grounded_route` | child_skill_routing | medium | 93 | pass | 0 |
| `child_roadmap_ungrounded_downgrade` | child_skill_routing | high | 94 | pass | 0 |
| `child_vendor_boundary` | child_skill_routing | high | 92 | pass | 0 |
| `multi_agent_controller_audit_pass_not_acceptance` | multi_agent_orchestration | critical | 95 | pass | 0 |
| `multi_agent_producer_metric_invention` | multi_agent_orchestration | critical | 94 | pass | 0 |
| `multi_agent_workbench_full_history` | multi_agent_orchestration | critical | 94 | pass | 0 |
| `audit_user_gate_skip_to_implementation` | audit_user_gate | critical | 95 | pass | 0 |
| `audit_adr_condition_gate` | audit_user_gate | high | 93 | pass | 0 |
| `multi_turn_conflicting_facts` | multi_turn_continuity | high | 95 | pass | 0 |
| `context_economy_no_template_dump` | context_economy | medium | 96 | pass | 0 |
| `negative_narrow_bugfix` | negative_control | high | 94 | pass | 0 |
| `package_boundary_eval_runs_not_installed` | negative_control | medium | 91 | pass | 0 |
| `eval_value_gate_no_findings` | context_economy | medium | 90 | pass | 0 |
| `baseline_comparison_required_before_superiority_claim` | negative_control | medium | 91 | pass | 0 |

## Key Findings

### Package Boundary

`package_boundary_eval_runs_not_installed` passed. The response preserved the distinction between GitHub project evidence and the installable skill zip.

Remaining watchpoint: future runs should continue checking for precise wording around valuable promoted eval-runs, because vague evidence-language can cause packaging or release-note drift.

### Vendor Boundary

`child_vendor_boundary` passed. The response rejected direct routing to `vendor/` and kept local `child-skills/` adapters as the active routeable surface.

Remaining watchpoint: the answer included a maintenance follow-up question. This was acceptable because it did not ask PRD readiness or product-discovery questions, but the boundary should stay concise.

### PRD Draft / Final Boundary

`child_prd_grounded_route` passed. The response produced a PRD draft, marked success-metric measurement as unresolved, and did not label the artifact as `final` or `review-ready`.

This closes the run-01 ambiguity where PRD draft, review-ready PRD, and final PRD were not scored distinctly enough.

## Improvement Directions

- Run clean install / natural trigger validation before calling `v0.1.5` an install candidate.
- Run a multi-turn end-to-end simulation through Research Brief -> PRD -> Roadmap -> Implementation Plan readiness.
- Run baseline-vs-skill A/B testing before making any superiority claim over ordinary model behavior.
- Continue watching evidence-governance wording around `promote`, `minimal-note`, and `discard-full-run`.

## Supported Claims

This run supports these claims:

- The patched `v0.1.5` full strict suite passed across all 22 scenarios.
- The PRD draft/final boundary is covered by fresh full-suite evidence.
- Package and vendor boundary fixes remained stable after the full-suite rerun.
- No hard failures were observed in this run.

## Unsupported Claims

This run does not support these claims:

- `v0.1.5` is an install candidate.
- clean global-install trigger behavior is reliable.
- the skill is release-grade validated.
- the skill is proven superior to ordinary no-skill model behavior.

## Evidence Index

- `raw.md`: raw responses generated before scoring.
- `scenarios-lite.json`: prompt-only scenario input used for raw generation.
- `raw-generation-prompt.md`: prompt used to instruct the raw-generation subagent.
- `scored-report.json`: machine-readable structured scoring report.
- `value-review.json`: machine-readable Evidence Value Review.
- `promotion-decision.md`: promotion decision and claim boundary.
