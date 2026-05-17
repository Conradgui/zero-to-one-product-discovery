# v0.1.6 Windows Clean-Install Summary Report

Run ID: `2026-05-17-windows-clean-install-run-01`

## Purpose

This report summarizes the first Windows clean-install relay validation for `zero-to-one-product-discovery`. The run targeted the `v0.1.6` handoff package; its follow-up fixes are applied in the `v0.1.7` closeout patch.

The run tested whether a clean Windows Codex installation can:

- trigger the skill for early zero-to-one product discovery;
- avoid triggering for code review, existing MVP fixes, skill maintenance, and vendor/source-governance prompts;
- preserve multi-turn stage gates through a realistic product-discovery flow;
- keep package/runtime/evidence boundaries clear.

## Result

| Metric | Result |
|---|---:|
| Relay scenarios | 8 |
| Passed scenarios | 8 |
| Hard failures | 0 |
| Average score | 91.75 |
| Lowest score | 82 |
| Install candidate | false |

Interpretation: the Windows run is valuable validation evidence, but it is not release-grade proof and does not yet support an install-candidate claim.

## What Worked

- Positive trigger scenarios entered early discovery and avoided PRD, Roadmap, or coding.
- Negative controls for code review and existing MVP fixes did not trigger product discovery.
- Vendor/source-governance boundary was correctly preserved: `vendor/` remained source-only and `child-skills/` remained the routeable surface.
- The multi-turn E2E flow reached `PRD Draft` without labeling it final or entering implementation planning.
- Evidence and assumptions were usually separated, especially in the early E2E turns.

## Issues Found

### 1. Root GitHub Install URL Was Wrong

The README previously suggested installing from the repository root. The local skill-installer requires a path that contains `SKILL.md`; this project keeps the runtime skill in the `zero-to-one-product-discovery/` subdirectory.

Fix applied:

```text
https://github.com/Conradgui/zero-to-one-product-discovery/tree/main/zero-to-one-product-discovery
```

### 2. PowerShell Packaging Needed Explicit Support

Windows validation exposed that Unix `zip` instructions are not enough for Windows users.

Fix applied in `v0.1.7`: README now includes a PowerShell `Compress-Archive` command.

### 3. Promotion Path Was Version-Hardcoded

The pressure-test protocol still pointed promoted runs to:

```text
current/v0.1.5/<run-id>/
```

Fix applied:

```text
current/<tested-version>/<run-id>/
```

### 4. Maintenance Negative Control Mutated The Installed Skill

The N3 prompt correctly stayed out of product discovery, but the Windows assistant edited files inside the installed skill directory. This contaminated the clean-install environment and required a reset before N4 and E2E.

Fix applied in `v0.1.7`: the Windows test packet now instructs maintainers to request review-only maintenance output during clean-install validation and to stop if file edits are proposed or performed.

### 5. Minor Runtime Behavior Drift

The run exposed two non-blocking behavior issues:

- P3 surfaced `superpowers:brainstorming` in a user-facing response, which can make the platform-agnostic workflow look host-specific.
- E2E turns 3-4 used strong recommendation language before explicit user acceptance.

Fix applied in `v0.1.7`: `SKILL.md` now says optional host helper tools should remain invisible unless explicitly invoked, and strong recommendations remain candidate directions until user-gated acceptance.

## PowerShell Adaptation Notes

Windows packaging should use:

```powershell
$Version = "v0.1.7"
New-Item -ItemType Directory -Force -Path dist | Out-Null
Compress-Archive -Path zero-to-one-product-discovery -DestinationPath "dist/zero-to-one-product-discovery-skill-$Version.zip" -Force
```

Zip validation should confirm the package excludes:

```text
zero-to-one-product-discovery-eval-runs/
.git/
tmp/
dist/
```

## Remaining Claim Boundary

Supported after this run and patch:

- `v0.1.6` has Windows clean-install relay evidence with 0 hard failures, and `v0.1.7` applies the resulting closeout patch.
- Positive trigger, negative-control, vendor boundary, and multi-turn draft behavior are directionally validated.
- The run produced concrete cross-platform documentation and protocol fixes.

Still unsupported:

- Install-candidate status.
- Release-grade validation.
- Baseline superiority.
- Fully stable real-user multi-turn product quality.

## Evidence Index

- `raw.md`: relayed Windows raw responses.
- `scored-report.json`: structured scenario scoring.
- `value-review.json`: evidence value review.
- `promotion-decision.md`: promotion decision and claim boundary.
