# v0.1.6 Windows Clean-Install Handoff Status

Run ID: `2026-05-14-windows-clean-install-handoff`

## Status

`pending_external_raw_responses`

## Purpose

This handoff prepares `v0.1.6` for clean Windows Codex validation through a human relay.

`v0.1.6` is not an install candidate yet. It is a clean handoff version that packages the runtime skill, preserves the `v0.1.5` strict-suite evidence, and provides a test packet for a separate Windows environment.

## Local Precheck Completed

The local Mac workspace precheck covers only package and documentation boundaries:

- `v0.1.5` zip restored as historical artifact.
- `v0.1.6` docs prepared for Windows clean-install validation.
- `v0.1.6` test packet prepared for human relay.
- `v0.1.6` package must exclude `zero-to-one-product-discovery-eval-runs/`, `.git/`, and `tmp/`.

## External Evidence Pending

The following evidence must come from the Windows Codex environment before stronger claims:

- Fresh post-install positive trigger responses.
- Fresh post-install negative trigger responses.
- Raw multi-turn end-to-end discovery transcript.
- Scored report, value review, and promotion decision generated from those raw responses.

## Claim Boundary

Supported now:

- `v0.1.6` is ready for Windows clean-install validation.
- `v0.1.5` remains the latest strict-suite regression evidence.
- The repository has a structured relay protocol for collecting external clean-environment evidence.

Unsupported now:

- Install-candidate status.
- Release-grade validation.
- Cross-client natural trigger reliability.
- Baseline superiority.
