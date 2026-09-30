# GitHub AutoResearch 工作流对照

查阅日期：2026-09-29。通过 GitHub 仓库搜索 `autoresearch` 与 `AI Scientist` 发现候选，选取下列五个项目比较受控实验、全流程协作、写作审稿与记忆。下面固定到实际读取的提交；阅读 README、工作流文档和指定代码，不代表已经安装运行或验证其论文质量。

## 从项目中吸收什么

| 项目与固定版本 | 已查看的机制 | 本框架的采用方式与边界 |
|---|---|---|
| [karpathy/autoresearch — 228791f](https://github.com/karpathy/autoresearch/tree/228791fb499afffb54b46200aca536f79142f117) | `program.md` 要求先跑 baseline，再修改、定时运行、记录 commit/val_bpb/显存和保留或丢弃；训练代码按预算执行 | 代码与分析角色采用“小改动—稳定比较—真实记录”。其单 GPU、约五分钟、单主要指标适合特定训练优化；本框架按实际任务确定预算和多维评价 |
| [AutoResearchClaw — be4ba47](https://github.com/aiming-lab/AutoResearchClaw/tree/be4ba4755bf1b52220f25e13b2293b5956590070) | 代码定义检索到论文修订的 23 阶段及回退，文档支持 co-pilot；干预学习与经验存储有实现路径 | 借鉴关键设计的人机协作、结果驱动修订和经验复用；在七个角色内灵活安排工作，不照搬全部阶段门禁 |
| [AI Scientist v2 — 96bd516](https://github.com/SakanaAI/AI-Scientist-v2/tree/96bd51617cfdbb494a9fc283af00fe090edfae48) | README 描述实验管理与树搜索；主入口调用实验、图形聚合、引用收集、写作及文本/图像评审 | 支持从实验积累进入写作画图与评审，方法/分析共同选择后续探索；开放树搜索仅作候选实现，当前不要求所有课题自动展开 |
| [EvoScientist — 8a05cae](https://github.com/EvoScientist/EvoScientist/tree/8a05cae32ec8d23a077eeba07030cf7ded2951b4) | README 列出 plan/research/code/debug/analyze/write 分工；记忆代码区分用户 profile、项目记录与 observations，要求有稳定依据的更新 | 导师维护“明确偏好、候选习惯、项目经验”，重复稳定动作可沉淀 Skill。研究者深度参与设计是本框架的明确要求 |
| [FAROS — 4e4e96f](https://github.com/OpenNSWM-Lab/FAROS/tree/4e4e96fde842ced39b5bfd805b5666b4ce7cca0e) | README 描述文献证据、PlanPackage、代码实验、论文图表和 ReviewX；评审定位主张、证据和测量并形成修订动作 | 审稿意见写清“位置、依据、影响和最小修改”，导师安排处理；此处仅核读 README，未验证 ReviewX 的实际性能或完整实现 |

## 对框架设计的启发

**轻量实验记录有用。** autoresearch 的变更与结果记录适合代码和分析角色；保留失败与负结果，同时限制单轮投入。不能把特定训练任务的最好验证分数等同于通用科研结论。

**有审稿步骤不自动代表有独立的深读。** 所查 AutoResearchClaw 知识提取主要以 shortlist 和可选 web context 为输入；审稿函数读取稿件和实验等材料。该检查范围内，不能认定它已主动精读核心全文并独立广泛补查。因此本框架单独明确写作和审稿各自的实际阅读要求。

**记忆需要来源和作用范围。** EvoScientist 的 profile 与 observation 分离，以及 AutoResearchClaw 的干预统计/经验存储，提供了实现参考。本框架将用户明确偏好直接应用，把推断保持为候选，项目经验保留条件；既往同意不自动扩大授权，搜索结果不自动成为个人偏好。

**多数项目强调自动推进，本框架保留共同设计。** 导师统一讨论入口和优先级；方法规划与结果分析持续与研究者讨论有研究意义的取舍。阶段和子任务由当前问题决定，最终独立文献审稿保持重点。

## 直接核读的材料

- autoresearch：[工作指令](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md)、[训练实现](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/train.py)。
- AutoResearchClaw：[阶段定义](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/researchclaw/pipeline/stages.py)、[人机协作](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/docs/HITL_GUIDE.md)、[文献实现](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/researchclaw/pipeline/stage_impls/_literature.py)、[审稿实现](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/researchclaw/pipeline/stage_impls/_review_publish.py)、[干预学习](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/researchclaw/hitl/learning.py)、[经验存储](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/researchclaw/evolution.py)。
- AI Scientist v2：[README](https://github.com/SakanaAI/AI-Scientist-v2/blob/96bd51617cfdbb494a9fc283af00fe090edfae48/README.md)、[主入口](https://github.com/SakanaAI/AI-Scientist-v2/blob/96bd51617cfdbb494a9fc283af00fe090edfae48/launch_scientist_bfts.py)，核看实验到图形、引用、写作、审稿的调用关系。
- EvoScientist：[README](https://github.com/EvoScientist/EvoScientist/blob/8a05cae32ec8d23a077eeba07030cf7ded2951b4/README.md)、[记忆中间件](https://github.com/EvoScientist/EvoScientist/blob/8a05cae32ec8d23a077eeba07030cf7ded2951b4/EvoScientist/middleware/memory.py)、[记忆工作角色](https://github.com/EvoScientist/EvoScientist/blob/8a05cae32ec8d23a077eeba07030cf7ded2951b4/EvoScientist/memory/agents/memory_worker.py)、[写作角色配置](https://github.com/EvoScientist/EvoScientist/blob/8a05cae32ec8d23a077eeba07030cf7ded2951b4/EvoScientist/subagents/writing.yaml)。
- FAROS：[README](https://github.com/OpenNSWM-Lab/FAROS/blob/4e4e96fde842ced39b5bfd805b5666b4ce7cca0e/README.md)，本次只作流程与审稿表达参考。

以上为静态阅读，代码中存在某一步不表示它运行可靠；宣传中的性能、接收结果和成本未在这里独立验证。本仓库不包含这些项目的运行系统。参考机制落实在[七个 Agent](../agents/README.md)、[轻量工作流](workflows.md)和[个性化机制](personalization.md)。

nnU-Net 作为完整方法和跨任务实证的单独参照，见[nnU-Net 的研究启发](nnunet-lessons.md)。
