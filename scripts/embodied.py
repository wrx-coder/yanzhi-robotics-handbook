"""具身技能模块元数据和离线内容契约；来源版本不等同于实测环境。"""
import re
from collections import Counter

MODULE = dict(id='embodied', name='Embodied', subtitle='具身智能科研技能', icon='network', color='indigo',
    version='96 项技能 · 12 类 · 2026-09-21 索引快照',
    description='具身智能科研技能大全：从空间表示、机器人建模到 IL、RL、VLA 与真机部署。首版常用技能速查目录，按流程学习与检索。',
    prerequisites='这是跨工具学习索引。坐标方向、单位、机器人接口与软件版本须按各技能说明核对；阅读条目不代表完成实验验证。')
# key: title, URL, version / source baseline
REFERENCE_DATA = {
 'emb-rep103': ('ROS REP 103：单位与坐标约定', 'https://www.ros.org/reps/rep-0103.html', 'REP 103 · 2026-09-21 页面快照'),
 'emb-mr': ('Modern Robotics：作者教材与章节', 'https://hades.mech.northwestern.edu/index.php/Modern_Robotics', 'Lynch & Park · 2017 教材'),
 'emb-scipy-rotation': ('SciPy：Rotation 空间旋转', 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html', 'SciPy stable · 2026-09-21 索引快照'),
 'emb-scipy-opt': ('SciPy：least_squares 非线性最小二乘', 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html', 'SciPy stable · 2026-09-21 索引快照'),
 'emb-mj-model': ('MuJoCo：模型与执行器', 'https://mujoco.readthedocs.io/en/3.3.7/modeling.html', 'MuJoCo 3.3.7'),
 'emb-mj-compute': ('MuJoCo：动力学与接触计算', 'https://mujoco.readthedocs.io/en/3.3.7/computation/index.html', 'MuJoCo 3.3.7'),
 'emb-mj-xml': ('MuJoCo：MJCF 字段', 'https://mujoco.readthedocs.io/en/3.3.7/XMLreference.html', 'MuJoCo 3.3.7'),
 'emb-urdf': ('ROS 2：URDF 教程', 'https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html', 'ROS 2 Jazzy'),
 'emb-sdf': ('SDFormat：模型规范', 'https://sdformat.org/spec', 'SDFormat · 2026-09-21 索引快照'),
 'emb-calib': ('OpenCV：标定与三维重建', 'https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html', 'OpenCV 4.13.0'),
 'emb-img': ('OpenCV：图像处理', 'https://docs.opencv.org/4.13.0/d7/dbd/group__imgproc.html', 'OpenCV 4.13.0'),
 'emb-flow': ('OpenCV：视频运动分析与跟踪', 'https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html', 'OpenCV 4.13.0'),
 'emb-detection': ('TorchVision：检测与实例分割微调教程', 'https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html', 'PyTorch 教程 · 2026-09-21 索引快照'),
 'emb-o3d': ('Open3D：点云处理', 'https://www.open3d.org/docs/release/tutorial/geometry/pointcloud.html', 'Open3D release · 2026-09-21 索引快照'),
 'emb-icp': ('Open3D：ICP 配准', 'https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html', 'Open3D release · 2026-09-21 索引快照'),
 'emb-sync': ('ROS 2 message_filters：近似时间同步', 'https://docs.ros.org/en/jazzy/p/message_filters/doc/Tutorials/Approximate-Synchronizer-Python.html', 'ROS 2 Jazzy'),
 'emb-moveit': ('MoveIt 2：规划与操作教程', 'https://moveit.picknik.ai/main/index.html', 'MoveIt main · 2026-09-21 索引快照'),
 'emb-control': ('ros2_control：关节轨迹控制器', 'https://control.ros.org/jazzy/doc/ros2_controllers/joint_trajectory_controller/doc/userdoc.html', 'ros2_control Jazzy'),
 'emb-underactuated': ('MIT Underactuated Robotics：接触与操作', 'https://underactuated.mit.edu/manipulation.html', '课程目录 · 2026-09-21 索引快照'),
 'emb-trajopt': ('MIT Underactuated Robotics：轨迹优化', 'https://underactuated.mit.edu/trajopt.html', '课程目录 · 2026-09-21 索引快照'),
 'emb-lerobot': ('LeRobot：机器人学习文档', 'https://huggingface.co/docs/lerobot/index', 'LeRobot main · 2026-09-21 索引快照'),
 'emb-dataset': ('LeRobotDataset：v3.0 数据格式', 'https://huggingface.co/docs/lerobot/lerobot-dataset-v3', 'LeRobotDataset v3.0 · 2026-09-21 索引快照'),
 'emb-bc': ('LeRobot：机器人模仿学习教程', 'https://huggingface.co/docs/lerobot/il_robots', 'LeRobot main · 2026-09-21 索引快照'),
 'emb-dagger': ('DAgger：原始论文', 'https://proceedings.mlr.press/v15/ross11a.html', 'Ross et al. · AISTATS 2011'),
 'emb-act': ('ACT：Learning Fine-Grained Bimanual Manipulation', 'https://arxiv.org/abs/2304.13705', 'Zhao et al. · 2023'),
 'emb-act-doc': ('LeRobot：ACT 策略', 'https://huggingface.co/docs/lerobot/act', 'LeRobot main · 2026-09-21 索引快照'),
 'emb-diffusion': ('Diffusion Policy：原始论文', 'https://arxiv.org/abs/2303.04137', 'Chi et al. · 2023'),
 'emb-ppo': ('Proximal Policy Optimization Algorithms：原始论文', 'https://arxiv.org/abs/1707.06347', 'Schulman et al. · 2017'),
 'emb-sac': ('Soft Actor-Critic：原始论文', 'https://proceedings.mlr.press/v80/haarnoja18b.html', 'Haarnoja et al. · ICML 2018'),
 'emb-gym': ('Gymnasium：处理时间上限', 'https://gymnasium.farama.org/tutorials/gymnasium_basics/handling_time_limits/', 'Gymnasium · 2026-09-21 索引快照'),
 'emb-spinning': ('Spinning Up：强化学习概念', 'https://spinningup.openai.com/en/latest/spinningup/rl_intro.html', 'Spinning Up · 2026-09-21 索引快照'),
 'emb-cql': ('Conservative Q-Learning：原始论文', 'https://arxiv.org/abs/2006.04779', 'Kumar et al. · 2020'),
 'emb-isaac': ('Isaac Lab：任务工作流', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/overview/core-concepts/task_workflows.html', 'Isaac Lab v2.3.0'),
 'emb-isaac-api': ('Isaac Lab：API 参考', 'https://isaac-sim.github.io/IsaacLab/v2.3.0/source/api/index.html', 'Isaac Lab v2.3.0'),
 'emb-openvla': ('OpenVLA：原始论文', 'https://arxiv.org/abs/2406.09246', 'Kim et al. · 2024'),
 'emb-openvla-code': ('OpenVLA：作者实现与动作接口', 'https://github.com/openvla/openvla', '作者仓库 · 2026-09-21 索引快照'),
 'emb-rt2': ('RT-2：视觉语言动作模型', 'https://arxiv.org/abs/2307.15818', 'Brohan et al. · 2023'),
 'emb-lora': ('LoRA：原始论文', 'https://arxiv.org/abs/2106.09685', 'Hu et al. · 2021'),
 'emb-oxe': ('Open X-Embodiment：跨机器人数据与模型', 'https://arxiv.org/abs/2310.08864', 'Open X-Embodiment Collaboration · 2023'),
 'emb-random': ('Domain Randomization：原始论文', 'https://arxiv.org/abs/1703.06907', 'Tobin et al. · 2017'),
 'emb-dynamics': ('Sim-to-Real Transfer with Dynamics Randomization', 'https://arxiv.org/abs/1710.06537', 'Peng et al. · 2018'),
 'emb-onnx': ('PyTorch：导出模型到 ONNX', 'https://docs.pytorch.org/tutorials/beginner/onnx/export_simple_model_to_onnx_tutorial.html', 'PyTorch 教程 · 2026-09-21 索引快照'),
 'emb-profiler': ('PyTorch：Profiler 性能分析', 'https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html', 'PyTorch 教程 · 2026-09-21 索引快照'),
 'emb-torch-repro': ('PyTorch：可复现性', 'https://docs.pytorch.org/docs/stable/notes/randomness.html', 'PyTorch stable · 2026-09-21 索引快照'),
 'emb-rliable': ('Deep RL at the Edge of the Statistical Precipice', 'https://arxiv.org/abs/2108.13264', 'Agarwal et al. · 2021'),
 'emb-binomial': ('SciPy：二项比例置信区间', 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html', 'SciPy stable · 2026-09-21 索引快照'),
 'emb-libero': ('LIBERO：作者基准协议与实现', 'https://github.com/Lifelong-Robot-Learning/LIBERO', '作者仓库 · 2026-09-21 索引快照'),
 'emb-robomimic': ('robomimic：数据集与算法文档', 'https://robomimic.github.io/docs/introduction/overview.html', 'robomimic · 2026-09-21 索引快照'),
}
SOURCES = {key: list(value[:2]) for key, value in REFERENCE_DATA.items()}
CATEGORIES = ['数学与空间表示','机器人建模','传感器与标定','视觉与三维感知','运动规划与控制','抓取与操作','数据采集与管理','模仿学习','强化学习','VLA 与多模态策略','仿真到部署','科研评估与复现']

def body_text(e):
    return ''.join([e['summary'],e['principle'],e['prerequisites'],*e['explain'],e['tools'],e['pitfall']])

def validate_skills(entries, sources):
    assert len(entries) == 96
    assert Counter(e['category'] for e in entries) == Counter({c: 8 for c in CATEGORIES})
    for e in entries:
        assert e['id'].startswith('embodied-') and e['module'] == 'embodied' and e['kind'] == '技能'
        for key in ['title','englishTitle','summary','principle','prerequisites','explain','tools','pitfall','keywords','sources','related','version']:
            assert e.get(key), (e['id'],key)
        assert len(e['explain']) >= 2 and e['level'] in ['基础','进阶']
        size = len(re.findall(r'[\u4e00-\u9fff]', body_text(e)))
        assert 200 <= size <= 400, (e['id'], '正文汉字数', size)
        assert e['source'] == e['sources'][0]['key']
        for ref in e['sources']:
            assert ref['key'] in sources and ref['version'] and ref['checked'] == '2026-09-21'
            assert sources[ref['key']][1].startswith('https://')
        assert not e.get('code') and not e.get('language'), e['id']
