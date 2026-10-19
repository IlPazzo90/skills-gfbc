# CRM — ticket, attività, e come si incatenano

Mappato operando su una sandbox (Azienda 3), aprendo un ticket vero su un
impianto di prova. Quello che è stato osservato è dichiarato tale; quello che non è
stato verificato è marcato **[da verificare]** e non va usato come se fosse noto.

## Il modello

**Il ticket non si crea: si apre aprendo un'attività.** Non esiste una voce «nuovo
ticket» da nessuna parte. È un contenitore che raccoglie le attività fatte su un
impianto per una stessa faccenda, e serve a leggere una storia invece di righe sparse.

Nei dati la griglia è un **albero**: ogni nodo è `{ payload, children }`, il ticket è
il padre e le attività sono i figli.

- `IdTicket` — id interno (numerico, assegnato da Unicò)
- `NumeroTicket` — **è il numero della prima attività del ticket**
- `NumeroAttivita` — numero progressivo della singola attività (100001, 100002…)

Quindi la prima attività dà il nome al ticket, e le successive si accodano.

## Le tre attività

Dalla scheda impianto → **ATTIVITÀ** → pulsante `+`:

| Voce | `TipologiaAttivita` | Ticket |
|---|---|---|
| Nuova attività ufficio | `AttivitaUfficio` | può **aprirne uno nuovo** |
| Nuova richiesta di intervento | RDI | **obbligatorio** (campo con asterisco) |
| Nuovo intervento eseguito | intervento | [da verificare] |

Differenza che conta: **un'attività ufficio può nascere senza ticket e crearlo; una
RDI deve appartenere a un ticket già aperto.** È coerente col mestiere: la telefonata
apre il caso, la richiesta di intervento sta dentro un caso.

I tab sopra la griglia — `Tutti · Richieste di intervento · Interventi · Attività
ufficio` — filtrano per tipo, e l'interruttore **`Raggruppa per ticket`** decide se
vedere l'albero o l'elenco piatto.

## La macchina a stati

Cinque booleani nel payload:

| campo | significato |
|---|---|
| `IsProgrammabile` | può essere pianificata |
| `IsProgrammata` | ha una data di scadenza ed è assegnata |
| `IsEvasa` | è stata eseguita, ha un esito |
| `IsSospesa` | sospesa |
| `IsChiuso` | il **ticket** è chiuso |

Misurati sulle due attività del test:

| | prima attività | seconda attività |
|---|---|---|
| `IsEvasa` | **true** | false |
| `IsProgrammata` | false | **true** |
| `IsChiuso` | false | false |
| chi | `OperatoreEsecutore` = operatore di prova | `OperatoreAssegnato` = operatore di prova |
| quando | `DataEvasione` 03/09/2026 | `DataProgrammata` 04/09/2026 |

Due campi diversi per la persona, a seconda che l'attività sia da fare o fatta:
**assegnato** finché è aperta, **esecutore** quando è evasa.

`IsChiuso` era `false` su entrambe con una attività ancora aperta: **il ticket resta
aperto finché ha attività non evase.** [Non è stato verificato che si chiuda da solo
evadendo l'ultima.]

## L'incatenamento: è l'esito a generare l'attività dopo

È la parte che fa di questo un CRM e non un elenco.

Nel form, scegliendo `Evadi ora` compare il campo **Esito**. Selezionando
**«2. Da richiamare»** il dialogo **si trasforma in un wizard**: il pulsante diventa
`AVANTI` e compare un secondo passo, che è **una seconda attività ufficio già
precompilata** con tipologia **«3. PRENDI APPUNTAMENTO»**, sullo **stesso ticket**, in
modalità `Pianifica`.

Una conferma sola ha quindi creato **due attività e un ticket**: quella evasa e quella
che ne discende.

L'oggetto `Esito` porta due campi che spiegano il meccanismo:

- **`AzioneSuccessiva`** — il codice dell'azione da concatenare (valeva `"0"` per
  «2. Da richiamare»). **[La mappatura dei codici alle azioni non è stata
  ricostruita: non si assuma che "0" significhi "nessuna".]**
