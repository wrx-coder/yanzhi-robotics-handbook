"""比较两次训练的 TensorBoard 奖励曲线，报告尾部窗口，不伪造训练结果。"""
import argparse
import json
import statistics
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('baseline', help='基线运行的 TensorBoard 目录')
parser.add_argument('variant', help='自定义任务运行目录')
parser.add_argument('--tag', default='Train/mean_reward')
parser.add_argument('--window', type=int, default=20)
args = parser.parse_args()
if args.window<1:
    parser.error('window 必须为正数')
result = {}
for name in ['baseline','variant']:
    accumulator = EventAccumulator(getattr(args,name), size_guidance={'scalars':0})
    accumulator.Reload()
    tags = accumulator.Tags()['scalars']
    if args.tag not in tags:
        raise SystemExit(f'{name} 找不到 {args.tag}；可用标签：{tags}')
    values = accumulator.Scalars(args.tag)[-args.window:]
    if not values:
        raise SystemExit(f'{name} 无数据')
    result[name] = {'tag':args.tag,'count':len(values),'last_step':values[-1].step,
                    'tail_mean':statistics.mean(v.value for v in values)}
print(json.dumps(result, ensure_ascii=False, indent=2))
print('奖励定义不同，数值不可直接证明策略更好；需固定评估环境并比较回合长度/成功率。')
