#!/bin/bash
set -e
CAM=$1
OUT="/workspace/renders/preview_0044_${CAM}_"
echo "RENDERING $CAM -> $OUT"
docker exec ilportale-api sh -c "\
blender --background /workspace/versions/0044.blend \
  --python-expr 'import bpy; c=bpy.data.objects.get(\"$CAM\"); bpy.context.scene.camera = c' \
  -E BLENDER_EEVEE -F PNG -o $OUT -s 1 -e 1 -a 2>&1 | tail -1"
echo "DONE $CAM"