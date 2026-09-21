"""
Core — interfaccia con Blender via bpy in modalità headless.

Tutte le funzioni assumono di essere eseguite dentro un'istanza di
Blender lanciata con `blender --background file.blend --python script.py`.
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from app.models import (
    BlendFileInfo,
    SceneInfo,
    ObjectInfo,
    ObjectType,
    VersionMetadata,
)


WORKSPACE = Path(os.environ.get("WORKSPACE_DIR", "/workspace"))
BLENDER_HEADLESS = os.environ.get(
    "BLENDER_HEADLESS_CMD", "blender --background"
)


# ─── File discovery ────────────────────────────────────


def list_blend_files() -> list[BlendFileInfo]:
    """Elenca tutti i file .blend nel workspace."""
    results: list[BlendFileInfo] = []
    for f in sorted(WORKSPACE.rglob("*.blend")):
        if f.is_file():
            stat = f.stat()
            results.append(
                BlendFileInfo(
                    path=str(f.relative_to(WORKSPACE)),
                    filename=f.name,
                    size_bytes=stat.st_size,
                    modified_iso=stat.st_mtime,
                )
            )
    return results


def resolve_blend(relative_or_absolute: str) -> Path:
    """Risolve un path .blend, assicurandosi sia dentro workspace."""
    p = Path(relative_or_absolute)
    if not p.is_absolute():
        p = WORKSPACE / p
    p = p.resolve()
    if not str(p).startswith(str(WORKSPACE.resolve())):
        raise PermissionError(f"Accesso negato: {relative_or_absolute} è fuori dal workspace")
    if not p.exists():
        raise FileNotFoundError(f"File non trovato: {p}")
    return p


# ─── Scene inspection (via headless Blender) ────────────


_INSPECT_SCENE_SCRIPT = """
import bpy
import json

data = {
    "name": bpy.context.scene.name,
    "objects": [],
    "camera": bpy.context.scene.camera.name if bpy.context.scene.camera else None,
    "world": bpy.context.scene.world.name if bpy.context.scene.world else None,
}

for obj in bpy.context.scene.objects:
    obj_data = {
        "name": obj.name,
        "type": obj.type,
        "location": tuple(obj.location),
        "rotation": tuple(obj.rotation_euler),
        "scale": tuple(obj.scale),
        "dimensions": tuple(obj.dimensions),
        "materials": [m.name for m in obj.data.materials if m] if hasattr(obj, "data") and hasattr(obj.data, "materials") else [],
        "parent": obj.parent.name if obj.parent else None,
    }
    data["objects"].append(obj_data)

data["object_count"] = len(data["objects"])
print(json.dumps(data))
"""


def inspect_scene(blend_path: str) -> dict:
    """
    Apre un file .blend in background, ispeziona la scena, restituisce JSON.
    """
    resolved = resolve_blend(blend_path)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as f:
        f.write(_INSPECT_SCENE_SCRIPT)
        script_path = f.name

    try:
        cmd = f"{BLENDER_HEADLESS} {resolved} --python {script_path}"
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Blender exited with code {result.returncode}: {result.stderr}"
            )

        # L'ultima riga di stdout che è JSON valido
        for line in reversed(result.stdout.strip().split("\n")):
            line = line.strip()
            if line.startswith("{"):
                return json.loads(line)

        raise RuntimeError(
            f"Nessun output JSON da Blender. stdout:\n{result.stdout}"
        )
    finally:
        os.unlink(script_path)


# ─── Render preview ────────────────────────────────────


_RENDER_PREVIEW_SCRIPT = """
import bpy
import sys
import os

output_path = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/render.png"
resolution_x = int(sys.argv[sys.argv.index("--") + 2]) if "--" in sys.argv else 1920
resolution_y = int(sys.argv[sys.argv.index("--") + 3]) if "--" in sys.argv else 1080
samples = int(sys.argv[sys.argv.index("--") + 4]) if "--" in sys.argv else 64
frame = int(sys.argv[sys.argv.index("--") + 5]) if "--" in sys.argv else 1

