"""项目说明与网页条目同源；可运行文件保存在 projects/。"""
import json
from build import ROOT, MODULES, SOURCES

PROJECTS=[]


def project(module, slug, directory, title, summary, principle, prerequisites, source, steps, acceptance, errors, advanced=False):
    report_path=ROOT/'data/project-validation.json'
    reports=json.loads(report_path.read_text()) if report_path.exists() else {}
    verification=reports.get(directory,dict(status='未运行',date='2026-09-21',environment='待验证',evidence='尚未执行本项目检查。'))
    entry=dict(id=f'{module}-{slug}',module=module,title=title,category='完整实战',kind='实战',
        version=next(m['version'] for m in MODULES if m['id']==module),level='进阶' if advanced else '基础',
        summary=summary,principle=principle,prerequisites=prerequisites,source=source,
        code=steps[0][2],language='bash',explain=[s[1] for s in steps],
        pitfall='按顺序逐步验证；持续运行的服务要在独立终端启动。命令默认在解压后的项目根目录执行，终端编号标在步骤标题中。下载包含完整项目文件，运行依赖需另行安装。',
        sections=[dict(title=t,body=b,code=c) for t,b,c in steps[1:]]+[dict(title='验收与结果解释',body=acceptance)],
        related=errors,project=dict(directory=directory,verification=verification,acceptance=acceptance))
    if module in ['ros','gazebo']:
        entry['version']='Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic' if advanced or module=='gazebo' else 'Ubuntu 24.04 · ROS 2 Jazzy'
    PROJECTS.append(entry)
    lines=[f'# {title}',summary,'## 环境前提',prerequisites,'## 实验原理',principle,'## 使用步骤']
    for i,(title_,body,code) in enumerate(steps,1):
        lines += [f'### {i}. {title_}',body,'```bash\n'+code+'\n```']
    lines += ['## 验收',acceptance,'## 验证记录',f"状态：{verification['status']}。日期：{verification['date']}。环境：{verification['environment']}。\n\n{verification['evidence']}",
              '## 关联排障','在研知网站搜索以下条目 ID：\n\n'+'\n'.join('- '+x for x in errors),
              '## 官方参考',f'[{SOURCES[source][0]}]({SOURCES[source][1]})',
              '## 文件与复现','本目录中的代码为完整示例；README 与网页由同一说明源生成。外部依赖按上述固定版本准备。输出数据不随网站分发，需实际运行生成。修改参数后使用新输出目录，保留命令、版本、种子、日志与配置。']
    (ROOT/'projects'/directory/'README.md').write_text('\n\n'.join(lines)+'\n')


project('linux','experiment','linux-experiment','远程实验流程 · 独立环境、日志与归档',
 '运行随附的线性回归程序，隔离 Python 环境，用 tmux 管理会话并归档真实结果。',
 '梯度下降在合成数据上拟合 y=2x+1。固定种子控制采样；虚拟环境隔离依赖；Bash pipefail 将训练失败传递到流水线；tee 同时写入日志并显示输出；tar 将配置与结果打包。',
 'Ubuntu 22.04 / 24.04，Python 3.10+、python3-venv、tmux、tar。训练本身只用 Python 标准库，无 GPU 要求。','python',[
 ('准备独立环境','apt 安装虚拟环境支持与会话工具；venv 创建本目录环境；source 让当前 shell 的 python3 指向该环境。','sudo apt install python3-venv tmux\npython3 -m venv .venv\nsource .venv/bin/activate\npython3 --version'),
 ('启动并保留会话','tmux new 创建 research 会话；在新会话中 run.sh 调用真实 train.py，按时间与进程号建立输出目录，并在成功后归档。Ctrl+B 后按 D 可离开会话；完成后输入 exit 关闭空闲会话。','tmux new -s research\nsource .venv/bin/activate\nbash run.sh'),
 ('重新连接与检查','attach 连接仍在运行的会话；训练很快，若会话已退出则无需重连。find 列出结果；检查 JSON 中 loss 与两个拟合参数，并保留 tar.gz。','tmux attach -t research\nfind runs -maxdepth 2 -type f\ncat runs/*/result.json')],
 '每次运行生成 metrics.csv（200 行数据）、result.json、日志及 tar.gz。默认种子下 loss 应低于 0.01，weight 接近 2、bias 接近 1。归档解压后应含同一结果目录和日志。',
 ['linux-error-command','linux-error-permission','linux-error-module'])

