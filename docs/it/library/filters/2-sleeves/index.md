# Pulitore Filtro — 2 Maniche

## Panoramica

**Livello 2.** Il pulitore filtro a 2 maniche genera impulsi alternati di aria compressa tramite due Elettrovalvole (Livello 1, `XYA`/`XYB`) per pulire un filtro a doppia manica. Le maniche vengono pulsate in sequenza — mai simultaneamente — per minimizzare il calo di pressione nell'accumulatore e garantire una pulizia efficace di ciascuna manica. Non è presente alcuna retroazione di posizione — il sistema è ad anello aperto.

Nessun allarme proprio — nessun sensore di retroazione disponibile su cui basare una rilevazione di guasto.

---

## Interfaccia

### Composizione

| Tag | Tipo | Ruolo |
|-----|------|-------|
| `XYA` | Elettrovalvola (Livello 1) | Impulso manica A |
| `XYB` | Elettrovalvola (Livello 1) | Impulso manica B |

### Struttura dati

```mermaid
classDiagram
    class UDT_Filter_2_sleeves
    class DEVICES {
        -UDT_Solenoid_valve XYA
        -UDT_Solenoid_valve XYB
    }
    class CMD {
        +Bool manual_mode
        +Bool manual
        -Bool auto
    }
    class SETTING {
        +Time pulse_duration
        +Time interval_duration
    }
    class STATUS {
        -Int state
        -Int active_state
        -Int active_sleeve
        -Bool is_idle
        -Bool is_active
        -Bool is_pulsing
        -Bool is_waiting
        -Bool is_sleeve_A
        -Bool is_sleeve_B
    }
    UDT_Filter_2_sleeves *-- DEVICES
    UDT_Filter_2_sleeves *-- CMD
    UDT_Filter_2_sleeves *-- SETTING
    UDT_Filter_2_sleeves *-- STATUS
```

`+` = scrivibile da DCS/HMI, `-` = sola lettura.

### Segnali di controllo

| Segnale | Tipo | Direzione | Descrizione |
|---------|------|-----------|-------------|
| `DEVICES.XYA` | UDT_Solenoid_valve | OUT | Elettrovalvola impulso manica A — comandata, il proprio stato non viene riletto da questo blocco |
| `DEVICES.XYB` | UDT_Solenoid_valve | OUT | Elettrovalvola impulso manica B — comandata, il proprio stato non viene riletto da questo blocco |
| `CMD.manual_mode` | Bool | IN | TRUE = modalità manuale |
| `CMD.manual` | Bool | IN | Abilitazione in modalità manuale |
| `CMD.auto` | Bool | IN | Abilitazione in modalità automatica |

### Parametri

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `pulse_duration` | T#500ms | Durata di ogni impulso d'aria per manica |
| `interval_duration` | T#3s | Tempo di attesa tra gli impulsi |

---

## Comportamento

### Funzionamento

Quando abilitato, il sistema alterna tra le maniche A e B in un ciclo continuo:

1. **PULSING manica A** — `XYA` eccitato per `pulse_duration`
2. **WAITING** — entrambe le elettrovalvole spente per `interval_duration`
3. **PULSING manica B** — `XYB` eccitato per `pulse_duration`
4. **WAITING** — entrambe le elettrovalvole spente per `interval_duration`
5. Ripetere dal passo 1

La manica attiva è tracciata da `STATUS.is_sleeve_A`/`is_sleeve_B`. La rimozione del comando di abilitazione in qualsiasi momento riporta il sistema in **IDLE**.

In **modalità manuale** (`manual_mode = TRUE`), l'operatore abilita la pulizia tramite `manual`. In **modalità automatica**, il comando arriva dal processo tramite `auto`.

### Diagramma di stato

```mermaid
stateDiagram-v2
state FILTER{
    [*] --> IDLE
    IDLE --> ACTIVE : desired_command
    ACTIVE --> IDLE : !desired_command

    state ACTIVE {
        [*] --> PULSING
        PULSING --> WAITING : pulse_timer scaduto
        WAITING --> PULSING : interval_timer scaduto (cambia manica)
    }
}
```

```Pascal
desired_command := (CMD.manual_mode AND CMD.manual) OR (NOT CMD.manual_mode AND CMD.auto);
```

| Stato | `XYA` | `XYB` | Descrizione |
|-------|-------|-------|-------------|
| IDLE | FALSE | FALSE | Standby, nessuna pulizia |
| ACTIVE / PULSING (manica A) | TRUE | FALSE | Impulso d'aria nella manica A |
| ACTIVE / PULSING (manica B) | FALSE | TRUE | Impulso d'aria nella manica B |
| ACTIVE / WAITING | FALSE | FALSE | Intervallo tra impulsi |

### Timer

| Timer | Stato in cui è attivo | Soglia (parametro) |
|-------|------------------------|---------------------|
| `pulse_timer` | ACTIVE/PULSING | `SETTING.pulse_duration` |
| `interval_timer` | ACTIVE/WAITING | `SETTING.interval_duration` |
