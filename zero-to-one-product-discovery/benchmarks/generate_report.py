#!/usr/bin/env python3
"""Generate a Markdown benchmark report from evaluation JSON files."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any


DIMENSION_LABELS = {
    "stage_gate": "阶段门禁",
    "evidence_grounding": "证据扎根",
    "risk_prioritization": "风险优先级",
    "auditability": "可审计",
    "boundary_safety": "边界安全",
    "actionability": "可执行",
    "context_economy": "上下文经济",
    "child_skill_contract": "子 Skill Contract",
}


def load_evals(results_dir: str) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(Path(results_dir).glob("BM_*_eval.json"))
    ]


def fmt(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def judge_winner(ev: dict[str, Any]) -> str:
    judge = ev.get("llm_blind_judge", {})
    if judge.get("skipped"):
        return f"跳过：{judge.get('reason', '-')}"
    scores = judge.get("scores", {})
    winner = scores.get("winner", "-")
    mapping = judge.get("mapping", {})
    if winner in mapping:
        return f"{mapping[winner]}（盲评 {winner}）"
    return winner


def dimension_average(evals: list[dict[str, Any]], side: str, dimension: str) -> float | None:
    values = [
        ev[side]["dimension_scores"].get(dimension)
        for ev in evals
        if ev[side]["dimension_scores"].get(dimension) is not None
    ]
    if not values:
        return None
    return round(mean(values), 1)


def strongest_dimensions(evals: list[dict[str, Any]]) -> list[tuple[str, float]]:
    deltas = []
    for dimension in DIMENSION_LABELS:
        tool_avg = dimension_average(evals, "tool", dimension)
        baseline_avg = dimension_average(evals, "baseline", dimension)
        if tool_avg is None or baseline_avg is None:
            continue
        deltas.append((dimension, round(tool_avg - baseline_avg, 1)))
    return sorted(deltas, key=lambda item: item[1], reverse=True)


def generate_report(results_dir: str, output_path: str) -> None:
    evals = load_evals(results_dir)
    if not evals:
        print("No eval files found")
        sys.exit(1)

    avg_tool = round(mean(ev["tool"]["overall_score"] for ev in evals), 1)
    avg_baseline = round(mean(ev["baseline"]["overall_score"] for ev in evals), 1)
    avg_delta = round(avg_tool - avg_baseline, 1)
    strongest = strongest_dimensions(evals)

    lines: list[str] = []
    lines.append("# Z2O Benchmark Report: Tool vs Bare Model")
    lines.append("")
    lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"结果目录：`{Path(results_dir)}`")
    lines.append(f"任务数：{len(evals)}")
    lines.append("")
    lines.append("## 总览")
    lines.append("")
    lines.append("| 任务 | Baseline mode | 轮次 | Tool 总分 | Baseline 总分 | 差值 | Tool 过程分 | Baseline 过程分 | Tool 最终分 | Baseline 最终分 | Hard failures | 盲评胜者 |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for ev in evals:
        tool_hard = len(ev["tool"].get("hard_failures", []))
        base_hard = len(ev["baseline"].get("hard_failures", []))
        delta = ev["delta"]
        delta_str = f"+{delta:.1f}" if delta > 0 else f"{delta:.1f}"
        lines.append(
            "| {task} | `{mode}` | {turns} | {tool} | {base} | {delta} | {tp} | {bp} | {tf} | {bf} | T:{th}/B:{bh} | {judge} |".format(
                task=ev["task_id"],
                mode=ev["baseline_mode"],
                turns=ev["turn_count"],
                tool=fmt(ev["tool"]["overall_score"]),
                base=fmt(ev["baseline"]["overall_score"]),
                delta=delta_str,
                tp=fmt(ev["tool"].get("process_score")),
                bp=fmt(ev["baseline"].get("process_score")),
                tf=fmt(ev["tool"].get("final_artifact_score")),
                bf=fmt(ev["baseline"].get("final_artifact_score")),
                th=tool_hard,
                bh=base_hard,
                judge=judge_winner(ev),
            )
        )
    lines.append("")

    lines.append("## 维度平均分")
    lines.append("")
    lines.append("| 维度 | Tool | Baseline | 差值 |")
    lines.append("|---|---:|---:|---:|")
    for dimension, label in DIMENSION_LABELS.items():
        tool_avg = dimension_average(evals, "tool", dimension)
        baseline_avg = dimension_average(evals, "baseline", dimension)
        if tool_avg is None or baseline_avg is None:
            continue
        delta = round(tool_avg - baseline_avg, 1)
        lines.append(f"| {label} | {tool_avg} | {baseline_avg} | {'+' if delta > 0 else ''}{delta} |")
    lines.append("")

    lines.append("## 各任务详情")
    lines.append("")
    for ev in evals:
        lines.append(f"### {ev['task_id']}：{ev['task_name']}")
        lines.append("")
        lines.append(f"- 产品意义：{ev.get('product_meaning', '-')}")
        lines.append(f"- Baseline mode：`{ev['baseline_mode']}`；轮次：{ev['turn_count']}")
        lines.append(f"- Raw files：`{ev['raw_files']['tool']}` / `{ev['raw_files']['baseline']}`")
        lines.append("")
        lines.append("| 侧 | 总分 | 过程分 | 最终产物分 | Penalty | Hard failures |")
        lines.append("|---|---:|---:|---:|---:|---|")
        for side in ("tool", "baseline"):
            hard = ev[side].get("hard_failures", [])
            hard_text = "; ".join(item["id"] for item in hard) if hard else "-"
            lines.append(
                f"| {side} | {fmt(ev[side]['overall_score'])} | {fmt(ev[side].get('process_score'))} | {fmt(ev[side].get('final_artifact_score'))} | {fmt(ev[side].get('penalty'))} | {hard_text} |"
            )
        lines.append("")
        lines.append("| 检查项 | Tool | Baseline |")
        lines.append("|---|---|---|")
        check_ids = {check["id"] for check in ev["tool"]["checks"]} | {check["id"] for check in ev["baseline"]["checks"]}
        for check_id in sorted(check_ids):
            tool_check = next((check for check in ev["tool"]["checks"] if check["id"] == check_id), None)
            base_check = next((check for check in ev["baseline"]["checks"] if check["id"] == check_id), None)
            description = (tool_check or base_check or {}).get("description", check_id)
            tool_pass = "-" if tool_check is None else ("pass" if tool_check["passed"] else "fail")
            base_pass = "-" if base_check is None else ("pass" if base_check["passed"] else "fail")
            lines.append(f"| {description} | {tool_pass} | {base_pass} |")
        judge = ev.get("llm_blind_judge", {})
        if judge.get("skipped"):
            lines.append(f"\n- LLM 盲评：跳过（{judge.get('reason', '-')})")
        else:
            scores = judge.get("scores", {})
            lines.append(f"\n- LLM 盲评胜者：{judge_winner(ev)}")
            lines.append(f"- LLM 盲评理由：{scores.get('reason', '-')}")
        lines.append("")

    lines.append("## 弱项与失败解释")
    lines.append("")
    weak_items = [ev for ev in evals if ev["delta"] <= 0 or ev["tool"].get("hard_failures")]
    if not weak_items:
        lines.append("- 未出现 Tool 总分低于 Baseline 的任务；仍需人工复核 raw output，避免规则评分误判。")
    else:
        for ev in weak_items:
            lines.append(f"- {ev['task_id']}：Tool delta {ev['delta']}。需要复核 raw output 判断是任务设计问题、规则评分问题，还是 skill 真实弱项。")
    lines.append("")

    lines.append("## 面试用三句话")
    lines.append("")
    first = strongest[0] if strongest else ("stage_gate", avg_delta)
    second = strongest[1] if len(strongest) > 1 else first
    lines.append(
        f"1. 我用 {len(evals)} 个真实 API Benchmark 对比了 Z2O workflow 和同模型裸对话，Tool 平均 {avg_tool}/100，Baseline 平均 {avg_baseline}/100，差值 {'+' if avg_delta > 0 else ''}{avg_delta}。"
    )
    lines.append(
        f"2. 差距最明显的维度是{DIMENSION_LABELS[first[0]]}和{DIMENSION_LABELS[second[0]]}，说明它的价值不只是生成文本，而是把阶段门禁、证据边界和交付边界流程化。"
    )
    lines.append(
        "3. 我保留了每轮 raw output、规则评分和盲评结果；如果某个任务表现不好，会作为产品边界分析，而不是包装成成功。"
    )
    lines.append("")
    lines.append("## 结论边界")
    lines.append("")
    lines.append("- 本报告证明的是这些任务集上的可控性与可复盘优势，不代表所有模型、所有产品领域、所有用户输入下的绝对优势。")
    lines.append("- LLM 盲评是辅助判断；规则评分与 raw output 是主要证据。")
    lines.append("- 任何包含真实 API 的结论都应引用本目录下的 raw JSON，而不是只引用汇总表。")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"OK report: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_report.py <results_dir> <output.md>")
        sys.exit(1)
    generate_report(sys.argv[1], sys.argv[2])
