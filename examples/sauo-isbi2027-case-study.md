# SAUO 项目案例：医学图像分割论文的完整协作
## 2026-10-09 至 2026-10-12

这是一个真实的多智能体 AI 协作案例，展示了从接手已有项目、审计实验数据、设计关键实验、到准备投稿的完整流程。

## 项目背景

**研究课题**：左心房（LA）和左心耳（LAA）的 CT 分割，重点在两个结构的接触面几何质量

**起始状态**：
- 已完成的实验：15+ 个配置，包括 nnU-Net 基线和多个方法变体
- 交接文档：冻结了主表和消融表，列出了"排除"的对照臂
- 投稿目标：ISBI 2027，截稿日 2026-10-26（距离协作开始 17 天）

**协作目标**：审核实验完整性，补齐关键实验，确定投稿方案

## 协作流程

### 第 1 阶段：接收和初步审计（Day 1）

**任务**：理解项目状态，识别潜在问题

**角色**：`mentor` + `analysis`

**执行**：
1. 阅读交接文档（`handoff_gt_mesh_20260919.md`）
2. 检查所有实验的 per_case.csv 结果文件
3. 对比"冻结"的表格与实际数据
4. 检查训练日志、checkpoint 和配置文件

**发现的问题**：
- 主表 nnU-Net 基线（seed 1）是 293 轮早停版本
- 服务器上有标准 1000 轮训练的 nnU-Net，结果明显更强
- 交接文档将 MatchedDual 列为"排除"，但它是重要的表示消融
- 缺少验证"组合效应"的关键实验

**初步建议**：
```
1. 重新评估基线选择
2. 补齐 2×2 消融表（表示 × 接触损失）
3. 根据补充实验结果，准备两个投稿方案
```

### 第 2 阶段：深度数据审计（Day 2）

**任务**：定量评估方法的真实增益和新颖性

**角色**：`analysis` + `literature`

**审计维度**：

1. **基线强度检查**
   ```python
   # 对比两个 nnU-Net 版本
   seed1_laa_dice = 93.56%  # 293 轮早停
   seed0_laa_dice = 95.57%  # 1000 轮标准
   
   # SAUO 对不同基线的增益
   vs_seed1: +2.43 pt (+2.6%)
   vs_seed0: +0.42 pt (+0.4%)
   ```

2. **表示消融完整性**
   ```
   Historical Ours (双 SDF 父网络)  → LAA HD95: 1.61 mm
   + MatchedDual (独立双场)        → 1.07 mm  (主要增益)
   + u/d 表示 (SAUO no-contact)    → 1.07 mm  (无改善)
   + 接触损失 (SAUO full)          → 1.03 mm  (小改善)
   ```
   
   **关键发现**：u/d 表示本身增益为零

3. **MatchedDual 与 SAUO 的对比**
   所有 8 项指标的差异 < 0.04 mm（临床上不可区分）

4. **局部改进定位**
   按"到接触面的距离"分档，验证方法在目标区域的改进

**文献检索**：
- 启动子代理检索 LA/LAA 分割和接触面相关工作
- 识别新颖性威胁：BraTS 的层级分解、region-based 训练
- 对比评估指标和基线选择

### 第 3 阶段：关键实验设计（Day 2-3）

**任务**：设计能够回答核心问题的实验

**角色**：`method` + `code`

**核心问题**：
> 接触损失（L_c）是否需要 u/d 表示的拓扑约束才能工作？

**实验设计**：MatchedDual + L_c
- **如果失败（L_c 无效）** → 强故事：三层协同设计
- **如果成功（L_c 有效）** → 弱故事：有效的局部监督

**实现挑战**：
1. 第一次训练时出现 `FloatingPointError: Nonfinite independent dual objective`
2. 原因：接触损失和 SDF 损失可能产生冲突梯度
3. 解决：分两阶段训练
   - 阶段 1：只有 SDF 损失，验证基础稳定性
   - 阶段 2：加入接触损失，从小权重开始

