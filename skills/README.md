# 角色技能索引

本系统为十个现有角色各维护一项主技能，另有协作入口和通用代码维护专长，共十二项。角色文件负责分工与交接，技能保存可复用方法；单项任务直接调用对应技能，不要求先启动整套科研流程。

## 每个 Agent 的主技能

| 框架角色 / Codex 角色 | 主技能 | 具体职责 |
|---|---|---|
| `mentor` / `research-mentor` | [research-mentor](research-mentor/SKILL.md) | 定位当前瓶颈、优先级、派工与连续交接 |
| `literature` / `research-literature` | [research-literature](research-literature/SKILL.md) | 最接近工作、强基线、反证与真实核读 |
| `method` / `research-method` | [research-method](research-method/SKILL.md) | 机制假设、区分性验证、公平协议与取舍 |
| `code` / `research-code` | [research-code](research-code/SKILL.md) | 真实实现、运行状态、恢复与复现产物 |
| `analysis` / `research-analysis` | [research-analysis](research-analysis/SKILL.md) | 原始复算、可比性、失败诊断与主张范围 |
| `writing` / `research-writing` | [research-paper-writing](research-paper-writing/SKILL.md) | 以真实材料组织论证、正文与图表叙事 |
| `reviewer` / `research-reviewer` | [research-reviewer](research-reviewer/SKILL.md) | 同版材料、独立派工、原报告与问题整合 |
| `review-writing` / `research-review-writing` | [research-review-writing](research-review-writing/SKILL.md) | 有定位的语言审校与科学含义保持 |
| `review-domain` / `research-review-domain` | [research-review-domain](research-review-domain/SKILL.md) | 原文和实际证据支持的研究与论证审查 |
| `review-redundancy` / `research-review-redundancy` | [research-review-redundancy](research-review-redundancy/SKILL.md) | 按请求检测冗余，或交付保持原意的精简稿 |

## 协作入口与代码维护

- [ai-research-workflow](ai-research-workflow/SKILL.md)：根据当前材料连接所需角色、共享证据和交接；不重复执行导师或专家的全部工作。
- [readable-code-engineer](readable-code-engineer/SKILL.md)：可读代码、轻量环境、渐进重构和维护入口。科研实现由 `research-code` 按需组合，普通工程可单独使用。

## 加载、复用与移植

从当前问题选择一项主技能，只加载其任务所需参考。纯语言润色、完整综述、专业统计、成像研究与文件制作可按需复用本机已有专长；不叠加所有技能的流程，也不改动其他个人技能。

单项技能复制整个目录，保留实际存在的 `SKILL.md`、`agents/`、`references/` 和 `assets/`。角色主技能能独立使用；写作来源记录按需读取。协作入口通过相邻目录连接角色技能，移植该入口时需一并携带本次会用到的角色目录。代码维护模板按项目适配，不覆盖已有约定。

仓库内角色加载见[共享入口](../agents/README.md)。客户端须使用自己的技能发现或显式文件加载机制；文件存在不等于角色已启动，格式校验不等于行为或科学有效性得到验证。

以本仓库为分发源，修改后同步安装副本并核对资源、路径和角色绑定。用户当前要求与项目约定优先；复用已有授权，保留科研判断、数据和资源边界，不新增永久进程或对外发布权限。私人档案、研究数据与未获许可的来源全文不进入技能包。
