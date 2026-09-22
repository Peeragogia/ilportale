# Il Portale — AGENTS.md

## Missione

Pi è l'agente LLM di Il Portale. L'utente parla in italiano naturale, Pi interpreta
l'intento, sceglie il tool, e chiama il container Blender via REST.

Pi sostituisce completamente il parser regex come cervello del sistema. Le regex
in `agent.py` restano solo come fallback/debug per il vecchio endpoint `/chat`.

## Stack

- **Pi → LLM agent**: interpreta NL, decide tool, chiama REST
- **Container**: `ttl.sh/peeragogia/il-portale:latest` su Coolify
- **Deploy**: `91.99.70.26`, container `ilportale-api`
- **Registry**: `ttl.sh/peeragogia/il-portale:latest`
- **Volume workspace**: `qfrr3ylfwtz97sws9bjuwl8y_workspace` → `/workspace/`

### Nuova architettura

```
Utente (Italiano)
  │
  ▼
┌───────────────────────────────────────────┐
│  Pi (LLM)                                 │
│  • Capisce "Vediamo com'è fatta..."      │
│  • Decide: /tools/inspect                 │
│  • Chiama: blender_tool.py inspect ...     │
└──────────────────┬────────────────────────┘
                   │ REST (HTTPS)
                   ▼
┌───────────────────────────────────────────┐
│  Container (8100)                         │
│  /tools/inspect → blender_tools.py        │
│  /tools/duplicate → ...                   │
│  /tools/move → ...                        │
│  /tools/render → blender -F PNG CLI       │
│  /tools/undo → ripristino versione        │
└───────────────────────────────────────────┘
                   │ Subprocess
                   ▼
┌───────────────────────────────────────────┐
│  Blender --background                      │
│  Data API (no bpy.ops)                     │
│  Salva versione + audit trail             │
└───────────────────────────────────────────┘
```

### Struttura file
```
/workspace/
├── base/           # PORTALE.blend (originale, mai modificato)
├── versions/       # 0001.blend ... 00XX.blend (versioni incrementali)
├── renders/        # preview_*.png (render output)
├── changes/        # audit trail (JSON + script)
└── state.db        # SQLite — stato conversazione persistente
```

### Servizi nel container
| Servizio | Porta | URL |
|----------|-------|-----|
| API REST | 8100 | `https://agent.blender.pyragogy.org` |
| MCP Server | 8200 | direct (non via Traefik) |
| Blender GUI | 3000 | `https://blender.pyragogy.org` (schermo nero — bug Selkies/Wayland) |

## Convenzioni di codice

### Tool endpoints (api.py — v0.2.1)
- **`/tools/inspect`** — ispeziona oggetto per nome, risolve fuzzy
- **`/tools/list`** — elenca oggetti nella scena
- **`/tools/duplicate`** — duplica oggetto, salva versione
- **`/tools/move`** — sposta (relativo default), salva versione
- **`/tools/rotate`** — ruota in gradi, salva versione
- **`/tools/hide`** / **`/tools/show`** — visibilità
- **`/tools/render`** — render via CLI `-F PNG`
- **`/tools/undo`** — ripristina versione precedente
- **`/tools/reset`** — resetta stato persistente
- **`/tools/schema`** — descrizione tool per LLM

Tutti i tool endpoints **non richiedono `blend_path`** — si risolve automaticamente
dallo stato SQLite persistente (ultimo file modificato).

### Persistent state (state.py)
- SQLite in `/workspace/state.db` (sopravvive a restart container)
- Chiavi: `current_blend`, `last_referenced_object`, `last_created_object`,
  `last_change_id`, `last_tool_call`
- Inizializzato al primo import, thread-safe con WAL mode

### Pi-side tool (blender_tool.py)
Script che Pi esegue via bash per ogni operazione:
```bash
python3 blender_tool.py inspect '{"object_name": "Tastiera"}'
python3 blender_tool.py duplicate '{"object_name": "Tastiera", "new_name": "Tastiera_copia"}'
python3 blender_tool.py move '{"object_name": "Tastiera_copia", "x": 2.0, "y": 0, "z": 0}'
python3 blender_tool.py render '{"frame": 1}'
python3 blender_tool.py undo '{}'
python3 blender_tool.py status '{}'
```
Config: `BLENDER_API_URL` (default: `https://agent.blender.pyragogy.org`)

