# Zero-to-One Product Discovery Eval Runs

This directory is the public evidence archive for the `zero-to-one-product-discovery` project. It is intentionally outside the installable skill package.

Default rule: do not load these files during ordinary skill use. Use them only when reviewing validation evidence, preparing release notes, or writing portfolio/project material.

## Repository Boundary

These records should be committed to the GitHub repository when they are promoted as meaningful evidence. They should not be included in the skill zip that users install.

The installable skill should keep only reusable evaluation assets:

- `zero-to-one-product-discovery/evals/evals.json`
- `zero-to-one-product-discovery/evals/eval-rubric-template.md`
- `zero-to-one-product-discovery/evals/claude-code-pressure-test-protocol.md`
- `zero-to-one-product-discovery/evals/eval-report.schema.json`
- `zero-to-one-product-discovery/evals/value-review.schema.json`
- concise evidence interpretation in `zero-to-one-product-discovery/evals/evaluation-package.md`

Do not package raw responses, JSONL traces, long scored reports, handoff notes, or retrospective transcripts into the skill runtime.

## Layout

```text
archive/pre-v0.1.5/          Historical runs before the v0.1.5 multi-agent architecture.
archive/<version>/           Superseded but still useful evidence for a version.
current/v0.1.5/<run-id>/     Promoted v0.1.5 regression evidence worth reviewing.
current/v0.1.6/<run-id>/     Current handoff and external validation evidence.
current/v0.1.7/<run-id>/     Reserved for v0.1.7 reruns after the Windows closeout patch.
design-records/              Architecture and design decision records.
handoffs/                    Project status handoff notes.
tmp/<run-id>/                Scratch raw/report outputs before value review.
```

Archived records may contain historical paths from before this archive layout. Treat those paths as evidence context, not current file locations.

## Post-Test Value Gate

New test output starts in `tmp/<run-id>/`.

After raw generation, deterministic checks, and rubric grading, create a value review. Promote a run into `current/<version>/<run-id>/` only when it produces at least one of these useful signals:

- A real defect or regression in trigger behavior, stage gates, evidence grounding, child-skill routing, multi-agent orchestration, user gates, or context economy.
- A concrete improvement direction for `SKILL.md`, `references/`, `child-skills/`, `evals/`, packaging, or release criteria.
- Evidence that materially changes release, install, architecture, or quality decisions.
- A new scenario that should become part of the regression suite because it caught a realistic failure.

A run is not valuable evidence when it only says the suite passed, repeats expected behavior, gives generic praise, or does not identify any product-relevant risk or improvement.

## Promotion Policy

Use one of three decisions after value review:

| Decision | When To Use | What To Keep |
|---|---|---|
| `promote` | The run found a substantive issue, regression, or release-relevant confidence signal | Preserve raw responses or JSONL trace, scored report, value review, and promotion decision in `current/<version>/<run-id>/` |
| `minimal-note` | The run was clean but confirms a release gate that was previously unverified | Preserve a short note with metadata, aggregate score, and why full evidence was not retained |
| `discard-full-run` | The run adds no actionable information | Delete or leave only a transient local scratch copy in ignored `tmp/` |

Promotion requires enough metadata to interpret the run:

- Date and run ID.
- Skill version.
- Agent/tool and model, or `not exposed by CLI` when unavailable.
- Scenario set and git state.
- Known limitations.
- Link or path to any patch created from the findings.

## Minimum Valuable Run Contents

A promoted run should normally contain:

```text
raw.md or trace.jsonl
scored-report.json
value-review.json
promotion-decision.md
```

If a run uses manual scoring instead of JSON output, preserve the same sections in Markdown and clearly label it as manual.

## Current Evidence Policy

For `v0.1.5`, `current/v0.1.5/2026-05-12-run-01/` is the first fresh strict-suite run, `current/v0.1.5/2026-05-14-run-02/` is a targeted boundary rerun that closes the package/vendor findings from that run, and `current/v0.1.5/2026-05-14-run-03/` is the patched full strict-suite rerun.

For run-03, read `current/v0.1.5/2026-05-14-run-03/summary-report.md` first. It is the human-readable entry point. `scored-report.json` and `value-review.json` remain the machine-readable scoring and value-review sources of truth.

For `v0.1.6`, `current/v0.1.6/2026-05-14-windows-clean-install-handoff/` contains the Windows relay test packet and response template. The first returned Windows run is promoted at `current/v0.1.6/2026-05-17-windows-clean-install-run-01/`. `v0.1.7` is the follow-up patch release that applies the findings from that run; any post-patch rerun should be stored under `current/v0.1.7/<run-id>/`.

Read the Windows run in this order:

1. `summary-report.md`
2. `promotion-decision.md`
3. `value-review.json`
4. `scored-report.json`
5. `raw.md`

These records are valuable GitHub project evidence, but they are not release-grade proof by themselves. The patched full suite and first Windows relay run have passed without hard failures, and `v0.1.7` applies the first relay follow-up patches. A post-patch Windows rerun and baseline-vs-skill comparison are still needed before install-candidate or stronger public claims.
