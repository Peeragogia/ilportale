"""
Server MCP — espone strumenti Blender via Model Context Protocol
in modalità Streamable HTTP (MCP SDK v2).

Avviabile come processo standalone su MCP_PORT (default 8200).
"""

import os
import json
from pathlib import Path

from mcp.server import MCPServer

from app.blender import (
    core_list_blend_files as _list_blend_files,
    core_inspect_scene as _inspect_scene,
    core_duplicate_version as _duplicate_version,
    core_render_preview as _render_preview,
    core_apply_blender_script as _apply_script,
)


# ─── MCP Server setup ─────────────────────────────────

mcp = MCPServer(
    name="ilportale-blender",
    instructions=(
        "Strumenti per interrogare file Blender (.blend) "
        "all'interno del workspace di Il Portale. "
        "Tutte le operazioni sono non-distruttive sugli originali. "
        "Il workspace è /workspace.\n\n"
        "Per il milestone 0.1 sono disponibili: list, inspect, render, duplicate.\n"
        "apply_script è disponibile solo se ENABLE_RAW_PYTHON è true."
    ),
)


# ─── Strumenti MCP ────────────────────────────────────


@mcp.tool()
def list_blend_files() -> str:
    """
    Elenca tutti i file .blend presenti nel workspace.
    Restituisce un array JSON con path, nome, dimensione e data modifica.
    """
    files = _list_blend_files()
    return json.dumps([f.model_dump() for f in files], indent=2)


@mcp.tool()
def inspect_blend(path: str) -> str:
    """
    Ispeziona un file .blend e restituisce la struttura completa della scena.
    path: percorso relativo al workspace o assoluto (es. originals/file.blend)
    """
    try:
        data = _inspect_scene(path)
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(data, indent=2)


@mcp.tool()
def inspect_object(path: str, object_name: str) -> str:
    """
    Restituisce i dettagli di un singolo oggetto in un file .blend.
    path: percorso del .blend
    object_name: nome dell'oggetto (case-sensitive)
    """
    try:
        data = _inspect_scene(path)
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        return json.dumps({"error": str(e)}, indent=2)
    for obj in data.get("objects", []):
        if obj["name"] == object_name:
            return json.dumps(obj, indent=2)
    return json.dumps({"error": f"Oggetto '{object_name}' non trovato"}, indent=2)


@mcp.tool()
def duplicate_version(
    source_path: str,
    description: str = "",
) -> str:
    """
    Crea una copia versionata di un file .blend.
    source_path: percorso del .blend originale
    description: descrizione della modifica
    Restituisce path della nuova versione e metadati.
    """
    try:
        path, meta = _duplicate_version(source_path, description)
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        return json.dumps({"error": str(e)}, indent=2)
    result = {"path": path, "metadata": meta.model_dump()}
    return json.dumps(result, indent=2)


@mcp.tool()
def render_preview(
    blend_path: str,
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    samples: int = 64,
    frame: int = 1,
) -> str:
    """
    Genera un render preview di un file .blend.
    Restituisce il path dell'immagine renderizzata (sempre in workspace/renders/).
    """
    try:
        output_name = f"preview_{Path(blend_path).stem}_f{frame:04d}.png"
        result = _render_preview(
            blend_path=blend_path,
            output_name=output_name,
            resolution_x=resolution_x,
            resolution_y=resolution_y,
            samples=samples,
            frame=frame,
        )
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps({"status": "ok", "output": result}, indent=2)


@mcp.tool()
def apply_script(
    blend_path: str,
    script_content: str,
    description: str = "",
) -> str:
    """
    [GATED] Applica uno script Python arbitrario a un file .blend.

    Crea una nuova versione in workspace/versions/ e registra l'audit trail
    in workspace/changes/.
    Disponibile solo se ENABLE_RAW_PYTHON=true.

    blend_path: percorso del .blend di input
    script_content: codice Python da eseguire (usa bpy per modificare la scena)
    description: descrizione della modifica
    """
    try:
        output_path, change_record = _apply_script(
            blend_path=blend_path,
            script_content=script_content,
            description=description,
        )
    except (PermissionError, FileNotFoundError, RuntimeError) as e:
        return json.dumps({"error": str(e)}, indent=2)

    return json.dumps(
        {
            "status": "ok",
            "output": output_path,
            "change": change_record.model_dump(),
        },
        indent=2,
    )


# ─── ASGI entrypoint (per uvicorn) ────────────────────

# MCPServer expone un'app Starlette pronta per uvicorn
mcp_app = mcp.get_asgi_app()


def main():
    """Avvia MCP server standalone."""
    import uvicorn

    mcp_port = int(os.environ.get("MCP_PORT", "8200"))
    uvicorn.run(mcp_app, host="0.0.0.0", port=mcp_port, log_level="info")


if __name__ == "__main__":
    main()