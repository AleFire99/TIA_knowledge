# Ciclo di Carico e Scarico

## Panoramica

**Livello 1.** Non incorpora sotto-istanze — a differenza degli altri moduli Livello 1 di questa libreria (l'Elettrovalvola, atomica), `UDT_Load_cells` è la struttura dati condivisa tra due blocchi funzionali indipendenti — `Loading` e `Unloading` — ciascuno con la propria macchina a stati, memorizzata rispettivamente in `STATUS.LOADING` e `STATUS.UNLOADING` della stessa istanza UDT. `Loading` gestisce il riempimento di un contenitore a peso; `Unloading` gestisce lo svuotamento con possibilità di pausa e ripresa.

Il campo `IN` di questa struttura (`current_weight`, `scale_error`, `plant_error`) è la superficie generica su cui scrive qualsiasi interfaccia trasmettitore collegata — vedere [Celle di Carico](../index.md) per come funziona il disaccoppiamento tra questo blocco e il trasmettitore fisico effettivo.

---

## Interfaccia

### Struttura dati

```mermaid
classDiagram
    class UDT_Load_cells
    class CMD {
        +Bool ack
        +Real loading_setpoint
        +Real unloading_setpoint
        +Bool tare_request
        +Bool loading_start
        +Bool unloading_start
        +Bool stop
        +Bool reset
    }
    class IN {
        -Real current_weight
        -Bool scale_error
        -Bool plant_error
    }
    class SETTING {
        +Real min_weight
        +Real max_weight
        +Real loading_tail
        +Real unloading_tail
        +Time loading_timeout
        +Time unloading_timeout
    }
    class STATUS_LOADING {
        -Int state
        -Int normal_state
        -Bool is_idle
        -Bool is_loading
        -Bool is_fault
        -Bool loading_finished
    }
    class STATUS_UNLOADING {
        -Int state
        -Bool is_idle
        -Bool is_unloading
        -Bool is_paused
        -Bool is_fault
        -Bool unloading_finished
    }
    class BATCH {
        -Real transferred
        -Real weight_at_start
    }
    class ALARMS {
        -Bool weight_invalid
        -Bool loading_timeout
        -Bool unloading_timeout
    }
    UDT_Load_cells *-- CMD
    UDT_Load_cells *-- IN
    UDT_Load_cells *-- SETTING
    UDT_Load_cells *-- STATUS_LOADING
    UDT_Load_cells *-- STATUS_UNLOADING
    UDT_Load_cells *-- BATCH
    UDT_Load_cells *-- ALARMS
```

`+` = scrivibile da DCS/HMI, `-` = sola lettura. `IN` è scritto dall'interfaccia trasmettitore collegata (es. [Interfaccia Pavone DAT 1400](../pavone-dat-1400/index.md)), non da DCS/HMI direttamente.

### Segnali di controllo

| Segnale | Tipo | Direzione | Descrizione |
|---------|------|-----------|-------------|
| `CMD.ack` | Bool | IN | Conferma per stato FAULT (Loading o Unloading) |
| `CMD.loading_setpoint` | Real | IN | Peso di riferimento per il carico [kg] |
| `CMD.unloading_setpoint` | Real | IN | Peso da scaricare nel ciclo [kg] |
| `CMD.tare_request` | Bool | IN | Richiesta tara, letta dall'interfaccia trasmettitore collegata |
| `CMD.loading_start` | Bool | IN | Avvio ciclo di carico |
| `CMD.unloading_start` | Bool | IN | Avvio o ripresa ciclo di scarico |
| `CMD.stop` | Bool | IN | Arresto del ciclo attivo |
| `CMD.reset` | Bool | IN | Ritorno a IDLE da PAUSED (solo Unloading) |
| `IN.current_weight` | Real | IN | Peso corrente [kg] |
| `IN.scale_error` | Bool | IN | Guasto hardware trasmettitore |
| `IN.plant_error` | Bool | IN | Errore di impianto esterno (es. perdita materiale) |
| `STATUS.LOADING.state` | Int | OUT | 0=FAULT, 1=NORMAL |
| `STATUS.LOADING.normal_state` | Int | OUT | 1=IDLE, 2=LOADING (valido solo in NORMAL) |
| `STATUS.LOADING.is_idle` | Bool | OUT | TRUE in NORMAL/IDLE |
| `STATUS.LOADING.is_loading` | Bool | OUT | TRUE in NORMAL/LOADING |
| `STATUS.LOADING.is_fault` | Bool | OUT | TRUE in FAULT |
| `STATUS.LOADING.loading_finished` | Bool | OUT | Impulso 1-scan all'ingresso in IDLE dopo un carico completato |
| `STATUS.UNLOADING.state` | Int | OUT | 0=FAULT, 1=IDLE, 2=UNLOADING, 3=PAUSED |
| `STATUS.UNLOADING.is_idle` | Bool | OUT | TRUE in IDLE |
| `STATUS.UNLOADING.is_unloading` | Bool | OUT | TRUE durante il convogliamento (UNLOADING) |
| `STATUS.UNLOADING.is_paused` | Bool | OUT | TRUE in PAUSED |
| `STATUS.UNLOADING.is_fault` | Bool | OUT | TRUE in FAULT |
| `STATUS.UNLOADING.unloading_finished` | Bool | OUT | Impulso 1-scan all'ingresso in IDLE dopo scarico completato |
| `BATCH.transferred` | Real | OUT | Quantità elaborata nel ciclo corrente [kg] |
| `BATCH.weight_at_start` | Real | OUT | Peso acquisito all'ingresso della fase attiva [kg] |
| `ALARMS.weight_invalid` | Bool | OUT | Peso fuori scala: `current_weight < min_weight OR current_weight > max_weight` — stessa condizione per Loading e Unloading |
| `ALARMS.loading_timeout` | Bool | OUT | Rispecchia `internal_error` di Loading (timeout carico, guasto trasmettitore o errore di impianto) |
| `ALARMS.unloading_timeout` | Bool | OUT | Rispecchia `internal_error` di Unloading (timeout scarico, guasto trasmettitore o errore di impianto) |

### Parametri

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `SETTING.min_weight` | 0.0 | Soglia inferiore peso valido [kg] (usata anche per la transizione UNLOADING → PAUSED) |
| `SETTING.max_weight` | 1000.0 | Soglia superiore peso valido [kg] |
| `SETTING.loading_tail` | — | Anticipazione fine carico rispetto al setpoint [kg] |
| `SETTING.unloading_tail` | — | Anticipazione fine scarico rispetto al setpoint [kg] |
| `SETTING.loading_timeout` | T#10M | Durata massima ciclo LOADING prima di FAULT |
| `SETTING.unloading_timeout` | T#10M | Durata massima ciclo UNLOADING prima di FAULT |

---

## Comportamento

### Funzionamento

#### FB Loading

**NORMAL/IDLE** — Attende `CMD.loading_start` con peso valido (`NOT weight_invalid`). All'ingresso in IDLE: `BATCH.transferred := 0`, impulso `loading_finished`.

**NORMAL/LOADING** — Calcola ogni scan: `BATCH.transferred := current_weight − weight_at_start` (clampato a 0). Torna a IDLE quando `CMD.stop OR (current_weight ≥ loading_setpoint − loading_tail)`. `weight_at_start` viene acquisito all'ingresso in LOADING.

**FAULT** — Si entra da NORMAL quando `internal_error := loading_timer.Q OR IN.scale_error OR IN.plant_error`. `CMD.ack AND NOT internal_error` riporta a NORMAL, ripartendo da IDLE.

#### FB Unloading

**IDLE** — Attende `CMD.unloading_start` con peso valido. All'ingresso in IDLE: `BATCH.transferred := 0`, impulso `unloading_finished`.

**UNLOADING** — Calcola ogni scan: `BATCH.transferred := weight_at_start − current_weight` (clampato a 0). Priorità delle uscite, in ordine: `internal_error` → FAULT; altrimenti `CMD.stop OR current_weight ≤ min_weight` → PAUSED; altrimenti `transferred ≥ unloading_setpoint − unloading_tail` → IDLE.

Alla ripresa (PAUSED → UNLOADING): `weight_at_start := current_weight + transferred` — l'ancora viene ricalcolata così il contatore `transferred` prosegue senza scatti.

**PAUSED** — `BATCH.transferred` congelato. `CMD.unloading_start` riprende (→ UNLOADING); `CMD.reset` torna a IDLE.

**FAULT** — `internal_error := unloading_timer.Q OR IN.scale_error OR IN.plant_error`. `CMD.ack` passa a PAUSED (non direttamente a IDLE).

### Allarmi

- [`LC-W01`](../index.md#allarmi-delle-celle-di-carico) — `weight_invalid`, condiviso da Loading e Unloading; impedisce l'avvio di un nuovo ciclo in entrambi i blocchi. Verificare celle, cablaggio e trasmettitore
- [`LC-E01`](../index.md#allarmi-delle-celle-di-carico) — ciclo di carico durato oltre `loading_timeout`, o guasto trasmettitore/impianto durante LOADING
- [`LC-E02`](../index.md#allarmi-delle-celle-di-carico) — ciclo di scarico durato oltre `unloading_timeout`, o guasto trasmettitore/impianto durante UNLOADING

### Diagrammi di stato

#### Loading

```mermaid
stateDiagram-v2
state LOADING_FB{
    [*] --> NORMAL

    NORMAL --> FAULT : internal_error
    FAULT --> NORMAL : ack & !internal_error

    state NORMAL {
        [*] --> IDLE
        IDLE --> LOADING : loading_start & !weight_invalid
        LOADING --> IDLE : stop | peso >= setpoint - tail
    }
}
```

| Stato | Descrizione |
|-------|-------------|
| FAULT | `internal_error` attivo; attende `ack` |
| NORMAL/IDLE | In attesa; `transferred=0` all'ingresso |
| NORMAL/LOADING | Carico attivo; `transferred` aggiornato ogni scan |

#### Unloading

```mermaid
stateDiagram-v2
state UNLOADING_FB{
    [*] --> IDLE

    IDLE --> UNLOADING : unloading_start & !weight_invalid
    UNLOADING --> IDLE : transferred >= setpoint - tail
    UNLOADING --> PAUSED : stop | peso <= min_weight
    UNLOADING --> FAULT : internal_error
    PAUSED --> UNLOADING : unloading_start
    PAUSED --> IDLE : reset
    FAULT --> PAUSED : ack
}
```

| Stato | Descrizione |
|-------|-------------|
| FAULT | `internal_error` attivo; `ack` → PAUSED (non IDLE) |
| IDLE | In attesa; `transferred=0` all'ingresso |
| UNLOADING | Scarico attivo; `transferred` aggiornato ogni scan |
| PAUSED | Batch sospeso; `transferred` congelato |

### Timer

#### Loading

| Timer | Stato in cui è attivo | Soglia (parametro) |
|-------|------------------------|---------------------|
| `loading_timer` | NORMAL/LOADING | `SETTING.loading_timeout` |

#### Unloading

| Timer | Stato in cui è attivo | Soglia (parametro) |
|-------|------------------------|---------------------|
| `unloading_timer` | UNLOADING | `SETTING.unloading_timeout` |
