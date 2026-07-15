# NTE Process — PLC Library

Knowledge base for NTE Process's TIA Portal V21 global library: function blocks and UDTs
for pneumatic field devices (valves, diverters, filters, gates, load cells, Nolvac, pipeline).

Every page in this wiki comes from the actual source code — a VCI (Simatic SD) export of
the TIA Portal library — not hand-written notes. An ingestion pipeline reads the exported
blocks and UDTs, structures them into a manifest, and regenerates each module's I/O signals,
alarms, parameters, state machine, and data structure automatically. When the library
changes, the documentation regenerates with it — no page drifts from the code it describes.

## Library Objects

| Category | Description |
|----------|-------------|
| [Valves](library/valves/index.md) | Butterfly (SS/DS), pinch, solenoid valves |
| [Diverters](library/diverters/index.md) | Pinch-type diverters |
| [Filters](library/filters/index.md) | 1-sleeve and 2-sleeve filters |
| [Gate](library/gate/index.md) | Pneumatic gate/door |
| [Nolvac](library/nolvac/index.md) | Nolvac unit |
| [Load cells](library/load-cells/index.md) | Load cells for batching |
| [Pipeline](library/pipeline/index.md) | Pipeline pressure state supervision |
