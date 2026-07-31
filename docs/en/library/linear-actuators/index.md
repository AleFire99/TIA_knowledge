# Linear Actuators

Pneumatic linear piston, embedding a single Solenoid Valve (Livello 1) as its own actuator. The two variants share the same command scheme (`manual_mode`/`manual`/`auto` resolved every scan toward the embedded solenoid valve) and differ in whether position feedback exists: the "No Sensors" variant transitions immediately on command alone, the "With Sensors" variant confirms every transition through two limit switches (`ZSL`/`ZSH`) and adds a FAULT tier with a movement timeout.

## Linear actuator alarms

Applicable only to the position-feedback variant.

| ID | Title | Condition | Applies to |
|----|-------|-----------|------------|
| `AL-E01` | Sensor mismatch | Current stable state (RETRACTED/EXTENDED) not confirmed by the expected limit switch | Piston — With Sensors |
| `AL-E02` | Sensor conflict | `ZSL` and `ZSH` both TRUE at the same time | Piston — With Sensors |
| `AL-E03` | Failed to retract | Retraction not confirmed within `actuator_timeout` | Piston — With Sensors |
| `AL-E04` | Failed to extend | Extension not confirmed within `actuator_timeout` | Piston — With Sensors |

All four feed into `internal_error`, the block-internal variable that drives the transition to `FAULT`.

## Modules

| Module | Livello | Description |
|--------|------|-------------|
| [Piston — No Sensors](no-sensors/index.md) | 2 | Immediate transition on command alone; no feedback |
| [Piston — With Sensors](sensors/index.md) | 2 | Position feedback via ZSL/ZSH; movement timeout; FAULT |
