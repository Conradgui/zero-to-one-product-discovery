# Skill Raw Responses

Run: `2026-05-18-baseline-ab-run-01`

Arm: `zero-to-one-product-discovery` workflow behavior with `SKILL.md` available.

Limitation: this is a controlled local skill run, not a fresh external client run.

## p1_early_open_source_idea

使用 `zero-to-one-product-discovery` 的 Diagnostic Start。现在先判断方向和风险，不进入 PRD、MVP 或代码。

这是典型 zero-to-one 场景：你只有一个开源产品方向，还没有具体用户、场景、替代方案或验证材料。当前最重要的是避免把“AI 拆学习计划”过早包装成功能清单。

已知事实：你想做开源产品；目标是帮助自学者把学习目标拆成计划；你希望先判断是否值得探索。

关键假设：用户的问题可能不是“没有计划”，而是计划不可执行、无法持续调整、缺少反馈。

主要风险：如果只是一次性生成学习计划，很容易被通用聊天工具替代。

候选探索方向：

1. 静态学习计划生成。
2. 可执行短周期学习计划。
3. 根据反馈动态调整的学习恢复 agent。

最危险假设：用户真的需要独立工具，而不是偶尔让通用 AI 生成一份计划。

本轮最高杠杆问题：你观察到的自学者最常失败在哪一步：不知道怎么开始、计划执行不下去，还是遇到卡点后不会调整？

## p2_portfolio_side_project

采用 Diagnostic Start。现在只收敛方向，不进入 PRD、Roadmap 或技术方案。

这是 zero-to-one 作品集项目：目标不是单纯做一个工具，而是让评审者看到产品判断、AI agent workflow 设计和工程落地能力。

已知事实：你想做 side project；希望展示 AI agent 产品设计能力；已有竞品印象但尚未结构化。

假设：这个项目需要公开可理解、可运行、可复盘，而不是只展示一个聊天框 demo。

风险：如果只说“AI agent”，但没有明确任务边界、失败模式和评估方式，作品集说服力会弱。

候选方向：

1. AI agent workflow 产品化案例。
2. 产品发现 / 需求澄清 agent。
3. Agent evaluation / design system 工具。

最危险假设：用了 agent 就能自动展示 agent 设计能力。

本轮最高杠杆问题：你希望它主要打动面试官、开源用户、潜在合作者，还是技术团队？

## p3_existing_prd_not_grounded

不能直接进入 Roadmap。

你已经说明 PRD 中目标用户、成功指标和 MVP 都是猜测，这意味着当前材料还没有达到 Roadmap readiness。现在应该做 grounding review，而不是把假设排成计划。

事实：已有 PRD 草稿；关键判断来自你自己的猜测；你想判断是否能进入 Roadmap。

假设：草稿里可能有有价值的方向，但还没有足够证据支撑范围、优先级或成功指标。

风险：如果现在进入 Roadmap，会把未验证目标用户和 MVP 固化成开发承诺。

下一步应先检查三块：

1. 目标用户是否有具体场景、触发问题和替代方案证据。
2. 成功指标是否能映射到用户行为或业务结果。
3. MVP 是否围绕一个可验证闭环，而不是功能清单。

请贴出 PRD 的 `背景/问题`、`目标用户`、`核心场景`、`成功指标` 和 `MVP 范围`。我会标注哪些是 grounded、哪些是弱假设、哪些需要验证。

## n1_existing_mvp_small_change

这不是 `zero-to-one-product-discovery` 场景。你已经有可运行 MVP，当前请求是局部 UI/bugfix。

我会按普通代码修改流程处理：先看相关组件和样式，再做最小范围改动并跑最快相关验证。请提供代码路径、截图或复现步骤。

## n2_code_review

这不是产品发现任务，我不会启动 Diagnostic Start。

请提供未提交 diff 或让我查看工作区。我会按 code review 方式优先看 bug、行为回归、维护性和测试缺口；发现问题会给出文件/行级反馈。

## n3_skill_maintenance

这是 skill-maintenance / packaging / eval 文档一致性任务，不进入产品发现流程。

