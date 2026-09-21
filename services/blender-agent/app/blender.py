"""
Core — interfaccia con Blender via bpy in modalità headless.

Tutte le funzioni eseguono Blender come sottoprocesso con argv list
(mai shell=True). I path sono sempre validati contro il workspace.
"""

import os
import json
import hashlib
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone

from app.models import (
    BlendFileInfo,
    ChangeRecord,
    VersionMetadata,
)


WORKSPACE = Path(os.environ.get("WORKSPACE_DIR", "/workspace")).resolve()
VERSIONS_DIR = WORKSPACE / "versions"
RENDERS_DIR = WORKSPACE / "renders"
CHANGES_DIR = WORKSPACE / "changes"
ORIGINALS_DIR = WORKSPACE / "originals"
BLENDER_CMD = os.environ.get("BLENDER_HEADLESS_CMD", "blender")


# ─── Confini ───────────────────────────────────────────


def _lazy_ensure_dirs():
    """Tenta di creare le directory di lavoro. Non fallisce se /workspace
    non esiste (es. in CI senza mount del volume)."""
    for d in (VERSIONS_DIR, RENDERS_DIR, CHANGES_DIR, ORIGINALS_DIR):
        try:
            d.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            pass


# NOTA: chiamata all'import — non fallisce in CI
_lazy_ensure_dirs()


# ─── Path validation ───────────────────────────────────


def resolve_input_blend(relative_or_absolute: str) -> Path:
    """
    Risolve un path .blend che DEVE ESISTERE ed essere dentro il workspace.
    Usata per file di input (originali o versioni esistenti).
    """
    p = Path(relative_or_absolute)
    if not p.is_absolute():
        p = WORKSPACE / p
    p = p.resolve()
    if not p.is_relative_to(WORKSPACE):
        raise PermissionError(
            f"Accesso negato: {relative_or_absolute} è fuori dal workspace"
        )
    if not p.exists():
        raise FileNotFoundError(f"File non trovato: {p}")
    return p


def resolve_workspace_output(relative_or_absolute: str, subdir: str = "versions") -> Path:
    """
    Risolve un path di output e lo confina in workspace/<subdir>/.
    Il file PUÒ non esistere ancora (verrà creato).
    Rifiuta path con '..', slash, o path assoluti esterni.

    subdir: "versions" | "renders"
    """
    p = Path(relative_or_absolute)

    # Rifiuta path traversal
    if ".." in p.parts:
        raise PermissionError(f"Path traversal rifiutato: {relative_or_absolute}")

    # Solo nome file, senza slash
    if p.is_absolute():
        raise PermissionError(f"Path assoluto non permesso per output: {relative_or_absolute}")

    allowed = {"versions": VERSIONS_DIR, "renders": RENDERS_DIR}
    base = allowed.get(subdir)
    if base is None:
        raise ValueError(f"subdir deve essere 'versions' o 'renders', non {subdir}")

    out = (base / p).resolve()
    if not out.is_relative_to(base):
        raise PermissionError(
            f"Output fuori dal confine {subdir}: {relative_or_absolute}"
        )
    return out


# ─── File discovery ────────────────────────────────────


def core_list_blend_files() -> list[BlendFileInfo]:
    """Elenca tutti i file .blend nel workspace (ricorsivo)."""
    results: list[BlendFileInfo] = []
    for f in sorted(WORKSPACE.rglob("*.blend")):
        if f.is_file():
            stat = f.stat()
            results.append(
                BlendFileInfo(
                    path=str(f.relative_to(WORKSPACE)),
                    filename=f.name,
                    size_bytes=stat.st_size,
                    modified_iso=datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ).isoformat(),
                )
            )
    return results


# ─── Blender subprocess helper ─────────────────────────


