# Peeragogy on Music — Publication Scaffold

Questa cartella ospita lo sviluppo editoriale del progetto **Peeragogy on Music**,
dal concept originale 2013–2016 al Civic Music Learning Point contemporaneo.

## Stato

**Scaffold iniziale** — nessun contenuto definitivo.

## Regole

1. **Fonte primaria**: il PDF storico in `docs/caprotti/source-material/Peeragogy_on_Music.pdf`
   è il documento originale. Non viene riscritto, corretto o reinterpretato liberamente.
2. **Distinzione rigorosa**: fonte originale, ricostruzione storica, sviluppi contemporanei
   e interpretazioni attuali sono tenuti separati.
3. **Niente claim nuovi presentati come storici** — ogni affermazione nuova è marcata come tale.
4. **Versioni**: il documento evolve per versioni, non in un unico passo.

## Arco narrativo

L'arco editoriale del documento segue cinque strati, ognuno con una sezione dedicata:

```
2013/2016 concept          → sections/01_origin.tex
     ↓
Original technical object  → sections/02_concept.tex
     ↓
Learning City Point       → sections/03_learning_point.tex
     ↓
Caprotti 2026             → sections/04_caprotti.tex
     ↓
Future work               → sections/05_future_work.tex
```

Ogni strato è concettualmente distinto: il passaggio dal secondo al terzo
separa *ciò che l'oggetto è* (stazione tecnica) da *ciò che diventa nella
città* (destinazione civica di apprendimento).

## Struttura

```
peeragogy-on-music/
├── README.md         ← questo file
├── main.tex          ← documento LaTeX principale
├── references.bib    ← bibliografia (minimale, provvisoria)
├── sections/         ← sezioni .tex separate
│   ├── 01_origin.tex
│   ├── 02_concept.tex
│   ├── 03_learning_point.tex
│   ├── 04_caprotti.tex
│   └── 05_future_work.tex
└── figures/          ← figure (da verificare, non copiate)
    └── README.md     ← catalogo provvisorio delle figure candidate
```

## Compilazione

```bash
pdflatex main.tex
```

Oppure, se `latexmk` è disponibile:

```bash
latexmk -pdf main.tex
```

La compilazione richiede un'installazione TeX Live standard (2020+).
Nessun pacchetto proprietario o font esterno obbligatorio.

## Roadmap editoriale

1. ✅ Scaffold LaTeX minimale (questo)
2. [ ] Revisione con Fabrizio e ChatGPT
3. [ ] Prima bozza completa
4. [ ] Revisione peer
5. [ ] Pubblicazione