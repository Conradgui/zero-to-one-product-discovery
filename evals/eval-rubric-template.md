# Skill Evaluation Rubric Template

## Document Purpose

This template defines a repeatable scoring process for evaluating whether a skill behaves reliably across pressure scenarios. It is intended for maintainers, contributors, and reviewers who want to assess skill quality before installation or release.

## Update Rules

- Append scenario results; do not overwrite historical findings.
- Keep raw model responses when possible so later reviewers can audit scores.
- If a scoring rule changes, record the date and reason before comparing old and new scores.
- A hard failure makes the scenario fail even if the numeric score is high.

## Scoring Summary

| Level | Meaning |
|---:|---|
| 90-100 | Candidate for global installation or release |
| 85-89 | Passes baseline; minor improvement recommended |
| 70-84 | Needs skill or rubric revision |
| <70 | Fails; do not install or release |

## Hard Failures

Check every scenario for these failures:

- `wrong_trigger_decision`: skill is used when it should not be, or not used when it should be.
- `asks_mature_product_question_upfront`: response asks for target user, MVP, tech stack, or business model before candidate interpretation.
- `produces_later_stage_artifacts`: response creates PRD, Roadmap, Milestones, ADRs, tech choices, MVP scope, scaffolding, or implementation plan too early.
- `asks_multiple_key_questions`: response asks more than one key question in the same turn. This is a per-turn UX rule, not a total question limit across the workflow.
- `generic_response`: response gives generic advice without grounding in the prompt or materials.
- `vendor_boundary_bypass`: response treats copied upstream files in `vendor/` as active routeable child skills or commands.

## Non-Trigger Scenarios

For scenarios where the skill should not trigger, score `trigger_accuracy`, `stage_purity`, `context_grounding`, and `context_economy` normally.

Award full credit for `fact / assumption / risk split`, `candidate exploration directions`, `dangerous assumption`, and `question quality` only when the response correctly avoids discovery artifacts, gives a concise boundary reason, and does not ask strategic product-discovery questions.

## Rubric

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

## Dimension Guide

### Trigger Accuracy

Scores whether the response correctly decides if the skill should apply.

### Stage Purity

Scores whether the response stays within the intended stage and avoids premature artifacts.

### Context Grounding

Scores whether the response uses the user's specific wording, materials, constraints, and goals.

### Fact / Assumption / Risk Split

Scores whether the response distinguishes facts, assumptions, risks, and unknowns.

### Candidate Exploration Directions

Scores whether the response gives two or three project-specific exploration directions when appropriate.

### Dangerous Assumption

Scores whether the response identifies the assumption most likely to mislead the project.

### Question Quality

Scores whether the response asks the highest-leverage question for the current turn and explains why it matters. A later turn may ask another question after the user's answer is incorporated.

### Context Economy

Scores whether the response avoids template dumping, padding phrases, repeated content, redundant summaries, premature reference loading, and premature later-stage artifacts.

Do not penalize dense, prompt-specific content solely because it is longer. Responses below 300 Chinese characters may under-deliver; responses above 1500 Chinese characters need long user material or an explicit deeper-mode request.

## Heavy Advisor Scenarios

For scenarios where the expected mode is Heavy Advisor, use these mappings:

- `Fact / assumption / risk split`: score explicit assumptions, unknowns, and named risks instead of requiring the Diagnostic Start four-way split.
- `Candidate exploration directions`: score decision branches, ADR candidates, or option surfaces instead of requiring two or three Diagnostic Start exploration directions.
- `Question quality`: score the leverage of the next alignment question, even if it asks for one-line domain context.

Heavy Advisor outputs should still avoid presenting early PRD, Roadmap, Milestones, or ADR content as final artifacts unless the product domain is already grounded.

## Child-Skill Routing Scenarios

For scenarios where the expected mode mentions a child-skill contract, score the main skill and the specialist route together:

- `Trigger accuracy`: score whether `zero-to-one-product-discovery` applies and whether the requested child capability is in scope.
- `Stage purity`: score whether the main skill routes, downgrades, blocks, or escalates the child output according to stage gates.
- `Context grounding`: score whether the child output uses only the provided facts, materials, assumptions, and constraints.
- `Fact / assumption / risk split`: score explicit evidence status, assumptions, unknowns, risks, blockers, and readiness signal.
- `Candidate exploration directions`: score route options, decision surfaces, or next-stage capability choices when a final artifact is not safe.
- `Dangerous assumption`: score whether the response identifies the assumption most likely to make the routed artifact misleading.
- `Question quality`: score whether the response asks one highest-leverage main-workflow question for the current turn when alignment is needed; final artifact turns may omit a question only if they return a clear readiness signal and no blocking ambiguity.
- `Context economy`: score whether the response avoids dumping full external templates, over-explaining child-skill internals, or producing multiple artifacts when only a route check was requested.

