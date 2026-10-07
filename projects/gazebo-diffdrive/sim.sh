#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
command -v gz >/dev/null
command -v ros2 >/dev/null
pids=()
cleanup() { trap - EXIT INT TERM; for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done; wait || true; }
trap cleanup EXIT INT TERM
gz sim -r world.sdf "$@" &
pids+=("$!")
ros2 run ros_gz_bridge parameter_bridge --ros-args -p "config_file:=$PWD/bridge.yaml" &
pids+=("$!")
ros2 run tf2_ros static_transform_publisher --x 0.1 --y 0 --z 0.18 --roll 0 --pitch 0 --yaw 0 --frame-id base_link --child-frame-id laser_frame &
pids+=("$!")
wait -n "${pids[@]}"
