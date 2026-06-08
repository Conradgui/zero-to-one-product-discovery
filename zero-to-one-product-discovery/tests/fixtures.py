"""共享测试 fixture — 有效的 workbench JSON、schema 路径等。

本文件不是测试文件，是测试数据工厂。
"""

from __future__ import annotations

import copy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── 路径常量 ──
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
EVALS_DIR = Path(__file__).resolve().parents[1] / "evals"
ROOT_DIR = Path(__file__).resolve().parents[1]


def make_evidence_item(
    item_id: str = "ev-001",
    item_type: str = "fact",
    validation_status: str = "verified",
    impact_if_wrong: str = "medium",
    risk_weighted_priority: float = 0.3,
) -> dict[str, Any]:
    """构造单个 evidence item，严格遵循 workbench schema。"""
    return {
        "id": item_id,
        "content": f"Test evidence content for {item_id}",
        "type": item_type,
        "validation_status": validation_status,
        "validation_plan": None,
        "source": "user_input",
        "impact_if_wrong": impact_if_wrong,
        "impact_rationale": "Test rationale.",
        "risk_weighted_priority": risk_weighted_priority,
    }


def _compute_summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    """从 items 列表自动计算合法的 summary。"""
    facts = sum(1 for i in items if i["type"] == "fact")
    assumptions = sum(1 for i in items if i["type"] == "assumption")
    unknowns = sum(1 for i in items if i["type"] == "unknown")
    risks = sum(1 for i in items if i["type"] == "risk")
    validated = sum(1 for i in items if i.get("validation_status") == "verified")
    critical = sum(1 for i in items if i.get("impact_if_wrong") == "critical")
    high = sum(1 for i in items if i.get("impact_if_wrong") == "high")
    total = len(items)

    highest_risk_id = None
    highest_risk_priority = None
    for item in items:
        p = item["risk_weighted_priority"]
        if p > 0 and (highest_risk_priority is None or p > highest_risk_priority):
            highest_risk_priority = p
            highest_risk_id = item["id"]

    maturity_pct = 0.0 if total == 0 else round((validated / total) * 100, 2)
    if maturity_pct > 75:
        maturity_level = "strong"
    elif maturity_pct >= 50:
        maturity_level = "sufficient"
    elif maturity_pct >= 25:
        maturity_level = "partial"
    else:
        maturity_level = "insufficient"

    return {
        "total": total,
        "facts": facts,
        "assumptions": assumptions,
        "unknowns": unknowns,
        "risks": risks,
        "validated": validated,
        "critical_impact_items": critical,
        "high_impact_items": high,
        "maturity_percentage": maturity_pct,
        "maturity_level": maturity_level,
        "highest_risk_item_id": highest_risk_id,
    }


def make_workbench(
    items: list[dict[str, Any]] | None = None,
    summary_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构造一个合法的 workbench JSON。

    结构严格遵循 evals/workbench.schema.json：
    - version, last_updated, workflow_state, evidence_snapshot,
      artifact_status, decision_log, skipped_stages
    """
    if items is None:
        items = [
            make_evidence_item("ev-001", "fact", "verified", "medium", 0.3),
            make_evidence_item("ev-002", "assumption", "unverified", "high", 0.6),
            make_evidence_item("ev-003", "risk", "unverified", "critical", 0.8),
        ]

    summary = _compute_summary(items)
    if summary_overrides:
        summary.update(summary_overrides)

    return {
        "version": "0.4.0-rc.4",
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "workflow_state": {
            "current_stage": "Problem Framing",
            "current_goal": "Validate the core problem.",
            "allowed_output_mode": "outline",
            "depth_mode": "standard",
            "quick_mode_entry_stage": None,
            "do_not_cross": "Do not finalize artifacts without audit.",
        },
        "evidence_snapshot": {
            "items": items,
            "summary": summary,
        },
        "artifact_status": {},
        "decision_log": [],
        "skipped_stages": [],
    }


def make_valid_workbench_json() -> dict[str, Any]:
    """返回一个完全合法的 workbench，可直接通过 schema + evidence summary 校验。"""
    return make_workbench()
