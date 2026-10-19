# Tabelle Web

Le tabelle sono la **configurazione** di Unicò: cambiare una riga qui cambia il
comportamento del programma per tutti. Il censimento aggiornato (**~68**, con rotte e conteggi) sta in `tabelle-rotte.md`; qui c'è **cosa fanno davvero** e **cosa non va toccato**.

Rotta: `#/tabelle/<Entità>/table` — **il nome dell'entità, non l'etichetta**.

**Le rotte censite, con conteggi e campi, stanno in `tabelle-rotte.md`**, insieme al
metodo per trovare quelle che mancano. Due cose da sapere subito: per le tabelle la
rotta scritta a mano **funziona**, e una rotta sbagliata **lascia in silenzio la tabella
precedente**.

---

## Meccanica comune

Tutte in una pagina sola, raggruppate per **Amministrazione, Assistenza, Installazione,
Magazzino**. Due ricerche rapide: quella di **sinistra cerca fra i nomi delle tabelle**,
quella di **destra dentro il contenuto** della tabella aperta.

- **`+`** crea. Il form di creazione e quello di modifica sono lo stesso, e `Escluso da
  liste` c'è già in creazione. Dopo il salvataggio si apre
  `#/tabelle/<Entità>/detail/<id>`.
- **occhio** — mostra anche le voci **escluse da liste** (sfondo grigio).
- **Esporta** — stessa griglia in una finestra: righe tutte o selezionate, xlsx o pdf,
  cloud o locale (o anteprima), orizzontale o verticale, **e la scelta se includere le
  escluse da liste**.
- **selezione multipla** — il quadratino in alto, oppure CTRL + click su una riga.

**Trappola dei conteggi**: le voci escluse da liste si mostrano o si nascondono, e il
totale cambia. Esempio: una tabella dà N voci nascondendo le escluse e N+k mostrandole. *«Quante ne
abbiamo?»* ha due risposte giuste — va detto quale si sta dando.

Le griglie delle tabelle **si ordinano e si filtrano dalle intestazioni** (a differenza
di quelle delle ricerche), si trascinano le colonne, si raggruppa per contenuto, e dal
menù della cella di intestazione si fissano colonne, si filtrano i valori e si
aggiungono/tolgono campi. E **non hanno il conteggio dichiarato**: la prova di
completezza dell'estrazione non si applica (la griglia si ferma da sola — verificato).

### Le operazioni massive, e perché non sono innocue

Compaiono in selezione multipla e cambiano da tabella a tabella.

- **ACCORPA RIGHE** — si sceglie la riga **di destinazione**; **tutte le altre vengono
  eliminate**. La conferma è di un altro colore e chiede di **scrivere il numero degli
  elementi da accorpare**. **Irreversibile.** Non tutte le righe si accorpano: alcune
  tabelle pretendono caratteristiche uguali (non si accorpa un'operazione di
  riscaldamento con una di condizionamento).
- **MODIFICA MASSIVA** — cambia campi a blocchi.
- **ELIMINAZIONE MASSIVA** — **irreversibile**. Chiede cosa fare con i record **già
  collegati** ad altro: saltarli e cancellare il resto (per «pulire»), oppure annullare
  tutto se anche uno solo è collegato.

⚠️ **Il rischio che non è scritto sui pulsanti**: le operazioni massive possono
**desincronizzare le tabelle memorizzate offline sui telefoni dei tecnici**. Il sintomo
è la **«nuvoletta rossa»** in Unicò Mobile, e in quel caso **i dati dell'intervento non
si salvano e vanno reinseriti a mano**. La procedura corretta, secondo Futura: **far
fare logout a tutti i tecnici prima**, e login dopo. Su un'azienda in produzione questo
è un intervento da concordare, non da fare a metà mattina.

---

## Assistenza

### Tecnici — la tabella più importante di Unicò

Cinque tab.

