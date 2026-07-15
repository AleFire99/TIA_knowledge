# Pipeline — Supervisione Stato di Pressione

La libreria fornisce due varianti di supervisione per pipeline pneumatiche, distinte per tipo di sensore. Entrambe sono implementate come **FC** (non FB): non hanno memoria propria, nessuna macchina a stati, nessun comando `ack` — ogni uscita è una funzione pura delle letture correnti, ricalcolata da zero ad ogni scan.

## Allarmi delle pipeline

Condivisi da entrambe le voci di questa categoria.

| ID | Titolo | Condizione | Applicabile a |
|----|--------|------------|-----------------|
| `PL-E01` | Tubazione intasata | `PSL` e `PSH` attivi contemporaneamente (variante digitale) / valore scalato ≥ `clogged_thresh` (variante analogica) | Pipeline digitale, Pipeline analogica |
| `PL-E02` | Disallineamento sensori | `PSH` attivo senza `PSL` attivo — combinazione fisicamente incoerente | Pipeline digitale |

`PL-E02` è esclusivo della variante digitale: un segnale analogico singolo non ha un secondo valore indipendente con cui essere in contraddizione. Nessuna classe Errore/Warning assegnata — questi blocchi sono FC stateless, senza una propria FSM da portare in FAULT; il chiamante decide se e come includerli nel proprio aggregato di guasto.

## Moduli

| Variante | UDT | Sensore | Stati |
|----------|-----|---------|-------|
| [Pipeline analogica](analogic/index.md) | `UDT_An_Pipeline` | Trasmettitore pressione analogico (PT) | Vuota, Pressurizzata, Con materiale, Intasata |
| [Pipeline digitale](digital/index.md) | `UDT_Dig_Pipeline` | Due pressostati digitali (PSL / PSH) | Vuota, Con materiale, Intasata (+ Disallineamento) |

Le due varianti condividono la stessa logica concettuale — una tabella di lookup che mappa letture di pressione in stati operativi — ma differiscono per sensore, risoluzione e gestione degli stati anomali.
