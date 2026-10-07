"""逐个子进程运行实验；失败写入表格，不阻断后续组合。"""
import argparse
import csv
import json
from pathlib import Path
import statistics
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('sweep-results'))
    parser.add_argument('--fail-seed', type=int, help='测试失败记录：该种子改用非法学习率')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    rows = []
    for rate in [.03, .1]:
        for seed in [0, 1, 2]:
            name = f'lr{rate}-seed{seed}'
            command = [sys.executable, str(Path(__file__).with_name('train.py')),
                       '--seed', str(seed), '--lr', str(-1 if seed == args.fail_seed else rate),
                       '--output', str(args.output/name)]
            with (args.output/(name+'.log')).open('w') as log:
                completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
            row = {'name': name, 'seed': seed, 'lr': rate, 'returncode': completed.returncode,
                   'status': 'failed' if completed.returncode else 'ok', 'loss': ''}
            if completed.returncode == 0:
                row['loss'] = json.loads((args.output/name/'result.json').read_text())['loss']
            rows.append(row)
    with (args.output/'summary.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = []
    for rate in [.03, .1]:
        group = [r for r in rows if r['lr']==rate]
        losses = [r['loss'] for r in group if r['status']=='ok']
        summary.append({'lr':rate,'success':len(losses),'failed':len(group)-len(losses),
                        'mean_loss':statistics.mean(losses) if losses else None,
                        'stdev_loss':statistics.stdev(losses) if len(losses)>1 else None})
    (args.output/'aggregate.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if any(r['returncode'] for r in rows) else 0


if __name__ == '__main__':
    sys.exit(main())
