"""Execution Bridge contract tests.

The bridge may prepare host-execution payloads, but it must not pretend that
external GitHub/Jira actions already happened without explicit user approval.
"""

from __future__ import annotations

import copy
import importlib.util
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


def _handoff_example() -> dict:
    schema = vc.load_json(EVALS_DIR / "execution-handoff.schema.json")
    return copy.deepcopy(schema["examples"][0])


def _validate_handoff(handoff: dict) -> None:
    schema = vc.load_json(EVALS_DIR / "execution-handoff.schema.json")
    vc.validate_instance(handoff, schema, schema, "execution_handoff")


def _assert_no_unapproved_host_execution(handoff: dict) -> None:
    host_execution = handoff["host_execution"]
    if handoff["mode"] == "host_executed" and not host_execution["requires_explicit_user_approval"]:
        raise AssertionError("host_executed mode requires explicit user approval")
    if handoff["mode"] == "dry_run":
        for task in handoff["tasks"]:
            if task["external_ref"] is not None:
                raise AssertionError("dry_run tasks must not contain created external refs")


class TestExecutionHandoffContract(unittest.TestCase):
    def test_P0_005__execution_handoff_requires_confirmation_boundary(self):
        handoff = _handoff_example()
        _validate_handoff(handoff)

        self.assertEqual(handoff["mode"], "dry_run")
        self.assertTrue(handoff["host_execution"]["requires_explicit_user_approval"])
        self.assertIn("review_payload", handoff["host_execution"]["allowed_host_actions"])
        self.assertIn("create_github_issues", handoff["host_execution"]["allowed_host_actions"])

        for task in handoff["tasks"]:
            self.assertIsNone(task["external_ref"])
            self.assertGreater(len(task["acceptance_criteria"]), 0)
            self.assertGreater(len(task["verification_commands"]), 0)

    def test_security_execution_bridge__dry_run_required_without_user_approval(self):
        handoff = _handoff_example()
        handoff["mode"] = "host_executed"
        handoff["host_execution"]["requires_explicit_user_approval"] = False

        _validate_handoff(handoff)
        with self.assertRaises(AssertionError):
            _assert_no_unapproved_host_execution(handoff)

    def test_junction_execution_handoff__action_names_are_known_host_actions(self):
        handoff = _handoff_example()
        allowed = set(handoff["host_execution"]["allowed_host_actions"])

        self.assertEqual(
            allowed,
            {"review_payload", "create_github_issues", "record_external_refs"},
        )
        for command in handoff["host_execution"]["suggested_commands"]:
            self.assertIn("gh issue create", command)

    def test_P0_005__execution_handoff_preserves_evidence_context(self):
        handoff = _handoff_example()
        _validate_handoff(handoff)

        task = handoff["tasks"][0]
        self.assertEqual(task["evidence_context"]["assumption_status"], "assumption")
        self.assertGreater(len(task["evidence_context"]["validation_needed"]), 0)
        self.assertIn("evidence-assumption", task["labels"])


if __name__ == "__main__":
    unittest.main()
