# Nolvac — Unità di Convogliamento Pneumatico

## Panoramica

Il Nolvac è un'unità di convogliamento pneumatico a ciclo aspirazione/pulizia. `XY03` attiva il percorso di aspirazione per convogliare il materiale durante la fase di convogliamento; `XV01` (valvola a farfalla SS) e `XY02` agiscono in combinazione durante la fase di pulizia per rigenerare il filtro interno. Il blocco funzionale `Nolvac` gestisce il ciclo completo tramite il parametro `VC : UDT_Nolvac`.

Il ciclo alterna due fasi: **convogliamento** (`suction_time`) e **pulizia** (`cleaning_time`). Al termine di ogni fase il ciclo riparte automaticamente finché `CMD.auto` è attivo.

---

## Componenti principali

- **Elettrovalvola convogliamento `XY03`** — attiva la depressione/il percorso d'aria per il convogliamento del materiale; eccitata per tutta la fase CONVEYING
- **Valvola di ingresso `XV01`** — valvola a farfalla SS che apre l'ingresso durante la fase di pulizia; vedere [Valvola a Farfalla SS](../valves/butterfly/single_solenoid/index.it.md)
- **Elettrovalvola pulizia `XY02`** — fornisce aria compressa per il retrolavaggio/pulizia del filtro durante la fase CLEANING

---

## Segnali I/O

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `DEVICES.XV01` | UDT_SS_Valve | Valvola farfalla SS; aperta durante CLEANING |
| `DEVICES.XY02` | UDT_Solenoid_valve | Solenoide pulizia; eccitato durante CLEANING |
| `DEVICES.XY03` | UDT_Solenoid_valve | Solenoide convogliamento; eccitato durante CONVEYING |
| `CMD.manual_mode` | Bool | TRUE = modalità manuale HMI |
| `CMD.auto` | Bool | Comando automazione: TRUE = avvia ciclo |
| `CMD.ack` | Bool | Conferma allarme operatore |
| `STATUS.state` | Int | Stato FSM corrente (0=ERROR, 1=IDLE, 2=CONVEYING, 3=CLEANING) |
| `STATUS.is_conveying` | Bool | TRUE durante la fase di convogliamento |
| `STATUS.is_cleaning` | Bool | TRUE durante la fase di pulizia filtro |
| `ALARMS.valve_error` | Bool | Guasto rilevato su `XV01` |

---

## Funzionamento

Il ciclo operativo standard si articola in due fasi che si alternano fintanto che il comando `auto` è attivo:

**Fase CONVEYING** — `XY03` viene eccitato per la durata `suction_time`. Il percorso di convogliamento è attivo e il materiale viene trasportato. Al termine del timer, il sistema transisce in CLEANING.

**Fase CLEANING** — `XV01` viene aperta e `XY02` eccitata per la durata `cleaning_time`. L'aria compressa rigenerava il filtro tramite retrolavaggio. Al termine del timer, il sistema torna in CONVEYING se `CMD.auto` è ancora attivo.

Se `CMD.auto` viene rimosso in qualsiasi momento durante CONVEYING o CLEANING, il sistema torna immediatamente a IDLE, disattivando tutte le uscite.

Un guasto su `XV01` (rilevato tramite `XV01.ALARMS.error`) imposta `ALARMS.valve_error = TRUE` e porta il sistema in ERROR indipendentemente dalla fase corrente. Per riprendere, l'operatore deve risolvere il guasto sulla sotto-valvola e confermare con `CMD.ack`. Dopo la conferma, il sistema torna in IDLE e può ricevere un nuovo comando `auto`.

---

## Allarmi

| ID | Condizione | Causa |
|----|------------|-------|
| NV-E01 | `ALARMS.valve_error` | Guasto su `XV01` — vedere [allarmi valvola SS](../valves/butterfly/single_solenoid/index.it.md#allarmi) |

---

## Parametri

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `SETTING.suction_time` | T#30s | Durata della fase di convogliamento |
| `SETTING.cleaning_time` | T#30s | Durata della fase di pulizia filtro |

---

## Struttura dati

```mermaid
classDiagram
    class UDT_Nolvac
    class DEVICES {
        +UDT_SS_Valve XV01
        +UDT_Solenoid_valve XY02
        +UDT_Solenoid_valve XY03
    }
    class CMD {
        +Bool manual_mode
        +Bool auto
        +Bool interlocked
        +Bool ack
    }
    class SETTING {
        +Time suction_time
        +Time cleaning_time
    }
    class STATUS {
        +Int state
        +Bool is_conveying
        +Bool is_cleaning
    }
    class ALARMS {
        +Bool valve_error
    }
    UDT_Nolvac *-- DEVICES
    UDT_Nolvac *-- CMD
    UDT_Nolvac *-- SETTING
    UDT_Nolvac *-- STATUS
    UDT_Nolvac *-- ALARMS
```

---

## Macchina a stati (FSM)

```mermaid
stateDiagram-v2
    [*] --> IDLE

    IDLE --> CONVEYING : CMD.auto
    IDLE --> ERROR : valve_error

    CONVEYING --> IDLE : NOT CMD.auto
    CONVEYING --> CLEANING : suction_time scaduto
    CONVEYING --> ERROR : valve_error

    CLEANING --> IDLE : NOT CMD.auto
    CLEANING --> CONVEYING : cleaning_time scaduto
    CLEANING --> ERROR : valve_error

    ERROR --> IDLE : CMD.ack
```

### Tabella stati e uscite

| Stato | `XV01` | `XY02` | `XY03` | Descrizione |
|-------|--------|--------|--------|-------------|
| IDLE | chiusa | spenta | spenta | In attesa del comando auto |
| CONVEYING | chiusa | spenta | eccitata | Convogliamento attivo per `suction_time` |
| CLEANING | aperta | eccitata | spenta | Pulizia filtro per `cleaning_time` |
| ERROR | — | spenta | spenta | Guasto valvola; attende conferma operatore |

### Tabella transizioni di stato

| Stato attuale | Condizione | Stato successivo | Azione |
|---------------|------------|-----------------|--------|
| IDLE | CMD.auto = TRUE | CONVEYING | XY03 → eccitata; avvia suction_timer |
| IDLE | valve_error | ERROR | — |
| CONVEYING | NOT CMD.auto | IDLE | Tutte uscite → diseccitate |
| CONVEYING | suction_timer scaduto | CLEANING | XY03 → spenta; XV01 apre, XY02 → eccitata; avvia cleaning_timer |
| CONVEYING | valve_error | ERROR | Tutte uscite → diseccitate |
| CLEANING | NOT CMD.auto | IDLE | Tutte uscite → diseccitate |
| CLEANING | cleaning_timer scaduto | CONVEYING | XV01 chiude, XY02 → spenta; XY03 → eccitata; avvia suction_timer |
| CLEANING | valve_error | ERROR | Tutte uscite → diseccitate |
| ERROR | CMD.ack = TRUE | IDLE | Azzera allarmi; attende nuovo CMD.auto |
