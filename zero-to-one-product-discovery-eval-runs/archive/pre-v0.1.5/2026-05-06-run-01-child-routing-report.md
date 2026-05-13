# Child Routing Evaluation Report: 2026-05-06-run-01

## Environment

- Run ID: 2026-05-06-run-01
- Agent: Codex subagent
- Model: not exposed
- Date: 2026-05-06
- Repository: `/Users/conrad/Desktop/archive/AI学习/OmniWed`
- Evaluation file: `zero-to-one-product-discovery/evals/evals.json`
- Rubric file: `zero-to-one-product-discovery/evals/eval-rubric-template.md`
- Raw response source: subagent notification in current Codex session

## Summary

| Scenario | Expected Mode | Score | Hard Failure | Verdict |
|---|---|---:|---|---|
| `heavy_advisor_requested` | Heavy Advisor | 92 | None | Pass |
| `child_prd_route_grounded` | PRD child-skill contract | 90 | None | Pass |
| `child_roadmap_route_ungrounded` | Roadmap decision-surface mode | 93 | None | Pass |
| `child_research_brief_feedback` | Research Brief child-skill contract | 91 | None | Pass |
| `child_adr_escalation_platform` | ADR child-skill contract | 90 | None | Pass |
| `child_multi_handoff_ux_consistency` | Multi-child routing review | 88 | None | Pass |
| `artifact_source_boundary` | Do not trigger / skill-authoring boundary | 62 | `wrong_trigger_decision` | Fail |

## Aggregate

- Average score: 86.6
- Median score: 90
- Lowest score: 62
- Hard failure count: 1
- Suite pass threshold: 85
- Install candidate threshold: 90 and 0 hard failures
- Install candidate: No

## Findings

### Strengths

- Child-skill routing worked across PRD, Roadmap downgrade, Research Brief, ADR, and multi-child handoff scenarios.
- Readiness signals appeared consistently in child routing outputs.
- The model preserved main workflow authority for grounded and ungrounded artifact requests.
- Heavy Advisor stayed in outline / decision-surface mode and avoided final artifacts from vague input.

### Blocking Failure

`artifact_source_boundary` should not trigger `zero-to-one-product-discovery`, because the prompt is about modifying this skill and source-governance boundaries. The raw response rejected direct copying, which is good, but it still used Planning Artifacts / Source Boundary framing, produced a Context Resume Packet, and asked a main-skill style confirmation question.

Impact:

- The main skill can still bleed product-discovery UX into skill-authoring/source-governance requests.
- This weakens the boundary between building the discovery workflow and using the discovery workflow.

Required patch:

- Strengthen `SKILL.md` Do Not Use rules for meta-work on this skill, external source integration, skill authoring, and source governance.
- Add a source-governance boundary note to `source-attribution.md` or a dedicated reference.
- Tighten eval hard failures for `artifact_source_boundary` to include discovery-style Context Resume Packet or product-discovery readiness signal.

### Non-blocking Concerns

- `child_multi_handoff_ux_consistency` was safe, but long. Future UX tuning should keep route checks more compact when no source material is provided.
- Several child outputs used rich artifact bodies in the raw response. That is acceptable for grounded PRD and ADR surfaces, but the main skill should keep a concise routing note before long specialist output.

## Scenario Results

### `heavy_advisor_requested`

- Score: 92
- Hard failure: None
- Evidence: Warned about context cost and assumption hardening; produced outlines and decision surfaces; avoided final PRD/Roadmap/Milestone/ADR.
- Patch needed: None.

### `child_prd_route_grounded`

- Score: 90
- Hard failure: None
- Evidence: Routed to PRD child capability, preserved confirmed problem/MVP/risk/non-goal, returned readiness signal and Context Resume Packet.
- Patch needed: None.

### `child_roadmap_route_ungrounded`

- Score: 93
- Hard failure: None
- Evidence: Refused committed three-month roadmap, downgraded to decision surface, asked one high-leverage question.
- Patch needed: None.

### `child_research_brief_feedback`

- Score: 91
- Hard failure: None
- Evidence: Treated feedback as evidence, separated solution requests from problem signal, avoided requirements.
- Patch needed: None.

### `child_adr_escalation_platform`

- Score: 90
- Hard failure: None
- Evidence: Correctly escalated architecture/privacy/integration decision to ADR-ready surface while avoiding accepted decision.
- Patch needed: None.

### `child_multi_handoff_ux_consistency`

- Score: 88
- Hard failure: None
- Evidence: Enforced sequential route gates and blocked Implementation Plan until material review; output was longer than necessary.
- Patch needed: Optional UX tightening.

### `artifact_source_boundary`

- Score: 62
- Hard failure: `wrong_trigger_decision`
- Evidence: Correctly rejected direct copying, but used discovery workflow framing and Context Resume Packet for a skill-authoring/source-governance request.
- Patch needed: Strengthen meta-work boundary and eval hard failures.

## Required Follow-up

1. Patch source-governance / skill-authoring boundary.
2. Re-run `artifact_source_boundary` and `child_external_command_minihub_boundary`.
3. Do not globally install external skills until boundary scenarios pass with 0 hard failures.
