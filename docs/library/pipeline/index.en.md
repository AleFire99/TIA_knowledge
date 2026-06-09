# Pipeline — Pressure State Supervision

The library provides two pipeline supervision variants, distinguished by sensor type:

| Variant | UDT | Sensor | States |
|---------|-----|--------|--------|
| [Analogic pipeline](analogic/index.en.md) | `UDT_An_Pipeline` | Analogue pressure transmitter (PT) | Empty, Pressurised, With material, Clogged |
| [Digital pipeline](digital/index.en.md) | `UDT_Dig_Pipeline` | Two digital pressure switches (PSL / PSH) | Empty, With material, Clogged, Error |

Both variants share the same conceptual logic — a lookup table that maps pressure readings to operating states — but differ in sensor type, resolution, and fault-state handling.
