#!/bin/bash
set -e

# Avvia il backend Python in background
echo "[entrypoint] Starting blender-agent backend..."
cd /app
/venv/bin/python -m app.api &
API_PID=$!

# Avvia Blender web (s6 init di linuxserver/blender)
echo "[entrypoint] Starting Blender web UI..."
/init

# Se si arriva qui (es. /init termina), kill backend
kill $API_PID 2>/dev/null || true