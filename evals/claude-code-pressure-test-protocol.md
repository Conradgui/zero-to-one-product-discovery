# Claude Code Pressure Test Protocol

## Document Purpose

This document defines a reproducible pressure test protocol for evaluating `zero-to-one-product-discovery` in Claude Code or another independent agent environment. It is designed to produce auditable raw responses, numeric scores, hard-failure checks, and patch recommendations.

## Update Rules

- Append new evaluation runs; do not overwrite historical results.
- Keep raw responses and scored reports separate.
- Do not modify `SKILL.md` or references during a test run.
- If scoring criteria change, record the date, reason, and affected comparisons.
- A hard failure makes the scenario fail even if its numeric score is high.

## Files Under Test

Repository-relative paths:

- `zero-to-one-product-discovery/SKILL.md`
- `zero-to-one-product-discovery/references/`
- `zero-to-one-product-discovery/evals/evals.json`
- `zero-to-one-product-discovery/evals/eval-rubric-template.md`

## Evaluation Goals

This protocol tests whether the skill:

- Triggers only for zero-to-one product discovery situations.
- Does not trigger for existing runnable MVP improvement or narrow implementation tasks.
- Uses Diagnostic Start by default.
- Avoids premature PRD, Roadmap, Milestones, ADRs, MVP scope, tech stack, repository scaffolding, or implementation plans.
- Routes specialist child-skill artifacts through main workflow stage gates instead of letting child skills bypass prerequisites.
- Grounds responses in the user's actual words and materials.
- Distinguishes facts, assumptions, risks, and unknowns.
- Asks the highest-leverage question for the current turn, while preserving the multi-turn question loop.
- Keeps context usage controlled.

## Scientific Controls

Use these controls for every run:

- Start from a fresh Claude Code session when possible.
- Do not paste prior self-eval conclusions into the generation pass.
- Do not edit the skill during evaluation.
- Do not use web search unless a scenario explicitly requires current external facts.
- Generate raw responses first, then score them in a second pass.
- Save raw responses before scoring.
- Record model, agent, date, repository state, and skill version.
- Verify repository state with `pwd`, `git rev-parse --show-toplevel`, and `git status --short` when available.
- Record the exact model name if the agent exposes it. If it does not, write `not exposed by CLI`; do not guess.

## Two-Pass Evaluation

### Pass 1: Raw Response Generation

Goal: generate one response per scenario using the skill, without scoring yet.

Rules:

- Read `SKILL.md` and only the references needed by the skill.
- Read `evals.json` only for each scenario's `id` and `prompt`.
- Do not inspect or use `should_trigger`, `expected_mode`, `expected_behavior`, `scenario_hard_failures`, or `scoring_focus` until Pass 2.
- For each scenario, write the raw response the agent would give to the user.
- Do not patch the skill during this pass.
- Use a `run-XX` sequence for same-day runs. Increment it instead of overwriting existing run files.

Output file:

```text
zero-to-one-product-discovery-eval-runs/YYYY-MM-DD-run-XX-claude-code-raw.md
```

### Pass 2: Scoring

Goal: score each raw response against the rubric.

Rules:

- Read `evals.json` fully.
- Read `eval-rubric-template.md`.
- Check hard failures first.
- If any hard failure appears, mark the scenario as failed regardless of numeric score.
- Score each dimension with evidence from the raw response.
- Record patches needed after all scenarios are scored.
- Do not patch the skill during scoring.

Output file:

```text
zero-to-one-product-discovery-eval-runs/YYYY-MM-DD-run-XX-claude-code-report.md
```

## Scoring Thresholds

| Metric | Threshold |
|---|---:|
| Scenario pass | 85 |
| Suite pass | 85 average |
| Install candidate | 90 average and 0 hard failures |

## Hard Failures

Check every scenario for:

- `wrong_trigger_decision`
- `asks_mature_product_question_upfront`
- `produces_later_stage_artifacts`
- `asks_multiple_key_questions`
- `generic_response`
- `child_skill_stage_bypass`

Scenario-specific hard failures are defined in `evals.json`.

## Claude Code Copy-Paste Prompt

Copy this entire prompt into Claude Code from the repository root:

