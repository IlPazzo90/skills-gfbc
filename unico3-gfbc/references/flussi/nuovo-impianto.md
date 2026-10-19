# Flusso 3 — Creare un impianto da zero

**Eseguito su una sandbox.** Risultato: un impianto di prova,
con un'anagrafica di prova, GT1 Immergas VICTRIX ZEUS 26 ErP con matricola di prova
e piano di manutenzione ordinaria annuale.

Sono **tre creazioni distinte**, non una: anagrafica+impianto, installato, piano di
manutenzione. **Fermarsi alla prima lascia un impianto che non entrerà mai in un giro di
manutenzione.**

---

## Dove si parte

`Assistenza → Azioni → Nuovo impianto`. Dalla home c'è anche il collegamento rapido
**`+ Nuovo impianto`**, che apre lo stesso wizard.

**Prima di creare un'anagrafica, si cerca se esiste già.** Il passo 1 ha due schede:
`Scegli anagrafica` cerca in rubrica, `Inserisci anagrafica` ne crea una nuova. Digitare
il cognome nella prima costa cinque secondi ed evita un doppione — che poi si porta
dietro documenti e impianti su due schede diverse. Se non c'è, risponde
*«Nessun risultato»*. Il filtro parte **solo dopo un tasto in più**: col cognome scritto
tutto resta su «Caricamento...»; si cancella l'ultima lettera e la si riscrive
(`interazione.md`) [sandbox, 15/10/2026].

Un'anagrafica esistente si apre anche per rotta, `#/amministrazione/anagrafica/<Id>/dati-fiscali`,
dove `<Id>` è l'identificativo interno e **non il codice**:
La tab aperta dice «ANAGRAFICA <codice> <nominativo>». Nel wizard invece si
sceglie leggendo codice e nominativo [sandbox, 15/10/2026].

⚠️ Cliccando `Azioni` **la tab corrente viene riusata**, non se ne apre una nuova: se
avevi una ricerca aperta lì, la perdi. Aprire prima una tab nuova se serve tenerla.

---

## Wizard 1 — Nuovo impianto, 5 passi

### 1. Dati anagrafica

`Scegli anagrafica` (da rubrica) oppure **`Inserisci anagrafica`**. Poi:
Fisica/Giuridica · **CAT** · `Ditta indiv./profess.` · Cognome\* e Nome\* · CF · Email ·
PEC · Comune · Indirizzo e civico · tre telefoni con **tipo cliccabile**
(Fisso/Cellulare/Fax) · **CONSENSO PRIVACY** (`Prestato`/`Negato` + data) e
`Informativa consegnata`.

Il consenso privacy si registra **qui, alla creazione**. Se non lo si mette adesso resta
vuoto e nessuno ci torna.

⚠️ **Il comune si sceglie leggendo CAP e provincia, non il nome.** In tabella possono esistere
due voci con lo stesso nome, una con provincia e una senza. Prendere il secondo
significa mandare i tecnici in un'altra regione, sbagliare **ente di controllo**,
**durezza dell'acqua** e **tipo di RCEE** — che nella tabella Comuni dipendono dal comune.

Il Comune è un `x-select-trigger` con filtro. Un capoluogo rende più righe, una
per CAP, nella forma «<CAP> <COMUNE> <PR>», e in fondo **«Aggiungi elemento»**, che crea un
comune nuovo in tabella. Si prende la riga col CAP dell'indirizzo [sandbox, 15/10/2026].

⚠️ La tendina dei CAT qui mostrava **due** voci, mentre il
modello interno ne elenca tre. **Ciò che è selezionabile in un punto può essere un
sottoinsieme**: non dedurre l'elenco da un'altra schermata.

### 2. Ruoli

`Occupante` è **già spuntato**. Gli altri: Proprietario · Amministratore · 3° responsabile ·
Progettista · Installatore · **Cliente** · Referente · Conduttore · Titolare Fornitura.
Più `Data inizio incarico`.

**`Cliente` è il ruolo che conta per fatturazione e per la spia dei saldi**: se manca,
l'impianto non ha un intestatario e i documenti vanno compilati a mano.

### 3. Figure

Quattro: **Responsabile**, **Dest. corrispondenza**, Utilizzatore FGAS, Referente FGAS.
Le prime due arrivano già impostate su `Occupante` — è l'effetto delle
*Impostazioni → Assistenza → Riferimenti*.

