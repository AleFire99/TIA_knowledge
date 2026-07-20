# Nolvac

Unità di convogliamento pneumatico a ciclo aspirazione/pulizia. Le varianti della famiglia condividono lo stesso schema di base (una Valvola a Farfalla SS per l'ingresso, due Elettrovalvole per aspirazione e pulizia filtro) e si distinguono per come determinano la durata delle fasi: la variante attuale usa una durata fissa configurata a parametro; una futura variante con sensore di livello alto (`ZSH`) triggererebbe le fasi in base al livello di materiale rilevato invece che a tempo.

## Moduli

| Modulo | Livello | Descrizione |
|--------|------|-------------|
| [Nolvac — Ciclo a Tempo](timed-cycle/index.md) | 3 | Cicli alternati di aspirazione materiale e pulizia filtro, temporizzati a `SETTING` |
