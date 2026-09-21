"""
Server MCP — espone gli strumenti Blender via Model Context Protocol
in modalità Streamable HTTP.

L'SDK MCP ufficiale fornisce già ASGI compatibility.
Montiamo l'app FastMCP su una route e la esponiamo via uvicorn.
"""

import os
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializationOptions

from app.blender import (
    list_blend_files,
    inspect_scene,
    duplicate_version,
    render_preview,
    apply_blender_script as core_apply_script,
)


# ─── MCP Server setup ─────────────────────────────────

mcp = FastMCP(
    "ilportale-blender",
    instructions=(
        "Strumenti per interrogare e modificare file Blender (.blend) "
        "all'interno del workspace di Il Portale. "
        "Tutte le operazioni sono non-distruttive sugli originali. "
        "Il workspace è /workspace."
    ),
)


# ─── Helpers ───────────────────────────────────────────


def _run_blender_script(script_path: str, blend_path: str, *args: str) -> str:
    """Esegue Blender headless con uno script e argomenti aggiuntivi."""
    import subprocess
    import tempfile

    resolved_blend = blend_path  # assume già risolto in chiamante

    if args:
        cmd = f"blender --background {resolved_blend} --python {script_path} -- {' '.join(args)}"
    else:
        cmd = f"blender --background {resolved_blend} --python {script_path}"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"Blender exit {result.returncode}: {result.stderr}")
    return result.stdout


# ─── Strumenti MCP ────────────────────────────────────


@mcp.tool()
def list_blend_files() -> str:
    """
    Elenca tutti i file .blend presenti nel workspace.
    Restituisce un array JSON con path, nome, dimensione e data modifica.
    """
    files = list_blend_files()
    return json.dumps([f.model_dump() for f in files], indent=2)


@mcp.tool()
def inspect_blend(path: str) -> str:
    """
    Ispeziona un file .blend e restituisce la struttura completa della scena.
    path: percorso relativo al workspace o assoluto (es. originals/file.blend)
    """
    data = inspect_scene(path)
    return json.dumps(data, indent=2)


@mcp.tool()
def inspect_scene_tool(path: str) -> str:
    """
    Alias per inspect_blend. Ispeziona la scena di un file .blend.
    Restituisce oggetti, materiali, camera, luci, statistiche.
    """
    return inspect_blend(path)


@mcp.tool()
def inspect_object(path: str, object_name: str) -> str:
    """
    Restituisce i dettagli di un singolo oggetto in un file .blend.
    path: percorso del .blend
    object_name: nome dell'oggetto (case-sensitive)
    """
    data = inspect_scene(path)
    for obj in data.get("objects", []):
        if obj["name"] == object_name:
            return json.dumps(obj, indent=2)
    return json.dumps({"error": f"Oggetto '{object_name}' non trovato"}, indent=2)


@mcp.tool()
def duplicate_version_tool(
    source_path: str,
    description: str = "",
) -> str:
    """
    Crea una copia versionata di un file .blend.
    source_path: percorso del .blend originale
    description: descrizione della modifica
    Restituisce path della nuova versione e metadati.
    """
    path, meta = duplicate_version(source_path, description)
    result = {"path": path, "metadata": meta.model_dump()}
    return json.dumps(result, indent=2)


@mcp.tool()
def render_preview_tool(
    blend_path: str,
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    samples: int = 64,
    frame: int = 1,
) -> str:
    """
    Genera un render preview di un file .blend.
    Restituisce il path dell'immagine renderizzata.
    """
    output = f"/workspace/renders/preview_{Path(blend_path).stem}_f{frame:04d}.png"
    result = render_preview(
        blend_path=blend_path,
        output_path=output,
        resolution_x=resolution_x,
        resolution_y=resolution_y,
        samples=samples,
        frame=frame,
    )
    return json.dumps({"status": "ok", "output": result}, indent=2)


@mcp.tool()
def apply_blender_script_tool(
    blend_path: str,
    script_content: str,
    output_name: str = "",
) -> str:
    """
    APPLICA UNO SCRIPT PYTHON A UN FILE .BLEND — OPERAZIONE SENSIBILE.

    Esegue script_content come codice Blender Python (bpy) su blend_path
    e salva il risultato come nuova versione.

    blend_path: percorso del .blend di input
    script_content: codice Python da eseguire (usa bpy per modificare la scena)
    output_name: nome opzionale per l'output (default: auto-versionato)

    Non può sovrascrivere file fuori dal workspace.
    Lo script riceve blend_input e blend_output come variabili.
    """
    import tempfile

    from app.blender import resolve_blend

    # Determina output
    versions_dir = Path(os.environ.get("WORKSPACE_DIR", "/workspace")) / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)

    if not output_name:
        existing = sorted(versions_dir.glob("[0-9][0-9][0-9][0-9].blend"))
        next_num = 1
        if existing:
            last = int(existing[-1].stem)
            next_num = last + 1
        output_name = f"{next_num:04d}.blend"

    output_path = str(versions_dir / output_name)

    # Validazione path sicurezza (tramite core resolve)
    resolved_output = resolve_blend(output_path)

    result = core_apply_script(
        blend_path=blend_path,
        script_content=script_content,
        output_path=output_path,
    )

    return json.dumps({"status": "ok", "output": result}, indent=2)


# ─── ASGI entrypoint ──────────────────────────────────

# FastMCP espone già un'app ASGI pronta per uvicorn
mcp_app = mcp.get_asgi_app()


def main():
    """Avvia MCP server standalone."""
    import uvicorn

    mcp_port = int(os.environ.get("MCP_PORT", "8200"))
    uvicorn.run(mcp_app, host="0.0.0.0", port=mcp_port, log_level="info")


if __name__ == "__main__":
    main()