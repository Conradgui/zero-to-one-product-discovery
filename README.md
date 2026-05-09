# Zero-to-One Product Discovery

面向早期产品想法的 AI workflow skill：从一句模糊想法开始，逐步完成问题澄清、材料吸收、MVP 假设、规划产物和实施准备。

它适合个人开源项目、作品集项目、内部工具、side project 和 startup MVP 的早期探索。核心目标不是“快速套一个 PRD 模板”，而是防止 AI 在证据不足时过早进入 PRD、Roadmap、ADR 或编码阶段。

> Status: `v0.1.0-draft`。当前是开发中版本，适合试用、评审和迭代；尚未声明 release-grade validation。

## Highlights

- **主控 workflow**：由 `SKILL.md` 控制阶段门禁、上下文连续性、子能力路由和最终输出验收。
- **中文优先体验**：默认面向中文产品探索和协作场景，同时保留英文 artifact 名称以兼容常见 PM / engineering 术语。
- **一轮一个关键问题**：每轮只问当前最高杠杆问题；用户回答后再更新 facts / assumptions / risks / gaps。
- **防止过早产物化**：信息不足时只能输出 outline、decision surface、evidence gap 或 blocking question，不能伪造成最终 PRD。
- **专业子能力**：PRD、Roadmap、User Stories、Acceptance Criteria、ADR、Mermaid、Implementation Plan 等由本地 child skill adapter 承担。
- **Copy-first 来源治理**：高质量上游 skill 被保存在 `vendor/` 作为来源快照，但不能直接绕过本地 workflow。

## When To Use

适合：

- 只有一个初步产品、工具、开源项目或 startup 想法。
- 已有笔记、PRD 草稿、用户反馈、竞品研究或路线图，但缺少系统化发现过程。
- 想先确认问题、用户场景、MVP、风险、非目标和成功标准，再进入开发。
- 想把探索过程沉淀成可复盘、可展示的产品发现记录。

不适合：

- 已明确需求的小功能实现。
- bug fix、局部 UI 调整、纯 code review。
- 已有成熟产品的增长、运营或迭代优化。
- 在没有 grounded context 的情况下直接生成最终 PRD、Roadmap 或 Implementation Plan。

## Install

### Option 1: Install From GitHub With Codex

仓库公开后，可以在 Codex 中使用 `$skill-installer` 直接安装：

```text
$skill-installer install https://github.com/Conradgui/zero-to-one-product-discovery
```

如果未来把这个 skill 放进某个 monorepo 的子目录，再使用 GitHub tree 路径：

```text
$skill-installer install https://github.com/<your-name>/<your-repo>/tree/main/zero-to-one-product-discovery
```

安装后重启 Codex，让 skill 被重新发现。

### Option 2: Manual Install For Codex

从当前 workspace 复制到 Codex 的个人 skill 目录：

```bash
mkdir -p ~/.codex/skills
cp -R zero-to-one-product-discovery ~/.codex/skills/zero-to-one-product-discovery
```

然后重启 Codex。

### Option 3: Manual Install For Other SKILL.md-Compatible Agents

如果你的 agent 支持 `SKILL.md` 目录格式，把整个 `zero-to-one-product-discovery/` 文件夹复制到对应的 skills 目录即可。常见目录形态包括：

```text
~/.codex/skills/zero-to-one-product-discovery
~/.claude/skills/zero-to-one-product-discovery
.codex/skills/zero-to-one-product-discovery
.claude/skills/zero-to-one-product-discovery
```

不同客户端的目录名和重启方式可能不同，以你的客户端文档为准。

## Usage

自然语言触发：

```text
我有一个从零开始的开源产品想法，想先梳理问题和 MVP，不要急着写代码。
```

显式触发：

```text
Use $zero-to-one-product-discovery as the main workflow to explore this early product idea.
```

一个典型协作节奏：

1. 用户提出初步想法。
2. skill 输出 Diagnostic Start：事实、假设、风险、未知、候选探索方向和当前最高杠杆问题。
3. 用户逐轮回答关键问题或提供材料。
4. skill 吸收材料并推进 Problem Framing、Solution Exploration、Feasibility Discovery 和 MVP Hypothesis。
5. 当前置条件满足后，主控 workflow 路由到 PRD、Roadmap、User Stories、ADR 或 Implementation Plan 子能力。

## Workflow

```text
Diagnostic Start
  -> Material Assimilation
  -> Problem Framing
  -> Solution Exploration
  -> Feasibility Discovery
  -> MVP Hypothesis
  -> Planning Artifacts
  -> Implementation Planning
```

阶段不是死板 checklist，而是防止 AI 跳步的 guardrail。显式要求“直接给完整 PRD”也不能绕过门禁；如果前置条件不足，输出必须降级。

## Repository Layout

