"""Artifact export boundary tests.

These tests verify user-facing export guards: unready artifacts stay clearly
marked, and Quick Mode drafts cannot masquerade as accepted artifacts.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest

from tests.fixtures import EVALS_DIR, SCRIPTS_DIR


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "z2o_validate_contracts", SCRIPTS_DIR / "validate-contracts.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


vc = _load_validator()


def _manifest_example() -> dict:
    schema = vc.load_json(EVALS_DIR / "artifact-manifest.schema.json")
    return copy.deepcopy(schema["examples"][0])


def _validate_manifest(manifest: dict) -> None:
    schema = vc.load_json(EVALS_DIR / "artifact-manifest.schema.json")
    vc.validate_instance(manifest, schema, schema, "artifact_manifest")


def _artifact(manifest: dict, name: str) -> dict:
    for item in manifest["artifacts"]:
        if item["name"] == name:
            return item
    raise AssertionError(f"missing artifact: {name}")


class TestArtifactManifestBoundaries(unittest.TestCase):
    def test_P0_006__artifact_export_preserves_not_ready_status(self):
        manifest = _manifest_example()
        _validate_manifest(manifest)

        implementation_plan = _artifact(manifest, "implementation-plan")

        self.assertEqual(implementation_plan["status"], "not_ready")
        self.assertEqual(implementation_plan["content_mode"], "not_ready_marker")
        self.assertEqual(implementation_plan["status_guard"], "not_ready_marker_only")
        self.assertGreater(len(implementation_plan["blockers"]), 0)
        self.assertGreater(len(implementation_plan["required_inputs"]), 0)

    def test_P0_006__not_ready_markdown_requires_blocker_and_single_required_input(self):
        content = """# NOT_READY: Implementation Plan

## Status
not_started

## Blocker
Implementation Plan is not review-ready.

## Required Input
- Accepted Roadmap and acceptance criteria.

## Controller Decision
request_evidence
"""

        self.assertTrue(content.startswith("# NOT_READY: Implementation Plan"))
        self.assertIn("## Blocker", content)
        self.assertIn("## Required Input", content)
        self.assertIn("## Controller Decision", content)
        self.assertNotIn("## Final Requirements", content)

    def test_P0_006__quick_mode_export_requires_banner_and_manifest_guard(self):
        manifest = _manifest_example()
        quick_draft = _artifact(manifest, "prd")
        quick_draft.update(
            {
                "status": "ready_for_review",
                "source_status": "quick_mode_draft",
                "content_mode": "quick_mode_draft",
                "status_guard": "quick_mode_banner_required",
                "blockers": [
                    "Quick Mode draft has not been validated in Standard Exploration."
                ],
                "required_inputs": [
                    "Controller/user validation outside Quick Mode."
                ],
            }
        )
        manifest["export_status"] = "partial"
        manifest["controller_decision"] = "downgrade"

        _validate_manifest(manifest)

        quick_mode_content = """# QUICK_MODE_DRAFT: PRD

This artifact was produced in Quick Mode. Treat `[Fact]`, `[Assumption]`,
and `[Unknown]` labels as binding until the Controller validates the draft in
Standard Exploration.
"""
        self.assertTrue(quick_mode_content.startswith("# QUICK_MODE_DRAFT: PRD"))
        self.assertEqual(quick_draft["source_status"], "quick_mode_draft")
        self.assertEqual(quick_draft["content_mode"], "quick_mode_draft")
        self.assertEqual(quick_draft["status_guard"], "quick_mode_banner_required")
        self.assertNotEqual(quick_draft["content_mode"], "accepted_artifact")

    def test_junction_artifact_manifest__content_missing_blocks_ready_status(self):
        manifest = _manifest_example()
        bad_entry = _artifact(manifest, "implementation-plan")
        bad_entry.update(
            {
                "status": "accepted",
                "source_status": "not_started",
                "content_mode": "not_ready_marker",
                "status_guard": "blocked_status_content_mismatch",
            }
        )

        _validate_manifest(manifest)
        self.assertEqual(bad_entry["status_guard"], "blocked_status_content_mismatch")
        self.assertNotEqual(
            bad_entry["status_guard"],
            "status_matches_content",
            "Accepted status with not-ready content must stay visibly blocked.",
        )


if __name__ == "__main__":
    unittest.main()
