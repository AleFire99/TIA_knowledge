# Propulsore a Ingresso Sigillato (Sealed Inlet Transporter)

## Panoramica

**Tier 3 — composito.** `Sealed_inlet_Transporter` gestisce un ciclo completo di trasporto pneumatico in pressione: carica materiale in un vessel, lo sigilla, lo pressurizza a pressione superiore a quella della linea, convoglia il materiale verso la linea e infine depressurizza il vessel prima di un nuovo ciclo.

Il blocco coordina cinque valvole (`XV01`–`XV05`), un'elettrovalvola di pressurizzazione (`XY`), una bilancia (`WT01`) e due trasmettitori di pressione analogici (`PT01` vessel, `PT02` linea). Due pressostati digitali (`PSL`, `LSH`) garantiscono la sicurezza operativa.

La FSM è a due livelli: `NORMAL`/`FAULT` al livello superiore; `IDLE`→`FILLING`→`CLEANING`→`SEALING`→`PRESSURIZING`→`CONVEYING`→`DEPRESSURIZING` al livello operativo.

---

## Composizione

| Tag | Tipo | Ruolo |
|-----|------|-------|
| `XV01` | Valvola Sigillata SS (Tier 3) | Valvola di ingresso; sigillata in riposo |
| `XV02` | Valvola a Farfalla DS (Tier 3) | Valvola di sfiato (vent); aperta in IDLE, FILLING, FAULT |
| `XV03` | Valvola a Farfalla SS (Tier 2) | Valvola orifizio; aperta durante FILLING |
| `XV04` | Valvola a Farfalla SS (Tier 2) | Valvola di scarico; aperta durante PRESSURIZING e CONVEYING |
| `XV05` | Valvola a Farfalla SS (Tier 2) | Valvola di linea; aperta durante CONVEYING |
| `XY` | Elettrovalvola (Tier 1) | Elettrovalvola pressurizzazione; eccitata durante PRESSURIZING e CONVEYING |
| `WT01` | Celle di Carico (Tier 3) | Bilancia; gestita da `Loading` e `Unloading` interni — vedere [Celle di Carico](../../load-cells/index.md) |
| `PT01` | UDT_Analogic_signal | Trasmettitore pressione vessel |
| `PT02` | UDT_Analogic_signal | Trasmettitore pressione linea |
| `PSL` | Bool | Pressostato sicurezza: TRUE = pressione entro limiti |
| `LSH` | Bool | Sensore livello alto: TRUE = vessel pieno (condizione di guasto) |

---

## Segnali I/O

### Comandi (`CMD`)

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `CMD.ack` | Bool | Conferma allarmi; propagato a tutti i sotto-dispositivi |
| `CMD.start_loading` | Bool | Avvia la sequenza di carico (IDLE → FILLING) |
| `CMD.start_convey` | Bool | Avvia la sequenza di convogliamento senza carico (IDLE → SEALING) |
| `CMD.stop` | Bool | Arresto operatore; porta verso DEPRESSURIZING o IDLE |

### Parametri (`SETTING`)

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `SETTING.cleaning_timer` | Time | Durata fase CLEANING |
| `SETTING.pressurizing_timeout` | Time | Timeout massimo per raggiungere la pressione di convogliamento |
| `SETTING.depressurizing_timeout` | Time | Timeout massimo per ritornare alla pressione atmosferica |
| `SETTING.pressure_delta` | Real | Sovrapressione minima vessel rispetto alla linea per aprire XV05 [bar] |
| `SETTING.vessel_empty_thresh` | Real | Soglia PT01 per considerare il vessel a pressione atmosferica [bar] |
| `SETTING.line_empty_thresh` | Real | Soglia PT02 per considerare la linea a pressione atmosferica [bar] |

### Stato (`STATUS`)

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `STATUS.state` | Int | 0=FAULT, 1=NORMAL |
| `STATUS.normal_state` | Int | 10=IDLE, 20=FILLING, 30=CLEANING, 40=SEALING, 50=PRESSURIZING, 60=CONVEYING, 70=DEPRESSURIZING |
| `STATUS.is_fault` | Bool | TRUE in FAULT |
| `STATUS.is_idle` | Bool | TRUE in IDLE |
| `STATUS.is_filling` | Bool | TRUE in FILLING |
| `STATUS.is_cleaning` | Bool | TRUE in CLEANING |
| `STATUS.is_sealing` | Bool | TRUE in SEALING |
| `STATUS.is_pressurizing` | Bool | TRUE in PRESSURIZING |
| `STATUS.is_conveying` | Bool | TRUE in CONVEYING |
| `STATUS.is_depressurizing` | Bool | TRUE in DEPRESSURIZING |

