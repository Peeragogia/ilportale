# ROADMAP.md

## Milestone 0.1 — Tubatura deterministica 🎯

Obiettivo: repo → Coolify → Blender web funzionante → .blend condiviso
→ agente che lo legge → MCP che restituisce la struttura della scena
→ render headless funzionante.

- [x] `docker-compose.yml` con blender + blender-agent
- [x] Blender GUI web via linuxserver/blender
- [x] Backend Python con FastAPI
- [x] Server MCP con strumenti di base
- [x] Script Blender (inspect_scene, render_preview, apply_change)
- [x] Versioning non-distruttivo
- [x] Validazione path sicurezza
- [ ] Deploy su Coolify e test end-to-end
- [ ] Blender web funzionante via browser
- [ ] MCP risponde con struttura scena reale
- [ ] Render headless produce immagine

## Milestone 0.2 — Operatività

- [ ] Upload .blend via API
- [ ] Comandi di modifica strutturale (aggiungi/rimuovi/sposta oggetti)
- [ ] Lista modifiche applicate con rollback
- [ ] Inventario completo dello stato

## Milestone 0.3 — Voce → AI → MCP

Percorso esplicito: **Voice → LLM → MCP → Blender Core → versioned .blend → render → multimodal review**

- [ ] Integrazione speech-to-text
- [ ] LLM agente che usa strumenti MCP
- [ ] Loop di review: AI vede render, decide se iterare
- [ ] Pipeline modulare (ogni blocco sostituibile)

## Milestone 0.4 — Multi-agente

- [ ] Più agenti specializzati (geometria, materiali, lighting)
- [ ] Coda richieste e lock sui file
- [ ] Notifiche su modifiche completate

## Principi guida

> **Niente "AI magic" nella prima iterazione.** Prima costruiamo una tubatura
> deterministica che sa aprire, interrogare, clonare e renderizzare un .blend.
> Quando quella funziona, collegarci un agente diventa quasi banale.

- Model-agnostic: MCP non contiene chiamate a LLM
- Non-distruttivo: mai modificare l'originale
- Tracciabile: ogni modifica ha script + output + render
- Deployabile: docker-compose funziona su Coolify out of the box