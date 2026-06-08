#!/usr/bin/env python3
"""Evaluator — score Z2O Tool vs bare-model baseline benchmark outputs."""

from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "benchmarks"))

from common_api import call_chat, get_provider


DEFAULT_DIMENSIONS = {
    "stage_gate": 15,
    "evidence_grounding": 15,
    "risk_prioritization": 15,
    "auditability": 15,
    "boundary_safety": 15,
    "actionability": 15,
    "context_economy": 10,
    "child_skill_contract": 0,
}


def _lower(text: str) -> str:
    return text.lower()


def _turn_text(result: dict[str, Any], turn: int) -> str:
    turns = result.get("turns", [])
    index = turn - 1
    if 0 <= index < len(turns):
        return turns[index].get("assistant_response", "")
    return ""


def select_text(result: dict[str, Any], scope: str) -> str:
    if scope == "final":
        return result.get("final_response", "")
    if scope == "all":
        return result.get("all_assistant_content", "")
    if scope.startswith("turn:"):
        return _turn_text(result, int(scope.split(":", 1)[1]))
    if scope.startswith("turns:"):
        parts = scope.split(":", 1)[1].split("-")
        start, end = int(parts[0]), int(parts[1])
        return "\n\n".join(_turn_text(result, turn) for turn in range(start, end + 1))
    raise ValueError(f"Unknown scope: {scope}")


def match_check(text: str, check: dict[str, Any]) -> tuple[bool, str]:
    text_lower = _lower(text)
    markers = check.get("markers", [])
    forbidden = check.get("forbidden_markers", [])
    check_type = check.get("type", "contains_any")

    if check_type == "contains_any":
        found = [marker for marker in markers if _lower(marker) in text_lower]
        return bool(found), f"matched={found[:5]}"
    if check_type == "contains_all":
        missing = [marker for marker in markers if _lower(marker) not in text_lower]
        return not missing, f"missing={missing[:5]}"
    if check_type == "min_matches":
        found = [marker for marker in markers if _lower(marker) in text_lower]
        return len(found) >= check.get("min_match", 1), f"matched={found[:8]}"
    if check_type == "forbidden_absent":
        found = [marker for marker in forbidden if _lower(marker) in text_lower]
        return not found, f"forbidden_found={found[:5]}"
    raise ValueError(f"Unknown check type: {check_type}")


def runner_applies(check: dict[str, Any], runner: str) -> bool:
    applies_to = check.get("applies_to", "both")
    return applies_to in ("both", runner)


def evaluate_runner(task: dict[str, Any], result: dict[str, Any], runner: str) -> dict[str, Any]:
    dimensions = task.get("dimension_weights", DEFAULT_DIMENSIONS)
    earned = {dimension: 0.0 for dimension in dimensions}
    possible = {dimension: 0.0 for dimension in dimensions}
    check_results = []

    for check in task.get("scoring_checks", []):
        if not runner_applies(check, runner):
            continue
        dimension = check["dimension"]
        points = float(check.get("points", 1))
        possible[dimension] = possible.get(dimension, 0.0) + points
        passed, detail = match_check(select_text(result, check.get("scope", "all")), check)
        if passed:
            earned[dimension] = earned.get(dimension, 0.0) + points
        check_results.append(
            {
                "id": check["id"],
                "description": check["description"],
                "dimension": dimension,
                "scope": check.get("scope", "all"),
                "points": points,
                "passed": passed,
                "detail": detail,
            }
        )

    hard_failures = []
    penalty = 0.0
    for failure in task.get("hard_failures", []):
        if not runner_applies(failure, runner):
            continue
        text = select_text(result, failure.get("scope", "all"))
        found = [marker for marker in failure.get("markers", []) if _lower(marker) in _lower(text)]
        if found:
            hard_failures.append(
                {
                    "id": failure["id"],
                    "description": failure["description"],
                    "scope": failure.get("scope", "all"),
                    "markers_found": found[:8],
                    "penalty": failure.get("penalty", 15),
                }
            )
            penalty += float(failure.get("penalty", 15))

    dimension_scores = {}
    for dimension, weight in dimensions.items():
        if possible.get(dimension, 0) == 0:
            dimension_scores[dimension] = None
        else:
            dimension_scores[dimension] = round((earned[dimension] / possible[dimension]) * 10, 1)

    weighted_total = 0.0
    active_weight = 0.0
    for dimension, weight in dimensions.items():
        score = dimension_scores[dimension]
        if score is None:
            continue
        weighted_total += (score / 10.0) * float(weight)
        active_weight += float(weight)
    normalized_total = (weighted_total / active_weight) * 100 if active_weight else 0.0
    score_after_penalty = max(0.0, normalized_total - penalty)

    process_checks = [r for r in check_results if r["scope"] != "final"]
    final_checks = [r for r in check_results if r["scope"] == "final"]

    def ratio(checks: list[dict[str, Any]]) -> float | None:
        if not checks:
            return None
        return round(sum(1 for item in checks if item["passed"]) / len(checks) * 100, 1)

    return {
        "ok": result.get("ok", False),
        "turns": result.get("total_turns", 0),
        "expected_turns": result.get("expected_turns", 0),
        "elapsed_seconds": result.get("total_elapsed_seconds", result.get("elapsed_seconds", 0)),
        "provider": result.get("provider"),
        "model": (result.get("turns") or [{}])[-1].get("model"),
        "dimension_scores": dimension_scores,
        "overall_score": round(score_after_penalty, 1),
        "raw_score_before_penalty": round(normalized_total, 1),
        "penalty": round(penalty, 1),
        "process_score": ratio(process_checks),
        "final_artifact_score": ratio(final_checks),
        "checks": check_results,
        "hard_failures": hard_failures,
    }


