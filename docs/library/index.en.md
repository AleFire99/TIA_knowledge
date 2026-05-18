# Library — Module Overview

NTE Process module library. Each module is a self-contained PLC function block with defined I/O, alarms, and settings.

Modules are grouped by type. Each module page covers: overview, components, I/O signals, operating routine, alarms, settings, data structure, and state machine.

---

## Diverters

Route conveyed material between two or more discharge paths using a pneumatically actuated mechanism.

| Module | Description |
|--------|-------------|
| [Pinch Diverter](diverters/pinch_type/index.md) | Dual pinch valves route material between two paths |
| [Plug-Type Diverter](diverters/plug_type/index.md) | Inflatable-seal plug with pneumatic actuator; handles abrasive powders |

---

## Valves

Pneumatically controlled valves for flow isolation, actuation, and process control.

| Module | Description |
|--------|-------------|
| [Solenoid Valve](valves/solenoid/index.md) | Simple on/off valve; no feedback |
| [Pinch Valve](valves/pinch/index.md) | Squeezes flexible sleeve to close; pressure sensor confirms position |
| [Butterfly Valve — Single Solenoid](valves/butterfly/single_solenoid/index.md) | Spring-return; position feedback via ZSL/ZSH; maintenance counter |
| [Butterfly Valve — Double Solenoid](valves/butterfly/double_solenoid/index.md) | Bistable; holds last position on de-energise; position feedback via ZSL/ZSH |

---

## Filters

Compressed-air pulse cleaning systems for dust filter sleeves.

| Module | Description |
|--------|-------------|
| [Filter Cleaner — 1 Sleeve](filters/1-sleeve/index.md) | Single solenoid periodic pulse cycle |
| [Filter Cleaner — 2 Sleeves](filters/2-sleeves/index.md) | Alternating pulse sequence across two sleeves |

---

## Load Cells

Weighing system using DAT 1400 PROFINET transmitter. Operator configuration layer plus transport cycle FSM.

| Module | Description |
|--------|-------------|
| [Load Cells](load-cells/index.md) | Batch weighing with DAT 1400 PROFINET; tare, setpoint validation, conveyed tracking |

---

## Pipeline

Pipeline pressure state derived from a PT transmitter reading. No FSM — state is a direct function of PT with hysteresis.

| Module | Description |
|--------|-------------|
| [Pipeline Supervision](pipeline/index.md) | Four states (EMPTY / PRESSURISED / WITH_MATERIAL / CLOGGED) from PT with band hysteresis |
