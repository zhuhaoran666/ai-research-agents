# 可运行的证据链演示

这里的四条预测记录全部为合成数据，只演示如何连接原始记录、评价输出、运行清单和报告中的数字，不代表真实研究结果。

在仓库根目录运行（Python 3.9+，无第三方依赖）：

```sh
python3 examples/evidence-demo/evaluate.py
python3 scripts/check_evidence.py examples/evidence-demo/manifest.json
```

第一条命令从四条 `predictions.json` 记录重新计算 accuracy，得到 `3 / 4 = 0.75`，并写入确定性的 `metrics.json`。第二条命令只检查清单、文件哈希、JSON 来源数值和声明记录的一致性；它不会运行评价代码，也不会自动从预测重算指标。报告中的对应句位于 `report.md` 第 5 行；检查器核对报告文件哈希及清单中的 `reported_value`，不解析自然语言句子。

`manifest.json` 默认以其所在目录为文件根。指定 `--root` 后，所有 artifact 路径都相对于指定根目录；检查器拒绝越界路径及指向根外的符号链接。`templates/run-manifest.example.json` 提供相同结构的项目模板，复制后必须更新路径、哈希、版本、状态和真实运行信息。

有基线清单时可增加 `--compare BASELINE_MANIFEST`，分别完整检查两次运行，再核对评价协议、选型范围、聚合方式、数据版本、切分 ID/文件哈希以及同名指标的定义、单位和方向。这些标识相同仍不足以证明科学比较公平。

清单中的 `validity` 是项目提供的检查记录；`passed` 必须至少有一条带 artifact 证据的通过检查。检查器不会证明这些检查确实执行、代码正确实现假设或数据没有泄漏。`budget` 是可为空的预算记录，不是计费器或进程限制器。计划中或失败运行可以保留空 `claims`；声明证据必须来自 `completed` 且 `validity.status=passed` 的运行。

修改任一 artifact 后，原清单应报错。确认这是合法的新版本、重新评价并记录原因后，才更新相应哈希；不要为消除报错而盲目重写哈希。这个演示不包含任何训练、外部任务或网络访问。
