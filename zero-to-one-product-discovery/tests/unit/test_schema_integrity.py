"""test_schema_integrity.py — 9 个 schema 结构校验

覆盖用例：
  1. 所有 9 个 schema 可被 JSON 解析
  2. 所有 schema 的 examples 数组非空
  3. 所有 schema 的 type 为 object
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.fixtures import EVALS_DIR

SCHEMA_FILES = [
    "agent-work-order.schema.json",
    "agent-return-packet.schema.json",
    "audit-report.schema.json",
    "workbench.schema.json",
    "pattern-index.schema.json",
    "artifact-manifest.schema.json",
    "execution-handoff.schema.json",
    "revision-index.schema.json",
    "revision-record.schema.json",
]


class TestSchemaParsable(unittest.TestCase):
    """用例 1：所有 schema 可被 JSON 解析"""

    def test_all_schemas_are_valid_json(self):
        for filename in SCHEMA_FILES:
            path = EVALS_DIR / filename
            with self.subTest(schema=filename):
                self.assertTrue(path.exists(), f"{filename} 文件不存在")
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                self.assertIsInstance(data, dict, f"{filename} 顶层不是 JSON 对象")


class TestSchemaExamples(unittest.TestCase):
    """用例 2：所有 schema 的 examples 数组非空"""

    def test_all_schemas_have_examples(self):
        for filename in SCHEMA_FILES:
            path = EVALS_DIR / filename
            with self.subTest(schema=filename):
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                examples = data.get("examples", [])
                self.assertIsInstance(examples, list, f"{filename} 的 examples 不是数组")
                self.assertGreater(len(examples), 0, f"{filename} 的 examples 为空")


class TestSchemaTopLevelType(unittest.TestCase):
    """用例 3：所有 schema 的 type 为 object"""

    def test_all_schemas_top_level_type_is_object(self):
        for filename in SCHEMA_FILES:
            path = EVALS_DIR / filename
            with self.subTest(schema=filename):
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                self.assertEqual(data.get("type"), "object", f"{filename} 的顶层 type 不是 object")


if __name__ == "__main__":
    unittest.main()
