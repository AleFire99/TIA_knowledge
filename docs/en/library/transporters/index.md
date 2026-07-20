# Transporters

Transport material between two points through a pressurized load, transfer and unload cycle.

## Transporter Alarms

| ID | Title | Condition | Applies to |
|----|--------|------------|----------------|
| `TR-E01` | Pressurization timeout | Conveying pressure not reached within `pressurizing_timeout` | Sealed Inlet Transporter |
| `TR-E02` | Depressurization timeout | Venting not completed within `depressurizing_timeout` | Sealed Inlet Transporter |
| `TR-E03` | Line air absent | `NOT PSL` — no compressed air available for actuation or pressurization | Sealed Inlet Transporter |
| `TR-E04` | High vessel level | `LSH` active — vessel filled beyond the expected level | Sealed Inlet Transporter |

A fault on an internal valve (`XV01`–`XV05`) or a Loading/Unloading timeout on the internal load cell (`WT01`) still contributes to `internal_error`, but without its own ID at this level — already entirely visible on the sub-device's page ([valve alarms](../valves/index.md#valve-alarms)/[load-cell alarms](../load-cells/index.md#load-cell-alarms)).

## Modules

| Module | Level | Description |
|--------|------|-------------|
| [Sealed Inlet Transporter](sealed-inlet/index.md) | 4 | Load → sealing → pressurization → conveying → depressurization cycle |
