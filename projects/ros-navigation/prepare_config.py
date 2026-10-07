"""从本机 Jazzy 的 Nav2 完整默认配置派生配置，保留同版本所需节点和插件。"""
from pathlib import Path
import hashlib
import json
import yaml
from ament_index_python.packages import get_package_share_directory

source = Path(get_package_share_directory('nav2_bringup'))/'params/nav2_params.yaml'
config = yaml.safe_load(source.read_text())


def adapt(value):
    if isinstance(value,dict):
        for key,item in value.items():
            if key in ('base_frame_id','robot_base_frame','base_frame'):
                value[key] = 'base_link'
            elif key=='enable_stamped_cmd_vel':
                value[key] = False
            elif key=='robot_radius':
                value[key] = .30
            elif key=='footprint':
                value[key] = '[[-0.24,-0.23],[-0.24,0.23],[0.24,0.23],[0.24,-0.23]]'
            else:
                adapt(item)
    elif isinstance(value,list):
        for item in value: adapt(item)


adapt(config)
for name in ['amcl','bt_navigator','controller_server','velocity_smoother','collision_monitor','behavior_server']:
    params = config.setdefault(name,{}).setdefault('ros__parameters',{})
    params['use_sim_time'] = True
    params['enable_stamped_cmd_vel'] = False
controller = config['controller_server']['ros__parameters']['FollowPath']
# Jazzy 默认使用 MPPI；若安装版本已替换插件，停止而不是错改无关参数。
if 'MPPIController' not in controller.get('plugin',''):
    raise SystemExit('该 Nav2 默认配置不是预期的 Jazzy MPPI，请核对安装版本')
controller.update(vx_max=.30,vx_min=-.15,wz_max=.8,ax_max=.5,ax_min=-.5,az_max=1.0)
velocity = config['velocity_smoother']['ros__parameters']
velocity.update(max_velocity=[.30,0.,.8],min_velocity=[-.15,0.,-.8],
                max_accel=[.5,0.,1.],max_decel=[-.5,0.,-1.])
destination = Path(__file__).with_name('nav2.generated.yaml')
destination.write_text(yaml.safe_dump(config,sort_keys=False))
Path(__file__).with_name('config-origin.json').write_text(json.dumps({
    'source':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'note':'派生自本机安装的 Nav2 Jazzy；将本文件与实验产物一同归档'},ensure_ascii=False,indent=2))
print(destination)
