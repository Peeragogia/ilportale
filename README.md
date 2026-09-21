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
cp [REDACTED SENSITIVE CONTEXT]example .env

# Avvia
docker compose up -d
```

## Servizi

| Servizio       | Porta | URL                    | Descrizione                        |
|---------------|-------|------------------------|------------------------------------|
| Blender GUI   | 3000  | http://localhost:3000   | Interfaccia web Blender            |
| API REST      | 8100  | http://localhost:8100   | Backend Python / health / files    |
| MCP (AI)      | 8200  | http://localhost:8200   | Model Context Protocol per agenti  |

## Health check

```bash
curl http://localhost:8100/health
# → {"status":"ok","service":"blender-agent","version":"0.1.0"}
```

## Stato attuale

> **Milestone 0.1 in corso** — tubatura deterministica.
> Vedi [ROADMAP.md](docs/ROADMAP.md) per dettagli.

### ✅ Funziona

- Struttura progetto completa
- `docker-compose.yml` funzionante
- API HTTP con endpoint /health, /files, /scene, /render, /versions
- Server MCP con 7 strumenti
- Versioning non-distruttivo
- Validazione path sicurezza
- Blender scripts (inspect, render, apply change)
- CI pipeline (validate)

### 🔧 Da testare su Coolify

- Deploy end-to-end
- Blender web funzionante via browser
- MCP che risponde con struttura scena reale
- Render headless funzionante

## Documentazione

- [Architettura](docs/ARCHITECTURE.md)
- [Deploy Coolify](docs/COOLIFY.md)
- [Sicurezza](docs/SECURITY.md)
- [Roadmap](docs/ROADMAP.md)

## Licenza

MIT — vedi [LICENSE](LICENSE)