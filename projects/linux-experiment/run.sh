#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p runs
run_id="$(date -u +%Y%m%dT%H%M%S)-$$"
python3 -u train.py --seed 42 --output "runs/$run_id" 2>&1 | tee "runs/$run_id.log"
tar -czf "runs/$run_id.tar.gz" -C runs "$run_id" "$run_id.log"
printf '归档：runs/%s.tar.gz\n' "$run_id"
