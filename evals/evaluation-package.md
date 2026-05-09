# Evaluation Package

## Document Purpose

This document packages the current evaluation evidence for `zero-to-one-product-discovery`. It is intended for maintainers, reviewers, and GitHub readers who need to understand what was tested, which artifacts belong together, and what the results can and cannot prove.

Run artifacts are stored outside the installable skill directory in `zero-to-one-product-discovery-eval-runs/` to keep the packaged skill lean. The `evals/` directory keeps only reusable scenarios, rubrics, and test protocols.

## Update Rules

- Append new evaluation records; do not rewrite historical results.
- Keep raw model outputs separate from scored reports and review notes.
- If a test run has metadata issues, record the limitation instead of silently correcting the original artifact.
- Do not describe a same-session static review as an independent pressure test.
- Do not describe a manually executed Claude Code run as release-grade evidence until its metadata, protocol compliance, and post-run review are documented.

## Records

### 2026-05-05: Initial Evaluation Package

#### Included Artifacts

| Artifact | Type | Role |
|---|---|---|
| `evals.json` | Scenario set and scoring model | Defines pressure scenarios, thresholds, hard failures, and mode-specific scoring rules. |
| `eval-rubric-template.md` | Rubric template | Defines repeatable scoring format and interpretation rules. |
| `claude-code-pressure-test-protocol.md` | Independent test protocol | Defines how to run a two-pass Claude Code pressure test without leaking scoring fields into raw response generation. |
| `zero-to-one-product-discovery-eval-runs/2026-05-05-self-eval.md` | Static self-evaluation | Same-session rule-coverage review by Codex. |
| `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-raw.md` | Manual Claude Code raw responses | Raw responses from a manually executed Claude Code pressure test. |
| `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md` | Manual Claude Code scored report | Numeric scoring of the manual Claude Code raw responses. |
| `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-review.md` | Codex review addendum | Post-run review of the Claude Code report, including metadata caveats and rubric patches. |

#### Evaluation Interpretation

| Evidence | Recommended Label | Use |
|---|---|---|
| `2026-05-05-self-eval.md` | Static self-evaluation | Useful for checking written rule coverage and obvious gaps. Not independent model evidence. |
| `2026-05-05-claude-code-raw.md` + `2026-05-05-claude-code-report.md` | Manual Claude Code pressure test with metadata caveats | Useful as an external response sample. Not release-grade on its own because environment metadata was imperfect. |
| `2026-05-05-claude-code-review.md` | Post-run review | Explains how to interpret the manual Claude Code result and which rubric/protocol issues were patched afterward. |

#### Known Limitations

1. Static self-evaluation was performed in the same Codex session that authored the skill. It checks whether rules appear sufficient, but it does not measure a fresh model's actual behavior.
2. The static self-evaluation did not capture full raw model responses. Its scores are rule-coverage estimates, not independently generated outputs.
3. The manual Claude Code run was initiated by copying a prepared prompt into Claude Code. This is closer to an independent pressure test than self-evaluation, but it is still not equivalent to testing the skill after global installation and natural trigger selection.
4. The manual Claude Code report recorded `claude-sonnet (assumed; this evaluator session)` instead of an exposed model identifier. Future runs must write `not exposed by CLI` when the exact model is unavailable.
5. The manual Claude Code report recorded the repository as `not a git repo`, which was incorrect in the Codex environment. Future runs must record `pwd`, `git rev-parse --show-toplevel`, and `git status --short`.
6. The manual Claude Code scores were produced before the post-review rubric and protocol patches were fully applied. They should not be treated as a final score for the current exact draft.
7. There is no baseline run without the skill. The current evidence does not yet prove that the skill fixes behavior that the model would otherwise get wrong.
8. The current suite is mostly single-turn. It does not yet validate multi-turn discovery, Context Resume Packet continuity, material assimilation over long user documents, or planning-artifact phase gates.
9. The current suite does not validate automatic trigger behavior after installing the skill globally in Codex or Claude Code.
10. The interrupted CLI rerun on 2026-05-05 produced no `rerun` raw/report files and is excluded from the evidence package.
11. On 2026-05-06, the skill architecture shifted from local artifact templates toward a main workflow plus specialist child-skill contracts. Evidence from 2026-05-05 predates that architecture and should be treated as baseline trigger evidence only.
12. The current evidence does not yet validate child-skill routing, downgrade behavior, readiness signals, or cross-child UX consistency.

#### README-Safe Claim

The current evidence supports this wording:

```markdown
The draft skill includes a scenario-based evaluation harness, a static same-session self-evaluation, one manually executed Claude Code pressure test with documented metadata caveats, and a newer child-skill routing scenario set. The first run found no hard failures across the initial scenarios, but it predates the hub-and-spoke refactor. The project does not yet claim release-grade validation. Follow-up work should prioritize child-skill routing pressure tests, cross-child UX consistency checks, and then baseline-vs-skill comparison.
```

