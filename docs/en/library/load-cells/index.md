# Load Cells

The weighing system is built around `UDT_Load_cells`, which holds all cycle logic — loading, unloading, timeouts, batch tracking — independent of which physical transmitter is connected. A separate hardware interface converts transmitter-specific registers into the UDT's generic `IN` fields: changing transmitter means writing a new interface against a new vendor-specific UDT, not touching `UDT_Load_cells` or the `Loading`/`Unloading` blocks. Today the only available interface is for the Pavone Sistemi DAT 1400 transmitter; further interfaces for other transmitters will be added in the future following the same pattern.

## Load Cell Alarms

| ID | Title | Condition | Applies to |
|----|-------|-----------|------------|
| `LC-W01` | Weight out of range | `ALARMS.weight_invalid` — doesn't cause a transition to ERROR, only blocks starting a cycle | Load Cells |
| `LC-E01` | Loading stalled | `ALARMS.loading_timeout` — no weight progress for `loading_timeout`; drives `Loading` to ERROR | Load Cells |
| `LC-E02` | Unloading stalled | `ALARMS.unloading_timeout` — no weight progress for `unloading_timeout`; drives `Unloading` to ERROR | Load Cells |

`LC-W01` is a warning (no state transition) because it only blocks entry into `LOADING`/`CONVEYING` from `IDLE` — unlike `LC-E01`/`LC-E02`, genuine errors each with their own transition to `ERROR` on their respective state machine.

## Modules

| Module | Description |
|--------|-------------|
| [Loading and Unloading Cycle](loading-unloading/index.md) | `Loading`/`Unloading` blocks: weight-based filling and emptying on `UDT_Load_cells`, with timeout and pause/resume |
| [Pavone DAT 1400 Interface](pavone-dat-1400/index.md) | Adapts the Pavone Sistemi DAT 1400 transmitter registers (`UDT_Pavone_IN`/`UDT_Pavone_OUT`) to the shared UDT's `IN` fields |
