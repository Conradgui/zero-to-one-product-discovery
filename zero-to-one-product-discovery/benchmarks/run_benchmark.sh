#!/usr/bin/env bash
# Run Z2O Benchmark: Tool vs bare model.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TASKS_DIR="$SCRIPT_DIR/tasks"
TOOL_RUNNER="$SCRIPT_DIR/tool_runner/run_tool.py"
BASELINE="$SCRIPT_DIR/baseline/run_baseline.py"
EVALUATOR="$SCRIPT_DIR/evaluator/evaluate.py"
RESULTS_DIR="${Z2O_BENCHMARK_RESULTS_DIR:-$SCRIPT_DIR/results/$(date +%Y%m%d_%H%M%S)}"
REPORT="$RESULTS_DIR/benchmark_report.md"
TASK_FILTER="${Z2O_TASK_FILTER:-}"

mkdir -p "$RESULTS_DIR"

{
  echo "{"
  echo "  \"started_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo "  \"provider_preference\": \"${Z2O_BENCHMARK_PROVIDER:-deepseek}\","
  echo "  \"task_filter\": \"${TASK_FILTER}\","
  echo "  \"llm_judge_skipped\": \"${Z2O_SKIP_LLM_JUDGE:-0}\""
  echo "}"
} > "$RESULTS_DIR/run_manifest.json"

echo "============================================"
echo " Z2O Benchmark: Tool vs Bare Model"
echo " Results: $RESULTS_DIR"
echo " Provider preference: ${Z2O_BENCHMARK_PROVIDER:-deepseek}"
echo "============================================"
echo ""

for task_file in "$TASKS_DIR"/task_BM_*.json; do
    task_id="$(basename "$task_file" .json | sed 's/task_//')"
    if [[ -n "$TASK_FILTER" && "$task_id" != "$TASK_FILTER" ]]; then
        continue
    fi

    echo "── $task_id ──"
    cp "$task_file" "$RESULTS_DIR/${task_id}_task_snapshot.json"

    echo "  [1/3] Tool Runner"
    python3 "$TOOL_RUNNER" "$task_file" "$RESULTS_DIR/${task_id}_tool.json"

    echo "  [2/3] Baseline Runner"
    python3 "$BASELINE" "$task_file" "$RESULTS_DIR/${task_id}_baseline.json"

    echo "  [3/3] Evaluator"
    python3 "$EVALUATOR" "$task_file" \
        "$RESULTS_DIR/${task_id}_tool.json" \
        "$RESULTS_DIR/${task_id}_baseline.json" \
        "$RESULTS_DIR/${task_id}_eval.json"

    echo "  done: $task_id"
    echo ""
done

echo "── Generate report ──"
python3 "$SCRIPT_DIR/generate_report.py" "$RESULTS_DIR" "$REPORT"
echo ""
echo "Report: $REPORT"
echo ""
cat "$REPORT"
