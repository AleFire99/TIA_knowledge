# Filters

Compressed-air pulse cleaning systems for filter sleeves.

The cleaning mechanism (wait/pulse alternation, timed by `interval_duration`/`pulse_duration`) is identical regardless of the number of sleeves: both variants share the same base state machine, with the only addition — in the multi-sleeve version — being a rotation counter (`active_sleeve`, advanced modulo the number of sleeves) to alternate which solenoid valve gets pulsed. The principle extends naturally to a larger number of sleeves.

| Module | Description |
|--------|-------------|
| [Filter Cleaner — 1 Sleeve](1-sleeve/index.md) | Periodic pulse cycle with a single solenoid valve |
| [Filter Cleaner — 2 Sleeves](2-sleeves/index.md) | Alternating pulse sequence over two sleeves |
