# AleFire Library Wiki

Technical documentation for the AleFire TIA Portal V20 global library.

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

## Regenerating Documentation

```bash
# Export sources from TIA Portal library
python wiki/scripts/export.py

# Regenerate docs and manifest
python wiki/scripts/generate_docs.py

# Local preview
uv run zensical serve --config-file zensical.en.toml
```
