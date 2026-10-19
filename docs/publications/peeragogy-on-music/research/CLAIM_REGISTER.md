# Claim Register — pubblicazione

Questo file serve a impedire che un'idea plausibile diventi, per ripetizione, un “fatto”.

| Claim | Stato | Evidenza | Azione |
|---|---|---|---|
| Il Portale è documentato come progetto 2013 in un PDF datato 2016 con intestazione FTG | SUPPORTATO | PUB-S01 | conservare formulazione prudente sul significato di “Filed” |
| Il progetto originale indica Parco Caprotti, via Tasso | SUPPORTATO | PUB-S01 | claim centrale |
| Il Padiglione del Tè era già indicato nel progetto 2013 | NON DOCUMENTATO NELLA FONTE | PUB-S01 | non dirlo: è scelta contemporanea |
| Il Parco fu realizzato nell'Ottocento dalla famiglia Caprotti | SUPPORTATO | PUB-S03 | cercare fonte archivistica più precisa |
| Carlo Caprotti progettò personalmente il giardino | DA VERIFICARE | PUB-S07 + fonte familiare | cercare archivio |
| Il Padiglione è del 1890 | CONFLITTO | PUB-S06 vs PUB-S07 | usare c. 1890–1891 |
| Il Padiglione è neorinascimentale e vetrato | SUPPORTATO contemporaneamente | PUB-S05 | cercare scheda storica/architettonica primaria |
| Il Giardino Caprotti è soggetto a vincolo ambientale dal 1949 | SUPPORTATO | PUB-S02 | distinguere vincolo giardino da tutela edificio |
| Il Parco fu donato al Comune nel 1947 | NON ANCORA SUPPORTATO | PUB-S08 | PUB-S08 prova solo manifestazione di volontà |
| Il Padiglione è stato usato nel 2023 per arte e attività pubbliche | SUPPORTATO | PUB-S05 | utile come precedente di riuso |
| Nel 2026 è stata annunciata una jam session giovanile a Parco Caprotti | SUPPORTATO COME ANNUNCIO | PUB-S12 | non assumere che il programma provi lo svolgimento |
| Il Portale migliora l'apprendimento musicale | NON DIMOSTRATO | nessuna | vietato come claim |
| L'apprendimento musicale informale può sostenere motivazione, autonomia e collaborazione | SUPPORTATO in letteratura | PUB-S18 | non generalizzare oltre gli studi |
| Un Learning City Point è una categoria riconosciuta UNESCO | FALSO | — | è un nostro termine; UNESCO supporta la cornice learning city, non il nome |
| Gli spazi pubblici e culturali possono ospitare apprendimento non formale urbano | SUPPORTATO | PUB-S14–PUB-S15 | usare come cornice, non come validazione del progetto |
| Il Portale è coerente con alcune direttrici del PGT 2023 di Bergamo | DA VERIFICARE | PUB-S10–PUB-S11 | reperire PUB-S11; nessuna approvazione istituzionale implicata |
| Il Padiglione è tecnicamente adatto all'installazione | NON DIMOSTRATO | — | servono rilievo, impianti, acustica, accessibilità e tutela |
| Il progetto può diventare attrazione culturale | IPOTESI | contesto PUB-S05/PUB-S10/PUB-S13 | da testare con pubblico e stakeholder |
| Il PDF prova un deposito legale o una pubblicazione sottoposta a peer review | NON DIMOSTRATO | PUB-S01 | «Filed» e intestazione editoriale sono metadati interni; non bastano come prova esterna |
| Il questionario coinvolse Orto Botanico e Università di Bergamo con ruoli distinti | SUPPORTATO DA FONTE SECONDARIA | PUB-S06, sezione sul questionario | non attribuire a entrambi la preparazione né datarla al 2024 senza prova |
| Il modello Blender valida acustica e accessibilità | NON DIMOSTRATO | nessuna misura calibrata presentata | distinguere modello proporzionale, rilievo e verifiche specialistiche |

| Il Cerchio di Gesso pubblica attività del Giardino dell’anima e un evento 2026 alla Sala del té | SUPPORTATO COME PROGRAMMA | PUB-S19 | verificare disponibilità e usi attuali con i responsabili; nessuna collaborazione col Portale già concordata |

## Claim decisivi aggiunti nella v0.5

