# Figures — Peeragogy on Music

Catalogo provvisorio delle figure candidate per la pubblicazione.
Nessuna figura è stata ancora copiata o inclusa nel documento LaTeX.
Ogni voce va verificata prima dell'inclusione.

## Figure candidate dal PDF storico

| # | Descrizione | Fonte | Stato |
|---|-------------|-------|:-----:|
| 1 | Original concept drawing — drop-shaped structure with keyboard, screen, audio (Figure 1 in the 2016 PDF) | `Peeragogy_on_Music.pdf`, pagina 3 | Da estrarre e verificare |
| 2 | Lateral view — structural diagram showing the physical layout (Figure 2 in the 2016 PDF) | `Peeragogy_on_Music.pdf`, pagina 4 | Da estrarre e verificare |
| 3 | Structural diagram — component breakdown (Tav:1 references) | `Peeragogy_on_Music.pdf`, pagina 3 | Da ricostruire o estrarre |
| 4 | 3D model — Blender blockout rendering | `workspace/renders/preview_0044_*.png` | Da selezionare la vista migliore |
| 5 | Learning City Point diagram — conceptual diagram of the civic music learning point | Non esiste ancora | Da creare |

## Note

- Le figure nel PDF storico sono scan/disegni tecnici. Potrebbero servire
  ricostruzioni vettoriali per la pubblicazione.
- I renders Blender esistono come PNG 1280×720; potrebbero essere
  ridimensionati o affiancati.
- Directory per le figure: `figures/` (stessa cartella di questo README).
- Inserire solo dopo verifica licenza e attribuzione.

## Comando di inclusione in LaTeX

```latex
\begin{figure}
    \centering
    \includegraphics[width=\textwidth]{figures/01_concept_drawing.png}
    \caption{Caption provvisoria. Fonte: \cite{terzi_peeragogy_2016}.}
    \label{fig:concept-drawing}
\end{figure}
```