**Dati generali**: anagrafica, **colore** (colora la sigla in agenda e nel selettore
tecnico), **lista materiale** associata (finisce nei documenti che il tecnico emette,
anche da mobile), categoria analytics, **tipo licenza planner**, **numerazione
automatica** dei documenti, **tipo feedback** (SMS), **certificazione F-Gas**.

**Codici manutentore**: ente + codice. **Indispensabile per gli invii al catasto.**

**Competenze** (SMART) — la logica non è ovvia:
- tecnico che sa fare tutto → **si lascia vuoto**
- tecnico che sa fare solo alcune cose → si inserisce un **range ristretto di competenze**
- tecnico che **non** sa fare solo alcune cose → prima una competenza «sa fare tutto»,
  **poi** il range di **non** competenze

Il tasto apposito **copia un set di competenze su altri tecnici**.

**Orari** (SMART): orari settimanali, pausa pranzo, opzione **flessibile** (sposta la
pausa entro un intervallo). Per il planner servono il **luogo base** (`Sede` o `altro
luogo` con coordinate) e il **luogo della pausa** (`torna alla sede` / `alla base` /
`ad altro luogo` / **`flessibile`**, cioè fra l'ultimo impegno del mattino e il primo
del pomeriggio). Se le giornate sono uguali si compila il lunedì e **si spuntano le
altre, che si autocompilano**.

**Impegni**: si vedono e si creano anche da qui, e si **copia un impegno su altri
tecnici**.

**App mobile**: licenza, funzionalità, stampe (→ `configurazione da Web di licenze e app
mobile`).

**Funzione unica: COPIA VINCOLI ORARI.** In selezione multipla si scelgono origine e
destinatari, e gli orari **vengono sovrascritti**. Attenzione: c'è un **controllo sulle
licenze** — senza licenze SMART disponibili la copia su tecnici non-SMART fallisce con
errore.

### Squadre tecnici

Nome, **caposquadra**, aiutanti. Vincoli: un tecnico **non può essere caposquadra e
aiutante insieme**, e lo stesso aiutante non si ripete. **I vincoli di orario e
competenza si verificano solo sul caposquadra.**

Toccare questa tabella **non cambia le RdI già compilate** — la squadra non viene
salvata sulla richiesta.

### Tipologie attività ufficio — dove vivono gli esiti del CRM

