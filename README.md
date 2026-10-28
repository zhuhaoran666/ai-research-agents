# 多智能体 AI 科研工作流

[English overview](README.en.md)

一个可移植的研究协作框架：从问题和初步想法出发，检索已有工作，共同设计方法与实验，执行和分析结果，写作画图，再由独立审稿角色检查实质问题。研究者负责科学判断和关键实验设计；Agent 负责检索、实现、运行、分析和提出可验证的改进。

**本仓库提供角色、技能、工作流与可选模板，是人在回路的协作框架。** 研究者参与重大科研判断；代理复用已有材料、决定和授权，在范围内推进工作。执行边界见[共享约定](agents/README.md)的“人在回路”。它不等于已启动的自动运行平台，不绑定模型、编排器、学科或计算环境。

长时间检索、比较与分析在已确认的范围内交后台；前台及时回应问题、反馈已核发现，每轮聚焦一个科研选择，帮助研究者保持注意力。实时交流及客户端能力限制的处理见[共享约定](agents/README.md)的“实时交流与后台工作”。

## 快速开始

1. 直接把想法、代码、结果或稿件交给导师 Agent，说清这次想解决什么。导师按[逐步引导](docs/mentor-guided-intake.md)判断起点，每轮只问一至三个影响下一步的问题；未知的文献、基线与环境由相关 Agent 帮助调查，不要求先填完整表格。
2. 有初步 idea 时，可参考[怎样描述一个 idea](docs/idea-guideline.md)或[简短模板](templates/idea.md)；暂无方法也可以开始。导师将已有材料与后续回答逐步整理进同一份[研究笔记](templates/research-note.md)。需要长期偏好时，再将 [`profiles/user.example.md`](profiles/user.example.md) 复制为本地 `profiles/user.md`；没有档案也能工作，该文件默认不纳入 Git。
3. 跨角色任务加载[科研协作入口](skills/ai-research-workflow/SKILL.md)与[共享约定](agents/README.md)；单项任务直接按[角色技能索引](skills/README.md)选择主技能。只加载当前任务所需材料，私人偏好与改进经验按相关性读取；没有多 Agent 编排器时可顺序执行并披露独立性限制。
4. 从当前最需要的工作开始。新 idea 通常先用 `literature + method`；已有代码或结果可直接进入 `code + analysis`；稿件交给 `writing`，最终通过 `reviewer` 入口安排独立的写作专家和领域专家审查。

一个可直接改写的起始任务：

> 复用本项目已有材料，按当前问题选择角色与技能。这次我想解决：……。只补问会改变下一步的必要信息，沿用已有决定和授权，继续可独立完成的工作；重大科研或资源取舍给我有依据的选项。交付实际成果、验证状态与重要缺口，不为局部任务启动完整流程。

进入实验后，按[实验反馈与证据链](docs/experiment-loop.md)接入现有运行环境，区分工程失败、有效负结果和证据不足。仓库还提供一个可选的 Python 标准库[证据检查器](scripts/check_evidence.py)，用于核对文件、指标来源与声明数字；它不执行实验，也不能代替科学审查。

## 研究与审校职责

| 角色 | 核心工作 |
|---|---|
| [`literature`](agents/literature.md) | 查已有解法、基线、可迁移机制与反证，记录证据来源 |
| [`method`](agents/method.md) | 与研究者共同形成方法和关键实验，评估可行性与缺陷 |
| [`code`](agents/code.md) | 实现、运行基线/方法/消融，保存配置、日志与复现入口 |
| [`analysis`](agents/analysis.md) | 复核结果、诊断失败，与方法角色提出下一轮比较 |
| [`writing`](agents/paper-writer.md) | 精读同类论文，基于真实证据写作并制作科研图表 |
| [`reviewer`](agents/manuscript-reviewer.md) | 双专家独立审稿：学术语言审校、领域写法对照及实质研究审查 |
| [`mentor`](agents/mentor.md) | 逐步引导用户补齐当前所需信息，统筹方向、优先级和协作 |
| [`review-redundancy`](agents/redundancy-reviewer.md) | 通过删除试验检测无交流价值的内容，保留原意并按需精简 |

