# Zero-to-One Product Discovery — Quality Test Suite
#
# 目录结构：
#   tests/
#   ├── __init__.py               ← 本文件
#   ├── conftest.py               ← 共享工具（API 调用、fixture）
#   ├── fixtures.py               ← 共享测试数据工厂
#   ├── run_tests.sh              ← 测试运行脚本
#   ├── unit/                     ← A/B/C/D/E 类测试（无需 API Key）
#   │   ├── __init__.py
#   │   ├── test_validate_contracts.py      (12 用例)
#   │   ├── test_persist_workbench.py       (14 用例)
#   │   ├── test_generate_revision_trace.py (15 用例)
#   │   └── test_schema_integrity.py        (3 用例)
#   └── integration/              ← F 类测试（需要 API Key）
#       ├── __init__.py
#       └── test_api_integration.py         (8 用例)
#
# 运行方式：
#   ./tests/run_tests.sh unit        # 无需 API Key
#   ./tests/run_tests.sh integration # 需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY
#   ./tests/run_tests.sh all         # 全部
#
# 共计 52 个用例（unit: 44 / integration: 8）
