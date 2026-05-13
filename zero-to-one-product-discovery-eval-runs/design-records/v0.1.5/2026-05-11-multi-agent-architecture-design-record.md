# Multi-Agent Architecture Design Record: 2026-05-11

## Purpose

Record the design decisions behind the multi-agent workflow refactor for `zero-to-one-product-discovery`. This file is an external project archive for review, resume storytelling, and future maintenance. It is not part of the installable skill package.

## Context

The project started as a zero-to-one product discovery workflow with local child-skill adapters for PRD, Roadmap, ADR, Research Brief, Implementation Plan, and related artifacts. The user identified two problems:

- The skill felt structurally noisy and repetitive.
- The child-skill layer lacked a clear multi-agent operating model, even though referenced upstream skill systems use agent roles, review gates, and parallelization patterns.

The user is new to skill and agent design and wants to act as a joint architect: they make product and architecture trade-off decisions, while Codex implements protocols, files, evaluations, and audit reports.

## Core Architecture Decision

Use this model:

```text
Workflow Rules = constitution / stage gates
Controller Agent = applies workflow rules and routes work
Producer Agents = create bounded artifacts
Auditor Agent = independently checks boundaries, evidence, and consistency
Runtime Workbench = current-state decision board
```

The controller is not a single super-agent that stores all raw communication. It reads bounded packets and keeps the user-facing workflow coherent.

## Accepted Decisions

1. Main control is `Workflow Rules + Controller Agent + Auditor Agent`, not one overloaded agent.
2. Producer agents communicate through the controller and Runtime Workbench, not direct free-form agent-to-agent chat.
3. The Runtime Workbench stores current decision state only. It does not store full transcripts or long histories.
4. User retrospectives use Audit Reports and optional Trace Reports. Trace Reports do not enter the real-time control path.
5. First producer set covers Research, PRD, Roadmap, ADR, and Implementation Plan.
6. Execution is stage-serial for production and locally parallel for review or consistency checks.
7. User gates are required only for stage upgrades, final artifact acceptance, major conflicts, ADR decisions, or blocking missing information.
8. Questioning is a loop: ask one highest-leverage question per turn, then continue until evidence is sufficient.
9. Multi-agent rules stay platform-agnostic and do not require Codex or Claude subagent APIs.

## Rejected Alternatives

### Full Meeting-Log Workbench

Rejected because it would make the controller read too much historical context and could degrade task completion quality. Detailed replay is useful for retrospectives, but should be generated as a Trace Report after the fact.

### Direct Producer-to-Producer Conversation

Rejected because it would let product artifacts amplify each other's assumptions and blur routing authority. Producers may raise dependencies or conflicts, but the controller decides what happens next.

### Single Super-Agent Controller

Rejected because one agent doing orchestration, production, audit, and memory management is more likely to become unstable. Separating controller and auditor gives clearer quality gates.

### Always-On ADR Generation

Rejected because ordinary product scope decisions should stay in the Decision Log. ADR is conditionally triggered only for durable technical, platform, data, security, deployment, dependency, or maintainability decisions.

## Protocol Shape

### Agent Work Order

Strict controller-to-producer task packet. It defines role, mission, current workflow state, input context, boundaries, required output, stop conditions, and return format.

### Agent Return Packet

Lightweight producer-to-controller packet. It contains status, output summary, evidence changes, blockers, conflicts, self-check, and recommended controller action.

### Runtime Workbench

Current-state board containing workflow state, evidence snapshot, artifact status, dependency board, conflict board, risk board, audit queue, and next controller action.

### Audit Report

User-readable review surface containing verdict, reviewed item, blocking issues, non-blocking issues, boundary check, evidence check, consistency check, and recommended next action.

### Trace Report

Optional retrospective summary used for review, resume material, or evaluation evidence. It is not runtime state.

## Resume / Portfolio Narrative

This project can be described as:

> Designed and implemented a platform-agnostic multi-agent workflow architecture for an AI product-discovery skill. The system separates workflow rules, controller execution, producer artifacts, independent auditing, and runtime state management. It uses strict work orders, lightweight return packets, current-state workbenches, and eval scenarios to prevent stage bypass, assumption leakage, and overproduction of ungrounded artifacts.

Potential bullet points:

- Built a hub-and-spoke AI workflow with gated producer agents for Research, PRD, Roadmap, ADR, and Implementation Planning.
- Designed lightweight agent communication protocols that avoid long transcript memory while preserving auditability.
- Added independent audit reports and eval scenarios for controller overreach, producer overreach, workbench overload, ADR qualification, and user gate omissions.
- Preserved installable skill cleanliness by keeping design records and pressure-test outputs outside the runtime package.

## Follow-up SOP Candidate

After the core five producers pass evaluation, create a repeatable SOP for extending the same pattern to User Stories, Acceptance Criteria, Mermaid, Review, and Context Handoff:

1. Define producer role and non-authority boundaries.
2. Define work order inputs and stop conditions.
3. Define concise return packet fields.
4. Add audit checks for stage, evidence, consistency, and output mode.
5. Add one eval scenario for producer overreach and one scenario for correct downgrade.
6. Run static review before claiming the adapter is route-ready.

## Versioning Note

This architecture is part of `v0.1.5`. `v0.1.0-draft` remains an early historical draft; the multi-agent workflow architecture is a larger versioned upgrade and should not be backfilled into the earlier draft version. Future package uploads, GitHub Releases, and tags should use the same version string across:

- Git tag: `v0.1.5`
- Release name: `v0.1.5`
- Package file: `dist/zero-to-one-product-discovery-skill-v0.1.5.zip`

Temporary publish directories are working artifacts only and should not be committed.
