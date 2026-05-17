# v0.1.6 Windows Clean-Install Test Packet

Use this packet on a separate Windows Codex environment after installing `zero-to-one-product-discovery`.

## Rules For The Windows Run

- Run each scenario in a fresh chat unless the section says it is a multi-turn scenario.
- Do not mention that this is a test unless the prompt itself says so.
- Copy the complete assistant response back to the relay operator.
- Do not summarize, translate, or clean up the assistant response.
- If Codex says the skill is unavailable, copy that response exactly.
- For negative-control maintenance scenarios, do not let the assistant edit the installed skill. If it proposes edits, stop and copy the proposal back. If it edits files anyway, record that as test-environment contamination and reset the installed skill before continuing.

## Install Target

Install from GitHub or from the v0.1.6 package:

```text
https://github.com/Conradgui/zero-to-one-product-discovery
dist/zero-to-one-product-discovery-skill-v0.1.6.zip
```

Restart Codex after installation before running the scenarios.

## Single-Turn Positive Trigger Scenarios

### P1 Early Open-Source Product Idea

```text
我有一个从零开始的开源产品想法，想先梳理问题和 MVP，不要急着写代码。
```

Expected high-level behavior: the skill should trigger and start a zero-to-one Diagnostic Start rather than jumping into implementation.

### P2 Existing PRD But Not Validated

```text
我已经有一份 PRD 草稿，但还没有验证目标用户、成功指标和 MVP 范围。请先帮我判断哪些部分还不够 grounded。
```

Expected high-level behavior: the skill should trigger, treat the PRD as existing material, and identify evidence gaps instead of treating the PRD as final.

### P3 Portfolio Side Project

```text
我想做一个作品集 side project，现在只有一个模糊概念和一些竞品印象，希望它能展示我的产品和 AI agent 设计能力。
```

Expected high-level behavior: the skill should trigger, preserve portfolio/public-credibility goals as constraints, and avoid premature Roadmap or Implementation Plan output.

## Single-Turn Negative Trigger Scenarios

### N1 Code Review

```text
请帮我 review 这段已经写好的代码，重点看 bug、可维护性和测试缺口。
```

Expected high-level behavior: the zero-to-one discovery skill should not run Diagnostic Start.

### N2 Existing MVP Small Change

```text
这个项目已经有 runnable MVP 了，现在只想修一个按钮样式和一个小 bug，不需要重新做产品发现。
```

Expected high-level behavior: the zero-to-one discovery skill should not trigger by default.

### N3 Skill Maintenance

```text
请评估这个 skill 的 README、打包说明和评测记录是否需要更新。不要进入产品发现流程，也不要修改任何文件；只输出你建议修改的地方、原因和验证方式。
```

Expected high-level behavior: the assistant should stay in skill-maintenance mode, not Diagnostic Start, and should not mutate the installed skill during clean-install validation.

### N4 Vendor Source-Governance Boundary

```text
vendor 里的 upstream skill 能不能直接调用？还是只能通过本地 child-skills adapter？
```

Expected high-level behavior: the assistant should explain that `vendor/` is a source snapshot library and local `child-skills/` adapters are the routeable surface. It should not ask PRD readiness or product-discovery follow-up questions.

## Multi-Turn End-To-End Scenario

Run this scenario in one continuous chat. Copy each assistant response back before sending the next user turn.

### E2E Turn 1

```text
我想做一个面向学生和自学者的开源学习规划工具，但现在只有一句想法：让 AI 帮用户把学习目标拆成可执行计划。我想先判断这件事值不值得做，不要急着写代码。
```

### E2E Turn 2

```text
我现在的直觉是目标用户可能是大学生、转行学习编程的人、以及准备考试的人。但我没有访谈，只有自己观察到很多人收藏了一堆课程却坚持不下来。
```

### E2E Turn 3

```text
我希望它作为我的作品集项目，同时也能开源。对我来说，最重要的是展示产品判断、AI agent workflow 设计和工程落地能力，而不是马上做商业化。
```

### E2E Turn 4

```text
如果要先验证，我能接受做一个很小的 MVP。比如用户输入一个学习目标，系统输出一周计划，再让用户每天反馈是否完成。但我不确定这个是否太普通。
```

### E2E Turn 5

```text
请基于目前信息，告诉我现在是否可以进入 PRD draft。如果不能，请说明还缺什么；如果可以，只能输出 draft，不要标成 final。
```

Expected high-level behavior: the assistant should preserve the question loop, separate evidence from assumptions, avoid final PRD, and block Roadmap / Implementation Plan until the PRD draft is grounded and accepted.
