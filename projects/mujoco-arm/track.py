"""Jacobian 阻尼最小二乘逆解 + 关节 PD 跟踪；输出真实仿真误差。"""
import csv
import json
from pathlib import Path
import mujoco
import numpy as np


def main():
    model = mujoco.MjModel.from_xml_path(str(Path(__file__).with_name('arm.xml')))
    data, solver = mujoco.MjData(model), mujoco.MjData(model)
    tip = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SITE, 'tip')
    data.qpos[:] = [0.0, 1.3]
    solver.qpos[:] = data.qpos
    jacobian = np.zeros((3, model.nv))
    records = []
    for _ in range(3000):
        time = data.time
        target = np.array([.65+.08*np.cos(time), .2+.08*np.sin(time)])
        for _ in range(15):
            mujoco.mj_forward(model, solver)
            delta = target - solver.site_xpos[tip, :2]
            if np.linalg.norm(delta) < 1e-6:
                break
            mujoco.mj_jacSite(model, solver, jacobian, None, tip)
            j = jacobian[:2]
            dq = j.T @ np.linalg.solve(j @ j.T + .001*np.eye(2), delta)
            mujoco.mj_integratePos(model, solver.qpos, np.clip(dq, -.1, .1), 1)
        mujoco.mj_forward(model, data)
        error = np.linalg.norm(data.site_xpos[tip, :2]-target)
        data.ctrl[:] = np.clip(70*(solver.qpos-data.qpos)-8*data.qvel, -20, 20)
        records.append([time, *target, *data.site_xpos[tip, :2], error])
        mujoco.mj_step(model, data)
        if not np.isfinite(data.qpos).all():
            raise RuntimeError('仿真状态非有限')
    with open('trajectory.csv', 'w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['time_s','target_x','target_y','actual_x','actual_y','error_m'])
        writer.writerows(records)
    rmse = float(np.sqrt(np.mean(np.square([r[-1] for r in records if r[0]>=1]))))
    result = {'steady_rmse_m':rmse, 'samples':len(records), 'acceptance':rmse<.03}
    Path('metrics.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
    if not result['acceptance']:
        raise SystemExit('误差超过 3 cm；检查版本、控制参数和轨迹可达性')


if __name__ == '__main__':
    main()
