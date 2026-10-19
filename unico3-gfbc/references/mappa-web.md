# Mappa — Unicò Web

Scritta il 03/09/2026 da osservazione diretta su **Azienda 3**, un'utenza
di prova. Ogni riga qui sotto è stata vista, non dedotta. Quello che non
è stato verificato è marcato **[da verificare]** e va trattato come tale.

## Stato dei selettori

Un selettore che funziona non è ancora un selettore buono: è **candidato** finché un
risultato che ne dipende non è stato confermato dal titolare.

**Promossi a buoni il 03/09/2026**, perché ha confermato il numero degli impianti attivi di
Azienda 3 come quello che si aspettava — e quel numero passa per tutta la catena:

- il percorso Assistenza → Ricerca e il campo `Cosa stai cercando`
- `div.search-results` come riquadro di una singola ricerca
- `div.main-tab.selected` come etichetta della ricerca aperta
- `.ag-root-wrapper` → `__agComponent.gridApi` e l'API della griglia
- il contatore «Sono stati trovati N risultati» e la prova di completezza
- i nomi dei campi della ricerca Impianto (`Codice`, `Nominativo`, `Comune__*`, …)

Tutto il resto di questo file resta **candidato**: osservato, usabile, non ancora
convalidato da un risultato. Le nove aree sono state mappate il 03/09/2026 su Azienda
3 — rotte, sottosezioni, azioni ed entità cercabili sono state viste, ma nessuna di
esse ha ancora prodotto un risultato che il titolare abbia confermato.

## Come ci si arriva

Portale `start.dcN.unico3.cloud` → riquadro *Applicazioni* → `Unico³ Web` / `APRI`.
Apre una **nuova scheda** su `app.dc3.unico3.cloud`, sempre su **Azienda 1**.

Il vecchio Unicò3 "classico" del portale è una **RemoteApp Windows**: su Mac non
parte. La skill vive solo nel web.

## L'azienda attiva sta nella URL

```
https://app.dc3.unico3.cloud/?c=/C<tenant>/A3/#/assistenza/home/search/Impianto/semplice
                                └── azienda ──┘└──────── rotta interna ────────┘
```

L'identificativo comprende il tenant, perché «A3» da solo nomina la terza azienda di
*qualche* installazione, non la nostra: `azienda_da_url` restituisce `C<tenant>/A3`, e
l'azienda 3 di un altro tenant vale produzione.

Quali aziende siano sandbox lo dice solo `UNICO3_SANDBOX` (vuota di default: tutto è
produzione). Nell'installazione su cui la skill è nata la produzione era A1 e le sandbox
dichiarate A3 e A2; la tua può essere diversa. Una sandbox può contenere **storico reale**
(impianti e documenti veri): non è per forza vuota. Esempio di sandbox di sperimentazione, con
le tabelle principali allineate ad A1 (tipologie d'impianto, gas, combustibili,
operatori RDI, tecnici, le operazioni dei casi di prova); operazioni restanti, marche e
modelli possono essere ancora quelli di A2. Vedi `references/guardrail.md`.

Si cambia da icona utente in alto a destra → *Sessione Corrente* → `Azienda: 1 2 3`.
**Non** leggere l'azienda dal testo della pagina: quel riquadro elenca tutti e tre i
numeri insieme, quindi cercare "3" nel testo è un falso positivo garantito. La
funzione giusta è `u3.sessione.azienda_da_url`.

Conseguenza utile: **due schede di Chrome possono stare su due aziende diverse
insieme.** Non è dedotto dalla forma della URL: è stato usato davvero il 02/09/2026
per ricostruire dei grafici da un'azienda all'altra. Osservazione di una sessione precedente.

## Struttura

Menu principale (hamburger in alto a sinistra), nell'ordine:

**Assistenza · Agenda · Geolocation · Magazzino · Amministrazione · Analisi dati**
poi, staccati in basso: **Tabelle · Files · Impostazioni**.

