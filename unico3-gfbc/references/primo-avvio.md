# Primo avvio: fare il punto sulla tua organizzazione

Questa skill è nata in un'altra azienda. Le procedure e le trappole di Unicò valgono
per tutti; la configurazione no. Sigle delle operazioni di manutenzione, nomi dei
magazzini, tipologie di attività e di intervento, esiti del CRM, ruoli: dove i file
`references/` ne citano, sono **esempi dell'azienda d'origine**. La tua installazione ha
i suoi, e finché non li hai letti la skill li indovina.

Il primo avvio serve a questo: leggere la tua configurazione una volta, scriverla in un
file tuo, e da lì in poi usare quella.

## Dove finisce quello che impari

```
~/.config/unico3/organizzazione.md
```

Fuori dalla cartella della skill, di proposito: contiene dati della tua azienda (nomi,
ruoli, sigle) e non deve finire in nessun repository. Così un `git pull` della skill non
lo tocca mai. Il modello vuoto sta in `modelli/organizzazione.md`.

```bash
mkdir -p ~/.config/unico3 && cp -n <cartella della skill>/modelli/organizzazione.md ~/.config/unico3/
```

## Quando scatta

- `~/.config/unico3/organizzazione.md` non esiste, o ha ancora i segnaposto `<...>`;
- l'utente chiede «fai il punto», «impara la mia organizzazione», «configura la skill»;
- un file `references/` cita una sigla o un nome che nella tua installazione non c'è.

In tutti i casi lo proponi, non lo imponi: se l'utente ha fretta, fai il lavoro chiesto
e dichiari che stai usando gli esempi d'origine.

## Regole del giro

- **Solo lettura.** Il primo avvio non scrive niente su Unicò. Ogni azienda non ancora
  dichiarata vale produzione (`guardrail.md` §5.1), quindi non c'è niente da scrivere
  comunque.
- **Il login lo fa l'utente.** Le credenziali non si toccano.
- **Le tabelle si leggono dalle tabelle, non dalle tendine.** Le tendine sono paginate
  e sembrano complete (`interazione.md`, «Anche le tendine sono paginate»). Rotte e
  metodo in `tabelle-rotte.md`; il titolo della tab si confronta sempre.
- **Due fonti, due marcature.** Quello che leggi su Unicò si scrive `[letto GG/MM/AAAA]`;
  quello che ti dice l'utente `[detto dal titolare]`, `[detto dal commerciale]` e così via. Non mescolarle.
- **Una tabella lunga si riassume.** Bastano le voci in uso e il loro significato, non
  l'export integrale: il file deve restare leggibile in un minuto.

## Il giro, in quest'ordine

### 1. Le aziende dell'installazione

Dall'icona utente → *Sessione Corrente* leggi tenant e aziende (`mappa-web.md`). Poi
**chiedi** all'utente, azienda per azienda: è produzione o prova? Il nome non lo dice, e
un'azienda di prova può contenere lo storico vero.

Per quelle di prova, dai all'utente la riga da mettere nel suo profilo di shell
(`~/.zshrc` o `~/.bashrc`):

```bash
export UNICO3_SANDBOX="C<tenant>/A<n>"
```

Non la scrivi tu nel profilo: è lui che decide dove la skill scrive senza chiedere.
Stessa cosa per `UNICO3_AUTORIZZATE` (`crea_articolo`, guardrail §5.1-ter): di default
resta vuota, e si accende solo se il titolare lo dice. La variabile vale dalla sessione
successiva; fino ad allora ogni azienda è produzione.

### 2. Versione di Unicò

Annota la release (dalla pagina di login o da *Impostazioni*). I file di questa skill
sono stati misurati sulla release 2026.3 (`fatti-misurati.md`). Se la tua è diversa, ogni
procedura in `flussi/` va trattata come `[da verificare]` la prima volta che la usi.

### 3. Persone e ruoli

Chiedi all'utente, e scrivi per ruolo:

- chi dà l'ok alle scritture in produzione (il «titolare» dei file);
- chi fa il login a Unicò per la skill, e con quale utente;
- commerciale, ufficio tecnico, magazzino, amministrazione: chi sono e come li si raggiunge;
- se esiste un **operatore RDI** dedicato all'agente (tabella `OperatoreRdI`), o se va creato
  (lo crea una persona, o lo crei tu su sua richiesta esplicita).

Tecnici e squadre li leggi da `Tecnico` e `SquadraTecnici`: basta sapere che esistono e
quanti sono attivi, non serve copiarli. Questi numeri, come ogni conteggio della tua
azienda, vanno in `organizzazione.md`, non in `fatti-misurati.md` (che registra fatti
del programma).

### 4. La configurazione che cambia il lavoro

