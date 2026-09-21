"""Test di sicurezza e correttezza del path resolver di blender.py."""

import os
import sys
import tempfile
from pathlib import Path
import pytest

# Assicura che il package app sia importabile
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.blender import (
    resolve_input_blend,
    resolve_workspace_output,
    core_list_blend_files,
)


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    """Crea un workspace temporaneo con struttura minima."""
    ws = tmp_path / "workspace"
    ws.mkdir()
    (ws / "originals").mkdir()
    (ws / "versions").mkdir()
    (ws / "renders").mkdir()
    (ws / "changes").mkdir()
    return ws


def test_resolve_input_rejects_relative_traversal(workspace: Path):
    """resolve_input_blend deve rifiutare path con .. che escono dal workspace."""
    os.environ["WORKSPACE_DIR"] = str(workspace)

    # Crea un file dentro il workspace per testare
    legit = workspace / "originals" / "test.blend"
    legit.write_text("dummy blend")
    resolve_input_blend("originals/test.blend")  # should succeed

    with pytest.raises(PermissionError):
        resolve_input_blend("../etc/passwd")


def test_resolve_input_rejects_absolute_outside(workspace: Path):
    """Path assoluto fuori dal workspace deve essere rifiutato."""
    os.environ["WORKSPACE_DIR"] = str(workspace)
    with pytest.raises(PermissionError):
        resolve_input_blend("/etc/passwd")


def test_resolve_input_requires_existing(workspace: Path):
    """resolve_input_blend deve fallire se il file non esiste."""
    os.environ["WORKSPACE_DIR"] = str(workspace)
    with pytest.raises(FileNotFoundError):
        resolve_input_blend("nonexistent.blend")


def test_workspace_output_rejects_traversal(workspace: Path):
    """resolve_workspace_output deve rifiutare .. nel nome output."""
    os.environ["WORKSPACE_DIR"] = str(workspace)
    with pytest.raises(PermissionError):
        resolve_workspace_output("../etc/passwd", "versions")


def test_workspace_output_rejects_absolute(workspace: Path):
    """resolve_workspace_output deve rifiutare path assoluti."""
    os.environ["WORKSPACE_DIR"] = str(workspace)
    with pytest.raises(PermissionError):
        resolve_workspace_output("/etc/passwd", "versions")


def test_workspace_output_accepts_simple_name(workspace: Path):
    """Nome file semplice deve funzionare."""
    os.environ["WORKSPACE_DIR"] = str(workspace)
    result = resolve_workspace_output("test.blend", "versions")
    assert "test.blend" in str(result)
    assert result.is_relative_to(workspace / "versions")


def test_workspace_output_rejects_subdir_slash(workspace: Path):
    """Output con slash nel nome deve essere rifiutato."""
    os.environ["WORKSPACE_DIR"] = str(workspace)
    with pytest.raises(PermissionError):
        resolve_workspace_output("sub/dir/file.blend", "versions")



def test_core_list_blend_files_empty(workspace: Path):
    """Lista vuota in workspace senza .blend."""
    os.environ["WORKSPACE_DIR"] = str(workspace)
    files = core_list_blend_files()
    assert files == []


def test_core_list_blend_files_finds_one(workspace: Path):
    """Trova file .blend in originals."""
    os.environ["WORKSPACE_DIR"] = str(workspace)
    (workspace / "originals" / "scene.blend").write_text("blend data")
    files = core_list_blend_files()
    assert len(files) == 1
    assert files[0].filename == "scene.blend"