Ogni area apre una **scheda** nella barra in alto, chiudibile con la ✕. Più schede
aperte insieme; `Alt` + `←`/`→` per passare da una all'altra.

Rotte osservate:

| Rotta | Cosa apre |
|---|---|
| `#/home` | benvenuto, Memo & Scadenze, Assistente virtuale (solo A1) |
| `#/assistenza/home/actions` · `#/assistenza/home/search/<Entita>/semplice` | Assistenza |
| `#/agenda/calendar?...` | Agenda |
| `#/geolocation` | Geolocation |
| `#/magazzino/home/actions` · `#/magazzino/home/search/<Entita>/semplice` | Magazzino |
| `#/amministrazione/home/actions` · `#/amministrazione/home/search/<Entita>/semplice` | Amministrazione |
| `#/analytics` · `#/analytics/analyze/editor/<id>` | Analisi dati |
| `#/tabelle/` | Tabelle |
| `#/files/` | Files |
| `#/impostazioni/<area>/<sezione>` | Impostazioni |

**Tre aree su nove condividono lo stesso schema** — Assistenza, Magazzino,
Amministrazione: colonnina con `Azioni` e `Ricerca`, stesso campo `Cosa stai
cercando`, stessa griglia, stesso menu ⋮. Imparata una, imparate tutte e tre. Il
colore della barra cambia per area (Assistenza blu, Magazzino arancione,
Amministrazione verde, Tabelle e Files viola): è un riscontro visivo utile, ma la
verità sta in `div.main-tab.selected`.

**La rotta si aggiorna, ma non si comanda.** Navigando, l'entità cercata compare
nella rotta; **per le RICERCHE, scrivere quella rotta nella barra degli indirizzi non cambia la
ricerca**. Verificato il 03/09/2026: portando la URL su
`.../search/Contratto/semplice`, lo schermo continuava a mostrare `RICERCA Impianto`
con i risultati precedenti. Alle ricerche si arriva a click, dal menu.

Corollario, e vale per tutta la skill: **la URL può mentire su cosa c'è a schermo.**
L'unica cosa che la URL dice sempre bene è l'azienda. Per sapere quale ricerca è
davvero aperta si legge l'etichetta della scheda interna attiva,
`div.main-tab.selected` (es. `RICERCA Impianto`).

## Assistenza → Ricerca

Due voci nella colonnina: **Azioni** e **Ricerca**.

`Cosa stai cercando` — **Assistenza: 23 entità** [misurato 03/09/2026]. L'`Id` è il
nome che compare nelle rotte:

`AttivitaUfficio` · `Bruciatore` · `Componente` · `Contratto` ·
*DettaglioDocumentoIntervento* · `DocumentoIntervento` · *FileAllegatoAssistenza* ·
`GruppoFrigo` · `GruppoTermico` · **`SuperSearch_Impegni_Tecnico`** · `Impianto` ·
`Intervento` · **`SuperSearch_OpMan`** · **`SuperSearch_OperazioniFGAS`** ·
`RataContratto` · `RCEE` · `RicambioGuasti` · `RicambioInstallati` · `Richiamo` ·
**`RdI`** · `RiferimentoImpianto` · `Scambiatore` · `UIR`

*(in corsivo i due che il filtro sui contenuti ha oscurato: dalle etichette della guida
sono «Dettaglio documento di intervento» e «File allegato assistenza»)*

Tre cose che nessuna etichetta lascia intuire: **`RdI`**, non `RichiestaIntervento`;
tre entità hanno il prefisso **`SuperSearch_`** (impegni per tecnico, operazioni di
manutenzione, operazioni F-Gas) e sono costruite diversamente dalle altre;
`RicambioGuasti` e `RicambioInstallati` sono due entità distinte.

> Prima qui ne erano scritte 16: le avevo contate **dalla tendina**, che ne rende una
> pagina per volta. Il numero giusto si legge dal view-model — tecnica in
> `interazione.md`. È la stessa trappola delle griglie, su un elenco più corto.

