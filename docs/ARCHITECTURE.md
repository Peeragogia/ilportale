# ARCHITECTURE.md

## Visione

```
Voce ─→ LLM ─→ MCP ─→ Blender Core ─→ versioned .blend ─→ render ─→ multimodal review
```

**Il Portale** è un ambiente Blender + AI deployabile su Coolify.
L'agente AI (esterno) ragiona e usa gli strumenti MCP per interrogare e modificare
file .blend in modo non-distruttivo e tracciabile.

## Stack

| Layer        | Tecnologia                          |
|-------------|-------------------------------------|
| GUI Blender | `lscr.io/linuxserver/blender`      |
| Backend     | Python 3.12 + FastAPI               |
| MCP Server  | Model Context Protocol (Streamable HTTP) |
| Container   | Docker Compose                      |
| Deploy      | Coolify                             |

## Servizi

### 1. blender (linuxserver/blender)

- GUI web via browser su porta 3000
- Config persistente su `./config/`
- Workspace condiviso su `./workspace/`
- **Non esporre direttamente su Internet** — contiene terminale e privilegi

### 2. blender-agent (custom Python)

- **API HTTP** (porta 8100): REST per health, files, scene, render, versioni
- **MCP server** (porta 8200): strumenti per agenti AI

## Workspace

```
workspace/
├── originals/     # File .blend originali — MAI MODIFICATI
├── versions/      # Copie versionate (0001.blend, 0002.blend, ...)
├── renders/       # Output render per verifica
└── changes/       # Script applicati (traccia modifiche)
```

## Versioning (non-distruttivo)

Ogni intervento produce:
1. Input (.blend originale)
2. Script eseguito (salvato in changes/)
3. Output (.blend versionato)
4. Render di verifica
5. Metadati della modifica

## MCP Tools

- `list_blend_files` — elenca .blend nel workspace
- `inspect_blend` — struttura completa scena
- `inspect_object` — dettagli singolo oggetto
- `duplicate_version` — crea copia versionata
- `render_preview` — render headless
- `apply_blender_script` — esegue script Python su .blend (sensibile)

## API HTTP

| Method | Path         | Descrizione                |
|--------|-------------|----------------------------|
| GET    | /health     | Health check               |
| GET    | /files      | Elenca file .blend         |
| GET    | /scene/{file} | Struttura scena          |
| POST   | /render     | Render preview             |
| POST   | /versions   | Crea versione con script   |

## Security

Vedi `SECURITY.md` per rischi e mitigazioni.

## Roadmap

Vedi `ROADMAP.md` per priorità e milestone.