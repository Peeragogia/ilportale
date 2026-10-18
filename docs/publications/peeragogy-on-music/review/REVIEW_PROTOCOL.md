# Il Portale — protocollo di revisione e confronto indipendente

Versione 1.0, 18 ottobre 2026. Documento di valutazione, non risultato di una valutazione. Nessun punteggio è stato attribuito alla pubblicazione o a un concorrente.

## Oggetto e unità del confronto

Valutare se una pubblicazione rende Il Portale comprensibile, distintivo, tecnicamente discutibile e concretamente sperimentabile nella città, conservandone la forza umana. La lunghezza, il numero di riferimenti, il prestigio del modello e la prosa assertiva non costituiscono evidenza di qualità.

Tenere separati due esercizi:

1. **Revisione dello stesso testo.** Due revisori ricevono l'identica pubblicazione e devono trovare difetti, verificarli, graduarli e proporre correzioni. Il risultato misura la qualità della revisione, non la superiorità delle pubblicazioni.
2. **Redazione indipendente.** Due sistemi ricevono l'identico brief, corpus congelato, vincoli e budget. Producono due pubblicazioni nuove. Soltanto questi elaborati si confrontano con la rubrica su 100 punti sotto riportata.

La v0.5 già prodotta può essere valutata in termini assoluti. Confrontarla con un testo scritto in condizioni differenti è un confronto esplorativo fra elaborati, non un esperimento controllato sulla capacità dei modelli. Non ricostruire retroattivamente un budget fittizio per rendere simmetrico il lavoro già svolto.

## Congelamento e condizioni comparabili

Prima dell'esecuzione, un coordinatore umano compila il registro seguente e congela un commit del corpus. Il corpus della redazione include la fonte originale, il dossier storico, i registri delle fonti e le eventuali verifiche già concluse. Esclude la nuova prosa v0.5 e i suoi schemi originali, per evitare che uno dei concorrenti riscriva il risultato dell'altro. Se la v0.4 viene fornita, deve esserlo a entrambi e dichiarata materiale di partenza.

| Campo | Valore da compilare prima dell'esecuzione |
|---|---|
| Tipo | Revisione / redazione indipendente / confronto esplorativo |
| Repository e commit corpus | — |
| Manifest dei file e SHA-256 | — |
| Brief identico e suo SHA-256 | — |
| Inclusione v0.4 | Sì / no, motivazione |
| Fonti escluse o irraggiungibili | — |
| Data limite delle fonti | — |
| Ricerca web | Vietata / consentita a entrambi |
| Tempo massimo di lavoro e ricerca | — |
| Budget strumenti e chiamate | — |
| Budget testo finale | — parole, ±10%; bibliografia esclusa |
| Budget di calcolo dichiarabile | Configurazione, modalità ragionamento, limiti; ignoto se non esposto |
| Delegazione | Numero massimo agenti e totale risorse, uguali per entrambi |
| Strumenti di compilazione | Versioni e dipendenze identiche |
| Prompt correttivi | Nessuno / numero e regola identici |
| Modello/versione/data di esecuzione | Registro riservato al coordinatore durante la valutazione |

Se il confronto è chiuso, non è ammessa ricerca esterna. Se è aperto, conservare un registro di query, URL, accessi e tempi per entrambi; l'uguaglianza del budget non garantisce identiche fonti reperite. Inaccessibilità e tool failure vanno riportati, senza penalizzare un sistema per condizioni che l'altro non ha incontrato. Dichiarare gli scostamenti e ripetere il confronto se essenziali. Un confronto fra sistemi a squadre non isola il modello base: rende conto dell'intero processo di lavoro.

## Cecità e giudizio

Il coordinatore assegna casualmente i codici A/B, rimuove soltanto indizi sul sistema autore dai metadati e conserva i contenuti e l'attribuzione storica del progetto. Non rimuove limiti, fonti o dichiarazioni di incertezza. La dichiarazione di assistenza AI può essere sostituita per entrambi con lo stesso testo neutro, mantenendo gli originali nel registro riservato. Alternare l'ordine A/B fra revisori.

Almeno due persone valutano indipendentemente prima del confronto: una competente in progetto tecnico/ricerca e una competente in educazione/città. Dichiarano rapporti con autore e progetto. Pi e altri modelli possono produrre audit supplementari; non sono l'unico giudice e non si considerano automaticamente indipendenti. Se non sono disponibili revisori umani, chiamare il risultato **audit modellistico preliminare**, senza dichiarare un vincitore affidabile.

