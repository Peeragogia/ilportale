# Audit della rifocalizzazione v0.6

Prima lettura 18 ottobre; seconda lettura 19 ottobre 2026. Revisione interna parziale, svolta durante la redazione concorrente dei capitoli. Non è una peer review esterna, una validazione sperimentale o un confronto già eseguito con un altro LLM. L'audit v0.5 era stato interrotto: nessuna dichiarazione di completezza viene trasferita alla v0.6.

## Criterio

La precisazione autoriale pone al centro OLED e camera, presenza quasi speculare del pianista remoto anche a 10.000 km, ambizione di suonare contemporaneamente e modalità studio su piattaforma propria o esterna. Controllare che poesia, scelte tecniche e valutazione descrivano lo stesso progetto. Presenza, esecuzione contemporanea, coordinazione ritmica stretta e alternanza sono condizioni diverse.

## Prima lettura dei capitoli rifocalizzati

| ID | File/passaggio | Esito e conseguenza |
|---|---|---|
| F01 | `02_originality.tex`, precisazione autore | Corretto separare la precisazione del 18 ottobre 2026 dal PDF 2016. La fonte autoriale deve esistere nel corpus consegnato e la chiave `teleconc_terzi2026` deve risolversi. |
| F02 | `02_originality.tex`, 10.000 km | Distinzione adeguata fra apertura geografica, simultaneità e sincronismo stretto; non risultano promesse di latenza nulla nel passaggio letto. Le fonti nuove sugli antecedenti non sono state riverificate da questo revisore: controllo documentale ancora necessario. |
| F03 | `03_design.tex`, immagine quasi speculare | Buona distinzione fra reciprocità percepita e specchiamento letterale; camera dietro un OLED ordinario non assunta come disponibile. Viste volto/mani e controllo dell'orientamento rendono verificabile la promessa visiva. |
| F04 | `03_design.tex`, modo studio | Il modo studio qui descrive soprattutto interazione con un altro pianista. Verificare nell'integrazione che sia altrettanto riconoscibile lo studio autonomo attraverso piattaforma propria/esterna; il collegamento umano non deve diventare prerequisito di tutte le attività. |
| F05 | `06_city.tex`, unità del progetto | La coppia di nodi è coerente con l'incontro remoto. Necessario che budget, responsabilità e prove comprendano anche il secondo terminale o dichiarino esplicitamente chi lo fornisce. Un preventivo del singolo nodo non copre il servizio fra due luoghi. |
| F06 | `06_city.tex`, storia e attività | Nei passaggi letti restano corrette le separazioni inventario/atto, programmazione/svolgimento, parco/Padiglione, partner proposti/acquisiti. Nessuna nuova attribuzione storica indebita identificata. |

## Disallineamenti transitori rilevati nella copia di lavoro

I seguenti punti sono stati segnalati all'integratore mentre i capitoli risultavano ancora in modifica. Non sono conclusioni sulla versione finale. Vanno ricontrollati dopo il congelamento.

| ID | File/passaggio | Rischio | Verifica richiesta |
|---|---|---|---|
| T01 | `04_engineering.tex`, schema con soli servizi opzionali Tutor/AI | Architettura ereditata dalla v0.5: il flusso audio remoto e la camera non costituiscono un percorso esplicito. | Diagramma distinto per audio locale, remoto, ritorno personale e video; non basta rinominare un nodo. |
| T02 | `04_engineering.tex`, «nessun servizio remoto entra nel percorso audio» | Frase corretta soltanto per il percorso locale tasto–suono; falsa se riferita all'intero ascolto del duo. | Precisare il percorso locale e mostrare come entra e viene monitorato il segnale remoto. |
| T03 | `04_engineering.tex`, collegamento tutor e assenza di esecuzione sincrona | Il vecchio perimetro rinunciava all'ambizione richiesta invece di specificarne le condizioni. | Budget distinti one-way/round-trip, audio/video, rete/carico; modalità simultanee condizionate e alternative esplicite. |
| T04 | `05_learning.tex`, pilota locale | L'esperimento a coppie locali non valuta la presenza remota né la piattaforma studio. | Separare fattibilità remota, attività di studio e eventuale confronto pedagogico; non generalizzare esiti locali al duo remoto. |
| T05 | `07_delivery.tex`, scenari economici | Possibile sottocosto: seconda postazione, presidio partner, rete e piattaforma non inclusi. | Elencare esclusioni e scenario minimo a due terminali; nessuna cifra diventa preventivo. |
| T06 | `main.tex`, `01_thesis.tex`, `09_requirements.tex` | Introduzione, abstract e matrice ereditati possono raccontare un progetto diverso dai nuovi capitoli. | Verificare copertura di presenza remota, coordinazione, piattaforma studio e priorità autoriali nelle righe finali. |