- **`IsRichiediFileAllegato`** — un esito può **pretendere un allegato** per essere
  registrato.

Esiti visti nel campo (elenco **non** completo, vedi la trappola sotto):
`1. Appuntamento · 2. Da richiamare · 3. Risolta telefonicamente ·
4. Consulenza Uff. Tec. · 5. Richiesta nominativo Installatore · 6. Annullato`.

Su A1 «0. TELEFONATA/MAIL IN INGRESSO» con esito
**«3. Da programmare»** fa lo stesso: AVANTI porta a una **URGENZA** in `Pianifica` sullo
stesso ticket. Quale esito porta a quale attività lo dice
la tabella delle tipologie (esiti con `AzioneSuccessiva` e destinazione). La seconda attività eredita data e ora
d'inserimento della prima. `Operatore RDI assegnato` arriva precompilato con chi
inserisce: per lasciarla senza assegnatario si sceglie **«Non selezionato»**, la prima voce
della tendina. Nel backend la telefonata ha un Id che è anche l'`IdTicket`, e
un `NumeroAttivita` che è il `NumeroTicket`; l'URGENZA ha Id e numero propri.

## Agganciare un'attività a un ticket aperto

Finché un ticket è aperto, il campo `Ticket` delle nuove attività lo elenca:

```
Apri nuovo ticket
APERTO Ticket 100001 Aperto il 03/09/2026
```

Prima che esistesse il ticket, il campo mostrava solo «Apri nuovo ticket». È così che
si tiene insieme la gestione di un cliente: tutte le attività della stessa faccenda
sullo stesso numero.

## Il flusso RDI, percorso per intero

Creata davvero su una sandbox, agganciata al ticket N. Wizard a **tre
passi**, e ognuno fa una cosa diversa.

### 1 — Dati generali

`Ricevuta il *` · `alle *` · `Operatore RDI *` (precompilato) · `Interlocutore RDI` ·
`Impianto *` · **`Ticket *`** · `Tipologia RDI` · `Motivo RDI` · `Tag RDI` · `Note` ·
caselle `Note importanti` e **`RCEE`**.

**`Richiamo` non è selezionabile.** La tabella `Tipologie RDI` ha tre voci — Normale,
Richiamo, Urgente — ma la tendina ne offre due: **Normale e Urgente**. Il richiamo non
si sceglie, **nasce** quando il cliente chiede di rimandare, ed è quello che il flag
`IsRichiamo` marca. Una regola di dominio che si vede solo provando.

### 2 — Operazioni di Manutenzione

L'albero dell'installato con, per ogni macchina, `Operazioni Straordinarie` e
`Operazioni Ordinarie`, e per ciascuna operazione: **Periodicità · Ultima Esec. ·
Scad. Legale · Scad. Progr.** — le due scadenze distinte del dominio, affiancate.
**Le operazioni scadute hanno la riga rosa.**

Su GT1 dell'impianto di prova: Manutenzione ordinaria (Annuale, scaduta), Analisi
combustione (Biennale), Rilascio bollino (Quadriennale) — cioè MO, AF e RB.

Spuntando un'operazione compare **`Durata Stimata: 01:00 → 01:00`**: a sinistra quella
calcolata dalle operazioni scelte, a destra quella modificabile. **È il legame
operazioni → durata → lunghezza dello slot in agenda.**

Qui si decide anche cosa verrà spuntato a intervento eseguito, e quindi — vedi
`dominio.md` — **quali scadenze successive verranno generate**.

### 3 — Pianificazione

L'agenda dentro il form: `Tecnico *` (di default **`# Non segnalato`**, il valore
precodificato), `Aiutanti/orari aggiuntivi`, `Giorno`, **`Tipo programmazione *`** —
**Ora precisa · Mattino · Pomeriggio · Qualsiasi ora**, cioè la promessa fatta al
cliente — `Ora`, `Durata` (ereditata dal passo 2), **`Zona` dedotta dall'impianto**,
`Luogo operazione`, `Programmata Da`, e il calendario del giorno con lo slot
evidenziato.

