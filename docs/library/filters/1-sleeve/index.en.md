# Filter Cleaner — 1 Sleeve

## Overview

**Tier 2.** The 1-sleeve filter cleaner drives periodic compressed air pulses through a single Solenoid Valve (Tier 1, `XY`) to dislodge accumulated dust from a filter sleeve. When enabled, the cycle always begins with a waiting interval (`interval_duration`) before the first pulse, then alternates waiting and pulsing indefinitely. There is no position feedback — the system is open-loop.

---

## Composition

| Tag | Type | Role |
|-----|------|------|
| `XY` | Solenoid Valve (Tier 1) | Cleaning pulse |

---

## Control Signals

| Signal | Type | Description |
|--------|------|-------------|
| `DEVICES.XY` | UDT_Solenoid_valve | OUTPUT — Cleaning pulse solenoid |
| `CMD.manual_mode` | Bool | COMMAND — TRUE = manual mode |
| `CMD.manual` | Bool | COMMAND — Enable in manual mode |
| `CMD.auto` | Bool | COMMAND — Enable in automatic mode (ReadOnly external) |
| `STATUS.state` | Int | STATE — 1=Idle, 2=Active |
| `STATUS.active_state` | Int | SUB-STATE — 1=Pulsing, 2=Waiting |
| `STATUS.is_idle` | Bool | STATE — Filter waiting for enable command |
| `STATUS.is_active` | Bool | STATE — Cleaning cycle running |

---

## Operating Routine

**IDLE** — Filter inactive. `XY` de-energised. When an enable command arrives (manual or auto), state transitions to ACTIVE with `active_state = WAITING`.

**ACTIVE / WAITING** — Filter active but resting between pulses. `XY` de-energised. Interval timer (`interval_duration`) running. When the timer expires, internal state transitions to PULSING.

**ACTIVE / PULSING** — `XY` energised for the duration of the pulse (`pulse_duration`). When the pulse timer expires, internal state returns to WAITING.

The WAITING → PULSING → WAITING cycle repeats as long as the enable command remains active. Removing the enable command at any point returns the filter to IDLE.

In **manual mode** (`manual_mode = TRUE`), the command comes from `CMD.manual`. In **automatic mode**, from `CMD.auto`.

---

## Alarms

This module raises no alarms of its own — `UDT_Filter_1_sleeve` has no `ALARMS` struct.

---

## Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `pulse_duration` | T#500ms | Duration of each cleaning pulse |
| `interval_duration` | T#3s | Rest time between successive pulses |

---

## Data Structure

```mermaid
classDiagram
    class UDT_Filter_1_sleeve
    class DEVICES {
        +UDT_Solenoid_valve XY
    }
    class CMD {
        +Bool manual_mode
        +Bool manual
        +Bool auto
    }
    class SETTING {
        +Time pulse_duration
        +Time interval_duration
    }
    class STATUS {
        +Int state
        +Int active_state
        +Bool is_idle
        +Bool is_active
    }
    UDT_Filter_1_sleeve *-- DEVICES
    UDT_Filter_1_sleeve *-- CMD
    UDT_Filter_1_sleeve *-- SETTING
    UDT_Filter_1_sleeve *-- STATUS
```

---

## State Machine (FSM)

```mermaid
stateDiagram-v2
    [*] --> IDLE

    IDLE --> ACTIVE : enable command
    ACTIVE --> IDLE : disable command

    state ACTIVE {
        [*] --> WAITING
        WAITING --> PULSING : interval_timer expired
        PULSING --> WAITING : pulse_timer expired
    }
```

### State and Output Table

| State | Sub-state | XY.CMD.auto | Description |
|-------|-----------|-------------|-------------|
| IDLE | — | FALSE | Filter inactive |
| ACTIVE | WAITING | FALSE | Resting between pulses; interval_timer running |
| ACTIVE | PULSING | TRUE | Cleaning pulse active; pulse_timer running |

### State Transition Table

| State | Condition | Next state | Action |
|-------|-----------|------------|--------|
| IDLE | Enable command | ACTIVE / WAITING | Start interval_timer |
| ACTIVE | Disable command | IDLE | Stop timers, XY → FALSE |
| ACTIVE / WAITING | interval_timer.Q | ACTIVE / PULSING | XY → TRUE; start pulse_timer |
| ACTIVE / PULSING | pulse_timer.Q | ACTIVE / WAITING | XY → FALSE; start interval_timer |
