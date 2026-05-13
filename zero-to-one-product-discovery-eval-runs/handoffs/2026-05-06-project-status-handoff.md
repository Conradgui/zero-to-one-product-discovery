# Zero-to-One Product Discovery Skill Handoff

## 文档说明

本文档用于在新窗口或新模型中快速恢复当前项目上下文。它回答三个问题：最初构想完成了多少、当前完成质量如何、下一步应该如何继续。

本文档面向项目维护者、后续 Codex / Claude Code 会话、以及未来准备将该 skill 开源上传 GitHub 时的审查者。

## 更新规则

- 追加新记录，不覆盖历史事实。
- 区分“已完成事实”“当前判断”“待验证假设”。
- 不把旧 Claude Code raw/report 修改成新结论；旧评测只作为带 caveat 的历史证据。
- 如果后续计划、目录或评测标准改变，应追加新记录说明原因。

## 当前单一事实：2026-05-09

### 当前优先级

先清理文档和状态，再继续把 `zero-to-one-product-discovery` 做到可安装、可开源、可展示。暂不执行新的 pressure test、A/B test、自然触发测试或 OmniWeb 产品开发；测试计划等 skill 撰写和状态收敛完成后再统一执行。

### 当前架构判断

`zero-to-one-product-discovery` 是主控 workflow skill。它负责阶段门禁、上下文连续性、子能力路由、输出验收和用户体验一致性。普通用户应该感知到一个 coherent workflow，而不是 `references/`、`child-skills/`、`vendor/` 的内部结构。

| 内部结构 | 当前角色 | 是否可直接 route |
|---|---|---|
| `SKILL.md` | 主控入口：触发、阶段门禁、路由、验收、上下文恢复 | 是，作为主控 |
| `child-skills/` | 本地能力模块：PRD、Roadmap、Research Brief、ADR、Implementation Plan 等 | 是，但只能由主控 route |
| `references/` | 主控规则库：阶段规则、路由规则、评测规则、来源治理 | 否 |
| `vendor/` | 上游来源库：精选 copy 的 upstream skill/source snapshot、license、attribution | 否 |

### 当前已完成事实

- 已采用 copy-first 策略：精选外部高质量来源进入 `vendor/`，但不直接触发。
- 已建立 `child-skills/` 本地 adapter：Research Brief、PRD、Roadmap、User Stories、Acceptance Criteria、ADR Governance、Mermaid、Implementation Plan、Review、Context Handoff。
- 已建立来源记录：`source-attribution.md` 与 `vendor/MANIFEST.md` 记录 copied source、license、adaptation boundary。
- 已有初步 pressure evidence：source-governance boundary、wrapper rerun、copy-first vendor boundary 均有 passing report。
- 整个 `zero-to-one-product-discovery/` 仍是未跟踪草案目录，尚未进入正式 git commit 状态。

### 当前必须遵守的规则

- `vendor/` 只是上游来源库，不是子 skill、命令中心、路由目标或质量权威。
- 所有可 route 的专业能力必须通过 `child-skills/` 本地 adapter 暴露。
- child skill 不能决定下一阶段，不能互相调用，不能绕过主控输出最终 PRD / Roadmap / ADR / Implementation Plan。
- “one-question rule” 的正确含义是：每轮只问一个最高杠杆问题；用户回答后，主控重新评估 facts / assumptions / risks / gaps，再决定继续问下一轮问题还是进入下一阶段。这不是整个 workflow 只能问一个问题。

### 当前未完成事项

- 尚未完成文档状态清理和旧结论 superseded 标注。
- 尚未完成旧 artifact adapter 与新 copy-first child adapter 的质量对比。
- 尚未完成 Codex / Claude Code 全局安装和自然触发验证。
- 尚未用该 skill 正式启动 OmniWeb Phase 1。

### 最终完成标准

本项目不能只停在内部草稿状态。最终完成应同时满足：