**代码实现**：
```python
def contact_loss_dual(fields, label, spacing):
    """Contact loss for independent dual fields.
    
    KEY EXPERIMENT: does contact supervision work on independent fields,
    or does it require the u/d representation's topological constraint?
    """
    phi_la, phi_laa = fields.float().split(1, dim=1)
    
    # Find reference contact voxels
    contact = ((left == LA) & (right == LAA)) | \
              ((left == LAA) & (right == LA))
    
    # Midpoint penalty: sum should be ~0 at contact
    sum_l = la_l + laa_l
    sum_r = la_r + laa_r
    midpoint = F.smooth_l1_loss(0.5 * (sum_l + sum_r), zeros)
    
    # Union-inside penalty: both fields slightly negative
    union_inside = F.relu(0.25 * step + 0.5 * (la_l + la_r)) + \
                   F.relu(0.25 * step + 0.5 * (laa_l + laa_r))
    
    return (midpoint + union_inside).mean()
```

**实验监控**：
- 使用 `Monitor` 工具实时跟踪训练进度
- 每 60 秒检查 `state.json` 中的 epoch 和 loss
- 捕获错误和异常，及时调整

### 第 4 阶段：工具和脚本开发（Day 3）

**任务**：自动化后续的评估和表格生成

**角色**：`code`

**创建的工具**：

1. **regenerate_table1.py**
   - 自动重新生成主表
   - 使用 1000-epoch nnU-Net 基线
   - Bootstrap 置信区间（20,000 重采样，固定种子）
   - 生成 LaTeX 格式输出

2. **regenerate_table2.py**
   - 智能生成消融表
   - 根据 MatchedDual + L_c 结果自动选择故事版本
   - 支持两种叙事：强组合效应 vs 有效监督
   
   ```python
   # 故事选择逻辑
   if abs(mdc_effect) < 0.02:
       story = "strong"  # L_c 需要 u/d
   elif abs(mdc_vs_sauo) < 0.02:
       story = "weak"    # L_c 在两种表示都有效
   else:
       story = "mixed"   # 需要进一步解释
   ```

3. **batch_evaluate.sh**
   - 统一的评估流水线
   - 从服务器导出预测 → 本地网格评估
   - 避免服务器磁盘空间问题

4. **update_dual_objective_with_contact.sh**
   - 一键更新目标函数
   - 准备在基础训练完成后立即启动

### 第 5 阶段：文档和方案准备（Day 3-4）

**任务**：整理发现，准备投稿方案

**角色**：`writing` + `reviewer`

**生成的文档**：

1. **idea_review_20261012.md**（9 页）
   - 完整的 Idea 审计报告
   - 定量证据链
   - 识别的问题和风险
   - 两个投稿方案的详细对比

2. **experiment_status_20261012.md**
   - 所有实验的状态追踪
   - 完成 ✅ / 进行中 🔄 / 待补充 ❌
   - 数据文件位置和访问方式

3. **action_plan_20261012.md**
   - 14 天投稿倒计时计划
   - 每日检查清单
   - 风险缓解措施
   - 成功标准定义

4. **collaboration_summary_20261012.md**
   - 协作复盘和经验总结
   - 技术亮点和挑战
   - 对未来项目的建议

**两个投稿方案**：

**方案 A：强故事（组合效应）**
```
贡献：三层协同设计
1. u/d 表示：硬约束保证互斥
2. 分离的 union/partition 目标
3. 局部接触监督（需要 u/d 的拓扑约束）

证据：MatchedDual + L_c ≈ MatchedDual（L_c 无效）
     SAUO (u/d + L_c) > SAUO no-contact（组合有效）
```

**方案 B：弱故事（有效监督）**
```
贡献：轻量几何 head + 局部监督
1. 8338 参数达到接近最优性能
2. 接触面监督改善分界质量
3. u/d 参数化提供互斥保证

证据：MatchedDual + L_c ≈ SAUO（L_c 在两种表示都有效）
```

## 协作成果

### 量化指标

