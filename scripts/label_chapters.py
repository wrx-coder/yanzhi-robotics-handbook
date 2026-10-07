"""人工中文目录映射。顺序对应已冻结的官方目录快照，长度检查避免错位。"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
unmapped=json.loads((ROOT/'data/chapter-unmapped.json').read_text())
labels={}


def fill(group, translations):
    keys=[k for k in unmapped if k.startswith(group+'|')]
    values=[v.strip() for v in translations.strip().split('¦')]
    assert len(keys)==len(values),(group,len(keys),len(values))
    for key,value in zip(keys,values):labels[key]={'title':value,'entries':[]}


fill('mujoco-nav','''引擎概览¦计算原理¦流体力¦模型构建¦XML 元素参考¦编程指南¦物理仿真¦可视化¦用户界面¦程序化模型编辑¦代码示例¦扩展机制¦API 参考¦数据类型¦函数接口¦全局变量¦Python 接口¦MuJoCo XLA 加速¦MuJoCo Warp 加速¦Warp API 参考¦Unity 插件¦OpenUSD 集成¦构建 OpenUSD 插件¦mjcPhysics 物理模式¦文件格式插件¦导入模型¦导出模型¦模型示例库¦版本变更''')
fill('gazebo-nav','''开始使用¦安装指南¦Ubuntu 二进制安装¦macOS 二进制安装¦Windows 二进制安装¦Ubuntu 源码安装¦macOS 源码安装¦Windows 源码安装¦安装排障¦ROS 与 Gazebo 配套安装¦ROS 2 的 Gazebo 供应包¦仿真教程¦构建自己的机器人¦驱动机器人¦SDF 世界¦传感器¦动画角色¦理解图形界面¦操作模型¦从 Fuel 插入模型¦键盘快捷键¦生成 URDF 模型¦实践指南¦ROS 2 集成概览¦从 ROS 2 启动 Gazebo¦使用 ROS 2 与 Gazebo 交互¦ROS 2 仿真接口交互¦使用 ROS 2 生成模型¦ROS 2 互操作性¦ROS 2 集成项目模板¦网页可视化¦仿真架构¦各组件库实践指南¦Gazebo 包持续集成¦发展路线¦开发指南¦参与贡献¦维护者指南¦持续集成¦发布流程¦发布操作说明¦版本功能¦发行版本¦项目治理¦Fuel 资源平台¦内容删除政策¦贡献新模型¦贡献新世界¦版权说明¦数据与隐私政策¦合理使用说明¦使用 Gazebo 的项目¦支持渠道¦从 Ignition 迁移¦功能对比¦Gazebo Classic 迁移¦Gazebo 11 与新版共存安装¦ROS 2 Classic 项目迁移¦组件库参考¦CMake 构建库¦通用工具库¦Fuel 工具库¦图形界面库¦启动管理库¦数学计算库¦消息定义库¦物理引擎库¦插件库¦渲染库¦传感器库¦仿真核心库¦命令行工具库¦传输通信库¦辅助工具库¦SDFormat 格式库''')
fill('isaac-nav','''Isaac Lab 生态系统¦本地安装¦使用 Isaac Sim Pip 包安装¦使用 Isaac Sim 预编译包安装¦使用 Isaac Sim 源码安装¦使用 Isaac Lab Pip 包安装¦资产缓存¦容器部署¦Docker 指南¦通过 Docker 运行示例¦集群指南¦在 Kubernetes 部署 CloudXR 遥操作¦云端部署¦参考架构¦快速入门¦创建自己的项目或任务¦创建新项目或任务¦项目目录结构¦逐步入门¦环境设计背景¦类与配置¦环境设计¦训练 Jetbot：真值观测¦探索强化学习问题¦教程总览¦创建空场景¦在场景中生成对象¦深入 AppLauncher¦添加新机器人¦与刚体交互¦与关节机构交互¦与可变形物体交互¦与表面夹爪交互¦使用交互场景¦创建管理器式基础环境¦创建管理器式强化学习环境¦创建直接式强化学习环境¦注册环境¦使用强化学习智能体训练¦配置强化学习智能体¦修改已有直接式环境¦在 USD 环境中推理策略¦向机器人添加传感器¦使用任务空间控制器¦使用操作空间控制器¦实践指南¦导入新资产¦编写资产配置¦固定物理对象¦生成多种资产¦保存渲染图像与三维重投影¦估算相机数量与配置¦配置渲染设置¦创建可视化标记¦封装环境¦接入自己的学习库¦录制仿真动画¦录制训练视频¦课程学习工具¦面向机器人的 Omniverse 使用¦配置 CloudXR 遥操作¦仿真性能与调优¦优化场景创建¦开发者指南¦配置 Visual Studio Code¦仓库组织¦扩展开发¦核心概念¦任务设计工作流¦执行器¦传感器¦运动生成器¦可用环境¦强化学习¦强化学习运行脚本¦强化学习库比较¦性能基准¦调试与训练指南¦模仿学习¦使用 Isaac Lab Mimic 遥操作与模仿学习¦增强模仿学习¦SkillGen 自动生成演示¦展示示例¦简单智能体¦Hydra 配置系统¦多 GPU 与多节点训练¦种群训练¦平铺渲染¦Ray 任务分发与调参¦可复现性与确定性¦实验性前沿功能¦Newton 物理集成¦Newton 安装¦Newton 训练环境¦Newton 可视化¦Newton 使用限制¦求解器切换¦仿真间策略迁移¦策略迁移到真实机器人¦部署 Isaac Lab 训练的真实机器人策略¦训练并部署 HOVER 策略¦输入输出描述符入门¦从 IsaacGymEnvs 迁移¦从 OmniIsaacGymEnvs 迁移¦从 Orbit 迁移¦API 参考¦应用启动接口¦执行器接口¦资产接口¦控制器接口¦交互设备接口¦环境接口¦管理器接口¦可视化标记接口¦场景接口¦传感器接口¦仿真接口¦地形接口¦辅助工具接口¦马尔可夫决策过程接口¦环境界面接口¦传感器采样模式接口¦资产转换接口¦物理模式接口¦场景生成接口¦强化学习封装接口¦模仿学习数据生成接口¦模仿学习环境接口¦任务工具接口¦扩展资源¦贡献指南¦技巧与排障¦Isaac Sim 迁移指南¦已知问题¦发行说明¦扩展变更日志¦许可说明¦参考文献''')
fill('coreutils','''手册介绍¦通用选项¦备份选项¦块大小¦信号表示¦用户名与数值标识的区分¦随机数据来源¦目标目录¦末尾斜杠¦遍历符号链接¦根目录特殊处理¦特殊内建工具¦退出状态¦浮点数¦标准兼容性¦coreutils 多调用程序¦输出完整文件¦cat：连接并输出文件¦tac：逆序输出文件¦nl：添加行号¦od：以八进制等格式查看数据¦base32：可打印编码¦base64：可打印编码¦basenc：通用编码转换¦格式化文件内容¦fmt：重排段落¦pr：分页与分栏¦fold：按宽度换行¦输出部分文件¦head：输出文件开头¦tail：输出文件末尾¦split：拆分文件¦csplit：按上下文拆分文件¦文件摘要¦wc：统计行词与字节¦sum：校验与块计数¦cksum：计算与验证校验和¦md5sum：MD5 摘要¦b2sum：BLAKE2 摘要¦sha1sum：SHA-1 摘要¦SHA-2 摘要工具¦处理有序文件¦sort：文本排序¦shuf：随机排列¦uniq：去除相邻重复行¦comm：逐行比较有序文件¦ptx：生成排列索引¦tsort：拓扑排序¦按字段处理¦cut：提取行内字段¦paste：合并文件行¦join：按公共字段连接¦按字符处理¦tr：替换压缩与删除字符¦expand：制表符转空格¦unexpand：空格转制表符¦目录列表¦ls：列出目录内容¦dir：简洁目录列表¦vdir：详细目录列表¦dircolors：配置列表颜色¦基本文件操作¦cp：复制文件与目录¦dd：转换并复制数据¦install：复制并设置属性¦mv：移动和重命名¦rm：移除文件与目录¦shred：更安全地覆盖文件¦特殊文件类型¦link：创建硬链接¦ln：创建文件链接¦mkdir：创建目录¦mkfifo：创建命名管道¦mknod：创建块与字符设备¦readlink：读取链接目标¦rmdir：移除空目录¦unlink：移除文件链接¦修改文件属性¦chown：修改所有者与组¦chgrp：修改所属组¦chmod：修改访问权限¦touch：修改时间戳¦文件空间使用¦df：文件系统空间¦du：估算文件空间¦stat：文件与文件系统状态¦sync：同步缓存写入¦truncate：调整文件长度¦输出文本¦echo：输出文本行¦printf：格式化输出¦yes：重复输出字符串¦条件判断¦false：返回失败¦true：返回成功¦test：文件属性与值比较¦expr：计算表达式¦输出重定向¦tee：分发输出到文件与进程¦文件名处理¦basename：提取基本文件名¦dirname：提取目录部分¦pathchk：检查路径有效性¦mktemp：创建临时文件¦realpath：解析规范路径¦工作环境¦pwd：当前工作目录¦stty：终端属性¦printenv：环境变量¦tty：终端设备名¦用户信息¦id：用户身份¦logname：登录名¦whoami：有效用户名¦groups：所属用户组¦users：当前登录用户¦who：登录会话¦pinky：用户信息¦系统环境¦date：日期与时间¦arch：硬件架构¦nproc：可用处理器数¦uname：系统信息¦hostname：主机名¦hostid：主机数值标识¦uptime：运行时间与负载¦SELinux 安全上下文¦chcon：修改安全上下文¦runcon：指定上下文执行¦改变命令执行环境¦chroot：改变根目录执行¦env：修改环境执行¦nice：调整调度优先级¦nohup：忽略挂断信号¦stdbuf：修改流缓冲¦timeout：限定执行时间¦进程控制¦kill：发送进程信号¦延时操作¦sleep：等待指定时间¦数值操作¦factor：质因数分解¦numfmt：数值格式化¦seq：生成数字序列¦文件权限¦文件时间戳¦组合软件工具''')
fill('findutils','''手册介绍¦范围¦工具概览¦查找文件¦find 表达式¦搜索起点¦名称匹配¦链接处理¦时间匹配¦大小匹配¦类型匹配¦所有者匹配¦权限位¦内容匹配¦目录处理¦文件系统¦组合条件与运算符¦执行动作¦输出文件名¦输出文件信息¦运行命令¦删除文件¦添加测试条件¦文件名数据库¦数据库位置¦数据库格式¦换行符处理¦文件权限¦配置¦叶节点优化¦目录类型优化¦命令参考¦调用 find¦调用 locate¦调用 updatedb¦调用 xargs¦正则表达式¦环境变量¦常见任务¦查看与编辑¦归档文件¦清理文件¦特殊文件名¦修复权限¦文件分类¦完整示例¦删除文件示例¦复制文件子集¦更新时间戳文件¦查找最浅层实例¦安全注意事项¦风险级别¦find 安全注意事项¦xargs 安全注意事项¦locate 安全注意事项¦安全总结¦安全扩展阅读¦错误消息¦find 错误消息¦xargs 错误消息¦locate 错误消息¦updatedb 错误消息''')
fill('bash','''介绍¦什么是 Bash¦什么是 Shell¦术语¦Shell 基础功能¦Shell 语法¦Shell 命令¦Shell 函数¦Shell 参数¦Shell 展开¦重定向¦执行命令¦Shell 脚本¦Shell 内建命令¦Bourne Shell 内建命令¦Bash 内建命令¦修改 Shell 行为¦特殊内建命令¦Shell 变量¦Bourne Shell 变量¦Bash 变量¦Bash 功能¦调用 Bash¦启动文件¦交互式 Shell¦条件表达式¦算术运算¦别名¦数组¦目录栈¦提示符控制¦受限 Shell¦POSIX 模式¦兼容模式¦作业控制¦作业控制基础¦作业控制内建命令¦作业控制变量¦命令行编辑¦编辑介绍与符号¦Readline 交互¦Readline 初始化文件¦可绑定编辑命令¦Readline 的 vi 模式¦可编程补全¦补全内建命令¦补全示例¦交互式历史使用¦历史记录机制¦历史内建命令¦历史展开¦安装 Bash¦基本安装¦编译器与选项¦多架构编译¦安装名称¦指定系统类型¦共享默认配置¦操作控制¦可选功能¦报告问题¦与 Bourne Shell 的主要差异¦与 SVR4.2 Shell 的实现差异¦GNU 自由文档许可¦索引¦内建命令索引¦保留字索引¦变量索引¦函数索引¦概念索引''')
fill('openssh','''SSH 客户端¦SSH 服务端¦SSH 客户端配置¦SSH 服务端配置¦认证代理¦管理代理密钥¦SFTP 文件传输¦SCP 文件复制¦生成与管理密钥¦SFTP 服务端¦获取主机公钥¦基于主机的签名辅助''')
fill('systemd','''管理器说明¦单元类型¦单元目录¦信号处理¦环境变量¦内核命令行¦系统凭据¦就绪通知协议¦启动选项¦相关文件¦版本历史¦另见参考''')
fill('ros2','''第一步¦入门：命令行工具¦配置 ROS 2 环境¦认识 Turtlesim¦理解节点¦理解话题¦理解服务¦理解参数¦理解动作¦使用 RQt 日志控制台¦启动多个节点¦记录与回放数据¦入门：客户端库¦Colcon 构建教程¦创建工作空间¦创建第一个 ROS 2 包¦编写 C++ 发布与订阅¦编写 Python 发布与订阅¦编写 C++ 服务与客户端¦编写 Python 服务与客户端¦自定义 ROS 2 接口¦在单包中定义和使用接口¦C++ 类中的参数¦Python 类中的参数¦使用 ros2 doctor¦插件加载库¦中级教程¦Rosdep 依赖管理¦创建动作接口¦C++ 动作服务器与客户端¦Python 动作服务器与客户端¦编写可组合节点¦组件组合¦节点接口模板类¦C++ 监控参数变化¦Python 监控参数变化¦启动系统教程¦TF2 教程¦测试教程¦URDF 教程¦RViz 教程¦高级教程¦补充 Rosdep 键¦话题统计¦发现服务器¦自定义内存分配器¦Ament 代码规范检查¦Fast DDS 配置¦改进的动态发现¦C++ 节点中记录 Bag¦Python 节点中记录 Bag¦C++ 读取 Bag 文件¦创建 RQt Bag 插件¦ROS 2 跟踪与分析¦实现新的 RMW¦仿真器集成¦安全教程¦演示¦服务质量¦生命周期节点¦进程内通信¦通过 ROS 1 桥接记录¦实时编程¦虚拟机器人演示¦日志与记录器配置¦内容过滤订阅¦服务自省¦等待确认¦其他教程¦部署到 IBM 云¦Eclipse Oxygen 与 RViz¦构建实时内核¦使用 Eclipse 构建包¦基础概念¦接口、话题、服务和动作¦节点概念¦发现机制¦参数概念¦命令行工具概念¦启动概念¦客户端库概念¦中级概念¦通信域 ID¦中间件供应商¦日志概念¦服务质量设置¦执行器¦话题统计概念¦RQt 工具¦组件组合概念¦交叉编译¦安全概念¦TF2 概念¦高级概念¦构建系统¦内部接口¦中间件实现''')
fill('ros2-how','''安装排障¦开发 ROS 2 功能包¦为功能包编写文档¦Ament CMake 文档¦Ament CMake Python 文档¦从 ROS 1 迁移¦不同格式的启动文件¦启动可组合节点¦节点参数¦同步与异步调用¦DDS 调优¦记录回放时覆盖 QoS¦使用多种 RMW 实现¦交叉编译¦发布功能包¦使用 Python 包¦在一个或多个容器中运行节点¦使用 Foxglove 可视化¦核心维护者指南¦构建自定义 Deb 包¦带跟踪支持构建 ROS 2¦使用变体¦使用 ros2 param¦Ubuntu Jammy 的 ROS 1 桥接¦零拷贝借用消息¦树莓派安装¦使用回调组¦获取回溯¦ROS 2 开发环境¦VSCode 与 Docker 开发¦自定义发行版索引''')
fill('ros1','''安装与配置环境¦浏览文件系统¦创建功能包¦构建功能包¦理解节点¦理解话题¦理解服务与参数¦日志控制台与启动文件¦创建消息与服务¦Python 发布订阅¦C++ 发布订阅¦测试发布订阅¦Python 服务客户端¦C++ 服务客户端¦记录与回放¦使用 roswtf 检查''')
fill('gh-get-started','''开始使用¦账号入门¦使用 GitHub¦了解 GitHub¦学习编程¦无障碍使用¦在 GitHub 编写文档¦探索项目¦Git 基础¦使用 Git¦归档账号与公开仓库¦使用 GitHub 文档¦GitHub 认证考试''')
fill('gh-authentication','''账号安全¦双因素认证¦通行密钥认证¦SSH 连接¦SSH 排障¦验证提交签名¦提交签名排障''')
fill('gh-repositories','''创建与管理仓库¦仓库设置¦分支与合并¦处理文件¦发布项目¦查看活动与数据¦归档仓库''')
for group in ['gh-pull-requests','gh-actions']:fill(group,'入门¦核心概念¦实践指南¦参考手册¦教程')
fill('gh-issues','问题管理¦项目管理¦标签与里程碑')
fill('gh-code-security','入门¦核心概念¦实践指南¦参考手册¦教程¦负责任地使用')
fill('gh-pages','快速入门¦开始使用¦使用 Jekyll 建站¦配置自定义域名')
fill('gh-rest','''快速入门¦REST API 概览¦使用 REST API¦身份认证¦指南¦自动化接口¦活动接口¦智能体任务接口¦智能体接口¦应用接口¦账单接口¦分支接口¦安全活动接口¦检查接口¦课堂接口¦代码质量接口¦代码扫描接口¦代码安全设置接口¦行为准则接口¦云开发空间接口¦协作者接口¦提交接口¦Copilot 接口¦Copilot Spaces 接口¦凭据接口¦Dependabot 接口¦依赖关系图接口¦部署密钥接口¦部署接口¦表情符号接口¦企业团队接口¦代码片段接口¦Git 数据库接口¦忽略规则接口¦交互限制接口¦问题接口¦许可证接口¦Markdown 接口¦平台元信息接口¦指标接口¦迁移接口¦组织接口¦软件包接口¦静态站点接口¦私有注册表接口¦项目接口¦拉取请求接口¦速率限制接口¦表情回应接口¦发行版本接口¦仓库接口¦搜索接口¦密钥扫描接口¦安全公告接口¦团队接口¦用户接口''')
fill('gh-github-cli','GitHub 命令行工具')

entries=json.loads((ROOT/'dist/knowledge.json').read_text())['entries']
ids={e['id'] for e in entries}


def attach(group, original, refs, detailed=False):
    matches=[key for key in labels if key.startswith(group+'|') and unmapped[key]==original]
    assert matches,(group,original)
    references=refs.split(',') if refs else []
    assert all(i in ids for i in references),(group,original,references)
    for key in matches:
        labels[key]['entries']=references
        if detailed:labels[key]['status']='detailed'


def mapping(group, prefix, rows):
    for row in rows.strip().splitlines():
        original,refs=row.split('¦')
        attach(group,original,','.join(prefix+'-'+slug for slug in refs.split(',')))


mapping('mujoco-nav','mujoco','''Overview¦install,quickstart
Computation¦step,contact,integrator
Modeling¦body,freejoint,inertia
XML Reference¦defaults,assets,actuator
Programming¦step,quickstart
Simulation¦quickstart,step,state-copy
Visualization¦render,viewer
User Interface¦viewer
Model Editing¦spec
Code samples¦quickstart,arm-project
API Reference¦jacobian,contact-force
Types¦model-data
Functions¦step,jacobian
Python¦install,quickstart
MuJoCo XLA¦mjx
Extensions¦spec''')
mapping('gazebo-nav','gazebo','''Get Started¦install,run
Install¦install
Binary Ubuntu Install¦install
Troubleshooting¦error-gz-command,error-render
ROS/Gazebo Installation¦install,classic
Simulation Tutorials¦quickstart,diffdrive-project
Building your own robot¦model,inertia
Moving the robot¦diff-drive,cmd-vel,diffdrive-project
SDF worlds¦world,quickstart
Sensors¦camera,lidar,imu
Understanding the GUI¦run
Manipulating Models¦spawn
Model Insertion from Fuel¦fuel
Spawn URDF¦urdf
How-to Guides¦bridge,diffdrive-project
ROS 2 integration overview¦bridge,clock
Launch Gazebo from ROS 2¦diffdrive-project
Use ROS 2 to interact with Gazebo¦bridge,diffdrive-project
Use ROS 2 to spawn a Gazebo model¦spawn
ROS 2 interoperability¦bridge-yaml
ROS 2 integration template¦diffdrive-project
Sim Architecture¦plugin,physics
Library How-to Guides¦plugin
Fuel¦fuel,mesh
Migration from Ignition¦classic
Feature Comparison¦classic
Gazebo Classic Migration¦classic
Migration from ROS 2 Gazebo Classic¦classic,bridge
Library Reference¦plugin,physics
physics¦physics
sensors¦camera,lidar
sim¦plugin
transport¦topic-inspect,service
sdformat¦world,frames''')
mapping('isaac-nav','isaac','''Isaac Lab Ecosystem¦compatibility
Local Installation¦install,compatibility
Installation using Isaac Sim Pip Package¦install
Installation using Isaac Sim Pre-built Binaries¦compatibility
Quickstart Guide¦quickstart
Build your Own Project or Task¦randomized-project,register
Create new project or task¦randomized-project
Project Structure¦register
Environment Design Background¦manager,direct
Classes and Configs¦asset-cfg
Environment Design¦manager,observations,rewards
Tutorials¦empty,articulation,quickstart
Creating an empty scene¦empty,launcher
Spawning prims into the scene¦usd,rigid-object
Deep-dive into AppLauncher¦launcher
Adding a New Robot to Isaac Lab¦asset-cfg
Interacting with a rigid object¦rigid-object
Interacting with an articulation¦articulation
Using the Interactive Scene¦scene
Creating a Manager-Based Base Environment¦manager
Creating a Manager-Based RL Environment¦randomized-project,manager
Creating a Direct Workflow RL Environment¦direct
Registering an Environment¦register,randomized-project
Training with an RL Agent¦quickstart
Configuring an RL Agent¦train,hydra
Modifying an existing Direct RL Environment¦direct
Policy Inference in USD Environment¦play,export
Adding sensors on a robot¦camera,contact,raycaster
Using a task-space controller¦ik
Using an operational space controller¦osc
How-to Guides¦usd,asset-cfg,video
Importing a New Asset¦usd
Writing an Asset Configuration¦asset-cfg
Saving rendered images and 3D re-projection¦camera
Find How Many/What Cameras You Should Train With¦memory
Recording video clips during training¦video
Curriculum Utilities¦curriculum
Simulation Performance  and Tuning¦memory,decimation
Developer’s Guide¦install,register
Core Concepts¦manager,direct,scene
Task Design Workflows¦manager,direct
Actuators¦actuators
Sensors¦camera,contact,raycaster,frame-transformer
Motion Generators¦ik,osc
Available Environments¦list-envs
Reinforcement Learning¦train,play
Reinforcement Learning Scripts¦quickstart,train,play
Debugging and Training Guide¦error-nan,error-reward
Imitation Learning¦imitation
Teleoperation and Imitation Learning with Isaac Lab Mimic¦imitation
Simple Agents¦zero-agent
Hydra Configuration System¦hydra
Multi-GPU and Multi-Node Training¦multi-gpu
Tiled Rendering¦camera
Reproducibility and Determinism¦repro
Sim2Real Deployment of Policies Trained in Isaac Lab¦sim2real,export
From IsaacGymEnvs¦migration
From OmniIsaacGymEnvs¦migration
From Orbit¦migration
API Reference¦tensor,scene
isaaclab.app¦launcher
isaaclab.actuators¦actuators
isaaclab.assets¦articulation,rigid-object
isaaclab.controllers¦ik,osc
isaaclab.envs¦manager,direct
isaaclab.managers¦rewards,events,curriculum
isaaclab.scene¦scene
isaaclab.sensors¦camera,contact
isaaclab.sim¦empty,step-order
isaaclab.terrains¦terrain
isaaclab.envs.mdp¦observations,rewards,termination
isaaclab.sim.converters¦usd
isaaclab_rl¦train,play
isaaclab_tasks.utils¦register
Tricks and Troubleshooting¦error-driver,error-memory
Migration Guide (Isaac Sim)¦compatibility,migration
Known Issues¦compatibility''')

# 独立命令章节可精确匹配；聚合章节仍单独评估，不由子章自动继承。
for key,original in unmapped.items():
    if key.startswith('coreutils|') and ':' in original:
        command=original.split(':')[0]
        if 'linux-'+command in ids:labels[key]['entries']=['linux-'+command]
mapping('coreutils','linux','''Output of parts of files¦head-tail
Summarizing files¦wc,sha256sum
Operating on sorted files¦sort,uniq
Operating on fields¦cut
Operating on characters¦tr
Directory listing¦ls
Basic operations¦cp,mv,rm
Special file types¦ln,mkdir
Changing file attributes¦chmod,chown
File space usage¦df,du,stat
Redirection¦tee
Working context¦pwd,env
User information¦id
System context¦hostname,lscpu
Modified command invocation¦env,nice,nohup,timeout
Process control¦kill
File permissions¦chmod,umask
File timestamps¦stat
Exit status¦pipefail
Common options¦man
sha2 utilities: Print or check SHA-2 digests¦sha256sum''')
for original in ['pwd: Print working directory','tee: Redirect output to multiple files or processes','mkdir: Make directories']:
    command=original.split(':')[0];attach('coreutils',original,'linux-'+command,True)
mapping('findutils','linux','''Finding Files¦find
find Expressions¦find
Name¦find
Links¦find,ln
Time¦find
Size¦find
Type¦find
Combining Primaries With Operators¦find
Actions¦find,xargs
Run Commands¦xargs
Print File Name¦find
Reference¦find,xargs
Invoking find¦find
Invoking xargs¦xargs
File Permissions¦chmod
Common Tasks¦find
Archiving¦tar
Security Considerations¦xargs
Security Considerations for xargs¦xargs''')
mapping('bash','linux','''Basic Shell Features¦pipefail,redirect,quoting
Shell Syntax¦pipefail,redirect
Shell Commands¦pipefail,for
Shell Parameters¦env
Redirections¦redirect
Executing Commands¦type
Shell Scripts¦pipefail,experiment
Shell Builtin Commands¦cd,type
Bash Builtins¦type
Modifying Shell Behavior¦pipefail
Shell Variables¦env
Bash Variables¦env
Job Control¦jobs
Job Control Basics¦jobs
Job Control Builtins¦jobs
Job Control Variables¦jobs''')
mapping('openssh','linux','''ssh(1)¦ssh,ssh-tunnel
ssh_config(5)¦ssh
scp(1)¦scp
ssh-keygen(1)¦ssh-keygen
ssh-agent(1)¦ssh-keygen
ssh-add(1)¦ssh-keygen''')
mapping('systemd','linux','''Description¦systemctl
Units¦systemctl
Signals¦kill
See Also¦journalctl,systemctl''')
mapping('ros2','ros','''First Steps¦versions
Beginner: CLI tools¦ros2-node,ros2-topic
Configuring ROS2 Environment¦versions,colcon
Understanding ROS2 Nodes¦ros2-node
Understanding ROS2 Topics¦ros2-topic,ros2-pub
Understanding ROS2 Services¦service
Understanding ROS2 Parameters¦params,params-file
Understanding ROS2 Actions¦action
Using Rqt Console¦logging,rqt
Launching Multiple Nodes¦launch
Recording And Playing Back Data¦bag-record,bag-play
Beginner: Client libraries¦package,quickstart
Colcon Tutorial¦colcon
Creating A Workspace¦colcon,quickstart
Creating Your First ROS2 Package¦package,quickstart
Writing A Simple Py Publisher And Subscriber¦quickstart
Custom ROS2 Interfaces¦custom-msg
Getting Started With Ros2doctor¦doctor
Intermediate¦launch,tf2,test
Rosdep¦rosdep
Creating an Action¦custom-msg,action
Writing a Composable Node¦composition
Composition¦composition
Launch Main¦launch
Tf2 Main¦tf2,tf-tree,tf-static
Testing Main¦test
URDF Main¦urdf
RViz Main¦rviz
Advanced¦security,multimachine
Supplementing Custom Rosdep Keys¦rosdep
Topic Statistics Tutorial¦topic-hz
Discovery Server¦multimachine
FastDDS Configuration¦rmw
Improved Dynamic Discovery¦domain
Simulation Main¦sim-time,navigation-project
Security Main¦security
Demos¦qos,lifecycle
Quality of Service¦qos,durability
Managed Nodes¦lifecycle
Intra Process Communication¦composition
Rosbag with ROS1 Bridge¦migration
Logging and logger configuration¦logging
Basic Concepts¦ros2-node,interface
Interfaces Topics Services Actions¦interface,service,action
About Nodes¦ros2-node
About Discovery¦domain,multimachine
About Parameters¦params
About Command Line Tools¦ros2-run
About Launch¦launch
About Client Libraries¦quickstart
Intermediate Concepts¦qos,executors
About Domain ID¦domain
About Different Middleware Vendors¦rmw
About Logging¦logging
About Quality of Service Settings¦qos
About Executors¦executors
About Topic Statistics¦topic-hz
About RQt¦rqt
About Composition¦composition
About Security¦security
About Tf2¦tf2
About Build System¦colcon
About Middleware Implementations¦rmw''')
attach('ros2','Writing A Simple Py Publisher And Subscriber','ros-quickstart',True)
mapping('ros2-how','ros','''Installation Troubleshooting¦error-package,error-dependency
Developing a ROS 2 Package¦package,quickstart
Migrating from ROS1¦migration
Launch file different formats¦launch
Launching composable nodes¦composition
Node arguments¦remap,params
Sync Vs Async¦executors
DDS tuning¦qos,multimachine
Overriding QoS Policies For Recording And Playback¦qos,bag-record
Working with multiple RMW implementations¦rmw
Using Python Packages¦quickstart
Using ros2 param¦params
Using callback groups¦executors''')
mapping('ros1','ros','''InstallingandConfiguringROSEnvironment¦versions,ros1-core
NavigatingTheFilesystem¦ros1-run
CreatingPackage¦ros1-create
BuildingPackages¦ros1-catkin
UnderstandingNodes¦ros1-node
UnderstandingTopics¦ros1-topic
UnderstandingServicesParams¦ros1-service,ros1-param
UsingRqtconsoleRoslaunch¦ros1-launch,ros1-debug
ExaminingPublisherSubscriber¦ros1-topic,ros1-pub
Recording and playing back data¦ros1-bag
Getting started with roswtf¦ros1-debug''')
mapping('gh-get-started','github','''Start your journey¦concepts
Onboarding¦auth
Using GitHub¦research-release
Writing on GitHub¦readme
Explore projects¦issue-search
Git basics¦clone,remote,branch
Using Git¦fetch,pull,push''')
mapping('gh-authentication','github','''Account security¦auth,token
Connect with SSH¦ssh
Troubleshooting SSH¦error-ssh''')
mapping('gh-repositories','github','''Create & manage repositories¦create,clone
Manage repository settings¦rules,codeowners
Branches and merges¦branch,merge,conflict
Work with files¦ignore,lfs,submodule
Release projects¦release,research-release''')
mapping('gh-pull-requests','github','''Get started¦pr-create
Concepts¦pr-review,merge
How-tos¦pr-create,pr-review,conflict
Reference¦pr-review''')
mapping('gh-actions','github','''Get started¦actions,ci-project
Concepts¦actions,runner,artifacts
How-tos¦ci-project,matrix,secrets
Reference¦actions
Tutorials¦python-ci,ci-project''')
mapping('gh-issues','github','''Issues¦issues,templates
Projects¦projects
Labels and milestones¦issues''')
mapping('gh-code-security','github','''Getting started¦secrets
Concepts¦secrets''')
mapping('gh-pages','github','''Quickstart¦pages
Get started¦pages''')
mapping('gh-rest','github','''Quickstart¦api
About the REST API¦api
Using the REST API¦api
Authentication¦token,api
Rate limit¦api''')
attach('gh-github-cli','GitHub CLI','github-auth,github-run-inspect,github-pr-create')

assert len(labels)==len(unmapped)
(ROOT/'data/chapter-labels.json').write_text(json.dumps(labels,ensure_ascii=False,indent=2)+'\n')
print(f'已填写 {len(labels)} 个章节中文映射')
