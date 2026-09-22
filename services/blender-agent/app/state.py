"""
Persistent conversation state via SQLite in workspace.

Sopravvive a restart del container (volume workspace è persistente).
Usato da agent.py e api.py per mantenere contesto tra messaggi.
"""

import os
import json
import sqlite3
import threading
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Optional


_db_lock = threading.Lock()


def _get_db_path() -> Path:
    ws = os.environ.get("WORKSPACE_DIR", "/workspace")
    return Path(ws) / "state.db"


def _get_conn() -> sqlite3.Connection:
    db_path = _get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Crea la tabella state se non esiste."""
    with _db_lock:
        conn = _get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversation_state (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_iso TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                role     TEXT NOT NULL,
                message  TEXT NOT NULL,
                timestamp_iso TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()


def get_state(key: str, default: Any = None) -> Any:
    """Legge un valore dallo stato persistente."""
    with _db_lock:
        conn = _get_conn()
        row = conn.execute(
            "SELECT value FROM conversation_state WHERE key = ?", (key,)
        ).fetchone()
        conn.close()
        if row:
            try:
                return json.loads(row["value"])
            except json.JSONDecodeError:
                return row["value"]
        return default


def set_state(key: str, value: Any):
    """Scrive un valore nello stato persistente."""
    with _db_lock:
        conn = _get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO conversation_state (key, value, updated_iso) VALUES (?, ?, ?)",
            (key, json.dumps(value) if not isinstance(value, str) else value,
             datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        conn.close()


def get_all_state() -> dict:
    """Restituisce tutto lo stato come dict."""
    with _db_lock:
        conn = _get_conn()
        rows = conn.execute("SELECT key, value FROM conversation_state").fetchall()
        conn.close()
        result = {}
        for r in rows:
            try:
                result[r["key"]] = json.loads(r["value"])
            except (json.JSONDecodeError, TypeError):
                result[r["key"]] = r["value"]
        return result


def reset_state():
    """Resetta tutto lo stato."""
    with _db_lock:
        conn = _get_conn()
        conn.execute("DELETE FROM conversation_state")
        conn.execute("DELETE FROM conversation_history")
        conn.commit()
        conn.close()


def add_history(role: str, message: str):
    """Aggiunge un messaggio alla cronologia."""
    with _db_lock:
        conn = _get_conn()
        conn.execute(
            "INSERT INTO conversation_history (role, message, timestamp_iso) VALUES (?, ?, ?)",
            (role, message[:2000], datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        conn.close()


def get_history(limit: int = 50) -> list[dict]:
    """Restituisce la cronologia recente."""
    with _db_lock:
        conn = _get_conn()
        rows = conn.execute(
            "SELECT role, message, timestamp_iso FROM conversation_history ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in reversed(rows)]


def get_latest_blend() -> str:
    """Trova l'ultimo file .blend in workspace/versions/ (stato persistente)."""
    versions_dir = Path(os.environ.get("WORKSPACE_DIR", "/workspace")) / "versions"
    if not versions_dir.exists():
        return "base/PORTALE.blend"
    blends = sorted(versions_dir.glob("[0-9][0-9][0-9][0-9].blend"))
    if blends:
        return f"versions/{blends[-1].name}"
    # Fallback all'originale
    base_dir = Path(os.environ.get("WORKSPACE_DIR", "/workspace")) / "base"
    for f in ["PORTALE.blend", "PORTALE.blend1"]:
        if (base_dir / f).exists():
            return f"base/{f}"
    return "base/PORTALE.blend"


# Inizializza al primo import
init_db()