# Access Devices

The PLC never physically moves these devices — access is carried out by the operator by hand. The PLC only grants or denies unlock permission based on the current state, unlike valves, which the PLC actuates directly. They don't use the `manual_mode`/`manual`/`auto` arbitration common to the rest of the library: commands are direct (open/close), driven by the internal state of their own state machine.

## Access Device Alarms

| ID | Title | Condition | Applies to |
|----|-------|-----------|------------|
| `AD-E01` | Unlock failure | `CMD.open` accepted (state `OPENING`), close sensor not released within `unlock_timeout` | Gate Leaf — Electric Lock |

No timeout alarm on re-locking: an indefinite wait is normal behavior, not a fault, since completion depends on the operator's physical action rather than on the PLC.

## Modules

| Module | Level | Description |
|--------|-------|--------------|
| [Gate Leaf — Electric Lock](gate/index.md) | 2 | Solenoid unlock/lock on operator request; no PLC-commanded movement |
