
# Cose da considerare per la ricerca:
  - path cost
  - azioni possibili
  - giusta rappresentazione dello stato (matrice?)
  - fuzione euristica
  - test goal corretto
  - check mossa giusta


## Path Cost
Il costo del path dovrebbe essere equo per ogni mossa. Una mossa non ha un costo diverso da un'altra, a meno che non si voglia implementare come costo il fatto di perdere una posizione di favore rispeto ad altre pedine avversarie, di copertura del re (nel caso caso di squadra Bianca), o di attacco del re (nel caso di squadra Nera). Questi ultimi dettagli probabilmente devono essere inclusi invece nella funzione euristica.

## Azioni Possibili
Le Azioni possibili sono:
    - in direzione verticale o orizzontale
    - di tutte le pedine
        - con destinazione in una cella vuota
        - la cui direzione non bloccata da un'altra pedina
    - non verso i campi
        - a meno che non sei un pedone Nero che si trova già nel campo
    - non nelle celle di vittoria   (da verificare ma sembra logico)
        - a meno che non sei il re

## Funzione Euristica
### Buone mosse per la squadra Nera
- la pedina si accosta al Re
- la pedina si accosta ad una pedina bianca il cui lato opposto
- la pedina si accosta a più di una pedina bianca

### Cattive mosse per la squadra Nera
- la pedina sblocca una via d'uscita per il Re
- la pedina sblocca una via d'uscita per una pedina Bianca

### Buone mosse per la squadra Bianca
- la pedina si accosta al Re occupando la linea di una pedina Nera
- la pedina si accosta ad una pedina bianca
- la pedina si accosta a più di una pedina bianca
