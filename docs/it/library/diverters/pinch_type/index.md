# Deviatore a Manicotto

## Panoramica

**Tier 3 — composito.** Il deviatore a manicotto indirizza il flusso di materiale tra due linee (A e B) incorporando due istanze di Valvola a Manicotto (Tier 2), `XVA` e `XVB`. Solo una linea è aperta alla volta. Non ci sono sensori fisici propri del deviatore — lo stato di instradamento è interamente derivato dal feedback di posizione delle due sotto-valvole.

---

## Composizione

| Tag | Tipo | Ruolo |
|-----|------|-------|
| `XVA` | Valvola a Manicotto (Tier 2) | Verso il percorso A |
| `XVB` | Valvola a Manicotto (Tier 2) | Verso il percorso B |

Un'unica decisione manuale/automatica (`manual_mode`/`manual`/`auto`, risolta in `desired_route_B`: FALSE = instradamento su A, TRUE = instradamento su B) stabilisce quale valvola va aperta; l'altra è sempre comandata chiusa — le due istanze non arbitrano mai in autonomia. Vedere [Valvola a Manicotto](../../valves/pinch/index.md) per il dettaglio delle sotto-valvole.

---

## Segnali di controllo

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `DEVICES.XVA` | UDT_Pinch_Valve | Sotto-valvola verso il percorso A |
| `DEVICES.XVB` | UDT_Pinch_Valve | Sotto-valvola verso il percorso B |
| `CMD.manual_mode` | Bool | TRUE = modalità manuale HMI |
| `CMD.manual` | Bool | Selezione percorso in modalità manuale (TRUE = percorso B) |
| `CMD.auto` | Bool | Selezione percorso dall'automazione (ReadOnly external) |
| `CMD.ack` | Bool | Conferma allarmi — inoltrato a entrambe le sotto-valvole |

`CMD.ack` viene propagato sia a `XVA.CMD.ack` sia a `XVB.CMD.ack` ad ogni scan.

---

## Parametri di regolazione

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `SETTING.actuator_timeout` | T#2s | Inoltrato a `XVA.SETTING.actuator_timeout` e `XVB.SETTING.actuator_timeout` |

---

## Stati e output

| Stato | `XVA` (comandata) | `XVB` (comandata) | Descrizione |
|-------|--------------------|--------------------|-------------|
| ROUTE_A | aperta | chiusa | Instradamento su A stabilito |
| A_TO_B | chiusa | aperta | Transizione da A verso B |
| ROUTE_B | chiusa | aperta | Instradamento su B stabilito |
| B_TO_A | aperta | chiusa | Transizione da B verso A |
| FAULT | chiusa | chiusa | Guasto; nessun comando esplicito di apertura su nessuna delle due (fail-safe) |

---

## Diagramma di stato

```mermaid
stateDiagram-v2
state DIVERTER{
    [*] --> NORMAL : XVA aperta, XVB chiusa (o viceversa) al primo scan
    [*] --> FAULT : posizioni ambigue al primo scan

    NORMAL --> FAULT : internal_error
    FAULT --> NORMAL : ack & !internal_error

    state NORMAL {
        [*] --> ROUTE_A : XVA.is_open
        [*] --> ROUTE_B : XVB.is_open

        ROUTE_A --> A_TO_B : desired_route_B
        A_TO_B --> ROUTE_B : XVA.is_closed & XVB.is_open

        ROUTE_B --> B_TO_A : !desired_route_B
        B_TO_A --> ROUTE_A : XVA.is_open & XVB.is_closed
    }
}
```

```Pascal
internal_error := valve_mismatch OR XVA.is_fault OR XVB.is_fault;
```

Al rientro da `FAULT`, il blocco rilegge lo stato delle due sotto-valvole per determinare il percorso stabile — stesso meccanismo del primo scan.

---

## Allarmi

| ID | Condizione specifica |
|----|----------------------|
| [`DIV-E01`](../index.md#allarmi-dei-deviatori) | Stato stabile corrente (`ROUTE_A`/`ROUTE_B`) non confermato da `XVA.STATUS.is_open`/`XVB.STATUS.is_open` |

Il guasto di `XVA` o `XVB` concorre a `internal_error` (transizione a `FAULT`) ma non genera un proprio ID a questo livello — vedere [allarmi Valvola a Manicotto](../../valves/pinch/index.md#allarmi).

---

## Struttura dati

```mermaid
classDiagram
    class UDT_Pinch_diverter
    class DEVICES {
        +UDT_Pinch_Valve XVA
        +UDT_Pinch_Valve XVB
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
        +Bool is_in_A
        +Bool is_moving_to_B
        +Bool is_in_B
        +Bool is_moving_to_A
        +Bool is_fault
    }
    class ALARMS {
        +Bool valve_mismatch
    }
    UDT_Pinch_diverter *-- DEVICES
    UDT_Pinch_diverter *-- CMD
    UDT_Pinch_diverter *-- SETTING
    UDT_Pinch_diverter *-- STATUS
    UDT_Pinch_diverter *-- ALARMS
```

`internal_error` è interno al blocco funzionale, non esposto tramite l'UDT.
