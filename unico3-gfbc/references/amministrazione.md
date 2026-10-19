# Amministrazione

> ⚠️ **Questo file descrive in gran parte il TERMINALE Windows, non il web.**
> Nel web l'area Amministrazione ha **due sole azioni, entrambe anagrafiche**: niente
> prima nota, incassi, IVA, registri, bilancio, chiusure. Vedi `cosa-il-web-non-fa.md`.
> Resta conoscenza utile — per capire i dati che leggo e per parlare con chi tiene la
> contabilità — **ma da qui non si esegue**.

Documenti, contabilità, IVA, scadenze. **È l'area dove quasi tutto è irreversibile o
fiscalmente rilevante**: numerare, protocollare, liquidare, chiudere un esercizio.
Qui la regola «su una sandbox si può scrivere» **non basta**: una sandbox può contenere registri veri di un'altra società del gruppo.
Numerazioni, liquidazioni e chiusure **chiedono conferma comunque**; gli invii telematici sono **vietati** alla skill (`VERSO_ESTERNO`).

Cosa ci si fa: anagrafiche · emissione documenti · registrazione documenti in ingresso ·
scadenziario RiBa e RID · compensazioni · elenchi telematici per l'Agenzia delle Entrate ·
piano dei conti · prima nota · mastrini · partitari · bilancio · registri fiscali ·
tabelle amministrative.

---

## Il ciclo di un documento emesso

Tre fasi, sempre: **dati di testata** → **righe di dettaglio** → **numerazione**.

### Tipi di riga

| Tipo | Note |
|---|---|
| **Articolo** | articolo codificato a magazzino |
| **Articolo a distinta** | vedi sotto |
| **Articolo manuale** | tutti i campi a mano; **non genera movimenti di magazzino** |
| **Testo** | anche pescato da **Glossari** |
| **Salto pagina** | solo nei preventivi |
| **Totale sezione** | solo nei preventivi, subtotale per separare le sezioni |

Sulla riga articolo: descrizione e descrizione estesa **si modificano liberamente e non
toccano l'articolo a magazzino**; la **contropartita** compare solo se il documento genera
movimenti contabili; **lotto/matricola** — se l'articolo è gestito a matricola la
**quantità si blocca a 1**; **nascondi in stampa/fatt. elettronica** rende la riga
contabilmente neutra (importi a zero) **ma la merce si muove lo stesso**; **competenza**
serve a ratei e risconti; lo **sconto** accetta combinazioni (`20+10+5`); scrivendo
l'**importo** al posto del prezzo unitario, il prezzo si ricalcola dividendo e
arrotondando a due decimali.

Il **prezzo viene dal listino corrente** mostrato nella zona azzurra: cambiandolo, il
nuovo listino **resta corrente** fino alla modifica successiva.

**Articolo a distinta** — comportamento diverso secondo il documento:
- documenti **contabili**: riga padre + righe figlie; prezzo, sconto e IVA stanno **solo
  sulla padre**. L'importo della padre è la somma delle figlie se la valorizzazione è
  *Pr. Analitico*, oppure un valore libero se è *Pr. Forfait*.
- documenti **di trasporto**: la distinta **si esplode** e movimenta tutti gli articoli
  semplici.

La distinta si modifica sul documento: **la modifica vale solo per quella riga**, non
tocca il magazzino.

**Modalità bozza** (impostazioni utente, per tipo documento): inserimenti e modifiche
non ricaricano la pagina — molto più veloce — ma alla fine serve un **`Ridisegna`**
manuale.

### Numerazione — l'operazione da non prendere alla leggera

Numerare **congela** il documento *(nel terminale: **nel web no** — misurato, vedi
`flussi/intervento-e-documento.md`)*. Per modificarlo va **annullata la numerazione**, e
non sempre si può (**una fattura già inviata allo SDI no**).

La guida è netta, e vale la pena riportarlo com'è: annullare una numerazione **annulla
anche tutti i movimenti contabili e di magazzino collegati**, che verranno riscritti alla
rinumerazione. E **il numero annullato non si recupera da solo**: va riforzato a mano,
altrimenti resta un buco nella cronologia.

Unicò **impedisce** cronologie incoerenti: non si può avere il n. 7 del 21 gennaio e il
n. 8 del 20 gennaio nello stesso anno.

---

## Documenti ricevuti

Due strade:

1. **Ricezione documento** — manuale: DDT, fatture, fatture accompagnatorie, note di
   credito e di debito. Genera i movimenti contabili e il carico di magazzino.