project('linux','sweep','linux-sweep','多种子实验 · 参数扫描、失败记录与指标汇总',
 '对两档学习率和三个种子执行六次真实实验，保留失败退出码、日志及统计摘要。',
 '每组参数由独立子进程执行，避免随机状态串扰。汇总表保留成功与失败两类记录；均值和样本标准差仅使用成功数据，同时报告失败数量，避免把失败实验悄悄丢弃。',
 'Python 3.10+，仅标准库。目录中已包含 train.py；在可写的新输出目录运行。','bash',[
 ('完整参数扫描','sweep.py 按固定参数表顺序启动六个子进程。--output 必须是不存在的目录，防止覆盖旧实验。','python3 sweep.py --output sweep-results\ncat sweep-results/summary.csv\ncat sweep-results/aggregate.json'),
 ('验证失败记录','--fail-seed 1 为两个 seed=1 实验注入非法学习率。其余实验继续完成，进程最后返回 1，代表该扫描存在失败。紧接着 echo $? 读取退出码；不要在其间执行其他命令。','python3 sweep.py --output sweep-with-failure --fail-seed 1\necho $?\ncat sweep-with-failure/summary.csv'),
 ('保存可复现结果','tar 归档全部分组日志与配置结果。查看失败日志应能追溯明确异常，而不是只看到汇总里的 failed。','cat sweep-with-failure/lr0.03-seed1.log\ntar -czf sweep-results.tar.gz sweep-results')],
 '正常扫描：summary.csv 有 6 条 ok，aggregate.json 有 2 组统计。注入失败：4 条 ok、2 条 failed，两个失败日志明确指出学习率非法，程序退出码为 1。统计可复现意味着保留种子、配置、失败比例与环境，而不是只复制一个均值。',
 ['linux-error-space','linux-error-oom','linux-error-permission'],True)

project('mujoco','quickstart','mujoco-pendulum','最小仿真实验 · 从模型到控制与日志',
 '无需图形窗口，建立有质量、惯量和执行器的单摆，完成 2 秒物理仿真并记录 CSV。',
 'MJCF 编译为只读结构 MjModel，状态存入 MjData。每步先写入有限幅值力矩，再 mj_step 积分，最后记录仿真时间与更新后的状态。阻尼项消耗能量，正弦项持续激励系统。',
 'Python 3.10+、mujoco==3.3.7、NumPy。CPU 即可，示例不打开 viewer 或离屏渲染。','mj-python',[
 ('准备依赖','venv 隔离 Python 包；requirements.txt 固定 MuJoCo 引擎基线。安装阶段需要网络或预先准备的 wheel。','python3 -m venv .venv\nsource .venv/bin/activate\npython -m pip install -r requirements.txt'),
 ('执行完整实验','mujoco_minimal.py 内嵌完整模型并运行 1000 个步长，每步 0.002 秒；没有隐藏的 robot.xml 或控制器。','python mujoco_minimal.py'),
 ('逐行验证日志','DictReader 按列名读取记录；断言验证样本数、结束时间和非有限状态。末行时间可能有浮点误差，因此用容差。',"python - <<'PY'\nimport csv, math\nrows=list(csv.DictReader(open('pendulum.csv')))\nassert len(rows)==1000\nassert abs(float(rows[-1]['time_s'])-2)<1e-8\nassert all(math.isfinite(float(v)) for r in rows for v in r.values())\nprint('1000 条有限状态，2 秒仿真验收通过')\nPY")],
 '输出 pendulum.csv，1000 条数据加一行表头。角度、速度、力矩均有限；力矩限制在 ±2 N·m。日志可作为控制器修改前的基线，不把“可运行”当作控制效果最优。',
 ['mujoco-error-import','mujoco-error-nan','mujoco-error-trajectory'])

