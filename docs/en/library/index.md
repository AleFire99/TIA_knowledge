# Library — Module Overview

NTE Process module library. Each module is a self-contained PLC function block with defined I/O, alarms, and parameters.

Modules are grouped by type. Each module page describes: overview, composition, I/O signals, operation, alarms, parameters, data structure, and state diagram.

The `manual_mode`/`manual`/`auto` command resolves only at the outermost level exposed to HMI/DCS; nested components (e.g. internal solenoid valves) only receive the `auto` already resolved by the block that embeds them — they don't arbitrate on their own.

Every timer in this library follows the same pattern: it's a TON whose `IN` is tied exclusively to the state (or sub-state) it needs to be active in — it starts on entering that state and resets automatically on leaving it, with no other conditions. That's why every module page's Timer table only lists `Timer | State it's active in | Threshold (parameter)`: the reset condition is never separate information, it's always "leaving that state."

---

## [Valves](valves/index.md)

Pneumatically controlled valves for isolation, actuation, and process control.

| Module | Description |
|--------|-------------|
| [Solenoid Valve](valves/solenoid/index.md) | Simple on/off valve; no feedback |
| [Pinch Valve](valves/pinch/index.md) | Pinches a flexible tube shut; a pressure switch confirms position |
| [Butterfly Valve — Single Solenoid](valves/butterfly/single_solenoid/index.md) | Spring return; position feedback via ZSL/ZSH |
| [Butterfly Valve — Double Solenoid](valves/butterfly/double_solenoid/index.md) | Bistable, double-acting; position feedback via ZSL/ZSH |
| [Sealed Valve — Single Solenoid](valves/sealed/ss/index.md) | SS valve + dedicated sealing solenoid valve |

---

## [Access Devices](access/index.md)

The PLC only grants unlock permission based on the current state — physical access stays with the operator, the PLC never moves anything.

| Module | Description |
|--------|-------------|
| [Gate Leaf — Electric Lock](access/gate/index.md) | Solenoid unlock/lock on operator request; no PLC-commanded movement |

---

## [Filters](filters/index.md)

Compressed-air pulse cleaning systems for filter sleeves.

| Module | Description |
|--------|-------------|
| [Filter Cleaner — 1 Sleeve](filters/1-sleeve/index.md) | Periodic pulse cycle with a single solenoid valve |
| [Filter Cleaner — 2 Sleeves](filters/2-sleeves/index.md) | Alternating pulse sequence across two sleeves |

---

## [Diverters](diverters/index.md)

Divert conveyed material between two or more discharge paths via a pneumatically actuated mechanism.

| Module | Description |
|--------|-------------|
| [Pinch-Type Diverter](diverters/pinch_type/index.md) | Dual pinch valve diverting material between two paths |

---

## [Nolvac](nolvac/index.md)

Pneumatic conveying unit with a suction/cleaning cycle; variants differ in how they determine phase duration.

| Module | Description |
|--------|-------------|
| [Nolvac — Timed Cycle](nolvac/timed-cycle/index.md) | Alternating material-suction and filter-cleaning cycles, timed by parameter |

---

## [Load Cells](load-cells/index.md)

Weighing system built around a single shared data structure, with cycle logic decoupled from the physical transmitter via a swappable interface.

| Module | Description |
|--------|-------------|
| [Loading and Unloading Cycle](load-cells/loading-unloading/index.md) | Weight-based filling and emptying; timeout, pause/resume |
| [Pavone DAT 1400 Interface](load-cells/pavone-dat-1400/index.md) | Adapts the Pavone Sistemi DAT 1400 transmitter to the shared IN fields |

---

## [Analog Signals](io/index.md)

Shared library utility: converts a raw analog input count into a value scaled to engineering units.

| Module | Description |
|--------|-------------|
| [Analog Signals](io/index.md) | Raw count → scaled value conversion, used by the Analog Pipeline and Sealed Inlet Transporter |

---

## [Transporters](transporters/index.md)

Convey material between two points through a load, transfer, and pressurized discharge cycle.

| Module | Description |
|--------|-------------|
| [Sealed Inlet Transporter](transporters/sealed-inlet/index.md) | Load → sealing → pressurizing → conveying → depressurizing cycle |

---

## [Pipeline](pipeline/index.md)

Derives pipeline pressure state from a PT transmitter reading or two digital pressure switches. No state machine — state is a direct, instantaneous function of the current reading, with no hysteresis.

| Module | Description |
|--------|-------------|
| [Analog Pipeline](pipeline/analogic/index.md) | Pressure state from a PT transmitter; 3 configurable thresholds, no hysteresis today (possible future extension) |
| [Digital Pipeline](pipeline/digital/index.md) | Pressure state from 2 pressure switches (PSL/PSH); clogging and sensor-mismatch alarms |
