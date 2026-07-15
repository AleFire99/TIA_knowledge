# Deviatori

Deviano il materiale convogliato tra due o più percorsi di scarico tramite un meccanismo attuato pneumaticamente.

## Allarmi dei deviatori

| ID | Titolo | Condizione | Applicabile a |
|----|--------|------------|----------------|
| `DIV-E01` | Disallineamento instradamento | Lo stato stabile corrente (`ROUTE_A`/`ROUTE_B`) non è confermato dal sensore della sotto-valvola corrispondente | Deviatore a Manicotto |

Il guasto delle sotto-valvole interne (`XVA`/`XVB`) contribuisce a `internal_error` ma non riceve un proprio ID a questo livello — è già interamente visibile sulla pagina della sotto-valvola; vedere gli [allarmi delle valvole](../valves/index.md#allarmi-delle-valvole).

## Moduli

| Modulo | Livello | Descrizione |
|--------|------|-------------|
| [Deviatore a Manicotto](pinch_type/index.md) | 3 | Doppia valvola a manicotto che devia il materiale tra due percorsi |