project('mujoco','arm-project','mujoco-arm','二维机械臂 · Jacobian 逆解与闭环轨迹跟踪',
 '包含两自由度 MJCF、阻尼最小二乘逆解、关节 PD 控制、轨迹 CSV 和误差验收。',
 '末端速度近似为 J·dq，阻尼最小二乘 Jᵀ(JJᵀ+λI)⁻¹ 限制奇异附近的逆解增益。逆解使用独立 MjData，避免把目标解直接写入真实动力学状态；PD 力矩驱动真实关节跟随。',
 'Python 3.10+、MuJoCo 3.3.7 与 NumPy。零重力二维教学模型，无碰撞和关节限位，仅测试平面内可达轨迹。','mj-api',[
 ('准备与运行','requirements 固定引擎；track.py 从脚本旁加载 arm.xml，因此模型路径不依赖运行目录。CSV 输出到当前目录。','python3 -m venv .venv\nsource .venv/bin/activate\npython -m pip install -r requirements.txt\npython track.py'),
 ('检查轨迹误差','metrics.json 保存去掉首秒瞬态后的 RMSE；CSV 同时保留目标、实际位置与逐步误差，可用任意绘图工具复查。','cat metrics.json\nhead -n 6 trajectory.csv'),
 ('建立对照实验','复制完整目录到新实验位置，再分别改变 PD 增益或阻尼项；每次只改变一个因素，避免直接覆盖上次轨迹。','python -c "import mujoco; print(mujoco.__version__)"\ncp metrics.json metrics-baseline.json\ncp trajectory.csv trajectory-baseline.csv')],
 '应产生 3000 条轨迹记录，metrics.json 的 acceptance=true，首秒之后 RMSE < 0.03 m。程序超阈值会非零退出。此阈值是示例验收条件，不是所有机械臂系统的性能保证。',
 ['mujoco-error-name','mujoco-error-shape','mujoco-error-nan'],True)

project('gazebo','quickstart','gazebo-falling','最小世界实验 · 重力、碰撞与 ROS 时钟',
 '自包含 SDF 世界让球体落到地面，同时检查 Gazebo 传输和 ROS 仿真时间。',
 'Physics 系统在固定步长推进刚体，碰撞几何产生接触约束，SceneBroadcaster 为界面同步实体。/clock 是仿真时间，不等同于机器墙钟；ROS 桥接只转换消息，不推动物理。',
 'Ubuntu 24.04 + 已安装 ROS 2 Jazzy。安装 ros-jazzy-ros-gz 将使用配套 Gazebo Harmonic。GUI 需要可用图形驱动，纯服务端可加 -s。','gz-world',[
 ('安装与启动 · 终端 1','apt 安装 ROS 对应桥接和 Gazebo；source 加载 ROS 工具。gz sim -r 加载随附世界并立即运行。','sudo apt install ros-jazzy-ros-gz\nsource /opt/ros/jazzy/setup.bash\ngz sim -r world.sdf'),
 ('观察传输 · 终端 2','gz topic -l 枚举话题；-e 订阅时钟。此命令持续输出，检查后 Ctrl+C。若运行了多个世界，请选择列表中对应世界的 clock 话题。','gz topic -l\ngz topic -e -t /clock'),
 ('桥接时钟 · 终端 3','引号中的 [ 表示 Gazebo 到 ROS 单向桥接，防止两个时钟互相回传。该桥接应持续运行。','source /opt/ros/jazzy/setup.bash\nros2 run ros_gz_bridge parameter_bridge "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"'),
 ('验证 ROS · 终端 4','echo --once 检查消息结构，hz 连续计算接收频率；检查后 Ctrl+C。','source /opt/ros/jazzy/setup.bash\nros2 topic echo /clock --once\nros2 topic hz /clock')],
 '球体由 z=1 下落并停在地面上方约自身半径处；仿真运行时时钟前进，暂停时停止。ROS /clock 存在且内容与仿真一致。结束时分别关闭桥接和 Gazebo 进程。',
 ['gazebo-error-gz-command','gazebo-error-paused','gazebo-error-clock'])

