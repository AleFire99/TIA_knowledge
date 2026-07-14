# Valves

Pneumatically controlled valves for flow isolation, actuation, and process control.

## Valve Alarms

Shared by every entry in this category that has position feedback.

| ID | Class | Title | Condition | Applies to |
|----|-------|-------|-----------|------------|
| `XV-E01` | E | Sensor mismatch | Current stable state (CLOSED/OPEN) not confirmed by the expected position sensor | Pinch, Butterfly SS, Butterfly DS |
| `XV-E02` | E | Sensor conflict | Both position limit switches TRUE at the same time | Butterfly SS, Butterfly DS |
| `XV-E03` | E | Failed to close | Closing movement not confirmed within `actuator_timeout` | Pinch, Butterfly SS, Butterfly DS |
| `XV-E04` | E | Failed to open | Opening movement not confirmed within `actuator_timeout` | Pinch, Butterfly SS, Butterfly DS |

All four feed into `internal_error`, a block-internal variable (not exposed via the UDT) that drives the transition to `FAULT`. The Pinch valve has only one position sensor (`PSL`) and cannot raise `XV-E02`.

## Modules

| Module | Tier | Description |
|--------|------|-------------|
| [Solenoid Valve](solenoid/index.md) | 1 | Atomic on/off actuator; no position feedback |
| [Pinch Valve](pinch/index.md) | 2 | Squeezes a flexible sleeve; a pressure switch confirms the closed position |
| [Butterfly Valve — Single Solenoid (SS)](butterfly/single_solenoid/index.md) | 2 | Spring-return to closed; position feedback via ZSL/ZSH |
| [Butterfly Valve — Double Solenoid (DS)](butterfly/double_solenoid/index.md) | 3 | Bistable, double-acting; position feedback via ZSL/ZSH |
| [Sealed Valve — Single Solenoid (SS Sealed)](sealed/ss/index.md) | 3 | SS valve plus a dedicated seal solenoid |
