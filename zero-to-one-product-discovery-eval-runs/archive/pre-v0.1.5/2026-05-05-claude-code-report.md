# Claude Code Evaluation Report: 2026-05-05

## Environment

- Agent: Claude Code (Anthropic CLI)
- Model: claude-sonnet (assumed; this evaluator session)
- Date: 2026-05-05
- Repository: /Users/conrad/Desktop/archive/AI学习/OmniWed (not a git repo)
- Skill version: zero-to-one-product-discovery 0.1.0-draft
- Evaluation file: zero-to-one-product-discovery/evals/evals.json
- Rubric file: zero-to-one-product-discovery/evals/eval-rubric-template.md

## Summary

| Scenario | Expected Mode | Score | Hard Failure | Verdict |
|---|---|---:|---|---|
| zero_idea_vague | Diagnostic Start | 99 | None | Pass |
| zero_open_source_project | Diagnostic Start | 99 | None | Pass |
| existing_prd_no_mvp | Diagnostic Start + Material Assimilation rec. | 99 | None | Pass |
| existing_mvp_improvement | Do not trigger | 100 | None | Pass |
| narrow_bugfix | Do not trigger | 100 | None | Pass |
| heavy_advisor_requested | Heavy Advisor | 88 | None | Pass |
| design_reference_early | Diagnostic Start | 100 | None | Pass |

## Aggregate

- Average score: 97.86
- Median score: 99
- Lowest score: 88
- Hard failure count: 0
- Suite pass threshold: 85
- Install candidate threshold: 90
- Install candidate: Yes (avg 97.86 ≥ 90, lowest 88 ≥ 85, no hard failures)

## Scenario Results

### Scenario: zero_idea_vague

#### Hard Failure Check

- [ ] wrong_trigger_decision — correctly used Diagnostic Start
- [ ] asks_mature_product_question_upfront — did not lead with "target user / MVP / tech stack / business model"; the single question came after candidate interpretations
- [ ] produces_later_stage_artifacts — no PRD / Roadmap / Milestones / ADR / tech stack / MVP scope
- [ ] asks_multiple_key_questions — exactly one trade-off question
- [ ] generic_response — explicitly anchored on students, courses, assignments, club activities; called out 教务系统 / QQ / 班群 / 社长 as the existing ecosystem

#### Score

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger accuracy | 15 | 15 | Defaulted to Diagnostic Start; offered deeper modes without forcing a choice. |
| Stage purity | 15 | 15 | Output respected the seven-section Diagnostic Start template; no MVP scope, tech stack, or roadmap leaked. |
| Context grounding | 15 | 15 | Mentioned 大学生、课程、作业、社团活动; specifically named 教务系统、QQ、微信群、班群、老师、社长 as existing players. |
| Fact / assumption / risk split | 15 | 15 | Explicit 4-way split with separate facts, assumptions, risks, unknowns sections; each populated. |
| Candidate exploration directions | 10 | 10 | Three sharp directions: 学业纵深 / 社团协同 / 学生信息聚合, each genuinely different in user, surface, and competition. |
| Dangerous assumption | 10 | 10 | Identified the unification assumption (三件事必须由同一个工具来管) — directly attacks the prompt's premise rather than a generic risk. |
| Question quality | 10 | 10 | Single trade-off ("最痛的是哪一件") with explanation that surfaces three different product forms. |
| Context economy | 10 | 9 | ~700 Chinese chars, near the upper end of the recommended range; structure is dense without filler. |
| Total | 100 | 99 |  |

#### Verdict

Pass.

#### Patch Needed

None for this scenario.

---

### Scenario: zero_open_source_project

#### Hard Failure Check

- [ ] wrong_trigger_decision — correctly Diagnostic Start
- [ ] asks_mature_product_question_upfront — no mature-product question upfront; question came after candidate interpretations
- [ ] produces_later_stage_artifacts — no scaffolding, ADR, repo layout, tech stack
- [ ] asks_multiple_key_questions — exactly one
- [ ] generic_response — referenced 开源、简历、AI 编程工具、效率, named cursor rules / awesome-prompts / wrapper / benchmark 仓库 as competitive context
- [ ] scenario-specific: did not jump to repository scaffolding; did not assume product form (left CLI / plugin / dashboard open via three directions); preserved open-source + resume value as evaluation constraints

