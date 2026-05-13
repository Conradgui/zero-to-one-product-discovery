# Child-Skill Routing Static Self-Eval: 2026-05-06

## Document Purpose

This same-session static review checks whether the written skill rules cover the new hub-and-spoke routing behavior. It is not an independent model pressure test and must not be treated as release-grade evidence.

## Update Rules

- Do not overwrite this review with later model runs.
- Keep future raw model responses and scored reports in separate files.
- If a later run contradicts this review, trust the later run's raw evidence.

## Scope

Reviewed files:

- `zero-to-one-product-discovery/SKILL.md`
- `zero-to-one-product-discovery/references/workflow.md`
- `zero-to-one-product-discovery/references/planning-artifacts.md`
- `zero-to-one-product-discovery/references/artifact-adapters.md`
- `zero-to-one-product-discovery/evals/evals.json`
- `zero-to-one-product-discovery/evals/eval-rubric-template.md`
- `zero-to-one-product-discovery/evals/claude-code-pressure-test-protocol.md`

## Checklist

| Requirement | Status | Evidence |
|---|---|---|
| Main skill owns orchestration | Covered | `SKILL.md` and `planning-artifacts.md` state that the main workflow controls stage gates, routing, downgrade, escalation, and readiness acceptance. |
| Child skills cannot jump stages | Covered | `artifact-adapters.md` prohibits child skills from choosing the next workflow stage; `evals.json` adds `child_skill_stage_bypass`. |
| Universal handoff packet exists | Covered | `artifact-adapters.md` and `planning-artifacts.md` define current stage, facts, assumptions, unresolved questions, risks, materials, boundaries, and expected output mode. |
| Universal output contract exists | Covered | `artifact-adapters.md` requires evidence status, assumptions, blockers, Decision Log / ADR candidates, readiness signal, and Context Resume Packet. |
| UX consistency is explicit | Covered | `planning-artifacts.md` defines routing note, one-question rule, consistent labels, Context Resume Packet, and preservation of personal open-source constraints. |
| Heavy Advisor does not finalize ungrounded artifacts | Covered | `SKILL.md`, `workflow.md`, and `planning-artifacts.md` require outlines / decision surfaces / assumption clearings unless grounded. |
| Evaluation covers child routing | Covered structurally | `evals.json` adds PRD routing, roadmap downgrade, research synthesis, ADR escalation, and multi-child handoff scenarios. |
| Rubric covers child routing | Covered | `eval-rubric-template.md` defines scoring mappings and hard failures for child-skill routing scenarios. |
| Protocol checks child bypass | Covered | `claude-code-pressure-test-protocol.md` includes `child_skill_stage_bypass`. |

## Scenario Coverage Review

| Scenario | Expected Route | Static Coverage Judgment |
|---|---|---|
| `child_prd_route_grounded` | PRD child-skill contract | Covered by PRD contract prerequisites and final artifact allowance after grounding. |
| `child_roadmap_route_ungrounded` | Roadmap decision-surface mode | Covered by roadmap downgrade rules and prohibition on dated commitments from vague input. |
| `child_research_brief_feedback` | Research Brief contract | Covered by evidence / opinion / assumption / contradiction / gap separation and feedback-not-requirements rule. |
| `child_adr_escalation_platform` | ADR child-skill contract | Covered by ADR escalation criteria for architecture, privacy, integration, and maintainability. |
| `child_multi_handoff_ux_consistency` | Multi-child routing review | Covered by readiness signals, sequential route gates, and UX consistency rules. |

## Findings

### No Blocking Gaps Found In Written Rules

The written rules now support the requested architecture: main workflow first, specialist child skills second, with explicit downgrade and readiness controls.

### Important Remaining Evidence Gap

This review only proves that the rules exist. It does not prove a fresh model will follow them. The next validation must generate raw responses against the new child-skill scenarios and score them with the updated rubric.

## Recommended Next Test Run

Run a new pressure test with these priority scenarios:

1. `child_prd_route_grounded`
2. `child_roadmap_route_ungrounded`
3. `child_research_brief_feedback`
4. `child_adr_escalation_platform`
5. `child_multi_handoff_ux_consistency`
6. `heavy_advisor_requested`
7. `artifact_source_boundary`

Expected output files:

- `zero-to-one-product-discovery-eval-runs/YYYY-MM-DD-run-XX-child-routing-raw.md`
- `zero-to-one-product-discovery-eval-runs/YYYY-MM-DD-run-XX-child-routing-report.md`
