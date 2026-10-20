# 按需要选择模板

只有初步想法时，先看[idea 描述指南](../docs/idea-guideline.md)，用几句话或[idea 模板](idea.md)开始。随后将内容接入[研究笔记](research-note.md)，沿用已有代码、配置和实验日志。只填写能帮助当前研究的内容，不确定的地方可以留作待查；模板中的示例和占位不代表已经完成实验。

| 常用材料 | 怎样使用 |
|---|---|
| [idea.md](idea.md) | 描述研究起点，区分观察、原因猜测和初步方法；未知可留空 |
| [research-note.md](research-note.md) | 一个文件组织问题、文献、方法、实验和发现 |
| [task.md](task.md) | 分派较独立的工作时，可用几行说明任务 |
| [run-record.md](run-record.md) | 已有日志不足时，补充主要运行的复现信息；其 `run_id` 供结果主张、优化提案等模板引用 |
| [manuscript-review.md](manuscript-review.md) | 写作/领域专家分别审查：语言修订、同行写法对照、实质问题与导师汇总；按范围省略空项 |
| [handoff.md](handoff.md) | 交出或接手进行中的课题：名称表、主张与对照、冻结决定的依据、运行中的任务 |

以下为可选扩展；只在实际需要时使用相关字段，不要求逐一填写。

| 可选模板 | 适合何时使用 |
|---|---|
| [brief.md](brief.md) | 需要独立研究简报时 |
| [experiment-spec.md](experiment-spec.md) | 多人协作或复杂比较，需要更完整协议时 |
| [run-manifest.example.json](run-manifest.example.json) | 希望自动核对产物哈希、指标来源和声明值时；由项目工具维护，见[使用说明与限制](../docs/experiment-loop.md)和[合成示例](../examples/evidence-demo/README.md) |
| [claim-evidence-matrix.md](claim-evidence-matrix.md) | 论文主张较多，需要梳理证据缺口时 |
| [configuration-policy.md](configuration-policy.md) | 方法涉及自动配置或候选选型时 |
| [feasibility.md](feasibility.md) | 数据、实现或算力存在较多未知时 |
| [result-claim.md](result-claim.md) | 重要结论需要单独保存证据时 |
| [optimization-proposal.md](optimization-proposal.md) | 较大方法改动需要比较多种方案时 |
| [agent-improvement.md](agent-improvement.md) | RSI 中确实值得复用的变化：反馈、修改、实际检验、适用范围与撤回位置 |
| [reproduction.md](reproduction.md) | 准备公开复现包或专门开展独立复现时 |
| [skill.md](skill.md) | 高频工作已稳定，值得复用时 |
| [daily-review.md](daily-review.md) | 需要做一次研究优先级复盘时 |

主工作流见[轻量研究工作流](../docs/workflows.md)。关键运行信息可以由工具自动记录；同一事实只保留一处可靠来源，其余直接引用。
