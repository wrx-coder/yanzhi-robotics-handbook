# 研知 · 机器人科研手册

中文、本地、无需登录的静态知识库，包含 Linux、MuJoCo、Gazebo、ROS 1/2、Isaac Lab、GitHub 和 Embodied · 具身智能科研技能七个模块。

## 打开网站

直接用浏览器打开本目录的 **index.html**，无需安装任何依赖、构建工具或联网。

也可以在本目录执行：

```bash
bash 启动网站.sh
```

浏览器访问 http://127.0.0.1:8765 。需要其他端口时执行 `bash 启动网站.sh 8800`。服务仅监听本机。按 Ctrl+C 停止。

网站正文与搜索完全本地运行，不请求外部接口、不加载在线字体或 CDN。官方参考链接和教程中的软件下载仍需联网。浏览器禁止 file:// 下的持久存储或剪贴板时，页面仍能阅读和搜索，复制会尝试降级并显示结果。

## 使用方式

- 顶部全文搜索可查中文、命令、参数和代码；多个关键词要求同时匹配。`Ctrl+K` 或 `/` 聚焦搜索。
- 左侧切换模块，可按分类、类型、难度和版本筛选，结果支持分页。
- 点击词条查看适用前提、原理、示例、参数、边界和官方参考。
- 星标收藏仅保存在当前浏览器。`file://` 与 `http://` 属于不同存储来源，收藏不共用。
- 「报错库」包含 72 篇排障案例，原有六个工具模块各 12 篇。支持粘贴多行日志，优先匹配具体错误字符串；时间戳与临时路径不要求逐字一致。查看检查原因、正常/异常结果、条件修复与验证。粘贴日志只留在当前页面内存，不上传、不写入收藏存储或地址栏。
- 「完整实战」包含 12 套工程，原有六个工具模块各两套。可以展开查看完整源码，下载独立 ZIP，并按 README 的步骤运行。页面代码与下载包来自同一组文件。
- 「官方章节覆盖表」包含 21 份目录、797 个章节记录，支持模块、文档、覆盖状态和中英文标题筛选。每章关联本地文章、官方来源、版本与核对日期。
- 「Embodied · 具身智能科研技能」收录 96 项技能，12 类、每类 8 项。每篇有问题、原理、前置知识、流程、工具与输入输出、误区及深入阅读，可无代码阅读。支持具身智能、embodied、IL、RL、BC、ACT、VLA 等中英文搜索，并复用分类、难度、技能类型、分页、收藏与最近阅读。
- 原有 `#article/词条ID` 链接继续有效；新增入口为 `#errors`、`#practice`、`#coverage`、`#module/embodied`；技能深链接为 `#article/embodied-…`。

## 学习路线与练习

首页与侧栏点击「学习路线」，或打开 `dist/index.html#learn`。四条路线为科研基础、机械臂仿真与控制、ROS 移动机器人、具身智能学习；每条四阶段，每阶段包含 3–5 篇顺序阅读、一项练习和三道单选自测，共 16 个阶段、16 项练习、48 道题。

- 路线深链接：`#path/research-foundations`、`#path/arm-control`、`#path/ros-mobile`、`#path/embodied-learning`。阶段链接例如 `#path/ros-mobile?stage=navigation`；根目录入口也保留这些链接。
- 阶段可自由跳转，「建议先学」只提供前置链接。「继续学习」定位首个未完成阶段；四阶段都完成后显示「复习路线」。
- 阅读与练习分别手动勾选，可随时取消。自测三题全对才通过；三项同时满足才完成阶段。改答案或重新作答会撤销本次自测通过状态，保留阅读和练习勾选。
- 自测提交后显示每题答案、解释和阅读链接。选择尚未提交的答案也会保存；提示与参考解答可以自行展开。
- 练习勾选明确标为「个人自记」，不会改变工程的已有验证证据。打开文章、答题通过不代表实验成功。IL、VLA 与接触抓取方案练习不附完整训练或抓取工程；RL 无运行环境时可保存方案，运行验收仍应留作未完成。
- 进度独立存于 `yanzhi-learning-progress-v1`，不改收藏和最近阅读。只在当前浏览器、当前来源保存，不跨设备同步。清理站点数据会清除进度；`file://` 与 HTTP 进度不共用。
- 存储不可用时，页面明确提示仅保留会话进度。损坏的记录会安全重置；结构有效时保留其他正常阶段。网站阅读和答题不联网，实际安装依赖、获取运行时仍可能需要网络。

