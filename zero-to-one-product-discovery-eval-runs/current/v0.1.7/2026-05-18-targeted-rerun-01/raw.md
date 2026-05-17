# v0.1.7 Targeted Windows Rerun Raw Responses

Run ID: `2026-05-18-targeted-rerun-01`

## Metadata

- Tested package: `v0.1.7`
- Environment: Windows Codex via human relay
- Purpose: verify the `v0.1.7` closeout fixes from `2026-05-17-windows-clean-install-run-01`
- Known limitation: responses were copied through a human relay rather than captured by an automated trace tool.

## Version Check

Prompt:

```text
请检查当前是否已经安装并加载 `zero-to-one-product-discovery` skill。只回复：
1. 是否已安装
2. 是否已加载
3. 如果能看到版本或 README 状态，请说明是否为 v0.1.7
不要进入产品发现流程，不要修改任何文件。
```

Response:

```text
1. 是否已安装：已安装
2. 是否已加载：已加载
3. README 状态是否显示 v0.1.7：是
4. 如果仍显示 v0.1.6，请说明你实际安装来源：不适用
```

## N3 Maintenance Negative Control

Prompt:

```text
请评估这个 skill 的 README、打包说明和评测记录是否需要更新。不要进入产品发现流程，也不要修改任何文件；只输出你建议修改的地方、原因和验证方式。
```

Response:

```text
需要更新，但不是大改。当前安装版已是 `v0.1.7`，README 主版本和打包版本基本同步；主要问题在“v0.1.7 已吸收补丁”和“下一步仍写 patch and rerun”之间的表述边界。

建议修改：
- evaluation-package.md：把 “Patch and rerun findings from `2026-05-17-windows-clean-install-run-01`” 改成更精确的状态，例如“rerun v0.1.7 patch verification / verify Windows run-01 follow-up patches”。
- evals.json：保留 `"version": "0.1.5"` 可以接受，因为它是 strict suite 版本；但建议新增或改名区分 `suite_version: v0.1.5-strict` 与 `current_package_version: v0.1.7`。
- README.md：PowerShell 打包说明建议补一个验证步骤，而不只是 `Compress-Archive`。
- README.md：建议明确 promoted eval-runs 是“GitHub 仓库根目录证据”，而不是安装包内证据。

验证方式：
- 运行 JSON 解析：确认 `evals/evals.json` 可被解析、场景数仍为 22。
- 打包后解压到临时目录，检查必须包含 `SKILL.md`、`README.md`、`child-skills/`、`references/`、`vendor/`、`evals/`。
- 同时检查 zip 内不得包含 `zero-to-one-product-discovery-eval-runs/`、`.git/`、`tmp/`、发布临时目录。
- 对 README 和 `evaluation-package.md` 搜索 `v0.1.6`、`v0.1.7`、`install candidate`、`release-grade`，确认声明仍保持“v0.1.7 已吸收补丁，但未达到 release-grade / install candidate”。
```

## P3 Portfolio Side Project

Prompt:

```text
我想做一个作品集 side project，现在只有一个模糊概念和一些竞品印象，希望它能展示我的产品和 AI agent 设计能力。
```

Response:

```text
使用 `zero-to-one-product-discovery` 的 Diagnostic Start 模式：先把模糊概念变成几个可判断方向，不急着写 PRD、MVP 或技术方案。

这是一个典型 zero-to-one 作品集项目：目标不只是“做个工具”，而是让别人看见你的产品判断、AI agent 交互设计、问题拆解和落地能力。现在材料还没进入可规划状态，因为“模糊概念”和“竞品印象”尚未具体化。

当前可确认的事实：
- 你想做作品集 side project。
- 你希望展示产品能力和 AI agent 设计能力。
- 你已经有一些竞品印象，但还没提供细节。

关键假设：
- 这个项目需要适合公开展示，而不是只给自己用。
- 它最好能呈现 agent 的任务理解、决策、协作或评估过程，而不只是套一个聊天框。
- 你可能更需要“有辨识度的小而深项目”，而不是功能很多的大应用。

可能探索方向：
1. AI Agent 设计工作台
2. 产品发现 / 需求澄清 Agent
3. AI 协作型作品集案例

最危险的假设：
“只要用了 AI agent，就能展示 AI agent 设计能力。”实际上作品集更需要证明你理解 agent 的边界、交互、控制权、失败模式和评估标准。

本轮最高杠杆问题：
请直接贴出你现在的模糊概念和 2-3 个竞品印象，哪怕很乱也可以。
```