Schede **Semplice** / **Avanzata** [Avanzata da verificare]. In alto a destra
`RESET`, `SALVA` (salva la ricerca) e il menu ⋮.

**Cattura** c'è anche nel web: campo `Filtro cattura` più l'interruttore
`Catturati` / `Liberi`, esattamente come lo descrive il wiki per NET.

Filtri della ricerca Impianto (scheda Semplice): terne
Tutti/Con libretto emesso/Senza libretto, Tutti/Con contratto attivo/Senza
contratto, Tutti/Con targa/Senza targa, Tutti/Attivi/Dismessi (**default: Attivi**);
caselle Non georeferenziabile, Con impianti collegati, Singola unità immobiliare;
campi Tag impianti, Da codice, A codice, Gruppo, Suffisso, CAT, Nominativo,
Telefono, Indirizzo, Numero civico, Comune, Zona, Provincia, Regione.

**Attivi è preselezionato.** Una ricerca "tutti gli impianti" che non tocca quel
gruppo restituisce solo gli attivi e non lo dice.

### Assistenza SMART, non STANDARD — confermato

I campi **Tag impianti** e **CAT** nella ricerca e il contatore **Ticket** nel widget
Assistente virtuale lo suggerivano. **Confermato il 03/09/2026 aprendo una scheda
impianto**: c'è la sezione **VINCOLI** nella colonna di sinistra, e i Tag compaiono
come etichette sull'intestazione della scheda. Sono entrambe funzioni SMART.

## Magazzino

`Azioni`: Nuovo articolo · Nuova voce catalogo · Crea articoli da catalogo ·
**Importa catalogo Excel/CSV** · **Importa catalogo dal database**. [Le prime cinque
sono quelle visibili senza scorrere.]

Le due *Importa catalogo* sono **scritture di massa**: vanno trattate come tali, cioè
conferma esplicita e mai su produzione senza anteprima.

`Ricerca` — 10 entità: Articolo · Catalogo · Dettaglio lista materiale · File allegato
magazzino · Lista materiale · Listino · Materiale in ordine · Matricola · Movimento di
magazzino · Scorte articoli.

## Amministrazione

`Azioni`: Nuova anagrafica · Nuova anagrafica da impianto.

`Ricerca` — 10 entità: Anagrafica · Dettaglio documento emesso · Dettaglio documento
ricevuto · Documento emesso · Documento ricevuto · File allegato amministrazione ·
Memo · Ricevuta fiscale · Riferimento anagrafica · Scadenziario unificato.

`Dettaglio documento emesso` è lo stesso cubo che alimenta i grafici di **Analisi
dati** (vedi la sezione Analisi dati): la fatturazione
si può leggere da qui o da lì, e devono tornare uguali.

## Agenda

Rotta `#/agenda/calendar?...`, e **tutto lo stato sta nella query**: `Data`, `Days`,
`AttivitaInizio`, `AttivitaFine`, `Cat`, `TipoAttivita`, e `Tecnici` come array di id.
[Se quella query sia *comandabile* scrivendola, come per le ricerche, **non è stato
verificato** — e per le ricerche non lo è.]

A sinistra gli **impegni non programmati**, su sei cartelle: `Manutenzioni` ·
`Attività ufficio` · `Richiami` · `Richieste Intervento` · `Altri Impegni` ·
`Cestino`. Il wiki ne elencava quattro per NET: il web ha in più *Attività ufficio* e
*Cestino*, e chiama *Richieste Intervento* quelle che il wiki chiama Chiamate.
Colonne: Impianto (Codice, Nominativo, Telefono) e Operazione (Op., Scad. Legale,
Scad. Programmata, Tipo Macchina). Sopra, due selettori di data che delimitano la
finestra delle attività.

