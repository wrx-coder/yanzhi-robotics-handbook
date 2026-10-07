# 双终端实验 · 完整 ROS 2 发布订阅功能包

从真实 ament_python 包构建 talker/listener，验证节点发现、消息类型和 2 Hz 通信。

## 环境前提

Ubuntu 24.04 + ROS 2 Jazzy；包含 src/research_pubsub 的完整工作空间。每个新终端都需加载发行版及该工作空间。

## 实验原理

ament 资源索引决定包可见性，console_scripts 将 Python 函数安装为 ros2 run 可执行入口。rclpy executor 调度定时器与订阅回调，DDS 按消息类型和 QoS 建立通信。

## 使用步骤

### 1. 构建工作空间

apt 安装 colcon 与消息依赖；colcon 从 src 发现包，--symlink-install 便于开发。source install/setup.bash 将安装索引加入当前环境。

```bash
sudo apt install python3-colcon-common-extensions ros-jazzy-rclpy ros-jazzy-std-msgs
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 pkg executables research_pubsub
```

### 2. 发布 · 终端 1

talker 每 0.5 秒发布递增编号字符串。进程保持运行，Ctrl+C 结束。

```bash
ros2 run research_pubsub talker
```

### 3. 订阅 · 终端 2

在项目根目录开启新终端并加载环境，listener 回调打印收到的同一编号。

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run research_pubsub listener
```

### 4. 验收 · 终端 3

node list 检查两个节点；topic info 确认类型与端点；hz 检查持续频率后 Ctrl+C。

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 node list
ros2 topic info /chatter --verbose
ros2 topic hz /chatter
```

## 验收

可执行入口包含 talker/listener；两个节点可见，listener 接收“实验样本 N”，频率约 2 Hz。新增数据字段时应定义消息类型并更新依赖，不把任意对象塞进不匹配的消息。

## 验证记录

状态：静态检查通过。日期：2026-09-21。环境：Linux x86_64 · Python 3.10.12。

已检查 4 个 Python / Bash / XML / YAML 文件的语法；未启动目标软件或云端服务。

## 关联排障

在研知网站搜索以下条目 ID：

- ros-error-package
- ros-error-dependency
- ros-error-qos
- ros-error-domain

## 官方参考

[ROS 2 Jazzy 官方教程](https://docs.ros.org/en/jazzy/Tutorials.html)

## 文件与复现

本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。