#### Score

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger accuracy | 15 | 15 | Correct Diagnostic Start. |
| Stage purity | 15 | 15 | No PRD, Roadmap, ADR, tech stack, scaffolding. |
| Context grounding | 15 | 15 | References crowded landscape (cursor rules / wrapper / benchmark) and specifically asks AIPM vs research vs ind dev for resume audience. |
| Fact / assumption / risk split | 15 | 15 | Clear 4-way split; risks include differentiation, abandonment, and unclear "developer" archetype. |
| Candidate exploration directions | 10 | 10 | Three differentiated forms: 工具增强 / 工作流编排 / 评测与基准. |
| Dangerous assumption | 10 | 10 | Calls out the "tool-side vs user-side bottleneck" question — strikes at whether building a tool is even the right move. |
| Question quality | 10 | 10 | One trade-off (resume audience) that genuinely changes the product's story. |
| Context economy | 10 | 9 | ~750 chars with explicit "evaluation constraints" callout; close to the upper bound of the recommended length. |
| Total | 100 | 99 |  |

#### Verdict

Pass.

#### Patch Needed

None for this scenario.

---

### Scenario: existing_prd_no_mvp

#### Hard Failure Check

- [ ] wrong_trigger_decision — correctly triggered (still zero-to-one because no MVP)
- [ ] asks_mature_product_question_upfront — the question is to inspect/summarize the existing material, which the skill explicitly permits ("the single high-leverage question may ask the user to provide or identify the material to inspect")
- [ ] produces_later_stage_artifacts — none
- [ ] asks_multiple_key_questions — one
- [ ] generic_response — explicitly references PRD draft + 用户反馈; gives concrete material-handling guidance
- [ ] scenario-specific: did not treat as product improvement; recommended Material Assimilation; required feedback triage rather than treating it as direct requirements

#### Score

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger accuracy | 15 | 15 | Triggered with explicit Material Assimilation recommendation. |
| Stage purity | 15 | 15 | Did not produce PRD edits, MVP cuts, or implementation plan; kept the next move at "consume materials". |
| Context grounding | 15 | 15 | Distinguishes "有 PRD 草稿/反馈" from "有产品"; flags PRD ↔ MVP gap and feedback triage explicitly. |
| Fact / assumption / risk split | 15 | 15 | Four-way split; risks include "feedback as direct requirements" and PRD-to-MVP断层. |
| Candidate exploration directions | 10 | 10 | 物料消化 / 反馈三角化 / MVP 假设推导 — each maps to a different theory about the PRD's maturity. |
| Dangerous assumption | 10 | 10 | "PRD 作为蓝图直接进入实施 + 反馈是直接需求清单" — exactly the failure mode the skill warns against. |
| Question quality | 10 | 10 | Single question that asks for the materials before continuing — the skill explicitly sanctions this form when materials are referenced but not provided. |
| Context economy | 10 | 9 | ~820 chars; within soft limit but on the heavy side. |
| Total | 100 | 99 |  |

#### Verdict

Pass.

#### Patch Needed

None for this scenario.

---

### Scenario: existing_mvp_improvement

#### Hard Failure Check

- [ ] wrong_trigger_decision — correctly did NOT trigger
- [ ] asks_mature_product_question_upfront — N/A (non-trigger); did not ask product strategy questions
- [ ] produces_later_stage_artifacts — none
- [ ] asks_multiple_key_questions — final question ("从哪一步开始") is an improvement-path follow-up, not a discovery key-question
- [ ] generic_response — referenced "可运行 MVP"、"十几个真实用户反馈"、"转化率"、"核心体验" directly; suggested漏斗诊断 / 反馈分诊 / 核心体验定义 as concrete improvement paths
- [ ] scenario-specific: identified the runnable MVP as the boundary; offered first-principles reset only as opt-in; suggested an improvement-style direction without fabricating a not-yet-existing skill (called it "I do not have a専门 skill" rather than inventing one)

