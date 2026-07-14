# Pipeline — Pressure State Supervision

The library provides two pipeline supervision variants, distinguished by sensor type. Both are implemented as **FC** (not FB): they have no memory of their own, no state machine, no `ack` command — every output is a pure function of the current readings, recomputed from scratch every scan.

## Pipeline Alarms

Shared by both entries in this category.

| ID | Title | Condition | Applies to |
|----|-------|-----------|------------|
| `PL-E01` | Pipeline clogged | `PSL` and `PSH` both active at the same time (digital variant) / scaled value ≥ `clogged_thresh` (analogic variant) | Digital pipeline, Analogic pipeline |
| `PL-E02` | Sensor mismatch | `PSH` active without `PSL` active — physically inconsistent combination | Digital pipeline |

`PL-E02` is exclusive to the digital variant: a single analog signal has no second independent value it can contradict. No Error/Warning class assigned — these blocks are stateless FCs with no FSM of their own to fault; it's up to the caller to decide whether and how to fold them into its own fault aggregate.

## Modules

| Variant | UDT | Sensor | States |
|---------|-----|--------|--------|
| [Analogic pipeline](analogic/index.en.md) | `UDT_An_Pipeline` | Analogue pressure transmitter (PT) | Empty, Pressurised, With material, Clogged |
| [Digital pipeline](digital/index.en.md) | `UDT_Dig_Pipeline` | Two digital pressure switches (PSL / PSH) | Empty, With material, Clogged (+ Mismatch) |

Both variants share the same conceptual logic — a lookup table that maps pressure readings to operating states — but differ in sensor type, resolution, and fault-state handling.
