# Interazione — come si opera davvero, non com'è fatto

`mappa-web.md` dice **dove** stanno le cose. Questo file dice **come** si toccano senza
sbagliare. Tutto verificato operando su una sandbox (Azienda 3).

## La regola che viene prima di tutte: guarda chi c'è sotto il punto

Prima di un click che conta, controlla che l'elemento che vuoi sia davvero quello in
cima in quel punto:

```js
const r = elemento.getBoundingClientRect();
const x = Math.round(r.left + r.width / 2), y = Math.round(r.top + r.height / 2);
document.elementFromPoint(x, y) === elemento   // deve essere true
```

Non è pedanteria. `getBoundingClientRect()` risponde **anche per un elemento coperto**:
il campo `Nominativo` risultava a (587, 474) e cliccabile, ma in quel punto c'era una
riga di griglia. Il click è finito sulla griglia, il filtro non è stato scritto, e la
ricerca successiva ha restituito il risultato vecchio — che sembrava una scoperta sul
comportamento dei filtri e invece era il mio errore.

## Il pannello dei risultati copre il form

Dopo `CERCA`, il pannello dei risultati sale e **copre i campi del filtro**, che restano
nel layout ma sotto. Il pulsante `CERCA` stesso si sposta: da y≈677 a y≈274.

Per rimettere mano ai filtri si chiude il pannello con la maniglia
**`div.expand-collapse`** (150×54, sopra la griglia, al centro). Poi i campi tornano
raggiungibili — e si verifica con la regola qui sopra.

⚠️ **`CERCA` lo riapre ogni volta.** L'11/09/2026 ci sono cascato due volte di fila
nella stessa sessione: chiuso il pannello, modificato il filtro, premuto CERCA, e al
giro dopo il triple-click sul campo è finito su una riga di griglia aprendo la scheda
di un impianto a caso. Chiudere il pannello una volta non basta: va richiuso **dopo
ogni ricerca**.

**La via che non ha questo problema: non toccare lo schermo.** Scrivere il campo e
premere CERCA da JavaScript funziona e non dipende da cosa copre cosa:

```js
const inp = Array.from(document.querySelectorAll('input')).find(i => i.value === 'Immergas');
const set = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
set.call(inp, '');                                     // o il nuovo valore
inp.dispatchEvent(new Event('input',  {bubbles: true}));
inp.dispatchEvent(new Event('change', {bubbles: true}));
inp.dispatchEvent(new Event('blur',   {bubbles: true}));
Array.from(document.querySelectorAll('button, .btn, [class*=button]'))
  .filter(e => e.offsetParent !== null && /^CERCA$/i.test(e.innerText.trim()))[0].click();
```

Poi si rilegge il contatore: se il numero non cambia, il filtro non è stato scritto.

## `javascript_tool` non aspetta le promise

Uno snippet `async` — `(async () => { ... })()` — torna **`{}`**, sempre, qualunque cosa
faccia dentro. Non è un blocco del filtro di sicurezza: è il tool che restituisce la
promise invece del suo valore.

Conseguenza: **gli snippet `async` scritti nei file di questa skill non funzionano più
così come sono** — `apriTabella()` in `tabelle-rotte.md` è uno di quelli. Vanno spezzati
in due chiamate: una che naviga, una che legge. La seconda chiamata arriva abbastanza
tardi da trovare la pagina pronta, ma **questo non va dato per scontato**: si verifica
sempre cosa c'è a schermo prima di usarlo.

Vale anche per il ritorno: un oggetto grosso o con strutture annidate può tornare `{}`
o `[BLOCKED: ...]`. Conviene restituire **una stringa costruita a mano**, o
`JSON.stringify` di un oggetto piatto.

## Portare fuori una tabella grossa: il download, non il ritorno

L'output del tool viene **troncato** intorno al paio di migliaia di caratteri, e una
tabella di 800 righe non ci passa. La strada che funziona è far scaricare un file al
browser, e poi leggerlo da disco:

```js
const blob = new Blob([JSON.stringify(righe)], {type: 'application/json'});
const a = document.createElement('a');
a.href = URL.createObjectURL(blob);
a.download = 'estrazione.json';
document.body.appendChild(a); a.click(); a.remove();
'scaricate ' + righe.length + ' righe, byte=' + blob.size;
```

