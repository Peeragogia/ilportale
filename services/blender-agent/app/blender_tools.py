"""
Blender manipulation tools — deterministic bpy operations in headless mode.

Ogni funzione genera uno script bpy, lo esegue come sottoprocesso
(blender --background ... --python ...), salva una nuova versione
e registra l'audit trail.
"""

import os
import json
import hashlib
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

from app.blender import (
    get_workspace,
    get_versions_dir,
    get_renders_dir,
    get_changes_dir,
    resolve_input_blend,
    resolve_workspace_output,
)


BLENDER_CMD = os.environ.get("BLENDER_HEADLESS_CMD", "blender")
_OPERATION_SEQ = 0


def _next_id() -> str:
    global _OPERATION_SEQ
    _OPERATION_SEQ += 1
    return f"{datetime.now(tz=timezone.utc).strftime('%Y%m%d-%H%M%S')}-{_OPERATION_SEQ:03d}"


def _run_blender(blend_path: Path, script_path: str,
                 extra_args: list[str] | None = None,
                 timeout: int = 300) -> str:
    """Run blender headless, return stdout."""
    cmd = [
        BLENDER_CMD, "--background", str(blend_path),
        "--python", script_path,
    ]
    if extra_args:
        cmd.append("--")
        cmd.extend(extra_args)
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Blender exit {result.returncode}.\n"
            f"STDERR: {result.stderr[-2000:]}\n"
            f"STDOUT: {result.stdout[-2000:]}"
        )
    return result.stdout


# ─── Script templates ─────────────────────────────────


_LIST_OBJECTS = """\
import bpy, json
objs = []
for o in bpy.context.scene.objects:
    objs.append({"name": o.name, "type": o.type,
        "location": tuple(round(v,4) for v in o.location),
        "rotation": tuple(round(v,4) for v in o.rotation_euler),
        "scale": tuple(round(v,4) for v in o.scale),
        "dimensions": tuple(round(v,4) for v in o.dimensions),
        "parent": o.parent.name if o.parent else None,
        "hide_viewport": o.hide_get(),
    })
print("OJSON:" + json.dumps(objs))
"""


_DUPLICATE_OBJECT = """\
import bpy, json
args = __import__("sys").argv[__import__("sys").argv.index("--")+1:]
obj_name = args[0] if len(args) > 0 else ""
new_name = args[1] if len(args) > 1 else ""
if obj_name in bpy.data.objects:
    src = bpy.data.objects[obj_name]
    # Duplica via data API — senza bpy.ops (fallisce in background)
    new_mesh = src.data.copy()
    new_obj = bpy.data.objects.new(new_name or src.name + "_copy", new_mesh)
    bpy.context.collection.objects.link(new_obj)
    new_obj.location = (src.location.x, src.location.y, src.location.z)
    new_obj.rotation_euler = src.rotation_euler
    new_obj.scale = src.scale
    bpy.ops.wm.save_mainfile()
    info = {"name": new_obj.name, "location": tuple(new_obj.location)}
else:
    info = {"error": f"Oggetto '{obj_name}' non trovato"}
print("OJSON:" + json.dumps(info))
"""


_MOVE_OBJECT = """\
import bpy, json
args = __import__("sys").argv[__import__("sys").argv.index("--")+1:]
obj_name = args[0]
x, y, z = float(args[1]), float(args[2]), float(args[3])
if obj_name in bpy.data.objects:
    bpy.data.objects[obj_name].location = (x, y, z)
    bpy.ops.wm.save_mainfile()
    info = {"name": obj_name, "location": tuple(bpy.data.objects[obj_name].location)}
else:
    info = {"error": f"Oggetto '{obj_name}' non trovato"}
print("OJSON:" + json.dumps(info))
"""


_ROTATE_OBJECT = """\
import bpy, json
args = __import__("sys").argv[__import__("sys").argv.index("--")+1:]
obj_name = args[0]
x, y, z = float(args[1]), float(args[2]), float(args[3])
if obj_name in bpy.data.objects:
    bpy.data.objects[obj_name].rotation_euler = (x, y, z)
    bpy.ops.wm.save_mainfile()
    info = {"name": obj_name, "rotation": tuple(bpy.data.objects[obj_name].rotation_euler)}
else:
    info = {"error": f"Oggetto '{obj_name}' non trovato"}
print("OJSON:" + json.dumps(info))
"""


