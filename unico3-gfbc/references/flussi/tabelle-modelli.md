# Correggere i modelli installato (gruppi termici e frigo)

Procedura **eseguita e misurata su una sandbox**, correggendo i dati tecnici dei
modelli gruppo termico delle marche Immergas, Hoval, Wolf, Clivet, Ariston, Aermec.

È il flusso da usare quando si sistemano le tabelle `ModelloGruppoTermico`,
`ModelloGruppoFrigo`, `ModelloComponente`, `ModelloUIR`, `ModelloBruciatore`.

---

## Le dimensioni del problema

La tabella dei modelli è molto più grande del parco macchine reale: migliaia di modelli
gruppo termico e frigo, contro poche centinaia di gruppi termici installati.

Conviene partire dai modelli **che qualcuno usa davvero**: incrociando modelli e
installati, i modelli con dati mancanti effettivamente usati sono pochi.
Il resto è coda da sistemare senza fretta.

### Quanto manca davvero

Letto dallo snapshot completo delle due tabelle, non a campione:

In una sandbox la maggior parte dei campi tecnici dei frigo (potenze, EER, COP, fluido, carica gas) e molti dei termici (portata, potenza, rendimento, NOx, codice prodotto) risultavano vuoti.

Numeri che spaventano e non devono: la tabella dei modelli è molto più grande del parco
macchine. Filtrando sui modelli **con almeno due apparecchi installati**, tolti i
generici e le voci tipo «Imp. Bagno», restano pochi modelli veri che coprono la maggior parte degli
apparecchi. Sono quelli per cui vale la pena cercare la scheda tecnica.

⚠️ **La carica gas dei frigo non è un campo del modello**: sta in `ListaCircuiti`, come
`KgFGas` di ogni circuito, accanto a `IdFluidoFGas`. Chi la cerca fra i campi di testata
non la trova e conclude che non esista.

E attenzione a una scorciatoia che sembra ovvia: alcuni apparecchi installati **hanno già**
la loro carica dichiarata, e stanno su modelli che non ce l'hanno. Copiarla
all'indietro sul modello è però una **deduzione**, non una misura — la carica di targa
del modello e quella effettiva della macchina in campo non sono lo stesso numero, e per
il registro F-Gas conta la seconda. Si prende dalla scheda.

## L'errore che questa tabella contiene più spesso

> **La portata è quella del sanitario, la potenza quella del riscaldamento.**

Non è un sospetto: è misurato. Dal libretto ufficiale *VICTRIX TERA 24/28 V2*:

| | Qn riscaldamento | Qnw sanitario | Pn riscaldamento | Pnw sanitario |
|---|---|---|---|---|
| TERA 24 V2 | **24,5** | 28,7 | **24,0** | 28,0 |
| TERA 28 V2 | **28,6** | 32,7 | **28,0** | 32,0 |

In Unicò la TERA 24 V2 aveva portata **28,70** e potenza **28,00**: due valori del
sanitario. La TERA 28 V2 aveva portata **32,70** (sanitario) e potenza **28,00**
(riscaldamento): mischiati.

**La regola sta scritta nella fonte**, nel PDF Immergas per la pratica ENEA:

> «Il valore di "Potenza nominale" da inserire, per i modelli con potenza differenziata
> per riscaldamento e produzione sanitaria, è quello riferito al funzionamento **in
> riscaldamento**.»

Quindi la terna **portata / potenza / rendimento si prende tutta dal riscaldamento**.

⚠️ **Il numero nel nome commerciale non dice quale.** Per la famiglia TERA il numero è
il riscaldamento (TERA 28 → 28 kW in riscaldamento). Per la famiglia ZEUS è il
**sanitario** (ZEUS 32 → 28,0 kW in riscaldamento; ZEUS SUPERIOR 25 → 20,2 kW). Le due
convenzioni convivono nello stesso listino: si guarda la scheda, non il nome.

## Il rendimento è un campo calcolato, ma scrivibile

Cambiando portata o potenza nella maschera, **Unicò ricalcola da solo il rendimento**
come `potenza / portata × 100`. Il campo resta editabile dopo.

Conseguenze pratiche:

1. **L'ordine è obbligato**: prima portata, poi potenza, **poi** il rendimento. Scritto
   per primo, il ricalcolo lo cancella.
2. I rendimenti assurdi già in tabella (**100%**, **114,29%**) non erano dati inventati:
   erano *il risultato del calcolo* su una portata sbagliata. Il 114,29% di `VICTRIX
   ZEUS 32` è 32/28. Sistemare portata e potenza li fa sparire da soli.
3. Questo dà un **controllo di coerenza gratuito**, che non richiede nessuna scheda:
   dove `|potenza/portata×100 − rendimento| > 3` c'è quasi sempre un errore. Su centinaia di
   modelli con tutti e tre i valori, alcuni sono incoerenti e alcuni hanno potenza **maggiore**
   della portata, che è fisicamente impossibile per una caldaia.

   ⚠️ Ma il controllo *segnala*, non *decide*: un modello combinato può avere la potenza
   sanitario accanto alla portata riscaldamento e sembrare impossibile senza esserlo.
   Si apre la scheda e si guarda.

## Come si scrive un valore, che non è ovvio

| Come scrivi | Separatore decimale | Il valore tiene? |
|---|---|---|
| Tastiera (`computer` → `type`) | **virgola** — `28,60` | sì |
| JavaScript (setter + evento `input`) | **punto** — `28.6` | sì per portata e potenza |

