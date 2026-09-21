"""
FastAPI HTTP entrypoint.

Espone:
- API REST su porta API_PORT (default 8100)
- Lancia MCP server su thread separato su porta MCP_PORT (default 8200)
"""

import os
import json
import threading
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.blender import (
    list_blend_files,
    inspect_scene,
    render_preview,
    duplicate_version,
    apply_blender_script,
)
from app.models import (
    RenderRequest,
    ChangeScript,
    VersionMetadata,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Avvia MCP server su thread separato all'avvio."""
    mcp_port = int(os.environ.get("MCP_PORT", "8200"))
    t = threading.Thread(
        target=_start_mcp,
        args=(mcp_port,),
        daemon=True,
    )
    t.start()
    yield


app = FastAPI(
    title="Il Portale — Blender Agent API",
    version="0.1.0",
    lifespan=lifespan,
)


def _start_mcp(port: int):
    """Lancia MCP server in modalità Streamable HTTP."""
    from app.mcp_server import mcp_app
    uvicorn.run(
        mcp_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )


# ─── Health ────────────────────────────────────────────


@app.get("/health")
async def health():
    return {"status": "ok", "service": "blender-agent", "version": "0.1.0"}


# ─── Files ─────────────────────────────────────────────


@app.get("/files")
async def get_files():
    files = list_blend_files()
    return {
        "count": len(files),
        "files": [f.model_dump() for f in files],
    }


# ─── Scene ─────────────────────────────────────────────


@app.get("/scene/{file:path}")
async def get_scene(file: str):
    try:
        data = inspect_scene(file)
        return {"file": file, "scene": data}
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Render ────────────────────────────────────────────


@app.post("/render")
async def post_render(req: RenderRequest):
    try:
        output = render_preview(
            blend_path=req.blend_path,
            output_path=req.output_dir or f"/workspace/renders/preview_{req.blend_path.replace('/', '_')}.png",
            resolution_x=req.resolution_x,
            resolution_y=req.resolution_y,
            samples=req.samples,
            frame=req.frame,
        )
        return {"status": "ok", "output": output}
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Versions ──────────────────────────────────────────


@app.post("/versions")
async def create_version(req: ChangeScript):
    """Crea una nuova versione applicando uno script di modifica."""
    try:
        # Prima crea versione di partenza
        version_path, meta = duplicate_version(
            source_path=req.source_blend,
            description=req.description,
        )

        # Applica script sulla nuova versione
        output = apply_blender_script(
            blend_path=version_path,
            script_content=req.script_content,
            output_path=version_path,  # sovrascrive la copia
        )

        return {
            "status": "ok",
            "version": meta.version_id,
            "path": output,
            "metadata": meta.model_dump(),
        }
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Entrypoint ────────────────────────────────────────


def main():
    api_port = int(os.environ.get("API_PORT", "8100"))
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=api_port,
        log_level="info",
    )


if __name__ == "__main__":
    main()