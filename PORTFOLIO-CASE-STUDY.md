# Portfolio Case Study: Zero-to-One Product Discovery Skill

## One-Line Summary

Built an AI product discovery workflow skill with multi-agent governance, stage gates, audit/user gates, and quantitative evals to prevent LLMs from overproducing ungrounded PRDs, Roadmaps, or implementation plans.

## Problem

General-purpose AI assistants are helpful in early product exploration, but they often move too fast:

- turning vague ideas into polished but ungrounded PRDs;
- accepting assumptions as facts;
- skipping user confirmation gates;
- mixing discovery, planning, and implementation;
- losing package/source boundaries during skill maintenance.

For a zero-to-one product workflow, those failures are not cosmetic. They create false confidence and push teams toward implementation before the problem is grounded.

## Solution

The project implements a `SKILL.md` workflow that acts as the controller for early product discovery:

- Diagnostic Start for vague ideas.
- Material Assimilation for notes, PRDs, sketches, feedback, or research.
- Problem Framing, Solution Exploration, Feasibility Discovery, and MVP Hypothesis.
- Planning Artifacts only after readiness gates.
- Implementation Planning only after review-ready planning artifacts.

The workflow separates responsibilities:

- Workflow rules define the stage gates.
- Controller Agent applies routing and next-action rules.
- Producer Agents generate bounded artifacts.
- Auditor Agent checks evidence quality and boundary compliance.
- Runtime Workbench stores only current decision state, not full history.

## Evaluation System

The project uses reusable eval assets inside the skill package and promoted evidence outside the installable runtime.

Core mechanisms:

- deterministic checks for hard failures;
- structured rubric grading;
- post-test Value Gate;
- machine-readable report schemas;
- Baseline A/B template and scoring rubric.

## Evidence Dashboard

| Evidence | Result | Interpretation |
|---|---|---|
| `v0.1.5` full strict suite | 22/22 pass, 0 hard failures, avg 93.73, lowest 90 | Core regression confidence for trigger, stage-gate, boundary, audit, and context-economy behavior |
| `v0.1.6` Windows relay | 8 pass, 0 hard failures | Found real Windows/package/runtime-context issues |
| `v0.1.7` targeted rerun | 4 pass, 1 partial, 0 hard failures, avg 89 | Verified fixes and exposed final PRD user-gate / packaging documentation gaps |
| `v0.1.9` Baseline A/B | skill avg 95.7 vs baseline avg 68.4, delta +27.3, 0 skill hard failures | Scenario-scoped improvement in stage gates, source/package boundaries, and user-gate behavior |

## Baseline A/B Result

The v0.1.9 A/B compared ordinary assistant behavior against the skill workflow on 10 paired scenarios.

Result:

- Baseline average: 68.4
- Skill average: 95.7
- Average delta: +27.3
- Skill wins: 8
- Baseline wins: 0
- Ties: 2
- Skill hard failures: 0

The largest improvements appeared in:

- rejecting premature full PRD/Roadmap/Implementation Plan requests;
- keeping `vendor/` as source snapshots rather than active route targets;
- separating GitHub evidence archives from installable runtime packages;
- keeping PRD Draft target users, MVP scope, and positioning as candidate assumptions until user acceptance.

## Engineering Decisions

- Kept eval run artifacts outside the installable skill zip to avoid runtime context bloat.
- Used versioned evidence directories so release decisions can be traced.
- Added explicit claim boundaries to avoid overstating validation.
- Preserved external source transparency while preventing upstream files from becoming runtime route targets.

## Claim Boundary

Supported:

- The workflow improves behavior in the tested early discovery and boundary-control scenarios.
- The project demonstrates multi-agent workflow design, evaluation discipline, and release gating.
- The A/B evidence is useful for portfolio and non-commercial installable showcase use.

Not supported:

- production-grade reliability;
- release-grade validation;
- cross-model superiority;
- long-term real-user workflow quality.