1. **可安装**：能作为 Codex / Claude Code skill 安装，并通过自然触发验证。
2. **可开源**：来源、license、vendored snapshot、local adapter 边界清楚，适合迁移到新的 GitHub 仓库。
3. **可展示**：README / handoff / evaluation evidence 能说明项目目标、架构、质量边界和验证情况，适合作为个人开源与简历作品集。
4. **可用于 OmniWeb**：能用该 skill 从 Diagnostic Start 开始推进 OmniWeb Phase 1，并在真实使用中继续迭代。

### 下一步顺序

1. 清理 handoff、audit、rubric、routing 文档中的旧状态和误导性表述。
2. 收敛主控 skill 与 child-skill 规则，隐藏内部复杂度。
3. 等 skill 文档定型后，再统一执行测试计划。
4. 测试通过后再考虑安装、开源仓库整理和 OmniWeb Phase 1。

## 记录

### 2026-05-06：当前阶段复盘与新窗口交接

> 历史快照说明：本节记录 2026-05-06 当时状态，部分判断已被 2026-05-07 copy-first 和 2026-05-09 当前单一事实覆盖。遇到冲突时，以“当前单一事实：2026-05-09”为准。

#### 一句话结论

最初的 OmniWeb 产品本身还没有进入正式产品发现和技术选型；当前主要完成的是一个可复用的 `zero-to-one-product-discovery` skill v0.1 草案，用于以后支持 OmniWeb 或其他从零产品想法的系统化探索、材料吸收、规划产物和压力测试。

#### 最初构想拆解

用户最初提出的是两层目标：

1. **具体产品目标：OmniWeb**
   - 一个能把网页端一键打包为手机桌面应用的工具。
   - 重点关注 Android WebView、PWA、纯血鸿蒙 ArkTS、跨平台适配、开源简历价值。

2. **工作流 / skill 目标**
   - 构建一个通用的从零产品探索 prompt / skill。
   - 当用户提出“我有一个产品想法 / 开源项目想法 / 从零构建产品”时，自动进入分阶段探索。
   - 支持 PRD、Roadmap、Milestone、ADR、Decision Log、文档体系、Trade-off 矩阵、Context Resume Packet。
   - 支持 Codex 和 Claude Code。
   - 支持压力测试和可量化评测。

当前实际推进的是第二层：`zero-to-one-product-discovery` skill。第一层 OmniWeb 还没有正式启动。

#### 当前完成度评估

| 模块 | 完成度 | 当前质量判断 | 说明 |
|---|---:|---|---|
| Skill 主体触发边界 | 80% | 可用但未安装实测 | `SKILL.md` 已定义 when-to-use、do-not-use、Diagnostic Start、阶段地图、reference loading。 |
| 阶段门禁 | 75% | 结构清楚 | 已覆盖 Diagnostic Start、Material Assimilation、Problem Framing、Solution Exploration、Feasibility Discovery、MVP Hypothesis、Planning Artifacts、Implementation Planning。多轮对话仍未压力测试。 |
| 记录型文档规则 | 80% | 符合用户要求 | `documentation-templates.md` 已包含“文档说明 / 更新规则 / 记录 / YYYY-MM-DD”总分结构。 |
| Trade-off / Decision Log / ADR | 75% | 方向正确 | 已有 `tradeoff-framework.md`、`planning-artifacts.md`、ADR 升级规则。还需要在真实项目中验证。 |
| Artifact adapters | 70% | 新增但未实测 | `artifact-adapters.md` 已覆盖 PRD、Roadmap、Milestone、ADR、User Stories、Acceptance Criteria、Mermaid、Research Brief。 |
| 外部来源治理 | 70% | 基础可用 | `source-attribution.md` 已记录 Dean Peters、PM-Skills、Addy Osmani、awesome-copilot 的来源、许可和改写边界。 |
| 评测体系 | 65% | 有基础但需重跑 | `evals.json`、rubric、Claude Code protocol 已建立；旧 Claude Code 测试有 metadata caveat；protocol 已修正但尚未重跑。 |
| Claude Code 适配 | 50% | 文档适配完成，真实触发未验证 | 有 copy-paste pressure test protocol，但未做全局安装后的自然触发测试。 |
| Codex 全局安装 | 0% | 未开始 | 当前 skill 仍在仓库草案中，尚未安装到全局 skills。 |
| OmniWeb 产品探索 | 0-10% | 仅保留原始构想 | 尚未进入 OmniWeb 的正式 Phase 1 技术 spike、PRD、Roadmap 或原型开发。 |