A destra il **calendario**, una colonna per tecnico identificata dalla sigla. Su
una sandbox i tecnici in vista sono tanti quanti gli id nella URL. In alto: numero di giorni
in vista, data, layout colonne, preset (`Default`), filtro tecnici a chip, e le icone
aggiungi-tecnico / aggiorna / stampa / ⋮.

**La griglia degli impegni non sta dentro `.search-results`**, quindi non può essere
scambiata per il risultato di una ricerca — verificato. Con l'Agenda in primo piano
la guardia dell'estrazione conta zero riquadri visibili e si ferma, invece di leggere
la griglia sbagliata.

## Geolocation

`#/geolocation`. Una mappa e basta: nessuna sottosezione, nessuna griglia.

## Tabelle

`#/tabelle/`. Elenco unico con campo **Cerca**, raggruppato in quattro cartelle —
**Amministrazione, Assistenza, Generali, Magazzino** — più tre sottogruppi (*Modelli
installato*, *Tag*, *Dati di conformità*). In tutto **79 nodi: 4 aree, 3 sottogruppi,
72 tabelle**, coerente con le «~70» del wiki.

> ⚠️ **Corretto il 03/09/2026 contandole nell'albero del web: sono ~68**, e distribuite
> diversamente (Amministrazione ne ha **una sola cartella con due tabelle**). Rotte,
> conteggi e campi in `tabelle-rotte.md`.

Nel DOM ogni nodo è `table-tree .table-node`, e si espande cliccando il `.pointer`
interno.

Le 72, per area:

- **Amministrazione** (4) — 1^ nota · Causali contabili · Causali e conti di default ·
  Categorie cespiti
- **Assistenza** (38) — *Modelli installato*: Bruciatore, Componente, Gruppo Frigo,
  Gruppo Termico, Scambiatore, UIR · *Tag*: impianti, modelli bruciatore, modelli
  componente, modelli gruppo frigo, modelli gruppo termico, modelli scambiatore,
  modelli UIR, RDI · Anomalie intervento · Combustibili · Fluidi GAS · Fornitori
  energia · Impianti di riciclaggio · Interlocutori RDI · Motivi dismissione · Motivi
  RDI · Motivi ritorno intervento · Operatori RDI · Sottotipi altro impegno · Squadre
  Tecnici · Tecnici · Tipologie attività ufficio · Tipologie componente · Tipologie
  contratti · Tipologie garanzie installati · Tipologie guasto · Tipologie impianti ·
  Tipologie intervento · Tipologie operazioni di manutenzione · Tipologie RDI · Voci
  validazione intervento
- **Generali** (15) — Aliquote IVA · Anagrafiche azienda · Banche · Comuni · Enti ·
  Glossario · Marche · Numerazioni · Pagamenti · Tag anagrafiche · Tipologie commesse ·
  Tipologie documenti · Tipologie file allegato · Unità di misura · Zone
- **Magazzino** (15) — *Dati di conformità*: Tipi giunzione, Tipologie componente
  conformità, Tipologie materiale · Attrezzature furgoni · Cantieri · Causali
  movimenti · Dotazioni standard e scorte minime · Famiglia merceologica · Furgoni ·
  Gruppi merceologici · Listini · Magazzini · Magazzini generici · Tag articoli ·
  Tipologie attrezzature furgoni · Tipologie lista materiale

Qui vive metà della zona rossa: `Numerazioni`, `Tipologie documenti`, l'accorpamento,
la rinomina di una voce e le operazioni massive con filtri attivi. Vedi
`references/guardrail.md` prima di toccare qualunque cosa in questa area.

## Files

`#/files/`. Documentale: albero cartelle a sinistra, elenco a destra con `Nome`,
`Ultima Modifica`, `Dimensioni File`. In alto a destra aggiorna · nuova cartella ·
**carica** · vista.

**Non è una AG Grid.** La procedura di estrazione non si applica qui, e infatti la
guardia si ferma da sola («griglie visibili: 0») invece di leggere la griglia di
un'altra scheda.