bpy.context.scene.render.resolution_x = resolution_x
bpy.context.scene.render.resolution_y = resolution_y
bpy.context.scene.cycles.samples = samples if hasattr(bpy.context.scene, "cycles") else 64
bpy.context.scene.frame_current = frame
bpy.context.scene.render.filepath = output_path
bpy.ops.render.render(write_still=True)
print(f"RENDER_OK:{output_path}")
"""


def render_preview(
    blend_path: str,
    output_path: str = "/workspace/renders/preview.png",
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    samples: int = 64,
    frame: int = 1,
    timeout: int = 600,
) -> str:
    """
    Esegue un render headless del frame corrente.

    Restituisce il path assoluto dell'immagine renderizzata.
    """
    resolved = resolve_blend(blend_path)
    output_abs = str(Path(output_path).resolve())

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as f:
        f.write(_RENDER_PREVIEW_SCRIPT)
        script_path = f.name

    try:
        cmd = (
            f"{BLENDER_HEADLESS} {resolved} --python {script_path} -- "
            f"{output_abs} {resolution_x} {resolution_y} {samples} {frame}"
        )
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Render fallito con codice {result.returncode}: {result.stderr}"
            )
        if "RENDER_OK" not in result.stdout:
            raise RuntimeError(
                f"Render non completato. stdout:\n{result.stdout}"
            )
        return output_abs
    finally:
        os.unlink(script_path)


# ─── Apply change script ───────────────────────────────


def apply_blender_script(
    blend_path: str,
    script_content: str,
    output_path: str,
    timeout: int = 300,
) -> str:
    """
    Esegue uno script Python arbitrario su un file .blend in modalità
    headless e salva il risultato in output_path.

    * input_path letto come primo argomento dopo `--`
    * output_path passato come secondo argomento dopo `--`
    * lo script si aspetta le variabili blend_input e blend_output
    """
    resolved_input = resolve_blend(blend_path)
    resolved_output = resolve_blend(output_path)

    wrapper = f"""
import bpy
import sys

blend_input = sys.argv[sys.argv.index("--") + 1]
blend_output = sys.argv[sys.argv.index("--") + 2]

# Carica il file di input
bpy.ops.wm.open_mainfile(filepath=blend_input)

# Script utente
{script_content}

# Salva output
bpy.ops.wm.save_as_mainfile(filepath=blend_output)
print(f"SAVE_OK:{{blend_output}}")
"""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as f:
        f.write(wrapper)
        script_path = f.name

    try:
        cmd = (
            f"{BLENDER_HEADLESS} --python {script_path} -- "
            f"{resolved_input} {resolved_output}"
        )
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Script fallito (exit {result.returncode}): {result.stderr}"
            )
        if "SAVE_OK" not in result.stdout:
            raise RuntimeError(
                f"Salvataggio non confermato. stdout:\n{result.stdout}"
            )
        return str(resolved_output)
    finally:
        os.unlink(script_path)


# ─── Version management ────────────────────────────────


def duplicate_version(
    source_path: str,
    description: str = "",
) -> tuple[str, VersionMetadata]:
    """
    Crea una copia versionata di un .blend in workspace/versions/.

    Restituisce (path_nuovo, metadati).
    """
    resolved = resolve_blend(source_path)

    versions_dir = WORKSPACE / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)

    existing = sorted(versions_dir.glob("[0-9][0-9][0-9][0-9].blend"))
    next_num = 1
    if existing:
        last = int(existing[-1].stem)
        next_num = last + 1

    new_name = f"{next_num:04d}.blend"
    new_path = versions_dir / new_name

    import shutil
    shutil.copy2(resolved, new_path)

    meta = VersionMetadata(
        version_id=new_name.replace(".blend", ""),
        source_blend=str(resolved.relative_to(WORKSPACE)),
        description=description,
        created_iso=str(new_path.stat().st_mtime),
    )

    return str(new_path), meta