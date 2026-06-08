"""test_validate_contracts.py — validate-contracts.py 全分支测试

覆盖用例：
  1.  所有 9 个 schema 有必需顶层字段
  2.  所有 schema 的 examples 通过自身校验
  3.  controller-actions.json 非空且唯一
  4.  controller-actions.json 版本号匹配
  5.  schema 中 controller action enum 与 registry 一致
  6.  evals.json 包含所有必需场景
  7.  evals.json 场景数 ≥ 39
  8.  evals.json 版本号匹配
  9.  packaging boundary：无运行时状态目录
  10. schema 文件不存在时报错
  11. evals.json 格式错误时报错
  12. controller-actions.json 格式错误时报错
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.fixtures import EVALS_DIR, ROOT_DIR, SCRIPTS_DIR

# ── 动态加载被测模块 ──
def _load_module():
    spec = importlib.util.spec_from_file_location(
        "z2o_validate_contracts", SCRIPTS_DIR / "validate-contracts.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

vc = _load_module()


class TestSchemaStructure(unittest.TestCase):
    """用例 1-2：schema 文件结构和 examples 自校验"""

    def test_all_schemas_have_required_top_level_keys(self):
        """用例 1：所有 9 个 schema 都有 $schema, title, type, required, properties"""
        for filename in vc.SCHEMA_FILES:
            path = EVALS_DIR / filename
            with self.subTest(schema=filename):
                schema = vc.load_json(path)
                for key in ("$schema", "title", "type", "required", "properties"):
                    self.assertIn(key, schema, f"{filename} 缺少顶层字段 {key!r}")

    def test_all_schema_examples_pass_self_validation(self):
        """用例 2：所有 schema 的 examples 能通过自身校验"""
        for filename in vc.SCHEMA_FILES:
            path = EVALS_DIR / filename
            with self.subTest(schema=filename):
                # validate_schema_file 内部会校验 examples
                vc.validate_schema_file(path)  # 不抛异常即通过


class TestControllerActionRegistry(unittest.TestCase):
    """用例 3-5：controller-actions.json 完整性"""

    def test_actions_non_empty_and_unique(self):
        """用例 3：actions 数组非空且无重复"""
        registry = vc.load_json(EVALS_DIR / "controller-actions.json")
        actions = registry.get("actions", [])
        self.assertIsInstance(actions, list)
        self.assertTrue(len(actions) > 0, "actions 不能为空")
        self.assertEqual(len(actions), len(set(actions)), "actions 有重复项")

    def test_package_version_matches(self):
        """用例 4：controller-actions.json 版本号为 v0.4.0-rc.4"""
        registry = vc.load_json(EVALS_DIR / "controller-actions.json")
        self.assertEqual(registry.get("package_version"), "v0.4.0-rc.4")

    def test_schema_controller_action_enums_match_registry(self):
        """用例 5：所有 schema 中的 controller action enum 与 registry 一致"""
        # 这个测试直接调用 validate_controller_action_registry，
        # 它会交叉校验所有 schema 的 enum 和 registry
        vc.validate_controller_action_registry()  # 不抛异常即通过


class TestEvalsCoverage(unittest.TestCase):
    """用例 6-8：evals.json 场景覆盖"""

    def test_required_scenarios_present(self):
        """用例 6：evals.json 包含所有 17 个必需场景"""
        evals = vc.load_json(EVALS_DIR / "evals.json")
        scenario_ids = {s.get("id") for s in evals.get("scenarios", [])}
        missing = vc.REQUIRED_SCENARIOS - scenario_ids
        self.assertEqual(missing, set(), f"缺少必需场景: {sorted(missing)}")

    def test_scenario_count_at_least_39(self):
        """用例 7：场景数 ≥ 39"""
        evals = vc.load_json(EVALS_DIR / "evals.json")
        count = len(evals.get("scenarios", []))
        self.assertGreaterEqual(count, 39, f"场景数 {count} < 39")

    def test_package_version_matches(self):
        """用例 8：evals.json current_package_version 匹配"""
        evals = vc.load_json(EVALS_DIR / "evals.json")
        self.assertEqual(evals.get("current_package_version"), "v0.4.0-rc.4")


class TestPackagingBoundary(unittest.TestCase):
    """用例 9：packaging boundary"""

    def test_no_runtime_state_dirs_in_skill_folder(self):
        """用例 9：skill 目录下不存在 .z2o-state、.z2o-patterns、z2o-artifacts"""
        # validate_packaging_boundary 会检查这 3 个目录
        vc.validate_packaging_boundary()  # 不抛异常即通过


class TestErrorHandling(unittest.TestCase):
    """用例 10-12：错误输入处理"""

    def test_missing_schema_file_raises_error(self):
        """用例 10：schema 文件不存在时报错"""
        original = vc.SCHEMA_FILES[:]
        vc.SCHEMA_FILES.append("nonexistent-schema.schema.json")
        try:
            with self.assertRaises((OSError, vc.ValidationError)):
                for f in vc.SCHEMA_FILES:
                    vc.validate_schema_file(vc.EVALS / f)
        finally:
            vc.SCHEMA_FILES.pop()

    def test_malformed_evals_json_raises_error(self):
        """用例 11：evals.json 格式错误时报错"""
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_json_path = Path(tmpdir) / "bad_evals.json"
            bad_json_path.write_text("not valid json {{{", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                vc.load_json(bad_json_path)

    def test_malformed_controller_actions_raises_error(self):
        """用例 12：controller-actions.json 格式错误时报错"""
        with patch.object(vc, "load_json", return_value={"actions": "not_a_list"}):
            with self.assertRaises(vc.ValidationError):
                vc.validate_controller_action_registry()


if __name__ == "__main__":
    unittest.main()