Le cartelle di primo livello sono configurazione dell'azienda. Esempi: Allegati ·
Cataloghi · DiCo (una per anno) · ENEA · EXPORT · F-GAS · Fatture XML · FattureSDI ·
FOTO ALLEGATE · IMPORTAZIONE · Inventario · ListaMateriale · LOGO · Mobile ·
Preventivi · RICHIESTE INTERVENTO · Schede tecniche.

## Impostazioni

`#/impostazioni/<area>/<sezione>`, con briciole di pane. Tre aree: **Agenda**
(`Visualizzazione`, `Scadenziario`), **Assistenza**, **Generale**. [Le sezioni di
Assistenza e Generale non sono state aperte.]

`Impostazioni > Agenda > Visualizzazione` decide **cosa si legge sulle card
dell'agenda**: modelli di testo composti da campi — Informazioni Richiesta di
Intervento (`Codice Impianto`, `Nominativo`, `Motivo`), Informazioni Intervento
Eseguito (`Nominativo` - `Tipologia Intervento`), Informazioni Altro Impegno (`Tipo` -
`Descrizione`) — più i tecnici in vista di default. Si conferma con `SALVA`.

**Questa area cambia il comportamento dell'applicazione per tutti gli utenti**, non
solo per chi la modifica. Nessuna scrittura qui senza richiesta esplicita, nemmeno su
Azienda 3.

## Le griglie sono AG Grid, e questo cambia tutto

Il risultato di una ricerca è una **AG Grid** (`.ag-root-wrapper`, righe `.ag-row`).
Misurato sulla ricerca Impianto di Azienda 3:

| | |
|---|---|
| dichiarati in pagina | **N** |
| righe presenti nel DOM | **26** |
| righe nel modello della griglia | **N** |

Leggere il DOM e fermarsi lì significa riportare 26 righe su migliaia **senza
accorgersene**. La procedura corretta sta in `references/flussi/estrazione.md` e non
è opzionale. Provata sul campo il 03/09/2026: prova passata, totale estratto uguale al dichiarato, e le
aggregazioni per provincia e per tipologia sommano entrambe esattamente al totale.

Il modello è **client side**: `rowModelType` non è impostato, quindi tutte le righe
sono già nel browser dopo la ricerca. Si arriva all'API così:

```js
Array.from(document.querySelectorAll('.search-results'))
  .filter(e => e.offsetParent !== null)[0]      // il riquadro visibile, non il primo
  .querySelector('.ag-root-wrapper').__agComponent.gridApi
```

**Mai `document.querySelector('.ag-root-wrapper')` da solo**: prende la prima griglia
del documento, che con una ricerca precedente rimasta nel DOM è quella sbagliata.
Vedi la trappola in fondo. La forma con la guardia completa — che si ferma se i
riquadri visibili non sono esattamente uno — sta in `flussi/estrazione.md`.

Da lì `getDisplayedRowCount()`, `forEachNode()`, `forEachNodeAfterFilter()`, e
`.columnApi.getAllColumns()` per le definizioni di colonna.

Menu ⋮ della griglia: **Stampa · Esporta · Personalizza campi · Personalizza
ordinamento · Cattura · Mostra totali**.

## Il framework è Aurelia

Gli elementi portano la classe `au-target`; ci sono elementi custom `x-button`,
`context-item`, `x-material`. **Non è Angular Material**, quindi:

- i menu **non** stanno in `.cdk-overlay-container`. Un menu aperto è
  `div.x-material.dropdown-menu`, le voci sono `context-item`, il click va sull'`a`
  interno;
- i menu a tendina dei campi (es. `Cosa stai cercando`) invece espongono
  `[role="option"]` e si leggono con quello.

Altri contenitori utili, verificati:

| Selettore | Cos'è |
|---|---|
| `div.search-results` | il riquadro di **una** ricerca: contiene sia il contatore «Sono stati trovati…» sia la sua griglia |
| `div.main-tab.selected` | la scheda interna attiva, la sua etichetta dice quale ricerca è aperta |
| `div.assistenza-home-tab.active` | la voce attiva fra `Azioni` e `Ricerca` |
| `x-tab.selected` | la scheda `Semplice` / `Avanzata` |

## Trappole verificate

- **Il conteggio dichiarato e il DOM non coincidono mai** su risultati grandi. Il
  numero vero è quello della griglia, non quello che si vede.
- **Le righe non portano tutti i campi delle colonne.** Sulla ricerca Impianto: 33
  colonne definite, 21 chiavi nell'oggetto della prima riga. Una chiave assente non
  vuol dire valore vuoto — vuol dire che quel campo non è stato spedito per quella
  riga. Non confondere le due cose in un conteggio.
- **Colonne duplicate.** `MotivoDismissione__Descrizione` compare due volte fra le
  33 definizioni. Deduplicare per `field` prima di costruire un'intestazione.
- **Alcune stringhe tornano `[BLOCKED: Base64 encoded data]`.** È il filtro di
  sicurezza del browser, non un errore di Unicò: scatta su nomi che sembrano dati
  codificati. Rimedio: **non riversare mai strutture intere**, chiedere i campi per
  nome. Vale anche per il DOM — ieri (02/09) lo stesso filtro aveva bloccato una
  lettura che conteneva la query string, e mi aveva fatto credere che
  `javascript_tool` fosse disabilitato. Non lo è.
- **`APRI` dal portale porta sempre su Azienda 1.** Verificare l'azienda dopo ogni
  apertura, prima di qualsiasi cosa.
- **La ricerca precedente resta nel DOM.** Contatore e griglia vanno quindi presi
  **dallo stesso `div.search-results` visibile**, mai il primo che si trova nel
  documento: altrimenti si accoppia il contatore di una ricerca con la griglia di
  un'altra, e i due numeri possono anche coincidere per caso — certificando come
  completa un'estrazione che non c'entra nulla.

  **Vale anche per le sonde usa-e-getta**, non solo per il codice della procedura.
  Mappando i Files ho scritto al volo un `document.querySelector('.ag-root-wrapper')`
  per leggere l'elenco cartelle: mi ha restituito **migliaia di «cartelle»** con dentro dei
  `Tipologia__Id`, perché aveva letto la griglia della ricerca Impianto rimasta
  aperta. Nessun errore, nessun avviso, un numero plausibile e sbagliato. Ogni volta
  che si tocca una griglia si parte dal contenitore visibile, anche per due righe di
  diagnostica.

- **Ogni scheda aperta lascia la sua griglia nel DOM**, non solo le ricerche: con
  Assistenza e Agenda aperte insieme ce ne sono due. Quelle che non sono ricerche
  però stanno fuori da `.search-results`, quindi la guardia le ignora.

## Le scritture del web: una CONFERMA, una PUT

Misurato il 14/10/2026 su A2 con un registratore di `fetch` e `XMLHttpRequest` nella pagina,
incrociato con il registro di rete del browser. Compilare wizard e modali non scrive:
passano letture, il long poll del tempo reale e qualche `POST` di calcolo.
Ogni CONFERMA misurata ha fatto 1 sola scrittura, sempre `PUT` sotto `/backend/<area>/json/reply/`;
nessuna GET con effetti. Gli `Upsert*` servono per creare e per modificare: in creazione
`CompositeId` (o `Id`) è null, in modifica porta l'identificativo, e la modifica di una
sezione manda solo quella sezione. Il `fetch` del client passa da `XMLHttpRequest`: un
registratore che avvolge entrambi vede ogni richiesta due volte.