**Con la virgola scritta via JS il campo resta vuoto senza dare errore.** È la trappola
peggiore del lotto: lo script riferisce «scritto», il campo è vuoto, e confermando si
azzera un dato che prima c'era. Difesa: **si rilegge sempre il campo dopo averlo scritto
e prima di confermare**, e se è vuoto non si conferma.

**Il rendimento forzato via JS non tiene**: al salvataggio prevale il ricalcolo (scritto
97,8 → salvato 97,96). Se serve il valore di targa esatto, quel campo si digita da
tastiera.

## La procedura

1. **Aprire la tabella**: `location.hash = '#/tabelle/ModelloGruppoTermico/table'`.
2. **Trovare il modello** con la casella `Cerca` in alto nella griglia. È **fuzzy per
   parole**: cercando `VICTRIX TERA 28 KW V2` compaiono anche `TERA 24 PLUS V2`. Non si
   presume che la prima riga sia quella giusta.
3. **Aprire la scheda**: doppio click sulla riga. Apre il dialogo di *testata* (marca,
   codice prodotto, descrizione, tag, escluso da liste) e **sotto** carica la scheda del
   record. Si chiude il dialogo con ANNULLA se si volevano i dati tecnici.
4. **Aprire i dati tecnici**: la **matita compare solo all'hover** sul pannello
   `Dati generali`, in alto a destra. Nel DOM è `editable x-icon-button.edit`.
5. **Verificare su quale record si sta per scrivere** — vedi sotto, non è opzionale.
6. Scrivere portata, potenza, **poi** rendimento. Rileggere.
7. `MODIFICA`.
8. **Verificare che abbia salvato davvero**, rileggendo dal modello della griglia.

### La guardia che ha evitato un danno vero

`#/tabelle/ModelloGruppoTermico/detail/<id>/data` seleziona la riga giusta, **ma la URL
cambia prima della scheda**. Leggendo subito, la scheda a schermo è ancora quella
precedente.

È successo davvero: navigato alla TERA 28 V2, lo schermo mostrava ancora la
TERA 24 V2. Senza guardia avrei scritto i dati della 28 sulla 24 — e sono due modelli
che differiscono di 4 kW, con molti apparecchi installati dietro.

La difesa è leggere l'intestazione della scheda e confrontarla con quella attesa:

```js
// unico <span> senza figli che contiene " - ": "MARCA - MODELLO"
const c = Array.from(document.querySelectorAll('span'))
  .filter(e => e.offsetParent !== null && e.children.length === 0
            && / - /.test(e.textContent) && e.textContent.length < 90);
const vista = c.length === 1 ? c[0].textContent.trim() : ('AMBIGUO:' + c.length);
if (vista !== attesoTesto) { /* NON scrivere */ }
```

⚠️ **Ad applicazione già caricata, cambiare l'hash del `detail` non cambia record**: il
routing riporta su quello precedente. Per spostarsi si usa la casella `Cerca` della
griglia e si clicca la riga.

### «Confermato» non è «salvato»

Il click sul pulsante restituisce sempre «fatto». Su `VICTRIX TERA 28 V2` (id N) la
PUT a `ModelloGruppoTermicoUpsert[]` ha risposto **200**, il payload conteneva
`"PortataKW":"28.60"`, e dopo un reload completo la portata era ancora **32,70**.
Quattro tentativi, nessun messaggio d'errore, nessuna modifica. **Caso aperto.**
Gli altri record dello stesso lotto si salvano normalmente.

Regola che ne esce: la prova del salvataggio è **rileggere il dato**, e va riletto in
una chiamata **separata** — subito dopo il click la griglia restituisce ancora il valore
vecchio. È la stessa trappola del contatore letto troppo presto.

## Cosa non si tocca

- **Il NOx**. Il campo è la **classe** UNI EN 15502 (6 = la migliore), non i mg/kWh. Il
  PDF ENEA di Immergas **non contiene il NOx**: dedurre «è a condensazione quindi è 6» è
  una deduzione, non una misura, e su centinaia di modelli senza NOx produrrebbe altrettanti dati
  inventati. Si valorizza solo con una fonte che lo dichiari per quel modello.
- **La descrizione del modello**. Rinominare una voce di tabella è zona rossa
  (`guardrail.md`): lo storico di tutti gli installati che la usano cambia nome.
- **L'accorpamento dei doppioni**. Irreversibile: vietato in produzione, su una sandbox chiede conferma.

## Accorpare i doppioni — provato su Wolf

**L'ordine che viene in mente è sbagliato, e il database lo dimostra.**

