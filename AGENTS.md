# Il Portale — AGENTS.md

## Missione

Pi è l'agente operativo end-to-end di Il Portale: l'utente parla in italiano, Pi controlla Blender via tool deterministici (MCP/REST), modifica il file reale, salva/versiona, e mostra risultati.

**Non** costruire UI sperimentali, parser NL custom, o chatbot separati. L'interfaccia è l'agente stesso su `agent.blender.pyragogy.org`.

## Stack

- **Container**: `lscr.io/linuxserver/blender:latest` esteso con Python backend
- **Servizi (stesso container)**: API (8100), MCP (8200), Blender GUI (3000 via KasmVNC)
- **Deploy**: Coolify su `console.pyragogy.org` → `91.99.70.26`
- **Registry**: `ttl.sh/peeragogia/il-portale:latest`
- **Volume workspace**: `qfrr3ylfwtz97sws9bjuwl8y_workspace` → `/workspace/`

### Struttura file
```
/workspace/
├── base/           # PORTALE.blend (originale, mai modificato)
├── versions/       # 0001.blend ... 00XX.blend (versioni incrementali)
└── renders/        # preview_*.png (render output)
```

### Servizi nel container
| Servizio | Porta | URL |
|----------|-------|-----|
| Chat API | 8100 | `https://agent.blender.pyragogy.org` (chat/agent endpoints) |
| MCP Server | 8200 | `https://agent.blender.pyragogy.org/mcp` (routing problematico) |
| Blender GUI | 3000 | `https://blender.pyragogy.org` (KasmVNC, schermo nero) |

## Convenzioni di codice

### Architettura agent (agent.py)
- Singleton `Agent` mantiene `ConversationState` in memoria (perde su restart)
- Flusso: `handle(msg)` → classify intent → extract entities → resolve references → execute → aggiorna stato
- Object resolution: exact → case-insensitive → fuzzy unico (mai fallback a active/selected)
- Pronoun: "ne", "la", "lo", "quello" → `last_referenced_object`; "copia" → `last_created_object`

### Blender scripts (blender_tools.py)
- **Mai usare `bpy.ops` per operazioni di modifica** — fallisce in background mode (nessun contesto viewport)
- Usare **data API** per tutto: `bpy.data.objects[].location = (x,y,z)`, `bpy.data.objects.new()`, etc.
- `bpy.ops.wm.save_mainfile()` funziona in background — usalo solo per salvare
- Ogni script tool produce `print("OJSON:" + json.dumps(info))` per output strutturato

### Render (blender.py)
- **Usare CLI flags di Blender**, non Python API: `blender -b file.blend -F PNG -o /output/preview_ -f 1`
- Motivo: Blender 5.2 bug — `image_settings.file_format` rifiuta settaggi PNG (il file PORTALE.blend ha FFMPEG bloccato)
- CLI bypassa completamente il bug

### Path safety
- `resolve_input_blend()`: solo path relativi a `/workspace/`, niente `..` o path assoluti
- `resolve_workspace_output()`: solo nome file, sempre in `versions/` o `renders/`
- `shell=False` in tutti i `subprocess.run()`
- `ENABLE_RAW_PYTHON=false` in produzione

## Deploy su Coolify

### Container docker
```bash
# Ricreare container sul server
docker compose -f /root/deploy-server.yml up -d --pull always

# Test locali
curl -s http://127.0.0.1:8100/health
curl -s http://127.0.0.1:8100/chat -H "Content-Type: application/json" \
  -d '{"message":"Analizza la Tastiera"}'

# Update singolo file e rebuild
scp services/blender-agent/app/agent.py root@91.99.70.26:/root/ilportale/services/blender-agent/app/
ssh root@91.99.70.26 "cd /root/ilportale && docker build -t ttl.sh/peeragogia/il-portale:latest . && docker push ttl.sh/peeragogia/il-portale:latest && docker compose -f /root/deploy-server.yml up -d --pull always"
```

### Coolify-specific
- Coolify gestisce Traefik via `coolify-proxy` container
- Docker labels su `coolify` network funzionano MA:
  - I router NEL container Coolify (blender-qfrr3ylfwtz97sws9bjuwl8y) hanno PRIORITÀ
  - Usare nomi router **unici** che non confliggono: `ilportale-api`, `ilportale-mcp`
  - Specificare SEMPRE `traefik.http.routers.<name>.service=<service>` esplicitamente
  - Il path `/mcp` su `agent.blender.pyragogy.org` non funziona via HTTPS (conflitto router Traefik)

### Versione Coolify
- Coolify 4.3.23 su server Pyragogy-Core (UUID: `h0okws84sock040owkokk0sk`)
- Service UUID: `qfrr3ylfwtz97sws9bjuwl8y`

## Test di accettazione

5 step che DEVONO funzionare end-to-end:

1. `"Analizza la Tastiera e dimmi come è costruita"` → inspect su PORTALE.blend
2. `"Creane una copia di lavoro senza modificare l originale"` → duplicate, Tastiera_copia, nuova versione
3. `"Spostala di lato cosi posso confrontarle"` → move verso destra, nuova versione
4. `"Fammi vedere il risultato"` → render con CLI `-F PNG`
5. `"Non mi piace torna indietro"` → undo a versione precedente

### Per testare
```bash
# Sul server
ssh root@91.99.70.26 "cd /root && python3 test_acceptance.py"

# Da remoto
curl -s https://agent.blender.pyragogy.org/chat -H "Content-Type: application/json" \
  -d '{"message":"Analizza la struttura"}' --max-time 120
```

## MCP Server

- `mcp_server.py` su porta 8200, Streamable HTTP transport (`streamable_http_path="/"`)
- Richiede **session management**: prima richiesta ottiene `mcp-session-id` in header, poi usa in requests
- Accetta: `Accept: application/json, text/event-stream`
- Tools: `inspect_scene`, `duplicate_object`, `move_object`, `rotate_object`, `hide_object`, `show_object`, `render_preview`

## Bug noti

1. **Traefik route `/mcp`**: conflitto router → MCP via HTTPS non funziona. Workaround: usare porta interna 8200 via SSH
2. **Blender GUI schermo nero**: KasmVNC/WebRTC su `blender.pyragogy.org` non mostra contenuto 3D
3. **Stato agente**: in-memory, si perde su restart container
4. **Nessuna LLM API key**: non c'è inferenza NL — agente usa regex pattern matching

## Roadmap futura

- [ ] Connessione ChatGPT via MCP (fixare routing Traefik per /mcp)
- [ ] LLM API key per NL inferenza (OpenRouter/OpenAI)
- [ ] State persistente (Redis/file)
- [ ] Blender GUI funzionante (configurazione virtual display)
- [ ] Merge fix/review-p0 → master

## Comandi utili

```bash
# SSH al server
ssh root@91.99.70.26

# Log container
docker logs ilportale-api --tail 20

# Log Traefik
docker logs coolify-proxy 2>&1 | grep -i "ilportale\|error" | tail -10

# Porte attive
docker exec ilportale-api sh -c 'ss -tlnp | grep -E "8100|8200"'

# Ripristina original (se workspace corrotto)
docker exec ilportale-api sh -c 'cp /workspace/base/PORTALE.blend /workspace/versions/0001.blend'

# Build e push
cd /home/coder/project/Il_Portale-20026
docker build -t ttl.sh/peeragogia/il-portale:latest .
docker push ttl.sh/peeragogia/il-portale:latest
```