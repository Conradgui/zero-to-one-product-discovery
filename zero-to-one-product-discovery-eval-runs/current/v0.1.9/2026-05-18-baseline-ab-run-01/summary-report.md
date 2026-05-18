# v0.1.9 Baseline A/B Summary Report

Run ID: `2026-05-18-baseline-ab-run-01`

## Purpose

This run compares ordinary assistant behavior against the `zero-to-one-product-discovery` workflow on the same 10 early product discovery and boundary-control scenarios.

The goal is scenario-scoped measurement, not broad model superiority. The baseline is a controlled local baseline, so the result should be read as a structured comparison of workflow guidance versus ordinary response behavior in this environment.

## Method

The run follows the new `baseline-ab-template.md` and `baseline-ab-scoring-rubric.md`:

1. Select 10 paired scenarios.
2. Generate baseline raw responses without reading or invoking the skill.
3. Generate skill raw responses with `SKILL.md` available.
4. Score each pair using deterministic hard failures and a 100-point rubric.
5. Apply the Value Gate and preserve evidence only if it changes product or release understanding.

This design follows the same general direction as OpenAI's agent eval guidance around traces, graders, datasets, and eval runs; Anthropic's evaluation-tool pattern for side-by-side prompt comparison and rerunning eval suites after changes; and Google DeepMind's benchmark practice around standardized tasks, factual grounding, and held-out/private sets to reduce contamination.

## Aggregate Results

| Metric | Result |
|---|---:|
| Scenario count | 10 |
| Baseline average | 68.4 |
| Skill average | 95.7 |
| Average delta | +27.3 |
| Skill wins | 8 |
| Baseline wins | 0 |
| Ties | 2 |
| Skill win rate | 80% |
| Baseline hard failures | 6 |
| Skill hard failures | 0 |
| Supports scenario-scoped improvement | true |

## Scenario Results

| Scenario | Category | Baseline | Skill | Delta | Winner |
|---|---|---:|---:|---:|---|
| `p1_early_open_source_idea` | trigger_boundary | 55 | 94 | +39 | skill |
| `p2_portfolio_side_project` | trigger_boundary | 62 | 93 | +31 | skill |
| `p3_existing_prd_not_grounded` | evidence_grounding | 60 | 95 | +35 | skill |
| `n1_existing_mvp_small_change` | negative_control | 94 | 96 | +2 | tie |
| `n2_code_review` | negative_control | 92 | 95 | +3 | tie |
| `n3_skill_maintenance` | negative_control | 85 | 96 | +11 | skill |
| `b1_vendor_boundary` | child_skill_routing | 68 | 98 | +30 | skill |
| `b2_package_boundary` | package_boundary | 88 | 98 | +10 | skill |
| `s1_user_demands_full_artifacts` | stage_gate | 35 | 96 | +61 | skill |
| `u1_prd_draft_user_gate` | audit_user_gate | 45 | 96 | +51 | skill |

## Main Findings

1. The skill's largest measurable advantage is not generic helpfulness. It is governance under pressure: preventing premature PRD/Roadmap/Implementation Plan output when the user asks for it too early.
2. The skill materially improves boundary safety for `vendor/`, install zip exclusions, GitHub eval evidence, and skill-maintenance requests.
3. The skill improves PRD Draft user-gate behavior by keeping suggested target users, MVP scope, and positioning as candidate assumptions until user acceptance.
4. The baseline is already strong on narrow negative controls like code review and existing MVP UI bugfixes. This is useful: it narrows the claim to where the skill actually adds value.

## Claim Boundary

Supported:

- In this controlled local 10-scenario A/B, the skill outperformed the ordinary baseline on stage gates, boundary safety, and user-gate discipline.
- `v0.1.9` can preserve this as scenario-scoped Baseline A/B evidence.

Not supported:

- Release-grade validation.
- Production stability.
- Broad superiority over ordinary models.
- Cross-model superiority across OpenAI, Anthropic, or Google models.
- Long-term real-user workflow quality.

## Evidence Files

- `scenario-set.json`
- `baseline-raw.md`
- `skill-raw.md`
- `baseline-ab-scored-report.json`
- `value-review.json`
- `promotion-decision.md`

## Methodology References

- OpenAI Agent Evals: https://platform.openai.com/docs/guides/agent-evals
- OpenAI Trace Grading: https://platform.openai.com/docs/guides/trace-grading
- Anthropic Evaluation Tool: https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool
- Google DeepMind FACTS Grounding benchmark: https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/
