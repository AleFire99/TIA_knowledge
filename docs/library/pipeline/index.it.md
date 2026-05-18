# Pipeline — Supervisione Stato di Pressione

## Panoramica

Lo stato della pipeline è derivato continuamente dalla lettura del trasmettitore di pressione (PT). Non è necessaria una FSM: lo stato corrente è una funzione diretta del valore PT, con isteresi applicata a ciascun confine per prevenire il chattering.

Quattro stati coprono l'intera escursione operativa: da pipeline vuota a ostruzione. Solo un flag di stato è TRUE in qualsiasi momento.

---

## Componenti principali

- **Trasmettitore di pressione** (`pipeline_PT`) — lettura analogica della pressione nella pipeline [bar]
- **Soglie centrali** (`P_EMPTY`, `P_MATERIAL`, `P_CLOG`) — tre valori che definiscono i confini tra i quattro stati
- **Banda di isteresi** (`P_HYST`) — semiampiezza applicata simmetricamente a tutti i confini; un singolo parametro controlla il deadband sull'intera escursione

---

## Segnali I/O

| Segnale | Tipo | Descrizione |
|---------|------|-------------|
| `pipeline_PT` | REAL | Lettura pressione trasmettitore [bar] — ingresso |
| `pipeline.empty` | BOOL | Pipeline vuota — PT < `P_EMPTY − P_HYST` |
| `pipeline.pressurised` | BOOL | Pipeline in pressione, senza materiale |
| `pipeline.with_material` | BOOL | Materiale presente nella pipeline |
| `pipeline.clogged` | BOOL | Pressione eccessiva — possibile ostruzione |

---

## Funzionamento

Ad ogni ciclo PLC, il valore PT viene confrontato con tre confini di isteresi. Ogni confine utilizza una coppia Set/Reset separata per creare la banda:

- **PT in salita**: la transizione allo stato superiore avviene quando PT supera `P_x + P_HYST`
- **PT in discesa**: la transizione allo stato inferiore avviene quando PT scende sotto `P_x − P_HYST`
- **PT all'interno della banda**: lo stato corrente si mantiene — nessuna transizione

Questa struttura impedisce che un segnale PT rumoroso vicino a un confine generi oscillazioni ripetute dello stato. L'ampiezza del deadband è `2 × P_HYST` per ogni confine.

L'assegnazione dello stato finale usa una catena di priorità: CLOGGED > WITH_MATERIAL > PRESSURISED > EMPTY. I flag `pipeline.pressurised` e `pipeline.with_material` vengono consumati dagli stadi di trasporto a monte.

---

## Allarmi

| ID | Condizione | Causa |
|----|------------|-------|
| PL-E01 | `pipeline.clogged` | PT ≥ `P_CLOG + P_HYST` — pressione eccessiva nella pipeline |

Un evento `pipeline.clogged` deve attivare un allarme e interrompere qualsiasi trasporto attivo.

---

## Parametri

| Parametro | Esempio | Descrizione |
|-----------|---------|-------------|
| `P_HYST` | 0.1 bar | Semiampiezza banda isteresi — applicata a tutti i confini |
| `P_EMPTY` | 0.3 bar | Soglia centrale EMPTY ↔ PRESSURISED |
| `P_MATERIAL` | 1.5 bar | Soglia centrale PRESSURISED ↔ WITH_MATERIAL |
| `P_CLOG` | 3.5 bar | Soglia centrale WITH_MATERIAL ↔ CLOGGED |

I valori di esempio sono indicativi — calibrare con i dati di commissioning reali del sistema. Se il segnale PT richiede filtraggio (media mobile) prima del confronto con le soglie, applicarlo a monte di questo blocco.