### Uscite (`OUT`)

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `OUT.loading_finished` | Bool | Impulso 1-scan all'ingresso in SEALING da CLEANING (carico completato) |
| `OUT.conveying_done` | Bool | Impulso 1-scan all'ingresso in IDLE (ciclo terminato) |
| `OUT.filter_cleaner_command` | Bool | TRUE durante CLEANING — abilita il sistema di pulizia filtro esterno |
| `OUT.last_transferred` | Real | Quantità convogliata nell'ultimo ciclo CONVEYING [kg] |

### Allarmi (`ALARMS`)

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `ALARMS.pressurization_timeout` | Bool | Pressurizzazione non completata entro `pressurizing_timeout` |
| `ALARMS.depressurization_timeout` | Bool | Depressurizzazione non completata entro `depressurizing_timeout` |

`internal_error` (OR di tutti i guasti interni: valvole, bilancia, `PSL`, `LSH`, oltre ai due allarmi sopra) è interno al blocco funzionale — non è un campo dell'UDT.

---

## Funzionamento

### Condizioni derivate (ogni scan)

- **`all_loading_closed`** — XV01, XV02, XV03 tutti confermati chiusi (prerequisito per SEALING → PRESSURIZING)
- **`pressure_gate_met`** — `PT01 ≥ PT02 + pressure_delta` (vessel abbastanza sovrapressurizzato rispetto alla linea)
- **`depressurized`** — `PT01 ≤ vessel_empty_thresh AND PT02 ≤ line_empty_thresh`
- **`internal_error`** — guasto su XV01/02/03/04/05, timeout bilancia, `NOT PSL` (pressione di sicurezza persa) o `LSH` (livello alto)

### Sequenza di carico

1. **IDLE** → `CMD.start_loading` → **FILLING**: XV01 (ingresso), XV02 (sfiato), XV03 (orifizio) aperti; il FB `Loading` gestisce la bilancia.
2. **FILLING** → bilancia raggiunge il setpoint (`loading_finished`) → **CLEANING**: filtro di ingresso rigenerato per `cleaning_timer`.
3. **CLEANING** → timer scaduto → **SEALING**: tutte le valvole di ingresso si chiudono.
4. **SEALING** → `all_loading_closed` → **PRESSURIZING**: XY eccitato + XV04 (scarico) aperto per pressurizzare il vessel.
5. **PRESSURIZING** → `pressure_gate_met` → **CONVEYING**: XV05 (linea) aperto; il FB `Unloading` gestisce la bilancia.
6. **CONVEYING** → bilancia svuotata o `CMD.stop` → **DEPRESSURIZING**: XV02 (sfiato) aperto per scaricare la pressione.
7. **DEPRESSURIZING** → `depressurized` → **IDLE**: `OUT.conveying_done` impulso 1-scan.

### Sequenza di convogliamento diretto

`CMD.start_convey` in IDLE porta direttamente a SEALING (saltando FILLING e CLEANING) per convogliare materiale già presente nel vessel.

### Comportamento in FAULT

In FAULT: XV02 (sfiato) aperto per sicurezza passiva; bilancia fermata e resettata. `CMD.ack` con `NOT internal_error` riporta a NORMAL/IDLE.

---

## Allarmi

