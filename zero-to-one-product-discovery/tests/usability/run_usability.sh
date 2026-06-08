#!/usr/bin/env bash
# Phase 4 real API usability runner. Uses DeepSeek by default via env vars.

set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_DIR"

if [ -z "${DEEPSEEK_API_KEY:-}" ] && [ -z "${MIMO_API_KEY:-}" ]; then
  echo "❌ 缺少 API Key：请设置 DEEPSEEK_API_KEY（首选）或 MIMO_API_KEY"
  exit 1
fi

passed=0
total=0
failed_paths=()

run_one() {
  local script="$1"
  total=$((total + 1))
  python3 "$SCRIPT_DIR/$script"
  local code=$?
  if [ "$code" -eq 0 ]; then
    passed=$((passed + 1))
  else
    failed_paths+=("$script")
  fi
}

run_one usability_P0_001.py
run_one usability_P0_002.py
run_one usability_P0_003.py
run_one usability_P0_004.py
run_one usability_P0_005.py
run_one usability_P0_006.py

echo "============================================"
echo "Phase 4 usability summary: $passed/$total paths passed"
if [ "${#failed_paths[@]}" -gt 0 ]; then
  echo "Failed scripts: ${failed_paths[*]}"
  exit 1
fi
echo "All usability paths passed"
