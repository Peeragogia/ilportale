#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  ECO MODE — controllo GUI Blender/Selkies
#
#  La GUI Blender (blender.pyragogy.org) consuma ~2-3GB di RAM
#  (Selkies + Wayland + Blender). L'API e MCP pesano pochissimo.
#  Per risparmiare RAM senza perdere l'agent:
#
#    bash eco.sh off    # spegni SOLO la GUI (API resta attiva)
#    bash eco.sh on     # riaccendi la GUI + carica 0023.blend
#    bash eco.sh status # stato attuale
#    bash eco.sh        # alias di status
# ═══════════════════════════════════════════════════════════════

GUI_CONTAINER="blender-qfrr3ylfwtz97sws9bjuwl8y"
API_URL="https://agent.blender.pyragogy.org/health"
BLEND_FILE="/workspace/versions/0023.blend"
STARTUP="/workspace/startup.py"

# ── Funzioni ──────────────────────────────────────────────────

status() {
  echo "═ GUI: $GUI_CONTAINER ═"
  if docker ps --format '{{.Names}}' | grep -q "^${GUI_CONTAINER}$"; then
    echo "  ⏺ GUI: ATTIVA"
  else
    echo "  ⏸ GUI: SPENTA (RAM liberata)"
  fi

  echo "═ API: agent.blender.pyragogy.org ═"
  if curl -s -m 5 "$API_URL" | grep -q '"status":"ok"'; then
    echo "  ✅ API: operativa"
  else
    echo "  ❌ API: NON raggiungibile"
  fi

  RAM=$(docker stats --no-stream --format "{{.MemUsage}}" \
    $(docker ps --format '{{.Names}}' | grep -E "blender|ilportale") 2>/dev/null | tr '\n' ' ')
  echo "  RAM usata: ${RAM:-n/d}"
  echo ""
  echo "Per risparmiare RAM: bash eco.sh off"
}

gui_off() {
  echo "⏸ Spegnimento GUI ($GUI_CONTAINER)..."
  docker stop "$GUI_CONTAINER" >/dev/null 2>&1
  echo "✅ GUI spenta — API su agent.blender.pyragogy.org resta attiva"
}

# Riavvia Blender GUI dentro il container con la scena giusta
restart_blender_gui() {
  local pid
  pid=$(docker exec "$GUI_CONTAINER" sh -c "pidof blender 2>/dev/null" 2>/dev/null | tr -d '\r')
  if [ -n "$pid" ]; then
    docker exec "$GUI_CONTAINER" sh -c "kill $pid 2>/dev/null" 2>/dev/null
    sleep 2
  fi
  docker exec "$GUI_CONTAINER" sh -c \
    "export XDG_RUNTIME_DIR=/config/.XDG; export WAYLAND_DISPLAY=wayland-1; export DISPLAY=:0; \
     blender $BLEND_FILE --python $STARTUP >/dev/null 2>&1 &" 2>/dev/null
  echo "  → Blender GUI caricato: $BLEND_FILE"
}

gui_on() {
  echo "⏺ Accensione GUI ($GUI_CONTAINER)..."
  if ! docker ps --format '{{.Names}}' | grep -q "^${GUI_CONTAINER}$"; then
    docker start "$GUI_CONTAINER" >/dev/null 2>&1
  fi

  echo "  → Attendo boot container (Wayland + Selkies)..."
  local n=0
  while [ $n -lt 40 ]; do
    if docker exec "$GUI_CONTAINER" sh -c "ls \$XDG_RUNTIME_DIR/wayland-1 2>/dev/null" 2>/dev/null | grep -q .; then
      echo "  → Wayland socket pronto"
      break
    fi
    sleep 3
    n=$((n+1))
  done

  restart_blender_gui
  echo "✅ GUI attiva — blender.pyragogy.org pronto in ~1 minuto"
}

# ── Dispatch ──────────────────────────────────────────────────

case "${1:-status}" in
  off|stop|down) gui_off ;;
  on|start|up)   gui_on ;;
  status|stat|"") status ;;
  *) echo "Uso: bash eco.sh [on|off|status]"; exit 1 ;;
esac