Ogni punteggio richiede un localizzatore nel testo e una breve motivazione. Per discrepanze maggiori di un livello su un criterio, i revisori discutono le evidenze; conservano comunque i punteggi iniziali. La media descrittiva e l'intervallo fra giudizi devono restare visibili. Non inventare intervalli di confidenza o significatività statistica su due giudizi.

## Rubrica della pubblicazione — 100 punti

Assegnare a ogni criterio un livello intero 0–4. Punti = peso × livello / 4. I mezzi punti nel totale sono possibili; la precisione numerica non esprime precisione scientifica. Ogni criterio contiene due o più aspetti: assegnare il livello sostenuto dalle evidenze complessive e indicare eventuali lacune, senza premiare una sola dimostrazione brillante come copertura dell'intera dimensione.

| Criterio | Peso | Evidenza richiesta per il livello 4 |
|---|---:|---|
| Concezione e bellezza progettuale | 12 | Tesi riconoscibile; relazione necessaria fra forma, corpo, musica, apprendimento e spazio civico; scelte e rinunce argomentate; scene d'uso che chiariscono il sistema, senza sostituire la dimostrazione. |
| Originalità e confronto | 10 | Comparazione corretta con precedenti pertinenti; contributo distintivo circoscritto, differenze verificabili e limiti; nessun primato senza prova; alternative che potrebbero raggiungere gli stessi obiettivi considerate seriamente. |
| Ricerca e onestà delle fonti | 16 | Affermazioni rintracciabili a fonti appropriate e localizzate; ricostruzione storica distinta dalla proposta; conflitti conservati; fonti primarie impiegate quando disponibili; citazioni effettivamente a sostegno del claim. |
| Architettura e verifica tecnica | 18 | Flussi, componenti, interfacce e stati coerenti; requisiti misurabili con metodo di accettazione; budget di latenza ragionato; guasti e recupero; manutenzione; separazione esplicita fra realizzato, proposto, stimato e da misurare. |
| Pedagogia e disegno di ricerca | 14 | Meccanismi di apprendimento tra pari osservabili; attività e facilitazione progettate; esiti musicali distinti da gradimento/attrazione; prova senza assistenza e, quando pertinente, differita; limiti causali e fattibilità della raccolta. |
| Città, luogo e accessibilità | 12 | Rapporto specifico con Parco Caprotti e usi documentati; alternative di collocazione; convivenza con non utenti; accessibilità fisica, sensoriale, cognitiva e sociale; interlocutori proposti distinti da partnership confermate. |
| Fattibilità, cura e responsabilità | 10 | Fasi e criteri di arresto; responsabilità e presidio; costo totale con ipotesi leggibili; sicurezza, dati e contenuti proporzionati; decisioni che richiedono rilievo o professionisti identificate senza simulare autorizzazioni. |
| Qualità editoriale e riproducibilità | 8 | Italiano preciso e vivo; progressione narrativa; diagrammi e tabelle utili, coerenti col testo; bibliografia leggibile; LaTeX/PDF verificabili; figure con provenienza; niente ridondanza usata per simulare profondità. |
| **Totale** | **100** | |

Ancore comuni:

- **0 — assente o contraddetto:** la dimensione manca o contiene errori che ne invalidano il trattamento.
- **1 — nominale:** promessa o elenco generico; dettagli insufficienti per controllare le affermazioni o discutere le scelte.
- **2 — parziale:** trattamento sostanziale, ma lacune importanti nelle evidenze, nella coerenza o nell'operatività.
- **3 — solido:** quasi tutte le evidenze richieste sono presenti e coerenti; limiti residui espliciti e non decisivi.
- **4 — eccellente:** tutte le evidenze richieste sono presenti con precisione e integrazione; un revisore può ricostruire il ragionamento e mettere alla prova le scelte. Non richiede che il progetto sia già costruito.

Un progetto non ancora realizzato può ricevere un voto alto se è una proposta rigorosa. Deve invece ricevere un voto basso se presenta come risultati le proprie intenzioni. La quantità di cautela non dà punti in sé: i limiti devono rendere la decisione più chiara.

## Errori bloccanti e gate separato dal voto

I seguenti errori sospendono il giudizio di pubblicabilità. Il punteggio diagnostico può essere compilato, ma non può autorizzare una dichiarazione di superiorità o di prontezza finché l'errore resta aperto:

- fonte, citazione, misura, esperimento o risultato inventato;
- attribuzione falsa di partner, autorizzazione, proprietà, deposito legale o validazione;
- conflitto fra requisito e architettura che rende impossibile la funzione centrale e viene occultato;
- indicazione operativa materialmente pericolosa presentata come verificata, oppure conformità normativa dichiarata senza base;
- riuso di immagini o contenuti con provenienza falsa, oppure assenza di elementi indispensabili a ricostruirla;
- PDF mancante/corrotto o materiali necessari alla revisione non consegnati.

Ogni blocco richiede localizzatore, evidenza e correzione minima. Un dubbio non verificato è un **rilievo da indagare**, non automaticamente un blocco. Un'ipotesi dichiarata come tale, una misura ancora da rilevare o l'assenza di autorizzazione in fase di proposta non sono di per sé errori bloccanti. Citazioni non definite e riferimenti interni rotti bloccano la consegna editoriale finché corretti, senza equipararli a falsificazione scientifica.

## Audit delle citazioni e dei numeri

Verificare tutte le affermazioni decisive: origine e date del concept; localizzazione storica; documenti d'archivio; usi del luogo; precedenti; principali risultati educativi; valori numerici da cui dipendono decisioni. Per il resto, estrarre un campione dichiarato e riproducibile, uguale per ampiezza nei due testi. Controllare anche almeno un claim *senza* citazione per sezione: il semplice numero di citazioni non misura la tracciabilità.

Per ogni numero: specificare se misura, dato di fonte, obiettivo progettuale, stima di scenario o soglia decisionale proposta; controllare unità, calcolo e ipotesi. Per ogni fonte: verificare esistenza, versione/data, passaggio richiamato e rapporto effettivo con il claim. Annotare le fonti non accessibili come non verificate. Non trasformare mancato accesso in falsità.

## Scheda compilabile del revisore

**Codice elaborato:** —  
**Commit e SHA-256 PDF:** —  
**Revisore / competenze / conflitti:** —  
**Data, tempo impiegato e strumenti:** —  
**Parti lette / fonti verificate / limiti dell'audit:** —

| Criterio | Peso | Livello 0–4 | Punti | Localizzatore ed evidenza | Lacuna decisiva |
|---|---:|---:|---:|---|---|
| Concezione | 12 | — | — | — | — |
| Originalità | 10 | — | — | — | — |
| Ricerca | 16 | — | — | — | — |
| Tecnica | 18 | — | — | — | — |
| Pedagogia | 14 | — | — | — | — |
| Città | 12 | — | — | — | — |
| Fattibilità | 10 | — | — | — | — |
| Editoria | 8 | — | — | — | — |
| **Totale** | **100** | | **—** | | |

| ID rilievo | Gravità | Localizzatore | Affermazione contestata | Evidenza / verifica | Correzione minima | Stato |
|---|---|---|---|---|---|---|
| R-01 | Bloccante / maggiore / minore / da indagare | — | — | — | — | Aperto |

**Gate:** pubblicabile / pubblicabile dopo correzioni / revisione sostanziale / non valutabile.  
**Tre contributi migliori:** —  
**Tre debolezze decisive:** —  
**Una scelta da abbandonare o riesaminare:** —  
**Che cosa servirebbe per cambiare il giudizio:** —

## Come confrontare due revisioni dello stesso testo

Per l'esercizio 1 non usare il voto di pubblicazione per valutare il revisore. Un arbitro umano verifica i rilievi e costruisce un registro di riferimento dopo la lettura indipendente. Valutare: correttezza dei rilievi (30), copertura dei problemi rilevanti (25), graduazione della gravità (15), localizzazione/evidenza (15), utilità delle correzioni (15). Applicare gli stessi livelli 0–4 e riportare separatamente falsi positivi e rilievi importanti mancati. La copertura si riferisce soltanto ai problemi del registro verificato, non a una pretesa conoscenza di tutti i difetti. Non premiare chi produce più accuse.

## Rapporto di confronto

Pubblicare entrambi i testi, schede individuali, registro dei rilievi, condizioni effettive e risposta degli autori. Mostrare prima i profili per criterio, poi il totale; distinguere miglior concezione, miglior dettaglio tecnico e miglior solidità delle fonti se non coincidono. Un totale maggiore con gate bloccato non equivale a un risultato migliore pronto per la pubblicazione. Se i revisori divergono o i budget non sono comparabili, dichiarare il confronto inconclusivo o esplorativo. Non generalizzare da un singolo progetto alla superiorità universale di un LLM.
