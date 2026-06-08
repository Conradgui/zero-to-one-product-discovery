#!/usr/bin/env python3
"""P0_004 — 从证据推进到规划产物."""

from usability_common import run_scenario


if __name__ == "__main__":
    raise SystemExit(
        run_scenario(
            path_id="P0_004",
            name="从证据推进到规划产物",
            scenario_type="evidence_to_planning",
            timeout_seconds=180,
            min_chars=50,
            max_tokens=1800,
            turns=[
                "我想做一个给自由职业设计师用的客户管理工具。",
                "目标用户是每天处理 3-5 个客户的自由职业设计师，痛点是客户资料、报价和交付状态散落在微信、邮件、备忘录里。",
                "MVP 只做客户档案、项目状态追踪、下一步提醒；不做发票、不做合同、不做团队协作。",
                "我做了小范围访谈，12 位设计师里 7 位说最大问题是忘记跟进或找不到上次报价。",
                "方向确认，请进入 PRD 和 Roadmap 规划。",
            ],
        )
    )
