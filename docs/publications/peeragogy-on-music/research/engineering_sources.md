# Architettura tecnica — provenienza e stato delle affermazioni

Data consultazione: 18 ottobre 2026. Autore della sezione: assistenza editoriale GPT; responsabilità autoriale e revisione finale al curatore. Nessun benchmark o dispositivo è stato realizzato durante questa redazione.

## Fonti primarie lette

| Chiave BibTeX | Fonte e URL | Contenuto effettivamente verificato | Limite |
|---|---|---|---|
| eng_midi | MIDI Association, https://midi.org/summary-of-midi-1-0-messages | Note On/Off, Channel Mode, All Sound Off e All Notes Off | Riepilogo, non specifica completa. Conformità reale richiede specifica e prove |
| eng_webmidi | W3C, https://www.w3.org/TR/webmidi/ | SecureContext, permesso MIDI, System Exclusive separato, fallimento richiesta | Non certifica supporto di un browser/dispositivo concreto |
| eng_webaudio | W3C Recommendation 2021, https://www.w3.org/TR/webaudio-1.0/ | Grafo audio; latencyHint come preferenza; baseLatency/outputLatency hanno ambiti distinti | Non misura percorso tasto-suono. Non usata bozza 1.1 come standard definitivo |
| eng_jack | JACK, https://jackaudio.org/api/group__ClientCallbacks.html | Callback realtime: evitare I/O, malloc/free e operazioni bloccanti | Non dimostra scelta/integrazione JACK nel progetto |
| eng_pipewire | PipeWire, https://docs.pipewire.org/devel/page_latency.html | Latenze aggregate nel grafo, porte/nodi/link | Documentazione devel: fissare versione in implementazione |
| eng_fluidsynth | FluidSynth, https://www.fluidsynth.org/api/settings_synth.html | sample-rate definita alla creazione; coerenza con driver | Candidato, nessuna misura timbrica/prestazionale locale |

Fonti storiche: lettura integrale del PDF originale locale `originale.pdf` (5 pagine) e sezioni 02/05 della v0.4. Il concept riporta MIDI, pedali, computer, grafica, webcam e Dolby Stereo Spectral Recording. L'architettura contemporanea non attribuisce al documento del 2016 prescrizioni software che non contiene.

## Decisioni proposte, non fatti dimostrati

- Core nativo Linux con UI kiosk; candidati FluidSynth/PipeWire/JACK. Browser integrale resta alternativa.
- Budget mediana <=15 ms, p95 <=20 ms, p95-mediana <=5 ms: obiettivi ingegneristici da validare, non soglie universali di percezione musicale. Quote 5+8+4+3 ms sono un'allocazione proposta. Nessun percentile è stato misurato.
- Calcolo 128/48000 = 2,6667 ms riguarda un blocco, non tutto il sistema.
- Sessione: avviso 120 s, grazia 30 s; non usare il solo silenzio per inferire abbandono.
- AI: timeout 8 s, contenuti curati disponibili. Validazione dei file musicali obbligatoria prima dell'esecuzione; nessuna esecuzione di codice generato.
- Log tecnici: proposta locale 7 giorni, da approvare. Nessuna dichiarazione di conformità GDPR o certificazione elettrica/acustica.
- Prove E1-E6: protocollo proposto, da eseguire. Campione 1.000 eventi/8 ore è una prima prova tecnica, non dimostrazione generale di affidabilità.
- Versioni, banca timbrica, hardware, budget energetico, struttura/impianti e livello acustico restano decisioni da collaudare con competenze specifiche.

## Verifiche editoriali suggerite a Pi

1. Controllare che tutti i numeri siano etichettati come obiettivi o calcoli, mai risultati.
2. Verificare assenza di dipendenza cloud nella catena gesto-suono.
3. Distinguere MIDI da audio; non confondere All Notes Off con silenziamento fisico.
4. Verificare sessioni, risposte AI tardive e reset tra visitatori.
5. Controllare che il testo non prometta musica sincrona remota attraverso una normale videochiamata.
6. Valutare ogni test rispetto al rischio che dovrebbe rilevare; aggiungere prove di sicurezza/acustica/accessibilità nell'apposita sezione.
