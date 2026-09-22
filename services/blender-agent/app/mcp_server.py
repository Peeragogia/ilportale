"""
Server MCP — espone tutti gli strumenti Blender via Model Context Protocol
in modalità Streamable HTTP (MCP SDK v2).

Include:
- Query: list, inspect, render
- Manipolazione: duplicate_object, move, rotate, hide, show, select
- Versioning: duplicate, apply_script (gated)
"""

import os
import json
import math
from pathlib import Path

from mcp.server import MCPServer

from app.blender import (
    core_list_blend_files as _list_blend_files,
    core_inspect_scene as _inspect_scene,
    core_duplicate_version as _duplicate_version,
    core_render_preview as _render_preview,
    core_apply_blender_script as _apply_script,
    resolve_input_blend,
    get_workspace,
)
from app.blender_tools import (
    core_list_objects as _list_objects,
    core_inspect_object_detail as _inspect_object,
    core_duplicate_object as _duplicate_object,
    core_move_object as _move_object,
    core_rotate_object as _rotate_object,
    core_hide_object as _hide_object,
    core_show_object as _show_object,
    core_select_object as _select_object,
    safe_operate,
)


# ─── MCP Server setup ─────────────────────────────────

mcp = MCPServer(
    name="ilportale-blender",
    instructions=(
        "Strumenti per modificare file Blender (.blend) nel workspace di Il Portale.\n"
        "WORKSPACE: /workspace\n"
        "FILE PRINCIPALE: base/PORTALE.blend\n\n"
        "Tutte le operazioni di modifica sono versionate e non-distruttive.\n"
        "Ogni modifica crea: 1) versione in workspace/versions/ 2) audit in workspace/changes/\n\n"
        "REGOLE:\n"
        "- Usa sempre inspect_object o inspect_scene per trovare il nome esatto degli oggetti\n"
        "- I nomi oggetto sono case-sensitive: 'Tastiera' ≠ 'tastiera'\n"
        "- Dopo una modifica, il version_path è il nuovo file su cui operare\n"
        "- apply_script è disponibile solo se ENABLE_RAW_PYTHON=true (escluso per milestone 0.1)\n"
    ),
)


# ─── Helper ────────────────────────────────────────────

def _resolve(path_or_name: str) -> str:
    """Risolve un path relativo al workspace."""
    p = Path(path_or_name)
    if not p.is_absolute():
        p = get_workspace() / p
    return str(p.resolve())


# ─── QUERY TOOLS ──────────────────────────────────────


@mcp.tool()
def list_blend_files() -> str:
    """
    Elenca tutti i file .blend presenti nel workspace.
    Restituisce un array JSON con path, nome, dimensione e data modifica.
    """
    files = _list_blend_files()
    return json.dumps([f.model_dump() for f in files], indent=2)


@mcp.tool()
def inspect_scene(blend_path: str) -> str:
    """
    Ispeziona un file .blend e restituisce la struttura completa della scena.
    blend_path: percorso relativo (es. 'base/PORTALE.blend') o assoluto.
    """
    try:
        data = _inspect_scene(blend_path)
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(data, indent=2)


@mcp.tool()
def list_objects(blend_path: str) -> str:
    """
    Elenca tutti gli oggetti nella scena di un file .blend.
    Restituisce nome, tipo, posizione, dimensione e visibilità per ogni oggetto.
    blend_path: percorso del .blend.
    """
    try:
        data = _list_objects(blend_path)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps({"objects": data, "count": len(data)}, indent=2)


@mcp.tool()
def inspect_object(blend_path: str, object_name: str) -> str:
    """
    Restituisce i dettagli completi di un singolo oggetto in un file .blend.
    blend_path: percorso del .blend.
    object_name: nome dell'oggetto (case-sensitive).
    Include: posizione, rotazione, scala, dimensioni, materiali,
             vertici/spigoli/facce (se mesh), parent, children.
    """
    try:
        data = _inspect_object(blend_path, object_name)
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(data, indent=2)


# ─── MANIPULATION TOOLS ───────────────────────────────


@mcp.tool()
def duplicate_object(
    blend_path: str,
    object_name: str,
    new_name: str = "",
) -> str:
    """
    Duplica un oggetto all'interno dello stesso file .blend.
    Crea automaticamente una nuova versione del file.

    blend_path: percorso del .blend.
    object_name: nome dell'oggetto da duplicare.
    new_name: nome per la copia (default: {object_name}_copia).

    Restituisce: version_id, version_path, nome del nuovo oggetto, posizione.
    """
    try:
        resolved = _resolve(blend_path)
        if not new_name:
            new_name = f"{object_name}_copia"
        r = safe_operate(
            resolved,
            _duplicate_object,
            [object_name, new_name],
            description=f"Duplica {object_name} -> {new_name}",
            user_request="",
        )
        result = {
            "status": "ok",
            "version_id": r["version_id"],
            "version_path": r["version_path"],
            "new_object": new_name,
            "position": r["result"].get("location"),
        }
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(result, indent=2)


@mcp.tool()
def move_object(
    blend_path: str,
    object_name: str,
    x: float,
    y: float,
    z: float,
) -> str:
    """
    Sposta un oggetto a coordinate assolute (x, y, z).
    Crea automaticamente una nuova versione del file.

    blend_path: percorso del .blend.
    object_name: nome dell'oggetto da spostare.
    x, y, z: coordinate target.

    Restituisce: version_id, nuova posizione.
    """
    try:
        resolved = _resolve(blend_path)
        r = safe_operate(
            resolved,
            _move_object,
            [object_name, x, y, z],
            description=f"Sposta {object_name} a ({x},{y},{z})",
            user_request="",
        )
        result = {
            "status": "ok",
            "version_id": r["version_id"],
            "version_path": r["version_path"],
            "new_position": r["result"].get("location"),
        }
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(result, indent=2)


