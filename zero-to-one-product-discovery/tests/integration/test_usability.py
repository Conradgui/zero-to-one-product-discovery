"""test_usability.py — 第四阶段：真实可用性测试

使用真实 API 验证 P0 路径的端到端可用性。
需要环境变量：DEEPSEEK_API_KEY 或 MIMO_API_KEY

覆盖路径：
  P0_001 — 从模糊想法启动产品发现（1 轮）
  P0_002 — 逐轮回答推进探索（10 轮）
  P0_003 — 吸收已有材料（3 轮）
  P0_004 — 获得规划产物（1 轮，复用 P0_002 上下文）
  P0_005 — 进入实施规划（1 轮，复用 P0_004 上下文）
"""

from __future__ import annotations

import os
import sys
import time
import unittest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from conftest import SKILL_SYSTEM_PROMPT, Conversation, get_available_provider, has_api_key

_has_any_key = has_api_key("deepseek") or has_api_key("mimo")


def _assert_contains_any(test: unittest.TestCase, text: str, markers: list[str],
                         msg_prefix: str = ""):
    """断言 text 包含 markers 中的至少一个。"""
    text_lower = text.lower()
    found = [m for m in markers if m.lower() in text_lower]
    test.assertTrue(
        len(found) > 0,
        f"{msg_prefix}输出缺少预期标记。期望至少包含 {markers[:5]}... 中的一个。"
        f"实际输出前 300 字：\n{text[:300]}"
    )


def _assert_not_contains_any(test: unittest.TestCase, text: str, markers: list[str],
                             msg_prefix: str = ""):
    """断言 text 不包含 markers 中的任何一个。"""
    text_lower = text.lower()
    found = [m for m in markers if m.lower() in text_lower]
    test.assertEqual(
        len(found), 0,
        f"{msg_prefix}输出不应包含 {found}。实际输出前 300 字：\n{text[:300]}"
    )