## Checklist prima del congelamento

- Nessun valore di latenza locale viene riusato come valore di rete; nessun round-trip chiamato one-way senza misura o ipotesi.
- Le stime fisiche a 10.000 km precisano mezzo, lunghezza effettiva del percorso e natura del limite; nessuna promessa che buffering o AI eliminino la propagazione.
- Le soglie sono obiettivi di progetto o risultati di fonte, con attività e condizioni; nessuna soglia musicale universale inventata.
- L'audio ricevuto non viene ritrasmesso come ritorno al mittente; monitoring, feedback e sincronizzazione audiovisiva sono trattati.
- La piattaforma studio ha funzioni e confini leggibili; uso di una risorsa esterna non equivale a integrazione sviluppata, licenza acquisita o accessibilità verificata.
- La precisazione contemporanea dell'autore non è retrodatata nel concept; l'OLED non è presentato come tecnologia inventata dal progetto.
- Tutte le nuove chiavi bibliografiche, figure e riferimenti interni sono risolti; registro fonti e protocollo concorrente usano il nuovo brief.
- La pubblicazione distingue esperienza civica aperta e campione adulto del pilota; accesso dei minori e ricerca con minori non vengono sovrapposti.
- Budget, calendario, numero di nodi e personale si riferiscono alla stessa configurazione; eventuali fasi locali preliminari sono nominate come tali.

## Seconda lettura sostanziale — 19 ottobre 2026

Letti integralmente i capitoli 01–08 nella copia di lavoro, con attenzione a 04, 05 e 07; `main.tex` e la matrice 09 sono in integrazione da parte del coordinatore. Il controllo riguarda coerenza e tracciabilità interna, non costituisce una riverifica indipendente integrale delle nuove fonti remote né verifica visiva del PDF.

### Disallineamenti risolti nella nuova stesura

T01–T03: architettura a due estremità, ascolto locale/remote separato, mix senza ritorno del segnale remoto, distinzione delle latenze e modalità musicali ora presenti. Il vecchio rifiuto generico dell'esecuzione connessa è stato sostituito con una specificazione condizionata alle prove. T04: la pedagogia tratta duo remoto, mentore e studio autonomo; separa presenza percepita, coordinazione e apprendimento. T05: budget A/B comprende due nodi, sviluppo comune e facilitazione a entrambi i lati. Lo scenario annuale non viene sommato al pilota. F04: studio autonomo e piattaforma sono descritti sostanzialmente in 01/04/05/06/08; la descrizione più circoscritta del modo studio in 03 non esclude più tali funzioni nel documento complessivo.

Controlli numerici eseguiti: PCM stereo 48 kHz/24 bit = 2.304.000 bit/s per direzione; propagazione dell'esempio fibra = circa 49 ms per 10.000 km; 24 appuntamenti × 3 ore × 2 facilitatori = 144 ore. Totali A: 27.840 + 9.480 = 37.320, con 20% = 44.784 euro. B: 45.280 + 26.640 = 71.920, con 20% = 86.304 euro. Triennio B: 125.200, con 20% = 150.240 euro. Calcoli coerenti; sono assunzioni illustrative, non prezzi verificati. Il testo dichiara esclusioni e carattere incompleto del TCO.

