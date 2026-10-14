# 多智能体 AI 科研工作流

[English overview](README.en.md)

一个可移植的研究协作框架：从问题和初步想法出发，检索已有工作，共同设计方法与实验，执行和分析结果，写作画图，再由独立审稿角色检查实质问题。研究者负责科学判断和关键实验设计；Agent 负责检索、实现、运行、分析和提出可验证的改进。

**本仓库提供角色指令、工作流与可选模板，不是已经实现的自动运行平台，也不追求全自动科研。** 它是人在回路（human-in-the-loop）的协作框架：研究者在关键决策点参与并确认（见[共享约定](agents/README.md)的“人在回路”），Agent 在已确认的范围内推进。可以在支持多 Agent 的工具中分配角色，也可以让同一个 Agent 按任务依次使用这些指令；不绑定模型、编排器、学科、论文 venue 或计算环境。

## 快速开始

1. 将 [`profiles/user.example.md`](profiles/user.example.md) 复制为本地 `profiles/user.md`，只填写与协作有关的偏好；该文件默认不纳入 Git。
2. 有初步 idea 时，先看[怎样描述一个 idea](docs/idea-guideline.md)，用几句话或[简短模板](templates/idea.md)说明任务、观察依据、原因猜测、初步方法与这次目标；暂无方法也可以开始。已有材料可直接整理进[研究笔记](templates/research-note.md)，后续持续维护同一份笔记。
3. 给主 Agent 加载 [`agents/README.md`](agents/README.md)、[`agents/mentor.md`](agents/mentor.md)、本地用户档案和研究笔记。所有角色同时加载 [RSI 约定](docs/rsi.md)及适用的本地改进经验；具体任务再加载相应角色指令及其配套文件（见 [`agents/README.md`](agents/README.md) 的“加载清单”）。没有多 Agent 编排器时也可顺序执行。
4. 从当前最需要的工作开始。新 idea 通常先用 `literature + method`；已有代码或结果可直接进入 `code + analysis`；稿件交给 `writing`，最终通过 `reviewer` 入口安排独立的写作专家和领域专家审查。

一个可直接改写的起始任务：

> 阅读共享原则、导师和文献检索角色指令，以及本项目研究笔记。检索按[来源清单](docs/literature-sources.md)覆盖核心来源和本领域的会议、期刊。先查这个问题的已有解法、最接近的强基线与关键局限；列出对初步想法最有影响的证据和两个值得共同设计的验证实验。注明实际检索和阅读范围，关键判断回到原论文，不把计划写成已经完成的结果。

## 七种职责

| 角色 | 核心工作 |
|---|---|
| [`literature`](agents/literature.md) | 查已有解法、基线、可迁移机制与反证，记录证据来源 |
| [`method`](agents/method.md) | 与研究者共同形成方法和关键实验，评估可行性与缺陷 |
| [`code`](agents/code.md) | 实现、运行基线/方法/消融，保存配置、日志与复现入口 |
| [`analysis`](agents/analysis.md) | 复核结果、诊断失败，与方法角色提出下一轮比较 |
| [`writing`](agents/paper-writer.md) | 精读同类论文，基于真实证据写作并制作科研图表 |
| [`reviewer`](agents/manuscript-reviewer.md) | 双专家独立审稿：学术语言审校、领域写法对照及实质研究审查 |
| [`mentor`](agents/mentor.md) | 统筹方向、优先级和协作，澄清重要意图并维护偏好 |

这些是职责，不要求七个常驻进程。审稿模块分为[写作专家 `review-writing`](agents/writing-reviewer.md)和[领域专家 `review-domain`](agents/domain-reviewer.md)：前者检查语法、用词和学术表达，后者实际对照同方向顶刊顶会的论证、结构、实验与图表写法，并保留方法、贡献和证据的实质审查。两者独立于写作画图 Agent，分别出意见后由导师汇总；`reviewer` 是派工入口，不是额外第三位审稿人。其他角色可以合并或临时增加专长。

## 工作原则

- **借鉴有证据。** 看别人怎么做，也看别人怎么写；新机制和新颖性判断回到论文原文、官方实现和真实对照。
- **人参与设计。** 研究者选择问题、假设、关键实验和重要取舍；AI 主动指出不足、可行性限制和替代解释。
- **实验推动写作，写作反过来推动实验。** 不要求固定阶段门禁；根据已有材料从任何节点进入。
- **结果可追溯。** 主要结论对应实际代码、配置、数据说明、运行输出和分析；负结果也保留。
- **所有角色可自我改进。** 每个 Agent 按用户要求、反馈与真实结果改进策略及自身指令，也能改进自己的诊断和验证方法；有效性需实际检查，未检验的策略保留为候选，改动可撤回。机制见 [RSI](docs/rsi.md)，按需执行，不另设常驻角色或逐项审批。
- **双专家独立审稿。** 写作专家与领域专家可并行审查，导师汇总时优先处理影响研究成立的问题；领域专家补查作者引用之外的工作，写法对照有实际原文依据。

## 导航

- [idea 描述指南](docs/idea-guideline.md) · [架构与角色协作](docs/architecture.md) · [轻量工作流](docs/workflows.md) · [日常任务调度](docs/operating-model.md)
- [文献、写作与审稿](docs/literature-and-writing.md) · [检索来源与领域选择](docs/literature-sources.md) · [个性化机制](docs/personalization.md) · [所有角色的 RSI](docs/rsi.md)
- [按需模板](templates/README.md) · [虚构项目示例](examples/README.md)
- [已有 AutoResearch 项目对照](docs/prior-art.md) · [nnU-Net 的跨任务研究启发](docs/nnunet-lessons.md)
- [真实使用复盘（2026-10）](docs/lessons-2026-10.md) · [版本记录](CHANGELOG.md)

`profiles/user.md` 和具体研究材料默认留在本地（`.gitignore` 也排除了 `studies/` 与 `docs/reference/`，可分别用来放本地研究项目和参考材料，需要时自行创建）。不要把私有数据、凭证、未获许可的论文全文或原始缓存加入公开仓库。
