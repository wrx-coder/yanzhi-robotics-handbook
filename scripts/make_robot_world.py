"""生成自包含的差速世界。无在线模型、纹理或 Fuel 依赖。"""
from pathlib import Path
import shutil
from build import ROOT


def box_model(name, pose, size):
    geometry = f'<geometry><box><size>{size}</size></box></geometry>'
    return f'<model name="{name}"><static>true</static><pose>{pose}</pose><link name="link"><collision name="collision">{geometry}</collision><visual name="visual">{geometry}</visual></link></model>'


def make_world():
    parts = ['''<?xml version="1.0"?>
<sdf version="1.9"><world name="research_room">
  <physics name="physics" type="ignored"><max_step_size>0.001</max_step_size><real_time_factor>1</real_time_factor></physics>
  <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
  <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
  <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
  <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors"><render_engine>ogre2</render_engine></plugin>
  <light name="sun" type="directional"><pose>0 0 10 0 0 0</pose><diffuse>0.9 0.9 0.9 1</diffuse><direction>-0.5 0.1 -0.9</direction></light>
''']
    parts += [box_model('floor','0 0 -0.05 0 0 0','8 8 0.1'),
              box_model('north','0 3 0.5 0 0 0','6 0.1 1'),
              box_model('south','0 -3 0.5 0 0 0','6 0.1 1'),
              box_model('east','3 0 0.5 0 0 0','0.1 6 1'),
              box_model('west','-3 0 0.5 0 0 0','0.1 6 1'),
              box_model('obstacle','1.2 1 0.4 0 0 0','0.6 0.6 0.8')]
    parts += ['''<model name="research_robot"><pose>0 0 0.15 0 0 0</pose>
  <link name="base_link">
    <inertial><mass>3</mass><inertia><ixx>0.0261</ixx><iyy>0.054225</iyy><izz>0.073125</izz></inertia></inertial>
    <collision name="body"><geometry><box><size>0.45 0.3 0.12</size></box></geometry></collision>
    <visual name="body"><geometry><box><size>0.45 0.3 0.12</size></box></geometry><material><diffuse>0.1 0.6 0.45 1</diffuse></material></visual>
    <sensor name="laser" type="gpu_lidar">
      <pose>0.1 0 0.18 0 0 0</pose><topic>/scan</topic><gz_frame_id>laser_frame</gz_frame_id>
      <always_on>true</always_on><update_rate>10</update_rate><visualize>true</visualize>
      <lidar><scan><horizontal><samples>360</samples><resolution>1</resolution><min_angle>-3.14159265</min_angle><max_angle>3.14159265</max_angle></horizontal></scan><range><min>0.08</min><max>8</max><resolution>0.01</resolution></range></lidar>
    </sensor>
  </link>''']
    for side, y in [('left',.2),('right',-.2)]:
        geometry='<geometry><cylinder><radius>0.1</radius><length>0.05</length></cylinder></geometry>'
        parts += [f'''<link name="{side}_wheel"><pose>0.1 {y} -0.05 1.57079632679 0 0</pose>
<inertial><mass>0.2</mass><inertia><ixx>0.000542</ixx><iyy>0.000542</iyy><izz>0.001</izz></inertia></inertial>
<collision name="wheel">{geometry}<surface><friction><ode><mu>1</mu><mu2>1</mu2></ode></friction></surface></collision><visual name="wheel">{geometry}</visual></link>
<joint name="{side}_joint" type="revolute"><parent>base_link</parent><child>{side}_wheel</child><axis><xyz expressed_in="__model__">0 1 0</xyz></axis></joint>''']
    parts += ['''<link name="caster"><pose>-0.18 0 -0.10 0 0 0</pose>
<inertial><mass>0.1</mass><inertia><ixx>0.0001</ixx><iyy>0.0001</iyy><izz>0.0001</izz></inertia></inertial>
<collision name="caster"><geometry><sphere><radius>0.05</radius></sphere></geometry><surface><friction><ode><mu>0</mu><mu2>0</mu2></ode></friction></surface></collision><visual name="caster"><geometry><sphere><radius>0.05</radius></sphere></geometry></visual></link>
<joint name="caster_fixed" type="fixed"><parent>base_link</parent><child>caster</child></joint>
<plugin filename="gz-sim-diff-drive-system" name="gz::sim::systems::DiffDrive">
<left_joint>left_joint</left_joint><right_joint>right_joint</right_joint><wheel_separation>0.4</wheel_separation><wheel_radius>0.1</wheel_radius>
<topic>/cmd_vel</topic><odom_topic>/odom</odom_topic><tf_topic>/tf</tf_topic><frame_id>odom</frame_id><child_frame_id>base_link</child_frame_id><odom_publish_frequency>30</odom_publish_frequency>
<max_linear_velocity>0.35</max_linear_velocity><min_linear_velocity>-0.35</min_linear_velocity><max_angular_velocity>1</max_angular_velocity><min_angular_velocity>-1</min_angular_velocity>
<max_linear_acceleration>0.5</max_linear_acceleration><min_linear_acceleration>-0.5</min_linear_acceleration>
</plugin></model></world></sdf>''']
    destination = ROOT/'projects/gazebo-diffdrive'
    destination.mkdir(parents=True,exist_ok=True)
    (destination/'world.sdf').write_text('\n'.join(parts)+'\n')
    navigation = ROOT/'projects/ros-navigation'
    navigation.mkdir(parents=True,exist_ok=True)
    for name in ['world.sdf','bridge.yaml','sim.sh','drive.py']:
        if (destination/name).exists():
            shutil.copyfile(destination/name,navigation/name)


if __name__=='__main__':
    make_world()
