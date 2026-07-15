# Dispositivi di Accesso

Il PLC non movimenta mai fisicamente questi dispositivi — l'accesso è compiuto dall'operatore a mano. Il PLC concede o nega solo il permesso di sblocco in base allo stato corrente, a differenza delle valvole, che il PLC aziona direttamente. Non usano l'arbitraggio `manual_mode`/`manual`/`auto` comune al resto della libreria: i comandi sono diretti (apertura/chiusura), pilotati dallo stato interno della propria macchina a stati.

## Allarmi dei dispositivi di accesso

| ID | Titolo | Condizione | Applicabile a |
|----|--------|------------|----------------|
| `GD-E01` | Mancato sblocco | `CMD.open` accolto (stato `OPENING`), sensore di chiusura non rilasciato entro `unlock_timeout` | Anta Cancello — Blocco Elettrico |

Nessun allarme di timeout sul ri-blocco: l'attesa indefinita è comportamento normale, non un guasto, poiché il completamento dipende dall'azione fisica dell'operatore e non dal PLC.

## Moduli

| Modulo | Livello | Descrizione |
|--------|------|-------------|
| [Anta Cancello — Blocco Elettrico](gate/index.md) | 2 | Sblocco/blocco elettrovalvola su richiesta operatore; nessun movimento comandato dal PLC |
