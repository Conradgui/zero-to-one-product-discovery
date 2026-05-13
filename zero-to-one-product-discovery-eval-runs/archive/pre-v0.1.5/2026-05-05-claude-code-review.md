# Claude Code Pressure Test Review: 2026-05-05

## Review Scope

Reviewed files:

- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-raw.md`
- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md`
- `zero-to-one-product-discovery/evals/evals.json`
- `zero-to-one-product-discovery/evals/eval-rubric-template.md`
- `zero-to-one-product-discovery/SKILL.md`
- `zero-to-one-product-discovery/references/workflow.md`

## Findings

### Medium: Environment Metadata Is Not Reproducible

Evidence:

- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-raw.md:6` records `Model: claude-sonnet (assumed; this evaluator session)`.
- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-raw.md:8` records the repository as `not a git repo`.
- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:6` repeats the assumed model.
- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:8` repeats the repository error.

This is not reliable release evidence. The directory is a Git repository in the current Codex session, and the model name should not be guessed.

Impact:

- Future reviewers cannot reliably reproduce the exact test environment.
- GitHub readers may discount the report because basic environment metadata is inaccurate.

Resolution:

- Keep the Claude raw/report files as generated artifacts.
- Update the pressure test protocol to require `pwd`, `git rev-parse --show-toplevel`, `git status --short`, and exact model reporting when exposed.
- If the model is not exposed, record `not exposed by CLI` instead of guessing.

### Medium: Heavy Advisor Scoring Was Biased Toward Diagnostic Start

Evidence:

- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:22` shows `heavy_advisor_requested` as the lowest-scoring scenario.
- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:228` to `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:230` applies Diagnostic Start-shaped scoring to Heavy Advisor output.
- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:294` to `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:306` correctly identifies the rubric mismatch and proposes a mode-aware scoring lens.

Impact:

- Heavy Advisor responses can be correct per skill behavior but under-scored by a rubric built for Diagnostic Start.
- The suite average may look lower or the wrong patch may be made if the scoring lens is not mode-aware.

Resolution:

- Add Heavy Advisor scoring mappings to the rubric:
  - FAR split maps to assumptions, unknowns, and named risks.
  - Candidate directions map to decision branches, ADR candidates, or option surfaces.
  - Question quality maps to the leverage of the next alignment question.
- Add a Heavy Advisor output skeleton to workflow references.

### Medium: Raw Character Count Is A Weak Proxy For Context Economy

Evidence:

- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:295` identifies the repeated character-count deductions as a rubric flaw.
- `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:307` to `zero-to-one-product-discovery-eval-runs/2026-05-05-claude-code-report.md:310` recommends moving context economy away from a strict length cap.
- `zero-to-one-product-discovery/evals/evals.json:12` now defines context economy by information density and actual waste patterns.
- `zero-to-one-product-discovery/evals/eval-rubric-template.md:83` to `zero-to-one-product-discovery/evals/eval-rubric-template.md:87` now mirrors the density-based scoring rule.

Impact:

- The rubric can penalize useful detail instead of actual context waste.
- Models may compress away the very analysis the skill is intended to force.

Resolution:

- Reframe context economy around template dumping, padding, repetition, premature references, and premature later-stage artifacts.
- Keep raw length as a warning signal, not a primary scoring rule.

## Positive Findings

- Claude Code followed the two-pass protocol and saved separate raw and scored reports.
- Trigger and non-trigger routing succeeded across all seven scenarios.
- Diagnostic Start stayed stage-pure in triggering scenarios.
- Existing PRD without MVP was correctly treated as zero-to-one with Material Assimilation.
- Existing runnable MVP was correctly routed away from the skill.
- Design references were acknowledged but deferred instead of driving early product definition.

## Patches Applied After Review

- `SKILL.md`: Heavy Advisor now requires outlines, decision surfaces, and assumption clearings when domain is under-specified.
- `SKILL.md`: Diagnostic Start length guidance now prioritizes information density over strict character count.
- `references/workflow.md`: Heavy Advisor now has a mode-specific output skeleton and scoring interpretation.
- `references/planning-artifacts.md`: Heavy Advisor artifact output is explicitly limited to outlines and decision surfaces unless grounded.
- `evals/evals.json`: added Heavy Advisor scoring rule and replaced strict length limit with density-based context economy.
- `evals/eval-rubric-template.md`: added Heavy Advisor scenario scoring and density-based context economy.
- `evals/claude-code-pressure-test-protocol.md`: added environment verification and model-name anti-guessing rules.

## Release Interpretation

The Claude Code run is useful as an independent pressure test, but the current raw/report files should be described as `independent pressure test, first run, reviewed with metadata caveats`.

Before global installation or GitHub release, rerun at least:

- `heavy_advisor_requested`
- one new Heavy Advisor scenario with a concrete product domain
- one long-material Material Assimilation scenario
- one existing-MVP first-principles reset scenario

## Recommendation

Do not install globally yet. Patch set is now applied; rerun the affected scenarios plus adjacent scenarios before treating this as release-grade evidence.