2. **Ricezione documenti SDI** — guidata e semiautomatica dalla fattura elettronica, con
   **creazione automatica di anagrafiche fornitori e articoli** presi dal documento.
   Funziona anche importando XML da fornitori terzi.

### Prima di usare la ricezione SDI

Tre tabelle vanno predisposte, altrimenti la registrazione esce sbagliata:
- **Tabella IVA → Natura**: i codici natura delle operazioni esenti/escluse/non imponibili
- **Conti di default → Aliquote IVA**: il codice per il trattamento IVA degli **abbuoni**
- **Tabella Pagamenti**: la **modalità SDI** per ogni tipologia, o lo scadenziario esce storto

### I colori dell'importazione — vanno letti, non cliccati via

Colonna **Articolo Unicò** (associazione articolo):

| Colore | Significato |
|---|---|
| **Rosso** | l'associazione sarebbe con un **articolo a distinta**: **non gestibile in automatico**, va fatto a mano |
| **Viola** | manca il codice articolo → la riga diventa **articolo manuale** |
| **Arancione** | in fattura ci sono **sconti** che possono alterare i valori di riga |
| **Blu** | incongruenza nel tipo di riga (tipico: righe di testo) |

Azioni: crea nuovo articolo · importa come articolo manuale · importa come riga di testo ·
cerca articolo · **importa tutte le righe come articoli manuali**.

Colonna **DDT** (riconciliazione del carico):

| Colore | Significato |
|---|---|
| **Rosso** | manca il riferimento al DDT nei movimenti — il magazziniere non ha caricato, o con numero diverso. Unicò genererà il carico dal riferimento in fattura |
| **Viola** | trovato, ma **quantità diversa**: proseguendo **la quantità del carico viene allineata alla fattura** |
| **Blu** | nessun carico per quell'articolo: verrà generato |

La colonna **Delta Prezzo DDT** mostra lo scostamento fra prezzo in fattura e prezzo di
carico; proseguendo, **il prezzo di carico viene aggiornato**.

Con **fattura accompagnatoria** va cambiata a mano la tipologia del documento ricevuto
nella prima fase, altrimenti non nascono i movimenti di magazzino.

**Il movimento contabile generato non è modificabile lì**: si corregge richiamando la
registrazione in **Prima Nota**.

---

## Prima Nota

Ogni registrazione chiede, in ordine: **tipo di registrazione → causale → data**. La
maschera cambia in base a quei tre.

### Documenti attivi

Data, numero, cliente (**il protocollo prende il numero fattura**), pagamento — che
**genera lo scadenziario attivo**, consultabile col pulsante `Scadenze`. La descrizione è
automatica e **non modificabile**.

Il **campo banca dipende dal pagamento**: nessuno per rimessa diretta; **banca del
cliente** per ricevuta bancaria; **banca aziendale** per bonifico.

Contropartita (avere): sottoconto + imponibile + IVA, poi `Aggiungi`. L'IVA è calcolata
e genera la riga con il sottoconto **IVA a debito** definito in *Causali e conti di
default*.

**Nota di credito da fornitore**: come una fattura emessa, ma si sceglie il **fornitore**
e il protocollo segue la **numerazione del registro acquisti**; la contropartita arriva
in automatico se l'anagrafica fornitore ha una contropartita abituale.

### Documenti passivi

Come sopra a segni invertiti. Unicò **controlla e segnala** sia i documenti con lo
**stesso numero per lo stesso fornitore**, sia i **protocolli duplicati** — in entrambi i
casi si può forzare. Il **protocollo progressivo proposto è quello da seguire**.

Banca: nessuna per rimessa diretta; **banca del fornitore** per bonifico; **banca
aziendale di addebito** per ricevuta bancaria.

**Nota di credito a cliente**: `nr documento = nr protocollo`, e **il protocollo non si
modifica se non cambiando il numero documento**.

### Autofatture — intraCEE, San Marino, reverse charge

Spunta **autofattura** nei dati documento (con un **progressivo autofatture separato**),
poi il **tipo di acquisto**: `Intracomunitario`, `S. Marino`, o
`Rev.Charge Art. 17 DPR 633/72`.

Nella contropartita dare **l'importo è il solo imponibile**, senza sommare l'IVA. Con
`Aggiungi` nascono **due righe IVA**: *IVA a credito* (dare) e *IVA a debito* (avere).
Nello **scadenziario passivo** la scadenza è **del solo imponibile**; nell'attivo **non
nasce nulla**.