def _run_blender(
    blend_path: Path,
    script_path: str,
    extra_args: list[str] | None = None,
    timeout: int = 300,
) -> str:
    """
    Esegue Blender headless: blender --background <blend> --python <script> [-- <extra_args>].

    Restituisce stdout.
    Mai shell=True.
    """
    cmd = [
        BLENDER_CMD,
        "--background",
        str(blend_path),
        "--python",
        script_path,
    ]
    if extra_args:
        cmd.append("--")
        cmd.extend(extra_args)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Blender exit code {result.returncode}.\n"
            f"STDERR: {result.stderr[-2000:]}\n"
            f"STDOUT: {result.stdout[-2000:]}"
        )
    return result.stdout


# ─── Scene inspection ──────────────────────────────────


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


def core_inspect_scene(blend_path: str) -> dict:
    """
    Apre un file .blend in background, ispeziona la scena, restituisce JSON.
    """
    resolved = resolve_input_blend(blend_path)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(_INSPECT_SCENE_SCRIPT)
        script_path = f.name

    try:
        stdout = _run_blender(resolved, script_path, timeout=120)

        # L'ultima riga di stdout che è JSON valido
        for line in reversed(stdout.strip().split("\n")):
            line = line.strip()
            if line.startswith("{"):
                return json.loads(line)

        raise RuntimeError(f"Nessun output JSON da Blender.\nstdout:\n{stdout[-1000:]}")
    finally:
        os.unlink(script_path)


# ─── Render preview ────────────────────────────────────


_RENDER_PREVIEW_SCRIPT = """
import bpy
import sys
import os

# Argv dopo --
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
output_path = args[0] if len(args) > 0 else "/tmp/render.png"
resolution_x = int(args[1]) if len(args) > 1 else 1920
resolution_y = int(args[2]) if len(args) > 2 else 1080
samples = int(args[3]) if len(args) > 3 else 64
frame = int(args[4]) if len(args) > 4 else 1

bpy.context.scene.render.resolution_x = resolution_x
bpy.context.scene.render.resolution_y = resolution_y
if hasattr(bpy.context.scene, "cycles"):
    bpy.context.scene.cycles.samples = samples
bpy.context.scene.frame_current = frame
bpy.context.scene.render.filepath = output_path
bpy.ops.render.render(write_still=True)
print(f"RENDER_OK:{output_path}")
"""


def core_render_preview(
    blend_path: str,
    output_name: str = "preview.png",
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    samples: int = 64,
    frame: int = 1,
    timeout: int = 600,
) -> str:
    """
    Esegue un render headless del frame corrente.
    output_name è un nome file (es. preview.png), sempre dentro renders/.
    Restituisce il path assoluto dell'immagine renderizzata.
    """
    resolved = resolve_input_blend(blend_path)
    output_path = resolve_workspace_output(output_name, subdir="renders")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(_RENDER_PREVIEW_SCRIPT)
        script_path = f.name

    try:
        stdout = _run_blender(
            resolved,
            script_path,
            extra_args=[
                str(output_path),
                str(resolution_x),
                str(resolution_y),
                str(samples),
                str(frame),
            ],
            timeout=timeout,
        )
        if "RENDER_OK" not in stdout:
            raise RuntimeError(f"Render non completato.\nstdout:\n{stdout[-1000:]}")
        return str(output_path)
    finally:
        os.unlink(script_path)


# ─── Duplicate version ─────────────────────────────────


def core_duplicate_version(
    source_path: str,
    description: str = "",
) -> tuple[str, VersionMetadata]:
    """
    Crea una copia versionata di un .blend in workspace/versions/.

    Restituisce (path_nuovo, metadati).
    """
    resolved = resolve_input_blend(source_path)

    existing = sorted(VERSIONS_DIR.glob("[0-9][0-9][0-9][0-9].blend"))
    next_num = 1
    if existing:
        last = int(existing[-1].stem)
        next_num = last + 1

    new_name = f"{next_num:04d}.blend"
    new_path = VERSIONS_DIR / new_name

    shutil.copy2(resolved, new_path)

    meta = VersionMetadata(
        version_id=new_name.replace(".blend", ""),
        source_blend=str(resolved.relative_to(WORKSPACE)),
        description=description,
        created_iso=datetime.now(timezone.utc).isoformat(),
    )

    return str(new_path), meta


