# Propulsori

Trasportano materiale tra due punti tramite un ciclo di carico, trasferimento e scarico pressurizzato.

## Allarmi dei propulsori

| ID | Titolo | Condizione | Applicabile a |
|----|--------|------------|----------------|
| `TR-E01` | Timeout pressurizzazione | Pressione di convogliamento non raggiunta entro `pressurizing_timeout` | Propulsore Ingresso Sigillato |
| `TR-E02` | Timeout depressurizzazione | Sfiato non completato entro `depressurizing_timeout` | Propulsore Ingresso Sigillato |
| `TR-E03` | Aria di linea assente | `NOT PSL` — nessuna aria compressa disponibile per attuazione o pressurizzazione | Propulsore Ingresso Sigillato |
| `TR-E04` | Livello alto vessel | `LSH` attivo — vessel pieno oltre il previsto | Propulsore Ingresso Sigillato |

Un guasto su una valvola interna (`XV01`–`XV05`) o un timeout di Loading/Unloading sulla bilancia interna (`WT01`) contribuisce comunque a `internal_error`, ma senza un ID proprio a questo livello — già interamente visibile sulla pagina del sotto-dispositivo (valvole/celle di carico).

## Moduli

| Modulo | Livello | Descrizione |
|--------|------|-------------|
| [Propulsore Ingresso Sigillato](sealed-inlet/index.md) | 4 | Ciclo carico → sigillatura → pressurizzazione → convogliamento → depressurizzazione |
