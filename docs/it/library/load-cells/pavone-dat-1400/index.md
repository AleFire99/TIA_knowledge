# Interfaccia Pavone DAT 1400

## Panoramica

**FC, senza stato.** `Pavone_DAT_1400` è l'interfaccia verso il trasmettitore di peso Pavone Sistemi DAT 1400: legge `UDT_Pavone_IN` (registri del trasmettitore) e scrive `UDT_Pavone_OUT` (registro comandi), convertendo i dati grezzi nei campi `IN` generici di [`UDT_Load_cells`](../loading-unloading/index.md) tramite il parametro `VAR_IN_OUT scale`. Nessuno stato proprio, nessun `CMD`/`ack` — ricalcola tutto da zero ogni scan.

Questa è, ad oggi, l'unica interfaccia trasmettitore della libreria. Un trasmettitore diverso richiederà una nuova coppia di UDT (`IN`/`OUT`) e un nuovo FC dedicato, scritti secondo lo stesso schema — [`UDT_Load_cells`](../loading-unloading/index.md) e i blocchi `Loading`/`Unloading` non cambiano.

---

## Interfaccia

### Struttura dati

```mermaid
classDiagram
    class UDT_Pavone_IN {
        -Bool Status_register.hold
        -Bool Status_register.backup
        -Bool Status_register.input_1
        -Bool Status_register.input_2
        -Bool Status_register.output_1
        -Bool Status_register.output_2
        -Bool Status_register.delta_weight
        -Bool Status_register.setup
        -Bool Status_register.zero_center
        -Bool Status_register.stable_weight
        -Bool Status_register.zero_band
        -Bool Status_register.tare_inserted
        -Bool Status_register.underload
        -Bool Status_register.overload
        -Bool Status_register.weight_error
        -Bool Status_register.not_tared
        -DWord gross_weight
        -DWord net_weight
        -DWord peak
        -Word digital_inputs
        -Word digital_outputs
        -Word monitor_register
        -DWord net_weight_weighing
        -DWord code_weighing
        -DWord setpoint_1
        -DWord setpoint_2
        -DWord capacity
        -Word sensitivity
        -Word weight_division_value
        -Word decimals
        -DWord fixed_tare
    }
    class UDT_Pavone_OUT {
        -Word Command_register
        -DWord data_register
        -Word monitor_register
    }
```

`-` = sola lettura — entrambi gli UDT sono interamente read-only da DCS/HMI, incluso `Command_register`, che pure viene scritto da questo stesso FC ogni scan: l'attributo governa l'accesso esterno DCS/HMI, non le scritture interne del FC che possiede l'istanza.

`Status_register` corrisponde bit a bit allo Status Register Modbus documentato dal manuale del trasmettitore (Holding Register 0001):

| Bit | Campo | Significato (da manuale) |
|-----|-------|---------------------------|
| 15 | `setup` | Configurazione in corso |
| 14 | `delta_weight` | Variazione di peso rilevata |
| 13 | `output_2` | Uscita logica 2 attiva |
| 12 | `output_1` | Uscita logica 1 attiva |
| 11 | `input_2` | Ingresso logico 2 attivo |
| 10 | `input_1` | Ingresso logico 1 attivo |
| 9 | `backup` | Esegui backup (salvataggio E²PROM in corso) |
| 8 | `hold` | Funzione di hold attiva |
| 7 | `not_tared` | Non tarato |
| 6 | `weight_error` | Errore peso (segnale cella assente o fuori campo) |
| 5 | `overload` | Sovraccarico |
| 4 | `underload` | Sottocarico |
| 3 | `tare_inserted` | Tara inserita |
| 2 | `zero_band` | Peso in banda di zero |
| 1 | `stable_weight` | Peso stabile |
| 0 | `zero_center` | Centro di zero |

### Segnali di controllo

Il FC riceve `dat_IN : UDT_Pavone_IN`, restituisce `dat_OUT : UDT_Pavone_OUT`, e riceve in `VAR_IN_OUT` l'istanza `scale : UDT_Load_cells` su cui scrive. Dei molti registri disponibili in `UDT_Pavone_IN`/`UDT_Pavone_OUT`, solo tre vengono letti e uno scritto:

| Segnale | Tipo | Direzione | Descrizione |
|---------|------|-----------|-------------|
| `dat_IN.Status_register.weight_error` | Bool | IN | Copiato in `scale.IN.scale_error` |
| `dat_IN.net_weight` | DWord | IN | Peso netto grezzo, convertito in `scale.IN.current_weight` |
| `dat_IN.decimals` | Word | IN | Numero di decimali del trasmettitore (0–4); seleziona il fattore di scala |
| `dat_OUT.Command_register` | Word | OUT | Scritto a `16#2` (Autotara) mentre `scale.CMD.tare_request` è TRUE, altrimenti `0` |

`UDT_Pavone_IN` espone anche `gross_weight`, `peak`, `digital_inputs`/`digital_outputs`, `net_weight_weighing`, `code_weighing`, `setpoint_1`/`setpoint_2`, e gli altri 15 bit di `Status_register` — tutti presenti nel tipo ma non letti da questo FC oggi. `UDT_Pavone_OUT.data_register`/`monitor_register` non sono scritti. `capacity`, `sensitivity`, `weight_division_value` e `fixed_tare` non sono letti perché sono gli stessi parametri già impostati direttamente sul trasmettitore tramite il suo menu CALIBRAZIONE (rispettivamente `L.C. CAP`, `L.C. SEN`, `rESoLU` e `dEAd L.` — manuale DAT 1400) — duplicarli qui non aggiungerebbe nulla. Sono margine grezzo del trasmettitore, non funzionalità mancante nella documentazione.

---

## Comportamento

### Funzionamento

```Pascal
scale.IN.scale_error := dat_IN.Status_register.weight_error;

CASE dat_IN.decimals OF
  0: magnitude := 1;
  1: magnitude := 0.1;
  2: magnitude := 0.01;
  3: magnitude := 0.001;
  4: magnitude := 0.0001;
END_CASE;

scale.IN.current_weight := DINT_TO_REAL(DWORD_TO_DINT(dat_IN.net_weight)) * magnitude;

IF scale.CMD.tare_request THEN
    dat_OUT.Command_register := 16#2;
ELSE
    dat_OUT.Command_register := 0;
END_IF;
```

`net_weight` arriva come `DWord` — viene reinterpretato come `DINT` (intero con segno) e poi convertito in `Real`, infine scalato per `magnitude` in base a `decimals`. Il comando tara è un valore continuo (`16#2`, Autotara secondo il manuale del DAT 1400, finché `tare_request` resta TRUE), non un impulso a fronte.
