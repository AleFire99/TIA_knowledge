# Pipeline — Supervisione Stato di Pressione

La libreria fornisce due varianti di supervisione per pipeline pneumatiche, distinte per tipo di sensore:

| Variante | UDT | Sensore | Stati |
|----------|-----|---------|-------|
| [Pipeline analogica](analogic/index.it.md) | `UDT_An_Pipeline` | Trasmettitore pressione analogico (PT) | Vuota, Pressurizzata, Con materiale, Intasata |
| [Pipeline digitale](digital/index.it.md) | `UDT_Dig_Pipeline` | Due pressostati digitali (PSL / PSH) | Vuota, Con materiale, Intasata, Errore |

Le due varianti condividono la stessa logica concettuale — una tabella di lookup che mappa letture di pressione in stati operativi — ma differiscono per sensore, risoluzione e gestione degli stati anomali.