project('gazebo','diffdrive-project','gazebo-diffdrive','差速机器人 · 激光雷达、里程计与 ROS 桥接',
 '完整离线房间、轮式机器人、GPU 激光雷达、双向指令与单向传感器桥接，可直接用于下一套建图实战。',
 '差速插件将线速度和角速度转换为左右轮角速度；轮径与轮距决定运动学比例。激光雷达通过渲染射线测距。Gazebo 发布 odom→base_link，静态 TF 补齐 base_link→laser_frame，bridge 转换时间、扫描、里程计和速度类型。',
 'Ubuntu 24.04、ROS 2 Jazzy、Gazebo Harmonic，支持 Ogre2 的图形环境。只在该仿真中运行速度示例。所有模型由本地几何组成。','gz-bridge',[
 ('准备依赖','ros-gz 提供桥接和配套 Gazebo；tf2-ros 提供静态坐标发布器。检查 source 后当前 ROS_DISTRO 应为 jazzy。','sudo apt install ros-jazzy-ros-gz ros-jazzy-tf2-ros\nsource /opt/ros/jazzy/setup.bash\nprintf "%s\\n" "$ROS_DISTRO"'),
 ('启动系统 · 终端 1','sim.sh 启动世界、桥接和静态 TF；任何子进程退出都会清理其他子进程。无 GUI 的支持环境可传 -s --headless-rendering，但 GPU 雷达仍需渲染能力。','bash sim.sh'),
 ('传感器检查 · 终端 2','检查 scan 的 frame_id 为 laser_frame，TF 连通且时钟在前进。tf2_echo 持续输出，用 Ctrl+C 结束后执行下一条。','source /opt/ros/jazzy/setup.bash\nros2 topic echo /scan --once --field header\nros2 run tf2_ros tf2_echo odom laser_frame\nros2 topic echo /odom --once'),
 ('小范围运动 · 终端 2','drive.py 发布有限时长速度并在结束时发送零速度。原地旋转便于观察扫描变化；短距离前进用于检查里程计符号。','python3 drive.py --angular 0.3 --seconds 5\npython3 drive.py --linear 0.15 --angular 0 --seconds 3')],
 'scan 约 10 Hz，odom 约 30 Hz；odom→base_link→laser_frame 连通。前进测试后 odom 位置变化约 0.45 m（受加减速影响）；雷达边界与房间一致。Ctrl+C sim.sh 后三类进程均被清理。',
 ['gazebo-error-drive','gazebo-error-sensor','gazebo-error-bridge','ros-error-tf'],True)

project('ros','quickstart','ros-pubsub','双终端实验 · 完整 ROS 2 发布订阅功能包',
 '从真实 ament_python 包构建 talker/listener，验证节点发现、消息类型和 2 Hz 通信。',
 'ament 资源索引决定包可见性，console_scripts 将 Python 函数安装为 ros2 run 可执行入口。rclpy executor 调度定时器与订阅回调，DDS 按消息类型和 QoS 建立通信。',
 'Ubuntu 24.04 + ROS 2 Jazzy；包含 src/research_pubsub 的完整工作空间。每个新终端都需加载发行版及该工作空间。','ros2',[
 ('构建工作空间','apt 安装 colcon 与消息依赖；colcon 从 src 发现包，--symlink-install 便于开发。source install/setup.bash 将安装索引加入当前环境。','sudo apt install python3-colcon-common-extensions ros-jazzy-rclpy ros-jazzy-std-msgs\nsource /opt/ros/jazzy/setup.bash\ncolcon build --symlink-install\nsource install/setup.bash\nros2 pkg executables research_pubsub'),
 ('发布 · 终端 1','talker 每 0.5 秒发布递增编号字符串。进程保持运行，Ctrl+C 结束。','ros2 run research_pubsub talker'),
 ('订阅 · 终端 2','在项目根目录开启新终端并加载环境，listener 回调打印收到的同一编号。','source /opt/ros/jazzy/setup.bash\nsource install/setup.bash\nros2 run research_pubsub listener'),
 ('验收 · 终端 3','node list 检查两个节点；topic info 确认类型与端点；hz 检查持续频率后 Ctrl+C。','source /opt/ros/jazzy/setup.bash\nsource install/setup.bash\nros2 node list\nros2 topic info /chatter --verbose\nros2 topic hz /chatter')],
 '可执行入口包含 talker/listener；两个节点可见，listener 接收“实验样本 N”，频率约 2 Hz。新增数据字段时应定义消息类型并更新依赖，不把任意对象塞进不匹配的消息。',
 ['ros-error-package','ros-error-dependency','ros-error-qos','ros-error-domain'])