@mcp.tool()
def rotate_object(
    blend_path: str,
    object_name: str,
    angle_degrees: float,
    axis: str = "Z",
) -> str:
    """
    Ruota un oggetto di un angolo in gradi su un asse.
    Crea automaticamente una nuova versione del file.

    blend_path: percorso del .blend.
    object_name: nome dell'oggetto.
    angle_degrees: angolo in gradi.
    axis: asse di rotazione ('X', 'Y', 'Z', default 'Z').

    Restituisce: version_id, nuova rotazione in radianti.
    """
    try:
        resolved = _resolve(blend_path)
        rad = math.radians(angle_degrees)
        axes = {"X": 0, "Y": 1, "Z": 2}
        idx = axes.get(axis.upper(), 2)
        rot = [0, 0, 0]
        rot[idx] = rad
        r = safe_operate(
            resolved,
            _rotate_object,
            [object_name, rot[0], rot[1], rot[2]],
            description=f"Ruota {object_name} {angle_degrees}° su {axis}",
            user_request="",
        )
        result = {
            "status": "ok",
            "version_id": r["version_id"],
            "version_path": r["version_path"],
            "new_rotation": r["result"].get("rotation"),
        }
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(result, indent=2)


@mcp.tool()
def hide_object(blend_path: str, object_name: str) -> str:
    """
    Nasconde un oggetto nella viewport.
    Crea automaticamente una nuova versione del file.

    blend_path: percorso del .blend.
    object_name: nome dell'oggetto.

    Restituisce: version_id.
    """
    try:
        resolved = _resolve(blend_path)
        r = safe_operate(
            resolved, _hide_object, [object_name],
            description=f"Nascondi {object_name}", user_request="",
        )
        result = {"status": "ok", "version_id": r["version_id"],
                  "version_path": r["version_path"]}
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(result, indent=2)


@mcp.tool()
def show_object(blend_path: str, object_name: str) -> str:
    """
    Mostra un oggetto precedentemente nascosto.
    Crea automaticamente una nuova versione del file.

    blend_path: percorso del .blend.
    object_name: nome dell'oggetto.

    Restituisce: version_id.
    """
    try:
        resolved = _resolve(blend_path)
        r = safe_operate(
            resolved, _show_object, [object_name],
            description=f"Mostra {object_name}", user_request="",
        )
        result = {"status": "ok", "version_id": r["version_id"],
                  "version_path": r["version_path"]}
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(result, indent=2)


@mcp.tool()
def select_object(blend_path: str, object_name: str) -> str:
    """
    Seleziona un oggetto nel file .blend.
    Crea una nuova versione con la selezione salvata.

    blend_path: percorso del .blend.
    object_name: nome dell'oggetto.

    Restituisce: version_id.
    """
    try:
        resolved = _resolve(blend_path)
        r = safe_operate(
            resolved, _select_object, [object_name],
            description=f"Seleziona {object_name}", user_request="",
        )
        result = {"status": "ok", "version_id": r["version_id"],
                  "version_path": r["version_path"]}
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    return json.dumps(result, indent=2)


# ─── RENDER TOOLS ─────────────────────────────────────


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

    blend_path: percorso del .blend.
    resolution_x, resolution_y: risoluzione (default 1920x1080).
    samples: campioni per Cycles (default 64, riduci per velocità).
    frame: fotogramma da renderizzare (default 1).
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


# ─── VERSIONING & ADVANCED ────────────────────────────


@mcp.tool()
def duplicate_version(
    source_path: str,
    description: str = "",
) -> str:
    """
    Crea una copia versionata di un file .blend.
    Utile per snapshot manuali.

    source_path: percorso del .blend originale.
    description: descrizione della modifica.

    Restituisce path della nuova versione e metadati.
    """
    try:
        path, meta = _duplicate_version(source_path, description)
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        return json.dumps({"error": str(e)}, indent=2)
    result = {"path": path, "metadata": meta.model_dump()}
    return json.dumps(result, indent=2)


@mcp.tool()
def apply_script(
    blend_path: str,
    script_content: str,
    description: str = "",
) -> str:
    """
    [GATED] Applica uno script Python arbitrario a un file .blend.
    Crea una nuova versione in workspace/versions/ e registra l'audit trail.
    Disponibile solo se ENABLE_RAW_PYTHON=true.

    blend_path: percorso del .blend di input.
    script_content: codice Python da eseguire (usa bpy per modificare la scena).
    description: descrizione della modifica.
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
        {"status": "ok", "output": output_path,
         "change": change_record.model_dump()},
        indent=2,
    )


# ─── ASGI entrypoint ────────────────────────────

# MCPServer espone un'app Starlette per Streamable HTTP
mcp_app = mcp.streamable_http_app()


def main():
    """Avvia MCP server standalone (porta 8200)."""
    import uvicorn
    mcp_port = int(os.environ.get("MCP_PORT", "8200"))
    uvicorn.run(mcp_app, host="0.0.0.0", port=mcp_port, log_level="info")


if __name__ == "__main__":
    main()