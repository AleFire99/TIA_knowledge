# AleFire Library Wiki

Documentazione tecnica per la libreria globale TIA Portal V20 AleFire.

## Oggetti della libreria

| Categoria | Descrizione |
|-----------|-------------|
| [Valvole](library/valves/index.md) | Valvole farfalla (SS/DS), a pizzico, solenoide |
| [Deviatori](library/diverters/index.md) | Deviatori a pizzico e a tappo |
| [Filtri](library/filters/index.md) | Filtri a 1 e 2 maniche |
| [Portello](library/gate/index.md) | Portello/cancello pneumatico |
| [Nolvac](library/nolvac/index.md) | Unità Nolvac |
| [Celle di carico](library/load-cells/index.md) | Celle di carico per pesatura |
| [Pipeline](library/pipeline/index.md) | Supervisione stato di pressione pipeline |

## Aggiornare la documentazione

```bash
# Esportare i sorgenti dalla libreria TIA Portal
python wiki/scripts/export.py

# Rigenerare la documentazione e il manifesto
python wiki/scripts/generate_docs.py

# Anteprima locale
cd wiki && mkdocs serve
```
