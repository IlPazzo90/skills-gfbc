# Agenda

Rotta: `#/agenda/calendar?...`. **Tutto lo stato sta nella query**: data, numero di
giorni, finestra dello scadenziario, tipo, e l'**array di id dei tecnici in vista**.

Due metà: a sinistra lo **scadenziario degli impegni**, a destra il **calendario**.

---

## Sinistra — lo scadenziario

Sei cartelle: **Manutenzioni, Attività ufficio, Richiami, Richieste di intervento, Altri
impegni, Cestino**. Contengono **solo gli impegni non ancora programmati**.

In alto l'**intervallo di date**, scrivibile a mano o dal calendario; l'icona accanto
apre gli intervalli pronti (`oggi`, `domani`, `prossima settimana`, `mese corrente`…).

`+` su *Attività ufficio* e *Richieste di intervento* per crearne una (in alternativa:
tasto destro su un punto vuoto del calendario).

Due modi di lavorare che fanno risparmiare tempo vero:

- **Manutenzioni**: si prende la manutenzione e **la si trascina in un punto libero del
  calendario**. Si apre la nuova RdI con **l'operazione di manutenzione già spuntata**.
- **Attività ufficio**: selezionata quella che interessa, l'icona nel dettaglio apre la
  **finestra di evasione**.

I due tasti in alto chiudono l'una o l'altra metà a tutto schermo.

---

## Destra — il calendario

**Vista a 1, 2, 5 o 7 giorni.** A 1 e 2 giorni parte dal giorno scelto; a **5 e 7 mostra
la settimana che contiene il giorno scelto, sempre a partire dal lunedì** — quindi
scegliere mercoledì non sposta la finestra in avanti.

Modalità: **Agenda** (default), **Lista**, **Timeline**, e il **Planner** (solo SMART).

### Quali tecnici si vedono — e perché a volte «l'appuntamento non c'è»

| Modalità | Cosa mostra |
|---|---|
| **Default** | i tecnici configurati nelle impostazioni |
| **Personalizzata** | stato **momentaneo, non salvato**: nasce appena aggiungi o togli un tecnico |
| **Singolo** | un tecnico alla volta |
| **CAT** | solo con MULTICAT — **non ancora implementata** |
| **Gruppo personalizzato** | solo SMART: liste proprie (es. installatori / manutentori) |

**Il calendario mostra solo i tecnici in vista.** Un impegno assegnato a un tecnico fuori
vista **non si vede**, e non c'è nessun avviso. Prima di concludere che un appuntamento
non esiste, si controlla l'elenco dei tecnici nella query.

### ⋮ del calendario

- **Riassegna impegni** — sposta **un'intera giornata** di impegni da un tecnico a un
  altro, anche su un giorno diverso. Operazione massiva: si chiede conferma.
- **Visualizza aiuto planner** (SMART) — accende le zone giallline coi buchi; doppio
  click apre il planner in modalità **tappa-buchi** per quell'orario.
- **Impostazioni**

### Muovere gli impegni

Trascinamento per spostare; il **bordo inferiore** allunga o accorcia la durata.

Le **barre oblique grigie o rosse** sono i vincoli (orario, competenze, tecnico).
Spostandoci sopra un impegno **compare un avviso ma il vincolo si può forzare**: Unicò
avverte, non impedisce. Quindi un impegno su un vincolo non è impossibile — è una scelta
che qualcuno ha fatto.

**Click sinistro** su un impegno: finestra con i dati dell'impegno (fondo blu) e
dell'impianto (fondo bianco), e a destra quattro icone — apri **scheda impianto** in una
tab, **modifica** l'impegno, **evadi** l'intervento, **cancella** l'impegno.

**Click destro** su un punto vuoto: nuova RdI, **RdI multiple**, altri impegni
(→ `assistenza.md`).

---

## Impostazioni Agenda

`#/impostazioni/agenda/...`. **Cambiano il comportamento per tutti gli utenti**: non si
scrivono senza richiesta esplicita, nemmeno su una sandbox. E **va premuto `Salva`** in alto a
destra — c'è un avviso se resta qualcosa di non salvato.

### Visualizzazione

- **Informazioni RDI / Intervento eseguito / Altro impegno**: si compone *cosa si legge
  dentro il riquadro in agenda*. Si clicca **nel punto esatto** in cui inserire il dato
  (fra «codice impianto» e «numero ticket», per dire), poi si sceglie il campo dalla
  lista.
- **Tecnici in vista di default** — la lista che si apre all'avvio
- **Orario inizio/fine giornata**
- **Tecnici per pagina (vista 1 giorno)** — gli altri finiscono nelle pagine successive
- **Colora etichette tecnici** — usa il colore della tabella Tecnici
- **Colora RDI programmate per**: `Zona` (default), `Tipologia RdI`, `Motivo RdI`
- **Colora interventi eseguiti per**: `Zona` (default) o `Tipologia intervento`

I colori si scelgono nelle tabelle omonime. Quindi **il colore in agenda è una
convenzione aziendale configurata**, non un significato fisso: prima di interpretarlo,
si guarda questa impostazione.

### Scadenziario

- **Intervallo date** di default all'apertura
- **Mostra manutenzioni per**: scadenza **legale** o **programmata**
- **Mostra richiami per**: data chiamata o data richiamo
- **Mostra RDI per**: data richiesta o data pianificazione
- **Mostra altri impegni per**: data messaggio o data appuntamento

Sono quattro scelte che cambiano *cosa compare in quella finestra di date*. Due persone
con impostazioni diverse vedono scadenziari diversi sugli stessi dati.

---

## Unicò Mobile — l'agenda del tecnico

L'app apre sulla giornata corrente; `<` e `>` scorrono. **La configurazione licenze può
bloccare la consultazione alla sola giornata odierna.** Cambiando data l'app prova a
riconnettersi per aggiornare.

Ogni impegno mostra nominativo e codice impianto, motivo della RdI, indirizzo, ora e
durata prevista, con icone di stato:

- intervento **programmato** non ancora compilato
- intervento **compilato, inviato e ricevuto** da Unicò
- intervento **compilato e inviato ma non ancora ricevuto** — di solito manca il segnale.
  L'app ritenta da sola. **In questa fase non si fa logout**: si perde quanto compilato.
- una **nota importante** inserita nella RdI, da leggere subito
- un **altro impegno**

In basso a sinistra il **report giornaliero** del tecnico (anche stampabile).

Il tecnico, **se abilitato**, può cercare altri impianti (`*` su tutti i campi, oppure
solo Nome / Indirizzo / Codice — sempre **full text**, cioè «contiene») e **aggiungersi
un appuntamento da solo**. Dalla ricerca la scheda è **in sola lettura**; dall'impegno in
agenda invece può modificare molti dati dell'impianto.
