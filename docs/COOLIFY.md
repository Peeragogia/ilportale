# COOLIFY.md — Deploy su Coolify

## 1. Importa la repository

1. Vai su **Coolify Dashboard → Resources → New Resource → Private Repository (Git)**
2. Connetti il tuo account GitHub / Git provider
3. Seleziona `Peeragogia/ilportale`
4. Seleziona il branch: `feat/blender-ai-stack`

## 2. Servizi nel docker-compose

Il `docker-compose.yml` definisce due servizi pubblicabili:

| Servizio        | Porta interna | Pubblica su |
|----------------|---------------|-------------|
| blender        | 3000          | Dominio A   |
| blender-agent  | 8100          | Dominio B (API) |
| blender-agent  | 8200          | Dominio C (MCP) |

## 3. Configurazione in Coolify

Per ogni servizio:

### blender (GUI)

- **Port**: 3000
- **Dominio**: imposta un sottodominio con HTTPS (es. `blender.iltuodominio.it`)
- **Persistent volumes**:
  - `/config` → volume persistente Coolify
  - `/workspace` → volume persistente condiviso con blender-agent

### blender-agent (API + MCP)

- **Porte**: 8100 (API), 8200 (MCP)
- **Dominio**: imposta due domini o usa path rewriting
- **Persistent volumes**: `/workspace` (stesso volume di blender)

## 4. Variabili d'ambiente

Imposta nel Coolify **Environment Variables** per ogni servizio:

```env
TZ=Europe/Rome
PUID=1000
PGID=1000
BLENDER_USER=admin
BLENDER_PASSWORD=your_secure_password
API_PORT=8100
MCP_PORT=8200
```

## 5. Dominio e HTTPS

1. Coolify gestisce automaticamente Let's Encrypt per i tuoi domini
2. Per il MCP server (porta 8200): è un server HTTP semplice, per produzione
   valuta di proteggerlo con **Basic Auth** o **API key** a monte

## 6. Health check

Dopo il deploy, verifica:

```bash
curl https://api.iltuodominio.it/health
# → {"status":"ok","service":"blender-agent","version":"0.1.0"}
```

## 7. Verifica Blender web

Apri `https://blender.iltuodominio.it` nel browser.
Dovresti vedere l'interfaccia Blender via web.

## Note importanti

- **Blender non va esposto direttamente su Internet pubblica** senza protezione
  aggiuntiva (password forte, IP whitelist, VPN). Vedi `SECURITY.md`.
- I render generano output PNG: imposta un volume persistente per `./workspace/renders/`
  se vuoi conservarli tra i deploy.