# v0.6 — Fonti dell'architettura della compresenza

Sezione: `sections/04_engineering.tex`. Ricerca iniziale 18 ottobre 2026; tutte le quattro fonti qui incluse riaperte e verificate il 19 ottobre 2026. Nessun collaudo del Portale eseguito. Nessuna prestazione di un sistema altrui viene attribuita al Portale.

## Registro delle fonti primarie effettivamente citate

| Chiave | Fonte primaria | Evidenza utilizzata | Limite |
|---|---|---|---|
| `net_jacktrip` | [Documentazione ufficiale JackTrip](https://jacktrip.github.io/jacktrip/index.html) | Audio bidirezionale multicanale non compresso; disponibilità su più sistemi operativi | Capacità documentate del software, non prova d'integrazione nel Portale. Nessuna garanzia di distanza o latenza |
| `net_jacktrip_latency` | [JackTrip Labs, Optimize Latency in JackTrip](https://support.jacktrip.com/how-to-optimize-latency-when-using-jacktrip) | Compromesso fra buffer, jitter, continuità e latenza; scomposizione della diagnostica e presenza di stime dell'interfaccia | Fonte del produttore, non confronto indipendente. Non adottate le generalizzazioni promozionali, soglie musicali universali o l'invito a disabilitare firewall |
| `net_lola_manual` | [LoLa Installation & User's Manual 2.0.0 rev.001](https://lola.conts.it/downloads/Lola_Manual_2.0.0_rev_001.pdf), Conservatorio Tartini/GARR, 2019, 45 pagine | Introduzione p.3; requisiti audio/video pp.4–6 e rete pp.7–9; sistema audiovisivo per interazione remota, hardware specifico, rete ad alte prestazioni per video non compresso | Edizione identificata, non assunta come versione software più recente. Condizioni della rete accademica non trasferibili automaticamente a un collegamento urbano commerciale. Non qualificato come open source |
| `net_fiber` | [Corning SMF-28 Ultra, PI1424, luglio2025](https://www.corning.com/content/dam/corning/media/worldwide/coc/documents/Fiber/product-information-sheets/PI-1424-AEN.pdf), p.2 | Indice di gruppo effettivo1,4682 a1550nm (e1,4676 a1310nm) | Esempio di fibra convenzionale, non descrizione della rotta del Portale. Distanza geografica, lunghezza fisica della fibra e instradamento sono distinti |

La chiave preesistente `eng_midi` resta usata nella sezione e deve essere conservata nella bibliografia generale. Rimane inoltre `terzi_peeragogy_2016` per pp.2–3 del concept originale.

## Calcoli propri, non risultati sperimentali

- Propagazione: `1.4682 * 10,000,000 m / 299,792,458 m/s = 0.0489739 s`, circa49ms unidirezionali per10000km di quella fibra. Due percorsi analoghi danno circa98ms, arrotondati a100ms. Routing, code, acquisizione, elaborazione, codifica e resa si aggiungono. Non è una misura di rete, né un limite universale per qualunque mezzo trasmissivo.
- Blocco128campioni a48kHz: `128/48000 = 2.6667ms`; non è latenza totale.
- Video60fps: intervallo16,6667ms; non è latenza camera-display.
- PCM stereo48kHz/24bit: payload2,304Mbit/s per direzione, oltre overhead, ridondanza e video. Nessuna promessa di banda effettivamente sufficiente.
- Target locale mediana15ms/p95 20ms: obiettivo progettuale non misurato; non applicato alla tratta geografica e non presentato come soglia percettiva universale.

## Scelte proposte e limiti intenzionali

1. Due estremità full duplex con mixer locale/remoto e nessun ritorno automatico del segnale ricevuto.
2. Audio come riferimento sonoro; MIDI opzionale con timbro e mappature dichiarate. Non si attribuiscono al pianista note previste o generate.
3. Ensemble simultaneo come obiettivo centrale. Alternanza e asincronia sono pratiche esplicite, non prove che l'ensemble sia riuscito. A grande distanza si sperimentano repertorio e ruoli; non si promette identica interazione a quella in presenza.
4. Nessuna soglia universale di latenza accettabile per tutta la musica; relazione fra ritardo, repertorio, tempo e partecipanti da osservare.
5. OLED/camera come ipotesi di presenza quasi speculare: sguardo, scala, orientamento e scarto audiovisivo da misurare. Nessun uso automatico di mirroring o ricostruzione generativa della persona.
6. N1–N8 sono prove da effettuare. Non indicano risultati acquisiti. Misure unidirezionali richiedono sincronizzazione e incertezza dichiarate; ping/2 non sostituisce il percorso musicale.
7. Invito, consenso, cifratura/autenticazione e revoca sono requisiti da implementare e verificare; non vengono attribuiti automaticamente al trasporto JackTrip o LoLa.

## Stato per integrazione e revisione Pi

Sezione completa, circa2175parole secondo conteggio shell del18ottobre. Schema TikZ e tabella N1–N8 inclusi; nessuna parte testuale lasciata con placeholder. Fonti aggiuntive complete (4 chiavi net_); non effettuata compilazione separata del capitolo. Il root integra nella bibliografia generale e verifica layout dell'equazione, schema e tabella.

Controlli prioritari: distinzione locale/one-way/RTT; non equiparare bandwidth e latenza; segnalare esplicitamente degradazione e riconnessione; impedire confusione fra registrazione e presenza dal vivo; preservare il desiderio di simultaneità senza affermare risultati inesistenti. Non è stata modificata alcuna altra sezione né eseguito push da questo agente.
