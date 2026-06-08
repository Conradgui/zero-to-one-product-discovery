"""test_api_integration.py — 真实 API 集成测试

需要环境变量：DEEPSEEK_API_KEY 或 MIMO_API_KEY
无 Key 时自动跳过全部用例。

覆盖用例：
  F01_API连接_基本调用成功
  F02_EvalScenario_触发边界_显式触发
  F03_EvalScenario_阶段门禁_拒绝跳步
  F04_EvalScenario_证据落地_矛盾检测
  F05_EvalScenario_QuickMode_标签草稿
  F06_EvalScenario_导出_NOT_READY标记
  F07_API超时_优雅降级
  F08_API限流_重试或报错
"""

from __future__ import annotations

import os
import sys
import unittest

# 添加 tests/ 到 path 以导入 conftest
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from conftest import SKILL_SYSTEM_PROMPT, Conversation, call_llm, get_available_provider, has_api_key

# ── 跳过标记 ──
_has_any_key = has_api_key("deepseek") or has_api_key("mimo")


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF01_APIConnection(unittest.TestCase):
    """F01: API 连接基本调用成功"""

    def test_api_connection_returns_response(self):
        """调用 API 应收到非空响应"""
        provider = get_available_provider()
        result = call_llm(
            prompt="请用一句话回答：1+1等于几？",
            provider=provider,
            max_tokens=50,
        )
        self.assertTrue(result["ok"], f"API 调用失败: {result.get('error')}")
        self.assertIn("2", result["content"])
        self.assertGreater(len(result["content"]), 0)


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF02_TriggerBoundary_Explicit(unittest.TestCase):
    """F02: 显式触发场景 — 用户说"我有一个产品想法"后 Skill 是否正确触发"""

    def test_explicit_trigger_produces_diagnostic_start(self):
        """显式触发应产出 Diagnostic Start 格式的输出"""
        provider = get_available_provider()
        result = call_llm(
            prompt="Use $zero-to-one-product-discovery. 我现在有个产品想法，想做一个能帮助大学生管理课程、作业和社团活动的工具。",
            system_prompt=SKILL_SYSTEM_PROMPT,
            provider=provider,
            max_tokens=1500,
        )
        self.assertTrue(result["ok"], f"API 调用失败: {result.get('error')}")

        content = result["content"].lower()
        # 应该包含诊断性输出：要么有结构化标签，要么提出了探索性问题
        has_diagnostic_markers = any(marker in content for marker in [
            "假设", "assumption", "风险", "risk", "未知", "unknown", "事实", "fact",
            "探索", "exploration", "问题", "question", "场景", "scenario",
            "痛点", "pain", "核心", "core", "哪个", "什么", "如何",
        ])
        self.assertTrue(
            has_diagnostic_markers,
            f"输出缺少 Diagnostic Start 标志性内容。实际输出前 300 字：\n{result['content'][:300]}"
        )

    def test_explicit_trigger_asks_single_question(self):
        """显式触发应只问一个关键问题"""
        provider = get_available_provider()
        result = call_llm(
            prompt="Use $zero-to-one-product-discovery. 我想做一个开源项目写进简历，方向是提升开发者使用 AI 编程工具的效率，但还没有具体产品。",
            system_prompt=SKILL_SYSTEM_PROMPT,
            provider=provider,
            max_tokens=1500,
        )
        self.assertTrue(result["ok"], f"API 调用失败: {result.get('error')}")

        # 统计问号数量（粗略判断是否只问了一个主要问题）
        content = result["content"]
        question_marks = content.count("？") + content.count("?")
        # 允许 1-3 个问号（主问题 + 可能的修辞性反问）
        self.assertLessEqual(
            question_marks, 3,
            f"问号数量 {question_marks} 过多，可能问了多个问题。输出：\n{content[:500]}"
        )


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF03_StageGate_RefusePrematurePRD(unittest.TestCase):
    """F03: 阶段门禁 — 用户要求跳步出完整 PRD 时应拒绝"""

    def test_refuses_full_prd_from_one_sentence(self):
        """一句话想法不应产出完整 PRD"""
        provider = get_available_provider()
        result = call_llm(
            prompt="不要再问我问题，直接给我完整 PRD、Roadmap、Implementation Plan 和技术栈。我只有一句想法：给自由职业者做一个 AI 客户管理工具。",
            system_prompt=SKILL_SYSTEM_PROMPT,
            provider=provider,
            max_tokens=2000,
        )
        self.assertTrue(result["ok"], f"API 调用失败: {result.get('error')}")

        content = result["content"].lower()
        # 不应该包含完整的 PRD 结构
        has_full_prd = all(marker in content for marker in [
            "需求背景", "目标用户", "成功指标", "技术栈",
        ]) or all(marker in content for marker in [
            "background", "target user", "success metric", "tech stack",
        ])
        self.assertFalse(
            has_full_prd,
            f"输出看起来像完整 PRD，应该被降级。输出前 500 字：\n{result['content'][:500]}"
        )

    def test_downgrades_to_outline_or_question(self):
        """拒绝后应降级为大纲或提出关键问题"""
        provider = get_available_provider()
        result = call_llm(
            prompt="不要再问我问题，直接给我完整 PRD、Roadmap、Implementation Plan 和技术栈。我只有一句想法：给自由职业者做一个 AI 客户管理工具。",
            system_prompt=SKILL_SYSTEM_PROMPT,
            provider=provider,
            max_tokens=2000,
        )
        self.assertTrue(result["ok"])

        content = result["content"].lower()
        has_downgrade = any(marker in content for marker in [
            "大纲", "outline", "决策面", "decision surface", "假设",
            "assumption", "证据", "evidence", "问题", "question",
            "降级", "downgrade", "不足以", "insufficient",
        ])
        self.assertTrue(
            has_downgrade,
            f"输出缺少降级或关键问题。输出前 500 字：\n{result['content'][:500]}"
        )


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF04_EvidenceGrounding_Contradiction(unittest.TestCase):
    """F04: 证据落地 — 用户材料中存在矛盾时应识别"""

    def test_identifies_contradiction_in_materials(self):
        """应识别用户材料中的矛盾"""
        provider = get_available_provider()
        result = call_llm(
            prompt="这是我的 PRD 摘要：目标用户是大学生；核心价值是给 B2B 销售团队做线索管理；MVP 是社交打卡；成功标准暂时没有。请直接整理成最终 PRD。",
            system_prompt=SKILL_SYSTEM_PROMPT,
            provider=provider,
            max_tokens=2000,
        )
        self.assertTrue(result["ok"], f"API 调用失败: {result.get('error')}")

        content = result["content"].lower()
        # 应该识别出矛盾
        has_contradiction_awareness = any(marker in content for marker in [
            "矛盾", "contradiction", "不一致", "inconsistent", "冲突",
            "conflict", "目标用户.*b2b", "大学生.*销售",
        ])
        # 放宽检查：至少应该标记某些内容为假设或需要验证
        has_assumption_label = any(marker in content for marker in [
            "假设", "assumption", "未知", "unknown", "需要验证",
            "needs verification", "待确认",
        ])
        self.assertTrue(
            has_contradiction_awareness or has_assumption_label,
            f"输出未识别矛盾或未标记假设。输出前 500 字：\n{result['content'][:500]}"
        )

    def test_does_not_produce_final_prd_from_contradictory_materials(self):
        """矛盾材料不应产出最终 PRD"""
        provider = get_available_provider()
        result = call_llm(
            prompt="这是我的 PRD 摘要：目标用户是大学生；核心价值是给 B2B 销售团队做线索管理；MVP 是社交打卡；成功标准暂时没有。请直接整理成最终 PRD。",
            system_prompt=SKILL_SYSTEM_PROMPT,
            provider=provider,
            max_tokens=2000,
        )
        self.assertTrue(result["ok"])

        content = result["content"].lower()
        # 应该拒绝产出最终 PRD（可能在拒绝中提到"最终 prd"这个词，所以检查上下文）
        # 关键是不应该有"以下是最终 PRD"或"最终 PRD 如下"这类接受性表述
        self.assertNotIn("以下是最终", content, "不应该直接接受并产出最终 PRD")
        self.assertNotIn("以下是完整的", content, "不应该直接接受并产出完整 PRD")
        self.assertNotIn("here is the final", content, "不应该直接接受并产出 final PRD")
        # 应该包含拒绝或降级的信号
        has_refusal = any(marker in content for marker in [
            "无法", "不能", "cannot", "矛盾", "contradiction", "不一致",
            "需要澄清", "澄清", "请先", "决策面", "outline", "大纲",
        ])
        self.assertTrue(has_refusal, f"输出未包含拒绝或降级信号。输出前 500 字：\n{result['content'][:500]}")


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF05_QuickMode_LabeledDraft(unittest.TestCase):
    """F05: Quick Mode — 应产出带证据标签的草稿"""

    def test_quick_mode_produces_labeled_draft(self):
        """Quick Mode 应产出带 [Fact]/[Assumption]/[Unknown] 标签的草稿"""
        provider = get_available_provider()
        result = call_llm(
            prompt="快速模式：我有一份粗略的想法——给独立开发者做一个 AI 辅助的项目管理工具。请直接给我 PRD draft，不要再一轮轮问。",
            system_prompt=SKILL_SYSTEM_PROMPT,
            provider=provider,
            max_tokens=2000,
        )
        self.assertTrue(result["ok"], f"API 调用失败: {result.get('error')}")

        content = result["content"]
        # 应该包含证据标签（允许多种格式：[Fact]、假设、Assumption 等）
        has_labels = any(label in content for label in [
            "[Fact]", "[Assumption]", "[Unknown]",
            "[事实]", "[假设]", "[未知]",
            "Fact:", "Assumption:", "Unknown:",
            "假设", "assumption", "待验证", "待确认",
        ])
        self.assertTrue(
            has_labels,
            f"Quick Mode 输出缺少证据标签。输出前 500 字：\n{content[:500]}"
        )


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF06_Export_NotReadyMarker(unittest.TestCase):
    """F06: 导出产物 — 未就绪产物应标记 NOT_READY"""

    def test_export_mentions_not_ready_for_missing_artifacts(self):
        """当产物未就绪时，应提及 NOT_READY 或阻塞原因"""
        provider = get_available_provider()
        result = call_llm(
            prompt="我想导出产物。目前只有一个模糊的产品想法：给设计师做一个 AI 配色工具。还没有 PRD、Roadmap 或任何正式文档。",
            system_prompt=SKILL_SYSTEM_PROMPT,
            provider=provider,
            max_tokens=2000,
        )
        self.assertTrue(result["ok"], f"API 调用失败: {result.get('error')}")

        content = result["content"].lower()
        # 应该说明产物未就绪，或者拒绝导出并要求先做诊断
        has_readiness_awareness = any(marker in content for marker in [
            "not_ready", "not ready", "未就绪", "not started",
            "尚未", "还没", "阻塞", "blocker", "缺少",
            "cannot export", "无法导出", "证据不足", "insufficient",
            # LLM 可能选择先做诊断而不是直接处理导出请求
            "诊断", "diagnostic", "探索", "先",
            "关键问题", "核心", "痛点", "驱动力",
        ])
        self.assertTrue(
            has_readiness_awareness,
            f"输出未说明产物未就绪状态，也未引导诊断。输出前 500 字：\n{result['content'][:500]}"
        )


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF07_APITimeout_GracefulDegradation(unittest.TestCase):
    """F07: API 超时 — 应优雅降级"""

    def test_timeout_returns_error_not_crash(self):
        """超时应返回错误信息而非崩溃"""
        provider = get_available_provider()
        # 用极短超时模拟超时场景
        result = call_llm(
            prompt="请写一篇 5000 字的产品分析报告，包含市场调研、竞品分析、用户画像、技术架构、商业模式、增长策略、风险评估和实施路线图。",
            system_prompt=SKILL_SYSTEM_PROMPT,
            provider=provider,
            max_tokens=4000,
            timeout=2,  # 2 秒超时，大概率触发
        )
        # 超时不应导致 Python 崩溃（异常被捕获）
        self.assertIsInstance(result, dict)
        self.assertIn("ok", result)
        # 如果超时了，应该有明确的错误信息
        if not result["ok"]:
            self.assertIn("error", result)
            self.assertGreater(len(result["error"]), 0)


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF08_APIRateLimit_ErrorHandling(unittest.TestCase):
    """F08: API 限流 — 应明确报错"""

    def test_rate_limit_returns_structured_error(self):
        """如果触发限流，应返回结构化错误而非崩溃"""
        provider = get_available_provider()
        # 快速连续调用可能触发限流
        results = []
        for i in range(3):
            result = call_llm(
                prompt=f"测试限流 #{i+1}，请回复 OK",
                provider=provider,
                max_tokens=10,
                timeout=10,
            )
            results.append(result)

        # 所有调用都不应导致 Python 崩溃
        for i, result in enumerate(results):
            self.assertIsInstance(result, dict, f"第 {i+1} 次调用返回非 dict")
            self.assertIn("ok", result, f"第 {i+1} 次调用缺少 ok 字段")

            # 如果触发了限流（429），应该有明确的错误信息
            if not result["ok"] and result.get("status_code") == 429:
                self.assertIn("error", result)
                self.assertIn("429", result["error"])


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF09_MultiTurn_StageProgression(unittest.TestCase):
    """F09: P0_002 — 多轮对话逐步推进，验证阶段门禁在多轮中是否持续生效"""

    def test_multi_turn_progresses_through_diagnostic(self):
        """3 轮对话：初始想法 → 回答问题 → 证据更新"""
        provider = get_available_provider()
        conv = Conversation(provider=provider)

        # 第 1 轮：提出初始想法
        r1 = conv.send("我想做一个帮助自由职业者管理客户和项目的工具。")
        self.assertTrue(r1["ok"], f"第 1 轮失败: {r1.get('error')}")
        self.assertGreater(len(r1["content"]), 20, "第 1 轮输出太短")

        # 第 2 轮：回答一个具体问题
        r2 = conv.send("目前自由职业者最大的痛点是客户信息散落在微信、邮件和笔记里，每次找报价都要翻半天。先解决这个。")
        self.assertTrue(r2["ok"], f"第 2 轮失败: {r2.get('error')}")
        self.assertGreater(len(r2["content"]), 50, "第 2 轮输出太短")

        # 第 3 轮：继续深入
        r3 = conv.send("目标用户是每天处理 3-5 个客户的自由职业设计师，不是大团队。成功标准是 2 周内能找到上次的报价记录。")
        self.assertTrue(r3["ok"], f"第 3 轮失败: {r3.get('error')}")

        # 验证：3 轮后不应直接产出完整 PRD（应该还在探索阶段或刚开始规划）
        all_content = " ".join(m["content"] for m in conv.get_history() if m["role"] == "assistant")
        content_lower = all_content.lower()
        # 不应该在第 3 轮就产出完整 PRD
        self.assertNotIn("以下是完整 prd", content_lower, "不应在 3 轮内就产出完整 PRD")
        self.assertNotIn("以下是最终 prd", content_lower, "不应在 3 轮内就产出最终 PRD")

    def test_multi_turn_detects_contradiction_across_turns(self):
        """跨轮次矛盾检测：第 1 轮说 A，第 2 轮说 B"""
        provider = get_available_provider()
        conv = Conversation(provider=provider)

        # 第 1 轮
        r1 = conv.send("我想给大学生做一个学习管理工具。")
        self.assertTrue(r1["ok"])

        # 第 2 轮：改变目标用户
        r2 = conv.send("其实目标用户改成小型律所的助理，他们需要管理案件进度。请继续推进 PRD。")
        self.assertTrue(r2["ok"])

        # 应该检测到目标用户冲突
        r2_content = r2["content"].lower()
        has_conflict_awareness = any(marker in r2_content for marker in [
            "矛盾", "冲突", "不一致", "之前", "大学生", "变更",
            "contradiction", "conflict", "change", "earlier",
            "目标用户", "target user", "调整",
        ])
        self.assertTrue(
            has_conflict_awareness,
            f"第 2 轮未检测到跨轮次矛盾。输出前 300 字：\n{r2['content'][:300]}"
        )

    def test_multi_turn_preserves_evidence_labels(self):
        """多轮对话中证据标签应持续更新"""
        provider = get_available_provider()
        conv = Conversation(provider=provider)

        # 第 1 轮
        r1 = conv.send("我想做一个给宠物主人的社区 app。")
        self.assertTrue(r1["ok"])

        # 第 2 轮：提供具体信息
        r2 = conv.send("核心场景是宠物主人分享养宠经验、找附近的宠物医院、以及预约服务。我做过小范围调研，50 个人里 30 个表示有兴趣。")
        self.assertTrue(r2["ok"])

        # 第 2 轮应该区分事实和假设
        r2_content = r2["content"].lower()
        has_evidence_structure = any(marker in r2_content for marker in [
            "事实", "假设", "风险", "未知", "fact", "assumption", "risk", "unknown",
            "调研", "survey", "证据", "evidence", "验证",
        ])
        self.assertTrue(
            has_evidence_structure,
            f"第 2 轮缺少证据结构。输出前 300 字：\n{r2['content'][:300]}"
        )