project('ros','navigation-project','ros-navigation','移动机器人闭环 · SLAM 建图、保存地图与 Nav2 导航',
 '随附与差速实战相同的完整仿真文件，完成扫描建图、地图落盘、AMCL 定位和导航目标验收。',
 'SLAM 估计地图与 map→odom；导航阶段由 AMCL 维护该变换，不能让 SLAM 和 AMCL 同时争用。Nav2 根据全局地图规划、局部扫描避障并生成速度。prepare_config.py 从已安装的 Jazzy 完整配置派生本机器人参数，记录来源哈希以便复现。',
 'Ubuntu 24.04、ROS 2 Jazzy、Harmonic；支持 GPU 雷达渲染。项目自包含机器人文件，无需先下载另一套 ZIP。每个终端先 source /opt/ros/jazzy/setup.bash 并进入本目录。','nav2',[
 ('准备导航环境','安装完整 Nav2、SLAM、桥接、TF 工具及 YAML 解析。依赖应来自同一 Jazzy 软件源，保存 apt 版本可复现实验。','sudo apt install ros-jazzy-ros-gz ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox ros-jazzy-tf2-tools python3-yaml\nsource /opt/ros/jazzy/setup.bash\nmkdir -p maps\ndpkg-query -W ros-jazzy-navigation2 ros-jazzy-slam-toolbox'),
 ('仿真 · 终端 1','本目录 sim.sh 提供时钟、扫描、里程计与固定传感器外参；保持运行。','bash sim.sh'),
 ('建图 · 终端 2','加载本项目 slam.yaml，配置扫描话题与坐标帧。SLAM 持续接收扫描并发布地图。','ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true "slam_params_file:=$PWD/slam.yaml"'),
 ('探索并保存 · 终端 3','先旋转扫描四周，再小幅移动增加视角；每段结束自动发零速度。等地图形成后 map_saver_cli 保存灰度地图与 YAML。','python3 drive.py --angular 0.3 --seconds 22\npython3 drive.py --linear 0.15 --angular 0 --seconds 4\nros2 run nav2_map_server map_saver_cli -f "$PWD/maps/room" --ros-args -p use_sim_time:=true\nls -l maps/room.*'),
 ('切换定位导航 · 终端 2','用 Ctrl+C 停止 SLAM，保持 Gazebo 运行，再执行 navigate.sh。脚本检查地图，生成完整 Nav2 YAML 并启动 map_server、AMCL 与导航节点。不要同时运行两个 map→odom 发布者。','bash navigate.sh'),
 ('设定位姿并导航 · 终端 4','RViz 默认配置展示地图与导航控件。Fixed Frame 设为 map，用 2D Pose Estimate 在地图上设置仿真机器人的实际位置与朝向；激光和墙壁对齐后用 Nav2 Goal 发送房间内、非障碍区域的近距离目标。','ros2 launch nav2_bringup rviz_launch.py use_sim_time:=true'),
 ('验收 · 终端 3','检查生命周期为 active，action 存在；RViz 应显示路径且机器人到达目标。保留生成配置和 config-origin.json 与地图。','ros2 lifecycle get /planner_server\nros2 lifecycle get /controller_server\nros2 action info /navigate_to_pose\ncat config-origin.json')],
 'maps/room.yaml 与图像存在；停止 SLAM 后 AMCL 建立唯一 map→odom；Nav2 关键节点 active，一次可达目标返回成功，机器人静止后速度回零。导航性能需在目标环境实测；本示例没有预填成功轨迹或地图。',
 ['ros-error-nav','ros-error-tf','ros-error-clock','gazebo-error-sensor'],True)

project('isaac','quickstart','isaac-cartpole','Cartpole 训练闭环 · 环境验证、训练与检查点回放',
 '用统一脚本执行官方任务的零动作验证、PPO 训练与显式检查点回放。',
 '先验证仿真与任务重置，再引入强化学习训练，可将环境故障与算法问题分开定位。PPO 收集并行环境轨迹并迭代更新策略；检查点回放复用同一任务和网络接口。',
 '已按官方说明完整安装 Isaac Lab v2.3.0、兼容 Isaac Sim/NVIDIA GPU/驱动及 RSL-RL。ISAACLAB_PATH 必须指向真实仓库绝对路径。此 ZIP 不包含大型运行时和资产。','il-train',[
 ('定位官方环境','把示例路径替换为本机真实仓库；describe 应对应 v2.3.0。安装 -i rsl_rl 安装该训练后端，可能需要联网。','export ISAACLAB_PATH=/absolute/path/IsaacLab\ngit -C "$ISAACLAB_PATH" describe --tags --always\n"$ISAACLAB_PATH/isaaclab.sh" -i rsl_rl'),
 ('环境验证','check 使用 16 个环境运行零动作，验证模型加载、步进与重置；观察成功后 Ctrl+C。','bash run.sh check'),
 ('训练与记录','train 固定种子 42、64 个环境、150 次迭代，运行结果写入 IsaacLab/logs/rsl_rl/cartpole。先确认小规模运行，再增加预算。','bash run.sh train\nfind "$ISAACLAB_PATH/logs/rsl_rl/cartpole" -name "model_*.pt"'),
 ('显式回放','CHECKPOINT 必须替换为上一步实际生成的文件。默认 headless 用于运行验证；如需图形展示，可按官方 play 脚本移除 --headless 后运行。','export CHECKPOINT=/absolute/path/to/model_149.pt\nbash run.sh play --checkpoint "$CHECKPOINT"')],
 '零动作阶段无资产/设备异常；训练产生真实 TensorBoard 事件与 model_*.pt；同一任务回放可加载检查点且动作有限。150 次迭代不是性能保证，记录实际回合长度和奖励；绝不把未运行的示例标为训练成功。',
 ['isaac-error-driver','isaac-error-asset','isaac-error-memory','isaac-error-checkpoint'])

