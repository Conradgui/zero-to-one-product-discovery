#!/usr/bin/env python3
"""P0_006 — 导出可审计交付包."""

from usability_common import run_scenario


if __name__ == "__main__":
    raise SystemExit(
        run_scenario(
            path_id="P0_006",
            name="导出可审计交付包",
            scenario_type="artifact_export_request",
            timeout_seconds=75,
            min_chars=80,
            turns=[
                "我想导出当前项目的可审计交付包。但现在只有模糊想法和少量访谈信息，"
                "还没有被确认的 PRD、Roadmap、用户故事或实施计划。"
                "请告诉我这个导出应该如何处理，哪些文件可以有，哪些必须标记未就绪。"
            ],
        )
    )