### Blender scripts (blender_tools.py, blender.py)
- **Mai `bpy.ops`** per modifiche (fallisce in background mode)
- Data API: `bpy.data.objects[].location = ...`, `.copy()`, `.new()`
- Render: CLI flags `-F PNG -o ... -f 1` (bypassa Blender 5.2 bug formato)
- shell=False sempre

### Object resolution
exact → case-insensitive → fuzzy unico (mai fallback a selected/active)

## Deploy su Coolify

### Build e deploy
```bash
cd /home/coder/project/Il_Portale-20026

# Build su server
scp -r services/ root@91.99.70.26:/root/ilportale/
ssh root@91.99.70.26 "cd /root/ilportale && docker build -t ttl.sh/peeragogia/il-portale:latest . && docker push ttl.sh/peeragogia/il-portale:latest"

# Deploy
docker compose -f /root/deploy-server.yml up -d --pull always

# Test base
curl -s http://127.0.0.1:8100/health
curl -s http://127.0.0.1:8100/tools/schema
```

### Coolify-specific
- Docker labels su `coolify` network funzionano
- Nomi router **unici**: `ilportale-api`, `ilportale-mcp`
- Servizio UUID: `qfrr3ylfwtz97sws9bjuwl8y`

## Test di accettazione — Frase spontanea

**5 test che DEVONO passare in linguaggio naturale vario:**

### Step 1: Ispezione
```
Frase: "Vediamo com'è fatta quella tastiera."
Tool:  /tools/inspect {"object_name": "Tastiera"}
→ Deve restituire 172 vertici, 148 facce
```

### Step 2: Duplica
```
Frase: "Facciamone una copia così posso pasticciarci senza rompere l'originale."
Tool:  /tools/duplicate {"object_name": "Tastiera", "new_name": "Tastiera_copia"}
→ Crea Tastiera_copia, nuova versione incrementale
```

### Step 3: Sposta
```
Frase: "Portamela un po' sulla destra."
Tool:  /tools/move {"object_name": "Tastiera_copia", "x": 2.0, "y": 0, "z": 0, "relative": true}
→ Delta X +2 from original, nuova versione
```

### Step 4: Render
```
Frase: "Fammi vedere com'è venuta."
Tool:  /tools/render {"frame": 1}
→ PNG in /workspace/renders/, URL /render-file/{name}
```

### Step 5: Undo
```
Frase: "No, era meglio prima."
Tool:  /tools/undo {}
→ Ripristina versione precedente, crea nuova versione undo
```

Nessuna di queste frasi è codificata in regex. Il sistema funziona perché
**Pi (LLM) interpreta il linguaggio naturale** e sceglie il tool giusto.

### Esecuzione
```bash
# Sul server
ssh root@91.99.70.26 "cd /root && python3 test_spontaneous.py"

# Da remoto con Pi
python3 blender_tool.py inspect '{"object_name": "Tastiera"}'
```

## Bug noti

1. **Blender GUI schermo nero**: Selkies/WebRTC non mostra contenuto 3D
   - Causa: Wayland compositor si ferma ("Capture loop stopped")
   - Workaround: usare API per tutte le operazioni
   - Fix potenziale: GPU passthrough o configurazione software rendering

2. **Traefik route `/mcp`**: conflitto router → MCP via HTTPS non funziona
   - Workaround: porta interna 8200 via SSH diretto

3. **MCP richiede sessione**: prima richiesta ottiene `mcp-session-id` in header
   (funziona su porta diretta, non via Traefik)

4. **Nessuna LLM API key nel container**: l'LLM è Pi (qui), non nel container

5. **Stato conversazione via /chat endpoint**: agent.py ha stato in-memory + SQLite
   (persistente via state.db). I /tools/* endpoints usano SQLite.

## Roadmap

- [x] **Milestone 0.1**: 5-step accettazione con regex agent
- [x] **Milestone 0.2**: Pi come LLM agent, /tools/* endpoints, stato persistente SQLite
- [ ] **Milestone 0.3**: Fix Blender GUI (schermo nero)
- [ ] **Milestone 0.4**: ChatGPT connector via MCP (quando account OpenAI lo supporta)
- [ ] **Milestone 0.5**: LLM API key nel container per agente autonomo

## Comandi utili

```bash
# SSH
ssh root@91.99.70.26

# Log API
docker logs ilportale-api --tail 30

# Log Traefik (filtro errori nostri)
docker logs coolify-proxy 2>&1 | grep -i "ilportale\|error" | tail -10

# Porte attive
docker exec ilportale-api sh -c 'ss -tlnp | grep -E "8100|8200"'

# Stato persistente
curl -s https://agent.blender.pyragogy.org/state
```