#### Score

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger accuracy | 15 | 15 | Correctly suppressed Diagnostic Start. |
| Stage purity | 15 | 15 | No FAR / candidate directions / MVP scope / artifacts. |
| Context grounding | 15 | 15 | Boundary message uses the user's exact framing (MVP + 反馈 + 转化率 + 核心体验). |
| Fact / assumption / risk split | 15 | 15 | Full credit per non-trigger rule (correctly avoided discovery artifacts). |
| Candidate exploration directions | 10 | 10 | Full credit per non-trigger rule. |
| Dangerous assumption | 10 | 10 | Full credit per non-trigger rule. |
| Question quality | 10 | 10 | Full credit per non-trigger rule (no strategic discovery questions). |
| Context economy | 10 | 10 | Concise; explained boundary then handed back. |
| Total | 100 | 100 |  |

#### Verdict

Pass.

#### Patch Needed

None for this scenario.

---

### Scenario: narrow_bugfix

#### Hard Failure Check

- [ ] wrong_trigger_decision — correctly did NOT trigger
- [ ] asks_mature_product_question_upfront — none
- [ ] produces_later_stage_artifacts — none
- [ ] asks_multiple_key_questions — the three asks are code/log requests, not strategic product questions
- [ ] generic_response — referenced React, button, onClick, popup component variants (Modal, Dialog, react-toastify, react-hot-toast)
- [ ] scenario-specific: avoided product-discovery framing; treated as implementation/debugging; did not ask strategic product questions

#### Score

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger accuracy | 15 | 15 | Correctly skipped product discovery. |
| Stage purity | 15 | 15 | No FAR / directions / artifacts. |
| Context grounding | 15 | 15 | Asked for the specific React snippet, dialog component, console output. |
| Fact / assumption / risk split | 15 | 15 | Full credit per non-trigger rule. |
| Candidate exploration directions | 10 | 10 | Full credit per non-trigger rule. |
| Dangerous assumption | 10 | 10 | Full credit per non-trigger rule. |
| Question quality | 10 | 10 | Full credit per non-trigger rule. |
| Context economy | 10 | 10 | Very tight — three concrete requests, no padding. |
| Total | 100 | 100 |  |

#### Verdict

Pass.

#### Patch Needed

None for this scenario.

---

### Scenario: heavy_advisor_requested

#### Hard Failure Check

- [ ] wrong_trigger_decision — correctly engaged Heavy Advisor
- [ ] asks_mature_product_question_upfront — did not ask "who's the target user / what's the MVP / what tech stack" upfront; the closing question for "一句话产品描述" came after the cost warning AND after the artifact outlines were laid out, matching the skill's "candidate interpretations first" rule
- [ ] produces_later_stage_artifacts — produced outlines + decision surfaces + assumption clearings, which the skill explicitly authorizes for Heavy Advisor with under-specified domain ("produce artifact outlines, decision surfaces, and assumptions"); items labeled [假设] / [决策面] / "骨架（待填）" / "候选条目"
- [ ] asks_multiple_key_questions — exactly one
- [ ] generic_response — Heavy Advisor outlines are inherently structural; named the user's request items (PRD / Roadmap / Milestone / ADR / 文档体系) verbatim and addressed each
- [ ] scenario-specific: did not refuse Heavy Advisor; warning came before the artifact outlines; every item labeled as assumption or decision surface, not fact

#### Score

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger accuracy | 15 | 15 | "确认进入 Heavy Advisor 模式" up front. |
| Stage purity | 15 | 15 | Outlines + decision surfaces + assumptions match the skill's HA-with-under-specified-domain rule; no completed PRD or final Roadmap. |
| Context grounding | 15 | 11 | Echoed the five artifact types the user named, but content remains structural because the user gave no domain. The grounding is in the request, not in any product substance — unavoidable but limits credit. |
| Fact / assumption / risk split | 15 | 11 | Contains a "全局假设清单" and risk callouts (cost, assumption-hardening) but is not the literal four-way split required of Diagnostic Start; the rubric still scores this dimension. |
| Candidate exploration directions | 10 | 7 | Did not give DS-style "two or three project-specific exploration directions"; the ADR candidates double as decision branches but are not exploration directions. Diagnostic Start vs Heavy Advisor difference accepted, but rubric dimension still partial. |
| Dangerous assumption | 10 | 10 | Named "假设硬化" — the meta-risk that is precisely most dangerous when entering HA prematurely; reinforced via a four-item global assumption list. |
| Question quality | 10 | 10 | Exactly one question; the trade-off is implicit but explicit reasoning ("通用模板 vs 针对你项目的输出") makes the leverage clear. |
| Context economy | 10 | 9 | Long but justifiable for HA; warning, outlines, assumption list, single question — no template dumping. |
| Total | 100 | 88 |  |

