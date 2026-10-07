"""在配置好的 IsaacLab v2.3.0 环境运行：./isaaclab.sh -p /实际路径/isaac_empty.py。"""
import argparse
from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser()
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()
launcher = AppLauncher(args)
simulation_app = launcher.app

# 此导入必须位于 AppLauncher 之后。
from isaaclab.sim import SimulationCfg, SimulationContext

try:
    sim = SimulationContext(SimulationCfg(dt=0.01, device=args.device))
    sim.set_camera_view([2, 2, 2], [0, 0, 0])
    sim.reset()
    for _ in range(200):
        if not simulation_app.is_running():
            break
        sim.step()
    print('空场景运行结束。')
finally:
    simulation_app.close()
