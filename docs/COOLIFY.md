# COOLIFY.md — Deploy su Coolify

## 1. Importa la repository

1. Vai su **Coolify Dashboard → Resources → New Resource → Private Repository (Git)**
2. Connetti il tuo account GitHub / Git provider
3. Seleziona `Peeragogia/ilportale`
4. Seleziona il branch: `fix/review-p0`

## 2. Servizi nel docker-compose

Il `docker-compose.yml` definisce **tre servizi** che condividono la stessa immagine:

| Servizio      | Porta interna | Comando                         |
|--------------|--------------|---------------------------------|
| blender      | 3000         | Default (backend + /init GUI)   |
| blender-api  | 8100         | `python -m app.api`             |
| blender-mcp  | 8200         | `python -m app.mcp_server`      |

Usano `expose:` (non `ports:`) — Coolify gestisce il routing via dominio.

## 3. Configurazione in Coolify

Per ogni servizio:

### blender (GUI)
- **Port**: 3000
- **Dominio**: `blender.iltuodominio.it` (es.)
- **Persistent volumes**:
  - `/config` → volume persistente
  - `/workspace` → volume persistente condiviso con API/MCP

### blender-api (backend)
- **Port**: 8100
- **Dominio**: `api.iltuodominio.it` (es.) — **non esporre pubblicamente**
- **Persistent volumes**: `/workspace` (stesso volume di blender)

### blender-mcp (MCP agents)
- **Port**: 8200
- **Dominio**: `mcp.iltuodominio.it` (es.) — **non esporre pubblicamente**
- **Persistent volumes**: `/workspace` (stesso volume)

## 4. Variabili d'ambiente globali

```env
TZ=Europe/Rome
PUID=1000
PGID=1000
CUSTOM_USER=admin
PASSWORD=your_secure_password
WORKSPACE_DIR=/workspace
ENABLE_RAW_PYTHON=false
```

## 5. Dominio e HTTPS

1. Coolify gestisce automaticamente Let's Encrypt
2. Per sicurezza: API e MCP su **rete interna** o dietro Basic Auth
3. La GUI Blender contiene terminale: proteggere con password forte

## 6. Health check

```bash
curl https://api.iltuodominio.it/health
# → {"status":"ok","service":"blender-api","version":"0.1.0"}
```

## 7. Verifica Blender web

Apri `https://blender.iltuodominio.it` nel browser.

## Note importanti

- **Blender GUI, API e MCP non vanno esposti su Internet pubblica** senza
  protezione. Vedi `SECURITY.md`.
- I render vanno in `workspace/renders/`: volume persistente tra i deploy.
- `ENABLE_RAW_PYTHON=false` per default: attiva solo se serve apply_script.