Quattro caselle che pesano: `Blocca cambio tecnico` · `Blocca cambio orario` ·
**`Avvisare cliente`** · `Non visibile da mobile`. La terza fa uscire una
comunicazione verso il cliente: **si tocca solo se richiesto esplicitamente.**

Confermando compare una seconda conferma, **`Sposta Impegni`**, che assegna l'impegno
al tecnico scelto.

### Risultato

RDI creata su `#/assistenza/impianto/<idImpianto>/attivita/RdI/<id>`, *Normale*, assegnata
a *Non segnalato* il 03/09/2026 alle 10:00, durata 1h, luogo Impianto, con
l'operazione *Manutenzione ordinaria su GT1* agganciata, dentro il ticket N.

Il contatore nel menu diventa **`ATTIVITÀ ①🔧 ①🎧`**: due conteggi separati, interventi
e attività d'ufficio.

## L'intervento eseguito, e la regola che regge tutto il ciclo

Wizard a **due passi**: `Dati intervento` → `Operazioni di Manutenzione`.

**1 — Dati intervento**: `Data *` · `Ora inizio` · `Durata` · `Tecnico *` ·
**`CAT *`** (su una sandbox multi-società è la società del gruppo che esegue) · **`Tipologia intervento *`**
· `Descrizione` · `Note` · casella **`Ritorno`**.

**Non c'è il campo Ticket.** E infatti l'intervento creato **non è finito nel ticket**:
sta nell'elenco dell'impianto insieme allo storico, che ha anch'esso la colonna TICKET
vuota. Gli interventi vivono sull'impianto; il ticket lega le attività d'ufficio e le
richieste, non l'esecuzione.

Le tipologie intervento sono **sigla + descrizione**, raggruppate per famiglia dal
prefisso, per esempio **`C-`** condizionamento, **`G-`** gas/riscaldamento, **`R-`**. Le sigle
sono configurazione della singola azienda. Una tendina lunga non mostra tutto alla prima
pagina: si legge per intero prima di concludere che una famiglia non c'è.

**2 — Operazioni di Manutenzione**: lo stesso albero del passo 2 della RDI, ma qui le
date hanno l'icona del calendario, cioè **sono modificabili**.

### La regola, misurata

Spuntando `Manutenzione ordinaria` (Annuale) su un intervento datato 03/09/2026, le
date si sono ricalcolate **prima ancora di salvare**:

| | prima | dopo la spunta |
|---|---|---|
| Ultima Esec. | 31/12/2024 | **03/09/2026** |
| Scad. Legale | 31/12/2025 | **03/09/2027** |
| Scad. Progr. | 31/12/2025 | **03/09/2027** |

Cioè: **l'ultima esecuzione diventa la data dell'intervento, ed entrambe le scadenze
si spostano di una periodicità in avanti.** Le nuove date restano modificabili a mano.

Confermando, la scheda impianto si aggiorna: `Manutenzione ordinaria (Annuale)
03/09/2027`, e **la riga non è più rossa** — l'impianto non risulta più scaduto.

È la verifica sul campo della regola di `dominio.md`: **se le operazioni non vengono
spuntate, le scadenze successive non vengono generate.** Un intervento registrato senza
spuntare non fa avanzare niente, e l'impianto resta scaduto pur essendo stato visitato.

### Cosa l'intervento *non* fa

**Non evade la RDI.** Dopo aver creato l'intervento il contatore restava `①🔧`, con la
richiesta ancora aperta. Le due cose vanno chiuse separatamente. [Come si evade una
RDI: non ancora verificato.]

## Come le attività finiscono in Agenda

**Il pannello di sinistra dell'Agenda contiene solo gli impegni NON programmati.** La
cartella `Richieste Intervento` risultava **vuota** dopo aver creato la RDI, perché
quella era già pianificata: da lì passa al calendario a destra. Colonne della cartella:
`DataInserimento`, `DataProgrammata`, `OraProgrammata`, `Tipologia`, `Motivo`,
`OperatoreInserimento`, `OperatoreProgrammazione`, `Interlocutore`, `Tecnico`,
`Numero`, `Impianto.Codice`, `Impianto.Nominativo`.

