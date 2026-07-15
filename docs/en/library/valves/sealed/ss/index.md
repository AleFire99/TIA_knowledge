# Sealed Valve — Single Solenoid (SS Sealed)

## Overview

**Tier 3 — composite.** `SS_Sealed_valve` wraps an SS Butterfly Valve (Tier 2) instance, adding a dedicated seal solenoid (`XY_seal`, Tier 1). The seal is energized automatically whenever the internal valve is confirmed `CLOSED`, ensuring pneumatic sealing at rest; it de-energizes as soon as the valve begins to open.

The block delegates all opening/closing logic, alarm detection, and the state machine to the internal `XV` instance; it has no FSM or `ALARMS` of its own — `STATUS` is a direct copy of `XV.STATUS` every scan.

---

## Composition

| Tag | Type | Role |
|-----|------|------|
| `XV` | SS Butterfly Valve (Tier 2) | Main valve — see [SS Butterfly Valve](../../butterfly/single_solenoid/index.md) |
| `XY_seal` | Solenoid Valve (Tier 1) | Seal solenoid — energized ↔ `XV` in `CLOSED` |

---

## Control Signals

| Signal | Type | Description |
|--------|------|-------------|
| `DEVICES.XV` | UDT_SS_Valve | Internal SS butterfly valve |
| `DEVICES.XY_seal` | UDT_Solenoid_valve | Seal solenoid |
| `CMD.manual_mode` | Bool | TRUE = HMI manual mode |
| `CMD.manual` | Bool | Open command in manual mode |
| `CMD.auto` | Bool | Open command from automation (ReadOnly external) |
| `CMD.ack` | Bool | Acknowledges alarms — forwarded to `XV.CMD.ack` |
| `STATUS.*` | — | Direct copy of `XV.STATUS.*` (state, normal_state, is_fault, is_closed, is_opening, is_open, is_closing) |

---

## Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SETTING.actuator_timeout` | T#2s | Forwarded to `XV.SETTING.actuator_timeout` every scan |

---

## Operating Routine

The desired command is resolved by the wrapper and written to `XV.CMD.auto`:

```
XV.CMD.auto := manual_mode ? manual : auto
```

The seal follows a single rule:

```
XY_seal.CMD.auto := XV.STATUS.is_closed
```

---

## States and Outputs

| State (from `XV`) | `XY_seal` |
|--------------------|-----------|
| CLOSED | TRUE (sealed) |
| OPENING / OPEN / CLOSING | FALSE |
| FAULT | FALSE |

---

## State Machine

The FSM is entirely managed by the internal `XV` instance — see [SS Butterfly Valve](../../butterfly/single_solenoid/index.md#state-machine). This block adds only the seal logic, with no states of its own.

---

## Alarms

No alarms of its own — this block has no `ALARMS` of its own. Alarms remain visible only through the internal instance: see [SS Butterfly Valve alarms](../../butterfly/single_solenoid/index.md#alarms).

---

## Data Structure

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

No `ALARMS` class — unlike other composite devices, this UDT doesn't even mirror one: alarms remain readable only via `DEVICES.XV.ALARMS`.
