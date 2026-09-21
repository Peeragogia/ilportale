"""
Modelli dati per il core Blender Agent.

Tutti i tipi usati da API e MCP condividono queste definizioni.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime, timezone


class BlendFileInfo(BaseModel):
    """Rappresenta un file .blend nel workspace."""
    path: str
    filename: str
    size_bytes: int
    modified_iso: str


class ObjectType(str, Enum):
    MESH = "MESH"
    CURVE = "CURVE"
    SURFACE = "SURFACE"
    META = "META"
    FONT = "FONT"
    ARMATURE = "ARMATURE"
    LATTICE = "LATTICE"
    EMPTY = "EMPTY"
    CAMERA = "CAMERA"
    LIGHT = "LIGHT"
    SPEAKER = "SPEAKER"
    LIGHTPROBE = "LIGHTPROBE"
    GPENCIL = "GPENCIL"
    VOLUME = "VOLUME"
    UNKNOWN = "UNKNOWN"


class ObjectInfo(BaseModel):
    name: str
    type: ObjectType
    location: tuple[float, float, float]
    rotation: tuple[float, float, float]
    scale: tuple[float, float, float]
    dimensions: tuple[float, float, float]
    materials: list[str] = Field(default_factory=list)
    parent: Optional[str] = None


class SceneInfo(BaseModel):
    name: str
    objects: list[ObjectInfo]
    camera: Optional[str] = None
    world: Optional[str] = None
    object_count: int


class VersionMetadata(BaseModel):
    version_id: str
    source_blend: str
    script_path: Optional[str] = None
    script_sha256: Optional[str] = None
    description: str = ""
    created_iso: str = ""


class ChangeRecord(BaseModel):
    """Audit trail per ogni modifica applicata a un .blend."""
    version_id: str
    source: str
    output: str
    description: str
    script_sha256: str
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class RenderRequest(BaseModel):
    blend_path: str
    output_dir: Optional[str] = None
    resolution_x: int = 1920
    resolution_y: int = 1080
    samples: int = 64
    frame: int = 1


class ChangeScript(BaseModel):
    script_content: str
    description: str
    source_blend: str


class BlenderCommand(BaseModel):
    command: str = Field(..., description="Comando bpy Python da eseguire in background")
    blend_path: str
    timeout_seconds: int = 120