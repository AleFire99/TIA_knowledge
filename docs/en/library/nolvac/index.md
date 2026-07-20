# Nolvac

Pneumatic conveying unit with a suction/cleaning cycle. Variants in this family share the same base layout (one SS Butterfly Valve for the inlet, two Solenoid Valves for suction and filter cleaning) and differ in how they determine phase duration: today's variant uses a fixed duration set by parameter; a future variant with a high-level sensor (`ZSH`) would trigger phases based on detected material level instead of time.

## Modules

| Module | Level | Description |
|--------|-------|-------------|
| [Nolvac — Timed Cycle](timed-cycle/index.md) | 3 | Alternating material-suction and filter-cleaning cycles, timed by `SETTING` |
