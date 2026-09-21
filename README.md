# Il Portale — Blender AI Stack

Ambiente Blender + AI deployabile su Coolify.

## Prerequisiti

- Docker + Docker Compose
- Coolify (opzionale, per deploy gestito)

## Avvio locale

```bash
# Clona
git clone https://github.com/Peeragogia/ilportale.git
cd ilportale

# Copia env e configura
cp .env.example .env

# Avvia (3 servizi: blender GUI, API, MCP)
docker compose up -d
```

## Servizi

| Servizio      | Porta (int.) | Descrizione                        |
|---------------|-------------|------------------------------------|
| Blender GUI   | 3000        | Interfaccia web Blender            |
| API REST      | 8100        | Backend Python per operazioni file |
| MCP (AI)      | 8200        | Model Context Protocol per agenti  |

## Health check

```bash
curl http://localhost:8100/health
# → {"status":"ok","service":"blender-api","version":"0.1.0",...}
```

## Milestone 0.1 — operazioni supportate

| Operazione      | API | MCP | Descrizione                            |
|----------------|-----|-----|----------------------------------------|
| list files     | ✅  | ✅  | Elenca file .blend nel workspace       |
| inspect scene  | ✅  | ✅  | Ispeziona struttura scena (oggetti, materiali) |
| render preview | ✅  | ✅  | Genera render da Blender headless      |
| duplicate      | ✅  | ✅  | Crea copia versionata in versions/     |
| apply script   | ⛔  | ⛔  | Disabilitato di default (vedi sotto)   |

**apply_script (raw Python)** è un RCE. Disabilitato per default con `ENABLE_RAW_PYTHON=false`.
Per il milestone 0.1 bastano list/inspect/render/duplicate.

## Audit trail

Ogni modifica applicata crea:
- `workspace/versions/NNNN.blend` — file versionato
- `workspace/changes/NNNN.py` — script archiviato
- `workspace/changes/NNNN.json` — metadati (source, output, sha256, timestamp)

## Documentazione

- [Architettura](docs/ARCHITECTURE.md)
- [Deploy Coolify](docs/COOLIFY.md)
- [Sicurezza](docs/SECURITY.md)
- [Roadmap](docs/ROADMAP.md)

## Licenza

MIT — vedi [LICENSE](LICENSE)