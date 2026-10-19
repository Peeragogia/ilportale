# Il Portale — Abitare la distanza attraverso la musica

**Monografia v0.6, 19 ottobre 2026.** 36 pagine: due pianisti, due luoghi, un incontro; forma poetica e apprendimento aumentato.

## Leggere

- [PDF completo](main.pdf)
- [Sorgente LaTeX](main.tex), [capitoli](sections/), [bibliografia](references.bib)
- [Precisazione autoriale che guida la riscrittura](research/AUTHOR_CLARIFICATION_2026-10-18.md)
- [Audit della rifocalizzazione](review/REFOCUS_AUDIT.md)
- [Protocollo 100 punti](review/REVIEW_PROTOCOL.md) e [prompt concorrente](review/COMPETITOR_PROMPT.md)
- [Consegna a Pi](review/PI_HANDOFF.md) e [verifica editoriale](review/BUILD_REPORT.md)

## Che cosa cambia

Riscrittura integrale degli otto capitoli: l'OLED e la camera collegano due pianisti in una presenza quasi speculare. Incontro musicale, apprendimento accompagnato e studio autonomo su piattaforma propria o risorse esterne sono funzioni centrali. Forma, audio bidirezionale, video, latenza, pedagogia, vita urbana, governance e costi ora si riferiscono a questa relazione e a due postazioni.

Sono distinti contemporaneità, coordinazione ritmica, presenza percepita e apprendimento. Le distanze intercontinentali restano un'ambizione da caratterizzare: nessuna prestazione a10000km è dichiarata realizzata. Nessun partner o sito disponibile è inventato. Proposta di ricerca e pre-fattibilità, non progetto esecutivo né prototipo costruito.

## Verifica e lavoro comune

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
python3 tools/check_publication.py
```

TeX Live 2023, Latin Modern, Babel, natbib, TikZ, enumitem, titlesec, fancyhdr, tabularx, longtable, xurl. Log, conteggi e hash in review/BUILD_REPORT.md e review/DELIVERY_MANIFEST.sha256. Le prove N1–N8 sono future prove del sistema; non sono eseguite dalla compilazione.

Si lavora direttamente su **master** per istruzione di Fabrizio. Prima delle modifiche sincronizzare la head e coordinare ownership nella [discussione con Pi](https://github.com/Peeragogia/ilportale/pull/2). La v0.5 è conservata al commit 70ba08febb60d9a1e814ca4dec32813960590540. Review e note precedenti restano datate: non attestano la validazione di questa riscrittura.

Sei agenti hanno contribuito; dopo l'interruzione del 18 ottobre per limiti di utilizzo, il 19 ottobre sono state completate bibliografie e revisione. Il coordinatore ha integrato e verificato il documento. Nessun concorrente è stato eseguito e nessun voto comparativo è inventato. Pi può valutare lo stesso commit con rubrica aggiornata e segnalare evidenze, limiti e correzioni.
