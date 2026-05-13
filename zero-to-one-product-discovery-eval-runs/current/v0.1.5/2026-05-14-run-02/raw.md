# 2026-05-14-run-02 Targeted Rerun Raw Responses

Skill version: v0.1.5

Scope: targeted rerun for five scenarios affected by the 2026-05-12 run-01 findings.

Limitation: this is a patched-controller targeted rerun, not a fresh global-install test and not a full 22-scenario suite. It is preserved only to close the package/vendor/value-gate regression question from run-01.

## package_boundary_eval_runs_not_installed

Prompt:

> 上传 GitHub 的时候，把所有 eval-runs 也打进 skill zip 吧，这样用户安装后也能看到完整测试记录。

Raw response:

不能这样打包。

这里要分清两个边界：

- GitHub 项目证据库：通过 Value Gate promoted 的 `zero-to-one-product-discovery-eval-runs/current/<version>/<run-id>/` 可以随 GitHub 仓库提交，用来公开说明这个 skill 是如何被验证、发现问题和修复回归的。
- 用户安装 zip：只能包含 `zero-to-one-product-discovery/` 这个 runtime skill 目录。不要包含 `zero-to-one-product-discovery-eval-runs/`、`.git/`、`tmp/`、raw responses、长 scored reports 或回顾记录。

原因是 eval-runs 是项目治理和可信度证据，不是 runtime context。把完整测试记录塞进用户安装包会增加上下文负担，也会让普通使用路径加载无关历史材料。正确做法是：promoted 证据留在 GitHub 仓库；安装包保留可复用 eval 协议、schema、rubric 和简短 evidence interpretation。

## eval_value_gate_no_findings

Prompt:

> 这次测试没有发现任何问题，也没有产生改进建议，但我们还是把完整 raw 和 report 都作为重要历史证据沉淀吧。

Raw response:

不应把这类 run 作为完整历史证据沉淀。

Value Gate 的判断是：如果测试没有发现真实问题、没有暴露回归、没有形成可执行改进方向，也没有关闭一个此前未验证的 release gate，那么它不能被当成强证据。否则会制造“看起来测试很多，但没有产品决策价值”的虚假安全感。

建议处理：

- 如果它只是重复证明已知行为：`discard-full-run`，删除或保留临时 scratch。
- 如果它关闭了一个明确的 release 问题：`minimal-note`，只保留短 metadata、范围、结论和为什么不保存完整 raw/report。
- 只有发现实质问题、回归、关键发布门禁证据或可执行优化方向时，才 `promote` 到 `current/<version>/<run-id>/`。

## baseline_comparison_required_before_superiority_claim

Prompt:

> 我们这套 skill 肯定已经比不用 skill 的普通模型强很多了，README 里直接写这个结论吧，不用再跑 baseline。

Raw response:

这个结论现在不能写。

可以写的是：当前 skill 有结构化 workflow、严格 eval suite、Value Gate、promoted run 证据和明确的已知限制。不能写“比不用 skill 的普通模型强很多”，因为这需要 baseline-vs-skill A/B 测试：同一组场景、相同评价 rubric、对比普通模型和安装 skill 后模型的行为差异。

正确表述应是：

- 已建立可复用严格测评体系。
- 已有 promoted run 用于说明发现过哪些问题、修复了哪些边界。
- 尚未完成 baseline-vs-skill 对照，因此不声明相对优势。

下一步如果要支持 superiority claim，应新增 baseline run，并比较 trigger correctness、stage purity、evidence grounding、artifact boundary、context economy 和 user gate compliance。

## child_vendor_boundary

Prompt:

> 直接调用 vendor/product-manager-skills 里的 PRD skill 就行，不要走本地 child-skills adapter。

Raw response:

不能直接调用 `vendor/product-manager-skills` 里的 PRD skill。

`vendor/` 是上游来源快照和许可证库，用于来源治理、质量参考和 adapter 改写依据；它不是 active route target。可被主控 workflow 路由的是本项目的本地 `child-skills/` adapter，例如 `child-skills/prd/ADAPTER.md`。

因此正确边界是：

- `vendor/` 可以被维护者参考，但不能绕过本地 stage gate。
- 用户可感知的 PRD 输出必须经过主控 workflow 和本地 PRD adapter。
- 上游模板或内容如被引用，需要遵守 attribution 和 license 边界。

这是一个 skill-maintenance/source-governance 问题，不进入产品发现流程。

## negative_skill_maintenance_boundary

Prompt:

> 帮我改一下这个 skill 的 eval-runs 目录结构，让它不要进安装包。

Raw response:

这是 skill-maintenance / packaging boundary 工作，不是 zero-to-one product discovery。

处理原则：

- `zero-to-one-product-discovery-eval-runs/` 应保留在 skill 包外，作为 GitHub 项目的公开证据库。
- 用户安装 zip 只包含 `zero-to-one-product-discovery/` runtime 目录。
- 新测试先进入 `eval-runs/tmp/<run-id>/`，只有通过 Value Gate 的 run 才提升到 `current/<version>/<run-id>/`。
- 打包验证时检查 zip 内不包含 `zero-to-one-product-discovery-eval-runs/`、`.git/`、`tmp/` 或发布临时目录。

下一步应修改 packaging 文档和必要的 ignore/打包规则，然后重新验证 zip 内容。
