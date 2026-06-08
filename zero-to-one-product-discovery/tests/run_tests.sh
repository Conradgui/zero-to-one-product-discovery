#!/usr/bin/env bash
# run_tests.sh — 运行质量测试套件
#
# 用法：
#   ./tests/run_tests.sh unit        # 只跑单元测试（无需 API Key）
#   ./tests/run_tests.sh integration # 只跑集成测试（需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY）
#   ./tests/run_tests.sh all         # 全部
#
# 环境变量：
#   DEEPSEEK_API_KEY  — DeepSeek API Key（integration 测试需要）
#   MIMO_API_KEY      — MIMO API Key（integration 测试需要）

set -euo pipefail

# 自动定位 zero-to-one-product-discovery 目录（无论从哪里运行）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# 如果在 tests/ 内，上一级就是项目目录；如果在仓库根，找子目录
if [ -f "$SCRIPT_DIR/../SKILL.md" ]; then
  PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
elif [ -f "$SCRIPT_DIR/zero-to-one-product-discovery/SKILL.md" ]; then
  PROJECT_DIR="$SCRIPT_DIR/zero-to-one-product-discovery"
elif [ -f "$SCRIPT_DIR/SKILL.md" ]; then
  PROJECT_DIR="$SCRIPT_DIR"
else
  echo "❌ 找不到 zero-to-one-product-discovery 目录"
  echo "请在仓库根目录或 zero-to-one-product-discovery/ 目录下运行"
  exit 1
fi

cd "$PROJECT_DIR"

MODE="${1:-unit}"

echo "============================================"
echo " Z2O Quality Test Suite"
echo " Mode: $MODE"
echo " Project: $PROJECT_DIR"
echo "============================================"
echo ""

case "$MODE" in
  unit)
    echo "▶ 运行单元测试（无需 API Key）..."
    echo ""
    python3 -m unittest discover -s tests/unit -v
    ;;
  integration)
    if [ -z "${DEEPSEEK_API_KEY:-}" ] && [ -z "${MIMO_API_KEY:-}" ]; then
      echo "⏭ 跳过集成测试：未设置 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量"
      echo ""
      echo "设置方式："
      echo "  export DEEPSEEK_API_KEY=sk-xxx"
      echo "  export MIMO_API_KEY=sk-xxx"
      exit 0
    fi
    echo "▶ 运行集成测试（需要真实 API Key）..."
    echo ""
    python3 -m unittest discover -s tests/integration -v
    ;;
  all)
    echo "▶ [1/2] 运行单元测试..."
    echo ""
    python3 -m unittest discover -s tests/unit -v
    echo ""
    echo "▶ [2/2] 运行集成测试..."
    echo ""
    if [ -z "${DEEPSEEK_API_KEY:-}" ] && [ -z "${MIMO_API_KEY:-}" ]; then
      echo "⏭ 跳过集成测试：未设置 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量"
    else
      python3 -m unittest discover -s tests/integration -v
    fi
    ;;
  *)
    echo "用法: $0 {unit|integration|all}"
    exit 1
    ;;
esac

echo ""
echo "============================================"
echo " ✅ 测试完成"
echo "============================================"
