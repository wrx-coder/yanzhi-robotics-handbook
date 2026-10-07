#!/usr/bin/env bash
set -euo pipefail
site_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
port="${1:-8765}"
if ! [[ "$port" =~ ^[0-9]+$ ]] || (( port < 1 || port > 65535 )); then
  printf '端口必须是 1–65535 的数字。\n' >&2
  exit 1
fi
printf '研知 · 本地科研手册\n打开：http://127.0.0.1:%s\n按 Ctrl+C 停止。也可以直接双击 index.html 离线阅读。\n' "$port"
exec python3 -m http.server "$port" --bind 127.0.0.1 --directory "$site_root/dist"
