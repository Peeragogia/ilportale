# Comandi Blender & Tool Reference

> Raccoglie tutti i comandi utili per operare su Il Portale.
> **Scopo**: evitare di bruciare token ripetendo comandi via SSH.

## 1. Blender CLI (background mode)

### Render di un'immagine
```bash
blender --background /path/to/file.blend \
  --python-expr "
import bpy
rs = bpy.context.scene.render
rs.image_settings.media_type = 'IMAGE'
rs.image_settings.file_format = 'PNG'
rs.filepath = '/workspace/renders/output'
bpy.ops.render.render(write_still=True)
"
```

> **⚠ Blender 5.2**: `file_format` si setta su `image_settings` NON su `render`.
> **⚠ Blender 5.2**: prima bisogna passare `media_type` da `VIDEO` a `IMAGE`,
>   altrimenti `file_format` accetta solo `FFMPEG`.

### Ispezionare la scena
```python
# Lista oggetti
import bpy
for o in bpy.context.scene.objects:
    print(f"{o.name:30s} type={o.type} parent={o.parent.name if o.parent else '—'}")

# Info materiale
mat = bpy.data.materials["Material.001"]
for node in mat.node_tree.nodes:
    print(f"  {node.name}: {node.type}")
    for inp in node.inputs:
        if inp.name in ("Base Color", "Roughness", "Metallic", "Color"):
            print(f"    {inp.name} = {inp.default_value}")
```

### Eseguire script da file
```bash
blender --background /workspace/versions/0023.blend --python /tmp/script.py
```
Usare `2>/dev/null` per silenziare l'output di Blender, poi grep per `OJSON:`.

### Rendering da remoto
```bash
scp script.py root@SERVER:/tmp/script.py
ssh root@SERVER "docker cp /tmp/script.py CONTAINER:/tmp/script.py && \
  docker exec CONTAINER sh -c \"blender --background FILE --python /tmp/script.py\" > /tmp/out.txt && \
  grep 'OJSON:' /tmp/out.txt"
```

## 2. Blender 5.2 API — differenze chiave

### `bpy.ops` NON funziona in background
```python
# NON FUNZIONA in --background:
bpy.ops.object.parent_set(keep_transform=True)    # ❌ poll() failed
bpy.ops.mesh.primitive_cube_add()                  # ❌ context is incorrect
bpy.ops.object.select_all(action='DESELECT')       # ❌
bpy.ops.object.location_clear()                    # ❌
bpy.ops.wm.save_mainfile()                         # ✅ funziona (solo questo)

# Alternative Data API:
obj.parent = empty                    # ✅ funziona
obj.location = (1, 2, 3)             # ✅ funziona
mesh = bpy.data.meshes.new(name)     # ✅
bpy.data.objects.remove(obj)         # ✅
```

### `image_settings.file_format` enum
```python
# File format validi:
# 'AVIF', 'JPEG', 'OPEN_EXR', 'PNG', 'WEBP', 'BMP', 'CINEON', 'DPX',
# 'IRIS', 'JPEG2000', 'HDR', 'TARGA', 'TARGA_RAW', 'TIFF',
# 'OPEN_EXR_MULTILAYER', 'FFMPEG'

# Per cambiare da FFMPEG a PNG:
rs.image_settings.media_type = "IMAGE"     # prima!
rs.image_settings.file_format = "PNG"      # poi
rs.filepath = "/path/to/output"
```

### Creare luci
```python
light = bpy.data.lights.new("Nome", type="AREA")
# type: 'POINT', 'SUN', 'SPOT', 'AREA'
light.energy = 600
light.color = (1.0, 0.95, 0.88)

obj = bpy.data.objects.new("Nome", light)
obj.location = (x, y, z)
bpy.context.collection.objects.link(obj)
```

### Materiali — settare colore su Principled BSDF
```python
mat = bpy.data.materials["Material.001"]
for node in mat.node_tree.nodes:
    if node.type == "BSDF_PRINCIPLED":
        node.inputs["Base Color"].default_value = (0.12, 0.12, 0.13, 1.0)
        node.inputs["Roughness"].default_value = 0.4
    if node.type == "BSDF_DIFFUSE":
        node.inputs["Color"].default_value = (0.12, 0.12, 0.13, 1.0)
```

## 3. Struttura workspace

```
/workspace/
├── base/PORTALE.blend         # Originale, mai modificato
├── versions/0001.blend        # Base pulita
├── versions/0023.blend        # Versione corrente (pulita + riorganizzata)
├── renders/*.png              # Render output
├── state.db                   # SQLite persistente
├── changes/                   # Audit trail (JSON)
└── originals/                 # File sorgente
```

## 4. Gerarchia scena (dopo pulizia)

