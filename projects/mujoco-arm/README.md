# 二维机械臂 · Jacobian 逆解与闭环轨迹跟踪

包含两自由度 MJCF、阻尼最小二乘逆解、关节 PD 控制、轨迹 CSV 和误差验收。

## 环境前提

Python 3.10+、MuJoCo 3.3.7 与 NumPy。零重力二维教学模型，无碰撞和关节限位，仅测试平面内可达轨迹。

## 实验原理

末端速度近似为 J·dq，阻尼最小二乘 Jᵀ(JJᵀ+λI)⁻¹ 限制奇异附近的逆解增益。逆解使用独立 MjData，避免把目标解直接写入真实动力学状态；PD 力矩驱动真实关节跟随。

## 使用步骤

### 1. 准备与运行

requirements 固定引擎；track.py 从脚本旁加载 arm.xml，因此模型路径不依赖运行目录。CSV 输出到当前目录。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python track.py
```

### 2. 检查轨迹误差

metrics.json 保存去掉首秒瞬态后的 RMSE；CSV 同时保留目标、实际位置与逐步误差，可用任意绘图工具复查。

```bash
cat metrics.json
head -n 6 trajectory.csv
```

### 3. 建立对照实验

复制完整目录到新实验位置，再分别改变 PD 增益或阻尼项；每次只改变一个因素，避免直接覆盖上次轨迹。

```bash
python -c "import mujoco; print(mujoco.__version__)"
cp metrics.json metrics-baseline.json
cp trajectory.csv trajectory-baseline.csv
```

## 验收

应产生 3000 条轨迹记录，metrics.json 的 acceptance=true，首秒之后 RMSE < 0.03 m。程序超阈值会非零退出。此阈值是示例验收条件，不是所有机械臂系统的性能保证。

## 验证记录

状态：目标环境运行通过。日期：2026-09-21。环境：Linux x86_64 · Python / MuJoCo / NumPy：3.11.15 3.3.7 2.4.6。

CPU 无图形运行通过；3000 条轨迹，去掉首秒后的末端 RMSE=0.009382 m，小于 0.03 m 阈值。

## 关联排障

在研知网站搜索以下条目 ID：

- mujoco-error-name
- mujoco-error-shape
- mujoco-error-nan

## 官方参考

[MuJoCo：函数参考](https://mujoco.readthedocs.io/en/3.3.7/APIreference/APIfunctions.html)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