Consiglio della guida: **codificare un'aliquota IVA imponibile dedicata**, con codice e
descrizione diversi, così nei riepiloghi queste operazioni restano distinte.

### Incassi e pagamenti

Sottoconto di contropartita → cliente → **si selezionano le scadenze aperte**. Si può
selezionare **più scadenze di documenti diversi e perfino di clienti diversi** nella
stessa registrazione.

**Doppio click su una scadenza** per incassare un importo diverso, e qui la regola non è
ovvia:

| Caso | Cosa fa Unicò |
|---|---|
| in **diminuzione, sotto il 5%** | propone di **chiudere la scadenza** e mette la differenza ad **abbuono** |
| in **diminuzione, sopra il 5%** | modifica l'importo e **apre una nuova scadenza** per la differenza |
| in **aumento** | tutta la differenza va ad **abbuono attivo** |

**Ritenuta d'acconto subita**: si abbassa la contropartita dare, `Modifica`, poi `Nuovo`
→ sottoconto ritenute → importo → `Aggiungi`, e la registrazione torna a bilanciare.
Per la **ritenuta operata** vale lo stesso sulla contropartita avere.

Un **costo aggiuntivo** contestuale a un pagamento **non si registra lì**: serve una
registrazione separata di tipo *Altro*.

### Corrispettivi

Solo **a scorporo** — Unicò **non gestisce la ventilazione**. Due causali:

- **Corrispettivi con scorporo** — ricevute fiscali registrate negli interventi e «a
  banco», per competenza **alla data di emissione**
- **Corrispettivi per cassa** — solo quelli **effettivamente incassati**

Con **una sola aliquota** la registrazione è automatica (sottoconti *Cassa* e *Ricavi da
corrispettivi* dai conti di default). Con **più aliquote** servono **tante registrazioni
quante sono le aliquote**, con importi a mano.

Il riepilogo mostra **totale analitico** e **totale documento**, ed evidenzia lo
**sbilancio** — che esiste perché il totale può essere forzato in emissione.

### Presentazione effetti, distinte CBI, insoluti

**Distinte CBI** gestisce RiBa, RID e bonifici nati dalle fatture di vendita. Filtri:
tipo scadenze, **stato** (aperti / chiusi / **insoluti**), intervallo di scadenza, n°
distinta, **non associate** (cioè gli effetti da presentare), CAT.

**Generazione distinta**: numero **automatico e sempre progressivo — non si azzera a
inizio anno**. Chi vuole distinguere gli anni forza `aaaannn` (2025001, 2025002…).

⚠️ **Una scadenza senza `Banca del cliente` viene scartata silenziosamente** in fase di
generazione. È il motivo più comune per cui «mancano degli effetti».

Per **togliere** effetti da una distinta: si selezionano, si richiama `Distinta` e si
conferma **lasciando vuoti numero e banca**.

**Esportazione**: tipo (RiBa/RID/bonifici), data presentazione, n° distinta, file di
destinazione, e il **codice SIA** dell'azienda (una lettera + 4 cifre, es. `T1234`). Il
file va poi caricato nell'home banking.

**Presentazione effetti** (prima nota) genera il movimento dal conto effetti al conto di
ogni cliente. La distinta si può anche usare per registrare in blocco i pagamenti
bancari: prima nota → pagamenti → sottoconto → opzione **`distinta`** → banca e numero →
`cerca` → si spuntano le righe e i movimenti si compongono da soli.

**Insoluti**: si sceglie banca e data, si clicca la riga impagata; gli **oneri bancari**
arrivano dai conti di default con l'importo spese insoluto della **tabella Banche**.
**Un insoluto non si modifica**: si elimina e si rifà.

Per **riemettere** un effetto insoluto: dalla ricerca movimenti si apre la fattura, si
seleziona la scadenza originaria, `aggiorna`, e si cambia il **tipo scadenza da
`insoluto` a `ricevuta bancaria`**. La scadenza insoluta resta a storico e ne nasce una
nuova aperta; poi nuova distinta e nuova presentazione.

### Scadenze SDD (SEPA Direct Debit)

Due tipi: **Core** (chiunque; **il debitore può chiedere il rimborso entro 8 settimane**)
e **B2B** (solo imprese; **nessun diritto di rimborso** se il mandato è valido, ma la
banca del debitore deve verificare il mandato prima del primo addebito).

