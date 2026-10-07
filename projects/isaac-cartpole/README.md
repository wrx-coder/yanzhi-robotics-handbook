# Cartpole 训练闭环 · 环境验证、训练与检查点回放

用统一脚本执行官方任务的零动作验证、PPO 训练与显式检查点回放。

## 环境前提

已按官方说明完整安装 Isaac Lab v2.3.0、兼容 Isaac Sim/NVIDIA GPU/驱动及 RSL-RL。ISAACLAB_PATH 必须指向真实仓库绝对路径。此 ZIP 不包含大型运行时和资产。

## 实验原理

先验证仿真与任务重置，再引入强化学习训练，可将环境故障与算法问题分开定位。PPO 收集并行环境轨迹并迭代更新策略；检查点回放复用同一任务和网络接口。

## 使用步骤

### 1. 定位官方环境

把示例路径替换为本机真实仓库；describe 应对应 v2.3.0。安装 -i rsl_rl 安装该训练后端，可能需要联网。

```bash
export ISAACLAB_PATH=/absolute/path/IsaacLab
git -C "$ISAACLAB_PATH" describe --tags --always
"$ISAACLAB_PATH/isaaclab.sh" -i rsl_rl
```

### 2. 环境验证

check 使用 16 个环境运行零动作，验证模型加载、步进与重置；观察成功后 Ctrl+C。

```bash
bash run.sh check
```

### 3. 训练与记录

train 固定种子 42、64 个环境、150 次迭代，运行结果写入 IsaacLab/logs/rsl_rl/cartpole。先确认小规模运行，再增加预算。

```bash
bash run.sh train
find "$ISAACLAB_PATH/logs/rsl_rl/cartpole" -name "model_*.pt"
```

### 4. 显式回放

CHECKPOINT 必须替换为上一步实际生成的文件。默认 headless 用于运行验证；如需图形展示，可按官方 play 脚本移除 --headless 后运行。

```bash
export CHECKPOINT=/absolute/path/to/model_149.pt
bash run.sh play --checkpoint "$CHECKPOINT"
```

## 验收

零动作阶段无资产/设备异常；训练产生真实 TensorBoard 事件与 model_*.pt；同一任务回放可加载检查点且动作有限。150 次迭代不是性能保证，记录实际回合长度和奖励；绝不把未运行的示例标为训练成功。

## 验证记录

状态：静态检查通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

已检查 1 个 Python / Bash / XML / YAML 文件的语法；未启动目标软件或云端服务。

## 关联排障

在研知网站搜索以下条目 ID：

- isaac-error-driver
- isaac-error-asset
- isaac-error-memory
- isaac-error-checkpoint

## 官方参考

[Isaac Lab：强化学习脚本](https://isaac-sim.github.io/IsaacLab/v2.3.0/source/overview/reinforcement-learning/rl_existing_scripts.html)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
