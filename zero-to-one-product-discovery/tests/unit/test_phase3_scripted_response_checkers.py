"""Scripted response checker tests for P0 user-path guardrails.

These tests do not claim that a real model behaves correctly. They verify the
offline checkers used by Phase 4/5 can catch obvious bad responses.
"""

from __future__ import annotations

import re
import unittest


def _question_count(text: str) -> int:
    return text.count("?") + text.count("？")


def assert_diagnostic_start(text: str) -> None:
    lowered = text.lower()
    forbidden_final_markers = [
        "以下是完整 prd",
        "以下是最终 prd",
        "完整需求文档",
        "here is the final prd",
    ]
    if any(marker in lowered for marker in forbidden_final_markers):
        raise AssertionError("diagnostic start must not produce a final PRD")
    if _question_count(text) == 0 or _question_count(text) > 3:
        raise AssertionError("diagnostic start should ask one focused question")
    if not any(marker in lowered for marker in ["假设", "风险", "未知", "assumption", "risk", "unknown"]):
        raise AssertionError("diagnostic start should expose evidence uncertainty")


def assert_material_review_flags_contradiction(text: str) -> None:
    lowered = text.lower()
    contradiction_markers = ["矛盾", "冲突", "不一致", "contradiction", "conflict", "inconsistent"]
    specific_pairing = re.search(r"(大学生|student).*(b2b|销售|sales)|(b2b|销售|sales).*(大学生|student)", lowered)
    if not any(marker in lowered for marker in contradiction_markers) and not specific_pairing:
        raise AssertionError("material review should explicitly flag contradiction")
    if any(marker in lowered for marker in ["以下是最终", "以下是完整", "here is the final"]):
        raise AssertionError("contradictory material must not be accepted as final")


def assert_multiturn_history_is_ordered(history: list[dict[str, str]], expected_turns: int) -> None:
    if len(history) != expected_turns * 2:
        raise AssertionError("history must contain user/assistant pairs for every turn")
    for index, message in enumerate(history):
        expected_role = "user" if index % 2 == 0 else "assistant"
        if message.get("role") != expected_role:
            raise AssertionError(f"turn {index} should be {expected_role}")
        if not message.get("content"):
            raise AssertionError(f"turn {index} content must be non-empty")


def assert_user_stories_have_acceptance_criteria(text: str) -> None:
    lowered = text.lower()
    story_markers = text.count("作为") + lowered.count("user story")
    if story_markers < 2:
        raise AssertionError("planning output should contain multiple user stories")
    if not any(marker in lowered for marker in ["验收标准", "acceptance criteria", "given", "when", "then"]):
        raise AssertionError("planning output should include acceptance criteria")
    forbidden = ["发票", "合同", "团队协作", "invoice", "contract"]
    if any(marker in lowered for marker in forbidden):
        raise AssertionError("planning output should preserve non-goals")


class TestPhase3ScriptedResponseCheckers(unittest.TestCase):
    def test_P0_001__scripted_diagnostic_start_requires_one_next_question(self):
        response = (
            "我先把这看作一个待验证的早期想法。\n"
            "[假设] 用户确实会为 side project 管理付费。\n"
            "[风险] 真实痛点可能只是提醒，而不是完整项目管理。\n"
            "你现在最想先解决的是忘记下一步、进度不可见，还是多个工具之间切换？"
        )

        assert_diagnostic_start(response)

    def test_P0_001__scripted_diagnostic_start_rejects_full_prd(self):
        bad_response = (
            "以下是完整 PRD：\n"
            "目标用户：独立开发者\n"
            "技术栈：React + SQLite\n"
            "成功指标：DAU 增长"
        )

        with self.assertRaises(AssertionError):
            assert_diagnostic_start(bad_response)

    def test_P0_003__material_review_checker_flags_contradictory_summary(self):
        response = (
            "材料里存在明显不一致：目标用户写的是大学生，但核心价值描述成 B2B 销售线索管理。\n"
            "我不会把它整理成 final PRD，先需要确认真实目标用户。"
        )

        assert_material_review_flags_contradiction(response)

    def test_P0_003__material_review_checker_rejects_accepting_conflict_as_final(self):
        bad_response = (
            "以下是最终 PRD：目标用户是大学生，核心价值是给 B2B 销售团队管理线索。"
        )

        with self.assertRaises(AssertionError):
            assert_material_review_flags_contradiction(bad_response)

    def test_P0_002__conversation_harness_preserves_turn_order_and_history(self):
        history = []
        for index in range(10):
            history.append({"role": "user", "content": f"user turn {index + 1}"})
            history.append({"role": "assistant", "content": f"assistant turn {index + 1}"})

        assert_multiturn_history_is_ordered(history, expected_turns=10)

    def test_P0_004__scripted_user_stories_require_acceptance_criteria(self):
        response = (
            "用户故事 1：作为自由职业设计师，我想查看客户档案。\n"
            "验收标准：能看到客户名称、项目状态和下一步提醒。\n"
            "用户故事 2：作为自由职业设计师，我想更新项目状态。\n"
            "验收标准：状态更新后提醒列表同步变化。"
        )

        assert_user_stories_have_acceptance_criteria(response)

    def test_P0_004__scripted_user_stories_reject_non_goal_leakage(self):
        bad_response = (
            "用户故事 1：作为自由职业设计师，我想生成发票。\n"
            "验收标准：系统自动创建合同。"
        )

        with self.assertRaises(AssertionError):
            assert_user_stories_have_acceptance_criteria(bad_response)


if __name__ == "__main__":
    unittest.main()
