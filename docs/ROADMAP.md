# ROADMAP.md — Il Portale

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
- [x] Deploy su Coolify e test end-to-end
- [x] Blender web funzionante via browser
- [x] MCP risponde con struttura scena reale
- [x] Render headless produce immagine

✅ **Milestone 0.1 completata** (13/10/2026).

## Milestone 0.2 — Blockout Caprotti 🎯

Obiettivo: modello Blender riconoscibile del Padiglione del Tè di Parco Caprotti,
con Il Portale installato all'interno, versioni tracciabili e renders di verifica.

### Fase 2.1 — Dossier e ricerca
- [x] Importazione dossier Caprotti (`docs/caprotti/`)
- [x] Review dossier — CONDITIONAL GO 83/100
- [x] Verifica 6 URL immagini pubbliche (HTTP 200)
- [x] Pixel analysis per proporzioni (OpenCV)

### Fase 2.2 — Blockout architettonico
- [x] Script blockout v1 (`services/scripts/caprotti_blockout_v1.py`)
- [x] 0044.blend — 215 oggetti, 5 camere, collezioni evidenza-taggate
- [x] 5 renders Eevee (3 esterni, 2 interni)
- [x] Auto-review: **76/100** — GATE NON SUPERATO (< 80)

### Bloccante: illuminazione interna
- [ ] Aggiungere point light soffuse dentro il padiglione
- [ ] Ri-renderizzare INT_ENTRANCE + INT_PORTALE_POSITION
- [ ] Re-auto-review (gate ≥ 80 per sbloccare Fase 2.3)

### Fase 2.3 — Ipotesi collocazione
- [ ] Ipotesi A — centrale/iconico
- [ ] Ipotesi B — laterale/funzionale
- [ ] Ipotesi C — ambiente integrato
- [ ] Renders comparativi + note PROVVISORIO

### Fase 2.4 — Raffinamento
- [ ] Refine architettonico (cornici, colonne, fregi, statue, materiali)
- [ ] Experience design (ingresso, utente, seduta, tastiera, schermo, audio)
- [ ] 6 renders finali (3 esterne + 2 interne + 1 esperienza utente)

## Milestone 0.3 — Misure reali e calibrazione

- [ ] Sopralluogo Fabrizio — foto retro/tetto + misure reali
- [ ] Riscalatura del modello da proporzionale a metrico
- [ ] Validazione con foto reali
- [ ] Report finale "Il Portale al Padiglione del Tè"

## Milestone 0.4 — Voce → AI → MCP

- [ ] Integrazione speech-to-text
- [ ] LLM agente che usa strumenti MCP
- [ ] Loop di review: AI vede render, decide se iterare
- [ ] Pipeline modulare (ogni blocco sostituibile)

## Milestone 0.5 — Multi-agente

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