def _assert_references_input(test: unittest.TestCase, text: str, input_keywords: list[str],
                             min_match: int = 2, msg_prefix: str = ""):
    """断言 text 引用了用户输入中的至少 min_match 个关键词。"""
    text_lower = text.lower()
    matched = [k for k in input_keywords if k.lower() in text_lower]
    test.assertGreaterEqual(
        len(matched), min_match,
        f"{msg_prefix}输出未充分引用用户输入。匹配了 {matched}，"
        f"期望至少 {min_match} 个。输入关键词：{input_keywords}"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# P0_001 — 从模糊想法启动产品发现
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY")
class TestP0_001_VagueIdeaToDiagnostic(unittest.TestCase):
    """P0_001: 用户说出模糊想法 → 系统产出 Diagnostic Start"""

    def test_P0_001__diagnostic_start_with_exploration_question(self):
        provider = get_available_provider()
        conv = Conversation(provider=provider)

        start = time.time()
        r = conv.send("我想做一个帮助独立开发者管理多个 side project 进度的工具，但还没想清楚具体做什么。")
        elapsed = time.time() - start

        # 行为验证
        self.assertTrue(r["ok"], f"API 调用失败: {r.get('error')}")
        self.assertGreater(len(r["content"]), 30, "输出太短")
        self.assertLess(elapsed, 30, f"耗时 {elapsed:.1f}s 超过 30s 上限")

        content = r["content"]

        # 内容验证：包含探索性问题
        _assert_contains_any(self, content, [
            "？", "什么", "哪个", "如何", "怎样", "why", "what", "how",
        ], "探索性问题: ")

        # 内容验证：包含假设/风险/未知标记，或直接提出了探索性问题（后者更好）
        has_labels = any(m in content for m in [
            "假设", "风险", "未知", "assumption", "risk", "unknown",
            "不确定", "uncertain", "待验证",
        ])
        has_exploration = any(m in content for m in [
            "？", "什么", "哪个", "如何", "怎样",
        ])
        self.assertTrue(
            has_labels or has_exploration,
            f"期望包含假设/风险标记或探索性问题。实际输出前 300 字：\n{content[:300]}"
        )

        # 内容验证：不问成熟产品问题
        _assert_not_contains_any(self, content, [
            "目标用户是谁", "技术栈是什么", "商业模式是什么",
            "who is the target user", "what tech stack", "business model",
        ], "成熟产品问题: ")

        # 内容验证：不产出完整 PRD/Roadmap
        _assert_not_contains_any(self, content, [
            "以下是完整 prd", "以下是最终 prd", "here is the final prd",
            "prd 如下", "完整需求文档",
        ], "过早产物: ")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# P0_002 — 逐轮回答推进探索（10 轮）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY")
class TestP0_002_MultiTurnProgression(unittest.TestCase):
    """P0_002: 10 轮对话逐步推进，验证阶段门禁和证据落地"""

    def test_P0_002__ten_turn_discovery_flow(self):
        provider = get_available_provider()
        conv = Conversation(provider=provider)
        total_start = time.time()

        # ── 第 1 轮：初始想法 ──
        r1 = conv.send("我想做一个给自由职业设计师用的客户管理工具。")
        self.assertTrue(r1["ok"], f"轮次 1 失败: {r1.get('error')}")
        self.assertGreater(len(r1["content"]), 50)
        # 不问成熟产品问题
        _assert_not_contains_any(self, r1["content"], [
            "目标用户是谁", "技术栈", "商业模式", "business model",
        ], "轮次 1: ")
        # 包含探索性问题
        _assert_contains_any(self, r1["content"], [
            "？", "什么", "哪个", "如何", "怎样",
        ], "轮次 1 探索问题: ")

        # ── 第 2 轮：提供目标用户和痛点 ──
        r2 = conv.send(
            "目标用户是每天处理 3-5 个客户的自由职业设计师。"
            "痛点是客户资料、报价、交付状态散落在微信、邮件和笔记里。"
        )
        self.assertTrue(r2["ok"], f"轮次 2 失败: {r2.get('error')}")
        # 引用用户提供的具体信息
        _assert_references_input(self, r2["content"],
                                 ["设计师", "客户", "报价", "散落", "微信", "邮件"],
                                 min_match=2, msg_prefix="轮次 2: ")

        # ── 第 3 轮：定义 MVP 范围 ──
        r3 = conv.send(
            "MVP 只做三件事：客户档案、项目状态追踪、下一步提醒。"
            "不做发票、不做合同、不做团队协作。"
        )
        self.assertTrue(r3["ok"], f"轮次 3 失败: {r3.get('error')}")
        # 引用 MVP 范围
        _assert_references_input(self, r3["content"],
                                 ["客户档案", "状态", "提醒", "发票", "合同", "MVP"],
                                 min_match=2, msg_prefix="轮次 3: ")

        # ── 第 4 轮：成功指标 ──
        r4 = conv.send(
            "成功指标：2 周内 5 位试用者能减少漏跟进的情况。"
            "非目标：不做 CRM 全功能，只做设计师场景。"
        )
        self.assertTrue(r4["ok"], f"轮次 4 失败: {r4.get('error')}")
        _assert_references_input(self, r4["content"],
                                 ["成功", "指标", "试用", "跟进", "漏"],
                                 min_match=1, msg_prefix="轮次 4: ")

        # ── 第 5 轮：竞品分析 ──
        r5 = conv.send(
            "竞品：Dubsado（太重）、HoneyBook（贵）、Notion（要自己搭）。"
            "我们比它们轻量，专注设计师。"
        )
        self.assertTrue(r5["ok"], f"轮次 5 失败: {r5.get('error')}")
        # 回应了竞品相关内容（提到竞品名或提出竞品相关的深入问题）
        _assert_contains_any(self, r5["content"], [
            "dubsado", "honeybook", "notion",
            # 或者提出了竞品相关的深入问题（更好的行为）
            "差异", "区别", "定位", "专注", "差异化",
            "differentiat", "position", "niche",
        ], "轮次 5 竞品回应: ")

        # ── 第 6 轮：用户声称假设为事实 ──
        r6 = conv.send("我觉得所有独立设计师都需要这个，这个假设应该没问题。")
        self.assertTrue(r6["ok"], f"轮次 6 失败: {r6.get('error')}")
        # 将"所有设计师都需要"标记为假设
        _assert_contains_any(self, r6["content"], [
            "假设", "未验证", "assumption", "unverified", "待验证",
            "验证", "validate", "测试", "test",
        ], "轮次 6 假设标记: ")

        # ── 第 7 轮：提供调研数据 ──
        r7 = conv.send(
            "我做过小范围调研，20 个设计师里 12 个表示有兴趣，其中 5 个愿意付费试用。"
        )
        self.assertTrue(r7["ok"], f"轮次 7 失败: {r7.get('error')}")
        # 区分事实和推断
        _assert_contains_any(self, r7["content"], [
            "调研", "样本", "调查", "survey", "数据",
            "假设", "推断", "验证", "局限",
        ], "轮次 7 事实/假设区分: ")

        # ── 第 8 轮：技术选型 ──
        r8 = conv.send(
            "第一阶段先做本地 app，不做云同步。技术栈我想用 React + SQLite。"
        )
        self.assertTrue(r8["ok"], f"轮次 8 失败: {r8.get('error')}")
        # 不锁定技术栈：检查没有把技术选型当作已确认事实
        # 正确行为可以是：标记为候选/待决策，或提出相关验证问题，或建议留到实施阶段
        r8_lower = r8["content"].lower()
        locks_tech = any(m in r8_lower for m in [
            "技术栈确定", "技术栈已定", "使用 react", "我们将使用",
            "tech stack confirmed", "we will use react",
        ])
        self.assertFalse(
            locks_tech,
            f"轮次 8 不应锁定技术栈。实际输出前 300 字：\n{r8['content'][:300]}"
        )

        # ── 第 9 轮：确认方向，请求 PRD ──
        r9 = conv.send("方向确认了，请进入 PRD 规划。")
        self.assertTrue(r9["ok"], f"轮次 9 失败: {r9.get('error')}")
        # 产出 PRD 相关内容
        _assert_contains_any(self, r9["content"], [
            "prd", "需求", "产品需求", "功能", "范围", "scope",
            "目标用户", "成功指标", "非目标",
        ], "轮次 9 PRD 内容: ")
        # PRD 内容与之前讨论一致
        _assert_references_input(self, r9["content"],
                                 ["设计师", "客户", "档案", "状态", "提醒"],
                                 min_match=2, msg_prefix="轮次 9 一致性: ")

        # ── 第 10 轮：确认 PRD，请求 Roadmap ──
        r10 = conv.send("PRD 确认，请进入 Roadmap。")
        self.assertTrue(r10["ok"], f"轮次 10 失败: {r10.get('error')}")
        # Roadmap 包含至少 2 个阶段
        _assert_contains_any(self, r10["content"], [
            "阶段", "phase", "milestone", "里程碑",
            "now", "next", "later", "第一阶段", "第二阶段",
            "phase 1", "phase 2",
        ], "轮次 10 阶段: ")
        # 阶段内容与 MVP 范围一致
        _assert_references_input(self, r10["content"],
                                 ["客户", "档案", "状态", "提醒", "设计师"],
                                 min_match=1, msg_prefix="轮次 10 一致性: ")

        # 全局验证
        elapsed = time.time() - total_start
        history = conv.get_history()
        self.assertEqual(len(history), 20, f"应有 20 条消息，实际 {len(history)}")
        self.assertLess(elapsed, 300, f"总耗时 {elapsed:.1f}s 超过 300s 上限")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# P0_003 — 吸收已有材料
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY")
class TestP0_003_MaterialAbsorption(unittest.TestCase):
    """P0_003: 用户提供 PRD 草稿 → 系统吸收并审查"""

    def test_P0_003__absorbs_prd_draft_with_review(self):
        provider = get_available_provider()
        conv = Conversation(provider=provider)

        # ── 第 1 轮：提供 PRD 草稿 ──
        r1 = conv.send(
            "我有一份 PRD 草稿：\n"
            "产品名：DevPulse\n"
            "目标用户：独立开发者\n"
            "核心功能：从 GitHub 同步 commit 记录，生成每周开发报告\n"
            "成功指标：用户每周查看报告\n"
            "技术栈：Next.js + GitHub API\n"
            "竞品：WakaTime（只追踪编码时间，不追踪项目进展）\n"
            "请审查。"
        )
        self.assertTrue(r1["ok"], f"轮次 1 失败: {r1.get('error')}")
        # 引用 PRD 中的具体元素
        _assert_references_input(self, r1["content"],
                                 ["devpulse", "github", "commit", "周报", "wakatime"],
                                 min_match=2, msg_prefix="轮次 1 引用: ")
        # 提出审查性问题（不是直接接受）
        _assert_contains_any(self, r1["content"], [
            "？", "什么", "哪个", "如何", "怎样", "为什么",
            "请澄清", "需要确认", "请补充",
        ], "轮次 1 审查问题: ")

        # ── 第 2 轮：补充竞品差异 ──
        r2 = conv.send(
            "竞品差异：WakaTime 只统计编码时间，DevPulse 关注项目级进展可视化。"
            "目标用户只做独立开发者，不做团队。"
        )
        self.assertTrue(r2["ok"], f"轮次 2 失败: {r2.get('error')}")
        # 审查行为：提出验证性问题或区分已确认/待验证信息
        _assert_contains_any(self, r2["content"], [
            "假设", "待验证", "assumption", "unverified", "需要验证",
            "确认", "事实", "fact",
            # 或者提出了具体的验证性问题（更好的行为）
            "？", "什么", "哪个", "如何", "具体",
        ], "轮次 2 审查行为: ")

        # ── 第 3 轮：确认推进 ──
        r3 = conv.send("确认，请继续推进到 PRD。")
        self.assertTrue(r3["ok"], f"轮次 3 失败: {r3.get('error')}")
        # PRD 内容与材料一致
        _assert_references_input(self, r3["content"],
                                 ["devpulse", "github", "独立开发", "周报"],
                                 min_match=2, msg_prefix="轮次 3 一致性: ")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# P0_004 — 获得规划产物（复用 P0_002 上下文）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY")
class TestP0_004_PlanningArtifacts(unittest.TestCase):
    """P0_004: 在 P0_002 的 10 轮基础上请求用户故事和验收标准"""

    def test_P0_004__user_stories_with_acceptance_criteria(self):
        provider = get_available_provider()
        conv = Conversation(provider=provider)
        total_start = time.time()

        # 复用 P0_002 的 10 轮对话
        turns = [
            "我想做一个给自由职业设计师用的客户管理工具。",
            "目标用户是每天处理 3-5 个客户的自由职业设计师。痛点是客户资料、报价、交付状态散落在微信、邮件和笔记里。",
            "MVP 只做三件事：客户档案、项目状态追踪、下一步提醒。不做发票、不做合同、不做团队协作。",
            "成功指标：2 周内 5 位试用者能减少漏跟进的情况。非目标：不做 CRM 全功能，只做设计师场景。",
            "竞品：Dubsado（太重）、HoneyBook（贵）、Notion（要自己搭）。我们比它们轻量，专注设计师。",
            "我觉得所有独立设计师都需要这个，这个假设应该没问题。",
            "我做过小范围调研，20 个设计师里 12 个表示有兴趣，其中 5 个愿意付费试用。",
            "第一阶段先做本地 app，不做云同步。技术栈我想用 React + SQLite。",
            "方向确认了，请进入 PRD 规划。",
            "PRD 确认，请进入 Roadmap。",
        ]
        for i, turn in enumerate(turns):
            r = conv.send(turn)
            self.assertTrue(r["ok"], f"P0_002 轮次 {i+1} 失败: {r.get('error')}")

        # ── 请求用户故事 ──
        r_plan = conv.send(
            "Roadmap 确认了，请生成详细的用户故事和验收标准。"
        )
        self.assertTrue(r_plan["ok"], f"规划产物请求失败: {r_plan.get('error')}")
        self.assertGreater(len(r_plan["content"]), 100, "规划产物输出太短")

        content = r_plan["content"].lower()

        # 内容验证：包含至少 3 个用户故事（检查"作为"/"用户故事"/"场景"出现次数）
        story_markers = ["作为", "用户故事", "user story", "场景", "scenario"]
        story_count = sum(content.count(m) for m in story_markers)
        self.assertGreaterEqual(story_count, 3,
                                f"用户故事数量不足（检测到 {story_count} 个标记）。"
                                f"输出前 500 字：\n{r_plan['content'][:500]}")

        # 内容验证：包含验收标准
        _assert_contains_any(self, r_plan["content"], [
            "验收", "标准", "acceptance", "criteria", "ac",
            "given", "when", "then", "条件", "验证",
        ], "验收标准: ")

        # 内容验证：与设计师客户管理场景相关
        _assert_references_input(self, r_plan["content"],
                                 ["设计师", "客户", "项目", "跟进", "档案", "提醒"],
                                 min_match=2, msg_prefix="场景一致性: ")

        # 内容验证：不包含非目标功能
        _assert_not_contains_any(self, r_plan["content"], [
            "发票", "合同", "团队协作", "invoice", "contract",
        ], "非目标功能: ")

        elapsed = time.time() - total_start
        self.assertLess(elapsed, 360, f"总耗时 {elapsed:.1f}s 超过 360s 上限")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# P0_005 — 进入实施规划（复用 P0_004 上下文）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY")
class TestP0_005_ImplementationPlanning(unittest.TestCase):
    """P0_005: 在 P0_004 基础上请求实施规划"""

    def test_P0_005__implementation_plan_with_tasks(self):
        provider = get_available_provider()
        conv = Conversation(provider=provider)
        total_start = time.time()

        # 复用 P0_002 的 10 轮 + P0_004 的 1 轮
        turns = [
            "我想做一个给自由职业设计师用的客户管理工具。",
            "目标用户是每天处理 3-5 个客户的自由职业设计师。痛点是客户资料、报价、交付状态散落在微信、邮件和笔记里。",
            "MVP 只做三件事：客户档案、项目状态追踪、下一步提醒。不做发票、不做合同、不做团队协作。",
            "成功指标：2 周内 5 位试用者能减少漏跟进的情况。非目标：不做 CRM 全功能，只做设计师场景。",
            "竞品：Dubsado（太重）、HoneyBook（贵）、Notion（要自己搭）。我们比它们轻量，专注设计师。",
            "我觉得所有独立设计师都需要这个，这个假设应该没问题。",
            "我做过小范围调研，20 个设计师里 12 个表示有兴趣，其中 5 个愿意付费试用。",
            "第一阶段先做本地 app，不做云同步。技术栈我想用 React + SQLite。",
            "方向确认了，请进入 PRD 规划。",
            "PRD 确认，请进入 Roadmap。",
            "Roadmap 确认了，请生成详细的用户故事和验收标准。",
        ]
        for i, turn in enumerate(turns):
            r = conv.send(turn)
            self.assertTrue(r["ok"], f"前置轮次 {i+1} 失败: {r.get('error')}")

        # ── 请求实施规划 ──
        r_impl = conv.send(
            "规划产物确认了，请进入实施规划，列出具体的开发任务和排序。"
            "时间估算由我自己填，你只需要列出任务和优先级。"
        )
        self.assertTrue(r_impl["ok"], f"实施规划请求失败: {r_impl.get('error')}")
        self.assertGreater(len(r_impl["content"]), 300, "实施规划输出太短")

        content = r_impl["content"].lower()

        # 内容验证：至少 5 个具体开发任务
        task_markers = ["任务", "task", "开发", "实现", "搭建", "创建", "对接", "编写"]
        task_count = sum(content.count(m) for m in task_markers)
        self.assertGreaterEqual(task_count, 5,
                                f"开发任务数量不足（检测到 {task_count} 个标记）。"
                                f"输出前 500 字：\n{r_impl['content'][:500]}")

        # 内容验证：有排序/优先级
        _assert_contains_any(self, r_impl["content"], [
            "阶段", "phase", "优先", "priority", "第 1", "第 2",
            "先做", "然后", "最后", "首先", "next", "then",
        ], "排序: ")

        # 内容验证：任务与设计师客户管理相关
        _assert_references_input(self, r_impl["content"],
                                 ["客户档案", "状态", "提醒", "数据库", "api", "ui"],
                                 min_match=2, msg_prefix="任务相关性: ")

        # 内容验证：包含验证/测试计划
        _assert_contains_any(self, r_impl["content"], [
            "测试", "验证", "test", "verify", "验收", "quality",
        ], "验证计划: ")

        # 内容验证：不包含非目标功能
        _assert_not_contains_any(self, r_impl["content"], [
            "发票", "合同", "团队协作", "invoice", "contract",
        ], "非目标功能: ")

        elapsed = time.time() - total_start
        self.assertLess(elapsed, 360, f"总耗时 {elapsed:.1f}s 超过 360s 上限")


if __name__ == "__main__":
    unittest.main()
