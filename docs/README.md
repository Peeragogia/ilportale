# Il Portale — Documentazione

Indice e bussola della documentazione di progetto.

## Documenti radice

| File | Contenuto |
|------|-----------|
| [`BRIEF.md`](BRIEF.md) | **Project Brief** — visione, concept, obiettivi, strategia. Fonte di verità per la progettazione. |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | **Architettura di sistema** — stack, servizi, API, MCP, versioning, path safety. |
| [`ROADMAP.md`](ROADMAP.md) | **Roadmap e milestone** — priorità, progresso, principi guida. |
| [`COMMANDS.md`](COMMANDS.md) | **Comandi operativi** — Blender CLI, API, MCP, docker, reference rapido. |
| [`COOLIFY.md`](COOLIFY.md) | **Deploy su Coolify** — configurazione servizi, networking, aggiornamenti. |
| [`SECURITY.md`](SECURITY.md) | **Sicurezza** — rischi e mitigazioni per il container Blender esposto. |
| [`REFERENCE_PADIGLIONE_TE.md`](REFERENCE_PADIGLIONE_TE.md) | **Reference originale** — foto e link del Padiglione del Tè (pre-dossier). |
| [`SESSION_2026-10-13.md`](SESSION_2026-10-13.md) | **Diario sessione** — blockout v1, renders, auto-review, GUI fix. |

## Dossier di ricerca — Caprotti

Il dossier completo è in [`docs/caprotti/`](caprotti/README.md):

| Documento | Contenuto |
|-----------|-----------|
| `PROJECT_ORIGIN.md` | Cosa proponeva il progetto originale 2013/2016 |
| `PROJECT_BRIEF.md` | Missione di design aggiornata |
| `RESEARCH_REPORT.md` | Ricerca storico-contestuale e conclusioni |
| `SOURCE_REGISTER.md` | Fonti e cosa supportano |
| `EVIDENCE_REGISTER.md` | Classificazione claim-by-claim (OBSERVED/INFERRED/UNKNOWN) |
| `IMAGE_REFERENCE_CATALOG.md` | Board visivo con riferimenti pubblici |
| `VISUAL_ANALYSIS.md` | Lettura architettonica del padiglione |
| `MEASUREMENT_AND_SURVEY_PLAN.md` | Come ottenere misure reali da foto + sopralluogo |
| `BLENDER_RECONSTRUCTION_PLAN.md` | Sequenza modellazione e struttura scena |
| `QUALITY_REVIEW_RUBRIC.md` | Gate qualità per Pi |
| `PI_START_PROMPT.md` | Prompt esatto per far partire Pi sul progetto |
| `DECISIONS_AND_OPEN_QUESTIONS.md` | Decisioni, incertezze e gap di ricerca |
| `evidence_matrix.csv` | Matrice evidenze machine-readable |
| `reference-manifest.schema.json` | Schema metadati per reference |

## Sessioni e meeting

| File | Data | Oggetto |
|------|------|---------|
| [`SESSION_2026-10-13.md`](SESSION_2026-10-13.md) | 13/10/2026 | Blockout v1, renders, auto-review, GUI fix |

## Reference images su disco

Le immagini pubbliche (6 foto da BergamoNews e PrimaBergamo) sono in:
```
workspace-reference-template/references/caprotti/public/
```
con versioni ridotte `_v.jpg` (max 1000px). Non sono in git — policy: nessuna immagine terza nel repository.

## Struttura sessioni future

Ogni sessione produce un file `SESSION_<DATA>.md` in `docs/` con:
- Scopo e milestone
- Decisioni prese
- Blend versions create
- Renders prodotti
- Problemi incontrati e soluzioni
- Prossimi passi