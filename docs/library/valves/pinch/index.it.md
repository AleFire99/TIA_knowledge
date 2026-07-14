# Valvola a Manicotto

## Panoramica

**Tier 2.** La valvola a manicotto controlla il flusso comprimendo meccanicamente un tubo flessibile. L'eccitazione del solenoide interno (`XY`) aziona l'attuatore pneumatico che schiaccia il tubo chiudendolo; la diseccitazione rilascia il tubo ripristinando il flusso. Un pressostato (`PSL`) conferma la posizione chiusa — è l'unico sensore di posizione del dispositivo. La valvola è normalmente aperta: richiede eccitazione attiva per rimanere chiusa.

---

## Composizione

| Tag | Tipo | Ruolo |
|-----|------|-------|
| `XY` | Valvola a Solenoide (Tier 1) | Attuatore — eccitato = chiuso |

L'arbitraggio manuale/automatico (`manual_mode`/`manual`/`auto`) segue lo stesso schema descritto in [Valvola a Solenoide](../solenoid/index.it.md).

---

## Segnali di controllo

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `DEVICES.PSL` | Bool | INPUT — Pressostato: TRUE = valvola chiusa (tubo schiacciato) |
| `DEVICES.XY` | UDT_Solenoid_valve | OUTPUT — Elettrovalvola attuatore |
| `CMD.manual_mode` | Bool | TRUE = modalità manuale HMI |
| `CMD.manual` | Bool | Comando di chiusura in modalità manuale |
| `CMD.auto` | Bool | Comando di chiusura dall'automazione (ReadOnly external) |
| `CMD.ack` | Bool | Conferma allarmi e ripristino da FAULT |

---

## Parametri di regolazione

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `SETTING.actuator_timeout` | T#2s | Tempo massimo consentito per completare una manovra di apertura o chiusura |

---

## Stati e output

| Stato | `XY` | `PSL` atteso | Descrizione |
|-------|------|-------------|-------------|
| CLOSED | TRUE | TRUE | Tubo schiacciato, flusso bloccato |
| OPENING | FALSE | (in transizione) | Attuatore rilascia il tubo |
| OPEN | FALSE | FALSE | Tubo libero, flusso consentito |
| CLOSING | TRUE | (in transizione) | Attuatore schiaccia il tubo |
| FAULT | — | — | Uscite congelate; richiede conferma operatore |

---

## Diagramma di stato

```mermaid
stateDiagram-v2
state PINCH_VALVE{
    [*] --> NORMAL

    NORMAL --> FAULT : internal_error
    FAULT --> NORMAL : ack & !internal_error

    state NORMAL {
        [*] --> CLOSED : PSL
        [*] --> OPEN : !PSL

        CLOSED --> OPENING : desired_open_command
        OPENING --> OPEN : !PSL
        OPEN --> CLOSING : !desired_open_command
        CLOSING --> CLOSED : PSL
    }
}
```

```Pascal
internal_error := sensor_mismatch OR failed_to_close OR failed_to_open;
```

Al rientro da `FAULT`, il blocco rilegge `PSL` per determinare lo stato stabile (`CLOSED` se TRUE, altrimenti `OPEN`) — stesso meccanismo del primo scan.

---

## Allarmi

| ID | Condizione specifica |
|----|----------------------|
| [`XV-E01`](../index.it.md#allarmi-delle-valvole) | Stato stabile corrente (CLOSED/OPEN) non confermato da `PSL` |
| [`XV-E03`](../index.it.md#allarmi-delle-valvole) | `CLOSING` non confermato entro `actuator_timeout` |
| [`XV-E04`](../index.it.md#allarmi-delle-valvole) | `OPENING` non confermato entro `actuator_timeout` |

Non applicabile: `XV-E02` (conflitto sensori) — il Manicotto ha un solo sensore di posizione.

---

## Struttura dati

```mermaid
classDiagram
    class UDT_Pinch_Valve
    class DEVICES {
        +Bool PSL
        +UDT_Solenoid_valve XY
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
    class ALARMS {
        +Bool sensor_mismatch
        +Bool failed_to_close
        +Bool failed_to_open
    }
    UDT_Pinch_Valve *-- DEVICES
    UDT_Pinch_Valve *-- CMD
    UDT_Pinch_Valve *-- SETTING
    UDT_Pinch_Valve *-- STATUS
    UDT_Pinch_Valve *-- ALARMS
```

`internal_error` è interno al blocco funzionale, non esposto tramite l'UDT.
