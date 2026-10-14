# Il Portale — Peeragogy on Music

## Versione attuale

Bozza italiana v0.3, 14 ottobre 2026. Riscrittura narrativa e progettuale: esperienza musicale, identità dell'oggetto, apprendimento condiviso e rapporto con Parco Caprotti. Fonti e limiti sono conservati, con le note metodologiche concentrate nella sezione finale. Scene d'uso e prima persona esprimono proposte, non risultati osservati.

Sette pagine. Sorgenti: main.tex, sections/*.tex e references.bib. PDF aggiornato: main.pdf.

## Lavoro sul ramo principale

Per istruzione di Fabrizio si lavora direttamente sul default branch **master** (in questa repository main non esiste). Pubblicazione e dossier di supporto sono stati portati qui dal branch di ricerca. Il confronto storico resta nella PR #2: https://github.com/Peeragogia/ilportale/pull/2

ChatGPT cura la scrittura; Pi verifica fonti, contenuti e compilazione. Prima di modificare gli stessi file ci si coordina nella discussione. Sincronizzare sempre l'ultima head e non forzare gli aggiornamenti. Non richiedere branch separati per routine editoriale già autorizzata.

## Compilazione

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

TeX Live 2023, Babel recente, Latin Modern, xurl. In alternativa pdflatex, bibtex, pdflatex due volte. Verifica locale v0.3: sette pagine, nessun warning, nessuna citazione irrisolta, nessun overfull/underfull box; controllo visivo delle pagine renderizzate.

## Principi editoriali

Prima il desiderio, l'oggetto e l'esperienza; la verifica deve renderli discutibili e realizzabili. Non cancellare voce e intenzione dell'autore per accumulare cautele. Non inventare biografia, risultati, partner, primati o approvazioni. Parco Caprotti compare nella fonte; Padiglione è candidato contemporaneo. La fonte originale resta invariata. I registri PUB-Snn sono distinti dagli ID del dossier tecnico.

La v0.2 è conservata nella storia git; la review specifica della v0.3 da parte di Pi resta da svolgere.
