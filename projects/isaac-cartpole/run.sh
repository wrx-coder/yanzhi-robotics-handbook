#!/usr/bin/env bash
set -euo pipefail
: "${ISAACLAB_PATH:?请设置 ISAACLAB_PATH 为 IsaacLab v2.3.0 仓库绝对路径}"
mode="${1:-check}"
if (( $# )); then shift; fi
cd -- "$ISAACLAB_PATH"
case "$mode" in
  check) ./isaaclab.sh -p scripts/environments/zero_agent.py --task Isaac-Cartpole-v0 --num_envs 16 --headless "$@" ;;
  train) ./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Cartpole-v0 --num_envs 64 --max_iterations 150 --seed 42 --headless "$@" ;;
  play) ./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play.py --task Isaac-Cartpole-v0 --num_envs 16 --headless "$@" ;;
  *) printf '用法：bash run.sh check|train|play [官方脚本参数]\n' >&2; exit 2 ;;
esac
