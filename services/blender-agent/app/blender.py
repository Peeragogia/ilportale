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


WORKSPACE = None  # lazy, letto via get_workspace()
VERSIONS_DIR = None
RENDERS_DIR = None
CHANGES_DIR = None
ORIGINALS_DIR = None
BLENDER_CMD = os.environ.get("BLENDER_HEADLESS_CMD", "blender")

_WORKSPACE_CACHE = {}


def get_workspace() -> Path:
    """Restituisce il workspace path, leggendo WORKSPACE_DIR da environ.
    Usa una cache che si invalida se l'env cambia."""
    ws_str = os.environ.get("WORKSPACE_DIR", "/workspace")
    cached = _WORKSPACE_CACHE.get("path")
    cached_env = _WORKSPACE_CACHE.get("env")
    if cached is not None and cached_env == ws_str:
        return cached
    p = Path(ws_str).resolve()
    _WORKSPACE_CACHE["path"] = p
    _WORKSPACE_CACHE["env"] = ws_str
    return p


def get_versions_dir() -> Path:
    return get_workspace() / "versions"


def get_renders_dir() -> Path:
    return get_workspace() / "renders"


def get_changes_dir() -> Path:
    return get_workspace() / "changes"


def get_originals_dir() -> Path:
    return get_workspace() / "originals"


# ─── Confini ───────────────────────────────────────────


def _lazy_ensure_dirs():
    """Tenta di creare le directory di lavoro. Non fallisce se /workspace
    non esiste (es. in CI senza mount del volume)."""
    for d in (get_versions_dir(), get_renders_dir(), get_changes_dir(), get_originals_dir()):
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
        p = get_workspace() / p
    p = p.resolve()
    if not p.is_relative_to(get_workspace()):
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
    Rifiuta path con '..', slash, o path assoluti.

    subdir: "versions" | "renders"
    """
    p = Path(relative_or_absolute)

    # Rifiuta path traversal
    if ".." in p.parts:
        raise PermissionError(f"Path traversal rifiutato: {relative_or_absolute}")

    # Rifiuta path assoluti
    if p.is_absolute():
        raise PermissionError(f"Path assoluto non permesso per output: {relative_or_absolute}")

    # Rifiuta path con componenti multipli (solo nome file)
    if len(p.parts) > 1:
        raise PermissionError(f"Output con sottodirectory non permesso: {relative_or_absolute}")

    allowed = {"versions": get_versions_dir(), "renders": get_renders_dir()}
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
    for f in sorted(get_workspace().rglob("*.blend")):
        if f.is_file():
            stat = f.stat()
            results.append(
                BlendFileInfo(
                    path=str(f.relative_to(get_workspace())),
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
    script_path: str | None,
    extra_args: list[str] | None = None,
    timeout: int = 300,
) -> str:
    """
    Esegue Blender headless.
    Se script_path è None, usa solo CLI flags (es. -F PNG -o ... -f 1).
    Altrimenti: blender --background <blend> --python <script> [-- <extra_args>].
    Mai shell=True.
    """
    cmd = [
        BLENDER_CMD,
        "--background",
        str(blend_path),
    ]
    if script_path:
        cmd.extend(["--python", script_path])
    if extra_args:
        if script_path:
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

# Render usando CLI -F PNG bypassa il bug API di Blender 5.2
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
output_path = args[0] if len(args) > 0 else "/tmp/render.png"
frame = int(args[1]) if len(args) > 1 else 1

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
    Esegue un render headless del frame corrente usando CLI flags.
    output_name è un nome file (es. preview.png), sempre dentro renders/.
    Restituisce il path assoluto dell'immagine renderizzata.
    """
    resolved = resolve_input_blend(blend_path)
    # Sostituisci .png con padding per formato Blender (es: preview_ → preview_0001.png)
    stem = Path(output_name).stem
    output_path = resolve_workspace_output(output_name, subdir="renders")

    # Usa CLI flags direttamente: -F PNG bypassa bug Blender 5.2
    # Blender aggiunge automaticamente padding frame (es. _0001) con -f
    # Output: /renders/preview_0001.png
    out_dir = str(output_path.parent)
    out_base = stem + "_"

    stdout = _run_blender(
        resolved,
        script_path=None,
        extra_args=[
            "-F", "PNG",
            "-o", os.path.join(out_dir, out_base),
            "-f", str(frame),
        ],
        timeout=timeout,
    )

    if "Saved:" not in stdout and "RENDER_OK" not in stdout:
        raise RuntimeError(f"Render non completato.\nstdout:\n{stdout[-1000:]}")

    # Trova il file renderizzato
    rendered = sorted(output_path.parent.glob(stem + "_*.png"))
    if rendered:
        return str(rendered[-1])
    return str(output_path)


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

    existing = sorted(get_versions_dir().glob("[0-9][0-9][0-9][0-9].blend"))
    next_num = 1
    if existing:
        last = int(existing[-1].stem)
        next_num = last + 1

    new_name = f"{next_num:04d}.blend"
    new_path = get_versions_dir() / new_name

    shutil.copy2(resolved, new_path)

    meta = VersionMetadata(
        version_id=new_name.replace(".blend", ""),
        source_blend=str(resolved.relative_to(get_workspace())),
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
        existing = sorted(get_versions_dir().glob("[0-9][0-9][0-9][0-9].blend"))
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
    script_archive = get_changes_dir() / f"{change_id}.py"
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
        source=str(resolved_input.relative_to(get_workspace())),
        output=str(resolved_output.relative_to(get_workspace())),
        description=description,
        script_sha256=script_sha256,
    )
    json_path = get_changes_dir() / f"{change_id}.json"
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