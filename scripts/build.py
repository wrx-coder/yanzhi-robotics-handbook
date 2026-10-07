#!/usr/bin/env python3
"""将可维护的中文词条编译为支持 file:// 的本地数据文件。无需第三方依赖。"""
import json
import hashlib
import zipfile
from pathlib import Path
from learning import validate_learning
from embodied import MODULE as EMBODIED_MODULE, SOURCES as EMBODIED_SOURCES, validate_skills

ROOT = Path(__file__).resolve().parent.parent
MODULES = [
    dict(id='linux', name='Linux', subtitle='命令与系统管理', icon='terminal', color='green', version='GNU/Linux · Ubuntu 22.04 / 24.04', description='从文件与文本处理，到远程计算、GPU 排障与实验复现。', prerequisites='终端示例默认使用 Ubuntu 上的 Bash。先阅读说明，并将文件、目录、用户、设备和进程编号替换为实际值。sudo 命令会修改系统；本网站只展示代码，不执行命令。'),
    dict(id='mujoco', name='MuJoCo', subtitle='动力学与机器人仿真', icon='box', color='blue', version='MuJoCo 3.3.7 · Python API', description='理解模型、接触与控制，建立可复现的机器人仿真。', prerequisites='示例以官方 mujoco 3.3.7 Python 包为基线。Python 片段中 m 是已加载的 MjModel，d 是对应的 MjData；np 表示已导入的 numpy。具名关节、执行器、传感器须先在模型中定义。完整起步代码见「最小仿真实验」。'),
    dict(id='gazebo', name='Gazebo', subtitle='场景、传感器与系统集成', icon='layers', color='orange', version='Harmonic · Classic 11 迁移', description='搭建世界、接入传感器，将机器人仿真连接到 ROS。', prerequisites='默认使用 Gazebo Harmonic（gz-sim8）与 ROS 2 Jazzy。gz 命令不是 Gazebo Classic 的 gazebo 命令。XML 是应放入相应 SDF 元素的配置片段，示例名称须匹配自己的世界和模型。'),
    dict(id='ros', name='ROS 1 / 2', subtitle='机器人通信与应用开发', icon='network', color='purple', version='Noetic · Humble / Jazzy', description='从节点通信、坐标变换，到导航、机械臂与系统调试。', prerequisites='以 ROS 2 Jazzy / Ubuntu 24.04 为默认；标有 ROS 1 的词条使用 Noetic / Ubuntu 20.04。Humble 对应 Ubuntu 22.04。先加载相应工作空间；不要在同一终端混合 source ROS 1 与 ROS 2。节点名、包名、话题名须按实际系统替换。'),
    dict(id='isaac', name='Isaac Lab', subtitle='并行仿真与机器人学习', icon='cpu', color='teal', version='Isaac Lab v2.3.0', description='构建 GPU 并行环境，训练、评估与部署机器人策略。', prerequisites='以 Isaac Lab v2.3.0 源码布局为基线；在 IsaacLab 仓库根目录执行 ./isaaclab.sh。先按该版本官方安装指南配置兼容的 Isaac Sim、Python 与 NVIDIA 驱动。配置片段需要放入已有的任务、场景或训练脚本，不是独立程序。'),
    dict(id='github', name='GitHub', subtitle='代码协作与科研发布', icon='branch', color='slate', version='GitHub · Git · GitHub CLI', description='管理研究代码、参与开源协作，建立可复现的发布与自动化流程。', prerequisites='Git 是本机版本管理工具，GitHub 是远程协作平台，gh 是可选的 GitHub CLI。示例中的 OWNER、REPO、用户名、分支和编号都需要替换。向远程 push、创建 PR 或修改设置会影响真实仓库，执行前核对当前仓库与权限。')
]
CORE_MODULE_IDS = {m['id'] for m in MODULES}
MODULES.append(EMBODIED_MODULE)
SOURCES = {
 'gh-start': ['GitHub：入门文档', 'https://docs.github.com/en/get-started'],
 'gh-flow': ['GitHub：分支协作流程', 'https://docs.github.com/en/get-started/using-github/github-flow'],
 'gh-pr': ['GitHub：Pull Request 与代码审查', 'https://docs.github.com/en/pull-requests'],
 'gh-issues': ['GitHub：Issue 与项目管理', 'https://docs.github.com/en/issues'],
 'gh-actions': ['GitHub Actions：自动化工作流', 'https://docs.github.com/en/actions'],
 'gh-security': ['GitHub：代码安全', 'https://docs.github.com/en/code-security'],
 'gh-auth': ['GitHub：身份验证', 'https://docs.github.com/en/authentication'],
 'gh-repo': ['GitHub：仓库管理', 'https://docs.github.com/en/repositories'],
 'gh-pages': ['GitHub Pages：静态网站', 'https://docs.github.com/en/pages'],
 'gh-cli': ['GitHub CLI 官方手册', 'https://cli.github.com/manual/'],
 'gh-api': ['GitHub REST API 文档', 'https://docs.github.com/en/rest'],
 'gh-limits': ['GitHub：大文件管理', 'https://docs.github.com/en/repositories/working-with-files/managing-large-files'],
 'gh-cite': ['GitHub：使用引用文件', 'https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files'],
 'core': ['GNU Coreutils 官方手册', 'https://www.gnu.org/software/coreutils/manual/'],
 'bash': ['GNU Bash 官方手册', 'https://www.gnu.org/software/bash/manual/bash.html'],
 'find': ['GNU Findutils 官方手册（网络访问可能受限）', 'https://www.gnu.org/software/findutils/manual/'],
 'grep': ['GNU grep 官方手册', 'https://www.gnu.org/software/grep/manual/grep.html'],
 'sed': ['GNU sed 官方手册', 'https://www.gnu.org/software/sed/manual/sed.html'],
 'awk': ['GNU awk 官方手册', 'https://www.gnu.org/software/gawk/manual/gawk.html'],
 'linux': ['Linux man-pages 项目', 'https://www.kernel.org/doc/man-pages/'],
 'systemd': ['systemd 官方手册', 'https://www.freedesktop.org/software/systemd/man/latest/'],
 'ssh': ['OpenSSH 官方手册', 'https://www.openssh.com/manual.html'],
 'rsync': ['rsync 官方手册', 'https://download.samba.org/pub/rsync/rsync.1'],
 'tar': ['GNU tar 官方手册', 'https://www.gnu.org/software/tar/manual/'],
 'git': ['Git 官方参考', 'https://git-scm.com/docs'],
 'docker': ['Docker 命令行官方参考', 'https://docs.docker.com/reference/cli/docker/'],
 'python': ['Python venv 官方文档', 'https://docs.python.org/3/library/venv.html'],
 'pip': ['pip 命令行官方参考', 'https://pip.pypa.io/en/stable/cli/'],
 'cmake': ['CMake 官方手册', 'https://cmake.org/cmake/help/latest/manual/cmake.1.html'],
 'gdb': ['GDB 官方文档', 'https://sourceware.org/gdb/current/onlinedocs/gdb.html/'],
 'nvidia': ['NVIDIA System Management Interface', 'https://docs.nvidia.com/deploy/nvidia-smi/'],
 'slurm': ['Slurm 官方命令', 'https://slurm.schedmd.com/man_index.html'],
 'apt': ['Ubuntu apt 官方手册', 'https://manpages.ubuntu.com/manpages/jammy/en/man8/apt.8.html'],
 'tmux': ['tmux 官方使用指南', 'https://github.com/tmux/tmux/wiki/Getting-Started'],
 'curl': ['curl 官方命令手册', 'https://curl.se/docs/manpage.html'],
 'mj-overview': ['MuJoCo：引擎概览', 'https://mujoco.readthedocs.io/en/3.3.7/overview.html'],
 'mj-python': ['MuJoCo：Python 接口', 'https://mujoco.readthedocs.io/en/3.3.7/python.html'],
 'mj-model': ['MuJoCo：建模指南', 'https://mujoco.readthedocs.io/en/3.3.7/modeling.html'],
 'mj-xml': ['MuJoCo：MJCF 元素参考', 'https://mujoco.readthedocs.io/en/3.3.7/XMLreference.html'],
 'mj-compute': ['MuJoCo：计算原理', 'https://mujoco.readthedocs.io/en/3.3.7/computation/index.html'],
 'mj-sim': ['MuJoCo：仿真编程', 'https://mujoco.readthedocs.io/en/3.3.7/programming/simulation.html'],
 'mj-api': ['MuJoCo：函数参考', 'https://mujoco.readthedocs.io/en/3.3.7/APIreference/APIfunctions.html'],
 'mj-edit': ['MuJoCo：程序化模型编辑', 'https://mujoco.readthedocs.io/en/3.3.7/programming/modeledit.html'],
 'mj-mjx': ['MuJoCo：MJX 加速后端', 'https://mujoco.readthedocs.io/en/3.3.7/mjx.html'],
 'mj-vis': ['MuJoCo：可视化', 'https://mujoco.readthedocs.io/en/3.3.7/programming/visualization.html'],
 'gz-start': ['Gazebo：开始使用', 'https://gazebosim.org/docs/harmonic/getstarted/'],
 'gz-install': ['Gazebo：ROS 版本配对', 'https://gazebosim.org/docs/harmonic/ros_installation/'],
 'gz-robot': ['Gazebo：构建机器人', 'https://gazebosim.org/docs/harmonic/building_robot/'],
 'gz-move': ['Gazebo：驱动机器人', 'https://gazebosim.org/docs/harmonic/moving_robot/'],
 'gz-world': ['Gazebo：SDF 世界', 'https://gazebosim.org/docs/harmonic/sdf_worlds/'],
 'gz-sensor': ['Gazebo：传感器教程', 'https://gazebosim.org/docs/harmonic/sensors/'],
 'gz-api': ['Gazebo Sim 8 官方教程', 'https://gazebosim.org/api/sim/8/tutorials.html'],
 'gz-bridge': ['ros_gz_bridge 官方源码与用法', 'https://github.com/gazebosim/ros_gz/tree/jazzy/ros_gz_bridge'],
 'gz-ros': ['Gazebo：ROS 2 集成', 'https://gazebosim.org/docs/harmonic/ros2_integration/'],
 'gz-migrate': ['Gazebo：Classic 迁移', 'https://gazebosim.org/docs/harmonic/gazebo_classic_migration/'],
 'sdf': ['SDFormat 官方规范', 'http://sdformat.org/spec'],
 'ros1': ['ROS 1 官方教程（可能触发访问验证）', 'https://wiki.ros.org/ROS/Tutorials'],
 'ros2': ['ROS 2 Jazzy 官方教程', 'https://docs.ros.org/en/jazzy/Tutorials.html'],
 'ros2-concept': ['ROS 2 Jazzy 核心概念', 'https://docs.ros.org/en/jazzy/Concepts.html'],
 'ros2-how': ['ROS 2 Jazzy 实践指南', 'https://docs.ros.org/en/jazzy/How-To-Guides.html'],
 'ros2-raw': ['ROS 2 文档官方源码（Jazzy）', 'https://github.com/ros2/ros2_documentation/tree/jazzy/source'],
 'ros-rep': ['ROS 官方平台与发行版规范', 'https://www.ros.org/reps/rep-2000.html'],
 'ros-control': ['ros2_control 官方文档', 'https://control.ros.org/jazzy/index.html'],
 'nav2': ['Nav2 官方文档', 'https://docs.nav2.org/'],
 'moveit': ['MoveIt 2 官方教程', 'https://moveit.picknik.ai/main/index.html'],
 'il-install': ['Isaac Lab：安装与兼容性', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/setup/installation/index.html'],
 'il-tutorial': ['Isaac Lab：教程目录', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/tutorials/index.html'],
 'il-how': ['Isaac Lab：实践指南', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/how-to/index.html'],
 'il-api': ['Isaac Lab：API 参考', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/api/index.html'],
 'il-env': ['Isaac Lab：环境设计工作流', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/overview/core-concepts/task_workflows.html'],
 'il-train': ['Isaac Lab：强化学习脚本', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/overview/reinforcement-learning/rl_existing_scripts.html'],
 'il-code': ['Isaac Lab v2.3.0 官方源码', 'https://github.com/isaac-sim/IsaacLab/tree/v2.3.0'],
 'il-sensor': ['Isaac Lab：传感器概念', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/overview/core-concepts/sensors/index.html'],
 'il-hydra': ['Isaac Lab：Hydra 配置', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/features/hydra.html'],
 'il-multi': ['Isaac Lab：多 GPU 训练', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/features/multi_gpu.html'],
 'il-repro': ['Isaac Lab：可复现性', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/features/reproducibility.html'],
}

SOURCES.update(EMBODIED_SOURCES)

def build():
    entries = []
    for module in MODULES:
        path = ROOT / 'data' / (module['id'] + '.txt')
        if not path.exists():
            continue
        for n, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip() or line.startswith('#'):
                continue
            fields = line.split('¦')
            if len(fields) != 9:
                raise ValueError(f'{path.name}:{n}: expected 9 fields, got {len(fields)}')
            slug, title, category, summary, principle, code, explain, pitfall, source = fields
            if not all(fields) or source not in SOURCES:
                raise ValueError(f'{path.name}:{n}: empty field or unknown source {source}')
            language, code = code.split('::', 1)
            advanced = any(s in category for s in ['高级', '优化', '学习', '集群', '控制', '调试', '性能'])
            version = module['version']
            if module['id'] == 'ros':
                version = 'ROS 1 Noetic' if category.startswith('ROS 1') else ('ROS 1 → ROS 2' if '迁移' in category else 'ROS 2 Humble / Jazzy')
            if module['id'] == 'gazebo' and 'Classic' in title:
                version = 'Gazebo Classic 11 → Harmonic'
            entries.append(dict(id=f"{module['id']}-{slug}", module=module['id'], title=title, category=category,
                summary=summary, principle=principle, code=code.replace('\\n', '\n'), language=language,
                explain=explain.split(';;'), pitfall=pitfall, source=source, version=version,
                level='进阶' if advanced else '基础', kind='命令' if language=='bash' else ('配置' if language in ['xml','yaml','cmake'] else '指南')))
    extra = ROOT / 'data' / 'workflows.json'
    if extra.exists():
        entries.extend(json.loads(extra.read_text()))
    projects_path = ROOT / 'data/projects.json'
    if projects_path.exists():
        projects = json.loads(projects_path.read_text())
        replacements = {entry['id']: entry for entry in projects}
        entries = [replacements.pop(e['id'], e) for e in entries] + list(replacements.values())
    errors_path = ROOT / 'data/errors.json'
    if errors_path.exists():
        errors = json.loads(errors_path.read_text())
        assert len(errors) == 72
        assert all(sum(e['module'] == mid for e in errors) == 12 for mid in CORE_MODULE_IDS)
        entries.extend(errors)
    skills = json.loads((ROOT / 'data/embodied.json').read_text())
    validate_skills(skills, SOURCES)
    entries.extend(skills)
    ids = [e['id'] for e in entries]
    assert len(ids) == len(set(ids)), 'Duplicate article IDs'
    for entry in entries:
        assert entry['module'] in {m['id'] for m in MODULES}
        assert entry['source'] in SOURCES
        for key in ['title','category','summary','principle','explain','pitfall','version','level','kind'] + ([] if entry['kind'] == '技能' else ['code','language']):
            assert entry.get(key), (entry['id'], key)
        for related in entry.get('related', []):
            assert related in ids and related != entry['id'], (entry['id'], related)
        if entry['kind'] == '报错':
            t = entry['troubleshooting']
            assert t['patterns'] and t['diagnosis'] and t['fixes'] and t['verification']['expected']
        if 'project' in entry:
            project = entry['project']
            directory = ROOT / 'projects' / project['directory']
            assert directory.is_dir(), directory
            files = sorted(p for p in directory.rglob('*') if p.is_file() and not any(x in p.parts for x in ['__pycache__','.git','build','install','log']) and p.suffix != '.pyc')
            assert files and (directory/'README.md').exists()
            download_dir = ROOT/'dist/downloads'
            download_dir.mkdir(exist_ok=True)
            archive = download_dir/(project['directory']+'.zip')
            project['files'] = []
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as package:
                for file in files:
                    relative = file.relative_to(directory).as_posix()
                    assert not file.is_symlink(), file
                    contents = file.read_text()
                    project['files'].append(dict(path=relative, content=contents))
                    info = zipfile.ZipInfo(project['directory']+'/'+relative, (2026,9,21,0,0,0))
                    info.external_attr = (0o100755 if file.suffix == '.sh' else 0o100644) << 16
                    package.writestr(info, contents.encode(), compress_type=zipfile.ZIP_DEFLATED)
            project['download'] = 'downloads/'+archive.name
            project['sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
            project['size'] = archive.stat().st_size
    chapters_path = ROOT/'data/chapters.json'
    coverage = json.loads(chapters_path.read_text()) if chapters_path.exists() else dict(books=[], chapters=[])
    chapter_ids = [c['id'] for c in coverage['chapters']]
    assert len(chapter_ids) == len(set(chapter_ids))
    for chapter in coverage['chapters']:
        assert chapter['status'] in ['detailed','overview','missing']
        assert chapter['verification'] in ['checked','pending']
        assert chapter['module'] in {m['id'] for m in MODULES}
        assert chapter['url'].startswith(('https://','http://'))
        assert all(ref in ids for ref in chapter['entries']), chapter
        assert bool(chapter['entries']) == (chapter['status'] != 'missing'), chapter
        if chapter.get('parent'):
            assert chapter['parent'] in chapter_ids
    for module in MODULES:
        module['count'] = sum(e['module']==module['id'] for e in entries)
    learning_paths = json.loads((ROOT/'data/learning-paths.json').read_text())
    validate_learning(learning_paths, entries)
    payload = dict(learningPaths=learning_paths, schemaVersion=4, updated='2026-09-21', modules=MODULES, sources=SOURCES, entries=entries, coverage=coverage)
    (ROOT/'dist'/'knowledge.js').write_text('window.KNOWLEDGE = ' + json.dumps(payload, ensure_ascii=False) + ';\n')
    (ROOT/'dist'/'knowledge.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f'已编译 {len(entries)} 篇中文词条 / {len(MODULES)} 个模块')
    for m in MODULES:
        print(f"  {m['name']}: {m['count']} 篇")

if __name__ == '__main__':
    build()