学习路线只是引用现有文章、报错和工程的独立教学索引，不重复存储正文；网站仍为 **7 个模块、503 篇条目**。

## 内容范围与准确性

这是独立编写的中文科研学习手册，不是官方文档全文翻译或镜像，也不承诺覆盖所有科研问题与全部 API。技能“大全”表示首版常用技能目录，覆盖从空间表示到科研复现的全流程；不包含全部前沿论文、全部机器人驱动或覆盖所有方向的完整课程，也不新增完整训练工程。技能正文为独立中文学习说明，每篇 200–400 汉字，阅读不代表已完成实验验证。每条命令和代码均配原理与具体说明；部分条目是需要嵌入已有项目的片段，不能脱离使用前提独立执行。

内容基线：GNU/Linux（Ubuntu 22.04/24.04）、MuJoCo 3.3.7、Gazebo Harmonic、ROS 1 Noetic、ROS 2 Humble/Jazzy、Isaac Lab v2.3.0，以及 GitHub 官方文档。Noetic 与 Gazebo Classic 属于已结束支持的历史路线。

当前共 503 篇中文词条，包括 96 项技能、72 篇报错与 12 套实战。章节覆盖状态为：4 章详解、340 章概述、453 章未收录；797 是目录记录数量，不能解释为已完整翻译 797 章。父章与子章独立判断，不因一个子主题有例子就将整章标为详解。ROS 1 的 16 项目录因 Wiki 访问验证保留“待核对”。

Embodied 属于跨工具技能索引，不计入上述 797 条官方章节覆盖记录。其来源包括 OpenCV 4.13.0、MuJoCo 3.3.7、Isaac Lab v2.3.0、MoveIt、LeRobot、PyTorch 官方文档，以及 ACT、Diffusion Policy、PPO、SAC、OpenVLA、LoRA 等原始论文。每篇分别标注来源版本或 2026-09-21 索引快照日期；动态文档日后可能变化，索引日期不是模型实测日期。

Linux 两套与 MuJoCo 两套项目的核心 CPU 流程已经实际运行；其余 8 套标为“静态检查通过”。GitHub 本地实验、提交与单元测试经过验证，远程 PR/Actions/Release 没有代为执行。完整 ROS、Gazebo、Isaac Lab 和真实 GPU 环境未运行。每套项目的日期、环境和验证范围直接显示在阅读页中；详见「验证记录.md」。

GNU 手册章节采用 Coreutils 9.5、Bash 5.3、Findutils 4.9.0 的文档目录基线；这不代表 Ubuntu 自带相同版本，运行选项仍需核对本机 `--help`。OpenSSH、systemd、GitHub 使用明确日期的在线目录快照。ROS 2 章节表按 Jazzy 核对；ROS 1 Noetic 用于历史项目。全文是独立中文讲解，官方目录快照只保存标题、层级和入口等索引信息。

## 文件组织与内容维护