Il file arriva in `~/Downloads` senza nessun dialogo. Centinaia di righe (centinaia di KB) portate fuori
in una chiamata sola. **Non** usa `alert`/`confirm`, che bloccherebbero
l'estensione.

## Scrivere in un campo

1. Chiudi il pannello dei risultati se è aperto.
2. Clicca il campo e **verifica `document.activeElement`**: se è `body`, il click non ha
   preso fuoco e tutto ciò che digiti va perso senza errori.
3. Per sostituire il contenuto usa **`cmd+a` poi digita**. I `Backspace` ripetuti alla
   cieca non bastano: se il campo non ha il fuoco non cancellano niente e sembra
   comunque tutto a posto.
4. **Rileggi il valore del campo prima di cercare.** Un filtro che sembra non cambiare
   il risultato quasi sempre non è stato applicato.
5. **Decimali con la virgola.** Il campo Kg del circuito di un gruppo frigo scarta il
   punto: «3.5» diventa 35, senza errori. I prezzi con la virgola arrivano giusti
   («10,50» → 10,5000) [misurato 14/10/2026, A2]. Il punto non è mai sicuro, nemmeno da
   script: su un campo importo **già formattato** («7,5000») viene letto come separatore
   delle migliaia, e «12.34» diventa 1.234,00 [misurato 14/10/2026, produzione, riga di carico
   DDT corretta prima di salvare]. Sempre la virgola, e dopo un decimale si rilegge il campo.
