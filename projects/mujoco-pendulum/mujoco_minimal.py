"""最小 MuJoCo 控制实验：python mujoco_minimal.py，无需图形界面。"""
import csv
import math
from pathlib import Path
import mujoco

XML = """
<mujoco model="research_pendulum">
  <compiler angle="radian"/>
  <option timestep="0.002" integrator="implicitfast"/>
  <worldbody>
    <geom type="plane" size="2 2 0.1"/>
    <body pos="0 0 1">
      <joint name="hinge" type="hinge" axis="0 1 0" damping="0.05"/>
      <geom type="capsule" fromto="0 0 0 0 0 -0.5" size="0.04" mass="1"/>
      <site name="tip" pos="0 0 -0.5" size="0.02"/>
    </body>
  </worldbody>
  <actuator>
    <motor name="drive" joint="hinge" gear="1" ctrllimited="true" ctrlrange="-2 2"/>
  </actuator>
</mujoco>
"""


def main():
    model = mujoco.MjModel.from_xml_string(XML)
    data = mujoco.MjData(model)
    data.qpos[0] = 0.4
    mujoco.mj_forward(model, data)
    output = Path('pendulum.csv')
    with output.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['time_s', 'angle_rad', 'velocity_rad_s', 'control_nm'])
        for _ in range(1000):
            data.ctrl[0] = max(-2, min(2, 0.2 * math.sin(data.time) - 0.5 * data.qvel[0]))
            mujoco.mj_step(model, data)
            writer.writerow([data.time, data.qpos[0], data.qvel[0], data.ctrl[0]])
    print(f'完成 {data.time:.3f} 秒仿真；记录文件：{output.resolve()}')


if __name__ == '__main__':
    main()