- **协作时间**：4 天（2026-10-09 至 10-12）
- **对话轮数**：~150 轮
- **审计实验**：15+ 个配置
- **发现问题**：3 个 major, 10+ minor
- **生成文档**：4 个主要报告（共约 30 页）
- **创建脚本**：4 个自动化工具
- **设计实验**：1 个关键实验（MatchedDual + L_c）

### 关键成就

1. **避免了弱基线投稿**
   - 发现 seed 1 基线偏弱
   - 建议使用 1000-epoch 标准基线
   - 虽然增益变小，但更可信

2. **明确了方法的真实贡献**
   - u/d 表示本身：零增益
   - 主要增益来源：几何监督 head
   - 需要验证的：组合效应

3. **设计了决定性实验**
   - MatchedDual + L_c 将回答核心问题
   - 准备好两个投稿方案
   - 降低了投稿风险

4. **建立了可重现的流程**
   - 所有脚本固定随机种子
   - Bootstrap CI 可重现
   - 评估流水线标准化

## 技术亮点

### 1. 分布式实验管理

**挑战**：
- 服务器在远程 GPU 集群
- 磁盘空间受限（AFS）
- 本地和服务器数据需同步

**方案**：
- `mirror/` 目录定期同步关键代码
- 评估分离：服务器导出预测，本地做网格评估
- 结果统一管理在 `results/` 目录

### 2. 实验监控自动化

使用 `Monitor` 工具实时监控：
```python
Monitor({
    command: 'ssh server "while sleep 60; do cat state.json; done"',
    description: 'MatchedDual training progress',
    timeout_ms: 1800000
})
```

**监控的内容**：
- Epoch 进度和 loss 变化
- 错误捕获（KeyError, FloatingPointError）
- 里程碑通知（epoch 5, 训练完成）

### 3. 统计分析的严谨性

**Bootstrap 置信区间**：
```python
def bootstrap_ci(values, n_boot=20000, seed=20261003):
    rng = np.random.RandomState(seed)  # 固定种子
    n = len(values)
    boots = [rng.choice(values, n, replace=True).mean() 
             for _ in range(n_boot)]
    return np.percentile(boots, [2.5, 97.5])
```

**配对检验**：
- SAUO full vs no-contact 的配对差值
- 判断显著性：CI 是否包含 0
- 多重比较校正（Bonferroni）

### 4. 智能表格生成

根据实验结果自动选择故事版本：
```python
if experiments["matched_dual_contact"] is None:
    # 等待关键实验
    generate_template()
else:
    # 分析结果，选择故事
    effect = analyze_contact_effect()
    if effect == "synergy":
        generate_strong_story_table()
    else:
        generate_weak_story_table()
```

## 遇到的挑战

### 挑战 1：训练不稳定

**问题**：MatchedDual + L_c 第一次训练出现 `FloatingPointError`

**根因**：独立双场 + 接触损失可能产生冲突梯度

**解决**：
1. 分阶段训练：先只用 SDF 损失验证稳定性
2. 监控前 10 轮，及时发现异常
3. 从小的接触损失权重开始

### 挑战 2：服务器磁盘满

**问题**：Boundary parent val100 评估完成，但写入失败

**错误**：`OSError: [Errno 28] No space left on device`

**应对**：
1. 评估结果导出到 `/tmp`
2. 立即下载到本地
3. 后续评估改为本地执行

### 挑战 3：数据完整性问题

**发现**：
- 部分实验的 summary.json 与实际 checkpoint 不匹配
- Region-based 和 boundary-loss nnUNet 缺少 val100
- 父网络的训练细节未充分记录

**应对**：
- 逐一核对 checkpoint 路径和训练日志
- 补齐缺失的评估
- 文档化父网络的完整训练过程

## 框架应用的经验

### 角色分工

**实际使用**：主会话按任务顺序使用不同角色指令

| 阶段 | 主要角色 | 次要角色 |
|------|---------|---------|
| 接收审计 | `mentor` | `analysis` |
| 数据审计 | `analysis` | `literature`（子代理）|
| 实验设计 | `method` | `code` |
| 工具开发 | `code` | - |
| 文档准备 | `writing` | `reviewer` |

### 有效的做法