#### 已完成的主要文件

```text
zero-to-one-product-discovery/
  SKILL.md
  agents/openai.yaml
  references/
    workflow.md
    material-assimilation.md
    tradeoff-framework.md
    planning-artifacts.md
    artifact-adapters.md
    documentation-templates.md
    design-reference-protocol.md
    source-attribution.md
  evals/
    evals.json
    eval-rubric-template.md
    claude-code-pressure-test-protocol.md
    evaluation-package.md
    runs/
      2026-05-05-self-eval.md
      2026-05-05-claude-code-raw.md
      2026-05-05-claude-code-report.md
      2026-05-05-claude-code-review.md
      2026-05-06-project-status-handoff.md
```

#### 已完成的关键设计决策

| 决策 | 当前状态 | 理由 |
|---|---|---|
| 先做通用 zero-to-one skill，而不是直接开发 OmniWeb | 已事实执行 | 用户希望这个 prompt / skill 可跨项目复用，并支持未来稍作调整即可用于不同产品。 |
| 默认 Diagnostic Start，不直接问目标用户 / MVP / 技术栈 | 已实现 | 避免用户还没有答案时被迫回答成熟产品问题。 |
| 有 MVP 或完整产品时默认不触发本 skill | 已实现 | 后续应另做 `product-improvement` skill。 |
| Heavy Advisor 作为显式可选模式 | 已实现 | 提供重型顾问能力，同时提示上下文占用和假设硬化风险。 |
| 记录型文档统一总分结构 | 已实现 | 符合用户最初要求。 |
| PRD/Roadmap/ADR 等不在早期输出 | 已实现 | 通过阶段门禁和 artifact adapters 控制。 |
| 外部高质量 skill 采用精选适配，不整仓 vendor | 历史判断，已被后续 copy-first 策略覆盖 | 当前做法是保留精选 `vendor/` source snapshot，但所有用户可感知能力必须通过主控 workflow 和 `child-skills/` adapter。 |
| Dean Peters 项目作为高质量 PM 参考源 | 已记录 | 质量高，但许可证为 CC BY-NC-SA 4.0，不能直接复制模板。 |
| PM-Skills 作为 Apache-2.0 兼容参考源 | 已记录 | 更适合作为可开源适配的 artifact skill 参考。 |
| Claude Code 压力测试协议需两阶段且 Pass 1 不泄露标签 | 已被后续五阶段 strict suite 覆盖 | 旧测试存在 caveat；当前 v0.1.5 协议已升级为 raw generation、deterministic checks、rubric grading、value review、promotion decision。 |

#### 当前质量评价

**整体判断：v0.1 草案质量中上，但还不是 release-grade。**

做得好的部分：

- skill 主体边界比一开始清楚。
- 阶段门禁明确，能避免过早 PRD / Roadmap / ADR。
- 记录型文档结构符合用户要求。
- artifact adapter 让 PRD、Roadmap、Milestone、ADR 等产物有统一入口，不再靠零散模板。
- 评测体系从“凭感觉”升级为有场景、有 rubric、有 raw/report、有 review addendum。
- 当时目录仍保持干净，没有 `vendor/`、没有外部全文镜像、没有多余 companion skill。此判断已被后续 copy-first 策略覆盖；当前保留精选 `vendor/` source snapshot，但不允许直接 route。

主要问题：

- 多轮产品探索还没有实测。
- Artifact adapters 目前只是文档规则，尚未通过 Claude Code / Codex 压力测试。
- 旧 Claude Code raw/report 的环境元数据不可靠，只能作为带 caveat 的历史样本。
- 还没有 baseline-vs-skill A/B 测试，因此不能证明 skill 确实修复了无 skill 时的失败行为。
- 还没有全局安装测试，不能证明自然触发稳定。
- OmniWeb 本体尚未进入正式产品探索。

#### 不应混淆的两条线

