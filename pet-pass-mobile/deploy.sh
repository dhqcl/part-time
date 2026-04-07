#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RAW_PORT="${1:-${HOST_PORT:-718}}"

if [[ ! "$RAW_PORT" =~ ^[0-9]+$ ]]; then
  echo "错误: 端口必须是纯数字，例如 718"
  exit 1
fi

HOST_PORT="$((10#$RAW_PORT))"

if (( HOST_PORT < 1 || HOST_PORT > 65535 )); then
  echo "错误: 端口必须在 1-65535 之间"
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "错误: 未检测到 docker，请先安装 Docker。"
  exit 1
fi

if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
else
  echo "错误: 未检测到 docker compose 或 docker-compose。"
  exit 1
fi

echo "开始部署 pet-pass-mobile ..."
echo "部署目录: $SCRIPT_DIR"
echo "映射端口: $HOST_PORT -> 80"

HOST_PORT="$HOST_PORT" "${COMPOSE_CMD[@]}" up -d --build

echo
echo "部署完成。"
echo "本机访问: http://127.0.0.1:$HOST_PORT/"
echo "局域网/公网访问: http://服务器IP:$HOST_PORT/"
echo
echo "常用命令:"
echo "  查看状态: ${COMPOSE_CMD[*]} ps"
echo "  查看日志: ${COMPOSE_CMD[*]} logs -f"
echo "  停止服务: ${COMPOSE_CMD[*]} down"