project('isaac','randomized-project','isaac-randomized','自定义管理器任务 · 奖励、重置随机化与对照实验',
 '提供可导入的配置类、Gymnasium 注册入口、训练包装器与 TensorBoard 对比脚本。',
 '自定义配置继承官方 CartpoleEnvCfg，分别调整杆角度惩罚、滑车速度惩罚及初始状态分布。字符串入口先注册，实际类在 AppLauncher 后加载，避免过早导入仿真扩展。改变奖励后总回报不可直接跨任务比较，应在相同评估条件下衡量回合长度和失败率。',
 'Isaac Lab v2.3.0 + RSL-RL，环境要求同 Cartpole 实战。compare.py 需要训练环境中的 TensorBoard。ISAACLAB_PATH 为绝对路径。','il-env',[
 ('定位与零动作验证','run.sh 调用 entry.py 注册 Research-Cartpole-Randomized-v0，然后运行官方 zero_agent。Ctrl+C 结束验证。','export ISAACLAB_PATH=/absolute/path/IsaacLab\nbash run.sh check'),
 ('训练基线','在独立运行名保存官方任务；--seed 42 与自定义任务相同，预算和环境数也保持一致。命令在官方仓库工作目录启动，日志写入该仓库。','cd "$ISAACLAB_PATH"\n./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Cartpole-v0 --num_envs 64 --max_iterations 150 --seed 42 --run_name baseline --headless'),
 ('训练自定义任务','重新进入解压的 isaac-randomized 目录后执行。使用 run_name 区分实验，注册任务的环境配置仍会保存到训练日志。','bash run.sh train --max_iterations 150 --seed 42 --run_name randomized'),
 ('对比真实曲线','把两个目录替换为刚刚生成的运行目录。compare.py 只读取真实事件文件；标签不存在时列出可用标签。尾部奖励只能描述各自训练进度，不能直接证明新奖励更好。','"$ISAACLAB_PATH/isaaclab.sh" -p compare.py /absolute/path/baseline_run /absolute/path/randomized_run --tag Train/mean_reward'),
 ('回放与复验','使用自定义注册入口回放对应检查点。随后用多个种子重复相同预算；要做单因素消融，应在 research_task.py 中一次仅修改一组配置并另存实验。','bash run.sh play --checkpoint /absolute/path/randomized_run/model_149.pt')],
 '任务注册与零动作步进通过，env 配置能看到新奖励权重和重置范围；基线/自定义日志独立，比较脚本使用真实标量。当前同时修改奖励与重置分布属于流程演示，不能作为单因素因果结论。需补做固定评估分布、多种子与置信区间后报告科研结论。',
 ['isaac-error-task','isaac-error-hydra','isaac-error-reward','isaac-error-nan'],True)