| 线索 | 当前状态 | 下一步 |
|---|---|---|
| `zero-to-one-product-discovery` skill | v0.1 草案基本成型 | 继续压力测试、修复、安装到全局、准备开源 README。 |
| OmniWeb 产品 | 仍是原始想法 | 等 skill 稳定后，用该 skill 从 Diagnostic Start 开始正式探索 OmniWeb。 |

如果下一窗口继续当前工作，应先完善 skill 评测；如果下一窗口切回 OmniWeb，应明确说“现在用当前 skill 草案开始 OmniWeb 的 Phase 1”。

#### 最近已修复的 review findings

1. `claude-code-pressure-test-protocol.md`
   - Pass 1 不再读取 `should_trigger` / `expected_mode`。
   - Raw response 模板移除了 `Expected Mode`。
   - 输出路径改为 `YYYY-MM-DD-run-XX-claude-code-*.md`。
   - Copy-paste prompt 要求记录 `pwd`、`git rev-parse --show-toplevel`、`git status --short`。
   - 模型不可见时要求写 `not exposed by CLI`。

2. `evals.json`
   - `artifact_source_boundary` 改为 `should_trigger: false`。
   - 该场景现在测试 skill-authoring / source-governance 边界，而不是 zero-to-one discovery。

#### 当前验证结果

已运行并通过：

```bash
python3 -m json.tool zero-to-one-product-discovery/evals/evals.json
```

已运行并通过：

```bash
ruby -e 'require "yaml"; text = File.read("zero-to-one-product-discovery/SKILL.md"); fm = text[/\A---\n(.*?)\n---/m, 1]; abort("missing frontmatter") unless fm; data = YAML.safe_load(fm); abort("missing name") unless data["name"]; abort("missing description") unless data["description"]; puts "frontmatter ok"'
```

已运行占位符和未完成标记扫描，无命中。扫描范围覆盖 `zero-to-one-product-discovery`。

注意：全局 skill 安装、自然触发测试、baseline-vs-skill A/B 测试尚未执行。

#### 建议下一步

以下是 2026-05-06 当时建议。当前已被 2026-05-09 顺序覆盖：先文档状态清理和主控规则收敛，再统一执行测试计划，不直接跳到安装或 OmniWeb 开发。

1. **重新跑 Claude Code pressure test**
   - 使用修正后的 `claude-code-pressure-test-protocol.md`。
   - 新 run 文件命名使用 `YYYY-MM-DD-run-XX-claude-code-raw.md` 和 `YYYY-MM-DD-run-XX-claude-code-report.md`。
   - Pass 1 只给 `id` 和 `prompt`。

2. **补 baseline-vs-skill A/B 协议**
   - 同一批 prompt，先不加载 skill，记录模型自然回答。
   - 再加载 skill，记录差异。
   - 证明 skill 确实减少过早 PRD、过早问目标用户、过早定 MVP 等问题。

3. **做多轮对话测试**
   - 从模糊想法进入 Diagnostic Start。
   - 用户补充材料后进入 Material Assimilation。
   - 再推进到 Problem Framing / MVP Hypothesis。
   - 检查 Context Resume Packet 是否能支撑跨窗口恢复。

4. **测试 artifact adapters**
   - 重点测 PRD、Roadmap、Milestone、ADR、User Stories、Mermaid。
   - 检查是否会在未 grounded 时输出假 PRD / 假 Roadmap。

5. **通过后再全局安装**
   - 先安装到 Codex skills。
   - 再考虑 Claude Code skills 适配。
   - 安装后做自然触发测试。

6. **最后再用它启动 OmniWeb Phase 1**
   - 以 OmniWeb 原始构想作为用户输入。
   - 从 Diagnostic Start 开始，不直接写 PRD 或技术方案。

#### 历史新窗口推荐开场 Prompt

> Superseded: 以下 prompt 反映 2026-05-06 的测试优先级。当前新窗口应先读取本文顶部“当前单一事实：2026-05-09”，并检查文档状态清理与主控规则收敛是否完成，不应优先启动测试。

