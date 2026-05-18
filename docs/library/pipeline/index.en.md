# Pipeline — Pressure State Supervision

## Overview

Pipeline state is derived continuously from the pressure transmitter (PT) reading. No FSM is needed: the current state is a direct function of the current PT value, with hysteresis applied on each boundary to prevent chattering.

Four states cover the full operating range: from empty pipeline to obstruction. Exactly one state flag is TRUE at any time.

---

## Main Components

- **Pressure transmitter** (`pipeline_PT`) — analogue pressure reading from the pipeline [bar]
- **Central thresholds** (`P_EMPTY`, `P_MATERIAL`, `P_CLOG`) — three values defining the boundaries between the four states
- **Hysteresis band** (`P_HYST`) — half-width applied symmetrically to all boundaries; one parameter controls the deadband across the full range

---

## I/O Signals

| Signal | Type | Description |
|--------|------|-------------|
| `pipeline_PT` | REAL | Pressure transmitter reading [bar] — input |
| `pipeline.empty` | BOOL | Pipeline empty — PT < `P_EMPTY − P_HYST` |
| `pipeline.pressurised` | BOOL | Pipeline pressurised, no material present |
| `pipeline.with_material` | BOOL | Material present in the pipeline |
| `pipeline.clogged` | BOOL | Excessive pressure — possible obstruction |

---

## Operating Routine

Each PLC scan, the PT value is compared against three hysteresis boundaries. Each boundary uses a separate Set/Reset pair to create the deadband:

- **Rising PT**: transition to the higher state when PT crosses `P_x + P_HYST`
- **Falling PT**: transition to the lower state when PT drops below `P_x − P_HYST`
- **PT within the band**: current state holds — no transition

This structure prevents a noisy PT signal hovering near a boundary from causing repeated state toggling. The deadband width is `2 × P_HYST` per boundary.

The final state assignment uses a priority chain: CLOGGED > WITH_MATERIAL > PRESSURISED > EMPTY. The `pipeline.pressurised` and `pipeline.with_material` flags are consumed by upstream transport stages.

---

## Alarms

| ID | Condition | Cause |
|----|-----------|-------|
| PL-E01 | `pipeline.clogged` | PT ≥ `P_CLOG + P_HYST` — excessive pressure in the pipeline |

A `pipeline.clogged` event must trigger an alarm and halt any active transport.

---

## Settings

| Parameter | Example | Description |
|-----------|---------|-------------|
| `P_HYST` | 0.1 bar | Hysteresis half-width — applied to all boundaries |
| `P_EMPTY` | 0.3 bar | Central threshold EMPTY ↔ PRESSURISED |
| `P_MATERIAL` | 1.5 bar | Central threshold PRESSURISED ↔ WITH_MATERIAL |
| `P_CLOG` | 3.5 bar | Central threshold WITH_MATERIAL ↔ CLOGGED |

Example values are indicative — calibrate against actual system commissioning data. If the PT signal requires filtering (e.g. moving average) before threshold comparison, apply it upstream of this block.