| Salvataggio | Endpoint (`PUT`) | Risposta |
|---|---|---|
| impianto nuovo con anagrafica | `assistenza/…/CreazioneImpianto` | 200 (corpo non registrato) |
| tipologia dell'impianto | `assistenza/…/UpsertTipologiaImpianto` `{IdImpianto, IdTipologia}` | 204, nessun corpo |
| GT nuovo o una sua sezione | `assistenza/…/UpsertGT` | `{Id}` |
| sezione Informazioni del GT | `UpsertGT` `{CompositeId{IdOrMobileId}, Informazioni{Matricola, Ubicazione[, DataCostruzione, DataInstallazione, CausaleInstallazione]}}` | `{Id}` |
| componente | `assistenza/…/UpsertComponente` | `{Id}` |
| gruppo frigo, circuiti compresi | `assistenza/…/UpsertGF` | `{Id}` |
| un circuito del GF | `assistenza/…/UpsertCircuitoGF` | `{Id}` |
| voce del piano (impianto, GT, GF) | `assistenza/…/UpsertOperazioniDiManutenzione` | `{Id}` |
| eliminazione di una voce del piano | `assistenza/…/CancellaOperazioneDiManutenzione` | 204 |
| articolo nuovo | `magazzino/…/UpsertArticolo` | `{Id}` |
| listino base o di un fornitore | `magazzino/…/UpsertListinoSchedaArticolo2` | 204 |
| movimento di magazzino (DDT) | `magazzino/…/UpsertMovimentoMagazzino` | 204 |
| attività d'ufficio | `assistenza/…/CreaNuovaAttivitaUfficio` | `{Id}` |
| richiesta di intervento | `assistenza/…/UpsertRdI` | `{Id, DataUltimaModifica}` |

Sono 13 endpoint di scrittura misurati. Base e fornitore del listino li distingue
`IdListino`. Le `POST` che non scrivono: `ExecuteSearch`, `ValoriMovimentoSchedaArticoloRequest`,
`SommaConPrecisioneDecimale`, `GetDatiPianificazionePerOpMan`. `SchedaArticolo` e
`ListiniSchedaArticolo` sono GET. Corpi campo per campo e classificazione per il cancello
di un eventuale agente: da rimisurare con il registratore di richieste.
L'eliminazione dell'impianto (dialogo che chiede di scrivere ELIMINA) non è stata
eseguita: endpoint non misurato.

Correzioni di un impianto esistente, misurate su A2 il 16/10/2026 (andata e ritorno, record
riletti identici byte per byte; da rimisurare con lo stesso metodo):
- **Informazioni del GT** (matita della sezione, col mouse sopra): `Matricola` e `Ubicazione`
  viaggiano sempre; le due date (`AAAA-MM-GG`) e `CausaleInstallazione` solo se compilate,
  `null` se svuotate nella modale. Causali: Nuova installazione (`NuovaInstallazione`),
  Sostituzione marca su marca, Sostituzione marca su altra marca, Non disponibile. Ogni
  tasto nella matricola fa una GET `ControlloMatricolaInstallato`. Nessuna rilettura dopo
  il salvataggio. Il «letto» sta nel nodo `CALDAIA` di `AlberoImpianto`
  (`Installati[0].ListaInstallatiFigli[]`), con i campi vuoti assenti.
- **Tipologia**: le voci ammesse vengono da `GET …/QueryTipologieImpianto?IdsInclusi=<attuale>&IdImpianto=<Id>&IncludiOpMan=false&IncludiEsclusiDaListe=false&IsGetUtilizzo=false`,
  filtrate per impianto (sull'impianto N di A2 solo IND e RES; «Impianto misto» non
  compare nemmeno con gli esclusi). Il cambio tocca tre foglie di `SchedaImpianto`
  (`IdTipologiaImpianto`, `TipologiaImpianto.Id`, `.Descrizione`) e **non aggiunge né
  toglie voci del piano**: albero identico a metà giro.
