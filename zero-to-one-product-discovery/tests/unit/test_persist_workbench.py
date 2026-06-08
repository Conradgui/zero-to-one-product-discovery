"""test_persist_workbench.py — persist_workbench.py 全分支测试

覆盖用例：
  1.  有效 workbench 通过校验并写入
  2.  输入不是 JSON 对象时报错
  3.  缺少必填字段时报错
  4.  evidence item id 重复时报错
  5.  summary.facts 与实际数量不匹配时报错
  6.  maturity_percentage 计算精度正确
  7.  maturity_level 映射正确
  8.  highest_risk_item_id 正确识别
  9.  无 evidence item 时 maturity 为 0
  10. 路径在 skill 目录内时拒绝写入
  11. 路径在 skill 目录外时允许写入
  12. 原子写入后文件内容完整
  13. 原子写入后临时文件被清理
  14. 输入文件不存在时报错
"""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

from tests.fixtures import (
    EVALS_DIR,
    ROOT_DIR,
    SCRIPTS_DIR,
    make_evidence_item,
    make_valid_workbench_json,
    make_workbench,
)

# ── 动态加载被测模块 ──
def _load_module():
    spec = importlib.util.spec_from_file_location(
        "z2o_persist_workbench", SCRIPTS_DIR / "persist_workbench.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

pw = _load_module()


class TestValidInput(unittest.TestCase):
    """用例 1：有效 workbench 通过校验并写入"""

    def test_valid_workbench_passes_validation(self):
        """有效 workbench JSON 能通过 validate_workbench"""
        wb = make_valid_workbench_json()
        result = pw.validate_workbench(wb)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["workflow_state"]["current_stage"], "Problem Framing")


class TestInputTypeValidation(unittest.TestCase):
    """用例 2-3：输入类型和完整性"""

    def test_non_object_input_raises_error(self):
        """用例 2：输入不是 dict 时报错"""
        with self.assertRaises(pw.PersistError):
            pw.validate_workbench([1, 2, 3])

    def test_missing_required_field_raises_error(self):
        """用例 3：缺少必填字段 evidence_snapshot 时报错"""
        wb = make_valid_workbench_json()
        del wb["evidence_snapshot"]
        with self.assertRaises(Exception):  # ValidationError from schema
            pw.validate_workbench(wb)


class TestEvidenceSummaryConsistency(unittest.TestCase):
    """用例 4-9：evidence summary 一致性校验"""

    def test_duplicate_item_id_raises_error(self):
        """用例 4：evidence item id 重复时报错"""
        items = [
            make_evidence_item("ev-001", "fact", "verified"),
            make_evidence_item("ev-001", "assumption", "unverified"),  # 重复 id
        ]
        wb = make_workbench(items)
        with self.assertRaises(pw.PersistError) as ctx:
            pw.validate_workbench(wb)
        self.assertIn("Duplicate evidence item id", str(ctx.exception))

    def test_facts_count_mismatch_raises_error(self):
        """用例 5：summary.facts 与实际 fact 数量不匹配时报错"""
        items = [
            make_evidence_item("ev-001", "fact", "verified"),
            make_evidence_item("ev-002", "assumption", "unverified"),
        ]
        # summary 说有 3 个 fact，实际只有 1 个
        wb = make_workbench(items, summary_overrides={"facts": 3})
        with self.assertRaises(pw.PersistError) as ctx:
            pw.validate_workbench(wb)
        self.assertIn("facts", str(ctx.exception))

    def test_maturity_percentage_precision(self):
        """用例 6：maturity_percentage 计算精度正确（1/3 = 33.33）"""
        items = [
            make_evidence_item("ev-001", "fact", "verified"),
            make_evidence_item("ev-002", "assumption", "unverified"),
            make_evidence_item("ev-003", "unknown", "unverified"),
        ]
        # 1 verified out of 3 = 33.33%
        wb = make_workbench(items)
        snapshot = wb["evidence_snapshot"]["summary"]
        self.assertAlmostEqual(snapshot["maturity_percentage"], 33.33, places=2)

    def test_maturity_level_mapping(self):
        """用例 7：maturity_level 映射正确"""
        test_cases = [
            (0, "insufficient"),
            (24, "insufficient"),
            (25, "partial"),
            (49, "partial"),
            (50, "sufficient"),
            (74, "sufficient"),
            (75, "sufficient"),  # 75 不算 >75
            (76, "strong"),
            (100, "strong"),
        ]
        for pct, expected_level in test_cases:
            with self.subTest(percentage=pct):
                result = pw.expected_maturity_level(float(pct))
                self.assertEqual(result, expected_level)

    def test_highest_risk_item_id_correctly_identified(self):
        """用例 8：highest_risk_item_id 正确识别最高优先级"""
        items = [
            make_evidence_item("ev-low", "assumption", "unverified", "low", 0.1),
            make_evidence_item("ev-high", "risk", "unverified", "critical", 0.9),
            make_evidence_item("ev-med", "assumption", "unverified", "medium", 0.5),
        ]
        wb = make_workbench(items)
        snapshot = wb["evidence_snapshot"]["summary"]
        self.assertEqual(snapshot["highest_risk_item_id"], "ev-high")

    def test_empty_items_maturity_zero(self):
        """用例 9：无 evidence item 时 maturity 为 0"""
        wb = make_workbench(items=[])
        # validate_workbench 应该通过，maturity = 0
        result = pw.validate_workbench(wb)
        summary = result["evidence_snapshot"]["summary"]
        self.assertEqual(summary["total"], 0)
        self.assertEqual(summary["maturity_percentage"], 0)
        self.assertEqual(summary["maturity_level"], "insufficient")


class TestPathSafety(unittest.TestCase):
    """用例 10-11：路径安全检查"""

    def test_refuse_write_inside_skill_directory(self):
        """用例 10：路径在 skill 目录内时拒绝写入"""
        target = ROOT_DIR / ".z2o-state" / "workbench.json"
        with self.assertRaises(pw.PersistError) as ctx:
            pw.ensure_target_allowed(target)
        self.assertIn("Refusing to write", str(ctx.exception))

    def test_allow_write_outside_skill_directory(self):
        """用例 11：路径在 skill 目录外时允许写入"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / ".z2o-state" / "workbench.json"
            pw.ensure_target_allowed(target)  # 不抛异常即通过


class TestAtomicWrite(unittest.TestCase):
    """用例 12-13：原子写入行为"""

    def test_written_file_content_matches_input(self):
        """用例 12：写入后文件内容与输入一致"""
        wb = make_valid_workbench_json()
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "workbench.json"
            pw.atomic_write_json(target, wb)
            self.assertTrue(target.exists())
            written = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(written, wb)

    def test_no_temp_files_left_behind(self):
        """用例 13：写入后无临时文件残留"""
        wb = make_valid_workbench_json()
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "workbench.json"
            pw.atomic_write_json(target, wb)
            tmp_files = list(Path(tmpdir).glob(".workbench.*.tmp"))
            self.assertEqual(len(tmp_files), 0, f"残留临时文件: {tmp_files}")


class TestMissingInput(unittest.TestCase):
    """用例 14：输入文件不存在"""

    def test_nonexistent_input_file_raises_error(self):
        """用例 14：指定的输入文件不存在时报错"""
        fake_path = Path("/nonexistent/path/workbench.json")
        with self.assertRaises((OSError, json.JSONDecodeError)):
            pw.load_json(fake_path)


if __name__ == "__main__":
    unittest.main()