#### Verdict

Pass (≥ 85). Lowest in suite.

#### Patch Needed

- Add an explicit note in `SKILL.md` (or `references/workflow.md`) clarifying how the Diagnostic-Start FAR split, candidate-direction count, and single-trade-off-question rule map onto Heavy Advisor outputs — currently the rubric scores those dimensions for HA scenarios but the skill does not specify HA-equivalent forms (assumption list ↔ FAR; ADR/decision branches ↔ candidate directions).
- Consider adding a Heavy-Advisor-specific output skeleton to `references/planning-artifacts.md` that names the "outlines + decision surfaces + assumption clearings" trio explicitly so the skill's HA execution is more uniform.

---

### Scenario: design_reference_early

#### Hard Failure Check

- [ ] wrong_trigger_decision — correctly Diagnostic Start
- [ ] asks_mature_product_question_upfront — closing question ("给谁用、解决什么问题") came after candidate interpretations and FAR; targets the missing domain rather than mature-product detail
- [ ] produces_later_stage_artifacts — none
- [ ] asks_multiple_key_questions — one
- [ ] generic_response — explicit named the two reference sites; characterized them as marketing/launch language, not generic "good visuals"
- [ ] scenario-specific: did not analyze visuals during Diagnostic Start; preserved them as later design inputs; treated visual lock-in as the dangerous assumption rather than letting it drive problem definition

#### Score

| Dimension | Points | Score | Evidence |
|---|---:|---:|---|
| Trigger accuracy | 15 | 15 | Correct Diagnostic Start. |
| Stage purity | 15 | 15 | Visual analysis explicitly deferred; no UI / brand / palette commentary. |
| Context grounding | 15 | 15 | Names Shopify Editions and GTA VI; characterizes their context (发布会 / 大作首页) instead of treating them as abstract style references. |
| Fact / assumption / risk split | 15 | 15 | Four-way split, risks include the form-mismatch and visual-driving-problem failure modes. |
| Candidate exploration directions | 10 | 10 | Three differentiated forms (营销/品牌站本身 / 强 IP 内容产品 / 功能型产品) that test whether the visual references even apply. |
| Dangerous assumption | 10 | 10 | "视觉风格可以在产品问题定义之前先被锁定" — directly diagnoses the trap of design-first zero-to-one. |
| Question quality | 10 | 10 | Single trade-off ("给谁用、解决什么问题") with reasoning that ties back to whether visual references can survive into later stages. |
| Context economy | 10 | 10 | ~720 Chinese chars; within target range; no template dumping. |
| Total | 100 | 100 |  |

#### Verdict

Pass.

#### Patch Needed

None for this scenario.

---

## Findings

### Strengths

- **Trigger discrimination is reliable.** All seven scenarios — three triggers, two non-triggers, one Heavy Advisor request, and one design-reference temptation — landed on the right mode without ambiguity. The non-trigger scenarios (`existing_mvp_improvement`, `narrow_bugfix`) produced concise boundary messages without spilling into discovery territory.
- **Diagnostic Start template is internalized.** Scenarios 1–3 and 7 followed the seven-section structure (mode notice, zero-to-one judgment, material judgment, FAR, directions, dangerous assumption, single question) consistently, with project-specific content rather than templated filler.
- **The skill correctly resists premature artifacts.** No scenario produced a PRD, Roadmap, Milestones, ADR, or implementation plan during Diagnostic Start. Scenario 6 (Heavy Advisor) produced only outlines + decision surfaces + assumption clearings, with every leaf labeled `[假设]` or `[决策面]`.
- **Material handling is well-distinguished from product completion.** Scenario 3 correctly held the line that "PRD draft + feedback ≠ existing product" and steered to Material Assimilation, with feedback triage flagged before MVP cutting.
- **Design-reference deferral works.** Scenario 7 acknowledged the references as later design inputs without analyzing their visuals, and named the visual-driving-problem trap as the dangerous assumption.

### Weaknesses

