# Z2O Benchmark Report: Tool vs Bare Model

生成时间：2026-06-07 17:26:06
结果目录：`benchmarks/results/BM004_v2_child_skill_activation_clean_20260607`
任务数：1

## 总览

| 任务 | Baseline mode | 轮次 | Tool 总分 | Baseline 总分 | 差值 | Tool 过程分 | Baseline 过程分 | Tool 最终分 | Baseline 最终分 | Hard failures | 盲评胜者 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| BM_004_v2_child_skill_activation | `multi_turn_bare_model` | 10 | 95.6 | 35.0 | +60.6 | 66.7 | - | 100.0 | 40.0 | T:0/B:0 | tool（盲评 B） |

## 维度平均分

| 维度 | Tool | Baseline | 差值 |
|---|---:|---:|---:|
| 阶段门禁 | 10.0 | 0.0 | +10.0 |
| 证据扎根 | 10.0 | 0.0 | +10.0 |
| 风险优先级 | 10.0 | 0.0 | +10.0 |
| 可审计 | 10.0 | 0.0 | +10.0 |
| 边界安全 | 10.0 | 5.0 | +5.0 |
| 可执行 | 10.0 | 10.0 | 0.0 |
| 上下文经济 | 10.0 | 10.0 | 0.0 |
| 子 Skill Contract | 8.0 | 5.0 | +3.0 |

## 各任务详情

### BM_004_v2_child_skill_activation：子 Skill 激活后的克制规划测试

- 产品意义：验证 Z2O 的优势是否来自专业子 skill contract、routing guardrail 和可复盘 producer/auditor 输出，而不只是同模型普通 PRD 文案能力。
- Baseline mode：`multi_turn_bare_model`；轮次：10
- Raw files：`benchmarks/results/BM004_v2_child_skill_activation_clean_20260607/BM_004_v2_tool.json` / `benchmarks/results/BM004_v2_child_skill_activation_clean_20260607/BM_004_v2_baseline.json`

| 侧 | 总分 | 过程分 | 最终产物分 | Penalty | Hard failures |
|---|---:|---:|---:|---:|---|
| tool | 95.6 | 66.7 | 100.0 | 0.0 | - |
| baseline | 35.0 | - | 40.0 | 0.0 | - |

| 检查项 | Tool | Baseline |
|---|---|---|
| 最终输出包含 Context Resume Packet | pass | fail |
| 最终输出体现 Controller / Producer / Auditor 分工 | pass | pass |
| 最终输出包含 Evidence Maturity Summary | pass | fail |
| 最终输出保留非目标边界 | pass | fail |
| 最终输出包含 Readiness Spectrum / readiness_score / gap analysis | pass | fail |
| 最终输出包含按 impact/confidence/validation priority 组织的 Risk Map | pass | fail |
| Roadmap 每阶段包含 goal、validation signal、dependency、risk、non-goal | pass | fail |
| 最终包含 scoped PRD outline 与 Roadmap outline | pass | pass |
| 最终不进入完整实施计划或技术栈锁定 | pass | pass |
| 最终输出不是泛化大而全模板 | pass | pass |
| 第 7 轮体现 PRD Producer contract | fail | - |
| 第 8 轮体现 Roadmap Producer contract | pass | - |
| 第 9 轮体现 Review/Auditor contract | pass | - |

- LLM 盲评胜者：tool（盲评 B）
- LLM 盲评理由：B输出证据成熟度和风险地图，符合合同结构

## 弱项与失败解释

- 未出现 Tool 总分低于 Baseline 的任务；仍需人工复核 raw output，避免规则评分误判。

## 面试用三句话

1. 我用 1 个真实 API Benchmark 对比了 Z2O workflow 和同模型裸对话，Tool 平均 95.6/100，Baseline 平均 35.0/100，差值 +60.6。
2. 差距最明显的维度是阶段门禁和证据扎根，说明它的价值不只是生成文本，而是把阶段门禁、证据边界和交付边界流程化。
3. 我保留了每轮 raw output、规则评分和盲评结果；如果某个任务表现不好，会作为产品边界分析，而不是包装成成功。

## 结论边界

- 本报告证明的是这些任务集上的可控性与可复盘优势，不代表所有模型、所有产品领域、所有用户输入下的绝对优势。
- LLM 盲评是辅助判断；规则评分与 raw output 是主要证据。
- 任何包含真实 API 的结论都应引用本目录下的 raw JSON，而不是只引用汇总表。