# Nolvac — Unità di Convogliamento Pneumatico

## Panoramica

**Livello 3 — composito.** Il Nolvac è un'unità di convogliamento pneumatico a ciclo aspirazione/pulizia, incorporando una Valvola a Farfalla SS (Livello 2) e due Elettrovalvole (Livello 1). `XY03` attiva il percorso di aspirazione per convogliare il materiale; `XV01` e `XY02` agiscono in combinazione durante la fase di pulizia per rigenerare il filtro interno.

---

## Interfaccia

### Composizione

| Tag | Tipo | Direzione | Ruolo |
|-----|------|-----------|-------|
| `XV01` | Valvola a Farfalla SS (Livello 2) | IN/OUT | Apre l'ingresso durante `CLEANING` — vedere [Valvola a Farfalla SS](../valves/butterfly/single_solenoid/index.md) |
| `XY02` | Elettrovalvola (Livello 1) | OUT | Aria compressa di retrolavaggio filtro durante `CLEANING` |
| `XY03` | Elettrovalvola (Livello 1) | OUT | Depressione di trasporto durante `SUCTION` |

`XV01` è IN/OUT: il Nolvac scrive `CMD.ack`/`CMD.auto` e rilegge `STATUS.is_fault` per la propria `internal_error`. `XY02`/`XY03` sono OUT-only: comandate, il proprio stato non viene mai riletto.

### Struttura dati

```mermaid
classDiagram
    class UDT_Nolvac
    class DEVICES {
        -UDT_SS_Valve XV01
        -UDT_Solenoid_valve XY02
        -UDT_Solenoid_valve XY03
    }
    class CMD {
        +Bool manual_mode
        +Bool manual
        -Bool auto
        +Bool ack
    }
    class SETTING {
        +Time suction_time
        +Time cleaning_time
    }
    class STATUS {
        -Int state
        -Int normal_state
        -Int active_state
        -Bool is_idle
        -Bool is_active
        -Bool is_suction
        -Bool is_cleaning
        -Bool is_fault
    }
    UDT_Nolvac *-- DEVICES
    UDT_Nolvac *-- CMD
    UDT_Nolvac *-- SETTING
    UDT_Nolvac *-- STATUS
```

`+` = scrivibile da DCS/HMI, `-` = sola lettura (`ReadOnly := External` nel sorgente). Nessuna classe `ALARMS` — questo UDT non ne possiede una propria.

### Segnali di controllo

| Segnale | Tipo | Direzione | Descrizione |
|---------|------|-----------|-------------|
| `DEVICES.XV01` | UDT_SS_Valve | IN/OUT | Valvola farfalla SS; aperta durante `CLEANING` |
| `DEVICES.XY02` | UDT_Solenoid_valve | OUT | Elettrovalvola pulizia; eccitata durante `CLEANING` |
| `DEVICES.XY03` | UDT_Solenoid_valve | OUT | Elettrovalvola aspirazione; eccitata durante `SUCTION` |
| `CMD.manual_mode` | Bool | IN | TRUE = modalità manuale HMI |
| `CMD.manual` | Bool | IN | Comando di avvio ciclo in modalità manuale |
| `CMD.auto` | Bool | IN | Comando di avvio ciclo in modalità automatica |
| `CMD.ack` | Bool | IN | Conferma allarme e ripristino da FAULT |

### Parametri

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `SETTING.suction_time` | T#30s | Durata della fase di aspirazione |
| `SETTING.cleaning_time` | T#30s | Durata della fase di pulizia filtro |

---

## Comportamento

### Funzionamento

Il ciclo alterna due fasi — **aspirazione** (`suction_time`) e **pulizia** (`cleaning_time`) — e riparte automaticamente finché il comando resta attivo.

La rimozione del comando in qualsiasi momento durante `ACTIVE` riporta immediatamente a `IDLE`, disattivando tutte le uscite.

### Allarmi

Nessun allarme proprio — `UDT_Nolvac` non possiede una struttura `ALARMS`. L'unico guasto rilevato dal blocco è la propagazione diretta di `XV01.STATUS.is_fault` — le elettrovalvole `XY02`/`XY03` non hanno sensori propri e non possono generare un guasto. Vedere [Allarmi delle valvole](../valves/index.md#allarmi-delle-valvole) per la causa effettiva quando `internal_error` è TRUE.

### Diagramma di stato

```mermaid
stateDiagram-v2
state NOLVAC{
    [*] --> NORMAL_BEHAVIOUR
    state NORMAL_BEHAVIOUR {
        [*] --> IDLE
        IDLE --> ACTIVE : desired_command
        state ACTIVE {
            [*] --> SUCTION
            SUCTION --> CLEANING : suction_timer scaduto
            CLEANING --> SUCTION : cleaning_timer scaduto
        }
        ACTIVE --> IDLE : !desired_command
    }
    NORMAL_BEHAVIOUR --> FAULT : internal_error
    FAULT --> NORMAL_BEHAVIOUR : ack & !internal_error
}
```

```Pascal
internal_error := XV01.STATUS.is_fault;
```

| Stato | `XV01` | `XY02` | `XY03` | Descrizione |
|-------|--------|--------|--------|-------------|
| IDLE | chiusa | spenta | spenta | Standby, in attesa del comando |
| ACTIVE / SUCTION | chiusa | spenta | eccitata | Aspirazione del materiale |
| ACTIVE / CLEANING | aperta | eccitata | spenta | Pulizia del filtro |
| FAULT | — | spenta | spenta | Guasto; attende conferma operatore |

### Timer

| Timer | Stato in cui è attivo | Soglia (parametro) |
|-------|------------------------|---------------------|
| `suction_timer` | ACTIVE/SUCTION (in NORMAL) | `SETTING.suction_time` |
| `cleaning_timer` | ACTIVE/CLEANING (in NORMAL) | `SETTING.cleaning_time` |