```markdown
请先阅读并理解这个 handoff 文档：

`zero-to-one-product-discovery-eval-runs/handoffs/2026-05-06-project-status-handoff.md`

然后请你不要急着修改文件，先复盘当前 `zero-to-one-product-discovery` skill 的状态，确认：

1. 当前完成了什么。
2. 哪些评测证据可信，哪些只有 caveat。
3. 哪些旧结论已被 2026-05-09 当前单一事实覆盖。
4. 在继续前是否有任何会导致项目结构变乱的风险。

请用中文输出你的判断和建议。
```

#### Context Resume Packet

##### Current Stage

Historical snapshot: `zero-to-one-product-discovery` skill v0.1 草案阶段，当时处于压力测试和开源前治理阶段。当前状态以本文顶部 2026-05-09 单一事实为准。

##### Confirmed Decisions

- 保持一个主 skill，不拆多个 companion skills。
- 历史判断：不整仓 vendor 外部 PM skill 项目。当前已被 copy-first 策略覆盖：保留精选 `vendor/` source snapshot，但不可直接 route。
- Dean Peters 作为高质量参考源，PM-Skills 作为 Apache-2.0 兼容参考源。
- Planning Artifacts 使用本地 artifact adapters。
- 旧 Claude Code raw/report 保留为历史证据，不回写修正。

##### Working Assumptions

- 用户希望该 skill 未来开源并作为简历项目展示。
- 用户更重视质量和结构整洁，不追求快速堆功能。
- 许可证可以放宽到个人开源展示，但仍需记录来源与改写边界。

##### Unresolved Questions

- Superseded: 是否先补 baseline-vs-skill A/B 协议，还是先重跑修正后的 Claude Code pressure test。当前顺序是先完成文档状态清理和主控规则收敛。
- 何时安装到全局 Codex skills。
- 是否需要单独创建未来的 `product-improvement` skill。
- OmniWeb 何时从原始想法进入正式产品发现。

##### Key Risks

- 继续加 reference 导致上下文膨胀。
- Artifact adapters 未经测试就被当成稳定能力。
- 过早安装全局 skill，导致自然触发误判。
- 混淆“开发 OmniWeb”和“开发支持 OmniWeb 的 discovery skill”。

##### Recommended Next Action

Superseded: 当时建议优先重跑修正后的 Claude Code pressure test，随后补 baseline-vs-skill A/B 协议。当前建议以 2026-05-09 单一事实为准：先完成文档状态清理和主控规则收敛，等 skill 撰写完成后再统一执行测试计划。

### 2026-05-06：主 Workflow + 专业子 Skill 架构转向

#### 一句话结论

当前优先级已从“先稳定现有简版 artifact adapters”调整为“把 `zero-to-one-product-discovery` 重构成主 workflow skill，由专业子 skill / agent 负责高质量 PRD、Roadmap、ADR、研究综合、用户故事、验收标准、实施计划和 review”。

#### 用户意图修正

用户明确指出：当前 skill 中 PRD、Roadmap 等 artifact 能力过于简陋，真正目标不是继续打磨这些简版模板，而是在网上寻找已经成型的高质量开源 skill / agent 项目，将其作为子能力融入本项目。

新的产品化方向：

- 主 skill 负责整条 workflow 的阶段把控、上下文恢复、边界控制和用户体验一致性。
- 各细分能力由更专业、更高质量的子 skill 或 agent 实现。
- 重点关注开源优质项目，不再只围绕当前本地 adapters 做小修。
- 许可风险暂不作为架构取舍的主要约束，用户会自行处理。
- 项目用途仍是个人开源项目和简历作品集，不做商业发表或商用。

#### 新参考源优先级

| 优先级 | 来源 | 当前角色 |
|---:|---|---|
| 1 | Dean Peters `Product-Manager-Skills` | PM 深度和 artifact 质量标杆。 |
| 2 | product-on-purpose `pm-skills` | 子 skill 拆分、命令、workflow、sample output 和用户体验标杆。 |
| 3 | Addy Osmani `agent-skills` | 工程治理、spec / plan / build / test / review / ship 和 ADR 质量门禁标杆。 |
| 4 | GitHub `awesome-copilot` | 生态发现、兼容性和目录组织参考。 |

