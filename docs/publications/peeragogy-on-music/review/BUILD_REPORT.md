# Verifica editoriale v0.5

18 ottobre 2026. PDF: **34 pagine**, copertina, tre pagine preliminari, trenta pagine numerate. Otto capitoli, appendice, 24 riferimenti citati (26 voci disponibili nel sorgente bibliografico). Due schemi vettoriali, illustrazione originale inalterata.

Comando: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.

Ambiente: TeX Live 2023, pdfTeX, BibTeX, Python3/PyMuPDF per controllo visivo. Log conservati in `review/build/main.log` e `review/build/main.blg`.

Esito finale: zero errori, zero warning LaTeX/BibTeX, zero citazioni irrisolte, zero overfull/underfull box. Controllati riferimenti a file e unicità delle chiavi. Renderizzate e ispezionate tutte le 34 pagine, più dettaglio del diagramma tecnico; corrette etichette, tabelle e code di capitolo quasi vuote. Nessun difetto residuo di sovrapposizione o taglio osservato. Il controllo non è una certificazione di accessibilità del PDF.

PDF SHA-256: `6d9b27a876d50e5026dcc052137b9907512dee47f0df167125037db113c631c4`

```json
{
  "inputs": 9,
  "bibliography_entries": 26,
  "cited_entries": 24,
  "errors": [],
  "pdf_sha256": "6d9b27a876d50e5026dcc052137b9907512dee47f0df167125037db113c631c4"
}
```

Questi sono controlli del documento. TR1–TR6/E1–E6 descrivono prove future sul sistema e non sono stati eseguiti. Nessuna prestazione o efficacia del Portale è stata misurata.