# ─── Apply change script (gated by ENABLE_RAW_PYTHON) ──


_APPLY_SCRIPT_TEMPLATE = """\
import bpy
import sys

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
blend_input = args[0] if len(args) > 0 else ""
blend_output = args[1] if len(args) > 1 else ""

# Carica il file di input
bpy.ops.wm.open_mainfile(filepath=blend_input)

# --- SCRIPT UTENTE (iniettato) ---
{script_content}
# --- FINE SCRIPT UTENTE ---

# Salva output
bpy.ops.wm.save_as_mainfile(filepath=blend_output)
print(f"SAVE_OK:{blend_output}")
"""


def core_apply_blender_script(
    blend_path: str,
    script_content: str,
    output_name: str | None = None,
    description: str = "",
    timeout: int = 300,
) -> tuple[str, ChangeRecord]:
    """
    Esegue uno script Python arbitrario su un file .blend e salva
    il risultato in una nuova versione in workspace/versions/.

    Crea anche l'audit trail in workspace/changes/.

    Restituisce (output_path, ChangeRecord).
    """
    ENABLE_RAW_PYTHON = os.environ.get("ENABLE_RAW_PYTHON", "false").lower() == "true"
    if not ENABLE_RAW_PYTHON:
        raise PermissionError(
            "Rifiutato: ENABLE_RAW_PYTHON non è abilitato. "
            "Per il milestone 0.1 sono disponibili solo: list, inspect, render, duplicate."
        )

    resolved_input = resolve_input_blend(blend_path)

    # Determina output name
    if output_name is None:
        existing = sorted(VERSIONS_DIR.glob("[0-9][0-9][0-9][0-9].blend"))
        next_num = 1
        if existing:
            last = int(existing[-1].stem)
            next_num = last + 1
        output_name = f"{next_num:04d}.blend"

    # Valida output
    resolved_output = resolve_workspace_output(output_name, subdir="versions")

    # Script SHA256 per audit trail
    script_sha256 = hashlib.sha256(script_content.encode()).hexdigest()

    # Scrivi lo script salvato in changes/ per audit
    change_id = output_name.replace(".blend", "")
    script_archive = CHANGES_DIR / f"{change_id}.py"
    script_archive.write_text(
        f"# Script applicato — {change_id}\n"
        f"# Source: {blend_path}\n"
        f"# SHA256: {script_sha256}\n"
        f"# ---\n"
        f"{script_content}\n"
    )

    # Wrapper con lo script utente
    wrapped = _APPLY_SCRIPT_TEMPLATE.format(script_content=script_content)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(wrapped)
        script_path = f.name

    try:
        stdout = _run_blender(
            resolved_input,
            script_path,
            extra_args=[str(resolved_input), str(resolved_output)],
            timeout=timeout,
        )
        if "SAVE_OK" not in stdout:
            raise RuntimeError(f"Salvataggio non confermato.\nstdout:\n{stdout[-1000:]}")
    finally:
        os.unlink(script_path)

    # Audit trail JSON
    change_record = ChangeRecord(
        version_id=change_id,
        source=str(resolved_input.relative_to(WORKSPACE)),
        output=str(resolved_output.relative_to(WORKSPACE)),
        description=description,
        script_sha256=script_sha256,
    )
    json_path = CHANGES_DIR / f"{change_id}.json"
    json_path.write_text(change_record.model_dump_json(indent=2))

    return str(resolved_output), change_record


# ─── Apply restricted: only list/inspect/render/duplicate ──


def core_duplicate_and_render(
    source_path: str,
    description: str = "",
    render_frame: int = 1,
) -> dict:
    """
    Duplica una versione e genera un render preview.
    Operazione combinata per il milestone 0.1.
    """
    version_path, meta = core_duplicate_version(source_path, description)
    output_name = f"preview_{meta.version_id}_f{render_frame:04d}.png"
    render_path = core_render_preview(
        blend_path=version_path,
        output_name=output_name,
        frame=render_frame,
    )
    return {
        "version": meta.model_dump(),
        "render": render_path,
    }