| ID | Affermazione | Stato | Evidenza o verifica necessaria |
|---|---|---|---|
| V05-C01 | Il contributo è l'integrazione di gesto, forma, scambio e continuità civica | TESI PROGETTUALE | Cap.1–2; confronto mirato, nessun primato universale |
| V05-C02 | Pianoforti pubblici e Reactable precedono il concept | DOCUMENTATO | conc_streetpianos, conc_reactable, conc_jorda2007 |
| V05-C03 | La forma a goccia facilita accesso e reciprocità | IPOTESI | Prototipo volumetrico, utenti e confronto orientamenti |
| V05-C04 | Catena audio indipendente da cloud e UI | REQUISITO PROPOSTO | TR1/E1, TR3/E3; non implementazione attestata |
| V05-C05 | Mediana15ms/p95 20ms/scarto5ms | OBIETTIVO PROPOSTO | TR2/E2, misura fisica end-to-end; nessun dato acquisito |
| V05-C06 | Blocco128 campioni a48kHz dura2,67ms | CALCOLO | 128/48000×1000; non latenza totale |
| V05-C07 | Log7giorni, timeoutAI8s, inattività120+30s | PARAMETRI CANDIDATI | Collaudo e governance prima dell'uso |
| V05-C08 | Studi musicali dimostrano efficacia del Portale | NON DIMOSTRATO | Review non valida componente digitale; nessun pilota svolto |
| V05-C09 | Suonare insieme causa coesione urbana | NON DIMOSTRATO | Studi contestuali discordanti; no generalizzazione |
| V05-C10 | Pilota36adulti/18coppie è sufficiente per efficacia | NON DIMOSTRATO | Campione operativo di fattibilità, nessun power analysis |
| V05-C11 | ScenariA/B/C costano18432/42912/90360euro | STIME INTERNE PARZIALI | Aritmetica esplicita, assunzioni e voci escluse; non preventivi |
| V05-C12 | ProgrammaCerchioGesso conferma spazio disponibile | NON DIMOSTRATO | PUB-S19 documenta programma; accordi da ottenere |
| V05-C13 | WCAG certifica accessibilità dell'intera installazione | FALSO | des_wcag22 riguarda interfaccia digitale; rilievo/prove fisiche necessari |
| V05-C14 | Un LLM concorrente è stato superato | NON VALUTATO | Nessun output concorrente o score disponibile; protocollo predisposto |

## Versione corrente v0.6 — la coppia di Portali

Il registro V05 sopra è storico: requisiti TR/E, campione36/18 e budget a nodo singolo non sono le specifiche correnti. La v0.6 usa prove N1–N8, requisiti R01–R14, disegno pilota preliminare a due nodi e budget di coppia. Il funzionamento locale resta un requisito, ma non esaurisce la funzione centrale.

| ID | Claim | Stato | Evidenza / prova |
|---|---|---|---|
| V06-C01 | L'autore intende una presenza quasi speculare fra pianisti lontani e uno spazio di studio | DOCUMENTATO COME INTENZIONE | teleconc_terzi2026, trascrizione18ott |
| V06-C02 | Il concept2016 contiene webcam e ritorno video a distanza | DOCUMENTATO | PUB-S01 p2; non dimostra prestazioni |
| V06-C03 | Il Portale funziona in duo sincronizzato a10000km | NON DIMOSTRATO | Ambizione, non test; N2–N5 richieste |
| V06-C04 | 10000km di fibra conng1,4682 implicano circa49ms per senso di sola propagazione | CALCOLO CONDIZIONALE | net_fiber, lunghezza e mezzo dichiarati; percorso reale ignoto |
| V06-C05 | Una latenza locale di20ms garantisce coordinazione remota | FALSO | Catene e misure distinte |
| V06-C06 | OLED consente automaticamente camera dietro il pannello e sguardo coincidente | NON DIMOSTRATO | Scelta ottica e geometria da provare |
| V06-C07 | L'inversione automatica dell'immagine è necessaria al quasi specchio | NON ASSUNTO | Postura frontale e reciprocità; orientamento mani preservato |
| V06-C08 | Studio autonomo richiede sempre partner o account | FALSO PER IL REQUISITO | Catalogo locale e primo gesto senza account; progressi facoltativi |
| V06-C09 | I costi di coppia sono44784euro pilota e86304euro anno | STIME INTERNE PARZIALI | Ipotesi aritmetiche cap7, esclusioni esplicite, non preventivi |
| V06-C10 | Presenza percepita prova apprendimento duraturo | NON DIMOSTRATO | Misure separate, prova individuale e richiamo |
| V06-C11 | Il prototipo/piattaforma del Portale esiste già | NON ATTESTATO | Proposta di sviluppo, no hardware o software musicale implementato in questa redazione |
| V06-C12 | Si può riprendere automaticamente la camera dopo una caduta rete | CONTRARIO AL REQUISITO | Nuova conferma, anteprima locale distinta, provaN6 |
