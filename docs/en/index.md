# NTE Process — PLC Library

Knowledge base for NTE Process's TIA Portal V21 global library: function blocks and UDTs
for pneumatic field devices (valves, diverters, filters, access devices, load cells, Nolvac,
transporters, pipeline).

Every page in this wiki comes from the actual source code — a VCI (Simatic SD) export of
the TIA Portal library — not hand-written notes. An ingestion pipeline reads the exported
blocks and UDTs, structures them into a manifest, and regenerates each module's I/O signals,
alarms, parameters, state machine, and data structure automatically. When the library
changes, the documentation regenerates with it — no page drifts from the code it describes.

## Library Objects

| Category | Description |
|----------|-------------|
| [Valves](library/valves/index.md) | Butterfly (SS/DS), pinch, solenoid valves |
| [Access Devices](library/access/index.md) | Pneumatic gate leaves and doors with unlock permission |
| [Filters](library/filters/index.md) | 1-sleeve and 2-sleeve filters |
| [Diverters](library/diverters/index.md) | Pinch-type diverters |
| [Nolvac](library/nolvac/index.md) | Nolvac unit |
| [Load Cells](library/load-cells/index.md) | Load cells for batching |
| [Transporters](library/transporters/index.md) | Sealed inlet transporter |
| [Pipeline](library/pipeline/index.md) | Pipeline pressure state supervision |