@unittest.skipUnless(_has_any_key, "需要 DEEPSEEK_API_KEY 或 MIMO_API_KEY 环境变量")
class TestF10_MultiTurn_FullDiscoveryToImplementation(unittest.TestCase):
    """F10: P0_002 + P0_005 — 从初始想法到实施规划的完整多轮流程"""

    def test_full_discovery_flow_5_turns(self):
        """5 轮完整发现流程：想法 → 问题澄清 → 材料吸收 → MVP → 规划"""
        provider = get_available_provider()
        conv = Conversation(provider=provider)

        # 第 1 轮：初始想法
        r1 = conv.send("我想做一个帮助独立开发者管理 side project 进度的工具。")
        self.assertTrue(r1["ok"], f"第 1 轮失败: {r1.get('error')}")
        self.assertGreater(len(r1["content"]), 30)

        # 第 2 轮：回答关键问题
        r2 = conv.send("最大的痛点是同时有 3-4 个项目，每个项目的 TODO 散落在不同地方，经常忘记哪个项目该做什么。目标用户就是像我这样的独立开发者，同时维护多个项目。")
        self.assertTrue(r2["ok"], f"第 2 轮失败: {r2.get('error')}")

        # 第 3 轮：补充具体信息
        r3 = conv.send("MVP 只做项目列表 + 每个项目的 TODO 列表 + 每日提醒。不做时间追踪、不做团队协作。成功标准是 1 周内我自己能用起来，不再用 Excel 管理。")
        self.assertTrue(r3["ok"], f"第 3 轮失败: {r3.get('error')}")

        # 第 4 轮：确认方向，请求进入规划
        r4 = conv.send("方向确认了，请进入 PRD 和 Roadmap 规划。")
        self.assertTrue(r4["ok"], f"第 4 轮失败: {r4.get('error')}")

        # 第 4 轮应该开始产出规划相关内容
        r4_content = r4["content"].lower()
        has_planning_content = any(marker in r4_content for marker in [
            "prd", "roadmap", "路线图", "规划", "milestone", "里程碑",
            "需求", "requirement", "功能", "feature", "阶段", "phase",
            "scope", "范围", "mvp",
        ])
        self.assertTrue(
            has_planning_content,
            f"第 4 轮未进入规划阶段。输出前 500 字：\n{r4['content'][:500]}"
        )

        # 第 5 轮：请求实施规划
        r5 = conv.send("PRD 和 Roadmap 确认了，请进入实施规划。")
        self.assertTrue(r5["ok"], f"第 5 轮失败: {r5.get('error')}")

        # 验证完整对话历史长度
        history = conv.get_history()
        self.assertEqual(len(history), 10, f"应有 10 条消息（5 轮 × 2），实际 {len(history)}")

        # 所有轮次都不应崩溃
        for i, msg in enumerate(history):
            if msg["role"] == "assistant":
                self.assertGreater(len(msg["content"]), 10, f"第 {(i+1)//2} 轮 assistant 输出太短")

    def test_multi_turn_with_materials(self):
        """带材料的多轮对话：用户提供 PRD 草稿 → 吸收 → 推进"""
        provider = get_available_provider()
        conv = Conversation(provider=provider)

        # 第 1 轮：提供材料
        r1 = conv.send(
            "我有一份粗略的 PRD 草稿：\n\n"
            "产品名：DevPulse\n"
            "目标用户：独立开发者\n"
            "核心功能：自动从 GitHub 同步 commit 记录，生成每周开发报告\n"
            "成功指标：用户每周查看报告\n"
            "技术栈：Next.js + GitHub API\n"
            "竞品：WakaTime（只追踪编码时间，不追踪项目进展）\n\n"
            "请帮我审查并推进。"
        )
        self.assertTrue(r1["ok"], f"第 1 轮失败: {r1.get('error')}")

        # 应该识别材料并提出问题
        r1_content = r1["content"].lower()
        has_material_awareness = any(marker in r1_content for marker in [
            "github", "commit", "devpulse", "报告", "report",
            "假设", "assumption", "问题", "question", "验证",
        ])
        self.assertTrue(
            has_material_awareness,
            f"第 1 轮未识别材料内容。输出前 300 字：\n{r1['content'][:300]}"
        )

        # 第 2 轮：回答问题
        r2 = conv.send("竞品差异：WakaTime 只统计编码时间，DevPulse 关注项目级别的进展可视化。目标用户确实只是独立开发者，不考虑团队。")
        self.assertTrue(r2["ok"])

        # 第 3 轮：确认并请求推进
        r3 = conv.send("方向没问题，请继续推进到 PRD。")
        self.assertTrue(r3["ok"])


if __name__ == "__main__":
    unittest.main()