```
G_Arredo           ← Tastiera, Sgabello, Schermo, Speaker, Struttura
G_Tavolo           ← Piano S, Piano N, Piedini 1-3, Sostegni DX
G_Architettura     ← Colonne, Parascopi, Particolari, Pianta-18, Plane.005
G_Luci             ← Point, Lamp, Key_Area, Fill_Area, Rim_Area, Ambient_Point
G_Scena            ← Plane, Plane.004, Cylinder.002
```

## 5. Materiali (colori assegnati)

| Materiale | Colore | Uso |
|-----------|--------|-----|
| Black | (0.03, 0.03, 0.03) | Tasti tastiera |
| Black.001 | (0.02, 0.02, 0.05) | Base nera |
| Material | (0.12, 0.12, 0.13) | Corpo tastiera |
| Material.001 | (0.18, 0.18, 0.20) | Base tastiera |
| Material.002 | (0.90, 0.92, 0.98) | Schermo |
| Material.003 | (0.50, 0.25, 0.10) | Legno tavolo |
| Material.004 | (0.65, 0.65, 0.70) | Metallo sostegni |
| Material.005 | (0.80, 0.35, 0.15) | Rame/ottone |
| Material.006 | (0.25, 0.55, 0.75) | Blu tessuto sgabello |
| Material.011 | (0.82, 0.82, 0.80) | Pareti |
| MediumGrey | (0.50, 0.50, 0.52) | Pavimento |

## 6. Luci (sistema a 4 punti)

| Luce | Tipo | Energia | Colore | Ruolo |
|------|------|---------|--------|-------|
| Key_Area | AREA | 600 | (1.0, 0.95, 0.88) — caldo | Principale, da destra |
| Fill_Area | AREA | 300 | (0.82, 0.88, 1.0) — freddo | Riempimento, da sinistra |
| Rim_Area | AREA | 200 | (1.0, 1.0, 1.0) — neutro | Controluce, da dietro |
| Ambient_Point | POINT | 80 | (0.9, 0.9, 1.0) — freddo | Ambiente soffuso |
| Lamp (sole) | SUN | 3.0 | (1.0, 0.95, 0.85) — caldo | Luce solare |

## 7. Docker — comandi rapidi

### Container names
```bash
CONTAINER=blender-qfrr3ylfwtz97sws9bjuwl8y   # GUI + desktop
API=blender-api-qfrr3ylfwtz97sws9bjuwl8y     # API standalone
```

### Stati
```bash
# Log
docker logs $CONTAINER --tail 20

# Porte
docker exec $CONTAINER sh -c "ss -tlnp | grep -E '3000|8100|8200'"

# Processi Blender
docker exec $CONTAINER ps aux | grep blend

# Riavvio GUI Blender
docker exec $CONTAINER sh -c "
  kill PID_GIANDIA 2>/dev/null
  export XDG_RUNTIME_DIR=/config/.XDG
  export WAYLAND_DISPLAY=wayland-1
  export DISPLAY=:0
  blender /workspace/versions/0023.blend --python-expr \\
    'import bpy; bpy.context.preferences.inputs.use_mouse_continuous = False' &
"

# Clean workspace
docker exec $CONTAINER rm -f /workspace/versions/*.blend1 /workspace/renders/*.png
```

### Stato persistente (API)
```bash
# Verifica
curl -s http://127.0.0.1:8100/state

# Tool list
curl -s http://127.0.0.1:8100/tools/list | python3 -m json.tool

# Tool inspect
curl -s -X POST http://127.0.0.1:8100/tools/inspect \
  -H "Content-Type: application/json" \
  -d '{"object_name": "Tastiera"}' | python3 -m json.tool

# Tool render
curl -s -X POST http://127.0.0.1:8100/tools/render \
  -H "Content-Type: application/json" \
  -d '{"frame": 1}' | python3 -m json.tool
```

## 8. Deployment e push

```bash
cd /home/coder/project/Il_Portale-20026

# Build immagine
docker build -t ttl.sh/peeragogia/il-portale:latest .
docker push ttl.sh/peeragogia/il-portale:latest

# Deploy su server
scp deploy-server.yml root@91.99.70.26:/root/
ssh root@91.99.70.26 "docker compose -f /root/deploy-server.yml up -d --pull always"

# Commit
git add -A
git commit -m "feat: descrizione"
git push origin master
```

## 9. Bug noti

1. **Renderer format locked**: `media_type = "VIDEO"` impedisce PNG — settare
   sempre `media_type = "IMAGE"` prima di cambiare `file_format`.
2. **bpy.ops fallisce in --background**: usare sempre Data API.
3. **GUI Blender schermo nero**: richiede `XDG_RUNTIME_DIR=/config/.XDG`
   e `WAYLAND_DISPLAY=wayland-1`. Se muore, kill e riavvia.
4. **Path texture mancanti**: le texture originali erano in una cartella
   separata non migrata nel container. I materiali funzionano con colori
   solidi (non texture).