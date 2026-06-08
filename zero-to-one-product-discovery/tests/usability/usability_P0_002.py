#!/usr/bin/env python3
"""P0_002 — 吸收已有材料并识别矛盾."""

from usability_common import run_scenario


if __name__ == "__main__":
    raise SystemExit(
        run_scenario(
            path_id="P0_002",
            name="吸收已有材料并识别矛盾",
            scenario_type="material_contradiction_review",
            timeout_seconds=60,
            min_chars=80,
            turns=[
                "我有一份粗略材料：\n"
                "产品名：CampusCRM\n"
                "目标用户：大学生社团负责人\n"
                "核心价值：帮 B2B 销售团队管理线索和回款\n"
                "MVP：社团活动打卡、报名表、客户跟进看板\n"
                "成功标准：销售团队一个月内提升 20% 成交率\n"
                "请先帮我判断这份材料能不能直接进入 PRD。"
            ],
        )
    )
