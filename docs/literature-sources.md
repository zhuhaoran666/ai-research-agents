# 文献检索来源与领域选择

与[文献 Agent](../agents/literature.md)一起使用。**本文件是核心来源与各领域来源清单的唯一出处**，其他文档只引用、不复述；新增领域时在本文件按同样格式补一节。先查目标任务的已有方法、问题解决程度与局限，再调查用户的候选方法和跨领域迁移；以下来源用于实际检索，不是论文数量配额。

每轮调研：检索下面三个核心来源，并结合至少一个本领域来源。每个来源的结果状态分开记录（见文末“记录与核实”）。

## 三个核心来源：每轮调研必查

| 来源 | 检索入口 | 主要用途 |
|---|---|---|
| PaperNotes | [papernotes.org](https://papernotes.org/) | 检索相关解读，浏览会议、年份和领域分类，发现方法与迁移线索；关键判断回到原论文 |
| Google Scholar | [Scholar](https://scholar.google.com/) | 同问题方法、强基线、不同术语、引用与被引追踪，覆盖早期与近期工作 |
| arXiv | [arxiv.org](https://arxiv.org/) | 近期预印本、全文与版本更新；记录 ID、所读版本、日期和发表状态 |

**PaperNotes 的收录范围有限。** 2026-10-09 查看时，站点收录 2024–2026 年 13 个会议场次的 AI 辅助生成解读，主要是 CVPR、ICCV、ECCV、NeurIPS、ICML、ICLR、ACL、AAAI，**不含 MICCAI、ISBI、ICRA、IROS、CoRL、RSS**（以站点当前页面为准，收录会变化）。因此它主要用来发现相邻领域的方法线索；目标领域的会议不在其收录范围时，记为“来源不覆盖”而不是“未命中”，领域结论依靠下面的领域来源。解读由 AI 辅助生成，只用于发现和理解，关键机制、结果与局限回到原论文核实。

## 医学图像：必查会议与期刊

医学图像课题必须检索下列渠道，围绕任务关键词、同义词与相关机制查找；会议覆盖相关的近期及历年论文，期刊兼顾已发表文章与提前在线版本。

| 渠道 | 官方入口 | 调研重点 |
|---|---|---|
| MICCAI | [学会开放论文](https://miccai.org/publications/miccai-open-access-reviews/) · [Springer 历年论文集](https://link.springer.com/conference/miccai) | 医学图像计算方法、评价、数据与挑战；区分主会和 workshop |
| ISBI | [会议官网](https://biomedicalimaging.org/) · [IEEE Xplore](https://ieeexplore.ieee.org/) | 按会议全名与年份检索成像、分割、配准及结构分析工作；区分归档论文与摘要条目 |
| Medical Image Analysis（MIA / MedIA） | [ScienceDirect](https://www.sciencedirect.com/journal/medical-image-analysis) | 医学与生物图像分析方法、系统性实验与扩展验证 |
| IEEE Transactions on Medical Imaging（TMI） | [期刊官网](https://ieeetmi.org/) · [IEEE Xplore](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=42) | 医学成像、图像处理与分析的任务内方法与证据 |
| IEEE Transactions on Pattern Analysis and Machine Intelligence（TPAMI） | [IEEE Computer Society](https://www.computer.org/csdl/journal/tp) · [IEEE Xplore](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=34) | 相关视觉、模式识别与机器学习方法，支持跨领域迁移；其范围不限于医学图像 |

按问题补查 PubMed、其他期刊、作者原文与官方实现。以上渠道已经满足领域来源要求，不为满足数量另加网站，也不将这份名单当作完整文献范围。

## 具身智能与机器人：重点会议

具身智能或机器人课题优先检索 IROS、ICRA，并根据任务涉及的学习、控制、感知、规划或操作问题补查 RSS、CoRL 等会议。

| 渠道 | 官方入口 | 主要用途 |
|---|---|---|
| IROS | [IEEE RAS 会议入口](https://www.ieee-ras.org/conferences-workshops/financially-co-sponsored/iros) · [IEEE Xplore](https://ieeexplore.ieee.org/) | 智能机器人系统、感知、规划、控制及实际系统验证；按会议全名与年份检索 |
| ICRA | [IEEE RAS 会议入口](https://www.ieee-ras.org/conferences-workshops/fully-sponsored/icra) · [IEEE Xplore](https://ieeexplore.ieee.org/) | 机器人与自动化的方法、系统和实验；按会议全名与年份检索 |
| Robotics: Science and Systems（RSS） | [官方论文集](https://roboticsproceedings.org/) | 与任务相关的机器人基础方法与系统研究 |
| Conference on Robot Learning（CoRL） | [会议官网](https://www.corl.org/) · [PMLR 论文集](https://proceedings.mlr.press/) | 机器人学习、模仿学习、强化学习及泛化；由会议与年份定位对应论文集 |

任务需要时继续补查机器人期刊，以及 CVPR、ICCV、ECCV、NeurIPS、ICLR、ICML 等相关视觉与学习论文集。跨领域研究同时沿多个相关方向检索，不受单一领域分类限制。

## 其他领域

其他方向按问题选择适用的会议、期刊或数据库，并在本文件按上面两节的格式补一节（渠道、官方入口、调研重点）。尚未补充时，在研究笔记里如实记录实际使用的来源。

## 访问受限时的兜底

核心来源和领域来源有时无法直接访问。按下面的顺序补查，并如实记录实际用了什么；替代渠道不等于已完成该来源的站内检索。

1. **同一来源的其他入口**：会议官网或官方论文页面、开放获取版本、作者主页与官方代码仓库。
2. **目录型索引**（适合按会议与年份列出论文、追踪引用）：[OpenAlex](https://openalex.org/)、[Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)；医学与生物医学再加 [PubMed](https://pubmed.ncbi.nlm.nih.gov/) 或 [Europe PMC](https://europepmc.org/)（REST 接口 `https://www.ebi.ac.uk/europepmc/webservices/rest/search`）。2026-10-09 对 OpenAlex、Crossref 和 Europe PMC 接口的请求，返回的是 JSON。[Semantic Scholar](https://www.semanticscholar.org/product/api) 的匿名请求返回 429。[DBLP](https://dblp.org/) 的接口对脚本请求返回的是反机器人验证页（HTTP 200，`text/html`），不能当作可用接口，也不要绕过验证；需要 DBLP 的结果时请研究者在浏览器中查询。**判断接口是否可用要看 `Content-Type` 和响应内容，不能只看 HTTP 状态码。** 这些索引主要提供题录和引用关系，摘要与全文不一定齐全，需要时回到出版方或开放版本核读。匿名访问有速率限制。
3. **站点限定搜索与会议目录。**
4. **仍无法覆盖时**，告知研究者哪些来源未能检索及其影响，由研究者决定是否人工检索或接受当前范围。

已知的访问特点（会随站点变化）：

- **arXiv API 可能返回 429**（2026-10-09 实测）。arXiv 使用条款要求旧版接口（含 arXiv API）每 3 秒不超过一次请求，且同一时间只开一个连接，以[官方条款](https://info.arxiv.org/help/api/tou.html)为准。遇到 429 时降低频率并退避重试，或改用网页检索与列表页。
- **IEEE Xplore 页面由前端渲染**（2026-10-09 对 TMI 期刊页实测：静态 HTML 中没有论文列表）。ISBI、TMI、TPAMI、IROS、ICRA 的官方入口都包含 IEEE Xplore，同类页面很可能有同样情况，纯 HTTP 抓取通常拿不到列表；使用能渲染页面的工具，或改用目录型索引。
- **Google Scholar 的 `robots.txt` 对 `/scholar` 设置了 `Disallow`**（2026-10-09 核对）。agent 不对它做脚本化抓取：列出查询词，由研究者人工检索并把结果贴回，agent 再据此记录阅读深度并核读原文；未执行时在检索记录中写“未由 agent 检索”，不写成已检索。

## 记录与核实

在现有研究笔记中记录来源、日期、查询词或分类入口、覆盖年份和结果状态即可。每个来源的结果状态分四种，不混用：**命中**（有相关工作）、**未命中**（已检索但没有相关工作）、**访问失败**（无法完成检索，附实际尝试）、**来源不覆盖**（该来源不收录目标领域或会议）。筛读候选，精读支撑主要判断的原文章节；不要求所有命中文献全文阅读。PaperNotes 解读、检索命中、摘要阅读、原文精读分别说明。

记录预印本、会议版、期刊扩展版的关系与实际差异；不把同一工作的不同版本当作独立验证。访问受限、未命中与全文不可取得分开记录，按上面的兜底顺序补查，不把替代途径写成站内检索成功。

已有同问题检索可复用；新增疑问、缺少的必查渠道和重要近期进展增量补查即可。这份清单不要求每个链接或每次写作反馈重做整轮调研。
