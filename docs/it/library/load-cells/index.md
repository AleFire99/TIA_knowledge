# Celle di Carico

Il sistema di pesatura è costruito attorno a `UDT_Load_cells`, che raccoglie tutta la logica di ciclo — carico, scarico, timeout, conteggio batch — indipendentemente da quale trasmettitore fisico sia collegato. Un'interfaccia hardware separata converte i registri specifici del trasmettitore nei campi `IN` generici dell'UDT: cambiare trasmettitore significa scrivere una nuova interfaccia contro un nuovo UDT dedicato al vendor, non toccare `UDT_Load_cells` né i blocchi `Loading`/`Unloading`. Ad oggi l'unica interfaccia disponibile è per il trasmettitore Pavone Sistemi DAT 1400; altre interfacce per trasmettitori diversi si aggiungeranno in futuro nello stesso schema.

## Allarmi delle celle di carico

| ID | Classe | Titolo | Condizione | Applicabile a |
|----|--------|--------|------------|----------------|
| `LC-W01` | W | Peso fuori scala | `ALARMS.weight_invalid` — non causa una transizione a ERROR, blocca solo l'avvio di un ciclo | Celle di Carico |
| `LC-E01` | E | Timeout carico | `ALARMS.loading_timeout` — porta `Loading` in ERROR | Celle di Carico |
| `LC-E02` | E | Timeout scarico | `ALARMS.unloading_timeout` — porta `Unloading` in ERROR | Celle di Carico |

`LC-W01` è un avviso (non causa una transizione di stato) perché blocca solo l'ingresso in `LOADING`/`CONVEYING` da `IDLE` — a differenza di `LC-E01`/`LC-E02`, errori veri e propri, ciascuno con la propria transizione a `ERROR` nella rispettiva macchina a stati.

## Moduli

| Modulo | Descrizione |
|--------|-------------|
| [Ciclo di Carico e Scarico](loading-unloading/index.md) | Blocchi `Loading`/`Unloading`: riempimento e svuotamento a peso su `UDT_Load_cells`, con timeout e pausa/ripresa |
| [Interfaccia Pavone DAT 1400](pavone-dat-1400/index.md) | Adatta i registri del trasmettitore Pavone Sistemi DAT 1400 (`UDT_Pavone_IN`/`UDT_Pavone_OUT`) ai campi `IN` dell'UDT condiviso |