| ID | Condizione specifica |
|----|----------------------|
| [`TR-E01`](../index.md#allarmi-dei-propulsori) | `ALARMS.pressurization_timeout` — verificare supply aria, XV04, PT01/02 |
| [`TR-E02`](../index.md#allarmi-dei-propulsori) | `ALARMS.depressurization_timeout` — verificare XV02, PT01/02 |
| [`TR-E03`](../index.md#allarmi-dei-propulsori) | Guasto su una valvola interna (`XV01`–`XV05`) — vedere gli [allarmi delle valvole](../../valves/index.md#allarmi-delle-valvole) |
| [`TR-E04`](../index.md#allarmi-dei-propulsori) | Timeout Loading o Unloading su `WT01` — vedere gli [allarmi delle celle di carico](../../load-cells/index.md#allarmi-delle-celle-di-carico) |
| [`TR-E05`](../index.md#allarmi-dei-propulsori) | `NOT PSL` — pressione di sicurezza persa |
| [`TR-E06`](../index.md#allarmi-dei-propulsori) | `LSH` — livello alto nel vessel |

---

## Parametri

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `SETTING.cleaning_timer` | T#2M | Durata fase CLEANING |
| `SETTING.pressurizing_timeout` | T#1M | Timeout massimo fase PRESSURIZING |
| `SETTING.depressurizing_timeout` | T#1M | Timeout massimo fase DEPRESSURIZING |
| `SETTING.pressure_delta` | 0.2 | Sovrapressione minima vessel-linea [bar] |
| `SETTING.vessel_empty_thresh` | 0.2 | Soglia PT01 per `depressurized` [bar] |
| `SETTING.line_empty_thresh` | 0.2 | Soglia PT02 per `depressurized` [bar] |
| `SETTING.actuator_timeout` | T#2s | Timeout propagato a tutte le valvole XV01–05 |

---

## Struttura dati

```mermaid
classDiagram
    class UDT_Sealed_inlet_Transporter
    class DEVICES {
        +UDT_SS_Sealed_Valve XV01
        +UDT_DS_Valve XV02
        +UDT_SS_Valve XV03
        +UDT_SS_Valve XV04
        +UDT_SS_Valve XV05
        +UDT_Solenoid_valve XY
        +UDT_Load_cells WT01
        +UDT_Analogic_signal PT01
        +UDT_Analogic_signal PT02
        +Bool PSL
        +Bool LSH
    }
    class CMD {
        +Bool ack
        +Bool start_loading
        +Bool start_convey
        +Bool stop
    }
    class SETTING {
        +Time cleaning_timer
        +Time pressurizing_timeout
        +Time depressurizing_timeout
        +Time actuator_timeout
        +Real pressure_delta
        +Real vessel_empty_thresh
        +Real line_empty_thresh
    }
    class STATUS {
        +Int state
        +Int normal_state
        +Bool is_fault
        +Bool is_idle
        +Bool is_filling
        +Bool is_cleaning
        +Bool is_sealing
        +Bool is_pressurizing
        +Bool is_conveying
        +Bool is_depressurizing
    }
    class ALARMS {
        +Bool pressurization_timeout
        +Bool depressurization_timeout
    }
    class OUT {
        +Bool loading_finished
        +Bool conveying_done
        +Bool filter_cleaner_command
        +Real last_transferred
    }
    UDT_Sealed_inlet_Transporter *-- DEVICES
    UDT_Sealed_inlet_Transporter *-- CMD
    UDT_Sealed_inlet_Transporter *-- SETTING
    UDT_Sealed_inlet_Transporter *-- STATUS
    UDT_Sealed_inlet_Transporter *-- ALARMS
    UDT_Sealed_inlet_Transporter *-- OUT
```

---

## Macchina a stati (FSM)

```mermaid
stateDiagram-v2
    [*] --> NORMAL
    NORMAL --> FAULT : internal_error OR pressurization_timeout OR depressurization_timeout
    FAULT --> NORMAL : CMD.ack AND NOT internal_error → IDLE

    state NORMAL {
        [*] --> IDLE
        IDLE --> FILLING : CMD.start_loading
        IDLE --> SEALING : CMD.start_convey
        FILLING --> CLEANING : loading_finished
        FILLING --> IDLE : CMD.stop
        CLEANING --> SEALING : cleaning_timer scaduto
        CLEANING --> IDLE : CMD.stop
        SEALING --> PRESSURIZING : all_loading_closed
        PRESSURIZING --> CONVEYING : pressure_gate_met
        PRESSURIZING --> DEPRESSURIZING : CMD.stop
        CONVEYING --> DEPRESSURIZING : unloading_finished OR is_paused OR CMD.stop
        DEPRESSURIZING --> IDLE : depressurized
    }
```

### Tabella uscite per stato operativo

| Stato | XV01 | XV02 | XV03 | XV04 | XV05 | XY | WT01 | OUT.filter_cleaner |
|-------|------|------|------|------|------|----|------|--------------------|
| IDLE | — | aperta | — | — | — | — | — | FALSE |
| FILLING | aperta | aperta | aperta | — | — | — | Loading | FALSE |
| CLEANING | — | — | — | — | — | — | — | TRUE |
| SEALING | — | — | — | — | — | — | — | FALSE |
| PRESSURIZING | — | — | — | aperta | — | eccitato | — | FALSE |
| CONVEYING | — | — | — | aperta | aperta | eccitato | Unloading | FALSE |
| DEPRESSURIZING | — | aperta | — | — | — | — | — | FALSE |
| FAULT | — | aperta | — | — | — | — | stop+reset | FALSE |

Le valvole non elencate per uno stato sono chiuse (CMD.auto = FALSE). XV01–05 e XY hanno il proprio controller sub-FB sempre in esecuzione; il wrapper scrive solo `CMD.auto`.
