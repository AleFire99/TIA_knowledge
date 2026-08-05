# Transporters

Transport material between two points through a pressurized load, transfer and unload cycle.

## Transporter Alarms

| ID | Title | Condition | Applies to |
|----|--------|------------|----------------|
| `TR-E01` | Pressurization timeout | Conveying pressure not reached within `pressurizing_timeout` | Transporter |
| `TR-E02` | Depressurization timeout | Venting not completed within `depressurizing_timeout` | Transporter |
| `TR-E03` | Line air absent | `NOT PSL` — no compressed air available for actuation or pressurization | Transporter |
| `TR-E04` | High vessel level | `LSH` active — vessel filled beyond the expected level | Transporter |

A fault on an internal valve (`XV01`–`XV05`) or a Loading/Unloading timeout on the internal load cell (`WT01`) still contributes to `internal_error`, but without its own ID at this level — already entirely visible on the sub-device's page ([valve alarms](../valves/index.md#valve-alarms)/[load-cell alarms](../load-cells/index.md#load-cell-alarms)).

## Modules

| Module | Level | Description |
|--------|------|-------------|
| [Transporter](transporter/index.md) | 4 (typical) | Load → sealing → pressurization → conveying → depressurization cycle; inlet valve (`XV01`) and filter (`FI`) injected |
