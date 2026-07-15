# Propulsori

Trasportano materiale tra due punti tramite un ciclo di carico, trasferimento e scarico pressurizzato.

## Allarmi dei propulsori

| ID | Classe | Titolo | Condizione | Applicabile a |
|----|--------|--------|------------|----------------|
| `TR-E01` | E | Timeout pressurizzazione | Pressione di convogliamento non raggiunta entro `pressurizing_timeout` | Propulsore Ingresso Sigillato |
| `TR-E02` | E | Timeout depressurizzazione | Sfiato non completato entro `depressurizing_timeout` | Propulsore Ingresso Sigillato |
| `TR-E03` | E | Guasto valvola interna | Guasto su una delle valvole interne (`XV01`–`XV05`) | Propulsore Ingresso Sigillato |
| `TR-E04` | E | Guasto bilancia | Timeout Loading o Unloading sulla bilancia interna (`WT01`) | Propulsore Ingresso Sigillato |
| `TR-E05` | E | Perdita pressione di sicurezza | `NOT PSL` — pressione di sicurezza persa | Propulsore Ingresso Sigillato |
| `TR-E06` | E | Livello alto vessel | `LSH` attivo — vessel pieno oltre il previsto | Propulsore Ingresso Sigillato |

`TR-E03` e `TR-E04` sono propagazioni dirette dei guasti delle sotto-istanze (`XV01`–`XV05`, `WT01`) — non ripetono la causa specifica, già interamente visibile sulla pagina del sotto-dispositivo.

## Moduli

| Modulo | Tier | Descrizione |
|--------|------|-------------|
| [Propulsore Ingresso Sigillato](sealed-inlet/index.md) | 3 | Ciclo carico → sigillatura → pressurizzazione → convogliamento → depressurizzazione |