Tre caselle: **pianificabile** (permette di rimandare l'esito e fissare giorno e ora),
**visibile da mobile**, **inseribile da mobile**.

Poi la griglia **`esiti attività ufficio`**, e qui sta il motore del CRM. Ogni esito ha:

- **Esito attività ufficio** — il nome
- **Esito azione successiva** — e i valori possibili sono **tre soli**:
  1. **apre una richiesta di intervento**
  2. **programma un'altra attività ufficio** (e allora va scelta **quale tipologia**)
  3. **chiude il ticket**
- **Categoria analytics**

**Questo risponde a come si chiude un ticket**: non c'è un pulsante «chiudi». Si chiude
**evadendo un'attività con un esito la cui azione successiva è «chiudi ticket»**. Se
nessun esito di quella tipologia chiude, il ticket resta aperto per definizione.

### Tipologie intervento

Campi facoltativi che però cambiano il comportamento:

- **Lista materiale** — precaricata nei documenti creati da quella tipologia, anche da mobile
- **Colore** — colora le righe della sezione interventi e, se impostato in agenda, gli
  interventi in calendario
- **Categoria e Area analytics** — etichette per i filtri e i grafici di Analytics
- **Considera come manutenzione per analytics**
- **Aggiorna collaudi** — **attiva la sezione Collaudi** nella scheda intervento
- **Tipo feedback** — decide quali interventi generano la **richiesta di feedback via SMS**

### Voci di validazione intervento

Si definisce la voce e **in quali tipologie intervento compare** (alcune, o tutte con
l'apposita casella). **Priorità visualizzazione**, default 100: **più alto = più in alto**
nella lista. Una validazione che deve stare per forza prima va messa a 100.

### Tipologie operazioni di manutenzione

`Tipologia` (ordinaria/straordinaria), codice, descrizione, **lista materiale**,
**durata media** (proposta come durata intervento e **fondamentale per il planner**),
descrizione estesa, la classe
**Riscaldamento / Condizionamento / Teleriscaldamento / Altro** — e **per il
Condizionamento si indica il tipo di operazione F-Gas** —, note.

Per accorpare: stessa classe, stesso tipo F-Gas, e **mai ordinarie con straordinarie**.

### Tipologie RdI e Motivi RdI

Entrambe hanno il **colore**, e in agenda colorano lo sfondo della RdI **se
l'impostazione agenda è su quello** (di default colora per **Zona**).

Differenza in creazione RdI: la **tipologia** colora il campo **`Sigla`** — e **se la
sigla non è compilata non si vede né sigla né colore**; il **motivo** aggiunge un
tassellino colorato a sinistra.

### Tipologie impianti

Si assegnano una o più **classi**. Le classi **attivano le schede tecniche**
(Caldaie, Gruppi Frigo, Scambiatori) sull'impianto — ecco perché su certi impianti non
si possono appendere certi installati. Senza classe l'impianto è **generico**
(fotovoltaico, depurazione, ascensore). Selezionando una classe **se ne deselezionano
automaticamente altre incompatibili**. Si possono precaricare le **operazioni di
manutenzione** che nasceranno con ogni impianto di quella tipologia.

### Zone

Descrizione, **sigla di 3 caratteri** (compare in agenda), **colore**, e **minuti
parcheggio** — la stima del tempo per parcheggiare in quella zona, **usata dal Planner
nel calcolo**. Chi non le usa lascia la zona `nessuna`.

### Motivi dismissione

Motivo + una o più categorie (impianto, tecnico, riferimento). **Accorpando, le categorie
delle righe assorbite diventano quelle della destinazione.**

### Modelli installato — sei tabelle

Gruppo Termico, Bruciatore, Gruppo Frigo, UIR, Componente, Scambiatore. Dati diversi,
meccanica uguale. In selezione multipla:

- tutte: **AGGIUNGI TAG** (SMART) e **ALLINEA CODICE PRODOTTO** — che è la funzione che
  serve davvero: aggiornato il codice sul modello, **sulle schede impianto resta il
  vecchio** finché non si allinea.
- Gruppi frigo: in più **ALLINEA POTENZE** e **AGGIORNA FLUIDO FRIGO**
- Componenti: in più **ALLINEA DATI AGGIUNTIVI**
- **Importazione massiva dei modelli**: GT e bruciatori per **Baxi, Westen, Immergas**;
  gruppi frigo e componenti **solo Immergas**

### Tag — otto tabelle (SMART)

Tag impianti, e tag modelli per GT, bruciatore, gruppo frigo, UIR, componente,
scambiatore. Più **Tag RDI**. Struttura elementare, servono a classificare e a cercare.

### Attrezzature furgoni / Furgoni / Dotazioni standard

**Non confondere le due**: *Attrezzature furgoni* è **cosa c'è a bordo** (analizzatore,
deprimometro, matricola, **scadenza controllo/revisione** — il sistema avvisa);
*Dotazioni standard e scorte minime* è **la soglia di riordino**, che entra nella lista
di riordino automatica **sommandosi alla scorta minima del magazzino centrale**.

**Furgoni**: ogni automezzo è **un magazzino periferico**. Assegnato un tecnico, per
ogni suo intervento **quel furgone viene proposto come magazzino di scarico** (si può
cambiare). Poi scadenze **bollo, assicurazione, revisione**, **costo chilometrico** (usato
da GeoLocation e Planner) e **ID localizzatore GPS**.

Utilità: **IMPORTA DA FURGONE** (copia l'attrezzatura sovrascrivendo), e sulle dotazioni
**CREA LISTA MATERIALE**, **IMPORTA DA TABELLE MAGAZZINO** e **IMPORTA DA LISTA
MATERIALE** — con la scelta fra **aggiungere** e **sovrascrivere**, che cancella tutto
prima.

### Le altre tabelle Assistenza

Combustibili · Fluidi F-Gas · Fornitori di energia · Impianti di riciclaggio ·
Interlocutori RdI · Motivi ritorno intervento · Operatori RdI · **Sottotipi altro
impegno** (quelli che si vedono in agenda) · Tipologia componente · Tipologia contratti ·
Tipologia garanzie installati · Tipologia guasto. Tutte aggiungi/modifica/elimina.

---

## Generali

- **Comuni** — molto più di un elenco. Un comune porta con sé: **Ente** (chi fa i
  controlli sugli impianti termici), **Zona** fissa facoltativa, **durezza totale
  dell'acqua** in gradi francesi (**usata nei RCEE**), **tipo di rapporto di controllo**
  (nazionale o regionale) e il **periodo annuale di riscaldamento**. Un comune con più
  CAP **va inserito una volta per CAP**. Utilità: **IMPORTA DA TABELLA ISTAT**, **ALLINEA
  DA TABELLA ISTAT**, e in selezione multipla **allinea durezza acqua su impianti**.
- **Enti** — contenitori da associare ai comuni. Servono dove l'**invio telematico** va
  differenziato per zona.
- **Numerazioni** — i contatori dei documenti. Zona rossa.
- **Glossari** — frasi precodificate (raccomandazioni e prescrizioni RCEE, testi
  standard di fatturazione). Gruppo + voce + descrizione estesa fino a **4000 caratteri**
  + le caselle che decidono **in quali punti del programma** la frase è disponibile.
- **Tipologie documenti** — la guida stessa avvisa: errori qui provocano
  «malfunzionamenti o errori potenzialmente anche molto gravi». Definisce la
  **numerazione** usata (più tipi possono condividere lo stesso contatore) e soprattutto
  **se il documento genera movimenti di magazzino, contabili o entrambi**: per il
  magazzino uno fra *scarico a cliente / scarico a fornitore / trasferimento* (o «non
  generare»), per la contabilità la **natura** (Dare per le fatture, Avere per le note di
  credito) e la **tipologia documento SDI**. **Zona rossa: non si tocca.**
- **Anagrafiche azienda** — esiste **solo nel web** (nel terminale è nel menù
  supervisore). Indirizzi · recapiti (compreso il **mittente SMS**) · **dati fiscali**
  (regime fiscale, REA, registro imprese, CCIAA, **EORI**, socio unico, liquidazione,
  capitale sociale, **ATECO**, luogo di conservazione dei documenti — quasi tutti finiscono
  nell'**XML della fattura elettronica PA**) · **certificazioni** (46/90, albo imprese
  artigiane, **F-Gas** con numeri, enti, rilascio e scadenza) · **serie numerazione**
  (solo multiCAT: preventivi, commesse, ordini).
- **Tag anagrafiche** (SMART) · **Tipologie commesse** · **Tipologie file allegato**
- **Unità di misura** — **non modificabile**, sono quelle del SI. Si può solo escludere
  da liste. Il flag **Decimale** dice se le quantità accettano decimali.

---

## Amministrazione

- **Causali contabili** — ogni registrazione di prima nota ne ha una. Alcune predefinite
  **non sono modificabili** perché legate agli automatismi. Ogni causale appartiene a una
  **famiglia**: *Documenti Attivi* (incasso: fatture, note di addebito a cliente, note di
  credito da fornitore) · *Documenti Passivi* · *Incassi* (chiudono un documento attivo) ·
  *Pagamenti* (chiudono un passivo) · *Corrispettivi* (**a scorporo — Unicò non fa la
  ventilazione**) · *Presentazioni effetti* (SBF) · *Maturazione* · *Insoluti* · *Altro*
  (giroconti, prelievi). Crearne una **richiede competenze ragionieristiche**: Dare e
  Avere sbagliati producono bilanci sbagliati.
- **Causali e conti di default** — «la tabella più diversa da tutte le altre», e la più
  pericolosa: contiene **i collegamenti che fanno funzionare gli automatismi di
  registrazione**. Sette sezioni: conti generali (clienti/fornitori, cassa, **erario IVA
  a credito e debito**, IVA differita, abbuoni, effetti e spese bancarie, ritenute) ·
  conti vendita/acquisto · conti apertura/chiusura · causali incasso/pagamento · causali
  apertura/chiusura (**usate nel passaggio di esercizio** e per i risconti) · aliquote IVA
  automatiche · spese e causali in fattura.
  **Se si tocca il piano dei conti, va rimessa a posto questa tabella**, altrimenti gli
  automatismi puntano a conti che non esistono più.
- **Aliquote IVA** — codice, descrizione, **tipologia** (imponibile, esente, escluso, non
  imponibile, **operazione PA/split payment**), % assoggettamento, % indetraibilità,
  **Natura IVA SDI** per le non imponibili, riferimento normativo SDI, **soggetto a
  imposta di bollo**.
- **Pagamenti** — la tabella che **genera le scadenze**. Tipologia e modalità **SDI**
  (ricevuta bancaria, tratta, bonifico, rimessa diretta, RID), sottoconto, **fino a 12
  rate**, % ritenuta d'acconto e se singola o rateizzata, **tipologia prima rata**
  (*normale* = parti uguali; *con IVA* = tutta l'imposta nella prima; *solo IVA*),
  **inizio prima rata** (data fattura o fine mese), giorni alla prima scadenza,
  periodicità, e **posticipi** (31 agosto, 31 dicembre, o sempre di N giorni).
  Le scadenze generate **restano modificabili a mano** dopo.
- **Banche** — proprie **e di clienti e fornitori**. La casella *Banca dell'azienda* la
  lega al sottoconto. Le **spese insoluto** indicate qui vengono proposte in automatico
  registrando un insoluto; l'**IBAN** finisce nelle distinte effetti, nello scadenziario
  e nella testata dei documenti.
- **Categorie cespiti** — tipologia (materiali, immateriali, spesa pluriennale), codice
  di 4 caratteri, **% ammortamento fiscale**, e i tre sottoconti: immobilizzazioni,
  ammortamento (attivo), **fondo ammortamento** (passivo). Precodificata sul piano dei
  conti standard.

---

## Magazzino

- **Listini** — `listino base` e `ultimo prezzo` sono precodificati e **non
  modificabili**. Un listino può essere **Standard** o **Calcolato**: quest'ultimo
  prende un **listino di origine** e applica un ricarico su *prezzo di vendita* o
  *prezzo di acquisto*, con la percentuale in valore assoluto.
- **Magazzini** — di default solo il **centrale**; se ne creano quanti si vuole. La
  casella **Chiuso** blocca ogni movimentazione ed **è attivabile solo a giacenza zero**:
  prima si trasferisce, poi si chiude.
- **Marche** — produttori di apparecchiature **e** di articoli di magazzino. Si può legare
  la marca a un **fornitore** in anagrafica, ma non è obbligatorio. Le caselle di
  tipologia dicono **dove** la marca è utilizzabile: le prime quattro nelle schede
  impianto, l'ultima negli articoli di magazzino.
- **Causali movimenti** — le precaricate sono **fisse, non modificabili né eliminabili**.
  Definiscono **DA** dove e **A** dove può muoversi la merce e **se il movimento entra nel
  calcolo dei prezzi medi di inventario** e nell'aggiornamento dell'ultimo prezzo.
  Crearne di nuove **influenza i prezzi di inventario**: la guida consiglia di limitarsi
  a quelle esistenti.
- **Gruppi merceologici** — consiglio esplicito: **10/20 gruppi bastano**. Una
  classificazione troppo analitica rende ingestibili inventario e stampe.
- **Cantieri** · **Famiglia merceologica** (non modificabile) · **Tag articoli** (SMART) ·
  **Tipi giunzione** · **Tipologie componente conformità** · **Tipologie materiale** ·
  **Tipologia lista materiale**.
