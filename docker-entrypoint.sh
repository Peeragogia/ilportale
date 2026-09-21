#!/bin/bash
set -e

# Se riceve argomenti (da docker-compose command:), esegui quelli
# Esempio: docker-compose command: ["/venv/bin/python", "-m", "app.api"]
# Usato da blender-api e blender-mcp
if [ $# -gt 0 ]; then
    exec "$@"
fi

# Default: avvia backend + Blender GUI
echo "[entrypoint] Starting backend..."
cd /app
/venv/bin/python -m app.api &
BACKEND_PID=$!

echo "[entrypoint] Backend started (PID $BACKEND_PID). Starting Blender GUI..."
exec /init