```markdown
You are evaluating the draft skill `zero-to-one-product-discovery`.

Do not install the skill globally. Do not modify `SKILL.md`, references, or eval files during this evaluation. This run must produce auditable raw responses and a scored report.

Before generating responses, record the environment:

- Run `pwd` and record the output as `Working directory`.
- Run `git rev-parse --show-toplevel` and record the output as `Git root command output`. If the command fails, record the exact failure.
- Run `git status --short` and record the output as `Git status command output`. If there is no output, write `clean`.
- Record the exact model name if Claude Code exposes it. If it does not, write `not exposed by CLI`; do not guess.
- Choose a `Run ID` in the form `YYYY-MM-DD-run-XX`. If a run file already exists for the same date, increment `XX`; do not overwrite existing run files.

## Files

Read:

- `zero-to-one-product-discovery/SKILL.md`
- `zero-to-one-product-discovery/evals/evals.json`
- `zero-to-one-product-discovery/evals/eval-rubric-template.md`

Load reference files from `zero-to-one-product-discovery/references/` only when the skill says they are needed.

## Pass 1: Raw Response Generation

Read `evals.json` only for each scenario's:

- `id`
- `prompt`

Do not use `should_trigger`, `expected_mode`, `expected_behavior`, `scenario_hard_failures`, or `scoring_focus` during Pass 1.

For each scenario, generate the exact response you would give to the user if the prompt were sent in a normal session.

Write all raw responses to:

`zero-to-one-product-discovery-eval-runs/YYYY-MM-DD-run-XX-claude-code-raw.md`

Use this structure:

# Claude Code Raw Responses: YYYY-MM-DD-run-XX

## Environment

- Run ID:
- Agent:
- Model:
- Date:
- Repository:
- Working directory:
- Git root command output:
- Git status command output:
- Skill version:

## Scenario: scenario_id

### Prompt

### Raw Response

## Pass 2: Scoring

After saving raw responses, read the full `evals.json` and `eval-rubric-template.md`.

Score each scenario using the 100-point rubric. Check hard failures before assigning the final verdict.

Write the scored report to:

`zero-to-one-product-discovery-eval-runs/YYYY-MM-DD-run-XX-claude-code-report.md`

Use this structure:

# Claude Code Evaluation Report: YYYY-MM-DD-run-XX

## Environment

- Run ID:
- Agent:
- Model:
- Date:
- Repository:
- Working directory:
- Git root command output:
- Git status command output:
- Skill version:
- Evaluation file:
- Rubric file:

## Summary

| Scenario | Expected Mode | Score | Hard Failure | Verdict |
|---|---|---:|---|---|

## Aggregate

- Average score:
- Median score:
- Lowest score:
- Hard failure count:
- Suite pass threshold:
- Install candidate threshold:
- Install candidate:

## Scenario Results

For each scenario:

### Scenario: scenario_id

#### Hard Failure Check

- [ ] wrong_trigger_decision
- [ ] asks_mature_product_question_upfront
- [ ] produces_later_stage_artifacts
- [ ] asks_multiple_key_questions
- [ ] generic_response
- [ ] child_skill_stage_bypass
- [ ] scenario-specific hard failure, if any

#### Score

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger accuracy | 15 |  |  |
| Stage purity | 15 |  |  |
| Context grounding | 15 |  |  |
| Fact / assumption / risk split | 15 |  |  |
| Candidate exploration directions | 10 |  |  |
| Dangerous assumption | 10 |  |  |
| Question quality | 10 |  |  |
| Context economy | 10 |  |  |
| Total | 100 |  |  |

#### Verdict

Pass / Fail.

#### Patch Needed

## Findings

### Strengths

### Weaknesses

### Required Patches

### Follow-up Scenarios

Do not apply patches in this run. Only report them.
```

## Expected Interpretation

Use the report to decide:

- If average score is at least 90 and hard failures are 0, the skill is a candidate for global install.
- If average score is 85-89 or hard failures are 0 but weaknesses are material, patch and rerun.
- If any hard failure appears, patch and rerun the failed scenario plus at least two adjacent scenarios.
- If non-trigger scenarios fail, tighten trigger boundaries before adding more features.

## Review Notes For Current Internal Self-Eval

The current internal self-eval is useful but insufficient as release evidence because:

- It did not capture raw model responses.
- It was performed in the same session that authored the skill.
- It scored rule coverage more than actual behavior.
- It cannot detect whether a fresh model will over-expand, ask multiple questions, or ignore trigger boundaries.

For GitHub release notes, describe it as "static self-evaluation" and describe Claude Code results as "independent pressure test" only after this protocol is run.
