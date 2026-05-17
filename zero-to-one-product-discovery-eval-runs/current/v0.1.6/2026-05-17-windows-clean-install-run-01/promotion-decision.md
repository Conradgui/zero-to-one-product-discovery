# Promotion Decision

Run ID: `2026-05-17-windows-clean-install-run-01`

Tested version: `v0.1.6`
Follow-up patch version: `v0.1.7`

Decision: `promote`

## Rationale

This run is valuable project evidence because it came from a separate Windows Codex environment after clean installation and produced raw responses for positive triggers, negative controls, vendor boundary behavior, and a multi-turn end-to-end scenario.

The run did not reveal hard failures in core product-discovery behavior:

- Positive trigger scenarios entered discovery without jumping to implementation.
- Negative controls avoided product discovery.
- `vendor/` remained source-only and not routeable.
- The E2E workflow produced `PRD Draft`, not final PRD, Roadmap, or Implementation Plan.

The run also found actionable improvements:

- Maintenance negative-control prompts can mutate the installed skill and contaminate clean-install testing.
- The pressure-test protocol should not hard-code `current/v0.1.5/<run-id>/`.
- Windows packaging and install documentation should be clearer.
- The workflow should reduce visible host-specific helper-skill references and mild advisor overreach.

## Claim Boundary

Supported:

- `v0.1.6` has Windows clean-install relay evidence for core trigger and boundary behavior.
- `v0.1.7` applies the closeout patch from this run.
- The skill maintained package/runtime/evidence boundaries in the tested scenarios.
- The run produced actionable improvements worth retaining.

Unsupported:

- Release-grade validation.
- Baseline superiority over ordinary model behavior.
- Fully stable multi-turn product quality.
- Install-candidate status without patching the findings and rerunning affected checks.

## Files Retained

```text
raw.md
scored-report.json
value-review.json
promotion-decision.md
```

## Required Follow-Up

Patch the repository before the next release candidate:

1. Fix GitHub install instructions to use the skill subdirectory URL.
2. Make pressure-test promotion paths version-aware.
3. Update Windows clean-install test packet to avoid mutation during negative controls.
4. Add a check for visible host-specific helper-skill drift.
