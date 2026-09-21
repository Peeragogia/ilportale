#!/bin/bash
set -e

echo "[entrypoint] Starting backend API..."
cd /app
/venv/bin/python -m app.api &
BACKEND_PID=$!

echo "[entrypoint] Backend started (PID $BACKEND_PID). Starting Blender GUI..."
exec /init