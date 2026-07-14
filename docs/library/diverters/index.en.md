# Diverters

Route conveyed material between two or more discharge paths using a pneumatically actuated mechanism.

## Diverter Alarms

| ID | Class | Title | Condition | Applies to |
|----|-------|-------|-----------|------------|
| `DIV-E01` | E | Routing mismatch | Current stable state (`ROUTE_A`/`ROUTE_B`) not confirmed by the corresponding sub-valve's sensor | Pinch Diverter |

Faults from the internal sub-valves (`XVA`/`XVB`) feed into `internal_error` but don't get their own ID at this level — they're already fully visible on the sub-valve's own page; see [Valve Alarms](../valves/index.en.md#valve-alarms).

## Modules

| Module | Tier | Description |
|--------|------|-------------|
| [Pinch Diverter](pinch_type/index.md) | 3 | Dual pinch valves route material between two paths |
