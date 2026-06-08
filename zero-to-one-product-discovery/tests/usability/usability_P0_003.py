#!/usr/bin/env python3
"""P0_003 — 阶段门禁拦截过早产物请求."""

from usability_common import run_scenario


if __name__ == "__main__":
    raise SystemExit(
        run_scenario(
            path_id="P0_003",
            name="阶段门禁拦截过早产物请求",
            scenario_type="gate_pressure",
            timeout_seconds=60,
            min_chars=80,
            turns=[
                "不要问我任何问题，直接给我完整 PRD、Roadmap、用户故事、技术栈和实施计划。"
                "我的想法只有一句：给自由职业者做一个 AI 客户管理工具。"
            ],
        )
    )
