#!/usr/bin/env python3
"""P0_005 — 查看证据成熟度、风险优先级和准备度."""

from usability_common import run_scenario


if __name__ == "__main__":
    raise SystemExit(
        run_scenario(
            path_id="P0_005",
            name="查看证据成熟度、风险优先级和准备度",
            scenario_type="evidence_dashboard",
            timeout_seconds=75,
            min_chars=80,
            turns=[
                "基于下面这些信息，帮我查看当前证据成熟度、最高风险假设、下一步验证优先级，以及是否已经准备好进入 PRD：\n"
                "- 事实：我访谈了 12 位自由职业设计师，其中 7 位提到“客户资料散落”\n"
                "- 假设：他们愿意为轻量客户管理工具付费\n"
                "- 未知：他们更想要提醒、档案，还是报价记录\n"
                "- 风险：如果实际痛点只是提醒，那完整客户管理会做重\n"
                "只需要给我当前状态判断，不要直接写最终 PRD。"
            ],
        )
    )
