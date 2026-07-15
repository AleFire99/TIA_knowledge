# NTE Process — Libreria PLC

Base di conoscenza per la libreria globale TIA Portal V21 di NTE Process: blocchi funzione
e UDT per dispositivi pneumatici di campo (valvole, deviatori, filtri, portelli, celle di
carico, Nolvac, trasportatori, pipeline).

Ogni pagina di questo wiki nasce dal codice sorgente reale — export VCI (Simatic SD) della
libreria TIA Portal — non da note scritte a mano. Una pipeline di ingestione legge i blocchi
e gli UDT esportati, li struttura in un manifest e rigenera automaticamente segnali I/O,
allarmi, parametri, macchina a stati e struttura dati di ogni modulo. Quando la libreria
cambia, la documentazione si rigenera con essa: nessuna pagina resta indietro rispetto al
codice che descrive.

## Oggetti della libreria

| Categoria | Descrizione |
|-----------|-------------|
| [Valvole](library/valves/index.md) | Valvole farfalla (SS/DS), a manicotto, elettrovalvola |
| [Portelli](library/gate/index.md) | Portelli/cancelli pneumatici |
| [Filtri](library/filters/index.md) | Filtri a 1 e 2 maniche |
| [Deviatori](library/diverters/index.md) | Deviatori a manicotto |
| [Nolvac](library/nolvac/index.md) | Unità Nolvac |
| [Celle di carico](library/load-cells/index.md) | Celle di carico per pesatura |
| [Propulsori](library/transporters/index.md) | Propulsore a ingresso sigillato |
| [Pipeline](library/pipeline/index.md) | Supervisione stato di pressione pipeline |
