# Libreria — Panoramica Moduli

Libreria moduli NTE Process. Ogni modulo è un blocco funzionale PLC autonomo con I/O, allarmi e parametri definiti.

I moduli sono raggruppati per tipo. Ogni pagina modulo descrive: panoramica, componenti, segnali I/O, funzionamento, allarmi, parametri, struttura dati e macchina a stati.

---

## Deviatori

Deviano il materiale convogliato tra due o più percorsi di scarico tramite un meccanismo attuato pneumaticamente.

| Modulo | Descrizione |
|--------|-------------|
| [Deviatore a Manicotto](diverters/pinch_type/index.md) | Doppia valvola a manicotto che devia il materiale tra due percorsi |

---

## Valvole

Valvole controllate pneumaticamente per isolamento, attuazione e controllo di processo.

| Modulo | Descrizione |
|--------|-------------|
| [Elettrovalvola](valves/solenoid/index.md) | Valvola on/off semplice; nessun feedback |
| [Valvola a Manicotto](valves/pinch/index.md) | Comprime un tubo flessibile per chiudersi; pressostato conferma la posizione |
| [Valvola a Farfalla — Solenoide Singolo](valves/butterfly/single_solenoid/index.md) | Ritorno a molla; feedback posizione via ZSL/ZSH |
| [Valvola a Farfalla — Doppio Solenoide](valves/butterfly/double_solenoid/index.md) | Bistabile, doppio effetto; feedback posizione via ZSL/ZSH |
| [Valvola Sigillata — Solenoide Singolo](valves/sealed/ss/index.md) | Valvola SS + elettrovalvola di tenuta dedicata |

---

## Portello

Blocco elettrico per un portello ad apertura manuale — il PLC concede solo il permesso di sblocco, non movimenta nulla.

| Modulo | Descrizione |
|--------|-------------|
| [Portello con Blocco Elettrico](gate/index.md) | Sblocco/blocco elettrovalvola su richiesta operatore; nessun movimento comandato dal PLC |

---

## Nolvac

Unità di convogliamento pneumatico a ciclo aspirazione/pulizia.

| Modulo | Descrizione |
|--------|-------------|
| [Nolvac](nolvac/index.md) | Cicli alternati di aspirazione materiale e pulizia filtro |

---

## Trasportatori

Trasportano materiale tra due punti tramite un ciclo di carico, trasferimento e scarico pressurizzato.

| Modulo | Descrizione |
|--------|-------------|
| [Trasportatore Ingresso Sigillato](transporters/sealed-inlet/index.md) | Ciclo carico → sigillatura → pressurizzazione → convogliamento → depressurizzazione |

---

## Filtri

Sistemi di pulizia a impulsi d'aria compressa per maniche filtranti.

| Modulo | Descrizione |
|--------|-------------|
| [Pulitore Filtro — 1 Manica](filters/1-sleeve/index.md) | Ciclo a impulso periodico con una singola elettrovalvola |
| [Pulitore Filtro — 2 Maniche](filters/2-sleeves/index.md) | Sequenza di impulsi alternati su due maniche |

---

## Celle di Carico

Sistema di pesatura con trasmettitore DAT 1400 via PROFINET. Strato di configurazione operatore + FSM di ciclo trasporto.

| Modulo | Descrizione |
|--------|-------------|
| [Celle di Carico](load-cells/index.md) | Pesatura batch con DAT 1400 PROFINET; tara, validazione setpoint, conteggio conveyed |

---

## Pipeline

Derivazione dello stato di pressione dalla lettura di un trasmettitore PT o di due pressostati digitali. Nessuna FSM — stato funzione diretta e istantanea della lettura corrente, senza isteresi.

| Modulo | Descrizione |
|--------|-------------|
| [Supervisione Pipeline](pipeline/index.md) | Varianti analogica (PT) e digitale (PSL/PSH); stati vuota/pressurizzata/con materiale + allarme intasamento |