- **Heavy Advisor scoring fits the Diagnostic Start mold imperfectly.** Scenario 6 scored 88 — the lowest in the suite — primarily because the rubric scores `fact_assumption_risk_split`, `candidate_exploration_directions`, and `question_quality` against DS shape, but Heavy Advisor with an under-specified domain naturally produces a different shape (assumption list, ADR candidates, structural-leverage question). The response was correct per the skill's HA rule, but the rubric does not yet have an HA-specific scoring lens.
- **Diagnostic Start length consistently triggered the rubric's 700-char target deduction.** Scenarios 1, 2, 3 hovered around 700–820 Chinese characters and each lost 1 point on `context_economy`. **This is a rubric flaw, not a response flaw.** The skill is intended for Claude Opus 4.7 and GPT-5.5 thinking-x-high, where context is abundant; the responses used the space for genuine information density (FAR + 3 directions + dangerous assumption + reasoned question), not for filler. The character cap proxies for "no template dumping" but penalizes high-density output. See Patch 3 for the rubric fix.
- **The `existing_prd_no_mvp` material-inspection question doubles as both clarification and trade-off.** It is well-supported by the skill's explicit allowance, but a stricter reader could argue the question is closer to a request for input than a trade-off. Acceptable here; worth watching in future scenarios.

### Required Patches

The skill itself does not require code changes for the seven scenarios in this suite. The patches below are for the **rubric and supporting references**, to make Heavy Advisor scoring fairer and to give the skill a more uniform HA execution path:

1. **Rubric patch (`evals/eval-rubric-template.md` and `evals.json`)**: Add a Heavy-Advisor scoring lens. For scenarios where `expected_mode` is Heavy Advisor, map:
   - `fact_assumption_risk_split` → presence of an explicit assumption list + named risks (cost, assumption-hardening) rather than the literal four-way split.
   - `candidate_exploration_directions` → ADR candidates / decision branches surfaced in the outline.
   - `question_quality` → leverage and trade-off explanation, even if the question is for one-line domain rather than between two product paths.
2. **Skill patch (`SKILL.md` Exploration Depth or `references/workflow.md`)**: Add a one-paragraph HA-output skeleton — "outlines + decision surfaces + assumption clearings" — and explicitly state that under-specified domain HA must label every leaf as `[假设]` or `[决策面]`. This standardizes the response shape across runs.
3. **Rubric patch (`evals.json` `recommended_diagnostic_start_length` block)**: The current 700-char target / 900-char soft-limit penalty is solving the wrong problem. This skill is intended to run on Claude Opus 4.7 and GPT-5.5 thinking-x-high — both have abundant context. A character cap proxies for "no template dumping / no filler", but on top-tier models the actual filler rate is already low; capping length compresses high-density content, not bloat. Recommended changes:
   - Reframe `context_economy` scoring to look for **template dumping, padding phrases, redundant summaries, repeated content**, NOT raw character count.
   - Either widen the soft limit substantially (e.g., 1500+) or remove it entirely; the skill's "Target 300-700" line in `SKILL.md` should be read as "below 300 you're probably under-delivering", not as a ceiling.
   - This aligns with the model-deployment reality: forcing compression at 700 chars actively limits what these models can deliver in a Diagnostic Start that legitimately uses FAR + 3 directions + dangerous assumption + reasoned question.

### Follow-up Scenarios

1. **Heavy Advisor with a real domain.** A scenario where the user requests Heavy Advisor and gives one-line domain context (e.g., "做一个面向独立咖啡店的库存管理 SaaS"). Tests whether HA produces concrete outlines vs hardening assumptions when grounding is available.
2. **Material Assimilation execution.** A follow-up turn where the user provides their PRD draft (not just announces it). Tests whether the skill reads, challenges, and upgrades existing material rather than rewriting it.
3. **Mid-stream first-principles reset.** A user with a runnable MVP who explicitly says "I want to revisit from first principles." Tests the boundary-crossing path that scenario 4 only mentioned in passing.
4. **Conflicting user-stated requirements.** A scenario where the user lists features and asks Claude to "just plan the build." Tests demand-triage-before-acceptance.
5. **Long-material prompt.** A scenario where the user pastes a 2000-character PRD draft inline. Tests whether the skill stays concise (summarize, don't dump templates) when given long inputs.
