#!/usr/bin/env python3
"""
Pi Blender Tool — bridge tra Pi (LLM agent) e il container Blender API.

Pi esegue questo script per ogni operazione Blender.
Lo script:
1. Riceve comando + parametri in JSON
2. Chiama l'API REST sul container
3. Restituisce risultato strutturato

Usage:
  python blender_tool.py inspect '{"object_name": "Tastiera"}'
  python blender_tool.py list '{}'
  python blender_tool.py duplicate '{"object_name": "Tastiera", "new_name": "Tastiera_copia"}'
  python blender_tool.py move '{"object_name": "Tastiera_copia", "x": 2.0, "y": 0, "z": 0}'
  python blender_tool.py render '{"frame": 1}'
  python blender_tool.py undo '{}'
  python blender_tool.py schema '{}'  # stampa lo schema dei tool
  python blender_tool.py status '{}'  # stato corrente
"""

import sys
import json
import os
import urllib.request
import urllib.error


# ─── Configurazione ─────────────────────────────────────


API_BASE = os.environ.get("BLENDER_API_URL", "https://agent.blender.pyragogy.org")
# Per test interni sul server:
# API_BASE = "http://127.0.0.1:8100"

TIMEOUT = int(os.environ.get("BLENDER_API_TIMEOUT", "120"))


# ─── API call helper ────────────────────────────────────


def _call_api(endpoint: str, payload: dict) -> dict:
    """Chiama l'API REST e restituisce JSON."""
    url = f"{API_BASE}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"status": "error", "error": f"HTTP {e.code}: {body[:500]}"}
    except urllib.error.URLError as e:
        return {"status": "error", "error": f"Connessione fallita: {e.reason}"}
    except json.JSONDecodeError as e:
        return {"status": "error", "error": f"JSON non valido: {e}"}


def _call_api_get(endpoint: str) -> dict:
    """Chiamata GET."""
    url = f"{API_BASE}{endpoint}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ─── Tool handlers ──────────────────────────────────────


def cmd_inspect(params: dict) -> dict:
    """Ispeziona un oggetto."""
    obj_name = params.get("object_name", "")
    if not obj_name:
        return {"status": "error", "error": "Specifica object_name"}
    return _call_api("/tools/inspect", {"object_name": obj_name})


def cmd_list(params: dict) -> dict:
    """Elenca oggetti."""
    return _call_api("/tools/list", {})


def cmd_duplicate(params: dict) -> dict:
    """Duplica un oggetto."""
    obj_name = params.get("object_name", "")
    if not obj_name:
        return {"status": "error", "error": "Specifica object_name"}
    new_name = params.get("new_name", "")
    return _call_api("/tools/duplicate", {
        "object_name": obj_name,
        "new_name": new_name,
    })


def cmd_move(params: dict) -> dict:
    """Sposta un oggetto."""
    obj_name = params.get("object_name", "")
    if not obj_name:
        return {"status": "error", "error": "Specifica object_name"}
    return _call_api("/tools/move", {
        "object_name": obj_name,
        "x": params.get("x", 0),
        "y": params.get("y", 0),
        "z": params.get("z", 0),
        "relative": params.get("relative", True),
    })


def cmd_rotate(params: dict) -> dict:
    """Ruota un oggetto."""
    obj_name = params.get("object_name", "")
    if not obj_name:
        return {"status": "error", "error": "Specifica object_name"}
    return _call_api("/tools/rotate", {
        "object_name": obj_name,
        "x": params.get("x", 0),
        "y": params.get("y", 0),
        "z": params.get("z", 0),
    })


def cmd_hide(params: dict) -> dict:
    """Nascondi oggetto."""
    obj_name = params.get("object_name", "")
    if not obj_name:
        return {"status": "error", "error": "Specifica object_name"}
    return _call_api("/tools/hide", {
        "object_name": obj_name,
        "hidden": True,
    })


def cmd_show(params: dict) -> dict:
    """Mostra oggetto."""
    obj_name = params.get("object_name", "")
    if not obj_name:
        return {"status": "error", "error": "Specifica object_name"}
    return _call_api("/tools/hide", {
        "object_name": obj_name,
        "hidden": False,
    })


def cmd_render(params: dict) -> dict:
    """Render preview."""
    frame = params.get("frame", 1)
    return _call_api("/tools/render", {"frame": frame})


def cmd_undo(params: dict) -> dict:
    """Annulla ultima modifica."""
    return _call_api("/tools/undo", {})


def cmd_reset(params: dict) -> dict:
    """Resetta stato."""
    return _call_api("/tools/reset", {})


def cmd_schema(params: dict) -> dict:
    """Stampa lo schema dei tool."""
    return _call_api_get("/tools/schema")


def cmd_status(params: dict) -> dict:
    """Stato corrente (persistente)."""
    return _call_api_get("/state")


# ─── Dispatch ──────────────────────────────────────────


COMMANDS = {
    "inspect": cmd_inspect,
    "list": cmd_list,
    "duplicate": cmd_duplicate,
    "move": cmd_move,
    "rotate": cmd_rotate,
    "hide": cmd_hide,
    "show": cmd_show,
    "render": cmd_render,
    "undo": cmd_undo,
    "reset": cmd_reset,
    "schema": cmd_schema,
    "status": cmd_status,
}


def main():
    if len(sys.argv) < 2:
        print(json.dumps(COMMANDS), file=sys.stderr)
        print(f"Usage: {sys.argv[0]} <comando> '<json_params>'", file=sys.stderr)
        print(f"Es: {sys.argv[0]} inspect '{{\"object_name\": \"Tastiera\"}}'", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    params = {}
    if len(sys.argv) >= 3:
        try:
            params = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            result = {"status": "error", "error": f"JSON params non valido: {e}"}
            print(json.dumps(result))
            sys.exit(1)

    handler = COMMANDS.get(command)
    if not handler:
        result = {
            "status": "error",
            "error": f"Comando sconosciuto: {command}",
            "available": list(COMMANDS.keys()),
        }
        print(json.dumps(result))
        sys.exit(1)

    try:
        result = handler(params)
        print(json.dumps(result))
    except Exception as e:
        result = {"status": "error", "error": str(e)}
        print(json.dumps(result))
        sys.exit(1)


if __name__ == "__main__":
    main()