**`Dest. corrispondenza` è chi riceve le mail delle stampe.** Vale la pena guardarlo
adesso, non quando una comunicazione è già partita alla persona sbagliata.

`Utilizzatore FGAS` si sceglie fra i ruoli spuntati al passo 2: per una pompa di calore
il cui registro F-gas è intestato al proprietario si mette `Proprietario` [produzione,
14/10/2026, impianto N].

### 4. Dati impianto

- **`Origine nominativo impianto con nominativo di questa anagrafica`** — spuntandola il
  Nominativo si compila da solo (con un badge che dice **da quale ruolo** l'ha preso) e
  arrivano anche i telefoni.
- ⚠️ **`Tipologia impianto` arriva precompilata con l'ultima usata** — nel mio caso
  `Condizionamento`, che non c'entrava niente. **Va guardata ogni volta.** Non è un
  dettaglio estetico: **la tipologia decide quali installati si potranno appendere**.
- `Combustibile`, `CAT`.

Esempio di configurazione, da adattare: le tipologie sono tre: `Condizionamento` (esclusa dalle liste), `Impianto
Industriale`, `Impianto Residenziale` (privato o condominio → Residenziale, società →
Industriale). **`Impianto Residenziale` precarica sull'impianto tre voci da caldaia**
(Manutenzione generatore calore annuale, Analisi combustione e Rilascio bollino biennali)
anche quando la macchina è una pompa di calore: vanno convertite, vedi il piano più sotto.
In sandbox, con la RES copiata da produzione il 14/10, la precarica **non arriva**: gli impianti
creati in sandbox avevano il nodo Impianto senza voci. Non viene da
`OpManDefault`, vuota in produzione e in sandbox. Nella scheda impianto la tipologia si legge per
descrizione («Impianto Residenziale»), non per sigla [sandbox, 15/10/2026].
In produzione non esiste un combustibile elettrico: per una pompa di calore il campo resta vuoto,
senza «Aggiungi elemento» [produzione, 14/10/2026].

⚠️ Cercando un valore che **non esiste**, l'unica voce proposta è **`Aggiungi elemento`**:
cliccarla **crea una voce nuova in tabella**. Mi è successo digitando
`Riscaldamento semplice`, che su una sandbox non esiste. Le tipologie vere erano
`Riscaldamento Alta Potenza`, `Riscaldamento complesso <35 kW`, `Riscaldamento complesso
>35 kW`. **Se compare solo «Aggiungi elemento», il termine è sbagliato: si riformula, non
si crea.**

*(La soglia 35 kW non è cosmetica: sopra, la scheda intervento chiede il **numero di
rapporto di controllo CT**.)*

### 5. Indirizzo impianto

Precompilato dall'anagrafica. In più: **`Zona *`** (obbligatoria, default `Nessuna`),
Palazzo, Piano, Scala, Interno, Citofono.

Le zone sono aree configurate dall'azienda (es. `Zona1`, `Zona2`,
`Zona3`…): si sceglie guardando il punto
sulla mappa. La «ZONA A» che compare nell'intestazione di alcuni impianti è un'altra
cosa, non questo campo.

La mappa di questo passo chiede a `maps.gstatic.com` due risorse (`/mapfiles/openhand_8_8.cur`,
`/mapfiles/transparent.png`) e fa qualche `POST` a `maps.googleapis.com`. Chi filtra la rete
deve lasciar passare le due GET; i POST si possono scartare, il salvataggio passa lo stesso
[sandbox, 15/10/2026].

⚠️ Senza comune e indirizzo la fascia arancione dice **«Dati mancanti»**; se l'indirizzo
c'è ma Google non lo riconosce dice **«Coordinate non precise, se possibile inserire
manualmente»**. Sono due stati diversi della stessa fascia. È lo stesso avviso che il tecnico vedrà in
mobile. Su un impianto vero **si sistema subito**, con la matita sulla mappa: dopo, il
navigatore del tecnico manda a un punto sbagliato.

