"""静态检查全部实战，在临时目录运行可用的 CPU 项目并记录实际范围。"""
import argparse
import ast
import csv
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import yaml

ROOT=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mujoco-python',type=Path)
args=parser.parse_args()
reports={}
environment=f'{platform.system()} {platform.machine()} · Python {platform.python_version()}'


def run(command,cwd,expected=0):
    result=subprocess.run(command,cwd=cwd,capture_output=True,text=True,timeout=120)
    if result.returncode!=expected:
        raise AssertionError((command,result.returncode,result.stdout,result.stderr))
    return result.stdout+result.stderr


for project in sorted((ROOT/'projects').iterdir()):
    if not project.is_dir():continue
    checked=[]
    for p in project.rglob('*'):
        if '__pycache__' in p.parts or not p.is_file():continue
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p));checked.append(p.name)
        elif p.suffix=='.sh':run(['bash','-n',str(p)],project);checked.append(p.name)
        elif p.suffix in ['.xml','.sdf']:ET.parse(p);checked.append(p.name)
        elif p.suffix in ['.yaml','.yml']:yaml.safe_load(p.read_text());checked.append(p.name)
    assert (project/'README.md').exists()
    reports[project.name]=dict(status='静态检查通过',date='2026-09-21',environment=environment,
        evidence=f"已检查 {len(checked)} 个 Python / Bash / XML / YAML 文件的语法；未启动目标软件或云端服务。")
    print('STATIC',project.name,len(checked))

with tempfile.TemporaryDirectory(prefix='yanzhi-projects-') as tmp:
    temp=Path(tmp)
    for name in ['linux-experiment','linux-sweep','github-release','github-ci']:
        dest=temp/name;shutil.copytree(ROOT/'projects'/name,dest)
        if name=='linux-experiment':
            run(['bash','run.sh'],dest)
            results=list(dest.glob('runs/*/result.json'));assert len(results)==1
            result=json.loads(results[0].read_text());assert result['loss']<.01
            assert len(list(dest.glob('runs/*.tar.gz')))==1
            reports[name].update(status='目标环境运行通过',evidence=f"Bash 流水线与真实训练运行成功，loss={result['loss']:.6f}，CSV/JSON/日志/tar.gz 均生成。未运行 tmux 交互会话；其命令已静态核对。")
        elif name=='linux-sweep':
            run([sys.executable,'sweep.py'],dest)
            rows=list(csv.DictReader((dest/'sweep-results/summary.csv').open()))
            assert len(rows)==6 and all(r['status']=='ok' for r in rows)
            run([sys.executable,'sweep.py','--output','failures','--fail-seed','1'],dest,expected=1)
            rows=list(csv.DictReader((dest/'failures/summary.csv').open()))
            assert len(rows)==6 and sum(r['status']=='failed' for r in rows)==2
            reports[name].update(status='目标环境运行通过',evidence='六组扫描全部成功；注入故障后四组成功、两组失败，程序退出码 1；CSV 与分组统计保留失败记录。')
        elif name=='github-release':
            run([sys.executable,'train.py'],dest)
            assert json.loads((dest/'runs/demo/result.json').read_text())['loss']<.01
            run(['git','init','-b','main'],dest)
            run(['git','add','train.py','README.md','PR.md','RELEASE.md','.gitignore'],dest)
            run(['git','-c','user.name=Local QA','-c','user.email=qa@example.invalid','commit','-m','本地验收'],dest)
            run(['git','switch','-c','experiment/qa'],dest)
            reports[name]['evidence']='Python 实验和临时仓库的初始化、提交、分支操作运行通过。未连接 GitHub；PR、推送、标签与 Release 的远端流程未运行。'
        else:
            output=run([sys.executable,'-m','unittest','discover','-s','tests','-v'],dest)
            assert 'Ran 3 tests' in output and 'OK' in output
            reports[name]['evidence']='本机三个单元测试通过，两个 Actions YAML 已解析。未在 GitHub Runner 运行 Python 矩阵或发布工作流。'
        print('RUN',name)
    if args.mujoco_python:
        python=str(args.mujoco_python.absolute())
        version=run([python,'-c','import sys,mujoco,numpy; print(sys.version.split()[0],mujoco.__version__,numpy.__version__)'],temp).strip()
        assert version.split()[1]=='3.3.7'
        for name,script in [('mujoco-pendulum','mujoco_minimal.py'),('mujoco-arm','track.py')]:
            dest=temp/name;shutil.copytree(ROOT/'projects'/name,dest)
            output=run([python,script],dest)
            if name=='mujoco-pendulum':
                rows=list(csv.DictReader((dest/'pendulum.csv').open()));assert len(rows)==1000
                assert abs(float(rows[-1]['time_s'])-2)<1e-8
                import math
                assert all(math.isfinite(float(v)) for row in rows for v in row.values())
                evidence='CPU 无图形运行通过；1000 条有限数值日志，最终仿真时间 2 秒。'
            else:
                metrics=json.loads((dest/'metrics.json').read_text())
                assert metrics['acceptance'] and metrics['samples']==3000
                evidence=f"CPU 无图形运行通过；3000 条轨迹，去掉首秒后的末端 RMSE={metrics['steady_rmse_m']:.6f} m，小于 0.03 m 阈值。"
            reports[name].update(status='目标环境运行通过',environment=f'Linux x86_64 · Python / MuJoCo / NumPy：{version}',evidence=evidence)
            print('RUN',name,evidence)

(ROOT/'data/project-validation.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
print('项目验证完成；目标软件缺失的项目保持静态状态')
