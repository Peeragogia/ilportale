"""
FastAPI HTTP entrypoint per Il Portale — Blender Agent API.

Processo standalone, NON avvia più MCP (che è servizio separato).
Espone API REST su API_PORT (default 8100).
"""

import os
import json
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from app.blender import (
    core_list_blend_files,
    core_inspect_scene,
    core_render_preview,
    core_duplicate_version,
    core_apply_blender_script,
)
from app.models import (
    RenderRequest,
    ChangeScript,
)


app = FastAPI(
    title="Il Portale — Blender Agent API",
    version="0.1.0",
)


# ─── Health ────────────────────────────────────────────


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "blender-api",
        "version": "0.1.0",
        "features": {
            "list": True,
            "inspect": True,
            "render": True,
            "duplicate": True,
            "apply_script": os.environ.get("ENABLE_RAW_PYTHON", "false").lower() == "true",
        },
    }


# ─── Files ─────────────────────────────────────────────


@app.get("/files")
async def get_files():
    files = core_list_blend_files()
    return {
        "count": len(files),
        "files": [f.model_dump() for f in files],
    }


# ─── Scene ─────────────────────────────────────────────


@app.get("/scene/{file:path}")
async def get_scene(file: str):
    try:
        data = core_inspect_scene(file)
        return {"file": file, "scene": data}
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Render ────────────────────────────────────────────


@app.post("/render")
async def post_render(req: RenderRequest):
    try:
        output_name = f"preview_{Path(req.blend_path).stem}_{req.frame:04d}.png"
        output = core_render_preview(
            blend_path=req.blend_path,
            output_name=output_name,
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
    """Crea una nuova versione duplicando e applicando uno script."""
    try:
        if req.script_content:
            # Applica script (gated da ENABLE_RAW_PYTHON)
            output_path, change_record = core_apply_blender_script(
                blend_path=req.source_blend,
                script_content=req.script_content,
                description=req.description,
            )
            return {
                "status": "ok",
                "path": output_path,
                "change": change_record.model_dump(),
            }
        else:
            # Solo duplica
            path, meta = core_duplicate_version(
                source_path=req.source_blend,
                description=req.description,
            )
            return {
                "status": "ok",
                "version": meta.version_id,
                "path": path,
                "metadata": meta.model_dump(),
            }
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/versions/duplicate")
async def duplicate(source_blend: str, description: str = ""):
    """
    Crea una copia versionata di un .blend senza applicare script.
    Operazione sicura (non raw Python).
    """
    try:
        path, meta = core_duplicate_version(
            source_path=source_blend,
            description=description,
        )
        return {
            "status": "ok",
            "version": meta.version_id,
            "path": path,
            "metadata": meta.model_dump(),
        }
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Changes / Audit trail ────────────────────────────


@app.get("/changes")
async def list_changes():
    """Elenca tutti i change record archiviati."""
    changes_dir = Path(os.environ.get("WORKSPACE_DIR", "/workspace")) / "changes"
    if not changes_dir.exists():
        return {"count": 0, "changes": []}
    records = []
    for f in sorted(changes_dir.glob("*.json")):
        records.append(json.loads(f.read_text()))
    return {"count": len(records), "changes": records}


@app.get("/changes/{change_id}")
async def get_change(change_id: str):
    """Restituisce il change record e lo script associato."""
    changes_dir = Path(os.environ.get("WORKSPACE_DIR", "/workspace")) / "changes"
    json_path = changes_dir / f"{change_id}.json"
    py_path = changes_dir / f"{change_id}.py"
    if not json_path.exists():
        raise HTTPException(status_code=404, detail=f"Change {change_id} non trovato")
    record = json.loads(json_path.read_text())
    script = py_path.read_text() if py_path.exists() else None
    return {"record": record, "script": script}


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
    # Serve per il startup script
    main()