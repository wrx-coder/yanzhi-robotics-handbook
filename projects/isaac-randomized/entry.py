"""先注册字符串入口，再让官方训练脚本初始化 AppLauncher。"""
import os
from pathlib import Path
import runpy
import sys
import gymnasium as gym

gym.register(id='Research-Cartpole-Randomized-v0',
             entry_point='isaaclab.envs:ManagerBasedRLEnv', disable_env_checker=True,
             kwargs={'env_cfg_entry_point':'research_task:ResearchCartpoleEnvCfg',
                     'rsl_rl_cfg_entry_point':
                     'isaaclab_tasks.manager_based.classic.cartpole.agents.rsl_rl_ppo_cfg:CartpolePPORunnerCfg'})

if len(sys.argv)<2 or sys.argv[1] not in ('train','play','check'):
    raise SystemExit('用法：entry.py train|play|check [官方脚本参数]')
mode = sys.argv.pop(1)
root = Path(os.environ['ISAACLAB_PATH']).resolve()
script = root/('scripts/environments/zero_agent.py' if mode=='check' else
               f'scripts/reinforcement_learning/rsl_rl/{mode}.py')
if not script.is_file():
    raise SystemExit(f'缺少官方脚本：{script}')
sys.path.insert(0, str(script.parent))
sys.argv[0] = str(script)
os.chdir(root)
runpy.run_path(str(script), run_name='__main__')
