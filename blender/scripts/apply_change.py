#!/usr/bin/env python3
"""
Script Blender — applica modifica strutturale a un .blend.

Questo script NON va eseguito direttamente.
Viene chiamato dal backend blender-agent con script_content
iniettato nel wrapper. Serve come template/documentazione.

Architettura:
    blender --background input.blend --python apply_change.py -- input.blend output.blend

Lo script utente riceve:
    blend_input  = path del file .blend caricato
    blend_output = path dove salvare il risultato

Regola: mai modificare l'originale. Usa workspace/versions/.
"""

import bpy
import sys

if "--" in sys.argv:
    args = sys.argv[sys.argv.index("--") + 1:]
    blend_input = args[0]
    blend_output = args[1]
else:
    raise RuntimeError("Usage: blender --background --python apply_change.py -- input.blend output.blend")

# Carica input
bpy.ops.wm.open_mainfile(filepath=blend_input)

# ─── INIZIO MODIFICHE ──────────────────────────────────
# Questo blocco viene sostituito dal backend con script_content

# Esempio: seleziona e sposta tutti i mesh
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.location.x += 1.0

# ─── FINE MODIFICHE ────────────────────────────────────

# Salva output
bpy.ops.wm.save_as_mainfile(filepath=blend_output)
print(f"SAVE_OK:{blend_output}")