Sembra naturale accorpare prima le marche e poi i modelli. Non si può: la tabella dei
modelli ha una **chiave univoca `(marca, descrizione)`**, e spostare i modelli della
marca sorgente sulla destinazione crea un duplicato. L'errore vero, letto in console
(a schermo compare solo *«Si è verificato un errore durante l'elaborazione»*):

```
Non è possibile inserire la riga di chiave duplicata nell'oggetto 'dbo.Tab052'
con indice univoco 'IX_Tab052'. Valore della chiave duplicata: (<IdMarca>, MGK-210).
```

**L'ordine giusto è l'inverso: prima i modelli omonimi, poi la marca.** Accorpare due
modelli con lo stesso nome ma marca diversa **è permesso dall'app** — e quando le due
marche sono la stessa azienda scritta in due modi, è anche corretto. Fuori da quel caso
non si fa: due modelli omonimi di marche davvero diverse sono apparecchi diversi.

Quante collisioni ci sono si conta prima, sui dati estratti, non a mano.

### La sequenza misurata

| Passo | Esito |
|---|---|
| 1. Accorpo `MGK-210` (WOLF, id N) su `MGK-210` (Wolf Italia, id N) | modelli GT N → **N−1** |
| 2. Accorpo la marca `WOLF` su `Wolf Italia S.r.l.` | marche N → **N−1** |
| 3. Verifico gli installati | stessi installati prima e dopo, tutti sulla marca di destinazione |

### Cosa chiede l'interfaccia, e dove inganna

- **`ACCORPA RIGHE` vive nella selezione multipla**, non nel menù ⋮ (che ha solo Esporta
  e Stampa). La guida parla di un menù «Utilità»: è il terminale Windows, nel web non c'è.
  Si attiva la modalità con la casella a sinistra del campo `Cerca`.
- ⚠️ **La casella in testata alla griglia seleziona TUTTE le righe filtrate.** Con un
  filtro attivo ne ho selezionate 5 con un click solo. Prima di accorpare si conta:
  `gridApi.getSelectedRows()` deve dare esattamente le righe volute, e `forEachNodeAfterFilter`
  dice quante sono visibili — se i due numeri non tornano, c'è selezione fuori vista.
- ⚠️ **Il numero da digitare nella finestra arancione è quello delle righe che
  spariscono, non di quelle selezionate.** Con 2 selezionate e 1 destinazione, chiede `1`.
- ⚠️ **La tendina della destinazione mostra solo la descrizione.** Accorpando due modelli
  omonimi si vedono **due voci identiche**, senza la marca, e il binding Aurelia non
  espone l'Id. Non c'è modo di distinguerle a schermo: si sceglie, si conferma, e si
  **verifica dopo** quale Id è sopravvissuto.
- ⚠️ **Uscendo dalla selezione multipla il filtro di ricerca si azzera**, ma le righe
  restano alle stesse coordinate. Un doppio click «sulla stessa riga» ha aperto
  `*** Generico` invece di `Wolf Italia`. Si rilegge sempre il record aperto.
- ⚠️ **I dialoghi sopravvivono al cambio di rotta**: il dialogo `Accorpa` della tabella
  Marche è riapparso sopra la tabella Modelli. Non si conferma mai un dialogo di cui non
  si è verificato il contesto; nel dubbio si ricarica la pagina.

### ⚠️ La selezione sopravvive al cambio di filtro

**È la trappola peggiore di tutto questo flusso.** Accorpato un gruppo, ho cambiato il
filtro e selezionato le due righe nuove: `getSelectedRows()` ne riportava **tre** — la
destinazione del gruppo precedente era ancora selezionata, fuori dalla vista.

Confermando avrei accorpato uno split Clivet da 5,3 kW dentro una macchina da 16 kW,
con molti apparecchi installati dietro, in modo irreversibile.

Unicò lo segnala con una fascia arancione *«ATTENZIONE: ci sono N righe selezionate non
visibili!»*, ma **è facile non vederla**: sta sopra la griglia e il dialogo di
accorpamento la copre. In più **non si aggiorna** dopo una deselezione: continuava a
dire «1» con zero righe selezionate.

Regola: **prima di ogni gruppo si azzera la selezione**, e la si ricostruisce per Id.

```js
const api = /* gridApi della griglia visibile */;
api.deselectAll();
const attesi = [<idA>, <idB>];               // decisi PRIMA, dai dati estratti
const presi = [];
api.forEachNodeAfterFilter(n => {
  if (n.data && attesi.includes(n.data.Id)) { n.setSelected(true); presi.push(n.data.Id); }
});
// e si controlla che siano esattamente quelli voluti prima di premere ACCORPA
api.getSelectedRows().length === attesi.length
```

Selezionare per **Id** invece che a coordinate toglie di mezzo anche il fatto che le
righe si spostano di 30 px quando compare la fascia d'avviso.

E **la destinazione precompilata non è quella giusta per definizione**: su `MU1-Y 61M`
il dialogo proponeva la riga con 2 campi su 9 invece di quella completa. Si sceglie
sempre a mano, e si rilegge il campo prima di confermare.

### Il ciclo che regge decine di accorpamenti di fila

Dopo averne fatti decine, la sequenza che non si rompe è questa — sei chiamate,
e ognuna che può fallire **si legge prima di andare avanti**:

1. `prepara([idDestinazione, ...idSorgenti])` — azzera la selezione, seleziona per Id,
   verifica il conteggio, apre `ACCORPA RIGHE`. Se torna `ERRORE…`, ci si ferma.
2. click sul campo `Destinazione` (783, 302).
3. `scegli(nome)` — **e solo se non ha dato errore** si preme `CONFERMA`.
4. Si legge quanti elementi chiede il dialogo arancione e si mette a fuoco il campo:
   `document.body.innerText.match(/numero di elementi \((\d+)\)/)` + `fuoco()`.
5. Si digita quel numero seguito da **`\n`**: l'Invio conferma.
6. `stato([...ids])` — dice il totale e **quale Id è sopravvissuto**. Nella stessa
   chiamata si può già preparare il gruppo successivo.

⚠️ **Mai concatenare la conferma a un passo che può fallire.** Scritto
`scegli(x) + ' >>> ' + bottone('CONFERMA')` su una riga sola: `scegli` non ha trovato la
voce — **e `CONFERMA` è partito lo stesso**, su una destinazione scelta dall'app e non
da me. È finita bene solo perché il campo del numero era ancora vuoto e ho potuto
annullare. La forma giusta (`window.__m` è un helper di pagina **non incluso**: `scegli` sceglie la voce nella
tendina e torna `ERRORE…` se non la trova, `bottone` clicca il pulsante per testo):

```js
const r = window.__m.scegli('CSRN-XHE 2 70.4');
r.startsWith('ERRORE') ? r : (r + ' >>> ' + window.__m.bottone('CONFERMA'));
```

Altre due cose imparate a spese di tentativi andati a vuoto:

- **La voce della tendina può avere il codice prodotto su una riga a parte**
  (`"2 70.4\nCSRN-XHE 2 70.4"`): si confronta l'**ultima riga**, non il testo intero.
- **Il campo del numero si sposta** di qualche pixel fra un dialogo e l'altro, e con lui
  il pulsante: cliccare a coordinate fallisce a intermittenza. Mettere a fuoco il campo
  via JS e premere Invio è l'unica via che ha retto per decine di volte.

### ⚠️ L'incidente dell'11/09/2026: due modelli accorpati per sbaglio

**Cosa è successo.** Dopo decine di accorpamenti riusciti, il confronto fra lo snapshot iniziale
e la tabella finale ha mostrato **due righe sparite in più del previsto**:
`CSRN-XHE 2 70.4` e `WSAT-XSC 220H`, che erano state *destinazioni* di accorpamenti
andati a buon fine. Alcuni apparecchi installati si sono ritrovati sotto modelli
sbagliati — uno da 232 kW finito su un modello da 35 kW.

**La causa più probabile**: il campo `Destinazione` del dialogo conserva l'ultimo valore
usato, e in una conferma data senza rileggerlo ha fatto da destinazione una riga di un
gruppo precedente. È la stessa famiglia della selezione che sopravvive: **lo stato del
dialogo non si azzera fra un'operazione e l'altra.**

**Come è stato scoperto**: non da un errore a schermo — tutte le operazioni avevano
detto «confermato» e i controlli intermedi tornavano giusti. È emerso solo dal
**confronto fra il conteggio atteso e quello reale** a fine giornata: N attesi,
N−2 trovati. Senza lo snapshot iniziale non ci sarebbe stato modo di accorgersene.

> **Regola che ne esce: si tiene lo snapshot pre-operazione e si riconcilia alla fine.**
> Non basta verificare ogni singola operazione: il danno può nascere fra una e l'altra.
> `spariti = id_prima - id_dopo` deve coincidere **esattamente** con quelli che si
> volevano eliminare, e gli installati vanno riconciliati per Id.

**Come è stata riparata** — il danno da accorpamento non si annulla, ma si ricostruisce:

1. I dati dei due modelli erano nello snapshot: ricreati col **+** della tabella
   (wizard in 4 passi: dati generali → altri dati → circuiti → allegati).
2. Gli apparecchi si riportano sul modello giusto dal **doppio click sull'intestazione
   della scheda installato** → *Modifica dati principali* → campo `Modello`.
   ⚠️ La maschera che si apre dalla matita accanto a `INFORMAZIONI` **non contiene il
   modello**: ha solo matricola, ubicazione e date.
3. Unicò avverte: *«modello cambiato, le potenze ed i circuiti verranno aggiornati al
   modello tabellato»*. Quindi **i dati specifici dell'apparecchio vengono
   sovrascritti** con quelli del modello: prima di cambiare, il modello dev'essere
   completo, altrimenti si perdono le potenze assorbite (è successo, e sono state
   rimesse a mano sul modello dallo snapshot).

**Cosa non si è potuto riparare**: un apparecchio *sostituito* nel 2024 vive nella
scheda **Storico installato**, e da lì **non è modificabile**. Resta con il modello
sbagliato: è un dato storico, ma è sbagliato e va saputo.

### Quello che l'accorpamento porta via

**L'accorpamento tiene i dati della destinazione e butta quelli della sorgente**, anche
quando la sorgente ne ha di più. la marca sorgente aveva il **riferimento anagrafica fornitore**
(un'anagrafica fornitore collegata), la destinazione no: dopo l'accorpamento quel legame **non
c'è più**. Si guarda cosa ha la sorgente *prima*, e si riporta a mano dopo.

**Nota**: reimpostarlo non è riuscito — il campo `Anagrafica` della marca risponde
«Nessun risultato» sia per nome, sia per codice, sia con `%`.
Probabilmente cerca solo fra le anagrafiche con ruolo Fornitore. **Rimasto da fare.**

**L'operazione è transazionale**: il primo tentativo fallito non ha lasciato niente a
metà — N marche prima e dopo, tutti i modelli al loro posto. È l'unica buona
notizia di questa pagina, e vale la pena saperla prima di avere paura di riprovare.

Infine, la finestra arancione avverte che l'operazione **può desincronizzare l'app dei
tecnici**. In una sandbox non opera nessuno; su un'azienda vera si fa fuori dall'orario di campo,
con i tecnici sloggati — vedi `guardrail.md` §5.2-bis.

## Esportare e reimportare: cosa si può fare davvero

Il menu **⋮ accanto al titolo della tabella modelli** ha tre voci: `Esporta`,
`Importa modelli`, `Stampa`. Sulla tabella **Marche** l'import non c'è.

**`Esporta` funziona** e produce un `.xlsx` con le **colonne visibili a schermo**:
Marca, Modello, Codice prodotto (e `Generatore a biomassa` sui GT). **Non esporta i
dati tecnici** — potenze, EER, COP, fluido restano fuori. Nel dialogo si toglie la
spunta *«Solo righe selezionate»* per prendere tutta la tabella.

⚠️ **`Importa modelli` NON carica un file tuo.** Scarica i listini delle marche
convenzionate — la guida dice Baxi, Westen e Immergas per i GT, **solo Immergas per i
gruppi frigo**. In una sandbox risponde:

> *«Non ci sono marche disponibili per l'importazione.»*

Quindi **il giro «esporto, correggo il file, reimporto» non esiste**. Un file corretto
resta utile come *fonte* per rifare l'inserimento a mano, o da girare a Futura SI, ma
non si ricarica da solo.

## Portare via una tabella intera senza pagarla in contesto

L'export dal menù ⋮ dà solo le colonne a schermo. Per avere **tutti i campi**, compresi
quelli tecnici, si legge il modello della griglia e si fa scaricare un file dal browser:

```js
const righe = [];
api.forEachNode(n => { if (n.data) righe.push(n.data); });
const a = document.createElement('a');
a.href = URL.createObjectURL(new Blob([JSON.stringify(righe)], {type:'application/json'}));
a.download = 'snapshot-gt.json';
document.body.appendChild(a); a.click(); a.remove();
```

Il file finisce in `~/Downloads` e si legge da lì. migliaia di modelli = pochi MB, **zero
token**: riversarli nel risultato dello strumento costerebbe decine di migliaia di token
e verrebbe troncato. È anche lo snapshot che serve per riconciliare a fine giornata.

Così si scopre dove stanno i dati che l'export non mostra. Sui gruppi frigo la **carica
gas non è un campo del modello**: sta in `ListaCircuiti`, un circuito per voce, come
`KgFGas` accanto a `IdFluidoFGas`.

## Scrivere in serie: il dialogo di testata, guidato

**La scrittura del nome passa da `ModelloGruppoTermicoUpsert[]` con sei soli campi** —
`Id, Tags, IdMarca, Descrizione, CodiceProdotto, IsEsclusoDaListe`. Verificato che **i
dati tecnici sopravvivono**: su un modello portata, potenza, rendimento,
NOx, Camera e ACS erano identici dopo un reload completo. Qui la PATCH parziale non
azzera il resto.

Il motore che guida il dialogo è uno script iniettato in pagina (~2,5 s a record).
Quattro cose imparate a caro prezzo:

1. ⚠️ **Nel DOM ci sono tante griglie quante schede aperte** — nove, in una sessione
   normale. `document.querySelector('.ag-row[row-index="1"]')` pesca da una griglia
   nascosta e restituisce una riga **senza geometria** (`0×0`): il click non arriva da
   nessuna parte. La griglia si cerca **solo dentro** la root con `offsetParent !== null`.
2. ⚠️ **Chiamare `gridOptions.onRowDoubleClicked()` da codice apre il dialogo del record
   PRECEDENTE.** Provato: chiesto il record 1, a schermo il record aperto prima, con la rotta
   ancora su `/table`. Scrivere lì avrebbe rinominato il modello sbagliato. Il doppio
   click **sintetico sulla cella** (`mousedown, mouseup, click, dblclick`) invece porta
   la rotta su `/detail/<id>/data` e carica il record giusto.
3. ⚠️ **`ANNULLA` su un modulo modificato non chiude niente**: apre una seconda conferma
   *«I dati inseriti e non salvati andranno persi. Continuare?»* con `RITORNA` e `ESCI`.
   Chi aspetta la chiusura senza premere `ESCI` resta fermo per sempre.
4. La guardia che regge tutto: prima di scrivere, **la rotta deve contenere
   `/detail/<id>/` e il campo deve valere esattamente il nome vecchio atteso**. Se uno
   dei due non torna, il ciclo si ferma invece di scrivere.
5. ⚠️ **`location.hash = ...` e `navigate` sulla stessa pagina NON ricaricano niente.**
   Cambiare solo il frammento lascia in piedi l'applicazione, i dialoghi aperti e le
   variabili. Per ripartire pulito serve `location.reload()` — e allora il motore va
   re-iniettato. Conviene tenerne una copia in `localStorage`: dopo il reload bastano
   due righe (`(0,eval)(localStorage.getItem('__motoreUnico'))`).
6. ⚠️ **Un solo ciclo alla volta.** Riprendendo a mano dopo un intoppo è facile
   lasciare vivo il timer di prima e avviarne un secondo: due cicli condividono
   `corrente` e si sovrascrivono a vicenda — le letture di stato diventano incoerenti
   («fermo» mentre invece avanza) e in teoria un ciclo può scrivere il valore
   dell'altro. Non si prova a fermare i timer a mano: si ricarica la pagina e si
   riparte una volta sola.
7. **La coda si ricalcola dai dati, non dal registro.** Dopo ogni ripartenza, invece
   di fidarsi di quanti risultano fatti, si rilegge la griglia e si tiene solo ciò che
   ancora non ha il nome giusto. Così una ripartenza non rifà e non salta niente.

### I gruppi frigo si comportano diversamente dai termici

Stessa maschera, esito diverso, e costa un'ora se non lo si sa:

| | Gruppi termici | Gruppi frigo |
|---|---|---|
| dopo `MODIFICA` il dialogo | si chiude | **resta aperto** |
| la griglia in memoria | si aggiorna subito | **spesso non si aggiorna** |
| `ANNULLA` / `ESCI` / Escape / cambio rotta | chiudono | **non chiudono niente** |

Il segnale che il salvataggio è passato, sui frigo, è che **`MODIFICA` diventa grigio**
(`x-button` prende la classe `disabled`). Letto come «pulsante rotto» fa perdere tempo:
è disabilitato *perché* ha già salvato.

La conclusione pratica è di non inseguire la chiusura del dialogo. Il doppio click sul
record successivo lo ricarica comunque, e a proteggere è la guardia — rotta
`/detail/<id>/` più nome vecchio atteso nel campo. I record che il ciclo segna
`presunto` li conferma la riconciliazione finale contro lo snapshot.

⚠️ E non ci si fida di `offsetParent !== null` per dire se un dialogo è aperto: i
dialoghi morti restano nel DOM **con geometria e stile intatti**, e anche
`elementFromPoint` li dà in cima. Su questa pagina non esiste un modo affidabile di
distinguerli: per questo il ciclo non li conta più.

### ⚠️ I dialoghi aperti sopravvivono al reload — è la sessione che li ricorda

Ricaricare la pagina **non basta** per ripartire puliti: Unicò riapre le schede della
sessione, e con loro i dialoghi rimasti aperti. Contati dopo un `location.reload()`
con una sola scheda modelli: **tre `ux-dialog` vivi**, 512×508.

Sono anche il motivo per cui il ritmo degrada: dopo un centinaio di record i dialoghi
non chiusi si accumulano e il doppio click smette di caricare quello nuovo. Chiudere le
schede doppie dalla barra di Unicò aiuta ma non li toglie tutti.

Conseguenza operativa: **il lavoro si fa a blocchi da ~100 record**, e fra un blocco e
l'altro si ricarica *dopo* aver riportato la rotta su `/table` — se si ricarica stando
su un `detail`, la sessione riapre quel dialogo e blocca il blocco successivo.

Quando il degrado non si riassorbe, ci si ferma: pochi nomi corretti e riconciliati
valgono più di molti tentati e non verificabili.

### La riconciliazione, e cosa deve dire

Esempio, dopo qualche centinaio di rinomine sui frigo:

```
righe prima N  dopo N  spariti 0  comparsi 0
nomi cambiati K | codici cambiati 0 | dati tecnici cambiati 0
nomi cambiati FUORI dal piano: 0
```

Le tre righe che contano sono le ultime: **nessun codice prodotto toccato** (era
l'errore dei tre RIELLO/SABIANA), **nessun dato tecnico perso** (la prova che la
scrittura di testata non azzera il resto), **niente cambiato fuori dal piano**.

### ⚠️ Il dialogo può mostrare un valore che non è mai stato salvato

Sembra che la griglia sia più vecchia del server: il dialogo di un modello mostra il
nome nuovo, la griglia il vecchio. **È il contrario.** Il componente del dialogo non si
azzera fra un record e l'altro e **conserva quello che ci è stato digitato**, anche
quando il salvataggio non è andato a buon fine e anche dopo `ANNULLA`.

Provato su `30GH-085-0300`: dialogo col nome pulito, griglia col nome sporco, e dopo un
reload completo **la griglia aveva ancora ragione** — sul server il nome era quello
vecchio.

Ne discende una regola secca: **il dialogo non è una fonte**. Vale come fonte solo la
griglia riletta dopo un reload, ed è per questo che la verifica vera è la
riconciliazione contro lo snapshot. Chi tratta «il dialogo mostra già il valore giusto»
come «già fatto» si segna come completati dei record che non lo sono.

#### ⚠️ Il campo si prende dall'etichetta, mai dal valore

Cercare l'input «quello che contiene il nome vecchio» sembra robusto e non lo è: quando
**il codice prodotto contiene la stessa stringa della descrizione**, nel DOM viene prima
lui, e la scrittura finisce nel codice. Il modello resta col nome sporco e **il codice
viene sovrascritto** — un danno silenzioso, perché il dialogo si chiude senza lamentarsi.

È successo su tre record: `RIELLO 3500-S455`, `RIELLO BENESSERE`, `SABIANA ATLASPLI`.
Tutti e tre avevano `CodiceProdotto == Descrizione`. Sono stati ripristinati dallo
snapshot, ma solo perché lo snapshot c'era.

Due difese, e servono entrambe:

- l'input si sceglie per **etichetta** (`Codice prodotto`, `Descrizione *`), leggendo
  `input.parentElement.parentElement.innerText`;
- si prende **l'ultimo** che corrisponde, perché **i dialoghi si impilano**: se ne resta
  uno aperto da prima, i suoi campi vengono per primi e si scrive nel record sbagliato.

E la verifica dopo il salvataggio guarda **tutti i campi toccati**, non solo il nome:
sono stati i due `DUBBIO` di fila sulla stessa marca a far fermare tutto dopo tre record
invece che dopo centocinquanta.

### ⚠️ L'unicità del nome è su TUTTA la tabella, non per marca

L'indice del database è composito — l'errore SQL di ieri diceva `(<IdMarca>, MGK-210)` — ma
**la maschera rifiuta prima**, con un *«Valore già presente»* rosso sotto il campo, se
il nome esiste **sotto una marca qualsiasi**.

Misurato: rinominare `. DIAMANTE 25 C` (marca `*** Generico`) in `DIAMANTE 25 C` è stato
respinto perché quel nome era già di CLIVET, PRIMA e FA.RE.L. — tre marche diverse. I
sei nomi accettati poco prima avevano **zero omonimi in tutta la tabella**.

Conseguenza sul piano: le rinomine si filtrano contro **tutti** i nomi della tabella, non
contro quelli della stessa marca. La differenza è grossa — molti nomi da correggere
sui GT e sui frigo risultano passabili solo in parte.

E il rifiuto va trattato come caso previsto: si annulla (con `ESCI`) e si va avanti. Un
rifiuto non è un guasto, e fermare tutto per uno solo costa l'intera coda.

Eseguite sui gruppi termici tutte le rinomine passabili. La riconciliazione contro lo
snapshot dice N righe prima e dopo, nessuna sparita, **zero** codici prodotto e
**zero** dati tecnici cambiati.

## I nomi dei modelli: cosa c'è finito dentro, su tutte le marche

I nomi portano i residui di vecchie importazioni. Misurato sull'export completo di una sandbox
(gruppi termici e gruppi frigo):

| Difetto | GT | GF |
|---|---|---|
| `CONDIZIONATORI …` / `(Ass.)` | frequente | frequente |
| nome lungo **esattamente 50** (il campo è troncato lì) | frequente | frequente |
| parentesi quadra aperta e mai chiusa | frequente | frequente |
| doppi spazi | frequente | frequente |
| prefisso della marca ripetuto nel nome | frequente | frequente |
| codice prodotto ripetuto fra `[ ]` | frequente | frequente |
| inizia con `(*)` | frequente | frequente |
| inizia con punto o spazio | frequente | frequente |

**La cosa che salva il recupero**: il campo Descrizione è lungo **50 caratteri**, e
quando prefisso e codice duplicato hanno mangiato spazio il nome è arrivato tagliato —
ma a essere tagliata è **la parte duplicata in coda**, non il nome. Togliendo la
parentesi quadra il nome vero ricompare:

```
'. PARADIGMA MODULA III 16-115 [PARADIGMA MODULA II'  ->  'PARADIGMA MODULA III 16-115'
```

L'ordine delle regole di pulizia conta — **prima la
coda**, altrimenti i troncati restano tali. Risultato: quasi tutti i nomi GT e GF
corretti**, e restano pochissimi nomi davvero più lunghi di 50 caratteri
(descrizioni intere finite nel campo, non recuperabili dal file).

⚠️ **Il codice prodotto non è stato toccato**, ed è il difetto successivo: su una gran parte dei
modelli con un codice, **circa la metà hanno lì dentro un pezzo del nome** invece di un codice
(`. <NOME> GENERICO` → codice `<NOME> GENERIC`, tagliato a 16 caratteri). Distinguere
un codice vero da un frammento non è automatizzabile in sicurezza: va deciso a mano.

### Pulire i nomi fa emergere i doppioni

Due righe che differivano solo per il prefisso diventano lo stesso nome, e la maschera
rifiuta la rinomina. Ma **non tutte le omonimie sono doppioni**, e la distinzione decide
se l'operazione è lecita:

| Caso | Frequenza | Cosa si fa |
|---|---|---|
| omonimo della **stessa marca** | molti | doppione vero: si accorpa |
| omonimo di **marca diversa** | pochi | apparecchi diversi: **non si tocca** |
| collide con un'altra rinomina in coda | pochi | si decide a mano quale nome tenere |

Il piano elenca, per ogni gruppo, la
destinazione scelta: **quella con più campi pieni**, e a parità quella con più
apparecchi installati — perché l'accorpamento tiene i dati della destinazione e butta
quelli della sorgente.

```
'DOMINA F24E'  <-  'FERROLI (Ass.) FERROLI DOMINA F24E'
'EOLO ECO'     <-  'EOLO ECO [3.011998*]'
```

⚠️ **Il codice che si butta può dire che sono due apparecchi diversi.** Su
`HERCULES CONDENSING 27 ABT` le due righe erano `[3.014357GPL]` e senza: **metano e GPL**,
stessa serie ma due macchine. Il nome non lo dice, il codice sì. Prima di accorpare si
cerca nel testo buttato `GPL / METANO / G20 / G30 / G31 / MONOFASE / TRIFASE`: su un centinaio di
gruppi ne è saltato fuori **uno**, ed è bastato a evitare una fusione sbagliata
irreversibile.

## Clivet — dove il problema è la spaziatura, non la marca

Clivet è la marca più grossa di una sandbox: gran parte dei modelli gruppo frigo e degli
apparecchi installati. La marca è **una sola** (id N), quindi qui non si accorpa niente
a livello di marca: il difetto è tutto nei nomi dei modelli.

**Lo stesso apparecchio è scritto in due modi diversi**, quasi sempre per uno spazio o
un trattino: `MU2-Y 53 M` / `MU2-Y 53M`, `MC2-Y 160 T` / `MC2-Y160T`,
`CSRN XHE2 70.4` / `CSRN-XHE 2 70.4`. Il parco si spezza in due senza che nessuno se ne
accorga: gli apparecchi `MU2-Y 53` erano divisi fra le due righe.

⚠️ **Ma i doppioni non hanno gli stessi dati, e non basta il nome per fonderli.**
Su `WSAN-YMI 81` una riga diceva R-32 e l'altra **R-410A**; su `MDAN-YMI5.1` l'EER era
2,91 contro 4,87. Fluido e prestazioni diversi possono voler dire **generazioni diverse
dello stesso nome commerciale** — e il fluido finisce negli adempimenti F-Gas.

Il confronto va fatto sui dati, non sul nome: dove divergono oltre il ~10% si guarda la
scheda ufficiale prima di decidere. Nel caso WSAN-YMI 81 la scheda ha dato ragione alla
riga R-32 (ELFOEnergy Edge EVO, 16 kW): l'altra aveva semplicemente il fluido sbagliato.

Il conto si fa per nome normalizzato: ci sono gruppi doppi, parte
coerenti e parte con dati in conflitto.

### Il conteggio dei doppioni è sempre una sottostima

Normalizzando solo togliendo spazi e trattini se ne trovano meno. Togliendo anche i
**prefissi descrittivi** e i codici fra parentesi quadre — `CONDIZIONATORI CLIVET (Ass.)
MM1-Y 53 M [MM1-Y 53`, `CAAT 242 [AB0432]` — i gruppi aumentano molto.
Molti modelli Clivet hanno un nome così.

Me ne sono accorto per caso: la guardia sugli Id attesi ha rifiutato di selezionare
perché il filtro restituiva **tre** righe invece di due. Senza quella guardia avrei
accorpato due righe credendo di aver chiuso il gruppo, lasciandone una terza in giro.

Quei nomi vanno trattati a parte e con più prudenza: la normalizzazione aggressiva
avvicina anche modelli che potrebbero essere diversi davvero.

### La regola per decidere se due righe sono lo stesso prodotto

**Il nome commerciale è dirimente, i dati no.** Un costruttore non vende due macchine
diverse con lo stesso nome: se `WSAN-YMI 81` compare due volte con fluidi diversi, una
delle due è sbagliata — non sono due generazioni. Si accorpa, e il dato giusto si prende
dalla scheda.

**Ma il codice articolo sì.** `WSAT 182 [AB1P28]` e `WSAT 182 [AC1P28]` hanno due codici
Clivet diversi: possono essere alimentazioni o allestimenti diversi dello stesso
modello. Quelli **non si toccano** senza conferma.

E se a differire è il **nome stesso** — `WRAT 2.80` contro `WRAT 280` — il dubbio è
legittimo: senza dati tecnici non si può escludere che siano due taglie. Lasciato stare.

**Quando i dati divergono, decide il catalogo del costruttore, non il buon senso.**
Su `WSHH-LEE1 60.2` una riga diceva 224 kW e l'altra 54,7. Sembrava che la più piccola
fosse quella giusta, visto il «60» nel nome. Invece la serie WSHH-LEE1 parte da 73 kW:
**54,7 è fuori serie**, quindi è quella sbagliata. Il nome non dice la taglia.

### Il risultato, e cosa resta

Esempio su una sandbox: i modelli gruppo frigo sono calati accorpando
doppioni di sola spaziatura, doppioni con dati in conflitto e nomi sporchi.

Restano alcuni gruppi, che però coinvolgono **pochissimi
apparecchi installati**: è pulizia d'archivio, si fa con calma.

## Il caso NO-<MARCA>, da non risolvere da soli

In una sandbox esiste la marca `NO-<MARCA>` (id N) accanto a `Immergas S.p.A.` (id N).
Contiene **diversi modelli, in gran parte copie di modelli Immergas** — stesso nome, spesso
**lo stesso codice prodotto** (`VICTRIX ZEUS 32` è `3.028382` sotto entrambe le marche).
Le copie hanno dati peggiori: codice vuoto, potenza a zero, rendimenti calcolati male.

**Ma non è una marca vuota: molti gruppi termici installati la usano**, concentrati in alcuni anni.
Accorparla sposterebbe quegli apparecchi.

L'ipotesi «sono quelli fuori garanzia» **è stata verificata ed è falsa**: anche gli
installati marca Immergas hanno garanzia «nessuna» (quasi tutti). Quindi la garanzia non
distingue le due marche, e cosa distingua resta da capire.

Stessa forma per `HOVAL` (id N) vs `HOVAL SRL` (id N) e `Wolf Italia S.r.l.` (id N)
vs `WOLF` (id N): gli Id alti dicono che le seconde sono nate dopo, probabilmente
perché chi inseriva non ha cercato la marca già presente.

**Deciso dal titolare**: sono doppioni da errore di inserimento, e vanno
accorpati. Il caso WOLF è stato fatto (sopra). Per NO-<MARCA> la strada è la stessa, ma
il volume è un altro: **molti modelli collidono** con un omonimo Immergas, e sotto ci
sono molti installati; gli altri passano con il solo accorpamento della marca.
Sono accorpamenti uno per volta, ciascuno con la sua finestra di conferma.

⚠️ **Un accorpamento di modelli non è una fusione dei dati**: sopravvive la scheda della
destinazione. Siccome la copia NO-<MARCA> ha quasi sempre dati peggiori (codice vuoto,
potenza a zero) e l'originale Immergas quelli buoni, **la destinazione dev'essere sempre
la riga Immergas**. Ma la tendina non distingue le due voci omonime: si verifica dopo
quale Id è rimasto, e se è sopravvissuta quella sbagliata si rimettono i dati a mano
dalle schede tecniche.

## I dati tecnici si salvano, non si ricercano due volte

Quello che si trova sulle schede ufficiali va salvato in un file, con la
fonte accanto a ogni modello. I dati di targa non cambiano fra sandbox e produzione: quel file è la
provvista per rifare lo stesso lavoro su produzione senza ricominciare da capo.

I PDF delle fonti vanno conservati. Il più utile trovato finora è
**«Dati tecnici caldaie a condensazione per pratica ENEA»** di Immergas: decine di modelli con
potenza e rendimento in tre pagine.

Quando la scheda non pubblica la portata al focolare si ricava:
`portata = potenza / (rendimento / 100)`. Verificato su due modelli contro il valore
pubblicato: TERA 28 V2 → 28,0/0,978 = 28,63 contro 28,6 dichiarati; TERA 24 V2 →
24,0/0,978 = 24,54 contro 24,5. Si segna `portataDerivata: true` per non spacciare un
calcolo per un dato di targa.

## Il webservice REST non è una scorciatoia

Passare dall'API per scrivere in blocco **non si può**: il webservice è **in sola
lettura** ed è abilitato **solo su Azienda 1**.
Le tabelle si correggono dall'interfaccia, un record per volta.
