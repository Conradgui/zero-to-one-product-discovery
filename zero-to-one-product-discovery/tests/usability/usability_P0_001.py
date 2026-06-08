#!/usr/bin/env python3
"""P0_001 — 从模糊想法启动产品发现."""

from usability_common import run_scenario


if __name__ == "__main__":
    raise SystemExit(
        run_scenario(
            path_id="P0_001",
            name="从模糊想法启动产品发现",
            scenario_type="vague_idea_start",
            timeout_seconds=45,
            min_chars=50,
            turns=[
                "我有个很模糊的想法：想做一个帮助应届生准备 AI 产品经理春招的工具，"
                "但我还不确定它应该是学习计划、项目管理、面试训练，还是作品集打磨。"
                "请用 zero-to-one-product-discovery 的方式带我开始。"
            ],
        )
    )
