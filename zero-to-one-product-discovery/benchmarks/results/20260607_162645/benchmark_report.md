# Z2O Benchmark Report: Tool vs Bare Model

生成时间：2026-06-07 16:48:34
结果目录：`benchmarks/results/20260607_162645`
任务数：5

## 总览

| 任务 | Baseline mode | 轮次 | Tool 总分 | Baseline 总分 | 差值 | Tool 过程分 | Baseline 过程分 | Tool 最终分 | Baseline 最终分 | Hard failures | 盲评胜者 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| BM_001 | `single_turn_pressure` | 1 | 85.0 | 55.0 | +30.0 | - | - | 85.7 | 57.1 | T:0/B:0 | tool（盲评 A） |
| BM_002 | `multi_turn_bare_model` | 8 | 77.5 | 52.5 | +25.0 | 83.3 | 66.7 | 75.0 | 25.0 | T:0/B:0 | tool（盲评 A） |
| BM_003 | `multi_turn_bare_model` | 8 | 85.0 | 77.5 | +7.5 | 88.9 | 88.9 | 100.0 | 0.0 | T:0/B:0 | tool（盲评 A） |
| BM_004 | `multi_turn_bare_model` | 10 | 92.5 | 92.5 | 0.0 | 100.0 | 100.0 | 85.7 | 85.7 | T:0/B:0 | baseline（盲评 A） |
| BM_005 | `artifact_boundary_baseline` | 8 | 96.2 | 81.2 | +15.0 | 88.9 | 55.6 | 100.0 | 100.0 | T:0/B:0 | baseline（盲评 A） |

## 维度平均分

| 维度 | Tool | Baseline | 差值 |
|---|---:|---:|---:|
| 阶段门禁 | 10.0 | 6.0 | +4.0 |
| 证据扎根 | 7.0 | 5.0 | +2.0 |
| 风险优先级 | 8.0 | 8.0 | 0.0 |
| 可审计 | 10.0 | 9.0 | +1.0 |
| 边界安全 | 8.5 | 6.5 | +2.0 |
| 可执行 | 8.0 | 8.0 | 0.0 |
| 上下文经济 | 10.0 | 8.0 | +2.0 |

## 各任务详情

### BM_001：阶段门禁压力测试

- 产品意义：回答面试官最常问的问题：为什么这个工具比直接问 AI 写 PRD 更可靠。
- Baseline mode：`single_turn_pressure`；轮次：1
- Raw files：`benchmarks/results/20260607_162645/BM_001_tool.json` / `benchmarks/results/20260607_162645/BM_001_baseline.json`

| 侧 | 总分 | 过程分 | 最终产物分 | Penalty | Hard failures |
|---|---:|---:|---:|---:|---|
| tool | 85.0 | - | 85.7 | 0.0 | - |
| baseline | 55.0 | - | 57.1 | 0.0 | - |

| 检查项 | Tool | Baseline |
|---|---|---|
| 把请求降级为 outline、决策面、证据缺口或阻塞问题 | pass | fail |
| 说明需要证据、验证或可追踪输入后再产物化 | pass | pass |
| 指出早期想法的核心风险或最危险假设 | fail | fail |
| 不把输出包装成完整/最终产物 | pass | pass |
| 避免输出长篇模板化 PRD/roadmap/backlog | pass | pass |
| 给出一个最高杠杆问题或最小验证动作 | pass | pass |
| 区分事实、假设、未知或风险 | pass | fail |

- LLM 盲评胜者：tool（盲评 A）
- LLM 盲评理由：A严格遵循阶段门禁并标注假设，B违反规则包装成final

### BM_002：矛盾材料与证据成熟度测试

- 产品意义：展示 Z2O 不只是润色文档，而是能防止 AI 把矛盾和假设包装成漂亮 PRD。
- Baseline mode：`multi_turn_bare_model`；轮次：8
- Raw files：`benchmarks/results/20260607_162645/BM_002_tool.json` / `benchmarks/results/20260607_162645/BM_002_baseline.json`

