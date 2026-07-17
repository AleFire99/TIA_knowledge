# Libreria — Panoramica Moduli

Libreria moduli NTE Process. Ogni modulo è un blocco funzionale PLC autonomo con I/O, allarmi e parametri definiti.

I moduli sono raggruppati per tipo. Ogni pagina modulo descrive: panoramica, componenti, segnali I/O, funzionamento, allarmi, parametri, struttura dati e diagramma di stato.

Il comando `manual_mode`/`manual`/`auto` si risolve solo al livello più esterno esposto a HMI/DCS; i componenti annidati (es. elettrovalvole interne) ricevono soltanto l'`auto` già risolto dal blocco che li incorpora — non arbitrano in autonomia.

Ogni timer di libreria segue lo stesso schema: è un TON il cui `IN` è legato esclusivamente allo stato (o sotto-stato) in cui deve essere attivo — si avvia entrando in quello stato e si resetta automaticamente uscendone, senza altre condizioni. Per questo la tabella Timer di ogni pagina modulo elenca solo `Timer | Stato in cui è attivo | Soglia (parametro)`: la condizione di reset non è mai un'informazione a parte, è sempre "si esce da quello stato".

---

## [Valvole](valves/index.md)

Valvole controllate pneumaticamente per isolamento, attuazione e controllo di processo.

| Modulo | Descrizione |
|--------|-------------|
| [Elettrovalvola](valves/solenoid/index.md) | Valvola on/off semplice; nessuna retroazione |
| [Valvola a Manicotto](valves/pinch/index.md) | Comprime un tubo flessibile per chiudersi; pressostato conferma la posizione |
| [Valvola a Farfalla — Singolo Solenoide](valves/butterfly/single_solenoid/index.md) | Ritorno a molla; retroazione di posizione via ZSL/ZSH |
| [Valvola a Farfalla — Doppio Solenoide](valves/butterfly/double_solenoid/index.md) | Bistabile, doppio effetto; retroazione di posizione via ZSL/ZSH |
| [Valvola Sigillata — Singolo Solenoide](valves/sealed/ss/index.md) | Valvola SS + elettrovalvola di tenuta dedicata |

---

## [Dispositivi di Accesso](access/index.md)

Il PLC concede solo il permesso di sblocco in base allo stato corrente — l'accesso fisico resta all'operatore, il PLC non movimenta nulla.

| Modulo | Descrizione |
|--------|-------------|
| [Anta Cancello — Blocco Elettrico](access/gate/index.md) | Sblocco/blocco elettrovalvola su richiesta operatore; nessun movimento comandato dal PLC |

---

## [Filtri](filters/index.md)

Sistemi di pulizia a impulsi d'aria compressa per maniche filtranti.

| Modulo | Descrizione |
|--------|-------------|
| [Pulitore Filtro — 1 Manica](filters/1-sleeve/index.md) | Ciclo a impulso periodico con una singola elettrovalvola |
| [Pulitore Filtro — 2 Maniche](filters/2-sleeves/index.md) | Sequenza di impulsi alternati su due maniche |

---

## [Deviatori](diverters/index.md)

Deviano il materiale convogliato tra due o più percorsi di scarico tramite un meccanismo attuato pneumaticamente.

| Modulo | Descrizione |
|--------|-------------|
| [Deviatore a Manicotto](diverters/pinch_type/index.md) | Doppia valvola a manicotto che devia il materiale tra due percorsi |

---

## Nolvac

Unità di convogliamento pneumatico a ciclo aspirazione/pulizia.

| Modulo | Descrizione |
|--------|-------------|
| [Nolvac](nolvac/index.md) | Cicli alternati di aspirazione materiale e pulizia filtro |

---

## [Celle di Carico](load-cells/index.md)

Sistema di pesatura basato su un'unica struttura dati condivisa, con la logica di ciclo separata dal trasmettitore fisico tramite un'interfaccia intercambiabile.

| Modulo | Descrizione |
|--------|-------------|
| [Ciclo di Carico e Scarico](load-cells/loading-unloading/index.md) | Riempimento e svuotamento a peso; timeout, pausa/ripresa |
| [Interfaccia Pavone DAT 1400](load-cells/pavone-dat-1400/index.md) | Adatta il trasmettitore Pavone Sistemi DAT 1400 ai campi IN condivisi |

---

## [Segnali Analogici](io/index.md)

Utility di libreria condivisa: converte un conteggio grezzo di ingresso analogico in un valore scalato in unità ingegneristiche.

| Modulo | Descrizione |
|--------|-------------|
| [Segnali Analogici](io/index.md) | Conversione conteggio grezzo → valore scalato, usata da Pipeline Analogica e Propulsore Ingresso Sigillato |

---

## [Propulsori](transporters/index.md)

Trasportano materiale tra due punti tramite un ciclo di carico, trasferimento e scarico pressurizzato.

| Modulo | Descrizione |
|--------|-------------|
| [Propulsore Ingresso Sigillato](transporters/sealed-inlet/index.md) | Ciclo carico → sigillatura → pressurizzazione → convogliamento → depressurizzazione |

---

## [Pipeline](pipeline/index.md)

Derivazione dello stato di pressione dalla lettura di un trasmettitore PT o di due pressostati digitali. Nessuna macchina a stati — stato funzione diretta e istantanea della lettura corrente, senza isteresi.

| Modulo | Descrizione |
|--------|-------------|
| [Pipeline Analogica](pipeline/analogic/index.md) | Stato pressione da trasmettitore PT; 3 soglie configurabili, nessuna isteresi attualmente (possibile estensione futura) |
| [Pipeline Digitale](pipeline/digital/index.md) | Stato pressione da 2 pressostati (PSL/PSH); allarme intasamento e disallineamento sensori |
