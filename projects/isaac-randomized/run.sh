#!/usr/bin/env bash
set -euo pipefail
: "${ISAACLAB_PATH:?请设置 IsaacLab v2.3.0 仓库绝对路径}"
project_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
mode="${1:-check}"
if (( $# )); then shift; fi
"$ISAACLAB_PATH/isaaclab.sh" -p "$project_dir/entry.py" "$mode" --task Research-Cartpole-Randomized-v0 --num_envs 64 --headless "$@"
