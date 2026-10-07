#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
[[ -f maps/room.yaml ]] || { printf '请先完成建图并保存 maps/room.yaml\n' >&2; exit 2; }
python3 prepare_config.py
ros2 launch nav2_bringup bringup_launch.py use_sim_time:=true use_composition:=False "map:=$PWD/maps/room.yaml" "params_file:=$PWD/nav2.generated.yaml"
