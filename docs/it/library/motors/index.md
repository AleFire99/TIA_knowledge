# Motori

Motore elettrico controllato on/off, senza alcun componente pneumatico incorporato — nessuna elettrovalvola, nessun elemento della famiglia Valvole. La variante attuale (`UDT_Motor_no_sensors`) non ha alcuna retroazione fisica propria: rileva il guasto solo tramite un segnale esterno di sovraccarico (`error_in`, tipicamente un contatto ausiliario del relè termico a monte). Il suffisso "Senza Sensori" anticipa una futura variante sensorizzata, stesso schema già seguito da Nolvac ("Ciclo a Tempo") e Dispositivi di Accesso ("Anta Cancello — Blocco Elettrico").

## Allarmi dei motori

| ID | Titolo | Condizione | Applicabile a |
|----|--------|------------|----------------|
| `MO-E01` | Sovraccarico termico | `error_in` TRUE mentre in marcia — tipicamente contatto ausiliario del relè termico | Motore — Senza Sensori |

## Moduli

| Modulo | Livello | Descrizione |
|--------|------|-------------|
| [Motore — Senza Sensori](no-sensors/index.md) | 1 | Marcia/arresto comandati; guasto rilevato solo da `error_in` esterno |
