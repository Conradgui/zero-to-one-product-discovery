---
name: execution-bridge
description: Use when the main workflow has a review-ready Implementation Plan and the user needs to convert it into executable downstream formats (GitHub Issues, Claude Code tasks, or Jira tickets).
---

# Execution Bridge

## Role

Convert a review-ready Implementation Plan into executable downstream formats while preserving evidence labels, acceptance criteria, and verification commands.

## Required Input

- Review-ready Implementation Plan with ordered tasks, acceptance checks, and verification commands.
- Target format: GitHub Issues, Claude Code tasks, or Jira tickets.
- Repository context when relevant: repo URL, project board, labels, assignees.
- Evidence snapshot: which inputs are facts, assumptions, or unknowns.

## Output Contract

For each task in the Implementation Plan, produce one output unit in the target format:

### GitHub Issues Format

```markdown
## Title
[Task title from Implementation Plan]

## Description
[Task description with context from PRD and Implementation Plan]

## Acceptance Criteria
- [ ] [Criterion 1 from Implementation Plan]
- [ ] [Criterion 2 from Implementation Plan]

## Evidence Context
- Source: [PRD section / User Story / ADR reference]
- Assumption status: [Fact / Assumption / Unknown]
- Validation needed: [Yes/No, what if yes]

## Labels
- evidence-[fact/assumption/unknown]
- priority-[high/medium/low]
- component-[name]

## Verification Commands
[Commands or scenarios from Implementation Plan]

## Dependencies
[Blocking tasks or external dependencies]
```

### Claude Code Tasks Format

```markdown
## Task
[Task description]

## Context
- PRD: [relevant PRD section summary]
- User Story: [if applicable]
- ADR: [if applicable]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Evidence Labels
- [Fact/Assumption/Unknown]: [what]

## Verification
[Commands or scenarios to verify completion]

## Boundaries
- Non-goals: [from Implementation Plan]
- Constraints: [from Implementation Plan]
```

### Jira Tickets Format

```markdown
## Summary
[Task title]

## Description
[Task description with context]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Evidence Context
Source: [PRD / User Story / ADR]
Assumption status: [Fact / Assumption / Unknown]

## Definition of Done
- [All acceptance criteria met]
- [Verification commands pass]
- [Evidence labels reviewed]

## Labels
evidence-[status], priority-[level], component-[name]
```

## Boundaries

- Only accept review-ready Implementation Plans as input. Do not convert PRD, Roadmap, or User Stories directly to execution format.
- Do not modify the Implementation Plan content. Transcode and restructure only.
- Every output unit must preserve evidence labels from the source artifacts.
- Do not invent tasks, acceptance criteria, or verification commands that are not in the Implementation Plan.
- Do not assign tasks to specific people unless the user provides assignment information.
- If the Implementation Plan has gaps, report them as blockers rather than filling them with assumptions.

## Readiness Signal

Return `ready_for_next_stage` when all tasks are converted to the target format.

Return `needs_more_evidence` if the Implementation Plan has gaps that prevent conversion (missing acceptance criteria, missing verification commands, unclear task boundaries).

Return `needs_main_skill_decision` if the user needs to choose between conflicting target formats or if task prioritization is unclear.

Return `blocked` if the Implementation Plan is not review-ready.

## Context Resume Packet

After conversion, include:

- Number of tasks converted.
- Evidence distribution: how many tasks are fact-grounded vs assumption-labeled.
- Gaps found in the Implementation Plan during conversion.
- Recommended next action.