### Rilievi verificati da correggere/chiudere

| ID | Priorità | Localizzatore | Problema verificato | Correzione minima | Stato alla lettura |
|---|---|---|---|---|---|
| V01 | Maggiore, coerenza funzionale | 04, Invito/consenso | «Prima dell'accettazione non partono camera o microfono; l'anteprima rimane locale» è incoerente: l'anteprima richiede acquisizione locale. | Distinguere acquisizione locale scelta dall'utente e trasmissione: prima dell'accettazione nessun audio/video è trasmesso. | Segnalato al coordinatore |
| V02 | Maggiore, perimetro della ricerca | 05, primo pilota | La delimitazione ad adulti era scomparsa nella prima copia letta. | Reintrodotti adulti consenzienti, procedure dedicate per minori e distinzione ricerca/accesso civico. | Risolto, rilettura 19 ottobre |
| V03 | Medio, misurazione | 04, scarto audio-video | Delta_AV = V_AB − L_AB richiede un'origine comune delle misure; il testo non esplicita il riferimento fisico condiviso. | Definire un unico evento osservabile in video e audio, oppure calibrare la differenza fra origini prima della sottrazione. | Segnalato al coordinatore |
| V04 | Blocco della consegna editoriale | 04/05 e bibliografia | I record erano assenti al primo controllo. | Ora presenti in `network_engineering.bib` e `remote_learning.bib`, con note fonti separate. Resta aggregazione e compilazione senza chiavi non definite. Non è stata svolta qui una riverifica web indipendente dei record. | Metadati risolti; build da verificare |
| V05 | Medio, riproducibilità futura | 05, disegno del pilota | Numerosità, intervallo del richiamo e soglie di completamento sono rinviati al protocollo esecutivo. Il disegno è leggibile ma non ancora eseguibile senza decisioni aggiuntive. | Mantenere dichiarazione esplicita di protocollo preliminare e includere questi campi nel gate che precede il reclutamento; non presentarlo come preregistrazione completa. | Limite documentale, non falsificazione |

La precisazione autoriale è citata in 02 tramite un record distinto e correttamente qualificata nel testo. Il documento storico non viene usato come prova di brevetto, esecuzione intercontinentale dimostrata o sede nel Padiglione. La metafora dello specchio resta distinta da inversione dell'immagine; non è stata trovata una promessa di latenza nulla. Le fonti storiografiche già controllate mantengono i loro limiti inventario/atto e programma/evento.

## Stato

Protocollo e prompt aggiornati al nuovo brief; nessun concorrente eseguito e nessun punteggio comparativo attribuito. Audit sostanziale 01–08 completato nei limiti qui dichiarati sulla copia di lavoro del 19 ottobre; rilievi V01/V03 da chiudere, V02 risolto, V04 in attesa della build e V05 da recepire nei gate. Il documento integrato, la matrice finale, le nuove fonti bibliografiche e il PDF richiedono i controlli finali dell'integratore. Questo registro non attesta un'approvazione finale.

## Chiusura integrativa del coordinatore — 19 ottobre 2026

V01 risolto: prima dell'accettazione non vengono trasmessi audio/video, anteprima locale attivata su scelta e dichiarata. V02 risolto: prima ricerca con adulti, minori con procedure dedicate; accesso civico distinto dal consenso alla ricerca. V03 risolto: deltaAV definito rispetto allo stesso evento fisico e origine temporale. V04 risolto: nuove bibliografie aggregate, tutte le citazioni risolte. V05 mantenuto come limite esplicito: disegno educativo preliminare, da preregistrare dopo accordi reali, non protocollo già eseguibile o reclutamento avviato.

Main, conclusione e matrice ora descrivono la coppia di Portali e lo studio autonomo. Fonte autoriale conservata in research/AUTHOR_CLARIFICATION_2026-10-18.md. Modalità studio autonomo esplicitata anche nel capitolo spaziale. Costi e calendario aggiornati per due nodi. La presente chiusura è del coordinatore; non viene attribuita al revisore indipendente.