`CONFERMA` è una sola `PUT …/CreazioneImpianto` (risposta 200). Nel corpo il client mette
valori che il wizard non chiede: `IdCAT` 1 (in testa e nell'intestazione), `IsPrivata`
true, `CategoriaSdI` «Privato», `TipoTelefono1/2/3` Fisso/Cellulare/Fax (sia in
`RecapitiTelefonici` sia in `Telefoni`), il ruolo con `TipologiaRiferimento` «Occupante» e
i flag `IsResponsabileImpianto`, `IsDestinatarioCorrispondenza`, `IsOrigineDatiImpianto` a
true, `Indirizzo.IdZona` 1 («Nessuna») [sandbox, 15/10/2026, anagrafica nuova persona fisica].
Con **Cliente** spuntato accanto a Occupante, `ListaInfoRuoli` ha **due elementi** della stessa forma: il secondo con `TipologiaRiferimento` «Cliente», il suo `IdRiferimento.UUID`, le sue chiavi in `RuoliUnici` e `DettagliRiferimento` con `Note` vuota e `DataInizioIncarico` null [sandbox, 16/10/2026, impianto N, anagrafica nuova persona fisica, salvato e riletto senza differenze].

Poi si apre la scheda impianto, rotta
`#/assistenza/impianto/<idInterno>/dettagli/IMP/piano-di-manutenzione`.

> **L'id nella rotta non è il codice impianto.** Qui: la rotta usa un id interno, diverso dal codice mostrato
> nell'intestazione. Per parlare con una persona si usa il codice; per navigare, l'id.

---

## Wizard 2 — L'installato

Nella scheda ci sono **due `+` rosa**: quello **a sinistra sotto l'albero** aggiunge un
**installato**, quello **a destra** aggiunge una riga al **piano di manutenzione**.

La barra `Gruppo Termico | Bruciatore | Gruppo Frigo | UIR | Componente` del «Nuovo
installato» è fatta di **filtri accesi o spenti**, non di schede: un click su una voce
accesa la **esclude**. Sotto un GF, «+ Nuovo installato figlio» accende solo `UIR` e
`Componente`: per un'unità interna si spegne `Componente` e restano Marca\* e Modello
UIR\* [produzione, 14/10/2026].

### La prova che la tipologia vincola

Con `Riscaldamento complesso <35 kW` il selettore mostrava attivi solo
**`Gruppo Termico`** e **`Componente`**; `Bruciatore`, `Gruppo Frigo` e `UIR` erano
**disabilitati** — il bruciatore perché va **dentro un GT**, gli altri perché la classe
della tipologia non li prevede.

Se al passo 4 avessi lasciato `Condizionamento`, **non avrei potuto installare la
caldaia**. Ed è così che ci si accorge dell'errore: tardi.

### ⚠️ La trappola del modello omonimo

Cercando `victrix zeus` la lista propone, con la **categoria in testa a ogni riga**:

```
Gruppo Termico   VICTRIX ZEUS 26 KW   3.020239   Immergas S.p.A.
Componente       VICTRIX ZEUS 26 KW   3.020239   Immergas S.p.A.
```

**Lo stesso apparecchio esiste come Gruppo Termico e come Componente.** Sceglierlo come
Componente significa che **non è una caldaia**: niente scheda tecnica GT, niente RCEE,
piano di manutenzione diverso. La riga sembra identica.

**Difesa**: dopo la scelta, il campo mostra un **badge con la categoria**. Va letto prima
di confermare.

### ⚠️ La tendina dei modelli mostra meno di quello che c'è

Peggio dell'omonimo: **il filtro corto restituisce un elenco incompleto, e sembra
completo.** [misurato 10/09/2026]

```
filtro corto (marca)        → poche voci, una sola del modello cercato
filtro lungo (marca+modello) → più voci di quel modello, prima invisibili
```

Con la prima lettura avrei giurato che di TERA 28 ce ne fosse una. È la stessa trappola
delle griglie e della tendina delle entità: **quello che è renderizzato non è quello che
esiste**. Si restringe il filtro finché il numero di voci smette di cambiare.

### ⚠️ E lo stesso codice prodotto esiste sotto due marche

Fra quelle cinque:

```
Gruppo Termico   VICTRIX TERA 28 METANO   3.027369   Immergas S.p.A.
Gruppo Termico   VICTRIX TERA 28          3.027369   NO-<MARCA>       ← stesso codice
```

**`NO-<MARCA>` è una marca vera in tabella.** Sceglierla su una caldaia Immergas rompe
le statistiche per marca, i ricambi e l'assistenza in garanzia — e la riga in elenco è
quasi identica: cambia solo il suffisso del nome.

**Difesa che funziona**: prima di cercare il modello, **si imposta il campo `Marca`**
(in cima al dialogo). Con `Immergas S.p.A.` le voci NO-<MARCA> spariscono e restano due
righe leggibili. Filtrare a monte è più sicuro che azzeccare il click.

### ⚠️ Il click calcolato non è il click avvenuto

Ci sono cascato: ho letto le coordinate della riga giusta via JS, ho cliccato, e
**è finita selezionata un'altra riga**. Il badge diceva `(3.027369) VICTRIX TERA 28` —
senza `METANO` — e me ne sono accorto solo al passo dopo, quando `Marca *` mostrava
`NO-<MARCA>`.

> **Dopo ogni selezione da una tendina, si rilegge il testo del campo e lo si confronta
> con quello che si voleva.** Le coordinate invecchiano fra il calcolo e il click; il
> contenuto del campo no.

Interruttore **`Modello componente non tabellato`** per gli apparecchi fuori tabella, e
due icone rosa per aprire la tabella modelli o crearne uno nuovo (**scrittura in
tabella**).

### I 3 passi del gruppo termico

1. **Nuovo installato** — scelta del modello
2. **Dati generali** — `Installato su`, **`Posizione *`** (proposta `GT 1`; nel corpo di
   `UpsertGT` è `DatiPrincipali.Codice` «G1», «G2» per il secondo GT dello stesso
   impianto [sandbox, 15/10/2026] e «G3» per il terzo [sandbox, 16/10/2026]: è il progressivo
   della posizione), Marca,
   Modello, Codice prodotto, **`Combustibile = Impianto`** (eredita), più Matricola,
   Ubicazione, Data costruzione, Data installazione, Causale installazione
3. **collaudo** — COLLAUDO (data, tecnico, ricevuta fiscale, importo) e **GARANZIA**
   (tipologia, scadenza)
4. **Completa** — **DESTINAZIONE** (Riscaldamento / Produzione ACS) e **TIRAGGIO**
   (Camino singolo / Canna fumaria collettiva / Scarico a parete)

Destinazione e tiraggio **finiscono nel libretto e nell'RCEE**: compilarli ora costa
dieci secondi, recuperarli dopo costa un sopralluogo.

Confermato, l'installato compare con un badge di **tipologia componente dedotta dal
modello** (nel mio caso `CALDAIA CON BOILER`), e nell'albero appare
**`+ Nuovo installato figlio`** — è da lì che si appende il bruciatore.

### I 5 passi del gruppo frigo [misurato 14/10/2026, sandbox]

Serve una tipologia d'impianto che ammetta il GF (in sandbox «Impianto misto»). `+` sotto
l'albero → «Nuovo installato» → barra `Gruppo Termico | Bruciatore | Gruppo Frigo | UIR |
Componente` → **Gruppo Frigo**:

1. **Nuovo installato** — Marca\* e Modello gruppo frigo\*: dal modello arrivano fluido,
   GWP, numero di circuiti, olio e potenze
2. **Dati generali** — come il GT
3. **Collaudo** — messa in funzione e garanzia
4. **Circuiti** — griglia N., Kg, TCO2Eq, Fluido, Rilevamento perdite, Data
   installazione, Matricola; matita → «Modifica circuito». TCO2Eq lo calcola il client
   (Kg × GWP / 1000).
   ⚠️ **Il campo Kg scarta il punto**: «3.5» diventa 35 (e il TCO2Eq si ricalcola su 35).
   Si scrive con la virgola: «3,5». Poi si rilegge la griglia.
5. **Completa** → CONFERMA: una sola `PUT …/UpsertGF`, i circuiti nello stesso corpo.

In produzione (Clivet MDAN-XMi 4.1) la griglia Circuiti arriva **già
compilata dal modello** (1 circuito, 2,8 kg di R-410A, 5,85 t CO2eq): la si confronta con il
registro F-gas, senza riscriverla. Il passo Completa ha anche **FGAS**: `Identificativo
F-GAS` (il codice apparecchiatura della Banca Dati, nella forma `31*…`) e `Tipologia
apparecchiatura FGAS` (sei voci: refrigerazione fissa, condizionamento d'aria fisso,
pompe di calore fisse, protezione antincendio, celle frigorifere di autocarri e
rimorchi, commutatori elettrici). Poi **DESTINAZIONE**: Raffrescamento, Riscaldamento,
Produzione ACS. La scheda «FGAS» del GF creato è lo storico dei controlli (Data
intervento, Circuito, Tecnico, Operazione): per il codice catasto F-gas non c'è un campo.

⚠️ **Dopo, correggere un circuito scrive subito.** Altri dati → sezione CIRCUITI → matita
→ «Modifica circuiti» → riga → matita → «Modifica circuito» → MODIFICA: questo salva
(`PUT …/UpsertCircuitoGF`). La MODIFICA della modale esterna «Modifica circuiti» non
scrive niente, e un ANNULLA lì **non** annulla il circuito già salvato.

### L'unità interna sotto il GF — «Nuova UIR», 3 passi [produzione, 14/10/2026]

Dal GF: «+ Nuovo installato figlio» → filtro `UIR` (spento `Componente`):

1. **Nuovo installato** — Marca\* e Modello UIR\*; il filtro cerca per inizio
   (`SRHM` → SRHM A, SRHM B, SRHME A)
2. **Dati generali** — `Installato su` (il GF), Codice proposto `U01`, Marca, Modello,
   Codice prodotto, Matricola, Ubicazione, Descrizione, date, Causale installazione
3. **Collaudo** — collaudo e garanzia → CONFERMA

La matricola dell'unità interna è sua, non quella del GF: (matricole diverse).
Elenco dei modelli dal backend:
`assistenza/json/reply/QueryModelliUIR`; `QueryModelliUnitaInterne`
risponde 405.

---

## Il passo che quasi tutti dimenticano — il piano di manutenzione

**Un impianto appena creato ha il piano di manutenzione VUOTO.** Verificato: zero righe.

Conseguenza, e va detta chiaramente:

> Senza almeno un'operazione nel piano, **quell'impianto non produrrà mai una scadenza**.
> Non comparirà nello scadenziario dell'agenda, non finirà in nessuna estrazione di
> manutenzioni in scadenza, non genererà proposte. **Esiste in archivio e basta.**

*(La tabella Tipologie impianti può precaricare le operazioni per una tipologia; su
`Riscaldamento complesso <35 kW` di una sandbox non era configurata. In sandbox «Riscaldamento
semplice <35 kW» ne precarica tre **sull'impianto**, con la stessa CONFERMA del wizard, e
rifiuta il piano sulla macchina: `flussi/piani-manutenzione.md`, Web, punto 8
[misurato 14/10/2026, sandbox].)*

`+` di destra → dialogo **`Nuova operazione di manutenzione`**:

- **Installato** — precompilato con quello selezionato
- **Tipologia operazione \*** — es. `MO Manutenzione ordinaria`
- **Periodicità \*** — 16 valori: Manuale · Settimanale · Bisettimanale · Mensile ·
  Bimestrale · Trimestrale · Quadrimestrale · Semestrale · **Annuale** · Biennale ·
  Triennale · Quadriennale · Quinquennale · Sessennale · Decennale · **Personalizzata**
- **Ultima**, **Scad. legale**, **Scad. progr.**

⚠️ La tendina delle periodicità è lunga: `Annuale` cadeva a **y=724 su una finestra alta
702**, cioè **fuori schermo**, e cliccarne le coordinate avrebbe mancato il bersaglio.
**Si digita un filtro** (`annua`) e la voce risale in vista. È la regola generale delle
tendine lunghe.

**Quali voci e quali date le decide l'azienda** (esempio in `flussi/piani-manutenzione.md`):
le voci stanno sulla macchina, non sull'impianto; senza storico la `Scad. progr.` va a
novembre per caldaie e pompe di calore (01/11), ad aprile per
clima e chiller; il CF va alla stessa data della manutenzione. `Ultima` e `Scad. legale`
restano vuote: le compila il primo intervento, spuntando l'operazione (vedi
`crm-ticket.md`).

**Le voci precaricate dalla tipologia non si cancellano: si convertono.** Matita sulla
riga → «Modifica operazione di manutenzione» → `Installato` sulla macchina, `Tipologia`,
`Periodicità`, data → MODIFICA. Esempio: MANC → MAOPDC e AF → CF sul GF1,
RB → CFUNZ sull'U01: tre MODIFICA, nessuna eliminazione, e il nodo Impianto resta senza
voci. In sandbox lo stesso spostamento lascia l'Id invariato: la voce tiene il
suo Id [sandbox, 15/10/2026].

---

## Controllo finale, prima di dire «fatto»

1. L'impianto ha almeno **un installato**? (albero non vuoto)
2. L'installato è della **categoria giusta**? (badge GT, non Componente)
3. Il **piano di manutenzione** ha almeno una riga?
4. Il ruolo **Cliente** è assegnato?
5. Le **coordinate** sono precise, o resta l'avviso arancione?
6. La **zona** è quella giusta, o è rimasta `Nessuna`?

I punti 3 e 5 sono quelli che non danno nessun errore e si pagano mesi dopo.