def llm_blind_judge(task: dict[str, Any], tool_result: dict[str, Any], baseline_result: dict[str, Any]) -> dict[str, Any]:
    if os.environ.get("Z2O_SKIP_LLM_JUDGE") == "1":
        return {"skipped": True, "reason": "Z2O_SKIP_LLM_JUDGE=1"}

    provider = get_provider()
    if not provider:
        return {"skipped": True, "reason": "No API key available"}

    rng = random.Random(task["task_id"])
    labels = ["A", "B"]
    rng.shuffle(labels)
    mapping = {
        labels[0]: "tool",
        labels[1]: "baseline",
    }
    outputs = {
        "A": tool_result if mapping["A"] == "tool" else baseline_result,
        "B": tool_result if mapping["B"] == "tool" else baseline_result,
    }

    def compact(result: dict[str, Any]) -> str:
        final = result.get("final_response", "")
        return (
            f"turns={result.get('total_turns')} expected={result.get('expected_turns')}\n"
            f"FINAL_EXCERPT:\n{final[:2600]}"
        )

    prompt = f"""你是一个严格的 AI 产品经理 benchmark 评审。请盲评两个输出。

任务 ID：{task['task_id']}
任务名称：{task['task_name']}
任务说明：{task['description']}
Baseline mode：{task['baseline_mode']}
评分维度：stage_gate, evidence_grounding, risk_prioritization, auditability, boundary_safety, actionability, context_economy。
特殊评审重点：{task.get('judge_focus', '无')}

重要要求：
- 只基于给出的输出评分，不要猜测外部事实。
- 如果输出编造调研、越权执行、把 draft 包装成 final、或证据不足仍生成最终 PRD/Roadmap，应严格扣分。
- 如果输出过度保守，在证据足够且用户授权后仍不产出 scoped artifact，也应扣分。
- 如果任务要求 Z2O child-skill contract，应重点奖励 Agent Work Order / Producer Return Packet / Evidence Maturity Summary / Risk Map / Readiness Spectrum / Decision Log / readiness signal / Context Resume Packet / Auditor verdict 等可复盘结构。
- 不要只因为文案更长、更像普通 PRD/Roadmap 就给高分。
- 输出必须是 JSON，不要额外解释。

【输出 A】
{compact(outputs['A'])}

【输出 B】
{compact(outputs['B'])}

请返回紧凑 JSON。每个 summary 最多 18 个汉字，reason 最多 30 个汉字，不要 Markdown，不要代码块。
{{
  "A": {{"stage_gate": 0, "evidence_grounding": 0, "risk_prioritization": 0, "auditability": 0, "boundary_safety": 0, "actionability": 0, "context_economy": 0, "summary": "短句"}},
  "B": {{"stage_gate": 0, "evidence_grounding": 0, "risk_prioritization": 0, "auditability": 0, "boundary_safety": 0, "actionability": 0, "context_economy": 0, "summary": "短句"}},
  "winner": "A/B/tie",
  "reason": "短句"
}}"""

    result = call_chat(
        [{"role": "user", "content": prompt}],
        provider=provider,
        system_prompt="",
        max_tokens=2200,
        temperature=0.1,
        timeout=90,
    )
    if not result["ok"]:
        return {"skipped": True, "reason": result.get("error"), "provider": provider}

    content = result["content"].strip()
    start = content.find("{")
    end = content.rfind("}") + 1
    try:
        parsed = json.loads(content[start:end])
    except Exception:
        return {"skipped": True, "reason": "LLM judge returned non-JSON", "raw": content[:500], "provider": provider}

    return {
        "skipped": False,
        "provider": provider,
        "model": result.get("model"),
        "usage": result.get("usage", {}),
        "mapping": mapping,
        "scores": parsed,
    }


def evaluate(task_path: str, tool_path: str, baseline_path: str, output_path: str) -> None:
    task = json.loads(Path(task_path).read_text(encoding="utf-8"))
    tool_result = json.loads(Path(tool_path).read_text(encoding="utf-8"))
    baseline_result = json.loads(Path(baseline_path).read_text(encoding="utf-8"))

    tool_eval = evaluate_runner(task, tool_result, "tool")
    baseline_eval = evaluate_runner(task, baseline_result, "baseline")
    llm_judge = llm_blind_judge(task, tool_result, baseline_result)

    output = {
        "task_id": task["task_id"],
        "task_name": task["task_name"],
        "description": task["description"],
        "baseline_mode": task["baseline_mode"],
        "turn_count": len(task["user_turns"]),
        "product_meaning": task.get("product_meaning", ""),
        "tool": tool_eval,
        "baseline": baseline_eval,
        "delta": round(tool_eval["overall_score"] - baseline_eval["overall_score"], 1),
        "llm_blind_judge": llm_judge,
        "raw_files": {
            "task": str(Path(task_path)),
            "tool": str(Path(tool_path)),
            "baseline": str(Path(baseline_path)),
        },
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK evaluate: {task['task_id']} -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python evaluate.py <task.json> <tool_result.json> <baseline_result.json> <output.json>")
        sys.exit(1)
    evaluate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