Obblighi: mandato **cartaceo** sottoscritto, dematerializzazione e conservazione a cura
del **creditore**, **notifica al cliente almeno 14 giorni prima** dell'addebito, diritto
di opposizione entro il giorno prima, e **rimborso fino a 13 mesi** se il mandato non era
valido.

In Unicò: il **Creditor Identifier** va nella tabella **Banche**, fra i dati della banca
aziendale; **IBAN di addebito, numero, data di sottoscrizione e scadenza del mandato**
stanno nella sezione *Banche* dell'**anagrafica del cliente**.

### Compensazioni

Serve quando la stessa anagrafica è **cliente e fornitore**. Si scelgono scadenze attive
e passive e **si annullano per compensazione**, senza movimenti di prima nota.

**Funziona solo se i due totali coincidono esattamente**: finché non si equivalgono, il
pulsante `Compensa` resta spento. Si annulla cercando la compensazione e premendo
`Elimina`: le scadenze tornano aperte.

### Altre registrazioni (causali «Altro»)

Movimenti generici con conti Dare e Avere predefiniti in tabella Causali.

Due causali di sistema, **riservate e non modificabili**: `Movimento di chiusura` e
`Movimento di apertura` — le usa Unicò per la chiusura e apertura d'esercizio.
**Mai usare la causale `MA` predefinita** per registrazioni proprie.

Utilità **`Copia da precedente registrazione`** (solo per le causali «Altro»): utile per
le registrazioni ricorrenti a molti sottoconti, tipo le retribuzioni.

**Ratei e risconti non sono calcolati da Unicò**: si gestiscono a mano con registrazioni
di tipo *Altro*.

---

## IVA

### Liquidazione periodica

Mensile, trimestrale o annuale. Le regole che contano:

- **La periodicità dev'essere omogenea nell'anno fiscale.**
- **Si parte sempre da gennaio** (o dal primo trimestre). Se la contabilità comincia dopo,
  vanno fatte **liquidazioni fittizie a zero** per i periodi precedenti.
- La **registrazione definitiva congela** i valori: **riaprendo si vedono i congelati**,
  anche se nel frattempo la prima nota è cambiata.
- **Un periodo si chiude solo se sono chiusi tutti i precedenti**, e si può eliminare la
  chiusura **solo se non ce ne sono di successivi chiusi**.
- Il **credito** si riporta al periodo dopo; un **debito sotto € 25,82** si riporta.
- Sulle **trimestrali** la registrazione definitiva calcola la **maggiorazione dell'1%**.
- Il **credito dell'anno precedente va inserito a mano** nel primo periodo: **Unicò non
  fa nessun controllo**.
- **Acconto di dicembre**: fra le periodicità ci sono `dicembre acconto` (01/12–20/12,
  mensili) e `ott.-dic. acconto` (01/10–20/12, trimestrali), con un pulsante `aggiorna`
  per inserire le operazioni effettuate **ma non ancora fatturate**.

### IVA per cassa

