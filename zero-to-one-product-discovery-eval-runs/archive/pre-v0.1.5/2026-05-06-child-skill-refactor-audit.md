# Child-Skill Refactor Audit: 2026-05-06

> Historical note: this audit reflects the state on 2026-05-06. Later copy-first work superseded several remaining-work items by adding `vendor/` source snapshots and `child-skills/` local adapters. Use `2026-05-06-project-status-handoff.md` current-state section for the latest status.

## Document Purpose

This audit checks whether the hub-and-spoke refactor stayed aligned with the user's stated goal: make `zero-to-one-product-discovery` the main workflow controller while specialist child skills or agents handle higher-quality artifacts.

## Update Rules

- Append future audits instead of overwriting this record.
- Separate implemented facts from remaining work.
- Use this audit to prevent drift back toward a single oversized artifact-template skill.

## Plan Completion Check

| Plan Item | Status | Evidence |
|---|---|---|
| External project deep research | Implemented as source evaluation note | `references/source-evaluation.md` ranks Product-Manager-Skills, pm-skills, agent-skills, and awesome-copilot by quality role and UX role. |
| Child skill capability map | Implemented as contract matrix | `references/artifact-adapters.md` defines Research Brief, PRD, Roadmap, Milestone, User Stories, Acceptance Criteria, ADR, Mermaid, Implementation Plan, and Review. |
| Main / child boundary protocol | Implemented as routing layer | `references/planning-artifacts.md` defines route, downgrade, escalation, handoff packet, readiness signals, and UX rules. |
| Main skill orchestration positioning | Implemented | `SKILL.md` now states that the main skill controls stage gates, context continuity, child-skill routing, and UX consistency. |
| UX consistency rules | Implemented | `planning-artifacts.md` defines routing note, per-turn highest-leverage question rule, assumption labels, Context Resume Packet, and personal open-source constraint preservation. |
| Evaluation updates | Implemented structurally | `evals.json`, `eval-rubric-template.md`, and `claude-code-pressure-test-protocol.md` include child-skill routing checks and hard failure coverage. |
| External candidate structural review | Implemented | `references/child-skill-integration-blueprint.md` maps Product-Manager-Skills and agent-skills candidates to integration modes and gates. |
| Command mini-hub boundary | Implemented | `SKILL.md`, `artifact-adapters.md`, `planning-artifacts.md`, and `evals.json` now prevent external command mini-hubs from becoming unwrapped child skills. |
| Grounding contract | Implemented | `planning-artifacts.md` defines minimum grounded inputs for each artifact route. |
| First child-routing pressure report | Implemented | `2026-05-06-run-01-child-routing-report.md` records one hard failure in source-governance boundary and passing child-routing behavior elsewhere. |
| Source-governance boundary patch | Implemented after failure | `SKILL.md`, `source-attribution.md`, and `evals.json` now state that skill-maintenance/source-governance requests must not trigger discovery framing. |
| First local wrappers | Implemented | `child-skill-wrappers.md` adds Problem Framing, ADR Governance, and Context Handoff wrappers. |
| Wrapper pressure test | Implemented | `2026-05-07-run-01-wrapper-report.md` found a per-turn question UX failure; `2026-05-07-run-02-wrapper-rerun-report.md` confirms the rerun passes. |

## Remaining Work

The plan's structural refactor is implemented, but these items are not yet completed:

1. Superseded: concrete external source has since been vendored into `vendor/`, and local routeable adapters now exist in `child-skills/`.
2. No comparison has been run between old artifact output and the new child-skill contract output quality.
3. No global installation or natural trigger test has been run after the architecture shift.
4. Superseded in part: pm-skills and awesome-copilot were later re-cloned and selectively copied into `vendor/`; deeper quality comparison is still pending.

## Drift Risks

| Risk | Monitoring Rule |
|---|---|
| Main skill grows back into a huge artifact-template file | Keep full artifact bodies out of `SKILL.md`; route through contracts. |
| Child skills bypass stage gates | Every child output must include readiness signal and be accepted or downgraded by the main skill. |
| External projects dominate local workflow | External source rules never override Diagnostic Start, MVP Hypothesis, Decision Log / ADR, or Context Resume Packet gates. |
| UX fragments across child skills | Use one routing note, per-turn highest-leverage question rule, consistent labels, and the same Context Resume Packet shape. |
| Evaluation lags behind architecture | Run child-skill routing pressure tests before claiming installation or release readiness. |

## Recommended Next Action

Historical recommendation: run a child-skill routing pressure test, then decide integration mode. Current order is superseded by the 2026-05-09 handoff: finish document/status cleanup and main workflow rule convergence first, defer new test execution until skill writing is complete.
