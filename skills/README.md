# 框架自有 Skill

Skill 保存可复用的工作方法；Agent 角色负责分工、协作和独立判断。本目录属于本研究框架，不要求使用框架外的 Skill。

| Skill | 何时使用 | 配套材料 |
|---|---|---|
| [research-paper-writing](research-paper-writing/SKILL.md) | AI 论文的起草、重组、修订与对应审稿任务；按当前章节与角色选择动作 | [来源学习记录](research-paper-writing/references/source-notes.md)、仓库内的[中文写作规则](../docs/chinese-academic-writing.md) |

## 怎样加载与移植

在当前仓库中，给相应角色加载 `skills/research-paper-writing/SKILL.md` 与任务材料即可；细分职责见[角色加载清单](../agents/README.md)。来源笔记用于理解和追溯学习依据，需要时再读，不要求每次整份加载。已有共享规则与本 Skill 复用同一原则，不新建审批或固定写作阶段。

跨工具移植时携带整个 `research-paper-writing/` 文件夹，保留 `SKILL.md` 与 `references/` 的相对路径。入口包含独立使用所需的核心动作，来源记录用于参考；科研事实仍要核读当前课题原文。依目标工具的 Skill 目录或显式文件加载机制使用，不能仅因文件存在就声称运行器已自动发现。

本次仅创建仓库内 Skill 并接入角色指令；未安装到全局 Skill 目录，未下载或执行外部 Skill。写作策略来自有限案例的归纳，效果需后续真实任务检验；新反馈按 [RSI](../docs/rsi.md)修订，并保留 Git 版本。
