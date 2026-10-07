# 自定义管理器任务 · 奖励、重置随机化与对照实验

提供可导入的配置类、Gymnasium 注册入口、训练包装器与 TensorBoard 对比脚本。

## 环境前提

Isaac Lab v2.3.0 + RSL-RL，环境要求同 Cartpole 实战。compare.py 需要训练环境中的 TensorBoard。ISAACLAB_PATH 为绝对路径。

## 实验原理

自定义配置继承官方 CartpoleEnvCfg，分别调整杆角度惩罚、滑车速度惩罚及初始状态分布。字符串入口先注册，实际类在 AppLauncher 后加载，避免过早导入仿真扩展。改变奖励后总回报不可直接跨任务比较，应在相同评估条件下衡量回合长度和失败率。

## 使用步骤

### 1. 定位与零动作验证

run.sh 调用 entry.py 注册 Research-Cartpole-Randomized-v0，然后运行官方 zero_agent。Ctrl+C 结束验证。

```bash
export ISAACLAB_PATH=/absolute/path/IsaacLab
bash run.sh check
```

### 2. 训练基线

在独立运行名保存官方任务；--seed 42 与自定义任务相同，预算和环境数也保持一致。命令在官方仓库工作目录启动，日志写入该仓库。

```bash
cd "$ISAACLAB_PATH"
./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Cartpole-v0 --num_envs 64 --max_iterations 150 --seed 42 --run_name baseline --headless
```

### 3. 训练自定义任务

重新进入解压的 isaac-randomized 目录后执行。使用 run_name 区分实验，注册任务的环境配置仍会保存到训练日志。

```bash
bash run.sh train --max_iterations 150 --seed 42 --run_name randomized
```

### 4. 对比真实曲线

把两个目录替换为刚刚生成的运行目录。compare.py 只读取真实事件文件；标签不存在时列出可用标签。尾部奖励只能描述各自训练进度，不能直接证明新奖励更好。

```bash
"$ISAACLAB_PATH/isaaclab.sh" -p compare.py /absolute/path/baseline_run /absolute/path/randomized_run --tag Train/mean_reward
```

### 5. 回放与复验

使用自定义注册入口回放对应检查点。随后用多个种子重复相同预算；要做单因素消融，应在 research_task.py 中一次仅修改一组配置并另存实验。

```bash
bash run.sh play --checkpoint /absolute/path/randomized_run/model_149.pt
```

## 验收

任务注册与零动作步进通过，env 配置能看到新奖励权重和重置范围；基线/自定义日志独立，比较脚本使用真实标量。当前同时修改奖励与重置分布属于流程演示，不能作为单因素因果结论。需补做固定评估分布、多种子与置信区间后报告科研结论。

## 验证记录

状态：静态检查通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

已检查 4 个 Python / Bash / XML / YAML 文件的语法；未启动目标软件或云端服务。

## 关联排障

在研知网站搜索以下条目 ID：

- isaac-error-task
- isaac-error-hydra
- isaac-error-reward
- isaac-error-nan

## 官方参考

[Isaac Lab：环境设计工作流](https://isaac-sim.github.io/IsaacLab/v2.3.0/source/overview/core-concepts/task_workflows.html)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
