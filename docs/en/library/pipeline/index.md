# Pipeline — Pressure State Supervision

The library provides two supervision variants for pneumatic pipelines, distinguished by sensor type. Both are implemented as **FC** (not FB): no memory of their own, no state machine, no `ack` command — every output is a pure function of the current readings, recalculated from scratch every scan.

## Pipeline Alarms

Shared by both entries in this category.

| ID | Title | Condition | Applies to |
|----|--------|------------|-----------------|
| `PL-E01` | Clogged pipe | `PSL` and `PSH` active simultaneously (digital variant) / scaled value ≥ `clogged_thresh` (analog variant) | Digital Pipeline, Analog Pipeline |
| `PL-E02` | Sensor misalignment | `PSH` active without `PSL` active — physically inconsistent combination | Digital Pipeline |

`PL-E02` is exclusive to the digital variant: a single analog signal has no second independent value it could be in contradiction with. No Error/Warning class assigned — these blocks are stateless FCs, with no state machine of their own to bring into FAULT; the caller decides whether and how to include them in its own fault aggregate.

## Modules

| Variant | UDT | Sensor | States |
|----------|-----|---------|-------|
| [Analog Pipeline](analogic/index.md) | `UDT_An_Pipeline` | Analog pressure transmitter (PT) | Empty, Pressurized, With material, Clogged |
| [Digital Pipeline](digital/index.md) | `UDT_Dig_Pipeline` | Two digital pressure switches (PSL / PSH) | Empty, With material, Clogged (+ Misalignment) |

The two variants share the same conceptual logic — a lookup table that maps pressure readings to operating states — but differ in sensor, resolution, and handling of anomalous states.
