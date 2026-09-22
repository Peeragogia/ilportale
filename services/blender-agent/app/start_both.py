"""Startup script — runs both API (8100) and MCP (8200)."""
import os, subprocess, sys, time

api_port = os.environ.get("API_PORT", "8100")
mcp_port = os.environ.get("MCP_PORT", "8200")

# Start both as subprocesses
api_proc = subprocess.Popen(
    [sys.executable, "-m", "app.api"],
    stdout=open("/tmp/api.log", "w"),
    stderr=subprocess.STDOUT,
)
mcp_proc = subprocess.Popen(
    [sys.executable, "-m", "app.mcp_server"],
    stdout=open("/tmp/mcp.log", "w"),
    stderr=subprocess.STDOUT,
)

print(f"Started API (pid={api_proc.pid}) on port {api_port}")
print(f"Started MCP (pid={mcp_proc.pid}) on port {mcp_port}")

# Wait for both
try:
    api_rc = api_proc.wait()
    print(f"API exited with code {api_rc}")
except KeyboardInterrupt:
    api_proc.terminate()
    mcp_proc.terminate()
    print("Shutting down...")