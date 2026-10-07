# 差速机器人 · 激光雷达、里程计与 ROS 桥接

完整离线房间、轮式机器人、GPU 激光雷达、双向指令与单向传感器桥接，可直接用于下一套建图实战。

## 环境前提

Ubuntu 24.04、ROS 2 Jazzy、Gazebo Harmonic，支持 Ogre2 的图形环境。只在该仿真中运行速度示例。所有模型由本地几何组成。

## 实验原理

差速插件将线速度和角速度转换为左右轮角速度；轮径与轮距决定运动学比例。激光雷达通过渲染射线测距。Gazebo 发布 odom→base_link，静态 TF 补齐 base_link→laser_frame，bridge 转换时间、扫描、里程计和速度类型。

## 使用步骤

### 1. 准备依赖

ros-gz 提供桥接和配套 Gazebo；tf2-ros 提供静态坐标发布器。检查 source 后当前 ROS_DISTRO 应为 jazzy。

```bash
sudo apt install ros-jazzy-ros-gz ros-jazzy-tf2-ros
source /opt/ros/jazzy/setup.bash
printf "%s\n" "$ROS_DISTRO"
```

### 2. 启动系统 · 终端 1

sim.sh 启动世界、桥接和静态 TF；任何子进程退出都会清理其他子进程。无 GUI 的支持环境可传 -s --headless-rendering，但 GPU 雷达仍需渲染能力。

```bash
bash sim.sh
```

### 3. 传感器检查 · 终端 2

检查 scan 的 frame_id 为 laser_frame，TF 连通且时钟在前进。tf2_echo 持续输出，用 Ctrl+C 结束后执行下一条。

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic echo /scan --once --field header
ros2 run tf2_ros tf2_echo odom laser_frame
ros2 topic echo /odom --once
```

### 4. 小范围运动 · 终端 2

drive.py 发布有限时长速度并在结束时发送零速度。原地旋转便于观察扫描变化；短距离前进用于检查里程计符号。

```bash
python3 drive.py --angular 0.3 --seconds 5
python3 drive.py --linear 0.15 --angular 0 --seconds 3
```

## 验收

scan 约 10 Hz，odom 约 30 Hz；odom→base_link→laser_frame 连通。前进测试后 odom 位置变化约 0.45 m（受加减速影响）；雷达边界与房间一致。Ctrl+C sim.sh 后三类进程均被清理。

## 验证记录

状态：静态检查通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

已检查 4 个 Python / Bash / XML / YAML 文件的语法；未启动目标软件或云端服务。

## 关联排障

在研知网站搜索以下条目 ID：

- gazebo-error-drive
- gazebo-error-sensor
- gazebo-error-bridge
- ros-error-tf

## 官方参考

[ros_gz_bridge 官方源码与用法](https://github.com/gazebosim/ros_gz/tree/jazzy/ros_gz_bridge)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
