# SECURITY.md

## Rischio principale

Il container `lscr.io/linuxserver/blender:latest` include:
- **Terminale web** accessibile tramite GUI
- **Privilegi elevati** — richiede `SYS_ADMIN` per DBus/audio
- **Esposizione di porta** su browser

Questo lo rende **potenzialmente pericoloso** se esposto su Internet pubblica
senza protezioni aggiuntive.

## Mitigazioni attuali

Nel `docker-compose.yml`:

- `no-new-privileges:true` — impedisce escalation via SUID
- `cap_drop: ALL` — rimuove tutte le capability non necessarie
- `cap_add: SYS_ADMIN` — la sola capability richiesta (e documentata)
- **NON** montiamo `/var/run/docker.sock` — nessun escape container via Docker
- Password per la GUI Blender impostabile via `BLENDER_PASSWORD`

## Rischi residui

1. **SYS_ADMIN** è una capability potente — riduce l'isolamento del container
2. Il terminale web Blender permette esecuzione di comandi arbitrari
3. Volume `/workspace` condiviso — un compromissione di un servizio
   compromette l'altro

## Raccomandazioni per produzione

- **Non esporre Blender su Internet pubblica**. Usa VPN (Tailscale/WireGuard)
  o IP whitelist se l'accesso deve essere remoto.
- Imposta una **password forte** per la GUI Blender.
- Considera un **reverse proxy** con Basic Auth aggiuntivo per blender-agent API/MCP.
- **Monitoraggio**: tieni traccia di chi accede alla GUI Blender.
- **Backup**: il workspace contiene i .blend originali — backup esterno.
- **Blender-agent** (`apply_blender_script_tool`) è un'operazione sensibile:
  lo strumento MCP valida che i path siano dentro il workspace.

## Non fare

- ❌ Montare `/var/run/docker.sock` per "comodità"
- ❌ Esporre Blender sulla porta 3000 senza autenticazione
- ❌ Usare `BLENDER_PASSWORD` vuoto in produzione
- ❌ Abilitare `privileged: true` nel container Blender