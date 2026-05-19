# Filter Cleaner — 1 Sleeve

## Overview

The 1-sleeve filter cleaner drives periodic compressed air pulses through a single solenoid valve (`XY`) to dislodge accumulated dust from a filter sleeve. The cleaning cycle runs automatically as long as the enable command is active, alternating between an active pulse and a waiting interval. There is no position feedback — the system is open-loop.

---

## Main Components

- **Filter housing** — contains the filter sleeve (sock, cartridge, or screen)
- **Compressed air supply / accumulator** — provides pulse pressure
- **Solenoid valve `XY`** — releases each air pulse into the sleeve

---

## I/O Signals

| Signal | Type | Description |
|--------|------|-------------|
| `XY` | Output — Bool | Solenoid command: TRUE = pulse active (air released into sleeve) |

---

## Operating Routine

When the enable command is received (`auto = TRUE` or `manual = TRUE` in manual mode), the system immediately begins pulsing. Each cycle:

1. **ACTIVE** — `XY` energized for `pulse_duration` (air blast into sleeve)
2. **WAITING** — `XY` de-energized for `interval_duration` (sleeve recovers, tank re-pressurizes)
3. Repeat until command is removed

Removing the command at any point returns the system to **IDLE** (`XY = FALSE`) at the end of the current phase. If `interlocked = TRUE`, the validated command freezes and pulsing pauses.

---

## Alarms

No alarms — no feedback sensors.

---

## Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `pulse_duration` | T#500ms | Duration of each air pulse (solenoid energized) |
| `interval_duration` | T#3s | Wait time between pulses |

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
        +Bool interlocked
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

## State Machine

```mermaid
stateDiagram-v2
	
	state FILTER{
    [*] --> IDLE

    IDLE --> ACTIVE: enabled = TRUE
    
    state ACTIVE{
    
    [*] --> PULSING
    
	    PULSING --> WAITING: pulse_timer complete
	    
	    WAITING --> PULSING: interval_timer complete
    
    }
    ACTIVE --> IDLE: enabled = FALSE
	}
```

### State and Output Table

| `state` | `active_state` | `XY` | Description |
|---------|---------------|------|-------------|
| IDLE (1) | — | FALSE | Standby, no cleaning |
| ACTIVE (2) | PULSING (1) | TRUE | Pulse active — air blast into sleeve |
| ACTIVE (2) | WAITING (2) | FALSE | Between pulses — interval timer running |

### State Transition Table

| Current State | Condition | Next State | Action |
|---------------|-----------|------------|--------|
| IDLE | enable command | ACTIVE | `XY` → TRUE; start pulse timer |
| ACTIVE | Pulse timer done | WAITING | `XY` → FALSE; start interval timer |
| ACTIVE | Command removed | IDLE | `XY` → FALSE |
| WAITING | Interval timer done AND command active | ACTIVE | `XY` → TRUE; start pulse timer |
| WAITING | Command removed | IDLE | — |
| WAITING | Interval timer done AND command inactive | IDLE | — |