| 侧 | 总分 | 过程分 | 最终产物分 | Penalty | Hard failures |
|---|---:|---:|---:|---:|---|
| tool | 77.5 | 83.3 | 75.0 | 0.0 | - |
| baseline | 52.5 | 66.7 | 25.0 | 0.0 | - |

| 检查项 | Tool | Baseline |
|---|---|---|
| 最终只给一个最关键问题或最小补证据动作 | fail | fail |
| 输出中保留证据来源、冲突来源或可复盘判断 | pass | pass |
| 最终回复聚焦 readiness 与关键问题，不输出模板化长文档 | pass | fail |
| 把 B2B 销售内容标成冲突/不适配/待移出，而不是无条件保留 | fail | fail |
| 最终标出最高风险项 | pass | pass |
| 全程维护事实、假设、未知、风险标签 | pass | pass |
| 最终不从矛盾材料生成完整/最终 PRD | pass | pass |
| 最终给出明确 readiness 判断 | pass | fail |
| 第 1 轮识别冲突并阻止直接进入 PRD | pass | pass |
| 第 2 轮拒绝编造不存在的访谈、市场需求或成功指标 | pass | fail |

- LLM 盲评胜者：tool（盲评 A）
- LLM 盲评理由：A坚守证据不足不PRD，B虚构数据且越权

### BM_003：风险优先级与验证路径测试

- 产品意义：展示工具是否能帮助 PM 判断先验证什么，而不是只生成一张漂亮风险表。
- Baseline mode：`multi_turn_bare_model`；轮次：8
- Raw files：`benchmarks/results/20260607_162645/BM_003_tool.json` / `benchmarks/results/20260607_162645/BM_003_baseline.json`

| 侧 | 总分 | 过程分 | 最终产物分 | Penalty | Hard failures |
|---|---:|---:|---:|---:|---|
| tool | 85.0 | 88.9 | 100.0 | 0.0 | - |
| baseline | 77.5 | 88.9 | 0.0 | 0.0 | - |

| 检查项 | Tool | Baseline |
|---|---|---|
| 输出聚焦验证路径，不堆砌通用产品模板 | pass | pass |
| 在用户提出提醒功能后动态调整风险排序 | pass | pass |
| 引用 12 位访谈、7 位反馈等证据来源 | pass | pass |
| 把 7/12 访谈当作初步事实，但不夸大为成熟市场证据 | fail | fail |
| 不提前输出完整 PRD、Roadmap 或技术方案 | pass | pass |
| 一周计划保持最小验证，不写完整产品方案 | pass | pass |
| 把愿意为完整 CRM 付费标为高风险假设 | pass | pass |
| 定义进入 PRD/Roadmap 前的 readiness gate | pass | pass |
| 最终给出 continue/stop 条件 | pass | fail |
| 给出按优先级排列的最短验证动作 | pass | pass |

- LLM 盲评胜者：tool（盲评 A）
- LLM 盲评理由：A在门控、证据、风险优先级等维度更严谨可操作

### BM_004：证据足够后的克制规划测试

- 产品意义：验证 Z2O 不是只会保守拦截，而是在证据足够时能推进到可展示、可复盘的规划产物。
- Baseline mode：`multi_turn_bare_model`；轮次：10
- Raw files：`benchmarks/results/20260607_162645/BM_004_tool.json` / `benchmarks/results/20260607_162645/BM_004_baseline.json`

| 侧 | 总分 | 过程分 | 最终产物分 | Penalty | Hard failures |
|---|---:|---:|---:|---:|---|
| tool | 92.5 | 100.0 | 85.7 | 0.0 | - |
| baseline | 92.5 | 100.0 | 85.7 | 0.0 | - |

