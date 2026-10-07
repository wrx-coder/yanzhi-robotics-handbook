"""纯标准库线性回归实验；合成数据避免依赖外部数据下载。"""
import argparse
import csv
import json
import math
import random
from pathlib import Path


def train(seed, learning_rate, epochs):
    if not 0 < learning_rate <= 1 or epochs < 1:
        raise ValueError('学习率应在 (0, 1]，训练轮数必须为正数')
    rng = random.Random(seed)
    samples = [(x := rng.uniform(-1, 1), 2 * x + 1 + rng.gauss(0, .05)) for _ in range(128)]
    weight = bias = 0.0
    history = []
    for epoch in range(epochs):
        errors = [(weight*x+bias-y, x) for x,y in samples]
        weight -= learning_rate * 2 * sum(e*x for e,x in errors) / len(errors)
        bias -= learning_rate * 2 * sum(e for e,x in errors) / len(errors)
        loss = sum((weight*x+bias-y)**2 for x,y in samples) / len(samples)
        if not math.isfinite(loss):
            raise ValueError('损失非有限，终止实验')
        history.append((epoch+1, loss))
    return {'seed': seed, 'learning_rate': learning_rate, 'epochs': epochs,
            'weight': weight, 'bias': bias, 'loss': history[-1][1]}, history


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--lr', type=float, default=.1)
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--output', type=Path, default=Path('runs/demo'))
    args = parser.parse_args()
    result, history = train(args.seed, args.lr, args.epochs)
    args.output.mkdir(parents=True, exist_ok=False)
    with (args.output/'metrics.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['epoch', 'loss'])
        writer.writerows(history)
    (args.output/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
