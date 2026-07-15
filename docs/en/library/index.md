# Library — Module Overview

NTE Process module library. Each module is a self-contained PLC function block with defined I/O, alarms, and settings.

Modules are grouped by type. Each module page covers: overview, components, I/O signals, operating routine, alarms, settings, data structure, and state machine.

---

## Diverters

Route conveyed material between two or more discharge paths using a pneumatically actuated mechanism.

| Module | Description |
|--------|-------------|
| [Pinch Diverter](diverters/pinch_type/index.md) | Dual pinch valves route material between two paths |

---

## Valves

Pneumatically controlled valves for flow isolation, actuation, and process control.

| Module | Description |
|--------|-------------|
| [Solenoid Valve](valves/solenoid/index.md) | Simple on/off valve; no feedback |
| [Pinch Valve](valves/pinch/index.md) | Squeezes flexible sleeve to close; pressure sensor confirms position |
| [Butterfly Valve — Single Solenoid](valves/butterfly/single_solenoid/index.md) | Spring-return; position feedback via ZSL/ZSH |
| [Butterfly Valve — Double Solenoid](valves/butterfly/double_solenoid/index.md) | Bistable, double-acting; position feedback via ZSL/ZSH |
| [Sealed Valve — Single Solenoid](valves/sealed/ss/index.md) | SS valve plus a dedicated seal solenoid |

---

## Gate

Electric lock for a manually operated gate — the PLC only grants unlock permission, it never moves anything.

| Module | Description |
|--------|-------------|
| [Gate with Electric Lock](gate/index.md) | Solenoid unlock/lock on operator request; no PLC-commanded movement |

---

## Nolvac

Pneumatic conveying unit operating on a suction/cleaning cycle.

| Module | Description |
|--------|-------------|
| [Nolvac](nolvac/index.md) | Alternating material suction and filter cleaning cycles |

---

## Transporters

Move material between two points via a load, transfer, and pressurized discharge cycle.

| Module | Description |
|--------|-------------|
| [Sealed Inlet Transporter](transporters/sealed-inlet/index.md) | Load → seal → pressurize → convey → depressurize cycle |

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

Pipeline pressure state derived from a PT transmitter reading or two digital pressure switches. No FSM — state is a direct, instantaneous function of the current reading, with no hysteresis.

| Module | Description |
|--------|-------------|
| [Pipeline Supervision](pipeline/index.md) | Analogic (PT) and digital (PSL/PSH) variants; empty/pressurised/with-material states + clogged alarm |