```text
index.html              双击入口
启动网站.sh              可选本地 HTTP 服务
dist/                   完整静态网站，复制此文件夹即可单独阅读
data/*.txt              各模块的中文词条源数据
data/skills/embodied.txt  人工编写的 96 项技能源稿（按分类分节）
data/embodied.json      编译后的技能结构化正文、关键词和多来源
data/embodied-source-audit.json  新增来源入口检查记录
data/learning-paths.json  4 条路线的独立教学数据（不计入文章数）
data/workflows.json     原始实战数据，构建时由同 ID 新工程替换
data/errors/*.txt       人工编写的 72 篇结构化排障源数据
data/projects.json      12 套实战网页说明
data/project-validation.json  每套工程的真实验证状态
data/chapters.json      官方章节树、覆盖状态与本地引用
data/chapter-labels.json      人工中文标题与覆盖依据
data/official-snapshots/      官方目录来源与标题快照
data/source-audit.json  官方链接检查记录（访问保护会单独标注）
projects/               12 套完整工程源码与中文 README
dist/downloads/         根据 projects/ 自动打包的独立 ZIP
examples/               保留早期单文件示例
scripts/build.py        校验、生成离线数据并打包工程
scripts/make_learning.py  人工维护的路线内容与 JSON 生成器
scripts/learning.py      路线、练习、自测与引用校验
scripts/verify_learning.cjs  学习进度、答题及存储异常回归
scripts/verify_learning_browser.cjs  独立无头 Chrome 离线与响应式检查
scripts/verify_package.py  完整 ZIP 解压离线重建与逐文件一致性检查
scripts/make_embodied.py  编译技能正文，校验每类数量与 200–400 汉字范围
scripts/embodied.py     技能模块、来源版本与数据契约
scripts/make_errors.py  生成结构化排障条目
scripts/make_projects.py  同源生成工程 README 与网页步骤
scripts/make_chapters.py  从冻结目录和中文映射生成覆盖表
scripts/verify.cjs       离线页面行为回归检查
scripts/verify_content.py   内容、引用与 ZIP 同源检查
scripts/verify_projects.py  工程静态与可用 CPU 环境验证
scripts/check_sources.py   可选在线链接检查
```

修改普通条目后运行 `python3 scripts/build.py`。修改实战代码直接编辑 `projects/` 中的文件；修改步骤说明编辑 `scripts/make_projects.py`，README 会由该脚本重建。不要把实际训练输出写入用于打包的源目录。完整重建顺序如下，只需要 Python 标准库，不会联网：

```bash
python3 scripts/make_embodied.py
python3 scripts/make_learning.py
python3 scripts/make_errors.py
python3 scripts/make_projects.py
python3 scripts/make_chapters.py
python3 scripts/build.py
```

差速世界如需从参数生成器重新生成，先运行 `python3 scripts/make_robot_world.py`；它会同步 Gazebo 与 ROS 导航项目的共享仿真文件。章节中文映射以 `chapter-labels.json` 为维护源；`label_chapters.py` 是初始人工映射生成记录，不必在日常构建中重复执行。在线目录更新必须重新核对标题、版本和引用，再保存快照，不能自动把新增章节视为已覆盖。

技能源稿每行用 `¦` 分隔 12 个字段：短 ID、中文标题、英文全称与缩写、难度、问题、原理、前置知识、流程、工具与输入输出、误区、来源键、关联 ID。流程用 `;;` 分隔，来源和关联 ID 用逗号分隔；分类行以 `# ` 开头。修改后先运行 `python3 scripts/make_embodied.py`，再构建。技能不需要 `code` 或 `language` 字段，JSON 同时保留兼容主来源 `source` 与带版本、日期的 `sources` 列表。

学习内容以 `scripts/make_learning.py` 为维护源，修改后运行 `python3 scripts/make_learning.py` 和 `python3 scripts/build.py`。路线及阶段 ID 用于进度键和深链接，发布后保持稳定。编译时校验数量、必填字段、题目答案范围、前置链接及文章/工程/排障引用。

运行 `python3 scripts/verify_content.py` 与 `node scripts/verify.cjs /tmp/yanzhi-qa/node_modules/linkedom` 检查内容和离线页面行为，再运行 `node scripts/verify_learning.cjs /tmp/yanzhi-qa/node_modules/linkedom` 检查学习进度。可用 Chrome 环境运行 `node scripts/verify_learning_browser.cjs /tmp/yanzhi-qa/node_modules/playwright` 验证离线交互与布局，最后运行 `python3 scripts/package_site.py` 更新完整 ZIP。

测试工具可能需要另外准备 `linkedom`、`PyYAML` 和用于仿真实测的 MuJoCo；这些都不是网站运行依赖。具体命令见验证记录。

普通工具词条行包含九个用 `¦` 分隔的字段：标识、标题、分类、用途、原理、语言与代码、参数说明、边界、官方来源键。代码换行用字面量 `\n`，参数说明用 `;;` 分隔。来源和模块元数据位于 scripts/build.py。

`dist/knowledge.json` 是便于扩展与检索的完整结构化内容；页面加载 `knowledge.js` 以兼容浏览器 file:// 访问，无需 fetch、服务端或数据库。

本项目按用户要求仅交付本地网站，未发布到远程托管服务，也未创建或修改 GitHub 仓库。