6. **La ricerca globale in alto a destra va digitata.** Impostare il valore via JS (anche
   con l'evento `input`) non rilancia la ricerca: click nel campo e `type` (13/10/2026).
   Copre impianti, anagrafiche (anche per codice fiscale) e articoli: prima di creare un
   impianto si cerca lì per cognome, via e CF, con un controllo positivo su un nome che
   esiste (A1, 14/10/2026).

## Convenzione dei filtri testuali — vale anche nel web

Misurato su `Nominativo`, ricerca Impianto, su una sandbox:

| filtro | risultati | contiene un cognome più lungo? |
|---|---|---|
| `%VERDI` | più risultati | sì (anche `GIUVERDI`) |
| `VERDI` | meno risultati | no (`GIUVERDI` escluso) |

`%` davanti = **contiene**; senza `%` = **inizia con**. È la regola che il wiki dà per
Unicò NET, e regge anche qui. Si concatena: `%valvola%sfera%`.

## Le griglie delle ricerche non si ordinano dalle intestazioni

Cliccare l'intestazione di colonna **non fa niente**, e non è un click sbagliato: ho
verificato che colpisce `.ag-header-cell-text` e che ogni colonna ha `sortable: false`,
`filter: false`, con `suppressContextMenu: true` sulla griglia. Niente ordinamento da
header, niente filtri di colonna, niente menu col tasto destro.

L'ordinamento si imposta da **⋮ → Personalizza ordinamento**: dialogo con casella di
ricerca, elenco campi a sinistra, campi scelti a destra, `ANNULLA` / `MODIFICA`.
**Non ancora provato ad applicarlo**: `personalizza_ricerca` cade nel ramo del guardrail
che chiede conferma, e non è ancora chiaro se `MODIFICA` valga solo per la vista
corrente o salvi la personalizzazione dell'utente.

## Ricerche e tabelle sono due griglie diverse

| | Ricerca | Tabella |
|---|---|---|
| colonne ordinabili | **no** | **sì** |
| filtri di colonna | **no** | **sì** |
| selezione righe | `multiple` | `single` |
| conteggio dichiarato | «Sono stati trovati N risultati» | **non c'è** |
| contenitore | `div.search-results` | fuori da `.search-results` |

Conseguenza operativa: **la prova di completezza di `flussi/estrazione.md` non si applica
alle tabelle**, perché manca il secondo termine di paragone. Verificato che in quel caso
la procedura **si ferma da sola** («riquadri di risultati visibili: 0») invece di
riportare un numero non verificato. Su una tabella, se serve un totale, va detto che
proviene da una sola fonte.

## Anche le tendine sono paginate

Stesso difetto della griglia, altro vestito. Il campo `Tipologia attività ufficio`
rende **17 elementi** (16 opzioni + «Aggiungi elemento») su **oltre cento valori esistenti**.
Digitando un filtro (es. `GESTIONE`) compaiono voci che nella prima pagina non c'erano.

Quindi `[...document.querySelectorAll('[role="option"]')]` restituisce **una pagina,
non l'elenco** — e sembra completo, perché una tendina corta è normale.

**Per sapere quali valori esistono si legge la tabella corrispondente, non la
tendina.** La tendina serve a scegliere: se serve trovarci qualcosa, si digita un
filtro e si legge il filtrato. Vale per ogni campo tabellato dell'applicazione.

## Un filtro fermo su «Caricamento...» vuole un tasto in più

Nei campi con filtro il testo scritto tutto d'un fiato lascia la lista su
«Caricamento...», e non arriva niente. Si cancella l'ultima lettera e la si riscrive: il
filtro parte e la lista compare in un paio di secondi. Misurato su `Scegli anagrafica`
del wizard impianto, sulla tipologia della voce di piano e sul modello del «Nuovo
installato» [A2, 15/10/2026]. Una lista che resta su «Caricamento...» non dice che il
valore manca: «Nessun risultato» lo dice.

## Una rotta sbagliata non dà errore: ti lascia dov'eri

Navigando a `#/tabelle/TipoIntervento/table`, che **non esiste**, l'applicazione
resta sulla tabella precedente senza dire niente. Se poi si legge la griglia, si
attribuiscono i dati di una tabella a un'altra — e i dati sono buoni, quindi niente
insospettisce.

**Dopo ogni navigazione si rilegge `div.main-tab.selected`** e si controlla che sia
quello che ci si aspetta. È lo stesso principio del riquadro visibile: non fidarsi
della richiesta, guardare il risultato.

## La griglia può contenere una riga finta mentre carica

Su una tabella appena aperta si legge una riga sola con testo
**«Caricamento dati (modifiche) non ancora completato»**. È un segnaposto: chi conta
subito conta quella. Prima di leggere una griglia si aspetta, e un conteggio di 1 su
una tabella che dovrebbe averne molte è il sintomo.

## Un dialogo non chiuso sopravvive ai cambi di rotta

`ANNULLA` su un form compilato apre la conferma *«I dati inseriti e non salvati
andranno persi»*. Se non si risponde, **il form resta aperto anche navigando altrove**:
ho fatto un'intera spazzata di tabelle con un form RDI ancora vivo dietro, e me ne sono
accorto solo quando la conferma è ricomparsa. Le navigazioni funzionavano lo stesso,
ma lo stato dell'applicazione non era quello che credevo.

Prima di dire «ho chiuso», si controlla che il testo del dialogo non sia più in pagina.

## Le rotte comandano tabelle e record, non le ricerche

Verificato: `#/tabelle/<Entita>/table` e
`#/assistenza/impianto/<id>/attivita/` **funzionano** scritte nella barra degli
indirizzi. Anche il dettaglio di un intervento: un click (o tasto destro) sulla riga
in ATTIVITÀ porta a `#/assistenza/impianto/<id>/attivita/Intervento/<idIntervento>` e
apre il **pannello laterale** con data/durata, descrizione, operazioni di manutenzione
con l'esito scritto dal tecnico, allegati, rapportino con righe e totale, cronologia
del ticket. Su A1 il 21/09/2026 (impianto N, intervento N) il pannello ha dato
tutto senza aprire la scheda intervento in una tab nuova. L'id intervento sta in
`node.data.payload.Id` della griglia attività (`TipologiaAttivita === 'Intervento'`). `#/assistenza/home/search/<Entita>/semplice` **no**. Quindi la navigazione
per link è utilizzabile, ma solo dove è stata provata — e va provata leggendo
`div.main-tab.selected` dopo.

## `javascript_tool` non regge cicli lunghi

Un ciclo con `await` di ~10 secondi (30 click con pause) ha fatto cadere l'estensione
(*«Browser extension is not connected»*). Si riconnette da sola, ma il lavoro si
perde. **Blocchi da pochi secondi**, mai loop lunghi dentro una sola valutazione.

## Le voci di una tendina lunga hanno coordinate fuori dallo schermo

`getBoundingClientRect()` di un'opzione dentro una lista scorrevole restituisce la sua
posizione **nel layout della lista**, non a schermo. Su una tendina lunga ho letto
`y: 880` e cliccato lì: la finestra è alta 707 px, quindi il click è andato nel vuoto e
il campo è rimasto vuoto.

Alla sonda va aggiunto il controllo, sempre:

```js
const r = opzione.getBoundingClientRect();
const inVista = r.top >= 0 && r.bottom <= window.innerHeight;
```

Se l'opzione non è in vista **non si clicca alle sue coordinate**: si **digita un
filtro** nel campo, che la porta in cima. È la stessa mossa che serve per superare la
paginazione della tendina, e risolve i due problemi insieme.

## Con la scheda in secondo piano i dialoghi restano a metà (misurato 14/10/2026, A2)

Quando la scheda Chrome pilotata non è quella in primo piano, Chrome rallenta i timer e
le animazioni CSS dei dialoghi Aurelia non finiscono. Il dialogo appena aperto resta
**invisibile** (`ux-dialog-container` a opacità 0) e, dopo CONFERMA, un container del
dialogo chiuso resta **sopra la pagina e assorbe i click**: la ricerca della griglia non
riceve testo, `document.activeElement` è `BODY`. Rimedio: mandare l'evento che
l'animazione non ha mandato, su container, overlay e corpo del dialogo:

```js
for (const s of ['ux-dialog-container', 'ux-dialog-overlay', 'ux-dialog-body'])
  document.querySelectorAll(s).forEach(e => e.dispatchEvent(new Event('transitionend', {bubbles: true})))
// after ~500 ms: document.querySelectorAll('ux-dialog-container').length is what is still there
```

Si chiama dopo ogni apertura e dopo ogni CONFERMA; dopo una CONFERMA si ripete finché
il conteggio dei container non è 0, perché un dialogo ancora aperto conta 1 anche lui.
Due click ravvicinati possono aprire **due dialoghi impilati**, invisibili finché non si
manda l'evento: chiuderne uno con ANNULLA prima di scrivere. Con i timer rallentati
niente attese lunghe dentro `javascript_tool` (la chiamata va in timeout a 45 s): si
aspetta con `computer wait` e poi si legge.

**I menu a tendina dei form** (Tipologia op. man., Tipo operazione FGAS) non si aprono
se il click arriva nella stessa raffica di click e digitazioni: si aprono al click
successivo, dopo una chiamata JS. Metodo che regge: compilare testi e caselle, poi in una
chiamata separata click sul menu, controllo che `[role="option"]` sia visibile, scelta.

## I form obbligatori si difendono, e conviene guardarli

Mancato il click sulla tipologia, il passaggio al passo successivo **non è avvenuto**:
il campo si è colorato di rosso con **«Valore obbligatorio»** sotto. È un
comportamento utile — il wizard non prosegue con un campo obbligatorio vuoto — ma va
letto: senza screenshot o senza rileggere il campo, sembra solo che «il pulsante non
abbia funzionato».

Dopo un `AVANTI` o un `CONFERMA` che sembra non fare nulla, la prima cosa da cercare è
un messaggio di validazione, non un problema di click.

## Navigare per rotta può aprire una seconda scheda interna

Navigando a `#/assistenza/impianto/<id>/attivita/` mentre quella scheda era già
aperta, Unicò ne ha aperta **una seconda uguale**. Non rompe nulla, ma le schede
interne si accumulano e le coordinate della barra si spostano. Conviene chiudere le
schede che non servono, o rileggere le posizioni invece di riusarle.

## AG Grid: l'ordine del DOM non è l'ordine a schermo

Le righe vengono riciclate: la prima `.ag-row` del DOM su una ricerca per cognome era la
**riga 14**. Per l'ordine vero si usa `forEachNodeAfterFilterAndSort`, mai la posizione
nel DOM.

## La selezione si sporca da sola, e non è innocua

Due click andati a vuoto sui filtri hanno **selezionato due impianti** nella griglia
sottostante, con tanto di spunta. Nessuna scrittura, ma le **operazioni massive leggono
la selezione**, e con filtri attivi sono zona rossa.

Regola: prima di aprire il menu ⋮ di una griglia, controlla e azzera la selezione.

```js
const api = /* griglia del riquadro visibile */;
api.getSelectedNodes().length;   // deve essere 0
api.deselectAll();
```

## Aprire un record

**Doppio click sulla riga.** Porta a
`#/assistenza/impianto/<idImpianto>/dettagli/<tipo>/<idInstallato>/<sezione>`.

La scheda impianto ha: intestazione con codice, nominativo e **Tag**; colonna
`DETTAGLI · ATTIVITÀ · RIFERIMENTI · CONTRATTI · ALTRI DATI · NOTE · SMS · FILE (n) ·
VINCOLI`; al centro l'albero dell'installato (GT1, GT2, SR1…) con le operazioni di
manutenzione e le loro scadenze — **quelle scadute sono in rosso**; a destra
`INFORMAZIONI` e `COLLAUDO` con la matita per modificare, e i tab
`Altri dati · Piano di manutenzione · Interventi · Storico installato`.

Le spie del wiki ci sono davvero: `NOTE` col pallino verde quando ci sono note
principali, `FILE` col numero di allegati.

## Tabelle

L'albero si filtra dalla casella **Cerca** in cima, che è molto più veloce dello scroll:
con l'albero tutto espanso il nodo `Zone` stava a y≈2455.

La rotta usa il **nome dell'entità, non l'etichetta**: `Zone` apre
`#/tabelle/Zona/table`.

Colonne notevoli, che sono la traduzione in dati delle regole di dominio:
`IsEsclusoDaListe` (il check «Escluso da liste»), `Id` con intestazione
**«Riga Bloccata»** (le voci di sistema col lucchetto), `AreaAnalytics`.

## Il menu ⋮ della griglia, provato

`Stampa · Esporta · Personalizza campi · Personalizza ordinamento · Cattura · Mostra
totali`.

### Mostra totali — non sporca i conteggi

Aggiunge una riga `TOTALI` in fondo. È una **riga fissata**
(`getPinnedBottomRowCount() === 1`) e **non entra** in `forEachNode`, in
`forEachNodeAfterFilter` né in `getDisplayedRowCount()`: con i totali accesi la prova
di completezza continua a dare 14 = 14 = 14. **Non finisce nemmeno nell'esportazione.**

Sulla ricerca Impianto risulta vuota, perché non ci sono colonne numeriche da sommare.

### Esporta — nel web non passa dal client FTP

Dialogo con: casella **`Solo righe selezionate`**, `Tipologia` = **Excel (.xlsx)** o
**PDF (.pdf)**, `Azione` = **Scarica nel pc** o **Salva in cloud**.

Niente client FTP e niente `Esplora Risorse`: quella è la meccanica di Unicò NET
descritta nel wiki, e **nel web non vale**.

Il file arriva in `~/Downloads` col nome `Export_(<Entità>)_<AAAAMMGGhhmm>.xlsx`.
Verificato aprendolo: N righe di dati più l'intestazione, cioè **l'esportazione è
completa** e coincide con la griglia. Le colonne sono quelle visibili **meno il
progressivo `N°`**.

Attenzione a `Solo righe selezionate`: una selezione sporcata da un click andato a
vuoto cambia in silenzio cosa esce dal file. Azzerare la selezione prima.

[Provato su un'estrazione piccola. Su un'estrazione grande resta da vedere se scatta un limite di
esportazione.]

### Personalizza ordinamento — rifà la query, non ordina la griglia

Dialogo con casella **Cerca** (e i campi delle entità collegate: *Destinatario
corrispondenza*, *Responsabile impianto*, *Ultimo intervento*). Si spunta un campo, che
compare a destra come `↑ Nome ✕` — freccia per il verso, ✕ per toglierlo — poi
`MODIFICA`.

Applicandolo l'ordine cambia davvero, **ma `columnApi` non riporta alcun `sort`
attivo**: Unicò rifà la query lato server con un `ORDER BY` e restituisce le righe già
ordinate. Ecco perché `sortable: false` sulle colonne non impedisce nulla.

**La scelta persiste**: riaprendo il dialogo il campo è ancora lì. Si toglie con la ✕
più `MODIFICA`, e l'ordine originale torna. Il conteggio non cambia mai (14 prima, 14
dopo, 14 dopo la rimozione).