Hard failures for child-skill scenarios include:

- Letting a child skill jump stages independently.
- Producing final PRD, Roadmap, Milestones, ADR, backlog, or implementation plan when prerequisites are missing.
- Omitting readiness signal or Context Resume Packet for substantial child output.
- Copying external skill wording or examples instead of using local contracts.

## Copy-First Vendor Scenarios

For scenarios involving copied external source, score whether the response preserves the two-layer boundary:

- `Trigger accuracy`: skill-maintenance prompts should not trigger product discovery.
- `Stage purity`: routeable behavior must come from `child-skills/`, not `vendor/`.
- `Context grounding`: attribution and copied-file records must match the actual source groups.
- `Fact / assumption / risk split`: license, copied text, local modification, and routeability status must be explicit.
- `Candidate exploration directions`: score integration modes such as vendored adapter, benchmark only, local rewrite, or quality gate.
- `Dangerous assumption`: score whether the response identifies direct command routing or unattributed copying as the highest-risk mistake.
- `Question quality`: copy-first maintenance work should not ask product-discovery questions.
- `Context economy`: score concise source-governance guidance without dumping upstream templates.

Hard failures for copy-first scenarios include:

- Pasting upstream templates into active workflow files without attribution.
- Routing directly to vendored command wrappers.
- Global-installing external skills before gate tests.
- Marking copied upstream text as locally rewritten.

## Local Wrapper Scenarios

For scenarios where the expected mode mentions a local wrapper, score whether the wrapper keeps the external inspiration narrow and subordinate to the main workflow:

- `Trigger accuracy`: score whether the zero-to-one workflow applies, or whether the prompt is skill-maintenance and should not trigger.
- `Stage purity`: score whether the wrapper stays in its intended stage and does not create downstream artifacts.
- `Context grounding`: score whether wrapper output uses the user's provided facts and labels missing evidence.
- `Fact / assumption / risk split`: score explicit separation of facts, assumptions, unknowns, risks, and blocker status.
- `Candidate exploration directions`: score reframed hypotheses, decision surfaces, HMW candidates, or route options as appropriate for the wrapper.
- `Dangerous assumption`: score whether the response identifies the assumption most likely to make the wrapper output misleading.
- `Question quality`: score one highest-leverage next question or a clear material request for the current turn.
- `Context economy`: score whether the wrapper avoids external template dumping and avoids reproducing a whole workshop flow when a compact wrapper output is enough.

Hard failures for local wrapper scenarios include:

- Letting wrapper output become PRD, Roadmap, ADR, backlog, or Implementation Plan before the main workflow gate.
- Copying external wrapper source text or template bodies.
- Letting the wrapper route to another wrapper directly.
- Omitting local readiness / blocker status for substantial wrapper output.

## Scenario Result Template

```markdown
## Scenario: scenario_id

### Prompt

Paste the scenario prompt.

### Expected Mode

Diagnostic Start / Standard Exploration / Heavy Advisor / Do not trigger.

### Actual Response

Paste or link to the raw response.

### Hard Failure Check

- [ ] wrong_trigger_decision
- [ ] asks_mature_product_question_upfront
- [ ] produces_later_stage_artifacts
- [ ] asks_multiple_key_questions
- [ ] generic_response
- [ ] vendor_boundary_bypass

### Score

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

### Verdict

Pass / Fail.

### Patch Needed

Describe what should change in `SKILL.md`, references, eval scenarios, or the rubric.
```

## Recommended Suite Report

```markdown
# Evaluation Run: YYYY-MM-DD

## Environment

- Agent:
- Model:
- Skill version:
- Evaluation file:

## Summary

| Scenario | Expected Mode | Score | Hard Failure | Verdict |
|---|---|---:|---|---|

## Aggregate

- Average score:
- Median score:
- Lowest score:
- Hard failure count:
- Install candidate: Yes / No

## Findings

### Strengths

### Weaknesses

### Required Patches

### Follow-up Scenarios
```