Regime opzionale (volume d'affari **sotto 2 milioni**), che differisce l'IVA all'incasso.
**Non si applica** a regimi speciali, reverse charge, contribuenti minimi e operazioni
verso privati/consumatori finali. Dopo **un anno** l'IVA è dovuta comunque.

In Unicò basta la spunta **`iva per cassa`** nei dati documento (attivata di default se
il regime è impostato in *Impostazioni → generali → Amministrazione*). La registrazione
usa i sottoconti **IVA a debito/credito DIFFERITA**; **all'incasso o al pagamento** l'IVA
si gira sui sottoconti normali, **in proporzione fra importo della scadenza e totale
documento**.

I registri IVA cambiano da soli: nascono le sezioni **«pagamenti fatture esigibilità
differita»** e **«incassi fatture esigibilità differita»**, e il riepilogo distingue
registrato / a esigibilità differita / incassato-pagato / **esigibile nel periodo**.

### Registri fiscali e Libro Giornale

Si sceglie **anno → periodicità → periodo → registro**, poi `Elabora`. Ogni finestra ha
`esporta` in Excel.

**Bollato del Libro Giornale**: l'imposta di bollo si assolve **ogni 100 pagine o
frazione**, e Unicò stampa il trafiletto per la marca. Il bollo vale sulle pagine
**effettivamente usate**: se il 2006 finisce a pagina 85, le marche su 2006/1 coprono
anche le prime 15 pagine del 2007, e le nuove vanno su **2007/16**.

Numerazione dei registri non vidimati: **progressiva per anno**, con l'anno indicato in
ogni pagina (`1/2006`, `2/2006`), e **l'anno è quello della contabilità, non quello della
stampa**.

Attenzione a due cose nella maschera di stampa: il numero pagina è quello **fisico**, che
può non coincidere con `anno/pag`; e **i progressivi si aggiornano solo con la stampa
vera, non con l'anteprima**.

**Discrimina IVA** riepiloga imponibili e imposta **per sottoconto di contropartita**.

---

## Bilancio, piano dei conti, chiusure

### Bilancio

Intervallo di date libero, casella **`Esercizio precedente`** per un esercizio già
chiuso, scelta delle sezioni (Stato Patrimoniale, Conto Economico, Analitico
Clienti/Fornitori) e vista **Analitica** (sottoconto) o **Sintetica** (conto).

**Simulazione ammortamenti/risconti**: due caselle che mostrano l'effetto **senza
registrare nulla** — righe **azzurre per i risconti, rosa per gli ammortamenti**. È il
modo giusto di guardare un bilancio infrannuale.

### Piano dei conti

Tre livelli: **Mastro → Conto → Sottoconto**. Si movimentano **solo i sottoconti**; i
livelli superiori si aggiornano da soli. Da 1 a 99 mastri, 1-99 conti, 1-9999 sottoconti;
**codici mai duplicati**.

Il **tipo del Mastro** (Economico o Patrimoniale) **si propaga a cascata** ai livelli
sotto: sbagliarlo lì sbaglia tutto il ramo. Sui conti si dichiara Attività/Passività
oppure Costi/Ricavi.

Si cancella **solo dal basso**: un conto con sottoconti non si elimina, e un sottoconto
usato in prima nota nemmeno.

⚠️ **Cambiare il piano dei conti obbliga a rimettere a posto la tabella *Causali e conti
di default***, altrimenti gli automatismi puntano a conti che non esistono più.

### Primo esercizio

L'apertura del **primo** esercizio è manuale. Servono causali di tipo *Altro* per aprire
attività e passività — **mai la causale `MA`** — e causali *Altro* di incasso/pagamento
per chiudere le scadenze pregresse, che non hanno un documento collegato.

### Chiusura e apertura d'esercizio

L'esercizio coincide **obbligatoriamente con l'anno solare**. La chiusura si può generare
**in qualunque momento**, in due modalità:

- **provvisoria** — ripetibile; i movimenti generati vengono cancellati automaticamente
  alla chiusura definitiva
- **definitiva** — **non più modificabile né ripetibile**. Si fa solo quando si è certi
  di non dover più toccare le registrazioni.

Chiusura: chiude i conti economici → rileva utile/perdita → chiude i patrimoniali.
Apertura: riporta al 01/01 i saldi patrimoniali del 31/12.

Il movimento di apertura **si può modificare a mano in prima nota**, ma la guida
sconsiglia: crea un disallineamento fra chiusura e apertura.

### Mastrini e partitari

**Mastrini**: dare/avere per intervallo di date, filtrando clienti, fornitori o
sottoconti (anche per insiemi **catturati**), con l'opzione di escludere i saldi a zero.
Limite: **l'intervallo può stare a cavallo di due esercizi ma non superare 12 mesi**.

**Partitari**: per singolo cliente o fornitore, partite aperte/chiuse, o elenco analitico
con il dettaglio dell'incasso o pagamento collegato.

### Ritenuta d'acconto

Il calcolo **dipende dalla tipologia di pagamento**, non dal cliente: in *Tabella
Pagamenti*, sezione «Applica R.A. in documenti», `% R.A.` e `Applicazione`
(**Singola** = tutta su una scadenza, **Rateizzata** = divisa).

Il flag **`Soggetto a ritenuta d'acconto`** nei dati fiscali del cliente **non è la
condizione che fa scattare il calcolo**: serve solo ad avvisare se il pagamento scelto
non è compatibile.

Registrando il documento nasce una **scadenza fittizia di tipo «RITENUTA D'ACCONTO»**
nello scadenziario, **aperta**, da chiudere insieme alla scadenza vera al momento del
pagamento. Chi non lo sa se la ritrova aperta a fine anno.

---

## Fine anno — la sequenza operativa

**Unicò tiene tutti gli anni fiscali in linea**: non c'è un «cambio archivio».

1. **Contatori documenti emessi** — prima di emettere nel nuovo anno si entra in tabella
   **Numerazioni** e si riportano **manualmente a `0`** tutti i contatori, mettendo come
   **suffisso le ultime due cifre dell'anno** (`0 / 22`). **Va fatto con nessun operatore
   che sta emettendo documenti**, o escono numerazioni sbagliate.
   Per un documento retrodatato all'anno vecchio (entro i 12-15 giorni di gennaio) si
   **forza numero e suffisso a mano**: il contatore progressivo non si tocca e i due anni
   proseguono in parallelo.
2. **Protocollo acquisti** — è automatico e legato **all'anno della data di registrazione**.
   La regola: la data di registrazione contabile è **uguale o successiva alla data di
   ricezione SDI**. Se la ricezione SDI è dell'anno vecchio, la registrazione **non va
   oltre il 31/12** e il protocollo segue il progressivo vecchio.
   **Da evitare**: fattura ricevuta dallo SDI nell'anno precedente, registrata nel nuovo,
   con protocollo dell'anno precedente.
3. **Ordini a fornitore** — **non** usano la tabella Numerazioni: progressivo automatico.
   Per ripartire da 1 basta numerare a `1` il primo ordine, o azzerare da
   `Utilità → Numerazione`.
4. **Inventario di magazzino** — si chiude **quando si vuole, anche molto dopo il 31/12**,
   quando i dati sono verificati. **Una volta chiuso i movimenti sono storicizzati e non
   più modificabili.** È **fortemente raccomandata**: alleggerisce moltissimo i calcoli
   sulle giacenze.
   **Prerequisito assoluto: nessuna giacenza negativa** in nessun magazzino, cantiere o
   furgone. Si sistemano con **Trasferimento** dal centrale ai periferici, e sul centrale
   con **Carico/Scarico di rettifica** (che **non incidono sul calcolo dei prezzi**).
   La chiusura genera per ogni articolo con giacenza ≠ 0 uno **scarico al 31/12** e un
   **carico al 01/01**, valorizzati a *prezzo medio ponderale progressivo*, *ultimo prezzo
   di acquisto* o *listino base* secondo il metodo scelto. **Può metterci molto tempo.**
5. **Commesse e preventivi** — `Utilità → Numerazione` per azzerare, oppure si prosegue
   progressivi.

---

## Esportazioni verso l'esterno

**XML SDI** — dal `Utilità` di una singola fattura, o **massivamente** dalla *Ricerca
documenti emessi*. La maschera segnala **quanti documenti passano i controlli SDI**;
**l'esportazione parte solo per quelli formalmente corretti**. Con più documenti esce
sempre uno **ZIP**. Colori: **bianco** ok · **giallo** ok ma **già esportato** ·
**rosso** errori, con il dettaglio nella colonna `Risultato`.

**Export TeamSystem** (modulo opzionale, specifiche *IMPPN Multi 2020.02.00*) — evita di
ridigitare tutto dal commercialista. Prima serve la **parametrizzazione dei «codice
export»**, da concordare con il consulente: su **tabella IVA**, **piano dei conti** (i
sottoconti di ricavo), **tabella Pagamenti** e, se serve, **anagrafica cliente** (per
bypassare l'abbinamento per codice fiscale/P.IVA quando ci sono anagrafiche doppie).
Poi: ricerca *Documenti emessi* → `Utilità → Teamsystem → Genera file per invio
elettronico` → **codice ditta** → si salva il file **TRAF2000**.

**Fatturazione elettronica**: soluzione **integrata** (LegalSolutionsDOC®, conservazione a
norma con **Namirial**) — invio, esiti e conservazione dentro Unicò; oppure **terze parti**
(servizi gratuiti AdE o altri conservatori), e allora si esportano gli XML e si caricano
altrove, **rinunciando agli esiti dentro Unicò**.

---

## Memo & Scadenze — la home

Il tool in home page sorveglia da solo tre cose:
- **bollo, assicurazione e revisione dei furgoni**
- **controllo/revisione delle attrezzature dei furgoni**
- **certificazione F-Gas dei tecnici**

Inserendo una di queste scadenze **nelle rispettive tabelle**, Unicò chiede **quanti
giorni prima** avvisare.

`+` crea **memo personalizzati**: data, ora, testo, destinatari (**tutti gli utenti o uno
solo**). Di default si vede la giornata; il riquadro `oggi` allarga a 7 o 30 giorni o a
un intervallo libero. C'è anche la ricerca **«memo e scadenze»**.