project('github','research-release','github-release','科研发布流程 · 从实验分支到论文版本',
 '使用真实可运行 train.py 演练本地提交、实验分支、PR 说明与带标签的发布。',
 '提交固定源码快照，分支指向一条实验历史，PR 记录变更和验证，标签将论文引用绑定到明确提交。数据产物与代码版本分别归档，避免把不断变动的默认分支当成论文版本。',
 'Git、Python 3.10+；远程步骤另需 GitHub 账号、已安装并登录 gh、有权限的仓库。先修改示例维护者信息。脚本不会自动创建仓库或推送。','gh-flow',[
 ('本地实验与提交','执行完整训练生成结果；git init 创建本地仓库，git add 只暂存指定源码与说明，避免误提交实验产物。首次 commit 前需已配置自己的 Git 身份。','python3 train.py --output runs/baseline\ngit init -b main\ngit add train.py README.md PR.md RELEASE.md .gitignore\ngit commit -m "建立可复现实验基线"'),
 ('实验分支','switch 创建独立分支；执行不同种子并记录结果到 PR.md。修改说明后提交，使后续 PR 有明确可审查内容。','git switch -c experiment/seed-check\npython3 train.py --seed 7 --output runs/seed7\ncat runs/seed7/result.json\n# 编辑 PR.md，填写真实对比结果\ngit add PR.md\ngit commit -m "记录种子对照实验"'),
 ('远程 PR · 由你在目标仓库执行','OWNER/REPO 替换为自己的空仓库。添加 origin 后分别推送 main 和当前分支；gh pr create 会真的向 GitHub 创建 PR，因此先核对仓库和 PR.md。','git remote add origin https://github.com/OWNER/REPO.git\ngit push -u origin main\ngit push -u origin experiment/seed-check\ngh pr create --base main --title "记录种子对照实验" --body-file PR.md'),
 ('合并后发布','PR 按仓库规则完成审查合并后，切回 main 并只接受快进更新。检查提交，再建立注解标签；push 标签和 gh release create 都作用于真实远程。','git switch main\ngit pull --ff-only\ngit log -1 --oneline\ngit tag -a v0.1.0 -m "科研实验基线 v0.1.0"\ngit push origin v0.1.0\ngh release create v0.1.0 --verify-tag --notes-file RELEASE.md')],
 '本地 train.py 生成有限结果且 loss < 0.01；分支提交可追溯。远程验收需真实 PR 已合并、标签对应预期提交、Release 说明记录环境与结果。本网站构建过程没有创建远程 PR 或 Release。',
 ['github-error-ssh','github-error-nonfast','github-error-protected'])

project('github','ci-project','github-ci','科研代码自动化 · Python 测试矩阵与标签发布',
 '完整指标代码、三个单元测试、双 Python 版本 CI 和仅标签触发的 Release 工作流。',
 'CI 在干净 Runner 上重建环境并测试数学结果与异常边界；矩阵检验 Python 兼容性。发布 job 先运行测试，再归档 HEAD，并用受限于标签事件的写权限创建 Release。PR 验证仅有只读权限。',
 '本地 Python 3.10+、Git；远端需你有权限的 GitHub 仓库且 Actions 已启用。工作流 actions/checkout@v4、setup-python@v5 是固定主版本入口，严格供应链复现时可自行审计并锁定提交 SHA。','gh-actions',[
 ('本地完整测试','unittest discover 从 tests 发现测试，覆盖已知数值、相同输入和非法输入；不需要下载第三方 Python 包。','python3 -m unittest discover -s tests -v'),
 ('加入已有仓库','把本项目文件放到目标仓库根目录；确认 .github 隐藏目录也被复制。git add 只暂存相关文件，远程 push 会触发 main 或 PR 检查。','git add research_math.py tests .github README.md RELEASE.md .gitignore\ngit commit -m "添加科研指标测试和发布流程"\ngit push'),
 ('检查矩阵执行','gh run list 显示运行，view --log-failed 定位失败步骤。只有远端两个 Python job 均通过才能声称云端矩阵验证通过。','gh run list --limit 5\ngh run view --log-failed'),
 ('标签触发发布','确认在已通过审查和测试的提交上；创建此前未使用的版本标签，推送触发 release.yml。工作流使用 RELEASE.md 并附上当前提交的 ZIP。','git tag -a v0.1.0 -m "指标与测试首版"\ngit push origin v0.1.0\ngh release view v0.1.0')],
 '本地输出 Ran 3 tests / OK。云端矩阵覆盖 Python 3.10 与 3.12；标签发布应出现 research-code.zip。远端工作流未由网站构建代为执行，首次使用需在自己的仓库核实权限与分支策略。',
 ['github-error-actions','github-error-ci','github-error-actions-permission'],True)

assert len(PROJECTS)==12
(ROOT/'data/projects.json').write_text(json.dumps(PROJECTS,ensure_ascii=False,indent=2)+'\n')
print('已生成 12 套实战说明与网页条目')
