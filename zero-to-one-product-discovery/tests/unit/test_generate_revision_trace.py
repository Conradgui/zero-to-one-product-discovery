"""test_generate_revision_trace.py — generate_revision_trace.py 全分支测试

覆盖用例：
  1.  基线版本（无 previous-root）正确生成
  2.  有 previous-root 时正确计算 diff
  3.  artifact 内容未变时 diff 为空
  4.  正确计算 SHA-256 hash
  5.  Markdown section summary 正确识别变更类型
  6.  revision ID 自动去重
  7.  metadata 中 controller_decision 无效时报错
  8.  metadata 缺失时使用默认值
  9.  change_reason 为空时标记 missing
  10. 路径指向 .z2o-state 时报错
  11. 路径指向 .z2o-patterns 时报错
  12. 路径指向 eval-runs 时报错
  13. export-root 不存在时报错
  14. 正确生成 revision-index.json
  15. 正确追加 revision-log.md
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from tests.fixtures import ROOT_DIR, SCRIPTS_DIR

# ── 动态加载被测模块 ──
def _load_module():
    spec = importlib.util.spec_from_file_location(
        "z2o_generate_revision_trace", SCRIPTS_DIR / "generate_revision_trace.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

grt = _load_module()


def _make_export_root(tmpdir: Path, prd_content: str = "# PRD\n\nDefault content.\n") -> Path:
    """在临时目录中创建一个最小的 export root 结构。"""
    root = tmpdir / "export"
    root.mkdir(parents=True, exist_ok=True)
    (root / "prd.md").write_text(prd_content, encoding="utf-8")
    (root / "roadmap.md").write_text("# Roadmap\n\nPlaceholder.\n", encoding="utf-8")
    (root / "user-stories.md").write_text("# User Stories\n\nPlaceholder.\n", encoding="utf-8")
    (root / "implementation-plan.md").write_text("# Implementation Plan\n\nPlaceholder.\n", encoding="utf-8")
    return root


class TestBaselineRevision(unittest.TestCase):
    """用例 1：基线版本（无 previous-root）"""

    def test_baseline_revision_generates_correctly(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            export_root = _make_export_root(Path(tmpdir))
            args = grt.parse_args.__wrapped__ if hasattr(grt.parse_args, '__wrapped__') else None

            # 直接调用 build_revision
            import argparse
            ns = argparse.Namespace(
                export_root=str(export_root),
                previous_root=None,
                metadata=None,
            )
            paths = grt.build_revision(ns)

            # 验证生成了文件
            self.assertTrue(paths["index"].exists())
            self.assertTrue(paths["record"].exists())
            self.assertTrue(paths["log"].exists())

            # 验证 record 中 baseline=True
            record = json.loads(paths["record"].read_text(encoding="utf-8"))
            self.assertTrue(record["baseline"])
            self.assertEqual(record["package_version"], "v0.4.0-rc.4")


class TestDiffCalculation(unittest.TestCase):
    """用例 2-3：diff 计算"""

    def test_diff_generated_when_content_changes(self):
        """用例 2：有 previous-root 且内容改变时生成 diff"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            prev_root = _make_export_root(tmpdir, "# PRD\n\nOld content.\n")
            curr_root = _make_export_root(tmpdir / "curr", "# PRD\n\nNew content.\n")

            import argparse
            ns = argparse.Namespace(
                export_root=str(curr_root),
                previous_root=str(prev_root),
                metadata=None,
            )
            paths = grt.build_revision(ns)

            record = json.loads(paths["record"].read_text(encoding="utf-8"))
            self.assertIn("prd", record["changed_artifacts"])

            # 验证 diff 文件存在
            diffs_dir = paths["index"].parent / "diffs"
            diff_dirs = list(diffs_dir.iterdir())
            self.assertTrue(len(diff_dirs) > 0)

    def test_no_diff_when_content_unchanged(self):
        """用例 3：内容未变时 diff 为空"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            content = "# PRD\n\nSame content.\n"
            prev_root = _make_export_root(tmpdir, content)
            curr_root = _make_export_root(tmpdir / "curr", content)

            import argparse
            ns = argparse.Namespace(
                export_root=str(curr_root),
                previous_root=str(prev_root),
                metadata=None,
            )
            paths = grt.build_revision(ns)

            record = json.loads(paths["record"].read_text(encoding="utf-8"))
            self.assertEqual(record["changed_artifacts"], [])


class TestHashComputation(unittest.TestCase):
    """用例 4：SHA-256 hash 计算"""

    def test_sha256_hash_format(self):
        """hash 格式为 sha256:<hex>"""
        result = grt.sha256_text("hello world")
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("sha256:"))
        self.assertEqual(len(result), 71)  # "sha256:" (7) + 64 hex chars

    def test_sha256_none_input_returns_none(self):
        """None 输入返回 None"""
        self.assertIsNone(grt.sha256_text(None))

    def test_sha256_deterministic(self):
        """相同内容产生相同 hash"""
        h1 = grt.sha256_text("test content")
        h2 = grt.sha256_text("test content")
        self.assertEqual(h1, h2)

    def test_sha256_different_content_different_hash(self):
        """不同内容产生不同 hash"""
        h1 = grt.sha256_text("content A")
        h2 = grt.sha256_text("content B")
        self.assertNotEqual(h1, h2)


class TestSectionSummary(unittest.TestCase):
    """用例 5：Markdown section summary"""

    def test_identifies_added_removed_modified_unchanged(self):
        previous = "# Title\n\nOld intro.\n\n## Section A\n\nContent A.\n"
        current = "# Title\n\nNew intro.\n\n## Section A\n\nContent A.\n\n## Section B\n\nNew section.\n"
        summary = grt.summarize_sections(previous, current)
        summary_by_heading = {s["heading"]: s["change_type"] for s in summary}

        self.assertEqual(summary_by_heading["Title"], "modified")
        self.assertEqual(summary_by_heading["Section A"], "unchanged")
        self.assertEqual(summary_by_heading["Section B"], "added")

    def test_none_previous_treats_all_as_added(self):
        current = "# Title\n\nContent.\n"
        summary = grt.summarize_sections(None, current)
        for s in summary:
            self.assertEqual(s["change_type"], "added")

    def test_none_current_treats_all_as_removed(self):
        previous = "# Title\n\nContent.\n"
        summary = grt.summarize_sections(previous, None)
        for s in summary:
            self.assertEqual(s["change_type"], "removed")


class TestRevisionIdUniqueness(unittest.TestCase):
    """用例 6：revision ID 自动去重"""

    def test_unique_id_when_conflict_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            records_dir = tmpdir / "records"
            diffs_root = tmpdir / "diffs"
            records_dir.mkdir()
            diffs_root.mkdir()

            # 创建一个已存在的 revision
            base_id = "rev-20260605T120000Z"
            (records_dir / f"{base_id}.json").write_text("{}", encoding="utf-8")

            # 应该生成带后缀的 ID
            unique_id = grt.unique_revision_id(base_id, records_dir, diffs_root)
            self.assertNotEqual(unique_id, base_id)
            self.assertTrue(unique_id.startswith(base_id))


class TestMetadataValidation(unittest.TestCase):
    """用例 7-9：metadata 校验"""

    def test_invalid_controller_decision_raises_error(self):
        """用例 7：无效的 controller_decision 报错"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            metadata_path = tmpdir / "metadata.json"
            metadata_path.write_text(json.dumps({
                "controller_decision": "invalid_action_name",
            }), encoding="utf-8")

            with self.assertRaises(grt.RevisionError) as ctx:
                grt.normalize_metadata(metadata_path, tmpdir)
            self.assertIn("controller_decision", str(ctx.exception))

    def test_missing_metadata_uses_defaults(self):
        """用例 8：metadata 为 None 时使用默认值"""
        result = grt.normalize_metadata(None, Path("/tmp/test-project"))
        self.assertEqual(result["controller_decision"], "ask_user")
        self.assertEqual(result["change_reason_status"], "missing")
        self.assertEqual(result["evidence_refs"], [])
        self.assertEqual(result["project_slug"], "test-project")

    def test_empty_change_reason_marked_missing(self):
        """用例 9：change_reason 为空字符串时标记 missing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            metadata_path = tmpdir / "metadata.json"
            metadata_path.write_text(json.dumps({
                "controller_decision": "accept",
                "change_reason": "",
            }), encoding="utf-8")

            result = grt.normalize_metadata(metadata_path, tmpdir)
            self.assertEqual(result["change_reason_status"], "missing")
            self.assertIsNone(result["change_reason"])


class TestPathSafety(unittest.TestCase):
    """用例 10-12：路径安全检查"""

    def test_refuse_z2o_state_path(self):
        """用例 10：路径指向 .z2o-state 时报错"""
        with self.assertRaises(grt.RevisionError):
            grt.ensure_allowed_path(Path("/some/.z2o-state/workbench.json"), "test")

    def test_refuse_z2o_patterns_path(self):
        """用例 11：路径指向 .z2o-patterns 时报错"""
        with self.assertRaises(grt.RevisionError):
            grt.ensure_allowed_path(Path("/some/.z2o-patterns/index.json"), "test")

    def test_refuse_eval_runs_path(self):
        """用例 12：路径指向 eval-runs 时报错"""
        with self.assertRaises(grt.RevisionError):
            grt.ensure_allowed_path(
                Path("/some/zero-to-one-product-discovery-eval-runs/data.json"), "test"
            )

    def test_allow_normal_export_path(self):
        """正常导出路径不报错"""
        grt.ensure_allowed_path(Path("/tmp/z2o-artifacts/my-project/prd.md"), "test")


class TestInputValidation(unittest.TestCase):
    """用例 13：输入校验"""

    def test_nonexistent_export_root_raises_error(self):
        """用例 13：export-root 不存在时报错"""
        import argparse
        ns = argparse.Namespace(
            export_root="/nonexistent/path",
            previous_root=None,
            metadata=None,
        )
        with self.assertRaises(grt.RevisionError) as ctx:
            grt.build_revision(ns)
        self.assertIn("does not exist", str(ctx.exception))


class TestOutputFiles(unittest.TestCase):
    """用例 14-15：输出文件完整性"""

    def test_revision_index_json_structure(self):
        """用例 14：revision-index.json 结构正确"""
        with tempfile.TemporaryDirectory() as tmpdir:
            export_root = _make_export_root(Path(tmpdir))
            import argparse
            ns = argparse.Namespace(
                export_root=str(export_root),
                previous_root=None,
                metadata=None,
            )
            paths = grt.build_revision(ns)
            index = json.loads(paths["index"].read_text(encoding="utf-8"))

            self.assertIn("schema_version", index)
            self.assertIn("package_version", index)
            self.assertIn("latest_revision_id", index)
            self.assertIn("artifacts", index)
            self.assertIn("records", index)
            self.assertEqual(len(index["artifacts"]), 4)  # 4 stable artifacts

    def test_revision_log_appends(self):
        """用例 15：revision-log.md 追加而非覆盖"""
        with tempfile.TemporaryDirectory() as tmpdir:
            export_root = _make_export_root(Path(tmpdir))
            import argparse

            # 第一次生成
            ns1 = argparse.Namespace(
                export_root=str(export_root),
                previous_root=None,
                metadata=None,
            )
            grt.build_revision(ns1)
            log_path = export_root / "revisions" / "revision-log.md"
            first_content = log_path.read_text(encoding="utf-8")

            # 第二次生成（内容不变，所以用相同 export root）
            ns2 = argparse.Namespace(
                export_root=str(export_root),
                previous_root=None,
                metadata=None,
            )
            grt.build_revision(ns2)
            second_content = log_path.read_text(encoding="utf-8")

            # 第二次内容应该比第一次长（追加了新记录）
            self.assertGreater(len(second_content), len(first_content))
            self.assertIn("rev-", second_content)


if __name__ == "__main__":
    unittest.main()