## Scrivere in una tabella — provato su una sandbox

Percorso: `Tabelle` → tabella → **`+` in alto a destra** (il pulsante rotondo).

Il form di creazione (`Nuova zona`) e quello di modifica (`Modifica zona`) sono **lo
stesso form**, cambia solo il pulsante: `CONFERMA` contro `MODIFICA`. La casella
**`Escluso da liste` c'è già in creazione**, quindi una voce può nascere già ritirata.

Dopo il salvataggio Unicò **apre il dettaglio del nuovo record**:
`#/tabelle/Zona/detail/<id>`. Sotto la griglia compare il pannello di dettaglio, con a
destra tre icone: **matita** (modifica), un'icona di accensione, **cestino**.

**Le icone non hanno né `title` né `aria-label`.** Non c'è modo di sapere cosa fanno
senza provarle: quella di accensione è probabilmente il ritiro rapido dalle liste, ma
non è stato verificato e non si tira a indovinare su un interruttore anonimo. Per
escludere una voce si usa la matita e la casella nel form.

### La trappola dei conteggi: le voci escluse

Contate sulla tabella `Zone` di una sandbox:

| momento | righe |
|---|---|
| all'inizio | **N** |
| dopo aver creato `ZZTEST` | **N+1** |
| dopo aver marcato `ZZTEST` escluso | **N+1+k** |