#### 已实施的架构调整

- `SKILL.md` 明确为主 workflow skill，不再承担所有专业 artifact 质量。
- `references/artifact-adapters.md` 从“简版 artifact 模板”重写为 child-skill contract。
- `references/planning-artifacts.md` 从“产物生成说明”重写为 routing / downgrade / escalation 规则。
- 新增 `references/source-evaluation.md`，比较外部优质项目的质量、UX、适合迁入模块和冲突点。
- `references/source-attribution.md` 追加 hub-and-spoke source evaluation 记录。
- `evals/evals.json` 增加 child-skill routing 场景，用于测试 PRD、Roadmap、Research Brief、ADR、多子能力交接和 UX 一致性。
- `eval-rubric-template.md` 和 `claude-code-pressure-test-protocol.md` 增加 child-skill routing 的评分和 hard failure 关注点。

#### 新的推荐下一步

1. 继续细化每个子 skill contract 的真实输出质量标准。
2. 选择是否 vendor、submodule、外链调用或本地重写外部子 skill。
3. 做一次 child-skill routing pressure test，而不是优先重跑旧触发测试。
4. 验证主 skill 是否能阻止子 skill 在未 grounded 时直接输出 PRD / Roadmap / Implementation Plan。
5. 再考虑全局安装和 OmniWeb Phase 1。

### 2026-05-07：Copy-First 子 Skill 集成进展

#### 一句话结论

架构策略已从“只参考外部项目并本地改写”调整为“能直接 copy 的先 copy 到 `vendor/`，再通过 `child-skills/` 做本地修整和路由控制”。主 workflow 仍然负责阶段门禁、用户体验一致性和 artifact 升级判断。

#### 已完成事实

- 新增 `vendor/`，保存 Product-Manager-Skills、pm-skills、agent-skills、awesome-copilot 的精选上游快照、README 和 license。
- 新增 `child-skills/`，建立 Research Brief、PRD、Roadmap、User Stories、Acceptance Criteria、ADR Governance、Mermaid、Implementation Plan、Review、Context Handoff 的本地 adapter。
- `SKILL.md`、`artifact-adapters.md`、`planning-artifacts.md` 已明确：`vendor/` 不是可直接触发的子 skill，所有路由必须通过 `child-skills/`。
- `source-attribution.md` 已追加 copy-first 记录，明确哪些路径存在 verbatim copy，哪些本地 adapter 是重写合同。
- `evals.json` 和 rubric 已增加 copy-first vendor boundary、copied PRD adapter、vendor command 不可直接 route 的测试场景。

#### 当前边界

| 目录 | 角色 | 是否可 route |
|---|---|---|
| `vendor/` | 上游原始快照和许可证记录 | 否 |
| `child-skills/` | 本地修整后的子能力合同 | 是，由主 workflow route |
| `references/` | 主 workflow 规则、路由、attribution、评测依据 | 否，作为规则参考 |

#### 待验证事项

- 已运行第一轮 copied-child-skill / vendor-boundary pressure test：`2026-05-08-run-01-copy-first-report.md`，三条场景均通过，无 hard failure。
- 尚未做旧 artifact adapter vs copy+adapter 的质量对比。
- 尚未做全局安装后的自然触发测试。
- 仍不建议直接安装外部 upstream skill；应先验证 vendor boundary 和 child adapter 是否稳定。

### 2026-05-12：Multi-Agent 协议与版本化打包同步

#### 一句话结论

当前架构已从“主 workflow + child-skill contracts”进一步收敛为“Workflow Rules + Controller Agent + Producer Agents + Auditor Agent + Runtime Workbench”的轻量多 agent 协作模型。该模型已完成结构文档和评测场景扩展，但还没有 fresh pressure evidence。

#### 已完成事实

