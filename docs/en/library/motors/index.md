# Motors

Electric motor with on/off control, no pneumatic component embedded at all — no solenoid valve, no member of the Valves family. The current variant (`UDT_Motor_no_sensors`) has no physical feedback of its own: it detects a fault only through an external overload signal (`error_in`, typically an upstream thermal relay auxiliary contact). The "No Sensors" suffix anticipates a future sensored variant, the same pattern already followed by Nolvac ("Timed Cycle") and Access Devices ("Gate Leaf — Electric Lock").

## Motor alarms

| ID | Title | Condition | Applies to |
|----|-------|-----------|------------|
| `MT-E01` | Thermal overload | `error_in` TRUE while running — typically a thermal relay auxiliary contact | Motor — No Sensors |

## Modules

| Module | Livello | Description |
|--------|------|-------------|
| [Motor — No Sensors](no-sensors/index.md) | 1 | Run/stop commanded; fault detected only from external `error_in` |