_SCALE_OBJECT = """\
import bpy, json
args = __import__("sys").argv[__import__("sys").argv.index("--")+1:]
obj_name = args[0]
x, y, z = float(args[1]), float(args[2]), float(args[3])
if obj_name in bpy.data.objects:
    bpy.data.objects[obj_name].scale = (x, y, z)
    bpy.ops.wm.save_mainfile()
    info = {"name": obj_name, "scale": tuple(bpy.data.objects[obj_name].scale)}
else:
    info = {"error": f"Oggetto '{obj_name}' non trovato"}
print("OJSON:" + json.dumps(info))
"""


_HIDE_OBJECT = """\
import bpy, json
args = __import__("sys").argv[__import__("sys").argv.index("--")+1:]
obj_name = args[0]; hide = args[1].lower() == "true"
if obj_name in bpy.data.objects:
    bpy.data.objects[obj_name].hide_set(hide)
    bpy.ops.wm.save_mainfile()
    info = {"name": obj_name, "hide": hide}
else:
    info = {"error": f"Oggetto '{obj_name}' non trovato"}
print("OJSON:" + json.dumps(info))
"""


_SELECT_OBJECT = """\
import bpy, json
args = __import__("sys").argv[__import__("sys").argv.index("--")+1:]
obj_name = args[0]
for obj in bpy.data.objects:
    obj.select_set(False)
if obj_name in bpy.data.objects:
    bpy.data.objects[obj_name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
    bpy.ops.wm.save_mainfile()
    info = {"name": obj_name, "selected": True}
else:
    info = {"error": f"Oggetto '{obj_name}' non trovato"}
print("OJSON:" + json.dumps(info))
"""


_INSPECT_OBJECT_DETAIL = """\
import bpy, json
args = __import__("sys").argv[__import__("sys").argv.index("--")+1:]
obj_name = args[0]
if obj_name in bpy.data.objects:
    o = bpy.data.objects[obj_name]
    data = {"name": o.name, "type": o.type,
        "location": tuple(round(v,4) for v in o.location),
        "rotation": tuple(round(v,4) for v in o.rotation_euler),
        "scale": tuple(round(v,4) for v in o.scale),
        "dimensions": tuple(round(v,4) for v in o.dimensions),
        "parent": o.parent.name if o.parent else None,
        "children": [c.name for c in o.children],
        "hide_viewport": o.hide_get(),
        "materials": []}
    if hasattr(o.data, "materials"):
        for m in o.data.materials:
            if m:
                data["materials"].append(m.name)
    if o.type == "MESH" and hasattr(o.data, "vertices"):
        data["vertex_count"] = len(o.data.vertices)
        data["edge_count"] = len(o.data.edges)
        data["face_count"] = len(o.data.polygons)
    if o.type == "CAMERA":
        data["lens"] = o.data.lens
    if o.type == "LIGHT":
        data["light_type"] = o.data.type
    print("OJSON:" + json.dumps(data))
else:
    print('OJSON:' + json.dumps({"error": f"Oggetto '{obj_name}' non trovato"}))
"""


# ─── Public API ────────────────────────────────────────


def core_list_objects(blend_path: str) -> list[dict]:
    """Elenco di tutti gli oggetti nella scena."""
    resolved = resolve_input_blend(blend_path)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(_LIST_OBJECTS)
        sp = f.name
    try:
        out = _run_blender(resolved, sp, timeout=60)
        for line in reversed(out.strip().split("\n")):
            if line.startswith("OJSON:"):
                return json.loads(line[6:])
        raise RuntimeError(f"Nessun output OJSON.\n{out[-1000:]}")
    finally:
        os.unlink(sp)


def core_inspect_object_detail(blend_path: str, object_name: str) -> dict:
    """Dettaglio completo di un oggetto."""
    resolved = resolve_input_blend(blend_path)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(_INSPECT_OBJECT_DETAIL)
        sp = f.name
    try:
        out = _run_blender(resolved, sp, extra_args=[object_name], timeout=60)
        for line in reversed(out.strip().split("\n")):
            if line.startswith("OJSON:"):
                return json.loads(line[6:])
        raise RuntimeError(f"Nessun output OJSON.\n{out[-1000:]}")
    finally:
        os.unlink(sp)