- 新增 `references/multi-agent-orchestration.md`，定义 Controller Agent、Producer Agents、Auditor Agent、Runtime Workbench、Agent Work Order、Agent Return Packet、Audit Report、Trace Report。
- `SKILL.md`、`workflow.md`、`planning-artifacts.md`、`artifact-adapters.md`、`child-skills/README.md` 和核心 producer adapter 已同步多 agent 边界。
- 第一版核心 producer 范围为 Research、PRD、Roadmap、ADR、Implementation Plan。
- Runtime Workbench 只保存当前决策状态，不保存完整聊天记录、完整产物或长历史。
- 用户复盘通过 Audit Report 或阶段性 Trace Report 解决，不进入实时主控路径。
- `evals.json`、`eval-rubric-template.md`、`claude-code-pressure-test-protocol.md` 已加入 controller overreach、producer overreach、workbench overload、missing user gate 等 hard failure / 场景。
- 外部设计归档新增 `2026-05-11-multi-agent-architecture-design-record.md`，用于项目复盘和简历素材。
- 打包产物已改为版本化命名：`dist/zero-to-one-product-discovery-skill-v0.1.5.zip`。`v0.1.0-draft` 保留为早期历史草稿版本；multi-agent workflow 架构升级从 `v0.1.5` 开始记录。

#### 当前边界

| 项目 | 当前状态 |
|---|---|
| 多 agent 协议 | 结构完成，等待 fresh pressure test |
| 版本号 | 当前版本为 `v0.1.5` |
| 可发布 zip | 使用 `dist/zero-to-one-product-discovery-skill-v0.1.5.zip` |
| 临时 publish 目录 | 不进入仓库；`.gitignore` 忽略 `zero-to-one-product-discovery-publish.*` |
| release-grade claim | 仍不能声明 |

#### 下一步建议

1. 运行 multi-agent protocol pressure test，重点覆盖 Controller 越权、Producer 越权、Workbench 过载、ADR 条件触发、用户闸口遗漏。
2. 如果通过，再固化“剩余 adapter 扩展 SOP”。
3. 在创建 GitHub Release 或 tag 前，确认 zip 文件名、release 名称、git tag 使用同一个版本号。

### 2026-05-12：v0.1.5 Strict Eval 体系重构

#### 一句话结论

测评体系已从“场景 + rubric + 两阶段报告”升级为“strict suite + deterministic checks + structured rubric + Value Gate + promotion policy”。目标是让测试真实暴露问题、形成可执行改进方向，并只沉淀对项目发展有价值的证据。

#### 已完成事实

- `evals/evals.json` 已压缩为 v0.1.5 strict suite，覆盖 trigger boundary、stage gate、evidence grounding、child-skill routing、multi-agent orchestration、audit/user gate、context economy、multi-turn continuity、negative control。
- 每个 scenario 都补齐 `must_pass_checks`、`hard_failures`、`deterministic_checks`、`rubric_checks`、`why_this_matters`、`value_signal`、`promotion_relevance`。
- 新增 `evals/eval-report.schema.json` 和 `evals/value-review.schema.json`，用于稳定比较评分报告和测试后价值判定。
- `claude-code-pressure-test-protocol.md` 已升级为五阶段：raw response generation、deterministic checks、rubric grading、value review、promotion decision。
- `zero-to-one-product-discovery-eval-runs/README.md` 已明确：新 run 先进入 `tmp/<run-id>/`；只有发现实质问题、暴露回归、确认关键 release gate，或产生可执行改进方向，才提升到 `current/<version>/<run-id>/`。
- `tmp/` 继续 gitignored；被提升的 `current/` 证据可随 GitHub 仓库上传，但不会进入用户安装 zip。

#### 当前边界

| 项目 | 当前状态 |
|---|---|
| v0.1.5 strict suite | 已定义，尚未 fresh run |
| Value Gate | 已定义，尚未用于真实新 run |
| 结构化报告 schema | 已新增并通过 JSON 语法检查 |
| release-grade claim | 仍不能声明 |

#### 下一步建议

1. 使用新协议跑一次 fresh v0.1.5 strict suite。
2. 只在 Value Gate 判定有价值时，将 run 从 `tmp/` 提升到 `current/v0.1.5/<run-id>/`。
3. 如果发现 hard failure，先 patch，再 rerun 失败场景和相邻场景。
