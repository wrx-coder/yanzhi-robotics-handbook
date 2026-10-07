# 移动机器人闭环 · SLAM 建图、保存地图与 Nav2 导航

随附与差速实战相同的完整仿真文件，完成扫描建图、地图落盘、AMCL 定位和导航目标验收。

## 环境前提

Ubuntu 24.04、ROS 2 Jazzy、Harmonic；支持 GPU 雷达渲染。项目自包含机器人文件，无需先下载另一套 ZIP。每个终端先 source /opt/ros/jazzy/setup.bash 并进入本目录。

## 实验原理

SLAM 估计地图与 map→odom；导航阶段由 AMCL 维护该变换，不能让 SLAM 和 AMCL 同时争用。Nav2 根据全局地图规划、局部扫描避障并生成速度。prepare_config.py 从已安装的 Jazzy 完整配置派生本机器人参数，记录来源哈希以便复现。

## 使用步骤

### 1. 准备导航环境

安装完整 Nav2、SLAM、桥接、TF 工具及 YAML 解析。依赖应来自同一 Jazzy 软件源，保存 apt 版本可复现实验。

```bash
sudo apt install ros-jazzy-ros-gz ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox ros-jazzy-tf2-tools python3-yaml
source /opt/ros/jazzy/setup.bash
mkdir -p maps
dpkg-query -W ros-jazzy-navigation2 ros-jazzy-slam-toolbox
```

### 2. 仿真 · 终端 1

本目录 sim.sh 提供时钟、扫描、里程计与固定传感器外参；保持运行。

```bash
bash sim.sh
```

### 3. 建图 · 终端 2

加载本项目 slam.yaml，配置扫描话题与坐标帧。SLAM 持续接收扫描并发布地图。

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true "slam_params_file:=$PWD/slam.yaml"
```

### 4. 探索并保存 · 终端 3

先旋转扫描四周，再小幅移动增加视角；每段结束自动发零速度。等地图形成后 map_saver_cli 保存灰度地图与 YAML。

```bash
python3 drive.py --angular 0.3 --seconds 22
python3 drive.py --linear 0.15 --angular 0 --seconds 4
ros2 run nav2_map_server map_saver_cli -f "$PWD/maps/room" --ros-args -p use_sim_time:=true
ls -l maps/room.*
```

### 5. 切换定位导航 · 终端 2

用 Ctrl+C 停止 SLAM，保持 Gazebo 运行，再执行 navigate.sh。脚本检查地图，生成完整 Nav2 YAML 并启动 map_server、AMCL 与导航节点。不要同时运行两个 map→odom 发布者。

```bash
bash navigate.sh
```

### 6. 设定位姿并导航 · 终端 4

RViz 默认配置展示地图与导航控件。Fixed Frame 设为 map，用 2D Pose Estimate 在地图上设置仿真机器人的实际位置与朝向；激光和墙壁对齐后用 Nav2 Goal 发送房间内、非障碍区域的近距离目标。

```bash
ros2 launch nav2_bringup rviz_launch.py use_sim_time:=true
```

### 7. 验收 · 终端 3

检查生命周期为 active，action 存在；RViz 应显示路径且机器人到达目标。保留生成配置和 config-origin.json 与地图。

```bash
ros2 lifecycle get /planner_server
ros2 lifecycle get /controller_server
ros2 action info /navigate_to_pose
cat config-origin.json
```

## 验收

maps/room.yaml 与图像存在；停止 SLAM 后 AMCL 建立唯一 map→odom；Nav2 关键节点 active，一次可达目标返回成功，机器人静止后速度回零。导航性能需在目标环境实测；本示例没有预填成功轨迹或地图。

## 验证记录

状态：静态检查通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

已检查 7 个 Python / Bash / XML / YAML 文件的语法；未启动目标软件或云端服务。

## 关联排障

在研知网站搜索以下条目 ID：

- ros-error-nav
- ros-error-tf
- ros-error-clock
- gazebo-error-sensor

## 官方参考

[Nav2 官方文档](https://docs.nav2.org/)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
