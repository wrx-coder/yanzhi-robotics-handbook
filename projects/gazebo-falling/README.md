# 最小世界实验 · 重力、碰撞与 ROS 时钟

自包含 SDF 世界让球体落到地面，同时检查 Gazebo 传输和 ROS 仿真时间。

## 环境前提

Ubuntu 24.04 + 已安装 ROS 2 Jazzy。安装 ros-jazzy-ros-gz 将使用配套 Gazebo Harmonic。GUI 需要可用图形驱动，纯服务端可加 -s。

## 实验原理

Physics 系统在固定步长推进刚体，碰撞几何产生接触约束，SceneBroadcaster 为界面同步实体。/clock 是仿真时间，不等同于机器墙钟；ROS 桥接只转换消息，不推动物理。

## 使用步骤

### 1. 安装与启动 · 终端 1

apt 安装 ROS 对应桥接和 Gazebo；source 加载 ROS 工具。gz sim -r 加载随附世界并立即运行。

```bash
sudo apt install ros-jazzy-ros-gz
source /opt/ros/jazzy/setup.bash
gz sim -r world.sdf
```

### 2. 观察传输 · 终端 2

gz topic -l 枚举话题；-e 订阅时钟。此命令持续输出，检查后 Ctrl+C。若运行了多个世界，请选择列表中对应世界的 clock 话题。

```bash
gz topic -l
gz topic -e -t /clock
```

### 3. 桥接时钟 · 终端 3

引号中的 [ 表示 Gazebo 到 ROS 单向桥接，防止两个时钟互相回传。该桥接应持续运行。

```bash
source /opt/ros/jazzy/setup.bash
ros2 run ros_gz_bridge parameter_bridge "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"
```

### 4. 验证 ROS · 终端 4

echo --once 检查消息结构，hz 连续计算接收频率；检查后 Ctrl+C。

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic echo /clock --once
ros2 topic hz /clock
```

## 验收

球体由 z=1 下落并停在地面上方约自身半径处；仿真运行时时钟前进，暂停时停止。ROS /clock 存在且内容与仿真一致。结束时分别关闭桥接和 Gazebo 进程。

## 验证记录

状态：静态检查通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

已检查 1 个 Python / Bash / XML / YAML 文件的语法；未启动目标软件或云端服务。

## 关联排障

在研知网站搜索以下条目 ID：

- gazebo-error-gz-command
- gazebo-error-paused
- gazebo-error-clock

## 官方参考

[Gazebo：SDF 世界](https://gazebosim.org/docs/harmonic/sdf_worlds/)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
