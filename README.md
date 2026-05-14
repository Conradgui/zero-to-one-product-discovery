# Zero-to-One Product Discovery

This repository contains the `zero-to-one-product-discovery` AI workflow skill and its public evaluation evidence.

The installable skill lives in:

```text
zero-to-one-product-discovery/
```

Evaluation runs, design records, and validation evidence live outside the installable skill package in:

```text
zero-to-one-product-discovery-eval-runs/
```

## Current Version

Current version: `v0.1.5`

Status: development / evaluation build. The patched full strict suite has passed, but `v0.1.5` is not yet an install candidate because clean install and natural trigger validation are still pending.

## Where To Start

| Need | File |
|---|---|
| Skill overview, install instructions, architecture, packaging rules | [`zero-to-one-product-discovery/README.md`](zero-to-one-product-discovery/README.md) |
| Runtime workflow instructions | [`zero-to-one-product-discovery/SKILL.md`](zero-to-one-product-discovery/SKILL.md) |
| Multi-agent orchestration protocol | [`zero-to-one-product-discovery/references/multi-agent-orchestration.md`](zero-to-one-product-discovery/references/multi-agent-orchestration.md) |
| Evaluation protocol and strict suite | [`zero-to-one-product-discovery/evals/`](zero-to-one-product-discovery/evals/) |
| Public evaluation evidence archive | [`zero-to-one-product-discovery-eval-runs/README.md`](zero-to-one-product-discovery-eval-runs/README.md) |
| Latest human-readable evaluation report | [`zero-to-one-product-discovery-eval-runs/current/v0.1.5/2026-05-14-run-03/summary-report.md`](zero-to-one-product-discovery-eval-runs/current/v0.1.5/2026-05-14-run-03/summary-report.md) |
| Packaged zip artifacts | [`dist/`](dist/) |

## Validation Snapshot

Latest promoted full-suite run:

```text
zero-to-one-product-discovery-eval-runs/current/v0.1.5/2026-05-14-run-03/
```

Result:

- 22 / 22 scenarios passed.
- 0 hard failures.
- Average score: 93.73.
- Median score: 94.
- Lowest score: 90.
- `install_candidate = false`.

This supports core regression confidence for `v0.1.5`, but does not prove clean global-install behavior or baseline superiority.

## Installable Package Boundary

User installation should use only the runtime skill folder or versioned zip:

```text
zero-to-one-product-discovery/
dist/zero-to-one-product-discovery-skill-v0.1.5.zip
```

Do not include `zero-to-one-product-discovery-eval-runs/` in the installable skill package. Those files are public project evidence for GitHub review, not runtime context.

## Source And License Notes

The skill uses a copy-first source strategy. Upstream source snapshots are preserved under `zero-to-one-product-discovery/vendor/` for attribution, review, and adapter development. They are not active child-skill routes.

Before redistribution or commercial use, review:

- [`zero-to-one-product-discovery/vendor/MANIFEST.md`](zero-to-one-product-discovery/vendor/MANIFEST.md)
- [`zero-to-one-product-discovery/references/source-attribution.md`](zero-to-one-product-discovery/references/source-attribution.md)
- upstream licenses in `vendor/`