- `SchedaImpianto` ripetuta con un `fetch` nudo dalla pagina torna un oggetto vuoto (`Id` 0):
  serve l'intestazione della sessione. `PianoDiManutenzione` invece risponde.

### Le tabelle scrivono con `<Entita>Upsert`, a lista

Misurato il 14/10/2026 su A2, allineando le tabelle ad A1. Le tabelle di configurazione
non usano `Upsert<Entita>` come i record: l'endpoint è **`<Entita>Upsert`** e il corpo è
**una lista** (`[{…}]`), anche per una voce sola. In creazione la voce porta un `UUID`
generato dal client e solo i campi valorizzati; in modifica porta `Id` e solo i campi
cambiati (l'operazione di manutenzione aggiunge sempre `DurataMedia: "00:00"`).
L'esclusione dalle liste è una modifica: `[{Id, IsEsclusoDaListe: true}]`. Tutte 200.

| Tabella | Endpoint (`PUT`) |
|---|---|
| Tipologie impianti | `TipologiaImpiantoUpsert[]` |
| Fluidi GAS | `FluidoGASUpsert[]` (GAS maiuscolo) |
| Combustibili | `CombustibileUpsert[]` |
| Operatori RDI | `OperatoreRdIUpsert[]` |
| Tecnici | `assistenza/json/reply/TecnicoUpsert`, record intero (il wizard manda anche contatti vuoti, licenza, colore, numerazioni) |
| Tipologie operazioni di manutenzione | `TipologiaOperazioneDiManutenzioneUpsert[]` |

Le stesse PUT rilanciate da script (`XMLHttpRequest` nella pagina) rispondono **403**:
si scrive solo dal form, una voce e una CONFERMA alla volta.

## Ancora da verificare

Le voci aperte si annotano dove le scopri, nel file dell'area. Quelle già chiuse hanno la risposta in
`flussi/ricerca-avanzata.md`, `ricerche.md`, `adempimenti.md` e `aree-minori.md`.

---

# Entità cercabili nelle altre aree, filtro cattura, CAT

**Amministrazione — 10 entità**: `Anagrafica` · *DettaglioDocumentoEmesso* ·
*DettaglioDocumentoRicevuto* · `DocumentoEmesso` · `DocumentoRicevuto` ·
*FileAllegatoAmministrazione* · `Memo` · `RicevutaFiscale` · *RiferimentoAnagrafica* ·
`Scadenza`

**Magazzino — 10**, dalla guida (da riconfermare col view-model quando la ricerca è
aperta): Articolo · Catalogo · Dettaglio lista materiale · File allegato magazzino ·
Lista materiale · Listino · Materiale in ordine · Matricola · Movimento di magazzino ·
Scorte articoli.

## Il filtro Cattura ha un elenco proprio, e corto

Non si cattura su qualsiasi campo. Le entità disponibili come **filtro cattura**:

- **Assistenza — 6**: `Impianto`, `TipologiaImpianto`, `Comune`, `MotivoDismissione`,
  `Zona`, `Combustibile`
- **Amministrazione — 4**: `Anagrafica`, `CAT`, `Comune`, `TipoPagamento`

## Rotte tabella

L'elenco completo, con conteggi e campi, sta in **`tabelle-rotte.md`**: qui non si
duplica, perché due elenchi divergono sempre.

Quello che serve sapere anche da qui: **non c'è una regola per il nome**. `Zona` e
`TipoAttivitaUfficio` usano il prefisso `Tipo`, `TipologiaIntervento` usa `Tipologia`.
La rotta si scopre cliccando la voce nell'albero o leggendo l'`Id` dal view-model — e
una rotta inventata **lascia la pagina precedente senza dire niente**.

## Un'azienda può essere multiCAT

`listaCat` può esporre **più CAT**, con Id numerico o alfanumerico. Conseguenza pratica: nelle maschere che chiedono il CAT — invio
telematico, distinte CBI, serie di numerazione — **la scelta esiste davvero** e non è una
formalità.
