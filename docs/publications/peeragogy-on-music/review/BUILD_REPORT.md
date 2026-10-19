# Verifica editoriale v0.6 — 19 ottobre 2026

PDF: 36 pagine. Otto capitoli e appendice; 29 riferimenti citati, 39 voci disponibili nella bibliografia canonica. Due schemi vettoriali e immagine originale inalterata.

Comando: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
Ambiente TeX Live 2023/pdfTeX/BibTeX; Python3 e PyMuPDF per rendering e controllo.

Esito finale: zero errori, zero warning LaTeX/BibTeX, zero citazioni irrisolte, zero overfull/underfull box. Controllati tutti i nove input e le chiavi bibliografiche. Ispezionate tutte le pagine renderizzate e i due diagrammi in dettaglio; corretta etichetta del flusso di controllo e rimosse code di capitolo quasi vuote. Nessun taglio o sovrapposizione residua osservati. Questo controllo non certifica l'accessibilità del PDF o la fattibilità del prototipo.

SHA-256 PDF: `58be31f2611dc40b9afe7810abf03a07de623950d48c8c2c022ba03e9fdaf9b0`

```json
{
  "inputs": 9,
  "bibliography_entries": 39,
  "cited_entries": 29,
  "errors": [],
  "pdf_sha256": "58be31f2611dc40b9afe7810abf03a07de623950d48c8c2c022ba03e9fdaf9b0"
}
```

N1–N8 sono futuri collaudi del sistema: non sono stati eseguiti. Nessuna misura di rete del Portale, esperimento educativo o confronto con un concorrente è stato simulato come risultato reale.
