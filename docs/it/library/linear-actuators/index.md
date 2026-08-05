# Attuatori Lineari

Pistone pneumatico lineare, incorpora una singola Elettrovalvola (Livello 1) come proprio attuatore. Le due varianti condividono lo stesso schema di comando (`manual_mode`/`manual`/`auto` risolto ad ogni scan verso l'Elettrovalvola incorporata) e si distinguono per la presenza o assenza di retroazione di posizione: la variante "Senza Sensori" transita in modo immediato sul solo comando, la variante "Con Sensori" conferma ogni transizione tramite due finecorsa (`ZSL`/`ZSH`) e aggiunge un livello FAULT con timeout di movimento.

## Allarmi degli attuatori lineari

Applicabili solo alla variante con retroazione di posizione.

| ID | Titolo | Condizione | Applicabile a |
|----|--------|------------|----------------|
| `AL-E01` | Disallineamento sensore | Lo stato stabile corrente (RETRACTED/EXTENDED) non è confermato dal finecorsa atteso | Pistone — Con Sensori |
| `AL-E02` | Conflitto sensori | `ZSL` e `ZSH` risultano TRUE contemporaneamente | Pistone — Con Sensori |
| `AL-E03` | Mancata retrazione | Movimento di retrazione non confermato entro `actuator_timeout` | Pistone — Con Sensori |
| `AL-E04` | Mancata estensione | Movimento di estensione non confermato entro `actuator_timeout` | Pistone — Con Sensori |

Tutti e quattro concorrono a `internal_error`, variabile interna al blocco che determina la transizione a `FAULT`.

## Moduli

| Modulo | Livello | Descrizione |
|--------|------|-------------|
| [Pistone — Senza Sensori](no-sensors/index.md) | 2 | Transizione immediata sul solo comando; nessuna retroazione |
| [Pistone — Con Sensori](sensors/index.md) | 2 | Retroazione di posizione via ZSL/ZSH; timeout di movimento; FAULT |