def _run_tool_on_blend(blend_path: str, script: str,
                       args: list[str], timeout: int = 120) -> dict:
    """Helper: esegue uno script tool su un blend, restituisce JSON output."""
    resolved = resolve_input_blend(blend_path)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        sp = f.name
    try:
        out = _run_blender(resolved, sp, extra_args=args, timeout=timeout)
        for line in reversed(out.strip().split("\n")):
            if line.startswith("OJSON:"):
                return json.loads(line[6:])
        raise RuntimeError(f"Nessun output OJSON.\n{out[-1000:]}")
    finally:
        os.unlink(sp)


def core_select_object(blend_path: str, object_name: str) -> dict:
    """Seleziona un oggetto (nel file)."""
    return _run_tool_on_blend(blend_path, _SELECT_OBJECT, [object_name])


def core_duplicate_object(blend_path: str, object_name: str,
                          new_name: str = "") -> dict:
    """Duplica un oggetto nella scena. Restituisce nome e posizione del nuovo."""
    return _run_tool_on_blend(blend_path, _DUPLICATE_OBJECT,
                              [object_name, new_name])


def core_move_object(blend_path: str, object_name: str,
                     x: float, y: float, z: float) -> dict:
    """Sposta un oggetto a coordinate assolute."""
    return _run_tool_on_blend(blend_path, _MOVE_OBJECT,
                              [object_name, str(x), str(y), str(z)])


def core_rotate_object(blend_path: str, object_name: str,
                       x: float, y: float, z: float) -> dict:
    """Ruota un oggetto (euler radians)."""
    return _run_tool_on_blend(blend_path, _ROTATE_OBJECT,
                              [object_name, str(x), str(y), str(z)])


def core_scale_object(blend_path: str, object_name: str,
                      x: float, y: float, z: float) -> dict:
    """Applica scala a un oggetto."""
    return _run_tool_on_blend(blend_path, _SCALE_OBJECT,
                              [object_name, str(x), str(y), str(z)])


def core_hide_object(blend_path: str, object_name: str) -> dict:
    """Nasconde un oggetto nella viewport."""
    return _run_tool_on_blend(blend_path, _HIDE_OBJECT,
                              [object_name, "true"])


def core_show_object(blend_path: str, object_name: str) -> dict:
    """Mostra un oggetto nascosto."""
    return _run_tool_on_blend(blend_path, _HIDE_OBJECT,
                              [object_name, "false"])


# ─── Safe operation: save version + modify + audit ────


def _save_version(blend_path: str, description: str = "") -> tuple[str, str]:
    """Crea copia versionata. Restituisce (path, version_id)."""
    from app.blender import core_duplicate_version
    path, meta = core_duplicate_version(blend_path, description=description)
    return path, meta.version_id


def safe_operate(
    blend_path: str,
    tool_fn,
    tool_args: list,
    description: str = "",
    user_request: str = "",
) -> dict:
    """
    Esegue un'operazione con safety: salva versione, modifica, registra audit.

    blend_path: file .blend di input
    tool_fn: funzione tool che modifica (es core_move_object)
    tool_args: args per tool_fn
    description: descrizione
    user_request: richiesta utente originale
    """
    # 1. Salva versione prima della modifica
    version_path, version_id = _save_version(blend_path, description)

    # 2. Esegui tool sulla nuova versione
    result = tool_fn(version_path, *tool_args)

    # 3. SHA256 dello script usato (in realtà è l'operazione)
    op_desc = f"{tool_fn.__name__}({', '.join(str(a) for a in tool_args)})"
    script_sha = hashlib.sha256(op_desc.encode()).hexdigest()

    # 4. Audit trail
    changes_dir = get_changes_dir()
    record = {
        "version_id": version_id,
        "source": blend_path,
        "output": version_path,
        "description": description or user_request,
        "user_request": user_request,
        "tool": tool_fn.__name__,
        "tool_args": tool_args,
        "result": result,
        "script_sha256": script_sha,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    json_path = changes_dir / f"{version_id}.json"
    json_path.write_text(json.dumps(record, indent=2))

    return {
        "version_id": version_id,
        "version_path": version_path,
        "result": result,
        "audit_path": str(json_path),
    }