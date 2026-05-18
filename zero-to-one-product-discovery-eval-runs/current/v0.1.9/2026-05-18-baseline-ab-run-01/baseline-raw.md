# Baseline Raw Responses

Run: `2026-05-18-baseline-ab-run-01`

Arm: ordinary assistant behavior without reading or invoking `zero-to-one-product-discovery`.

Limitation: this is a controlled local baseline generated in the same repo session, not an external clean-room model run.

## p1_early_open_source_idea

这个想法值得探索。自学者经常有目标但缺少执行路径，你可以先做一个 MVP：用户输入学习目标、当前水平和每天时间，系统输出一周学习计划，并每天提醒用户完成任务。建议先定义目标用户、核心功能、技术栈和 MVP。

下一步可以做：

- 目标用户：大学生、自学编程者、备考人群
- MVP：目标输入、一周计划、每日打卡、进度统计
- 技术栈：React + Node.js + LLM API

你可以先确认想做移动端还是 Web 端。

## p2_portfolio_side_project

如果你想展示 AI agent 产品设计能力，可以做一个 AI Agent 设计工作台。它可以包括任务拆解、工具调用、记忆管理、评估报告和可视化日志。这个项目适合作品集，因为能展示 agent 架构和产品体验。

建议 MVP：

1. 输入一个复杂任务。
2. Agent 自动拆解任务。
3. 调用多个工具或子 agent。
4. 生成最终报告。
5. 展示过程日志。

可以直接做原型和技术方案。

## p3_existing_prd_not_grounded

如果 PRD 里的目标用户、成功指标和 MVP 都是你自己猜的，那 grounded 程度还不够。建议先补充用户访谈、竞品分析和成功指标定义。

不过你可以先进入轻量 Roadmap，把后续验证工作排进去：

- Week 1: 完成用户访谈
- Week 2: 完成 MVP 原型
- Week 3: 找用户测试
- Week 4: 迭代 PRD

Roadmap 可以作为假设验证计划，不一定是最终开发计划。

## n1_existing_mvp_small_change

这不是从零到一问题，应该直接做局部实现。建议：

1. 找到登录按钮组件。
2. 把按钮颜色改成蓝色。
3. 检查移动端 spacing CSS。
4. 跑相关 UI 测试。

如果你贴代码，我可以帮你 review 或修改。

## n2_code_review

可以。请先提供 git diff 或相关文件。我会重点看 bug、维护性、测试缺口和潜在回归。建议运行：

```bash
git diff
git status --short
```

然后把输出贴出来。

## n3_skill_maintenance

这是 skill 文档和打包维护问题，不需要进入产品发现。建议检查 README、SKILL.md、evals/evaluation-package.md 和 dist 包名是否一致。

可以检查：

- README 版本号
- zip 文件版本号
- eval-runs 路径
- 安装说明是否指向正确目录

如果你希望，我可以继续梳理产品发现流程是否也需要同步更新。

## b1_vendor_boundary

一般不建议直接调用 vendor 里的 upstream skill。vendor 更适合作为参考或复制来源。正确方式是把有用内容封装成本地 adapter，再通过主 workflow 调用。

如果你已经确认这个 upstream skill 很成熟，也可以在早期先直接引用它作为子能力，再逐步改成本地 wrapper。

## b2_package_boundary

发布 zip 时不应该包含 `.git`、`tmp` 或临时目录。`zero-to-one-product-discovery-eval-runs` 如果很大，也不建议放进 zip，可以保留摘要或链接。

GitHub 仓库里可以保留 eval-runs 作为证据，但安装包最好只包含运行需要的 skill 文件。

`dist` 一般是发布产物目录，通常不要嵌套进 zip。

## s1_user_demands_full_artifacts

下面是一个简版完整方案。

PRD：AI Learning Planner 面向自学者，帮助用户输入学习目标并生成学习计划。核心功能包括目标输入、计划生成、每日打卡、进度提醒、复盘总结。

Roadmap：第一阶段做目标输入和计划生成；第二阶段做每日反馈；第三阶段做动态调整；第四阶段做可视化 dashboard。

Implementation Plan：使用 React + Express + SQLite。先创建项目结构，再实现用户输入表单、计划生成 API、任务列表和反馈记录。

## u1_prd_draft_user_gate

# PRD Draft

### Target Users

第一批用户是转行学习编程的人。他们目标明确、痛点强、资源过载明显，适合作为产品 MVP 的核心人群。

### Positioning

产品定位为一个面向转行编程自学者的 AI 学习计划恢复工具，帮助用户在计划偏离后重新调整节奏。

### MVP Scope

MVP 包括目标输入、当前水平、已有资源、一周计划生成、每日反馈、第 3 天调整、第 7 天复盘。

### Success Metrics

用户完成目标澄清、执行 3 天反馈，并认为调整后的计划更合理。
