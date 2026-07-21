# Filter Cleaner — 1 Sleeve

## Overview

**Level 2.** The 1-sleeve filter cleaner generates periodic compressed-air pulses through a single Electrovalve (Level 1, `XY`) to remove dust that has accumulated on a filter sleeve. There is no position feedback — the system is open-loop.

No alarms of its own — `UDT_Filter_1_sleeve` does not include an `ALARMS` struct: there is no sensor to base a fault detection on.

---

## Interface

### Composition

| Tag | Type | Role |
|-----|------|------|
| `XY` | Electrovalve (Level 1) | Cleaning pulse |

### Data Structure

```mermaid
classDiagram
    class UDT_Filter_1_sleeve
    class DEVICES {
        -UDT_Solenoid_valve XY
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
        -Bool is_idle
        -Bool is_active
        -Bool is_pulsing
        -Bool is_waiting
    }
    UDT_Filter_1_sleeve *-- DEVICES
    UDT_Filter_1_sleeve *-- CMD
    UDT_Filter_1_sleeve *-- SETTING
    UDT_Filter_1_sleeve *-- STATUS
```

`+` = writable by DCS/HMI, `-` = read-only.

### Control Signals

| Signal | Type | Direction | Description |
|---------|------|-----------|-------------|
| `DEVICES.XY` | UDT_Solenoid_valve | OUT | Cleaning-pulse electrovalve — commanded, its own state is not read back by this block |
| `CMD.manual_mode` | Bool | IN | TRUE = manual mode |
| `CMD.manual` | Bool | IN | Enable in manual mode |
| `CMD.auto` | Bool | IN | Enable in automatic mode |

### Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `pulse_duration` | T#500ms | Duration of each cleaning pulse |
| `interval_duration` | T#3s | Wait time between successive pulses |

---

## Behavior

### Operation

When enabled, the cycle always starts with a wait interval (`interval_duration`) before the first pulse, then alternates between wait and pulse indefinitely.

**IDLE** — The filter is inactive. `XY` is de-energized. When an enable command arrives (manual or automatic), the state transitions to ACTIVE with `active_state = WAITING`.

**ACTIVE / WAITING** — The filter is active but paused between one pulse and the next. `XY` is de-energized. The interval timer (`interval_duration`) is running. On expiry, the internal state moves to PULSING.

**ACTIVE / PULSING** — `XY` is energized for the whole pulse duration (`pulse_duration`). On expiry of the pulse timer, the internal state returns to WAITING.

The WAITING → PULSING → WAITING cycle repeats as long as the command stays active. Disabling the command at any point returns the filter to IDLE.

In **manual mode** (`manual_mode = TRUE`), the command comes from `CMD.manual`. In **automatic mode**, from `CMD.auto`.

### State Diagram

```mermaid
stateDiagram-v2
state FILTER_1_SLEEVE{
    [*] --> IDLE
    IDLE --> ACTIVE : enable command
    ACTIVE --> IDLE : disable command

    state ACTIVE {
        [*] --> WAITING
        WAITING --> PULSING : interval_timer expired
        PULSING --> WAITING : pulse_timer expired
    }
}
```

```Pascal
desired_command := (manual_mode AND manual) OR (NOT manual_mode AND auto);
```

| State | Sub-state | `XY` | Description |
|-------|-------------|------|-------------|
| IDLE | — | FALSE | Filter inactive |
| ACTIVE | WAITING | FALSE | Paused between pulses; `interval_timer` running |
| ACTIVE | PULSING | TRUE | Cleaning pulse active; `pulse_timer` running |

### Timer

| Timer | State in which it is active | Threshold (parameter) |
|-------|------------------------|---------------------|
| `interval_timer` | ACTIVE/WAITING | `SETTING.interval_duration` |
| `pulse_timer` | ACTIVE/PULSING | `SETTING.pulse_duration` |
