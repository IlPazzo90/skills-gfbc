# Anagrafiche

Un archivio solo, **trasversale a tutti i moduli**: clienti, fornitori, amministratori,
installatori, progettisti, terzi responsabili. Una scheda può avere **più categorie
insieme** — un cliente che è anche fornitore e amministratore di condominio è una
scheda, non tre.

## Categorie e ruoli

**Cliente** e **Fornitore** sono le due che pesano: coinvolgono amministrazione e
magazzino. **Marketing** e **Rubrica** sono filtri per i contatti da campagne.

Le categorie di sinistra sono le figure delle schede impianto, e **non serve
codificarle in anticipo**: vengono **ereditate** quando l'anagrafica viene usata in quel
ruolo. Nel web, di conseguenza, **certi ruoli non si tolgono**: se l'anagrafica è
proprietario e occupante di un impianto, quei ruoli sono bloccati finché lo è.

## Come si classifica una persona — la regola, che evita doppioni sbagliati

**Persone fisiche**: codice fiscale **alfanumerico**, nome e cognome.
- **Privati** — nessuna P.IVA, nessuna denominazione diversa, di norma nessun dato SDI
- **Ditte individuali / professionisti** — P.IVA, denominazione possibile, dati SDI

⚠️ Per fatturare alla **stessa persona fisica** una volta come privato e una come ditta
individuale servono **due anagrafiche distinte con lo stesso codice fiscale**: una senza
P.IVA, una con P.IVA e dati SDI.

**Persone giuridiche**: codice fiscale **numerico** (SNC, SAS, SRL, SPA, condomini, enti
pubblici), P.IVA spesso uguale al CF, dati SDI, **nessun nome/cognome**, una
denominazione.

## Dati principali

- **Codice** — solo per clienti e fornitori: progressivo automatico, forzabile purché
  **univoco**. La lente apre **assegna codice libero** per coprire i buchi.
- **Gruppo** — prefisso 6 + suffisso 3 caratteri, per filtrare gruppi omogenei
- **Tipo soggetto** — categorizzazione SDI. **Obbligatorio per la P.A.**, e **consigliato
  per i condomini** perché pilota automaticamente la causale di pagamento SDI.
- **Telefoni** — tre numeri, ognuno con un'icona che si cambia **cliccandola più volte**:
  fisso, fax, cellulare, e **cellulare abilitato agli SMS**. Quella distinzione decide se
  il numero riceve messaggi.

## Note — quattro tipi, e uno di questi blocca

- **Principale** — stampata su alcune schede
- **Storico** — mai stampata, solo a video
- **Riservato** — mai stampata
- **CLIENTE BLOCCATO** — **basta una nota qualsiasi di questo tipo** e su **tutti gli
  impianti collegati al cliente** compare la segnalazione di blocco (la spia «blocco
  anagrafica» rossa sulla scheda impianto)

## Riferimenti e ruoli

Un riferimento è **un'altra anagrafica** oppure dei dati inseriti a mano. Poi si sceglie
il **Ruolo** e la **data di inizio incarico**.

I ruoli sono **fissi, non personalizzabili**: **Referente** · **Altra sede** ·
**Rappresentante fiscale** · **Stabile organizzazione** · **Legale rappresentante**.
Lo stesso riferimento può avere ruoli diversi.

Quando una figura cessa **non si cancella**:
- **Sostituzione** — la sostituisce e **storicizza la data del cambio** (il cambio di
  amministratore di condominio è esattamente questo caso)
- **Dismissione** — la toglie storicizzando la data

## Dati fiscali

Oltre ai soliti: **Codice destinatario SDI** · **Codice EORI** (export/dogane) ·
**Codice CURIT** — *si attiva solo se l'anagrafica è un **Terzo Responsabile**, e serve
con l'ente regionale lombardo* · **Patentino** — *solo per gli **Operatori F-Gas*** ·
**N° iscrizione albo** — *solo per i **Progettisti*** · **Soggetto a ritenuta** ·
**Causale pagamento SDI** (il codice CUD) · **CCIAA** · **Tribunale** ·
**Riferimento amministrazione** (finisce nel tracciato SDI `2.1.1.7.8`) · **Codice export**
(per TeamSystem e simili) · **Dati privacy**: data del consenso o del diniego e data di
consegna dell'informativa.

Due caselle che servono a **non sbagliare**:
- **Escluso da utilizzo in fatturazione** — impedisce di selezionare quel nominativo.
  Il caso è il cambio di ragione sociale e P.IVA: si crea la nuova anagrafica e si
  **chiude la vecchia**, così l'abitudine non fa fatturare a quella sbagliata.
- **Escluso da invio dati fatture** — i documenti restano fuori dall'**Esterometro**.

## Vendita / Acquisto

Compare solo per clienti e fornitori.

**Vendita (cliente)**: pagamento abituale · **listino abituale** (senza, si usa il
listino base) · **sconto abituale**, applicato *a prescindere dal listino* ·
**aliquota IVA preferenziale**, che **vince su quella dell'articolo** (è così che si
gestisce un cliente in esenzione) · **sottoconto cliente** per l'automatismo di prima
nota · addebito spese incasso effetti · rivalsa del bollo in fattura.

**Acquisto (fornitore)**: **importo minimo ordine** — sotto soglia esce un alert
emettendo l'ordine · pagamento e listino abituali · **sottoconto fornitore** ·
**contropartita di prima nota** fissa, utile per consulenze, affitti e simili.

## Banche

Due banche per anagrafica, e **il significato si inverte** fra cliente e fornitore:

|  | **Banca del cliente/fornitore** | **Nostra banca** |
|---|---|---|
| **Cliente** | banca di **addebito** degli effetti attivi (RiBa) | banca aziendale di **appoggio per l'incasso** dei bonifici |
| **Fornitore** | banca su cui **pagare i bonifici** | banca con cui si **pagano le RiBa** |

`Nostra banca` si sceglie **solo fra le banche marcate come aziendali** in tabella Banche.

Serve anche a sapere **quanto si deve a ciascun istituto**, per confrontarlo con gli
affidamenti.

⚠️ Ricordare: **una scadenza RiBa senza `Banca del cliente` viene scartata** dalla
generazione della distinta effetti.

## Le sezioni di sola consultazione

**SMS** (storico invii) · **Impianti collegati** (tutti gli impianti e con quale ruolo,
apribili in una tab nuova) · **Scadenze** (solo aperte, con totale attivo, passivo e
**saldo**; pallino giallo col conteggio) · **Documenti / Preventivi** (pallino blu col
totale). **Doppio click apre l'elemento collegato** — tranne che sugli SMS.

**Contratti**: da qui si inseriscono i contratti di tipo **Avanzato** della gestione
impianti.

## Utilità

- **Numerazione** — forza il contatore dei codici cliente/fornitore
- **Crea anagrafica (Cliente) da Impianto** — legge i dati **principali dell'impianto**
  oppure quelli di **Occupante** o **Proprietario**; si può marcare anche come fornitore
  e importare note principali e referenti
- **Assegna codice libero** — bypassa la numerazione automatica usando un buco
- **Accorpa anagrafiche** — sostituisce l'**origine** con la **destinazione** ovunque, e
  **poi elimina l'origine**.
  > La guida stessa la definisce «potenzialmente molto pericolosa per l'integrità dei
  > dati». L'origine **non può essere cliente o fornitore**. **Zona rossa: non si esegue
  > senza richiesta esplicita**, nemmeno su una sandbox.
  Nel **web non è ancora implementata** (come la stampa).

Nel web il ⋮ della testata dà: tabella numerazioni, **registro operazioni**, elimina
anagrafica.
