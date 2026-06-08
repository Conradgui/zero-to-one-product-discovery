"""Revision Trace boundary tests.

Revision records are audit breadcrumbs, not a transcript/history database.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from tests.fixtures import SCRIPTS_DIR


def _load_revision_trace():
    spec = importlib.util.spec_from_file_location(
        "z2o_generate_revision_trace", SCRIPTS_DIR / "generate_revision_trace.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


grt = _load_revision_trace()


def _make_export_root(tmpdir: Path) -> Path:
    root = tmpdir / "export"
    root.mkdir(parents=True, exist_ok=True)
    (root / "prd.md").write_text("# PRD\n\nScoped content.\n", encoding="utf-8")
    (root / "roadmap.md").write_text("# Roadmap\n\nScoped content.\n", encoding="utf-8")
    (root / "user-stories.md").write_text("# User Stories\n\nScoped content.\n", encoding="utf-8")
    (root / "implementation-plan.md").write_text(
        "# Implementation Plan\n\nScoped content.\n", encoding="utf-8"
    )
    return root


class TestRevisionTraceBoundaries(unittest.TestCase):
    def test_junction_revision_trace__record_never_contains_full_transcript_or_hidden_reasoning(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            export_root = _make_export_root(Path(tmpdir))
            ns = argparse.Namespace(export_root=str(export_root), previous_root=None, metadata=None)

            paths = grt.build_revision(ns)
            record = json.loads(paths["record"].read_text(encoding="utf-8"))

        self.assertEqual(
            record["prohibited_content"],
            {
                "full_transcript": False,
                "full_agent_packets": False,
                "full_audit_reports": False,
                "hidden_reasoning": False,
            },
        )
        serialized = json.dumps(record, ensure_ascii=False).lower()
        self.assertNotIn("full transcript", serialized)
        self.assertNotIn("hidden reasoning", serialized)
        self.assertNotIn("assistant:", serialized)
        self.assertNotIn("user:", serialized)

    def test_junction_revision_trace__record_and_index_reference_each_other(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            export_root = _make_export_root(Path(tmpdir))
            ns = argparse.Namespace(export_root=str(export_root), previous_root=None, metadata=None)

            paths = grt.build_revision(ns)
            index = json.loads(paths["index"].read_text(encoding="utf-8"))
            record = json.loads(paths["record"].read_text(encoding="utf-8"))

        self.assertEqual(index["latest_revision_id"], record["revision_id"])
        self.assertEqual(index["latest_revision_record"], str(paths["record"].relative_to(export_root)))
        self.assertEqual(index["trace_store"]["ref"], "revisions/")

    def test_isolation_revision_trace__does_not_write_revision_data_into_workbench(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            export_root = _make_export_root(tmp_path)
            workbench_dir = export_root / "workbench"
            workbench_dir.mkdir(parents=True)
            before = sorted(p.relative_to(export_root) for p in workbench_dir.rglob("*"))

            ns = argparse.Namespace(export_root=str(export_root), previous_root=None, metadata=None)
            grt.build_revision(ns)
            after = sorted(p.relative_to(export_root) for p in workbench_dir.rglob("*"))

        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
