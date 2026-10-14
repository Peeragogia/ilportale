# Review editoriale v0.3

SHA: `8356449` — `publication: restore human and design voice in Italian v0.3 on primary branch`
Autore: Fabrizio Terzi (14 ott 2026)
Compilazione: 7 pagine · 0 errori · 0 warning · 0 citazioni undefined · 0 overfull/underfull
6 riferimenti risolti [1]–[6]; 2 warning `empty year` (UNESCO Learning Cities, Visit Bergamo — @misc senza anno, non bloccante)

## Criteri editoriali (da README PUB)

> Prima il desiderio, l'oggetto e l'esperienza; la verifica deve renderli discutibili e realizzabili.
> Non cancellare voce e intenzione dell'autore per accumulare cautele.

## Desiderio   ✅

La v0.3 apre con una scena viva: una persona attraversa il parco, vede una tastiera, si ferma. Il "perché" progettuale è immediato. L'oggetto è al centro del racconto, non la sua descrizione cautelativa. Rispetto alla v0.2 il cambiamento è radicale e va nella direzione chiesta da Fabrizio: l'esperienza precede la verifica.

## Chiarezza   ✅

I ruoli sono distinti in tutto il testo:
- **Fonte 2013–2016** = PDF originale, citato con pagine, mai riscritto
- **Proposta attuale** = in prima persona ("immagino", "propongo", "vorrei"), esplicita come scelta contemporanea
- **Padiglione del Tè** = candidato, non certa collocazione
- **Learning City Point** = termine del progetto, non categoria UNESCO
- **Peeragogy** = non parola galleggiante ma comportamento: "una persona diventa risorsa per un'altra"
- **Contemporary Locus / UBG / Orto** = precedente, non endorsement del progetto

Linguaggio piano, assenza di gergo. Le scene d'uso sono riconoscibili (due partecipanti che si scambiano il posto, cuffia/diffusione sonora, AI come supporto opzionale).

## Sostanza   ✅/⚠

### Punti forti
- **Struttura narrativa**: 5 sezioni = 5 strati dell'arco (desiderio → oggetto → apprendimento → luogo → verifica). Coerente e completa.
- **Tecnologia presente ma non dominante**: webcam disattivata all'avvio, Dolby non prescritto, AI opzionale, "il progetto musicale deve restare praticabile anche senza quel supporto". Ottimo.
- **Peeragogy calata nel comportamento** (§03): la scena dei due partecipanti non nomina mai la parola ma la realizza. La sezione educativa è la più matura del documento.
- **§05 trasparente**: Blender non verifica acustica/comfort, disegno di ricerca serve, "l'entusiasmo di una visita e una capacità acquisita sono esiti diversi, entrambi interessanti se distinti". Eccellente.
- **Nota sulle fonti finale**: Filed non = deposito, nessun risultato sperimentale, ricerca sul Padiglione aperta, ChatGPT dichiarato. Tutti i punti che la v0.2 trattava come cautele distribuite sono concentrati in un unico blocco onesto.

### Punti da segnalare

| # | Tipo | Dove | Cosa |
|---|------|------|------|
| 1 | **Errore** | §02 — "Anche la trasformazione" (x2) | "Anche" è refuso: in italiano è "anche". Due occorrenze (righe 7 e 35 di `02_concept.tex`). |
| 2 | **Minore** | §02 — "attrattività" | Neologismo comprensibile ma poco elegante. Sostituibile con "capacità di attrarre" o "interesse". Non bloccante. |
| 3 | **Precisazione** | §03 — "28 studi empirici" | Corretto, ma una nota "online 2024" aggiornerebbe chi cerca la fonte. Non bloccante. |
| 4 | **Accorgimento** | §05 — "misura, fotografia, stima o ipotesi" | Bella frase. Si può notare che nel modello Blender esiste già la convenzione `_PROXY`/`_EST` per gli elementi non misurati — utile da citare per coerenza dossiermodello. |

### Citazioni di pagina verificate vs PDF originale

| Testo | Pagina citata | PDF reale | Esito |
|-------|---------------|-----------|-------|
| §01 "struttura a goccia, tastiera, immagini, suoni" | pp. 2–3 | pp. 2–3 = oggetto, abstract, scheda | ✅ |
| §01 "Parco comunale dei Caprotti, via Tasso" | pp. 2 e 5 | p. 2 (abstract "Bergamo"), p. 5 (Status/Location) | ✅ |
| §02 "struttura a goccia" | pp. 2–4 | pp. 2–4 descrizione strutturale | ✅ |
| §02 "MIDI, pedali, webcam, Dolby" | pp. 2–3 | pp. 2–3 specifiche tecniche | ✅ |
| §03 "Learning City Point" | pp. 2 e 5 | p. 2 Project Abstract, p. 5 firma | ✅ |

Tutte corrispondono.

## Voto

**Approvata.** La v0.3 restituisce la voce all'autore, mantiene la distinzione fatti/proposta, e colloca la verifica nel suo ruolo di servizio. Il refuso "Anche" e gli appunti minimi non richiedono una nuova iterazione di scrittura: possono essere corretti nel prossimo incremento o assorbiti da Pi direttamente.

La v0.3 è quindi lo stato corrente su `master` — il ramo su cui Fabrizio ha chiesto di lavorare direttamente. Il coordinamento con ChatGPT prosegue sul ramo principale; la PR #2 è superata come canale editoriale.

*Reviewer: Pi — 14 ottobre 2026*