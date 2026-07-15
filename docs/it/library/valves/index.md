# Valvole

Valvole controllate pneumaticamente per isolamento, attuazione e controllo di processo.

## Allarmi delle valvole

Condivisi da tutte le voci di questa categoria che dispongono di retroazione di posizione.

| ID | Titolo | Condizione | Applicabile a |
|----|--------|------------|----------------|
| `XV-E01` | Disallineamento sensore | Lo stato stabile corrente (CLOSED/OPEN) non è confermato dal sensore di posizione atteso | Manicotto, Farfalla SS, Farfalla DS |
| `XV-E02` | Conflitto sensori | Entrambi i finecorsa di posizione risultano TRUE contemporaneamente | Farfalla SS, Farfalla DS |
| `XV-E03` | Mancata chiusura | Movimento di chiusura non confermato entro `actuator_timeout` | Manicotto, Farfalla SS, Farfalla DS |
| `XV-E04` | Mancata apertura | Movimento di apertura non confermato entro `actuator_timeout` | Manicotto, Farfalla SS, Farfalla DS |

Tutti e quattro concorrono a `internal_error`, variabile interna al blocco (non esposta tramite UDT) che determina la transizione a `FAULT`. La valvola a manicotto ha un solo sensore di posizione (`PSL`) e non può generare `XV-E02`.

## Moduli

| Modulo | Livello | Descrizione |
|--------|------|-------------|
| [Elettrovalvola](solenoid/index.md) | 1 | Attuatore atomico on/off; nessuna retroazione di posizione |
| [Valvola a Manicotto](pinch/index.md) | 2 | Comprime un tubo flessibile; un pressostato conferma la posizione chiusa |
| [Valvola a Farfalla — Singolo Solenoide (SS)](butterfly/single_solenoid/index.md) | 2 | Ritorno a molla in chiusura; retroazione di posizione via ZSL/ZSH |
| [Valvola a Farfalla — Doppio Solenoide (DS)](butterfly/double_solenoid/index.md) | 2 | Bistabile, doppio effetto; retroazione di posizione via ZSL/ZSH |
| [Valvola Sigillata — Singolo Solenoide (SS Sealed)](sealed/ss/index.md) | 3 | Valvola SS + elettrovalvola di tenuta dedicata |