这些是职责，不要求所有角色常驻。审稿模块分为[写作专家 `review-writing`](agents/writing-reviewer.md)和[领域专家 `review-domain`](agents/domain-reviewer.md)：前者检查语法、用词和学术表达，后者实际对照同方向顶刊顶会的论证、结构、实验与图表写法，并保留方法、贡献和证据的实质审查。两者独立于写作画图 Agent，分别出意见后由导师汇总；`reviewer` 是派工入口，不是额外第三位审稿人。其他角色可以合并或临时增加专长。

[冗余审校 `review-redundancy`](agents/redundancy-reviewer.md)跨角色检查对话、文稿、说明及代码。默认检测模式，只按“原文 → 建议（一句理由）”列可操作的问题；精简模式给完整精简稿。没有明确问题时只回复“未发现明确的可删冗余”。

## 工作原则

- **借鉴有证据。** 看别人怎么做，也看别人怎么写；新机制和新颖性判断回到论文原文、官方实现和真实对照。
- **研究者参与重要取舍。** 科研方向、关键协议和主张实质由研究者参与决定；已有授权范围内的具体工作持续推进，额外资源和外发不自动授权。
- **实验推动写作，写作反过来推动实验。** 不要求固定阶段门禁；根据已有材料从任何节点进入。
- **结果可追溯。** 主要结论对应实际代码、配置、数据说明、运行输出和分析；负结果也保留。
- **所有角色可改进做法。** 在任务范围内依据真实失败和明确反馈调整，保留验证、适用条件与可撤回版本；未验证策略保持候选，不把策略改善当作方法有效。详情见 [RSI](docs/rsi.md)。
- **双专家独立审稿。** 写作专家与领域专家可并行审查，导师汇总时优先处理影响研究成立的问题；领域专家补查作者引用之外的工作，写法对照有实际原文依据。

## 导航

- [导师逐步引导](docs/mentor-guided-intake.md) · [idea 描述指南](docs/idea-guideline.md) · [架构与角色协作](docs/architecture.md) · [轻量工作流](docs/workflows.md) · [日常任务调度](docs/operating-model.md)
- [实验反馈与证据链](docs/experiment-loop.md) · [可运行的合成证据示例](examples/evidence-demo/README.md)
- [文献、写作与审稿](docs/literature-and-writing.md) · [检索来源与领域选择](docs/literature-sources.md) · [个性化机制](docs/personalization.md) · [所有角色的 RSI](docs/rsi.md)
- [中文学术写作规则](docs/chinese-academic-writing.md)：领域惯用术语、具体现象、自然句法与科学含义核对
- [十个角色的技能索引](skills/README.md) · [科研协作入口](skills/ai-research-workflow/SKILL.md) · [科研论文写作](skills/research-paper-writing/SKILL.md) · [易读易维护的代码工程](skills/readable-code-engineer/SKILL.md)
- [按需模板](templates/README.md) · [虚构项目示例](examples/README.md)
- [已有 AutoResearch 项目对照](docs/prior-art.md) · [The AI Scientist 的启发与边界](docs/ai-scientist-lessons.md) · [nnU-Net 的跨任务研究启发](docs/nnunet-lessons.md)
- [真实使用复盘（2026-10）](docs/lessons-2026-10.md) · [版本记录](CHANGELOG.md)

`profiles/user.md` 和具体研究材料默认留在本地（`.gitignore` 也排除了 `studies/` 与 `docs/reference/`，可分别用来放本地研究项目和参考材料，需要时自行创建）。不要把私有数据、凭证、未获许可的论文全文或原始缓存加入公开仓库。
