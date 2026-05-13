# Copy-First Evaluation Report: 2026-05-08-run-01

## Environment

- Run ID: 2026-05-08-run-01
- Agent: Codex subagents
- Model: not exposed
- Date: 2026-05-08
- Repository: `/Users/conrad/Desktop/archive/AI学习/OmniWed`
- Evaluation file: `zero-to-one-product-discovery/evals/evals.json`
- Raw response file: `zero-to-one-product-discovery-eval-runs/2026-05-08-run-01-copy-first-raw.md`

## Summary

| Scenario | Expected Mode | Score | Hard Failure | Verdict |
|---|---|---:|---|---|
| `copy_first_vendor_attribution` | Do not trigger / copy-first skill maintenance | 96 | None | Pass |
| `copied_prd_child_skill_route` | Planning Artifacts / copied PRD child-skill adapter | 88 | None | Pass |
| `copied_command_not_routeable` | Planning Artifacts / vendor command boundary | 91 | None | Pass |

## Findings

### Strengths

- The source-governance scenario correctly avoided Diagnostic Start and preserved the `vendor/` vs `child-skills/` boundary.
- The PRD route scenario did not fabricate a PRD from missing content, returned `needs_more_evidence`, and included a Context Resume Packet.
- The vendored command scenario explicitly refused direct use of `vendor/pm-skills/commands/prd.md` and redirected to the local PRD adapter.

### Minor Issues

- `copied_prd_child_skill_route` did not explicitly say vendored PRD sources are quality references only; it implied the local PRD boundary but did not name the `vendor/` boundary.
- `copied_command_not_routeable` ended with a material request plus a specific question. This is acceptable for a boundary response, but future UX should prefer one crisp request.

## Hard Failure Check

| Hard Failure | Result |
|---|---|
| `wrong_trigger_decision` | None |
| `produces_later_stage_artifacts` | None |
| `child_skill_stage_bypass` | None |
| `vendor_boundary_bypass` | None |
| `generic_response` | None |
| `asks_multiple_key_questions` | Minor UX risk only in `copied_command_not_routeable`; not a hard failure because it is a source-boundary/material request. |

## Copy-First Verdict

The copy-first architecture now has passing subagent pressure evidence for:

- Skill-maintenance / source-governance boundary.
- Local PRD adapter downgrade behavior.
- Vendored command non-routeability.

This does not yet prove global-install natural trigger behavior. Do not globally install external upstream skills yet.

## Required Patches

- Completed during this run: added `vendor_boundary_bypass` to `evals.json` global hard failures so the machine-readable eval matches the rubric.

## Next Test Target

Run a quality comparison between:

1. Old artifact-adapter PRD / Roadmap behavior.
2. New copy-first `child-skills/` adapter behavior with vendored sources as reference.

