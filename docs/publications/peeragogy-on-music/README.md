# Il Portale — monografia tecnica v0.5

18 ottobre 2026. **Il Portale: una infrastruttura civica per imparare musica**. Autore e direzione: Fabrizio Terzi. Ricerca/redazione assistita ChatGPT con sei agenti specialistici; integrazione e revisione interna del coordinatore.

## Leggere e revisionare

- [PDF completo](main.pdf)
- [Sorgente principale](main.tex), [capitoli](sections/), [bibliografia canonica](references.bib)
- [Protocollo di valutazione: 100 punti](review/REVIEW_PROTOCOL.md)
- [Prompt per concorrente e revisore](review/COMPETITOR_PROMPT.md)
- [Revisione interna e correzioni](review/INTERNAL_REVIEW_V05.md)
- [Registri fonti e claim](research/)

Otto capitoli: tesi e origine; originalità e precedenti; forma/accessibilità/acustica; architettura MIDI/audio/software/AI; pedagogia e valutazione; città e sito; governance/costi/percorso; sintesi. Appendice con 12 requisiti trasversali, collegata ai 6 requisiti tecnici e 6 collaudi. Due schemi vettoriali e illustrazione originale inalterata.

Questa edizione sostituisce il taglio introduttivo della v0.4 con una proposta di sistema completa a livello di ricerca e pre-fattibilità. Non è un progetto esecutivo: non sono disponibili rilievo, collaudi hardware, autorizzazioni, accordi, preventivi definitivi o dati di partecipanti. Specifiche e soglie sono proposte, costi scenari interni parziali. L'originalità è argomentata tramite confronti mirati, senza primati inventati.

## Compilazione e controllo

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
python3 tools/check_publication.py
```

Richiede TeX Live, Latin Modern, Babel, natbib, TikZ, enumitem, titlesec, fancyhdr, tabularx, longtable e xurl. La verifica locale e gli hash sono in `review/BUILD_REPORT.md` e `review/DELIVERY_MANIFEST.sha256`. Nessuna prova sul dispositivo fisico è simulata dalla compilazione.

## Lavoro comune

Si lavora direttamente su **master**, ramo principale del repository, per istruzione di Fabrizio. Sincronizzare la head prima di modificare; non forzare gli aggiornamenti. Discussione con Pi: https://github.com/Peeragogia/ilportale/pull/2 . La review di Pi della v0.3 resta conservata; la v0.5 richiede una revisione nuova.

Le vecchie sezioni non più incluse sono conservate nella storia Git; la v0.4 completa è al commit `de9f82fb30971d95dfacb454abad97a18043971a`. Le note di ricerca pregresse conservano il loro statuto datato e non costituiscono automaticamente lo stato editoriale corrente.

## Confronto LLM

Protocollo, scheda di score e prompt sono pronti. Nessun concorrente è stato eseguito e nessun vincitore dichiarato. Per confronto cieco controllato congelare corpus e risorse prima di avviare entrambi; per confrontare questa edizione con un nuovo elaborato in condizioni diverse usare l'etichetta «confronto esplorativo». Pi può valutare ora questa monografia secondo la stessa rubrica, indicando evidenze e limiti.