```text
zero-to-one-product-discovery/
├── README.md                # GitHub 展示与安装说明
├── SKILL.md                 # 主控 workflow skill
├── agents/
│   └── openai.yaml          # Codex UI 元数据
├── child-skills/            # 本地子能力 adapter，只能由主控路由
├── references/              # 阶段规则、路由协议、来源治理和文档模板
├── vendor/                  # 上游 skill/source 快照和许可证，不可直接路由
└── evals/                   # 可复用评测场景、rubric 和测试协议
```

历史 raw responses、scored reports 和 handoff 记录不放入安装包；维护者可以在本地外部归档中保存它们，例如：

```text
zero-to-one-product-discovery-eval-runs/
```

## Child Skills

`child-skills/` 中的模块是本地 adapter，不是用户直接调用的独立流程。

| Child skill | Purpose |
|---|---|
| `research-brief` | 综合访谈、反馈、竞品、笔记，区分 evidence / assumption / contradiction / gap |
| `prd` | 在 grounded context 下输出 PRD；信息不足时只输出 PRD outline 和缺口 |
| `roadmap` | 生成 Now / Next / Later、阶段化路线图和验证门禁 |
| `user-stories` | 生成用户故事、故事地图和 release slice |
| `acceptance-criteria` | 为已确认需求或故事生成验收标准 |
| `adr-governance` | 判断 Decision Log vs ADR，处理长期技术决策 |
| `mermaid` | 基于已知结构生成 Mermaid 图 |
| `implementation-plan` | 从 review-ready planning artifacts 进入工程实施计划 |
| `review` | 从产品、UX、工程、测试和架构角度审查 artifact |
| `context-handoff` | 生成跨轮次或跨会话的 Context Resume Packet |

主控规则：

- child skill 不能自行跳阶段。
- child skill 不能调用其他 child skill。
- child skill 不能从 `vendor/` 直接执行上游 command。
- child skill 不能把假设包装成事实。
- 重要输出必须带 readiness signal 和 Context Resume Packet。

## Source Strategy

本项目采用 copy-first 策略：先把高质量上游项目的相关 skill/source snapshot 保存到 `vendor/`，再将其改写成本地 adapter contract。

主要参考来源：

- [Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills)：PM 深度、PRD、Roadmap、JTBD、故事地图。
- [pm-skills](https://github.com/product-on-purpose/pm-skills)：artifact skill 组织、PRD、ADR、Mermaid、用户故事、验收标准。
- [agent-skills](https://github.com/addyosmani/agent-skills)：工程治理、ADR、计划拆解、测试、review。
- [awesome-copilot](https://github.com/github/awesome-copilot)：生态索引和补充参考。

`vendor/` 是来源库，不是 route target。所有用户可感知行为必须经过 `child-skills/` 和主控 stage gate。

See also:

- `vendor/MANIFEST.md`
- `references/source-attribution.md`
- `references/source-evaluation.md`

## Evaluation

评测材料保存在 `evals/`：

- `evals/evals.json`：场景集、阈值和 hard failures。
- `evals/eval-rubric-template.md`：评分 rubric。
- `evals/claude-code-pressure-test-protocol.md`：两阶段 pressure test 协议。
- `evals/evaluation-package.md`：当前证据、限制和安全 claim。

当前可以谨慎声明：

- source-governance 与 command mini-hub boundary 有 passing rerun evidence。
- 第一批本地 wrapper 有 passing pressure evidence。
- copy-first vendor boundary 与 copied PRD adapter 有初步 passing evidence。

当前不能声明：

- release-grade validation。
- 全局安装后的自然触发可靠性。
- 完整多轮 workflow 质量。
- copy-first child adapter 相对旧 artifact adapter 的系统性 A/B 优势。

## Packaging

推荐发布包只包含：

```text
zero-to-one-product-discovery/
```

不要把本地外部归档打进 skill 安装包，例如：

```text
zero-to-one-product-discovery-eval-runs/
```

本地打包命令：

```bash
mkdir -p dist
zip -r dist/zero-to-one-product-discovery-skill.zip zero-to-one-product-discovery \
  -x '*/.DS_Store' \
  -x '*/__pycache__/*'
```

解压后应能看到：

```text
zero-to-one-product-discovery/SKILL.md
zero-to-one-product-discovery/README.md
zero-to-one-product-discovery/child-skills/
zero-to-one-product-discovery/references/
zero-to-one-product-discovery/vendor/
zero-to-one-product-discovery/evals/
```

## License And Attribution

This repository is intended for personal open-source / portfolio use while it is still in draft.

The `vendor/` directory contains copied upstream snapshots with mixed licenses, including CC BY-NC-SA 4.0, Apache-2.0, and MIT. Before publishing, redistributing, or reusing substantial upstream content, review:

- `vendor/MANIFEST.md`
- `references/source-attribution.md`
- upstream repository licenses

Local workflow and adapter text should remain clearly separated from verbatim upstream source snapshots.