Avoid this wording for now:

```markdown
This skill is independently validated and ready for global installation.
```

#### Deferred Evidence To Add

These evidence items remain required before release-grade validation, but they are deferred until the skill writing and state cleanup pass is complete:

1. Quality comparison between old artifact-adapter outputs and copy-first `child-skills/` adapter outputs.
2. Cross-child UX consistency review: routing note, assumption labels, per-turn highest-leverage question rule, readiness signal, and Context Resume Packet.
3. Multi-turn zero-to-one discovery simulation through Research Brief -> PRD -> Roadmap -> Implementation Plan readiness.
4. Baseline-vs-skill A/B run on the updated scenario set.
5. Fresh Claude Code protocol rerun with verified environment metadata.
6. Global-install trigger test in Codex and Claude Code.

### 2026-05-06: Hub-And-Spoke Refactor Evidence Package Update

#### Included Additions

| Artifact | Type | Role |
|---|---|---|
| `references/source-evaluation.md` | Source evaluation | Ranks Product-Manager-Skills, pm-skills, agent-skills, and awesome-copilot by quality role and UX role. |
| `references/artifact-adapters.md` | Child-skill contracts | Defines specialist capability contracts and readiness signals. |
| `references/planning-artifacts.md` | Routing protocol | Defines route, downgrade, escalation, UX consistency, and child-skill handoff packet rules. |
| `evals.json` child-skill scenarios | Scenario set extension | Tests PRD routing, roadmap downgrade, research synthesis, ADR escalation, and multi-child handoff. |
| `eval-rubric-template.md` child-skill section | Rubric extension | Defines how to score child-skill routing scenarios. |
| `zero-to-one-product-discovery-eval-runs/2026-05-06-child-skill-refactor-audit.md` | Refactor audit | Checks plan completion, remaining work, and drift risks after the hub-and-spoke refactor. |
| `zero-to-one-product-discovery-eval-runs/2026-05-06-child-skill-routing-self-eval.md` | Static self-evaluation | Checks written rule coverage for child-skill routing. Not independent model evidence. |
| `zero-to-one-product-discovery-eval-runs/2026-05-06-run-01-child-routing-report.md` | Child-routing scored report | Scores a fresh subagent raw response run; found one source-governance boundary hard failure. |
| `zero-to-one-product-discovery-eval-runs/2026-05-06-run-02-boundary-rerun-report.md` | Boundary rerun report | Confirms patched source-governance, command mini-hub, and Implementation Plan grounding boundary scenarios pass. |
| `zero-to-one-product-discovery-eval-runs/2026-05-07-run-01-wrapper-report.md` | Wrapper report | Scores Problem Framing, ADR Governance, and Context Handoff wrappers; found one Problem Framing per-turn question UX failure. |
| `zero-to-one-product-discovery-eval-runs/2026-05-07-run-02-wrapper-rerun-report.md` | Wrapper rerun report | Confirms the Problem Framing per-turn question issue is fixed. |

#### Current Interpretation

The refactor is documented and structurally testable. A first fresh child-routing subagent run passed PRD, Roadmap downgrade, Research Brief, ADR, multi-child handoff, and Heavy Advisor scenarios, but failed `artifact_source_boundary` because the response used product-discovery-style framing for a skill-maintenance request. That boundary has been patched in `SKILL.md`, `source-attribution.md`, and `evals.json`, but the failing scenario still needs a rerun before installation or release claims.

The boundary rerun passed after the patch. The first local wrappers have now been added for Problem Framing, ADR Governance, and Context Handoff.

The dedicated wrapper pressure test is now complete. ADR Governance and Context Handoff passed on the first run. Problem Framing initially failed the per-turn question UX rule, was patched in `child-skill-wrappers.md` and `evals.json`, and then passed rerun.

### 2026-05-09: State-Cleanup Interpretation Update

The project is currently in a documentation and rule-convergence pass. Do not execute new pressure tests, A/B tests, natural trigger tests, or OmniWeb product work during this pass.

Current evidence supports these claims only:

- Source-governance and command mini-hub boundaries have passing rerun evidence.
- The first local wrappers have passing pressure evidence after rerun.
- Copy-first vendor boundary and copied PRD adapter behavior have initial passing evidence from `2026-05-08-run-01-copy-first-report.md`.

Current evidence does not yet prove:

- Release-grade validation.
- Global-install trigger reliability.
- Full multi-turn workflow quality.
- Old artifact-adapter vs copy-first child-adapter quality improvement.

Next evidence work should begin only after skill writing and state cleanup are complete.