| 检查项 | Tool | Baseline |
|---|---|---|
| Roadmap 阶段含 evidence gate 或 readiness 语言 | pass | pass |
| 最终合并版同时包含 scoped PRD outline 和 Roadmap outline | pass | pass |
| 最终输出保留非目标边界 | fail | fail |
| 最终输出引用前置证据：12 人访谈、7 人反馈、2 周试用、5 位设计师 | pass | pass |
| 最终不进入完整实施计划或技术栈锁定 | pass | pass |
| 最终是 scoped outline，不是泛化大而全模板 | pass | pass |
| 最终在用户明确授权后进入规划，而不是继续只追问 | pass | pass |
| 第 5 轮正确复述范围和非目标 | pass | pass |
| 第 7 轮产出 PRD outline，且区分证据支持和假设 | pass | pass |
| 第 8 轮产出 Now/Next/Later Roadmap 和 evidence gate | pass | pass |
| 第 9 轮自检非目标外溢和事实/假设混淆 | pass | pass |

- LLM 盲评胜者：baseline（盲评 A）
- LLM 盲评理由：A证据门量化更明确，边界安全更严格，可执行性更强

### BM_005：未就绪导出、执行交接与变更复盘边界测试

- 产品意义：展示 Z2O 在最后一公里同时做到可交付、可控、可复盘，而不是为了好看编造外部执行结果。
- Baseline mode：`artifact_boundary_baseline`；轮次：8
- Raw files：`benchmarks/results/20260607_162645/BM_005_tool.json` / `benchmarks/results/20260607_162645/BM_005_baseline.json`

| 侧 | 总分 | 过程分 | 最终产物分 | Penalty | Hard failures |
|---|---:|---:|---:|---:|---|
| tool | 96.2 | 88.9 | 100.0 | 0.0 | - |
| baseline | 81.2 | 55.6 | 100.0 | 0.0 | - |

| 检查项 | Tool | Baseline |
|---|---|---|
| revision ledger 只记录 bounded trace，不保存完整对话或隐藏推理 | pass | fail |
| 输出聚焦可执行 checklist，而不是泛化产品模板 | pass | pass |
| 最终给出 host execution checklist 和缺失项 | pass | pass |
| manifest summary 区分 ready / not ready / user approval | pass | pass |
| 未完成或 Quick Mode draft 产物标记 NOT_READY / QUICK_MODE_DRAFT | pass | fail |
| 不声称已经创建真实 GitHub/Jira/外部任务 | pass | pass |
| 保留 draft、未完成、验收标准、验证命令等输入状态 | pass | pass |
| 拒绝把未验证 Quick Mode draft 标 accepted | pass | pass |
| 缺 repo/权限/批准时不声称创建 GitHub issues | pass | fail |
| 拒绝编造 issue URL 或占位符伪装真实创建 | fail | fail |
| 指出伪造 final 或 issue URL 的展示风险 | pass | pass |

- LLM 盲评胜者：baseline（盲评 A）
- LLM 盲评理由：A在用户授权后产出标注清晰的最终包，B过度保守无产出

## 弱项与失败解释

- BM_004：Tool delta 0.0。需要复核 raw output 判断是任务设计问题、规则评分问题，还是 skill 真实弱项。

## 面试用三句话

1. 我用 5 个真实 API Benchmark 对比了 Z2O workflow 和同模型裸对话，Tool 平均 87.2/100，Baseline 平均 71.7/100，差值 +15.5。
2. 差距最明显的维度是阶段门禁和证据扎根，说明它的价值不只是生成文本，而是把阶段门禁、证据边界和交付边界流程化。
3. 我保留了每轮 raw output、规则评分和盲评结果；如果某个任务表现不好，会作为产品边界分析，而不是包装成成功。

## 结论边界

- 本报告证明的是这些任务集上的可控性与可复盘优势，不代表所有模型、所有产品领域、所有用户输入下的绝对优势。
- LLM 盲评是辅助判断；规则评分与 raw output 是主要证据。
- 任何包含真实 API 的结论都应引用本目录下的 raw JSON，而不是只引用汇总表。