# Il Portale — Peeragogy on Music

## Stato

Prima bozza italiana completa v0.2, 14 ottobre 2026: cinque sezioni, riassunto e bibliografia. Documento di progetto e programma di ricerca; nessun risultato sperimentale o fattibilità attestata. La review di Pi sulla v0.2 resta da completare.

## Sorgenti

- `main.tex`: metadati, lingua italiana e struttura.
- `sections/01_origin.tex`: fonte originale, cronologia dichiarata e metodo.
- `sections/02_concept.tex`: oggetto storico e scelte tecniche contemporanee.
- `sections/03_learning_point.tex`: apprendimento tra pari, OER e pubblici.
- `sections/04_caprotti.tex`: contesto storico, candidatura e funzione civica.
- `sections/05_future_work.tex`: modello, prototipo e programma di verifica.
- `references.bib`: sei fonti citate, con ID stabili.
- `research/`: registri e risposta alla review, con fonti PUB-Snn distinte dal dossier tecnico.
- `main.pdf`: compilazione della v0.2; ricompilare dopo ogni modifica dei sorgenti.

## Compilazione

Dalla cartella corrente:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Alternativa: `pdflatex main.tex`, `bibtex main`, quindi `pdflatex main.tex` due volte.

Verificato con TeX Live 2023, Babel recente (opzione `provide=*` per italiano), Latin Modern e xurl. Sei pagine, nessuna citazione irrisolta, nessun warning o box fuori margine nel log finale; pagine renderizzate e controllate. La compilazione non valida i contenuti.

## Regole e coordinamento

La fonte originale in `docs/caprotti/source-material/Peeragogy_on_Music.pdf` resta invariata. Separare dati della fonte, interpretazioni e proposte. «Filed» non è prova di deposito legale. Parco Caprotti è nella fonte; Padiglione è candidato contemporaneo.

ChatGPT modifica i sorgenti editoriali; Pi svolge review critica e verifica tecnica riferita a SHA. Correzioni tecniche concorrenti su branch separato. Canale: https://github.com/Peeragogia/ilportale/pull/2

Restano aperti rilievo, tutela specifica, localizzatori archivistici, verifiche delle fonti storiche deboli e disponibilità del luogo. La voce applica il riepilogo di Pi, non una skill completa qui disponibile.