Non è un errore: **N erano le zone con le escluse nascoste.** Marcandone una, la
griglia si ricarica mostrando anche le escluse — che erano già k (per esempio `ZONA4`,
`ZONA5`). N + k + 1 = il totale, esatto.

Quindi *«quante zone abbiamo?»* ha **due risposte giuste diverse**, e quale sia quella
buona dipende dallo stato dell'icona occhio-sbarrato in alto a destra. Rispondendo su
una tabella va sempre detto se le voci escluse sono dentro o fuori.

## Cosa resta sulla sandbox dopo queste prove

Una voce nella tabella **Zone**: sigla `ZZTEST`, descrizione
*«ZZ TEST AUTOMAZIONE 03/09/2026 - NON USARE»*, id N, **esclusa dalle liste** —
quindi non compare nei menu a tendina. È l'unica scrittura fatta, ed è su una sandbox.
Va tolta quando non serve più.

Nient'altro è stato modificato: l'ordinamento personalizzato è stato rimosso, la
selezione azzerata, i dialoghi rischiosi annullati.

## Cose ancora da provare

- `Personalizza campi` — è il `Personalizza` di cui il wiki dice che un uso errato
  «può portare a risultati imprevedibili e/o blocchi del sistema». Ramo
  `personalizza_ricerca`: serve l'ok esplicito.
