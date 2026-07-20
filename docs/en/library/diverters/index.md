# Diverters

Divert conveyed material between two or more discharge paths through a pneumatically actuated mechanism.

## Diverter Alarms

| ID | Title | Condition | Applies to |
|----|--------|------------|----------------|
| `DIV-E01` | Routing misalignment | The current stable state (`ROUTE_A`/`ROUTE_B`) is not confirmed by the corresponding sub-valve's sensor | Pinch-Type Diverter |

Faults from the internal sub-valves (`XVA`/`XVB`) contribute to `internal_error` but don't get their own ID at this level — it's already fully visible on the sub-valve's page; see the [valve alarms](../valves/index.md#valve-alarms).

## Modules

| Module | Level | Description |
|--------|------|-------------|
| [Pinch-Type Diverter](pinch_type/index.md) | 3 | Dual pinch valve that diverts material between two paths |
