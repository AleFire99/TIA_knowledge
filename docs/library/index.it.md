# Libreria — Panoramica Moduli

Libreria moduli NTE Process. Ogni modulo è un blocco funzionale PLC autonomo con I/O, allarmi e parametri definiti.

I moduli sono raggruppati per tipo. Ogni pagina modulo descrive: panoramica, componenti, segnali I/O, funzionamento, allarmi, parametri, struttura dati e macchina a stati.

---

## Deviatori

Deviano il materiale convogliato tra due o più percorsi di scarico tramite un meccanismo attuato pneumaticamente.

| Modulo | Descrizione |
|--------|-------------|
| [Deviatore a Manicotto](diverters/pinch_type/index.md) | Doppia valvola a manicotto che devia il materiale tra due percorsi |
| [Deviatore a Spina (Plug-Type)](diverters/plug_type/index.md) | Spina con guarnizione gonfiabile e attuatore pneumatico; adatto per polveri abrasive |

---

## Valvole

Valvole controllate pneumaticamente per isolamento, attuazione e controllo di processo.

| Modulo | Descrizione |
|--------|-------------|
| [Valvola a Solenoide](valves/solenoid/index.md) | Valvola on/off semplice; nessun feedback |
| [Valvola a Manicotto](valves/pinch/index.md) | Comprime un tubo flessibile per chiudersi; pressostato conferma la posizione |
| [Valvola a Farfalla — Solenoide Singolo](valves/butterfly/single_solenoid/index.md) | Ritorno a molla; feedback posizione via ZSL/ZSH; contatore manutenzione |
| [Valvola a Farfalla — Doppio Solenoide](valves/butterfly/double_solenoid/index.md) | Bistabile; mantiene ultima posizione a solenoide diseccitato; feedback ZSL/ZSH |

---

## Filtri

Sistemi di pulizia a impulsi d'aria compressa per maniche filtranti.

| Modulo | Descrizione |
|--------|-------------|
| [Pulitore Filtro — 1 Manica](filters/1-sleeve/index.md) | Ciclo a impulso periodico con singolo solenoide |
| [Pulitore Filtro — 2 Maniche](filters/2-sleeves/index.md) | Sequenza di impulsi alternati su due maniche |

---

## Celle di Carico

Sistema di pesatura con trasmettitore DAT 1400 via PROFINET. Strato di configurazione operatore + FSM di ciclo trasporto.

| Modulo | Descrizione |
|--------|-------------|
| [Celle di Carico](load-cells/index.md) | Pesatura batch con DAT 1400 PROFINET; tara, validazione setpoint, conteggio conveyed |

---

## Pipeline

Derivazione dello stato di pressione dalla lettura di un trasmettitore PT. Nessuna FSM — stato funzione diretta del valore PT con isteresi.

| Modulo | Descrizione |
|--------|-------------|
| [Supervisione Pipeline](pipeline/index.md) | Quattro stati (EMPTY / PRESSURISED / WITH_MATERIAL / CLOGGED) da PT con isteresi a banda |
