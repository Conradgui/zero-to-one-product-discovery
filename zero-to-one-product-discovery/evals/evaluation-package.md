# Evaluation Package

## Purpose

This document summarizes the current evaluation system for `zero-to-one-product-discovery`.

The goal is not to collect large amounts of run output. The goal is to make failures explainable, turn real misses into regression scenarios, and preserve only evidence that improves release, install, architecture, or quality decisions.

## Design Reference

This evaluation system follows the core pattern from OpenAI's "Testing Agent Skills Systematically with Evals":

```text
prompt -> captured run trace / artifacts -> deterministic checks -> structured rubric -> comparable score
```

For this skill, deterministic checks protect hard workflow boundaries, while rubric grading covers qualitative behavior such as evidence grounding, user-question quality, and multi-agent separation.

## Package Boundary

The installable skill keeps only reusable evaluation assets:

- `evals.json`: strict scenario suite, success checks, hard failures, and scoring metadata.
- `eval-rubric-template.md`: scoring and value-review template.
- `claude-code-pressure-test-protocol.md`: five-pass pressure-test protocol.
- `eval-report.schema.json`: structured report schema.
- `value-review.schema.json`: post-test value-gate schema.
- `evaluation-package.md`: concise evidence interpretation and release boundary.

Raw responses, JSONL traces, scored reports, audit notes, handoff records, and design records stay outside the skill package in `zero-to-one-product-discovery-eval-runs/`.

Promoted records in `zero-to-one-product-discovery-eval-runs/current/<version>/<run-id>/` may be committed with the GitHub repository as public project evidence. They must not be included in the installable skill zip and must not be loaded during ordinary runtime use.

## Current Version

Current package version: `v0.1.5`.

`v0.1.0-draft` remains the early historical draft. The multi-agent workflow architecture is tracked as the larger `v0.1.5` upgrade.

## Strict Suite Shape

The `v0.1.5` suite is intentionally smaller and stricter than the earlier scenario set. It prioritizes high-risk failures over broad but shallow coverage.

Scenario categories:

- `trigger_boundary`
- `stage_gate`
- `evidence_grounding`
- `child_skill_routing`
- `multi_agent_orchestration`
- `audit_user_gate`
- `context_economy`
- `multi_turn_continuity`
- `negative_control`

Every scenario must define:

- `must_pass_checks`: required behaviors.
- `hard_failures`: fail-fast conditions.
- `deterministic_checks`: concrete checks that can be inspected from text, trace, or artifacts.
- `rubric_checks`: qualitative checks for structured grading.
- `why_this_matters`: the real product risk protected by the scenario.
- `value_signal`: what improvement a failure should produce.

## Evidence Value Gate

New run output starts in `zero-to-one-product-discovery-eval-runs/tmp/<run-id>/`.

After scoring, the evaluator must create a value review. A run becomes project evidence only if it finds a substantive issue, exposes a regression, confirms a previously unverified release gate, or produces a concrete improvement direction.

No-actionable-finding runs must not be presented as strong evidence. They can be discarded or preserved as a minimal note only when they close a specific release question.

## Current Evidence Summary

| Area | Status | Interpretation |
|---|---|---|
| Initial trigger and stage-purity checks | Historical evidence in `archive/pre-v0.1.5/` | Useful baseline only; predates later architecture changes. |
| Child-skill routing and wrapper behavior | Historical evidence in `archive/pre-v0.1.5/` | Supports prior refactor decisions, but is not fresh evidence for `v0.1.5`. |
| Copy-first source boundary | Historical evidence in `archive/pre-v0.1.5/` | Supports source-governance direction, with historical limitations. |
| Multi-agent workflow protocol | Structural design documented in `design-records/v0.1.5/` | Architecture is documented and has initial strict-suite pressure evidence. |
| `v0.1.5` strict suite | `current/v0.1.5/2026-05-12-run-01/` | Fresh run found one failed package-boundary scenario and two improvement points; it is valuable evidence but not install-candidate proof. |
| Targeted boundary rerun | `current/v0.1.5/2026-05-14-run-02/` | Five adjacent scenarios passed after patch; closes the package/vendor boundary regression, but does not replace a full-suite rerun. |

## Allowed Claims

The current evidence supports these claims:

- The skill has a reusable, strict scenario-based evaluation harness.
- The harness defines deterministic checks, rubric checks, hard failures, and a post-test value gate.
- Historical runs helped shape the current architecture, but they are not release-grade validation for `v0.1.5`.
- The `v0.1.5` multi-agent architecture is structurally documented and ready for fresh pressure testing.
- The first fresh strict-suite run produced actionable findings, and the targeted boundary rerun confirms the package/vendor boundary patch.

## Unsupported Claims

Do not claim:

- Release-grade validation.
- Global-install trigger reliability.
- Stable multi-agent runtime behavior in real model runs.
- Complete multi-turn workflow quality.
- Proven superiority over baseline model behavior.

## Next Evidence Needed

Before stronger release or installation claims, run and value-review:

1. Full 22-scenario strict-suite rerun after the boundary patch if v0.1.5 should become an install candidate.
2. Multi-turn discovery simulation through Research Brief -> PRD -> Roadmap -> Implementation Plan readiness.
3. Baseline-vs-skill A/B run on the updated scenario set.
4. Global-install trigger test in Codex and Claude Code.
