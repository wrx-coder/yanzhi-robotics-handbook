# 最小仿真实验 · 从模型到控制与日志

无需图形窗口，建立有质量、惯量和执行器的单摆，完成 2 秒物理仿真并记录 CSV。

## 环境前提

Python 3.10+、mujoco==3.3.7、NumPy。CPU 即可，示例不打开 viewer 或离屏渲染。

## 实验原理

MJCF 编译为只读结构 MjModel，状态存入 MjData。每步先写入有限幅值力矩，再 mj_step 积分，最后记录仿真时间与更新后的状态。阻尼项消耗能量，正弦项持续激励系统。

## 使用步骤

### 1. 准备依赖

venv 隔离 Python 包；requirements.txt 固定 MuJoCo 引擎基线。安装阶段需要网络或预先准备的 wheel。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. 执行完整实验

mujoco_minimal.py 内嵌完整模型并运行 1000 个步长，每步 0.002 秒；没有隐藏的 robot.xml 或控制器。

```bash
python mujoco_minimal.py
```

### 3. 逐行验证日志

DictReader 按列名读取记录；断言验证样本数、结束时间和非有限状态。末行时间可能有浮点误差，因此用容差。

```bash
python - <<'PY'
import csv, math
rows=list(csv.DictReader(open('pendulum.csv')))
assert len(rows)==1000
assert abs(float(rows[-1]['time_s'])-2)<1e-8
assert all(math.isfinite(float(v)) for r in rows for v in r.values())
print('1000 条有限状态，2 秒仿真验收通过')
PY
```

## 验收

输出 pendulum.csv，1000 条数据加一行表头。角度、速度、力矩均有限；力矩限制在 ±2 N·m。日志可作为控制器修改前的基线，不把“可运行”当作控制效果最优。

## 验证记录

状态：目标环境运行通过。日期：2026-09-21。环境：Linux x86_64 · Python / MuJoCo / NumPy：3.11.15 3.3.7 2.4.6。

CPU 无图形运行通过；1000 条有限数值日志，最终仿真时间 2 秒。

## 关联排障

在研知网站搜索以下条目 ID：

- mujoco-error-import
- mujoco-error-nan
- mujoco-error-trajectory

## 官方参考

[MuJoCo：Python 接口](https://mujoco.readthedocs.io/en/3.3.7/python.html)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
