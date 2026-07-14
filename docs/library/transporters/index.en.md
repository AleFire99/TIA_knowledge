# Transporters

Move material between two points via a load, transfer, and pressurized discharge cycle.

## Transporter Alarms

| ID | Class | Title | Condition | Applies to |
|----|-------|-------|-----------|------------|
| `TR-E01` | E | Pressurization timeout | Conveying pressure not reached within `pressurizing_timeout` | Sealed Inlet Transporter |
| `TR-E02` | E | Depressurization timeout | Venting not completed within `depressurizing_timeout` | Sealed Inlet Transporter |
| `TR-E03` | E | Internal valve fault | Fault on one of the internal valves (`XV01`–`XV05`) | Sealed Inlet Transporter |
| `TR-E04` | E | Load cell fault | Loading or Unloading timeout on the internal scale (`WT01`) | Sealed Inlet Transporter |
| `TR-E05` | E | Safety pressure lost | `NOT PSL` — safety pressure lost | Sealed Inlet Transporter |
| `TR-E06` | E | Vessel high level | `LSH` active — vessel overfilled | Sealed Inlet Transporter |

`TR-E03` and `TR-E04` are direct propagations of sub-instance faults (`XV01`–`XV05`, `WT01`) — they don't restate the specific cause, already fully visible on the sub-device's own page.

## Modules

| Module | Tier | Description |
|--------|------|-------------|
| [Sealed Inlet Transporter](sealed-inlet/index.md) | 3 | Load → seal → pressurize → convey → depressurize cycle |