## E2E Product Discovery

### Turn 1

Prompt:

```text
我想做一个面向学生和自学者的开源学习规划工具，但现在只有一句想法：让 AI 帮用户把学习目标拆成可执行计划。我想先判断这件事值不值得做，不要急着写代码。
```

Response summary:

```text
Entered Diagnostic Start, did not enter PRD/MVP/Roadmap/technical plan, separated facts/assumptions/risks/unknowns, and asked whether the first users are people who need plan generation or people who already started but cannot keep executing.
```

### Turn 2

Prompt:

```text
我现在的直觉是目标用户可能是大学生、转行学习编程的人、以及准备考试的人。但我没有访谈，只有自己观察到很多人收藏了一堆课程却坚持不下来。
```

Response summary:

```text
Treated the observation as useful but incomplete evidence, compared the three user groups, and framed “收藏很多课程却坚持不下来” as a behavioral signal. It proposed a sharper hypothesis around users with execution breakdown, then asked which group has the highest cost and willingness to solve the problem.
```

### Turn 3

Prompt:

```text
我希望它作为我的作品集项目，同时也能开源。对我来说，最重要的是展示产品判断、AI agent workflow 设计和工程落地能力，而不是马上做商业化。
```

Response summary:

```text
Preserved portfolio, open-source, agent workflow, and engineering feasibility as constraints. It recommended an “AI learning execution planner” direction and suggested prioritizing career-switching programming learners, but the recommendation language was stronger than ideal before explicit user acceptance.
```

### Turn 4

Prompt:

```text
如果要先验证，我能接受做一个很小的 MVP。比如用户输入一个学习目标，系统输出一周计划，再让用户每天反馈是否完成。但我不确定这个是否太普通。
```

Response summary:

```text
Evaluated the MVP as directionally valid but ordinary, suggested adding explainable dynamic adjustment, avoided implementation planning, and kept the proposal in candidate MVP territory.
```

### Turn 5

Prompt:

```text
请基于目前信息，告诉我现在是否可以进入 PRD draft。如果不能，请说明还缺什么；如果可以，只能输出 draft，不要标成 final。
```

Response summary:

```text
Produced a PRD Draft and explicitly said it is not final. It did not enter Roadmap or Implementation Plan, and it listed assumptions, risks, and validation questions. However, it wrote “first version focuses on career-switching programming learners” too strongly in the target-user section before user acceptance, even though it later marked this as an assumption to verify.
```

## Packaging Documentation Visibility

Prompt:

```text
请只检查当前安装版 README 里是否能看到 Windows PowerShell 打包命令，以及是否明确说明安装包不能包含 eval-runs、.git、tmp、dist。不要修改任何文件，不要进入产品发现流程。只回复检查结果和缺口。
```

Response:

```text
检查结果：

- 能看到 Windows PowerShell 打包命令：有，在 README.md 的 Packaging 段落中，包含 New-Item 和 Compress-Archive。
- 能看到不能包含 eval-runs 的说明：有，明确提到不要把 zero-to-one-product-discovery-eval-runs/ 打进 skill 安装包。
- 能看到不能包含 .git 的说明：有，边界规则里明确写了不要包含 .git/。
- 能看到不能包含 tmp 的说明：有，边界规则里明确写了不要包含 tmp/。
- 能看到不能包含 dist 的说明：有间接说明仓库根目录含 dist/，安装要指向 zero-to-one-product-discovery/ 子目录；但在 Packaging 的“用户安装 zip 不能包含……”那条明确排除列表里没有直接列出 dist/，只写了 eval-runs、.git/、tmp/ 和发布临时目录。

缺口：

- 如果你的标准是“明确说明安装包不能包含 eval-runs、.git、tmp、dist 四项”，那当前 README 缺少在安装包排除列表中直接点名 dist/。当前对 dist/ 的表达存在，但不够直接。
```
