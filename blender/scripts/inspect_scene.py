#!/usr/bin/env python3
"""
Script Blender — ispezione struttura scena.

Usage:
    blender --background file.blend --python inspect_scene.py

Output: JSON su stdout con la struttura della scena.
"""

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
        "materials": (
            [m.name for m in obj.data.materials if m]
            if hasattr(obj, "data") and hasattr(obj.data, "materials")
            else []
        ),
        "parent": obj.parent.name if obj.parent else None,
    }
    data["objects"].append(obj_data)

data["object_count"] = len(data["objects"])
print(json.dumps(data))