- `Cattura` e `Stampa` dal menu ⋮.
- L'icona di accensione sul dettaglio di una voce di tabella, e l'occhio sbarrato che
  mostra/nasconde le escluse.
- Se l'esportazione ha un limite di righe.
- La scheda `Avanzata` della ricerca.
- Aprire un impegno in Agenda e vedere cosa mostra senza spostarlo.
- Entrare in una cartella di Files.
- Scritture su entità vere (impianti, interventi, documenti): **nessuna provata**, e
  nessuna va provata senza chiedere.

---

## Leggere un elenco completo dal view-model, invece che dalla tendina

Questa risolve la trappola più costosa di tutte: **le tendine rendono una pagina, non
l'elenco**, e contarne le `[role="option"]` dà un numero che *sembra* completo.

Aurelia lascia il view-model attaccato agli elementi, in `elemento.au`. L'elenco vero di
un `x-select` sta in **`elemento.au[chiave].viewModel.initialItems`**:

```js
const nodi = Array.from(document.querySelectorAll('*')).filter(e => e.au);
const trovati = [];
for (const n of nodi) for (const k of Object.keys(n.au)) {
  const vm = n.au[k] && n.au[k].viewModel;
  if (!vm) continue;
  for (const p of Object.keys(vm)) {
    const v = vm[p];
    if (Array.isArray(v) && v.length > 2 && v[0] && typeof v[0] === 'object'
        && 'Id' in v[0] && 'Descrizione' in v[0])
      trovati.push({ el: k, prop: p, n: v.length, voci: v.map(x => x.Id) });
  }
}
```

Due avvertenze imparate sul campo:

- **Mai `JSON.stringify` su un view-model**: le strutture Aurelia sono circolari e
  l'esecuzione muore con *«Converting circular structure to JSON»*. Si estraggono i campi
  per nome.
