# ARCHITECTURE.md

## Visione

```
Voce ─→ LLM ─→ MCP (blender-mcp) ─→ API (blender-api) ─→ Blender headless + GPU
                    ↑                             ↑
                    └──── agenti esterni ─────────┘
```

**Il Portale** è un ambiente Blender + AI deployabile su Coolify.
L'agente AI (esterno) ragiona e usa gli strumenti MCP per interrogare e modificare
file .blend in modo non-distruttivo e tracciabile.

## Stack

| Layer        | Tecnologia                          |
|-------------|-------------------------------------|
| GUI Blender | `lscr.io/linuxserver/blender`       |
| Backend API | Python 3.12 + FastAPI + uvicorn     |
| MCP Server  | Model Context Protocol v2 (Streamable HTTP) |
| Container   | Docker Compose (3 servizi)          |
| Deploy      | Coolify                             |

## Servizi

### 1. blender — GUI web

- `ttl.sh/peeragogia/il-portale:latest` (default CMD)
- GUI web via browser su porta interna 3000
- Config persistente su `config/`
- Workspace condiviso su `workspace/`

### 2. blender-api — Backend Python

- `ttl.sh/peeragogia/il-portale:latest` con `command: ["/venv/bin/python", "-m", "app.api"]`
- **API HTTP** (porta interna 8100): REST per health, files, scene, render, versioni
- Avviato come processo separato

### 3. blender-mcp — Server MCP

- `ttl.sh/peeragogia/il-portale:latest` con `command: ["/venv/bin/python", "-m", "app.mcp_server"]`
- **MCP Server** (porta interna 8200): strumenti per agenti AI (SDK v2, Streamable HTTP)
- Avviato come processo separato

## Workspace

```
workspace/
├── originals/     # File .blend originali — MAI MODIFICATI
├── versions/      # Copie versionate (0001.blend, 0002.blend, ...)
├── renders/       # Output render per verifica
└── changes/       # Script applicati + metadati (audit trail)
```

## Versioning (non-distruttivo)

Ogni intervento produce:
1. Input (.blend originale)
2. Script eseguito (salvato in changes/ con SHA256)
3. Output (.blend versionato in versions/)
4. Render di verifica
5. ChangeRecord JSON con source, output, timestamp, script_sha256, description

## MCP Tools (v2 SDK)

- `list_blend_files` — elenca .blend nel workspace
- `inspect_blend` — struttura completa scena
- `inspect_object` — dettagli singolo oggetto
- `duplicate_version` — crea copia versionata
- `render_preview` — render headless
- `apply_script` — esegue script Python su .blend (gated)

## API HTTP

| Method | Path                | Descrizione                    |
|--------|---------------------|--------------------------------|
| GET    | /health             | Health check + feature flags   |
| GET    | /files              | Elenca file .blend             |
| GET    | /scene/{file}       | Struttura scena                |
| POST   | /render             | Render preview                 |
| POST   | /versions           | Crea versione (con/senza script) |
| POST   | /versions/duplicate | Solo duplica (sicura)          |
| GET    | /changes            | Elenca audit trail             |
| GET    | /changes/{id}       | Dettaglio change + script      |

## Path safety

- `resolve_input_blend()`: il file **deve esistere**, deve essere dentro workspace
- `resolve_workspace_output()`: il file **può non esistere**, confinato in versions/ o renders/
- Entrambe usano `Path.is_relative_to()`, non `startswith()`
- Output con `..`, `/`, path assoluti: rifiutati

## Security

Vedi `SECURITY.md` per rischi e mitigazioni.
`ENABLE_RAW_PYTHON=false` per default (apply_script disabilitato).

## Roadmap

Vedi `ROADMAP.md` per priorità e milestone.