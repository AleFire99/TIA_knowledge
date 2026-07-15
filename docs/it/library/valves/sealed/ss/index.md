# Valvola Sigillata — Monosolenoide (SS Sealed)

## Panoramica

**Tier 3 — composito.** `SS_Sealed_valve` avvolge un'istanza di Valvola a Farfalla SS (Tier 2) aggiungendo un'elettrovalvola di sigillo dedicata (`XY_seal`, Tier 1). Il sigillo viene eccitato automaticamente quando la valvola interna è confermata `CLOSED`, garantendo tenuta pneumatica in stato di riposo; si diseccita non appena la valvola inizia ad aprirsi.

Il blocco delega interamente la logica di apertura/chiusura, il rilevamento allarmi e la macchina a stati all'istanza interna `XV`; non possiede una propria FSM né un proprio `ALARMS` — `STATUS` è una copia diretta di `XV.STATUS` ad ogni scan.

---

## Composizione

| Tag | Tipo | Ruolo |
|-----|------|-------|
| `XV` | Valvola a Farfalla SS (Tier 2) | Valvola principale — vedere [Valvola a Farfalla SS](../../butterfly/single_solenoid/index.md) |
| `XY_seal` | Elettrovalvola (Tier 1) | Elettrovalvola di tenuta — eccitata ↔ `XV` in `CLOSED` |

---

## Segnali di controllo

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `DEVICES.XV` | UDT_SS_Valve | Valvola a farfalla SS interna |
| `DEVICES.XY_seal` | UDT_Solenoid_valve | Elettrovalvola di sigillo |
| `CMD.manual_mode` | Bool | TRUE = modalità manuale HMI |
| `CMD.manual` | Bool | Comando di apertura in modalità manuale |
| `CMD.auto` | Bool | Comando di apertura dall'automazione (ReadOnly external) |
| `CMD.ack` | Bool | Conferma allarmi — inoltrato a `XV.CMD.ack` |
| `STATUS.*` | — | Copia diretta di `XV.STATUS.*` (state, normal_state, is_fault, is_closed, is_opening, is_open, is_closing) |

---

## Parametri di regolazione

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `SETTING.actuator_timeout` | T#2s | Inoltrato a `XV.SETTING.actuator_timeout` ad ogni scan |

---

## Funzionamento

Il comando desiderato è risolto dal wrapper e scritto in `XV.CMD.auto`:

```
XV.CMD.auto := manual_mode ? manual : auto
```

Il sigillo segue una singola regola:

```
XY_seal.CMD.auto := XV.STATUS.is_closed
```

---

## Stati e output

| Stato (da `XV`) | `XY_seal` |
|------------------|-----------|
| CLOSED | TRUE (sigillato) |
| OPENING / OPEN / CLOSING | FALSE |
| FAULT | FALSE |

---

## Diagramma di stato

La FSM è interamente gestita dall'istanza interna `XV` — vedere [Valvola a Farfalla SS](../../butterfly/single_solenoid/index.md#diagramma-di-stato). Questo blocco aggiunge solo la logica del sigillo, senza stati propri.

---

## Allarmi

Nessun allarme proprio — questo blocco non possiede un proprio `ALARMS`. Gli allarmi restano visibili esclusivamente tramite l'istanza interna: vedere [allarmi Valvola a Farfalla SS](../../butterfly/single_solenoid/index.md#allarmi).

---

## Struttura dati

```mermaid
classDiagram
    class UDT_SS_Sealed_Valve
    class DEVICES {
        +UDT_SS_Valve XV
        +UDT_Solenoid_valve XY_seal
    }
    class CMD {
        +Bool manual_mode
        +Bool manual
        +Bool auto
        +Bool ack
    }
    class SETTING {
        +Time actuator_timeout
    }
    class STATUS {
        +Int state
        +Int normal_state
        +Bool is_fault
        +Bool is_closed
        +Bool is_opening
        +Bool is_open
        +Bool is_closing
    }
    UDT_SS_Sealed_Valve *-- DEVICES
    UDT_SS_Sealed_Valve *-- CMD
    UDT_SS_Sealed_Valve *-- SETTING
    UDT_SS_Sealed_Valve *-- STATUS
```

Nessuna classe `ALARMS` — a differenza di altri dispositivi compositi, questo UDT non ne ha nemmeno una a specchio: gli allarmi restano leggibili solo su `DEVICES.XV.ALARMS`.