- Alcuni valori tornano come `[BLOCKED: Base64 encoded data]`: è il filtro sul contenuto,
  non un errore. Si chiedono i campi singoli, o si incrocia con la guida.

**Il campo `Id` di queste liste è il nome che serve nelle rotte.** È il modo giusto di
scoprire una rotta invece di indovinarla — e indovinare non funziona: la tabella delle
tipologie intervento sta su **`TipologiaIntervento`**, non su `TipoIntervento`.

---

## Tre trappole delle tendine, imparate scrivendo su una sandbox

**1. «Aggiungi elemento» in fondo alla lista è una scrittura in tabella.** Se cercando un
valore l'**unica** voce proposta è quella, il termine digitato è sbagliato: si riformula,
non si crea. Digitando `Riscaldamento semplice` — tipologia che sulla sandbox non esiste — la
tendina offriva solo `Aggiungi elemento`, e un click distratto avrebbe creato una
tipologia impianto nuova. Vale identico per marche, comuni, tipologie operazione.

**2. Il filtro dei campi non gradisce più parole.** `gruppo term` → «Nessun risultato»;
`termic` → due campi. **Una parola sola.**

**3. Le voci quasi omonime non sono la stessa cosa.** Misurati sul campo:
- `Gruppi termici` ≠ **`Gruppi termici attivi`** (il primo conta anche i dismessi)
- due marche quasi omonime, di cui una creata come marcatore di esclusione (significato opposto)
- due comuni con lo stesso nome ma CAP e province diversi
- lo stesso apparecchio come **`Gruppo Termico`** e come **`Componente`**

Si legge l'etichetta per intero — CAP, provincia, categoria — non la prima riga che
somiglia.

## Un campo booleano nasce a «Vero»

Nella ricerca avanzata, scelto un campo booleano compaiono due bottoni `Vero`/`Falso` con
**`Vero` già acceso**. Prendere `Dismesso` e non toccare nulla significa cercare **gli
impianti dismessi**. Guardare sempre quale dei due è evidenziato.

## Il contatore dei risultati mente in due modi

**Troppo presto**: leggere subito dopo `CERCA` restituisce «Sono stati trovati 0
risultati» — indistinguibile da uno zero vero. **Mai attese a tempo fisso**: si aspetta
la condizione *dichiarato == righe nel modello* (codice in `flussi/ricerca-avanzata.md`).

**Troppo tardi**: il contatore mostra **l'ultima ricerca eseguita**, non i criteri
compilati adesso. Cambiando un operatore continuava a dire il numero vecchio finché non ho ripremuto
`CERCA`. **Nessun numero si riporta senza aver premuto `CERCA` dopo l'ultima modifica.**

## Chiamare il backend dalla pagina: serve `X-Requested-With`

Una `fetch` scritta a mano dalla console della pagina, con i soli cookie, torna **401**.
Una `POST` (per esempio `ExecuteSearch`) che copia `authorization`, `content-type` e
`accept` di una richiesta vera della pagina ma non la sua `X-Requested-With` torna
**403**: Unicò vuole quell'intestazione con il valore che manda l'app (non
`XMLHttpRequest`). Con `X-Requested-With` copiata la stessa POST torna 200;
`X-EventSession-Id` non serve; le GET (per esempio `MovimentiMagazzino?NumeroDistintaMovimento=`)
passano anche senza [misurato 15/10/2026, A2, dal Chrome del Mac]. Le intestazioni si
leggono da una richiesta osservata, mai si scrivono a mano, e non si stampano.

## Cliccare una voce di menù riusa la tab corrente

`Assistenza → Azioni` **non apre una tab nuova**: riusa quella attiva, e una ricerca
aperta lì viene persa. Se serve tenerla, si apre prima una tab nuova.

## Barra Cerca globale (misurato 30/09/2026)
`Return` con **un solo risultato apre direttamente l'articolo**, senza menu: prima di cliccare «il primo risultato», screenshot. Un click cieco in alto a destra della testata colpisce la matita e apre `Modifica anagrafica articolo` (uscita: `ANNULLA` → `ESCI`).


> ⚠️ 06/10/2026: passando da `#/magazzino/articolo/<id>/listini` a un altro id via `location.hash`, il titolo di `div.main-tab.selected` resta quello dell'articolo precedente mentre il contenuto cambia. Per l'articolo aperto si legge il codice in testata.
