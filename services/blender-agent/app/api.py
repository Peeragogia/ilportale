"""
FastAPI HTTP entrypoint per Il Portale — Blender Agent API.

Espone:
- API REST su API_PORT (default 8100) per i tool
- Chat endpoint su /chat per l'agente NL
- Static chat UI su / (root)
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional

from app.blender import (
    core_list_blend_files,
    core_inspect_scene,
    core_render_preview,
    core_duplicate_version,
    core_apply_blender_script,
)
from app.blender_tools import (
    core_list_objects,
    core_inspect_object_detail,
    core_select_object,
    core_duplicate_object,
    core_move_object,
    core_rotate_object,
    core_scale_object,
    core_hide_object,
    core_show_object,
    safe_operate,
)
from app.models import (
    RenderRequest,
    ChangeScript,
)
from app.agent import Agent


app = FastAPI(title="Il Portale — Blender Agent API", version="0.2.0")

# Istanza agente (conversation context)
agent = Agent()


# ─── Request models ───────────────────────────────────


class ManipulateRequest(BaseModel):
    blend_path: str
    object_name: str
    description: str = ""
    user_request: str = ""


class MoveRequest(ManipulateRequest):
    x: float = 0
    y: float = 0
    z: float = 0


class RotateRequest(ManipulateRequest):
    x: float = 0
    y: float = 0
    z: float = 0


class ScaleRequest(ManipulateRequest):
    x: float = 1.0
    y: float = 1.0
    z: float = 1.0


class DuplicateRequest(ManipulateRequest):
    new_name: str = ""


class ChatRequest(BaseModel):
    message: str


# ─── Health ────────────────────────────────────────────


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "blender-api",
        "version": "0.2.0",
        "features": {
            "list": True,
            "inspect": True,
            "render": True,
            "duplicate": True,
            "select": True,
            "move": True,
            "rotate": True,
            "scale": True,
            "hide": True,
            "show": True,
            "agent": True,
            "undo": True,
            "apply_script": os.environ.get("ENABLE_RAW_PYTHON", "false").lower() == "true",
        },
    }


# ─── Files ─────────────────────────────────────────────


@app.get("/files")
async def get_files():
    files = core_list_blend_files()
    return {"count": len(files), "files": [f.model_dump() for f in files]}


# ─── Scene ─────────────────────────────────────────────


@app.get("/scene/{file:path}")
async def get_scene(file: str):
    try:
        data = core_inspect_scene(file)
        return {"file": file, "scene": data}
    except (FileNotFoundError, PermissionError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/scene/{file:path}/objects")
async def get_objects(file: str):
    """List all objects in the scene."""
    try:
        data = core_list_objects(file)
        return {"file": file, "objects": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/scene/{file:path}/objects/{object_name}")
async def get_object_detail(file: str, object_name: str):
    """Detailed info about one object."""
    try:
        data = core_inspect_object_detail(file, object_name)
        return {"file": file, "object": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Manipulation (con safety: version + audit) ────────


@app.post("/operate/select")
async def operate_select(req: ManipulateRequest):
    try:
        op = safe_operate(
            req.blend_path,
            core_select_object, [req.object_name],
            description=req.description,
            user_request=req.user_request,
        )
        return {"status": "ok", **op}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/operate/duplicate")
async def operate_duplicate(req: DuplicateRequest):
    try:
        args = [req.object_name, req.new_name]
        op = safe_operate(
            req.blend_path, core_duplicate_object, args,
            description=req.description, user_request=req.user_request,
        )
        return {"status": "ok", **op}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/operate/move")
async def operate_move(req: MoveRequest):
    try:
        op = safe_operate(
            req.blend_path, core_move_object,
            [req.object_name, req.x, req.y, req.z],
            description=req.description, user_request=req.user_request,
        )
        return {"status": "ok", **op}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/operate/rotate")
async def operate_rotate(req: RotateRequest):
    try:
        op = safe_operate(
            req.blend_path, core_rotate_object,
            [req.object_name, req.x, req.y, req.z],
            description=req.description, user_request=req.user_request,
        )
        return {"status": "ok", **op}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/operate/scale")
async def operate_scale(req: ScaleRequest):
    try:
        op = safe_operate(
            req.blend_path, core_scale_object,
            [req.object_name, req.x, req.y, req.z],
            description=req.description, user_request=req.user_request,
        )
        return {"status": "ok", **op}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/operate/hide")
async def operate_hide(req: ManipulateRequest):
    try:
        op = safe_operate(
            req.blend_path, core_hide_object, [req.object_name],
            description=req.description, user_request=req.user_request,
        )
        return {"status": "ok", **op}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/operate/show")
async def operate_show(req: ManipulateRequest):
    try:
        op = safe_operate(
            req.blend_path, core_show_object, [req.object_name],
            description=req.description, user_request=req.user_request,
        )
        return {"status": "ok", **op}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/operate/render")
async def operate_render(req: RenderRequest):
    try:
        out = core_render_preview(
            blend_path=req.blend_path,
            resolution_x=req.resolution_x,
            resolution_y=req.resolution_y,
            samples=req.samples,
            frame=req.frame,
        )
        return {"status": "ok", "render_path": out}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Undo last change ────────────────────────────────


@app.post("/undo/{blend_path:path}")
async def undo_last_change(blend_path: str):
    """
    Annulla l'ultima modifica: ripristina la versione precedente.
    """
    from app.blender import get_versions_dir, get_workspace
    versions = sorted(get_versions_dir().glob("[0-9][0-9][0-9][0-9].blend"))
    if len(versions) < 2:
        raise HTTPException(status_code=400,
                            detail="Nessuna versione precedente disponibile per undo")
    # Prendi la penultima versione
    previous = versions[-2]
    current = versions[-1]
    # Copia indietro
    import shutil
    resolved = resolve_input_blend(blend_path)  # solo per validazione path
    # Sovrascrive il file corrente con la versione precedente
    # Ma meglio: salviamo una nuova versione che è copia della penultima
    from app.blender import core_duplicate_version
    new_path, meta = core_duplicate_version(
        source_path=str(previous),
        description=f"Undo: ripristino versione {previous.stem}",
    )
    return {
        "status": "ok",
        "message": f"Ripristinata versione {previous.stem} come {meta.version_id}",
        "previous_version": previous.stem,
        "new_version": meta.version_id,
        "path": new_path,
    }


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
    try:
        if req.script_content:
            output_path, change_record = core_apply_blender_script(
                blend_path=req.source_blend,
                script_content=req.script_content,
                description=req.description,
            )
            return {"status": "ok", "path": output_path,
                    "change": change_record.model_dump()}
        else:
            path, meta = core_duplicate_version(
                source_path=req.source_blend,
                description=req.description,
            )
            return {"status": "ok", "version": meta.version_id,
                    "path": path, "metadata": meta.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/versions/duplicate")
async def duplicate(source_blend: str, description: str = ""):
    try:
        path, meta = core_duplicate_version(
            source_path=source_blend, description=description,
        )
        return {"status": "ok", "version": meta.version_id,
                "path": path, "metadata": meta.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Changes / Audit trail ────────────────────────────


@app.get("/changes")
async def list_changes():
    changes_dir = Path(os.environ.get("WORKSPACE_DIR", "/workspace")) / "changes"
    if not changes_dir.exists():
        return {"count": 0, "changes": []}
    records = []
    for f in sorted(changes_dir.glob("*.json")):
        records.append(json.loads(f.read_text()))
    return {"count": len(records), "changes": records}


@app.get("/changes/{change_id}")
async def get_change(change_id: str):
    changes_dir = Path(os.environ.get("WORKSPACE_DIR", "/workspace")) / "changes"
    json_path = changes_dir / f"{change_id}.json"
    py_path = changes_dir / f"{change_id}.py"
    if not json_path.exists():
        raise HTTPException(status_code=404, detail=f"Change {change_id} not found")
    record = json.loads(json_path.read_text())
    script = py_path.read_text() if py_path.exists() else None
    return {"record": record, "script": script}


# ─── Agent Chat ────────────────────────────────────────


@app.post("/chat")
async def chat(req: ChatRequest):
    """Invia un messaggio in linguaggio naturale all'agente."""
    try:
        result = agent.handle(req.message)
        return result
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)[:500],
            "conversation_id": agent.conversation_id,
        }


