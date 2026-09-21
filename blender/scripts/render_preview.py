#!/usr/bin/env python3
"""
Script Blender — render preview headless.

Usage:
    blender --background file.blend --python render_preview.py -- <output.png> [res_x] [res_y] [samples] [frame]
"""

import bpy
import sys

# ─── Parsing argomenti ─────────────────────────────────
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
output_path = args[0] if args else "/tmp/render.png"
resolution_x = int(args[1]) if len(args) > 1 else 1920
resolution_y = int(args[2]) if len(args) > 2 else 1080
samples = int(args[3]) if len(args) > 3 else 64
frame = int(args[4]) if len(args) > 4 else 1

# ─── Configurazione render ─────────────────────────────
scene = bpy.context.scene
scene.render.resolution_x = resolution_x
scene.render.resolution_y = resolution_y
scene.frame_current = frame

# Engine detection
if hasattr(scene, "cycles"):
    scene.cycles.samples = samples

scene.render.filepath = output_path

# ─── Esegui render ─────────────────────────────────────
bpy.ops.render.render(write_still=True)
print(f"RENDER_OK:{output_path}")