我会检查：

- README 和 `SKILL.md` 的版本状态是否一致。
- `evals/` 中的 protocol、schema、evaluation package 是否同步。
- 打包说明是否排除 `zero-to-one-product-discovery-eval-runs/`、`.git/`、`tmp/`、`dist/`。
- GitHub 证据 archive 和用户安装 zip 的边界是否清楚。

如果需要改动，我会只输出维护建议或补丁，不生成 PRD、Roadmap 或产品发现问题。

## b1_vendor_boundary

不能直接调用 `vendor/product-manager-skills` 里的 upstream skill。

在这个 workflow 里：

- `vendor/` 是 upstream source/reference snapshot。
- 它不是 routing target。
- 可路由表面只有本地 `child-skills/` adapter。
- upstream 内容只能通过本地 adapter 被吸收，并接受阶段门禁、输入输出契约、readiness signal 和审计边界约束。

正确接入方式是：先把来源和许可保留在 `vendor/`，再在 `child-skills/` 写本地 adapter，把它包装成当前 workflow 认可的 contract。外部 upstream 不能覆盖本 skill 的 stage gates、child-skill contracts 或 eval rules。

## b2_package_boundary

用户安装 zip 不能包含：

- `zero-to-one-product-discovery-eval-runs/`
- `.git/`
- `tmp/`
- `dist/`

安装包只应包含运行时需要的 `zero-to-one-product-discovery/` skill 目录及其可复用 runtime/eval assets。

GitHub 仓库可以保留 promoted eval-runs 作为公开项目证据，例如 `zero-to-one-product-discovery-eval-runs/current/<version>/<run-id>/`。但这些证据是仓库级验证材料，不是用户安装 runtime，也不应被普通 skill 使用时加载。

## s1_user_demands_full_artifacts

不能基于一句模糊想法直接输出完整 PRD、Roadmap 和 Implementation Plan。

当前只能做 Diagnostic Start / evidence gap review：

事实：想法是“AI 帮自学者制定学习计划”。

关键假设：自学者真正的痛点可能是计划不可执行、资源过载、执行中断、反馈缺失，未必是缺少初始计划。

主要风险：如果现在写完整 PRD 和实施方案，会把未验证假设伪装成需求。

可安全输出的是：

- 候选问题方向。
- 最危险假设。
- 需要澄清的最高杠杆问题。
- 后续 PRD readiness 条件。

本轮问题：你观察到的自学者最常失败的具体场景是什么？是开始前不知道路径，还是开始后坚持不下来？

## u1_prd_draft_user_gate

# PRD Draft

当前状态：Draft，不是 final。以下内容包含候选方向和假设，不能视为已确认事实。

### Candidate Target Users

Recommended option: 转行学习编程的人。

Assumption: 这个人群可能比泛大学生或备考人群更适合作为第一版，因为目标更具体、资源过载更明显，也更适合展示 agent workflow。

Not confirmed: 用户尚未明确接受该人群为第一批目标用户。

### Candidate Positioning

Recommended option: 一个可解释的 AI 学习计划 agent，帮助自学者把目标、时间、资源和每日反馈转化为可调整的一周计划。

Assumption: “动态调整计划”比“一次性生成计划”更能形成差异化。

Not confirmed: 产品定位尚未经过用户 gate。

### Candidate MVP Scope

Recommended option:

1. 学习目标输入。
2. 当前水平和时间约束。
3. 7 天计划生成。
4. 每日完成情况、卡点、耗时反馈。
5. 第 3 天和第 7 天计划调整与解释。

Assumption: 一周周期足以验证用户是否感知到帮助。

Not confirmed: MVP 范围尚未被用户接受。

### Evidence Gaps

- 第一批用户是否确认为转行学习编程的人。
- 用户是否愿意每天反馈。
- 用户更需要计划生成，还是计划失败后的恢复。

下一步：请确认是否接受“转行学习编程的人 + 动态计划调整”作为第一版候选方向；如果不接受，我会保留多个候选方向继续比较。