1. **持久化关键信息**
   ```
   Memory 系统记录：
   - sauo-paper-state-2026-10.md：项目状态
   - sauo-project-server-access.md：服务器访问
   - subagent-model-routing.md：模型路由问题
   ```

2. **文档驱动协作**
   - 每个阶段生成 Markdown 报告
   - 脚本包含详细注释
   - 决策点记录在文档中

3. **工具自动化**
   - 避免重复性工作
   - 固定随机种子保证可重现
   - 标准化评估流水线

### 需要改进的地方

1. **更早的实验设计审查**
   - 如果在训练前就参与，可以避免部分返工
   - MatchedDual 应该在 SAUO 之前就作为对照

2. **版本控制**
   - 实验代码和配置应该用 Git 管理
   - Checkpoint 应该记录对应的代码版本

3. **文档先行**
   - 实验设计文档应该在训练前完成
   - 而非事后整理

## 对使用者的建议

### 1. 接手已有项目时

```markdown
检查清单：
□ 理解"冻结"决定的依据
□ 核对所有"排除"对照臂的理由
□ 验证基线是否使用标准设置
□ 检查每个声称的贡献是否有对照
□ 建立统一的名称表
```

### 2. 设计关键实验时

```markdown
原则：
- 一次只改变一个因素
- 补齐 2×2 或更完整的消融表
- 设计能够回答"为什么"的实验
- 准备多个故事版本应对不同结果
```

### 3. 投稿准备时

```markdown
两手准备：
- 强故事：需要更强的证据
- 弱故事：更保守但更容易站住脚
- 根据实验结果快速切换
- 不要等到最后一刻才决定
```

## 文件结构

```
SAUO_work/
├── results/                        # 所有实验的 per_case.csv
│   ├── nnunet_seed0_per_case.csv  # 1000-epoch 基线
│   ├── nnunet_seed1_per_case.csv  # 293-epoch 弱基线
│   ├── sauo_full_per_case.csv     # 主方法
│   ├── sauo_nocontact_per_case.csv # 消融
│   └── matched_dual_test100_per_case.csv
├── mirror/                         # 服务器代码镜像
├── figs/                          # Figure 渲染
├── paper_isbi2027/                # LaTeX 源文件
├── scripts/                       # 自动化脚本
│   ├── regenerate_table1.py
│   ├── regenerate_table2.py
│   ├── batch_evaluate.sh
│   └── update_dual_objective_with_contact.sh
├── predictions/                   # 导出的预测
├── docs/                          # 文档
│   ├── idea_review_20261012.md
│   ├── experiment_status_20261012.md
│   ├── action_plan_20261012.md
│   └── collaboration_summary_20261012.md
└── lit_review/                    # 文献检索结果
```

## 后续工作

**立即（24 小时内）**：
1. 检查 MatchedDual no-contact 训练完成
2. 启动 MatchedDual + L_c 训练
3. 修复 boundary parent 评估结果

**短期（1 周内）**：
1. 完成所有 test100 评估
2. 根据结果选择投稿方案
3. 重新生成表格和 figures
4. 改写论文主要部分

**中期（2 周内，截稿前）**：
1. 论文完整改写
2. 内部审校
3. LaTeX 排版
4. EDAS 提交

## 总结

这个案例展示了多智能体协作在真实科研项目中的应用：

**AI 的贡献**：
- 系统性审计大量实验数据
- 快速识别问题和设计解决方案
- 自动化重复性工作
- 保持严谨的科学标准

**人的作用**：
- 提供项目背景和目标
- 在关键决策点给予指导
- 确认实验设计和投稿方案
- 把控最终的科学判断

**协作的价值**：
- 4 天完成了通常需要 2-3 周的审计和准备工作
- 避免了弱基线和不完整消融的投稿
- 为 14 天内完成投稿奠定了基础
- 建立了可重现的工作流程

这次协作证明了：AI 可以成为科研过程中的可靠伙伴，但需要研究者在关键环节的参与和判断。框架的设计目标——"人在回路"的协作——在实践中得到了验证。