@app.get("/agent/context")
async def get_context():
    """Restituisce il contesto corrente della conversazione."""
    return {
        "conversation_id": agent.conversation_id,
        "last_action": agent.last_action,
        "last_object": agent.last_object,
        "current_blend": agent.current_blend,
        "history": agent.history[-20:],
    }


@app.post("/agent/reset")
async def reset_context():
    """Resetta il contesto della conversazione."""
    agent.reset()
    return {"status": "ok", "message": "Contesto resettato"}


# ─── Render file serving ─────────────────────────────


@app.get("/render-file/{filename}")
async def serve_render(filename: str):
    """Serve un file renderizzato dal workspace/renders/."""
    renders_dir = Path(os.environ.get("WORKSPACE_DIR", "/workspace")) / "renders"
    filepath = (renders_dir / filename).resolve()
    if not filepath.is_relative_to(renders_dir):
        raise HTTPException(status_code=403, detail="Accesso negato")
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File non trovato")
    return FileResponse(str(filepath), media_type="image/png")


# ─── Chat UI ──────────────────────────────────────────


_CHAT_HTML = """\
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Il Portale — Blender Agent</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:system-ui,sans-serif; background:#1a1a2e; color:#e0e0e0; height:100vh; display:flex; flex-direction:column; }
#header { background:#16213e; padding:12px 20px; border-bottom:1px solid #0f3460; display:flex; justify-content:space-between; align-items:center; }
#header h1 { font-size:18px; color:#e94560; }\n#header small { color:#888; font-size:12px; }
#header .debug-toggle { background:#1a3a5c; color:#888; border:1px solid #0f3460; padding:4px 10px; border-radius:4px; font-size:11px; cursor:pointer; }
#header .debug-toggle:hover { background:#0f3460; color:#e0e0e0; }
#debug-panel { display:none; background:#0d1b2a; border-bottom:1px solid #0f3460; padding:8px 16px; font-family:monospace; font-size:11px; max-height:200px; overflow-y:auto; }
#debug-panel.visible { display:block; }
#debug-panel .debug-step { padding:4px 0; border-bottom:1px solid #1a3a5c; }
#debug-panel .debug-step:last-child { border-bottom:none; }
#debug-panel .label { color:#888; }
#debug-panel .value { color:#e0e0e0; }
#debug-panel .value.intent { color:#e94560; }
#debug-panel .value.error { color:#ff6b6b; }
#debug-panel .value.result { color:#51cf66; }
#debug-panel .state-row { display:flex; gap:12px; flex-wrap:wrap; padding:4px 0; }
#debug-panel .state-item { background:#16213e; padding:2px 8px; border-radius:3px; }
#chat { flex:1; overflow-y:auto; padding:16px; display:flex; flex-direction:column; gap:12px; }
.msg { max-width:80%; padding:10px 14px; border-radius:12px; line-height:1.5; font-size:14px; }
.user { background:#0f3460; align-self:flex-end; border-bottom-right-radius:4px; }
.agent { background:#16213e; align-self:flex-start; border-bottom-left-radius:4px; }
.agent pre { background:#0d1b2a; padding:8px; border-radius:6px; margin:6px 0; overflow-x:auto; font-size:12px; }
.agent img { max-width:100%; border-radius:6px; margin:6px 0; }
.tool-call { background:#1a3a5c; font-size:12px; padding:4px 8px; border-radius:4px; margin:4px 0; color:#aaa; }
.error { color:#ff6b6b; }
.ok { color:#51cf66; }
#input-area { background:#16213e; padding:12px 16px; border-top:1px solid #0f3460; display:flex; gap:8px; }
#input { flex:1; background:#0f3460; border:1px solid #1a4a7a; color:#e0e0e0; padding:10px 14px; border-radius:8px; font-size:14px; outline:none; }
#input:focus { border-color:#e94560; }
#send { background:#e94560; color:#fff; border:none; padding:10px 20px; border-radius:8px; font-size:14px; cursor:pointer; }
#send:hover { background:#c73650; }
#send:disabled { opacity:.5; cursor:not-allowed; }
.status { font-size:12px; color:#666; padding:4px; text-align:center; }
</style>
</head>
<body>
<div id="header">
  <div><h1>🧊 Il Portale — Blender Agent</h1><small>Parla in italiano. L'agente interpreta e modifica il .blend.</small></div>
  <button class="debug-toggle" onclick="toggleDebug()">🐞 Debug</button>
</div>
<div id="debug-panel"></div>
<div id="chat"></div>
<div id="input-area">
<input id="input" placeholder="Es: 'Analizza la struttura'" autofocus>
<button id="send" onclick="send()">Invia</button>
</div>
<div id="status" class="status">Pronto</div>
<script>
const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const status = document.getElementById("status");
const debugPanel = document.getElementById("debug-panel");
let debugVisible = false;

function toggleDebug() {
    debugVisible = !debugVisible;
    debugPanel.classList.toggle("visible", debugVisible);
}

function updateDebug(data) {
    if (!data || !data.debug) return;
    let html = "";
    // Conversation state
    if (data.state) {
        html += '<div class="state-row">';
        for (const [k,v] of Object.entries(data.state)) {
            if (v) html += '<span class="state-item"><span class="label">' + k + '</span> <span class="value">' + v + '</span></span>';
        }
        html += '</div>';
    }
    // Steps
    if (data.debug.steps) {
        for (const step of data.debug.steps) {
            html += '<div class="debug-step">';
            if (step.step === "intent") {
                html += '<span class="label">🎯 Intent:</span> <span class="value intent">' + (step.intent || "?") + '</span> <span class="label">(conf:</span> <span class="value">' + (step.confidence || "?") + ')</span>';
            } else if (step.step === "entities") {
                html += '<span class="label">📦 Entità:</span> <span class="value">' + JSON.stringify(step.entities || {}) + '</span>';
            } else if (step.step === "resolution") {
                html += '<span class="label">🔗 Risolto:</span> <span class="value">' + JSON.stringify(step.resolved || {}) + '</span>';
            } else if (step.step === "execute") {
                const r = step.result || {};
                html += '<span class="label">⚡ Esegui:</span> <span class="value result">' + (r.status || "?") + '</span>';
                if (r.version_id) html += ' <span class="label">v:</span><span class="value">' + r.version_id + '</span>';
                if (r.last_object) html += ' <span class="label">obj:</span><span class="value">' + r.last_object + '</span>';
            } else if (step.step === "error") {
                html += '<span class="label">❌ Errore:</span> <span class="value error">' + (step.error || "").substring(0,100) + '</span>';
            } else {
                html += '<span class="label">' + step.step + ':</span> <span class="value">' + JSON.stringify(step).substring(0,150) + '</span>';
            }
            html += '</div>';
        }
    }
    debugPanel.innerHTML = html;
}

function addMsg(text, cls = "agent") {
    const div = document.createElement("div");
    div.className = "msg " + cls;
    div.innerHTML = text.replace(/\\n/g, "<br>");
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function send() {
    const msg = input.value.trim();
    if (!msg) return;
    addMsg(msg, "user");
    input.value = "";
    sendBtn.disabled = true;
    status.textContent = "⏳ L'agente sta lavorando...";
    try {
        const resp = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: msg}),
        });
        const data = await resp.json();
        if (data.status === "error") {
            addMsg('<span class="error">❌ ' + data.error + '</span>');
        } else {
            let html = data.response || data.message || JSON.stringify(data);
            addMsg(html);
            if (data.render_url) {
                addMsg('<img src="' + data.render_url + '" alt="render">');
            }
            if (data.version_id) {
                addMsg('<span class="ok">✔ Versione ' + data.version_id + ' creata</span>');
            }
        }
        updateDebug(data);
    } catch (e) {
        addMsg('<span class="error">❌ Errore di connessione: ' + e.message + '</span>');
    }
    sendBtn.disabled = false;
    status.textContent = "Pronto";
    input.focus();
}

input.addEventListener("keydown", (e) => { if (e.key === "Enter") send(); });

// Messaggio iniziale
addMsg("👋 Ciao! Sono l'agente Blender. Posso ispezionare, modificare e versionare il tuo file.\n\n🔍 Prova: 'Analizza la Tastiera'\n✏️ Poi: 'Creane una copia di lavoro'\n🎯 Poi: 'Spostala di lato'\n\n💡 Uso pronomi come 'ne', 'la', 'lo' per riferirmi all'ultimo oggetto.");
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def chat_ui():
    return _CHAT_HTML


# ─── Entrypoint ────────────────────────────────────────


def main():
    api_port = int(os.environ.get("API_PORT", "8100"))
    uvicorn.run("app.api:app", host="0.0.0.0", port=api_port, log_level="info")


if __name__ == "__main__":
    main()