**Si legge azienda per azienda.** Tipologie, esiti, magazzini e listini sono configurazione
dell'azienda Unicò, non dell'installazione: due aziende dello stesso tenant possono averli
diversi (`crm-ticket.md`, «il grafo vero dell'ufficio»). Fai i punti 4 e 5 su ogni azienda di
produzione, e sulle sandbox dove la skill lavorerà; nel file ogni azienda ha la sua sezione,
intestata con `C<tenant>/A<n>`. Per cambiare azienda segui `mappa-web.md` e rileggi la URL
dopo ogni cambio.

Leggi queste tabelle e scrivi le voci in uso con il loro significato:

| Cosa | Rotta | Perché serve |
|---|---|---|
| Tipologie attività ufficio, con i loro esiti | `TipoAttivitaUfficio` | la catena del CRM: quali attività esistono, e per ogni esito l'`AzioneSuccessiva` e la destinazione |
| Tipologie RDI | `TipologiaRdI` | come nasce una richiesta d'intervento |
| Tipologie impianti | `TipologiaImpianto` | decide quali installati si possono appendere a un impianto (`flussi/nuovo-impianto.md`) |
| Tipologie intervento | `TipologiaIntervento` | cosa scrivere su un intervento |
| Tipologie operazioni di manutenzione | `TipologiaOperazioneDiManutenzione` | le sigle dei piani di manutenzione: sostituiscono gli esempi in `flussi/piani-manutenzione.md` |
| Tipologie contratti | `TipologiaContratto` | `flussi/contratti.md` |
| Magazzini | `Magazzino` | da quale magazzino si carica e si scarica |
| Causali movimenti | `CausaleMovimentoMagazzino` | carico DDT fornitore, resi |
| Listini | `Listino` | listino base, listini fornitore, listino di vendita |
| Numerazioni | `Numeratore` | quali registri esistono: **solo lettura**, una numerazione non si tocca |
| Tipologie documenti | `TipologiaDocumento` | i documenti di intervento in uso |

Per gli esiti: stanno dentro `TipoAttivitaUfficio`, uno per riga di dettaglio della
tipologia. Per ciascuno leggi `AzioneSuccessiva` (`ProgrammaAttivita`, `ChiudiTicket`,
`ApriRdI`) e, se programma un'attività, la tipologia indicata da
`IdTipoAttivitaDaProgrammare` (`crm-ticket.md`, «Il motore degli esiti»). Così copri anche le
tipologie che oggi non hanno pratiche aperte. Se la tabella è grande, l'export descritto in
`crm-ticket.md` dà la catena intera in un file; nell'organizzazione ne scrivi solo i passi in uso.
Chi fa ogni attività non sta nella tabella: chiedilo all'utente.

### 5. Gli articoli di servizio

Le procedure di preventivi e contratti (`flussi/preventivo-net.md`, `flussi/contratti.md`)
usano articoli che ogni azienda codifica a modo suo, scritti nei file come segnaposto:
`<ART_MANODOPERA>`, `<ART_MANODOPERA_PREV>`, `<ART_MATERIALE_PREV>`,
`<ART_MATERIALE_GENERICO>`, `<ART_DIRITTO_CHIAMATA>`, `<ART_TRASPORTO>`, `<ART_CANONE>`,
`<ART_MAN_PDC>`, `<ART_MAN_IBRIDO>`. Chiedi all'utente quali codici usa per ciascuno (o
leggili da un preventivo e da un contratto recenti, in sola lettura) e scrivili nella
tabella del modello. Quelli che l'azienda non usa si segnano «non usato».

### 6. Le abitudini che Unicò non dice

Chiedi all'utente, in poche domande:

- come si scrive il codice impianto nell'oggetto delle mail, nelle note, nei file;
- dove stanno le foto degli impianti (allegati del ticket, cartelle, app dei tecnici);
- quali aree di Unicò l'azienda **non** usa (così non ci perdi tempo);
- cosa non deve mai fare la skill, oltre alla zona rossa.

### 7. Chiudi

- Rileggi il file con l'utente: un minuto, non di più. Correggi quello che dice.
- Scrivi in testa la data e la release.
- Ricorda all'utente le righe di shell del punto 1, se ce ne sono.
- Se è installata anche `ufficio-acquisti-gfbc`, proponi di proseguire con il suo primo avvio
  (`ufficio-acquisti-gfbc/references/primo-avvio.md`): fornitori, prezzi, posta e autonomie
  non si raccolgono qui.

## Dopo il primo avvio

All'inizio di ogni sessione leggi `~/.config/unico3/organizzazione.md` **prima** degli
esempi dei `references/`, e della configurazione usa **la sezione dell'azienda letta dalla
URL**: dove il tuo file e gli esempi divergono, vale il tuo file. Se quell'azienda non ha
una sezione, non è censita: non prendere in prestito quella di un'altra azienda, dichiaralo
e proponi di completare il punto 4 per lei.

Quando scopri qualcosa:

- se riguarda **la tua azienda** (una sigla, un ruolo, un'abitudine): va in
  `organizzazione.md`, mai nei `references/`;
- se riguarda **Unicò** (una rotta, una trappola, un comportamento del programma): va nei
  `references/` secondo `apprendimento.md`. Sono file del repository: tienili in un tuo
  fork, o proponi la correzione a chi mantiene la skill.

Rifai il giro, anche solo in parte, quando cambia la release, quando entra una persona
nuova o quando una sigla letta non torna più.