**Trappola seria: il calendario mostra solo i tecnici della vista.** L'appuntamento
assegnato a `Non segnalato` **non compare**, perché quel tecnico non è fra quelli della
vista corrente (l'elenco sta nella query, parametro `Tecnici`). *Non lo vedo* non
significa *non c'è*: prima di dire che un appuntamento manca, si controlla quali
tecnici sono in vista.

Le viste sono gruppi salvati, scelti dal menu accanto alla data: **Default · Singolo ·
Personalizzata · una vista per CAT o per gruppo di tecnici**. L'icona «aggiungi
tecnico» **non aggiunge alla vista: crea un nuovo gruppo tecnici**, cioè configurazione
persistente — da non premere per curiosità.

## Le tabelle che governano il flusso

### `Tipologie attività ufficio` → `#/tabelle/TipoAttivitaUfficio/table`

Le voci sono configurazione dell'azienda (ne esistono decine). Colonne:

| campo | cosa decide |
|---|---|
| `Descrizione` | il nome |
| `IsPianificabile` | se l'attività può essere **pianificata** o solo evasa subito |
| `IsVisibileMobile` | se il tecnico la vede dall'app |
| `IsInseribileMobile` | se il tecnico può **crearla** dall'app |
| `IsEsclusoDaListe` | ritiro dalla scelta senza perdere lo storico |
| `CodiceExport` | codice per l'esportazione |

La tassonomia è quella vera dell'ufficio, e si legge come un processo:

Le tipologie sono **configurazione della singola azienda**: ogni azienda ha le sue.
Quella usata per i test è organizzata così, come esempio:

- **numerate, in ingresso** — `0. TELEFONATA/MAIL IN INGRESSO` (l'unica con
  `IsPianificabile: false`, perché una telefonata la registri, non la pianifichi),
  poi urgenze per tipo di impianto, `PROPOSTA MANUTENZIONE`, `PRENDI APPUNTAMENTO`,
  `ELABORAZIONE PREVENTIVO`, `RECLAMO CLIENTE`
- **non numerate, di lavorazione** — attese (`ATTESA OFFERTA FORNITORE`),
  non conformità, amministrazione (`CONTROLLO SALDO`, `INVIO SOLLECITO VIA MAIL`),
  pratiche (`FARE PRATICA ENEA`), qualità (`GESTIONE FEEDBACK NEGATIVO`).

Solo una piccola parte è creabile (`IsInseribileMobile`) o visibile (`IsVisibileMobile`)
da mobile: l'app dei tecnici vede una fetta stretta di questo mondo.

### Tabelle usate dalla RDI — lette

Il form `Nuova richiesta di intervento` (wizard: `Dati generali` → `Operazioni di
Manutenzione` → `Pianificazione`) attinge a queste, più le caselle `Note importanti` e
**`RCEE`** (rapporto di controllo efficienza energetica):

| Tabella | Rotta | Contenuto |
|---|---|---|
| Tipologie RDI | `#/tabelle/TipologiaRDI/table` | **Normale · Richiamo · Urgente** |
| Motivi RDI | `#/tabelle/MotivoRDI/table` | configurazione dell'azienda |
| Tag RDI | `#/tabelle/TagRDI/table` | p.es. ANTICIPABILE · NON SPOSTARE |
| Interlocutori RDI | `#/tabelle/InterlocutoreRDI/table` | FAMILIARE · INQUILINO · INSTALLATORE · PROPRIETARIO · RESPONSABILE · VICINO DI CASA |
| Operatori RDI | `#/tabelle/OperatoreRDI/table` | nomi dell'ufficio, con il CAT di appartenenza |
| Tecnici | `#/tabelle/Tecnico/table` | Sigla, CAT, contatti, **`LivelloLicenza`**, **`ListaMateriale`**, colore |

**`Tipologie RDI` porta il flag `IsRichiamo`**, ed è il ponte con l'Agenda: una RDI di
tipo *Richiamo* è quella che finisce nella cartella `Richiami` degli impegni. I `Tag
RDI` sono istruzioni per chi pianifica — *ANTICIPABILE*, *NON SPOSTARE* — non
etichette decorative.

Quasi tutte le tabelle portano `CodiceExport` e `CategoriaAnalytics`: sono pensate per
essere aggregate nei cruscotti, non solo per riempire tendine.

### Il censimento delle tabelle

L'albero ha circa settanta tabelle, elencate per
area in `mappa-web.md`.

**Le rotte non seguono le etichette in modo affidabile.** `Zone` → `Zona`,
`Tipologie attività ufficio` → `TipoAttivitaUfficio`, `Tipologie RDI` →
`TipologiaRDI` — ma `TipoRDI`, `TipoIntervento`, `TipoOperazioneManutenzione` e
`Numerazione` **non esistono**. Il nome dell'entità non sta in nessun attributo del
DOM: la rotta la costruisce il codice al click. Quindi per una tabella non ancora
vista si arriva **dall'albero**, e la rotta la si annota dopo averla letta dalla URL.

### Dove stanno gli esiti

**Non individuata.** Fra le tabelle non c'è una voce «Esiti»: probabilmente gli
esiti sono figli della tipologia di attività, il che spiegherebbe perché portano
`AzioneSuccessiva`. **Da verificare aprendo il dettaglio di una tipologia.**

## La trappola che vale per tutto il resto: le tendine sono paginate

**Una tendina non mostra tutti i valori.** Misurato: il campo `Tipologia attività
ufficio` rende **17 elementi** (16 opzioni + «Aggiungi elemento») su un centinaio esistenti.
Digitando un filtro compaiono voci che nella prima pagina non c'erano.

È lo stesso difetto della griglia virtualizzata, e porta allo stesso errore: leggere
`[role="option"]` e credere di avere l'elenco. Ci si casca facilmente: si riporta «16 tipologie» come se fossero tutte.

**Regola: per sapere quali valori esistono si legge la tabella, non la tendina.** La
tendina serve a scegliere, la tabella a conoscere. Se serve cercare dentro la tendina,
si digita un filtro e si legge il risultato filtrato.

Nota di contorno: in fondo alla tendina c'è **«Aggiungi elemento»**, cioè la creazione
al volo di una voce di tabella dal campo — quella descritta nel wiki. È una scrittura
in tabella fatta da dentro un form: va trattata come tale.

## Altre cose osservate operando

- L'**Operatore RDI** è precompilato con l'operatore dell'utenza con cui si è entrati:
  l'attività risulta a lui, non a un utente generico.
- `Pianifica` con solo la data mette l'ora a **23:59**.
- La voce di menu diventa **`ATTIVITÀ ①`** con il contatore delle attività aperte.
- **`ANNULLA` su un form compilato apre una conferma** — *«I dati inseriti e non
  salvati andranno persi. Continuare?»* con `RITORNA` / `ESCI`. Finché non si risponde
  il form resta aperto: chi non se ne accorge crede di aver chiuso e continua a
  cliccare su un dialogo ancora vivo.
- Aprendo il dettaglio di un'attività la rotta diventa
  `#/assistenza/impianto/<idImpianto>/attivita/AttivitaUfficio/<idTicket>`.

## Cosa resta da mappare

- I passi 2 e 3 del wizard RDI (`Operazioni di Manutenzione`, `Pianificazione`).
- Il flusso `Nuovo intervento eseguito`, e il legame con le operazioni di manutenzione
  spuntate — che è il perno delle scadenze successive (vedi `dominio.md`).
- Come si **chiude** un ticket.
- I codici di `AzioneSuccessiva` e la tabella degli esiti.
- Il contenuto di `Tipologie RDI`, `Motivi RDI`, `Tag RDI`, `Interlocutori RDI`,
  `Operatori RDI`, `Anomalie intervento`, `Motivi ritorno intervento`,
  `Voci validazione intervento`.
- Come le attività aperte compaiono in **Agenda** (le sei cartelle degli impegni).

## Cosa è stato scritto sulla sandbox

Un ticket su un impianto di prova, con due attività ufficio e una RDI:

- **prima attività** — `0. TELEFONATA/MAIL IN INGRESSO`, evasa, esito
  «2. Da richiamare»
- **seconda attività** — `3. PRENDI APPUNTAMENTO`, aperta, con scadenza il giorno dopo alle 23:59,
  assegnata all'operatore di prova
- **RDI `RdI/<id>`** — *Normale*, programmata 03/09/2026 ore 10:00, 1h, tecnico
  *Non segnalato*, con l'operazione *Manutenzione ordinaria* su GT1

E fuori dal ticket, sullo stesso impianto:

- **Intervento `Intervento/<id>`** — `G-.Manutenzione ordinaria`, 03/09/2026, tecnico
  *Non segnalato*, con l'operazione *Manutenzione ordinaria* spuntata.

**Questo intervento ha cambiato dati dell'impianto**, ed è l'unica scrittura di questa
sessione che tocca qualcosa di diverso da una nota: su GT1 la manutenzione ordinaria è
passata da *ultima 31/12/2024, scadenza 31/12/2025* a **ultima = data dell'intervento, scadenza
= data + un anno**, e l'impianto non risulta più scaduto. Era il solo modo di verificare la
regola; se un domani quelle date dovessero tornare com'erano, si correggono a mano dal
piano di manutenzione.

Le note di entrambe cominciano con **«TEST AUTOMAZIONE 03/09/2026 - NON EVADERE»**.
Tenute come riferimento. **Il ticket è aperto**: finché
la seconda attività non viene evasa, l'impianto risulta con un'attività pendente.

---

# Il motore degli esiti, misurato

Aggiunto il 03/09/2026 leggendo `#/tabelle/TipoAttivitaUfficio/table` su una sandbox: centinaia di esiti,
nessuna tipologia senza esiti.

**`AzioneSuccessiva` ha tre valori letterali, e sono tutti qui:**

| Valore | Cosa fa |
|---|---|
| **`ProgrammaAttivita`** | apre un'**altra attività ufficio**, della tipologia indicata da `IdTipoAttivitaDaProgrammare` |
| **`ChiudiTicket`** | **chiude il ticket** |
| **`ApriRdI`** | apre una **richiesta di intervento** |

**Non esiste un pulsante «chiudi ticket».** Un ticket si chiude **solo** evadendo
un'attività con un esito la cui azione successiva è `ChiudiTicket`. Se la tipologia in
corso non ne ha uno, quel ticket **per costruzione non può chiudersi lì**: va portato
avanti fino a una tipologia che ne ha.

Le tipologie sono legate da molti collegamenti di catena: è il processo
dell'ufficio scritto in tabella, non nella testa delle persone.

**Quasi tutte le tipologie hanno almeno una via di chiusura.** Le poche **che non ce l'hanno**
non sono un errore — sono **passi intermedi**, e si riconoscono dal nome:

Per esempio: telefonate e mail di RDI, apertura di una non conformità, attese di una
telefonata del cliente, solleciti, riassegnazioni, rielaborazione di un allegato.

Attese, verifiche e solleciti: **spingono avanti, non chiudono**. Se qualcuno chiede
perché un ticket è aperto da settimane, la risposta sta spesso qui.

Dalla stessa lettura: quasi tutte le tipologie sono pianificabili, poche sono
inseribili da mobile (si conta `IsInseribileMobile` sulla tabella intera, non su una
lettura parziale), e **pochissimi esiti** hanno `IsRichiediFileAllegato`.

## Le tipologie intervento — `#/tabelle/TipologiaIntervento/table`

⚠️ **La rotta è `TipologiaIntervento`, al singolare.** `TipoIntervento` non esiste, e una
rotta sbagliata **lascia in silenzio la pagina precedente**.

Le tipologie sono organizzate per prefisso — è la tassonomia con cui si legge tutto lo
storico interventi:

| Prefisso | Area |
|---|---|
| **`R-`** | Riscaldamento |
| **`C-`** | Condizionamento |
| **`G-`** | Installazione / società del gruppo |
| **`Z-`** | tecnico (feedback disabilitato) |

Dentro ogni famiglia si ripete lo stesso schema: *Manutenzione ordinaria* · *Intervento
straordinario* · *Intervento in garanzia* · *Intervento non eseguito* · *Lavoro da
preventivo* · *Prima accensione* · *Sopralluogo* · *Non conformità*.

Le varianti che esistono **solo su Riscaldamento** raccontano il lavoro vero:
varianti come `R-.Manutenzione caldaia RAPIDA`, `R-.Ritorno per incasso saldo`, `R-.CRITER`, `R-.Consegna lettera`,
`R-.Prima accensione <tecnico>` e `R-.Sopralluogo <tecnico>`.

Campi per tipologia, oltre a quelli della guida: **`Sigla`** (è quella che si colora nella
creazione RdI), **`Colore`** (`#03A9F4` e simili), **`AreaAnalytics`** e
**`CategoriaAnalytics`** — *sono queste due che reggono i grafici, non la descrizione* —,
**`IsManutenzionePerAnalytics`** (attivo su tutte e tre le manutenzioni ordinarie più le
due varianti caldaia), **`TipoFeedback`** (`Standard` o `Disabilitato`), `IdListaMateriale`,
`CodiceExport`.

E uno che nella guida non c'è: **`IsRiprogrammaPrimaAccensione`**, attivo **solo sulle
quattro «Prima accensione»**. È il meccanismo per cui una prima accensione **riprogramma**
invece di limitarsi a registrare.

---

# Chiusura: percorsa e misurata su una sandbox

Il ticket lasciato aperto apposta è stato portato a chiusura. Ecco cosa succede
davvero, passo per passo.

## Evadere una RDI

Dal ticket si seleziona la riga della RDI: il pannello di destra si apre con, in alto,
**⋮ · ✓ · ✏️ · ✕** — la **✓ è «evadi»**.

Dialogo **`Evasione richiesta di intervento`**, un solo passo (`Dati Evasione`):

| Campo | Note |
|---|---|
| Impianto | in sola lettura |
| **Ticket** | mostrato come **`<numero> (proseguito)`** |
| **Evasa il / alle** \* | precompilati a adesso |
| **Operatore RDI** \* | precompilato |
| **Esito** \* | **obbligatorio** |
| ☐ **Inserisci intervento** | se spuntata, il wizard prosegue con l'intervento |

**Gli esiti di una RDI sono una tabella a sé**, diversa da quella delle attività ufficio.
Sono una ventina nell'azienda di prova, e raccontano l'esito tecnico dell'uscita:

Esempi (configurazione dell'azienda): `1.0 Risolto` · `1.1 Risolto - Pagamento da
incassare` · `2.0 Da tornare per completare lavoro` · `3.0 Da tornare per installazione
ricambio` · `4. Da tornare in seguito a preventivo` · `6.0 Sopralluogo eseguito` ·
`7. Caldaia da sostituire`

Confermando con **`1.0 Risolto`** e **senza** spuntare *Inserisci intervento*:

- il **badge 🔧 sparisce** dalla voce ATTIVITÀ (contava le RdI aperte non sospese)
- **il ticket resta aperto** e viola, perché ha ancora un'attività non evasa

## La scoperta sulle parentesi angolari

Prima dell'evasione la riga della RdI mostrava
`<03/09/2026 10:00>` · `<Non segnalato>` · `<Richieste di intervento>` · `<PROG.>`.
Dopo l'evasione: `<data/ora effettive>` · `<operatore>` · `Richieste di intervento`.

> **Le parentesi angolari `< >` marcano i valori *programmati* di un'attività non ancora
> evasa.** Evadendo diventano i valori *effettivi* e le parentesi spariscono.

È un modo rapido e affidabile di distinguere previsto ed eseguito leggendo la griglia,
senza aprire nulla. E l'esito `<PROG.>` **non è un esito**: è il segnaposto di
un'attività programmata.

## Evadere un'attività ufficio, e chiudere il ticket

Stessa ✓ sul pannello dell'attività. Dialogo **`Evadi - <nome tipologia>`**, con in più
rispetto alla RdI: **Interlocutore RDI**, il campo **Note** già pieno, e una sezione
**FILES ALLEGATI** con `+ · ✏️ · 🗑 · ⬇` — è lì che finisce l'allegato quando l'esito ha
`IsRichiediFileAllegato`.

Gli esiti di `3. PRENDI APPUNTAMENTO` sono **sei**: `1. Appuntamento` ·
`2. Non risponde` · `3. Da richiamare` · `4. Non risponde mai` · `5. Riassegna attività` ·
`6. Annullato`.

Scelto **`6. Annullato`** il dialogo **non aggiunge passi** — solo `ANNULLA` e `CONFERMA`.
*Questa è la spia da guardare*: se l'esito incatenasse qualcosa, comparirebbe un secondo
passo con l'attività o la RdI già precompilata.

**Dopo la conferma, verificato nel modello della griglia (non a occhio):**

```
NumeroTicket: <n>
IsChiuso: true      IsEvasa: true
figli: [ {esito: "1.0 Risolto",     evasa: true, chiuso: true},
         {esito: "2. Da richiamare", evasa: true, chiuso: true} ]
```

E a schermo: **la voce ATTIVITÀ non ha più alcun badge**, il gruppo del ticket si
collassa e perde il viola.

## Il riassunto che serve ricordare

1. **Un ticket non si chiude: si esaurisce.** Si chiude quando l'ultima attività viene
   evasa con un esito la cui `AzioneSuccessiva` è `ChiudiTicket`.
2. **Evadere la RdI non chiude il ticket.** Toglie il badge 🔧 e basta.
3. **L'esito è sempre obbligatorio**, sia sulle RdI sia sulle attività.
4. **Il campo `Ticket` dice `(proseguito)`** quando l'attività ne continua uno esistente.
5. **Un dialogo di evasione che resta a un passo solo non incatena nulla.** Se compare un
   secondo passo, Unicò sta per creare un'altra attività o una RdI: si legge prima di
   confermare.

**Stato lasciato sulla sandbox:** ticket **chiuso**, RdI evasa con `1.0 Risolto`,
seconda attività evasa con `6. Annullato`. Le note «TEST AUTOMAZIONE» restano come traccia.
L'intervento N resta fuori dal ticket, come da regola.

## Su A1, 09/10/2026 — il grafo vero dell'ufficio

Il numero e i nomi delle tipologie cambiano da azienda ad azienda: sono configurazione. La tabella intera, con esiti, `AzioneSuccessiva` e destinazione, si esporta dalla tabella e dà il flusso reale dell'ufficio. Esempio di differenza fra due aziende: «0. TELEFONATA/MAIL IN INGRESSO» (esiti da 1. a 9.), «1. PROPOSTA MANUTENZIONE» (non «2.0» come altrove).

Falle misurate:
- **Alcuni esiti possono puntare a tipologie che non esistono più** (id di destinazione senza riga nella tabella): si cercano incrociando `IdTipoAttivitaDaProgrammare` con gli id delle tipologie.
- Una tipologia può non avere esiti: l'attività non si chiude da lì.
- Un ciclo di passi intermedi può non avere un esito di uscita (rinuncia, revoca): da verificare sul grafo.

Le attività aperte in agenda vengono dal backend `assistenza/QueryAttivitaUfficio`, nella scheda «Attività ufficio» dell'agenda. La griglia dà `TipologiaAttivita.Descrizione`, `DataProgrammata` e `OperatoreAssegnato`, ma è filtrata a «assegnata a me o non assegnata» e alla finestra di date nella URL.
