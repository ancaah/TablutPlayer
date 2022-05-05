
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

## Considerazioni più avanzate
### Informazioni STATO
Potrebbe essere utile mantenere una rappresentazione diversa dello stato, che possa evitare numerosi cicli di ricerca delle pedine della matrice. L'esempio più lampante e banale da implementare sarebbe memorizzare la posizione del re per evitare di ricercarlo ad ogni test_goal del player, evitando molti accessi inutili alla matrice. Inoltre, per i fini di entrambi i team, bianco e nero, risulta utile nella funzione euristica sapere dove si trova il Re per poter dare un valore maggiore alle mosse che lo attaccano o difendono con efficacia.

### Immutabilità STATO
Lo stato deve essere immutabile? Posso modificare la matrice di stato oppure devo usare strutture immutabili a seconda dell'algoritmo di ricerca utilizzato? Questo dubbio mi è venuto leggendo cose su internet e ho bisogno di risolverlo, perché in tal caso è necessario fare cambiamenti al codice.

### Conoscenza dei due gicoatori
Il player bianco potrebbe avere bisogno di conoscere le euristiche del nero per capire quale mossa andrà a fare

### Giocatore NERO - Gerarchia mosse (Decrescente per livello di utilità)
CONTRO IL RE:
Vittoria se:
- Quarta pedina adiacente al Re nel castello (VITTORIA)
- Terza pedina adiacente al Re se adiacente al castello (VITTORIA)
- Seconda pedina adiacente al Re contando anche un campo (VITTORIA)

Inoltre sono buone:
- Prima pedina adiacente al Re + 2 muro o pedine Bianche
- Seconda pedina adiacente al Re
- Prima pedina adiacente al Re + 1 muro o pedina Bianca
- Prima pedina adiacente al Re

- Seconda pedina adiacente alla pedina Bianca anche condando muri(PRESA)
CONTRO PEDINE:

# UPDATE 05 MAGGIO
Fattorizzato parte del codice del metodo action(). Ora bisogna far si che action() chiami i metodi white o black behaviour a seconda del turno a cui sta.
## TODO
- implementare un modo per gestire i turni bianco e nero, fondamentale
- modificare metodo action, importante
- controllare e modificare il metodo goal_test che fa schifo