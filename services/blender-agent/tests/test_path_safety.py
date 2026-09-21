"""Test di sicurezza e correttezza del path resolver di blender.py.

ATTENZIONE: i test importano app.blender DOPO aver impostato
WORKSPACE_DIR. L'import è lazy (dentro le funzioni di test).
"""

import os
import sys
from pathlib import Path
import pytest


@pytest.fixture(autouse=True)
def _setup_workspace(monkeypatch, tmp_path: Path) -> str:
    """Crea workspace temporaneo e imposta WORKSPACE_DIR prima dell'import."""
    ws = tmp_path / "w"
    ws.mkdir()
    (ws / "originals").mkdir()
    (ws / "versions").mkdir()
    (ws / "renders").mkdir()
    (ws / "changes").mkdir()
    monkeypatch.setenv("WORKSPACE_DIR", str(ws))
    return str(ws)


def test_resolve_input_rejects_traversal():
    """resolve_input_blend deve rifiutare .. fuori dal workspace."""
    from app.blender import resolve_input_blend
    with pytest.raises(PermissionError):
        resolve_input_blend("../etc/passwd")


def test_resolve_input_rejects_absolute():
    """Path assoluto fuori dal workspace deve essere rifiutato."""
    from app.blender import resolve_input_blend
    with pytest.raises(PermissionError):
        resolve_input_blend("/etc/passwd")


def test_resolve_input_requires_existing():
    """resolve_input_blend fallisce se file non esiste."""
    from app.blender import resolve_input_blend
    with pytest.raises(FileNotFoundError):
        resolve_input_blend("nonexistent.blend")


def test_resolve_output_rejects_traversal():
    """resolve_workspace_output rifiuta .. nel nome."""
    from app.blender import resolve_workspace_output
    with pytest.raises(PermissionError):
        resolve_workspace_output("../etc/passwd", "versions")


def test_resolve_output_rejects_absolute():
    """resolve_workspace_output rifiuta path assoluti."""
    from app.blender import resolve_workspace_output
    with pytest.raises(PermissionError):
        resolve_workspace_output("/etc/passwd", "versions")


def test_resolve_output_rejects_subdir():
    """Output con slash rifiutato."""
    from app.blender import resolve_workspace_output
    with pytest.raises(PermissionError):
        resolve_workspace_output("sub/dir/file.blend", "versions")


def test_resolve_output_accepts_simple_name():
    """Nome file semplice accettato."""
    from app.blender import resolve_workspace_output, WORKSPACE
    result = resolve_workspace_output("test.blend", "versions")
    assert result.parent == WORKSPACE / "versions"
    assert result.name == "test.blend"



def test_list_blend_files_finds_one():
    """core_list_blend_files trova .blend in originals."""
    ws = Path(os.environ["WORKSPACE_DIR"])
    (ws / "originals" / "scene.blend").write_text("blend data")
    from app.blender import core_list_blend_files
    files = core_list_blend_files()
    assert len(files) == 1
    assert files[0].filename == "scene.blend"


def test_list_blend_files_empty():
    """Lista vuota in workspace senza .blend."""
    from app.blender import core_list_blend_files
    files = core_list_blend_files()
    assert files == []


def test_duplicate_version_works():
    """Duplica un .blend orig→versions/ crea file."""
    from app.blender import core_duplicate_version
    ws = Path(os.environ["WORKSPACE_DIR"])
    (ws / "originals" / "base.blend").write_text("blenddata")
    path, meta = core_duplicate_version("originals/base.blend", "test dup")
    assert Path(path).exists()
    assert meta.description == "test dup"
    assert meta.source_blend == "originals/base.blend"