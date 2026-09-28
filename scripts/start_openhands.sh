#!/bin/bash

WORKSPACE_DIR="/home/ww/openhands_workspace"

echo "🚀 正在清理舊的 OpenHands 容器..."
docker stop openhands-app 2>/dev/null || true
docker rm openhands-app 2>/dev/null || true

echo "🔥 啟動 OpenHands 容器 (已修正鏡像路徑與權限設定)..."
docker run -d \
  --name openhands-app \
  -e SANDBOX_USER_ID=$(id -u) \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.28-nikola \
  -e LOG_ALL_EVENTS=true \
  -e WORKSPACE_MOUNT_PATH=$WORKSPACE_DIR \
  -e LLM_MAX_INPUT_TOKENS=32768 \
  -e LLM_TIMEOUT=600 \
  -e TZ=Asia/Tokyo \
  -v $WORKSPACE_DIR:/opt/workspace_base \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.openhands-state:/.openhands-state \
  -v ~/.gitconfig:/etc/gitconfig:ro \
  -v /etc/localtime:/etc/localtime:ro \
  -p 3000:3000 \
  --add-host host.docker.internal:host-gateway \
  ghcr.io/all-hands-ai/openhands:0.28

echo "✅ 啟動成功！請開啟瀏覽器存取：http://localhost:3000"