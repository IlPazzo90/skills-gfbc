# Flusso 1 — Estrazione dati

Rispondere con numeri presi da Unicò. È il flusso che si usa più spesso ed è anche
quello dove è più facile sbagliare **senza accorgersene**, perché una griglia
troncata ha esattamente lo stesso aspetto di una griglia completa.

La regola che tiene tutto: **un numero si riporta solo se la prova di completezza è
passata.** Se non passa, si dice che non passa. Mai riportare "circa".

## Prima di partire

1. Leggi l'azienda dalla URL (`?c=/C<tenant>/An/`). Dichiarala in chat.
2. **Se l'azienda risulta `sconosciuta`, fermati qui.** Non per il rischio — una
   lettura non fa danni su nessuna azienda, e il guardrail infatti la consente
   sempre. Per la risposta: «N impianti» non è un dato finché non si sa se sono
   dell'azienda o di un'altra azienda del gruppo, e le due aziende hanno archivi diversi. Un numero senza
   l'azienda a cui appartiene non è una risposta parziale, è una risposta sbagliata
   che sembra giusta.
3. Se la domanda riguarda dati di clienti (nomi, telefoni, indirizzi, codici
   fiscali), **estrai solo i campi che servono per rispondere**. Non riversare in
   chat migliaia di righe di anagrafiche per contare quante sono.

## Passo 1 — Arrivare alla ricerca

**A click, dal menu.** Assistenza → Ricerca, poi si sceglie l'entità dal campo
`Cosa stai cercando`.

**Non per link.** La rotta cambia quando si naviga
(`#/assistenza/home/search/<Entita>/semplice`), ma **scrivere quella rotta nella
barra degli indirizzi non cambia la ricerca**: verificato il 03/09/2026 — con la URL
su `.../search/Contratto/semplice` lo schermo mostrava ancora `RICERCA Impianto` con
i risultati precedenti. La rotta è una conseguenza della navigazione, non un comando.

È la stessa ragione per cui il passo 3 non si fida della URL: **la URL può mentire su
cosa c'è a schermo.**

## Passo 2 — Impostare i filtri

Nella UI, come farebbe un tecnico. Due cose da ricordare ogni volta:

- Il gruppo Tutti/**Attivi**/Dismessi parte su **Attivi**. Se la domanda è "quanti
  impianti abbiamo", decidi se intende attivi o tutti, e **dillo nella risposta**.
- I filtri testuali seguono la convenzione Unicò: `%` davanti vuol dire "contiene",
  senza `%` vuol dire "inizia con", e si concatena (`%valvola%sfera%`).

Poi `CERCA`.

## Passo 3 — La prova di completezza

Due numeri da due fonti indipendenti, che devono coincidere — **presi dallo stesso
riquadro di risultati**, non dal documento intero.

Il vincolo non è formale. Unicò lascia nel DOM la ricerca precedente: cercare la
prima `.ag-root-wrapper` del documento e il primo «Sono stati trovati…» del
`body.innerText` può accoppiare il contatore di una ricerca con la griglia di
un'altra, e i due numeri potrebbero anche **coincidere per caso**, certificando come
completa un'estrazione che non c'entra niente. Il contenitore che tiene insieme i due
è `div.search-results`.

```js
(() => {
  const riquadri = Array.from(document.querySelectorAll('.search-results'))
    .filter(e => e.offsetParent !== null);
  if (riquadri.length !== 1)
    return { errore: 'riquadri di risultati visibili: ' + riquadri.length };
  const box = riquadri[0];
  const g = box.querySelector('.ag-root-wrapper');
  if (!g) return { errore: 'nessuna griglia nel riquadro visibile' };
  const m = box.innerText.match(/Sono stati trovati\s+([\d.]+)\s+risultati/);
  const scheda = document.querySelector('.main-tab.selected');
  return {
    ricerca: scheda ? scheda.innerText.trim().replace(/\s+/g, ' ') : null,
    dichiarati: m ? Number(m[1].replace(/\./g, '')) : null,
    nellaGriglia: g.__agComponent.gridApi.getDisplayedRowCount(),
    nelDom: box.querySelectorAll('.ag-center-cols-container .ag-row').length
  };
})()
```

- `ricerca` — l'etichetta della scheda interna attiva, es. `RICERCA Impianto`.
  **Va guardata**: dice su quale entità stai davvero rispondendo, e non deriva dalla
  URL. Se non corrisponde a quello che credevi di cercare, fermati.
- `dichiarati` — quello che Unicò scrive accanto al pulsante CERCA. Il separatore
  delle migliaia è il punto, va tolto prima di convertire.
- `nellaGriglia` — quello che la griglia ha davvero in memoria.
- `nelDom` — quante righe sono renderizzate. **Serve solo a ricordare perché questa
  procedura esiste**: su migliaia di risultati nel DOM ne erano 26.

Se `riquadri.length` non è 1, non indovinare quale sia quello giusto: chiudi le
schede interne che non servono e rifai.

**La guardia si ripete in ogni blocco, e non è una svista.** Ogni snippet qui dentro
è un'esecuzione separata: fra il passo 3 e il passo 4 il DOM può cambiare — una
scheda chiusa, una seconda ricerca aperta — e una verifica fatta prima non protegge
un'esecuzione fatta dopo. Un blocco che desse per buono il controllo di quello
precedente andrebbe in eccezione con zero riquadri e sceglierebbe in silenzio il
primo con due, cioè rimetterebbe esattamente il difetto che la guardia toglie. Per lo
stesso motivo ogni blocco è **eseguibile da solo**: nessuno usa variabili definite in
un altro.

**Se `dichiarati !== nellaGriglia`, fermati.** Non estrarre, non stimare. Riporta i
due numeri e dì che non tornano. Le cause plausibili: la ricerca stava ancora
caricando (riprova dopo un'attesa), oppure c'è un filtro di griglia attivo oltre a
quelli della maschera (in quel caso `forEachNode` e `forEachNodeAfterFilter` danno
numeri diversi — confrontali).

Se `dichiarati` è `null` la ricerca non è stata eseguita: non c'è niente da leggere.

## Passo 4 — Estrarre

Solo dopo che la prova è passata. Si chiedono **i campi per nome**, mai l'oggetto
intero:

```js
(() => {
  const riquadri = Array.from(document.querySelectorAll('.search-results'))
    .filter(e => e.offsetParent !== null);
  if (riquadri.length !== 1)
    return { errore: 'riquadri di risultati visibili: ' + riquadri.length };
  const box = riquadri[0];
  const api = box.querySelector('.ag-root-wrapper').__agComponent.gridApi;
  const m = box.innerText.match(/Sono stati trovati\s+([\d.]+)\s+risultati/);
  const dichiarati = m ? Number(m[1].replace(/\./g, '')) : null;

  const campi = ['Codice', 'Nominativo', 'Comune__Descrizione', 'Comune__Provincia'];
  const righe = [], assenti = {};
  let senzaDati = 0;
  api.forEachNodeAfterFilter(n => {
    if (!n.data) { senzaDati++; return; }   // nodo di gruppo, o riga non caricata
    const r = {};
    for (const f of campi) {
      if (f in n.data) r[f] = n.data[f];
      else { r[f] = null; assenti[f] = (assenti[f] || 0) + 1; }
    }
    righe.push(r);
  });

  return {
    dichiarati, estratte: righe.length, senzaDati, assenti,
    completa: dichiarati !== null && righe.length === dichiarati && senzaDati === 0,
    righe
  };
})()
```

**`completa` è la riga che decide.** La prova del passo 3 dice che la griglia
*contiene* tutte le righe; non dice che l'estrazione le abbia *prese tutte*. Fra le
due cose ci sta `if (!n.data) return`, che scarta in silenzio i nodi senza dati: con
N nodi di cui uno senza `data`, il passo 3 dichiara N=N e il passo 4 ne
restituisce N−1. Per questo il conteggio si riafferma **qui**, sulle righe davvero
costruite, e `senzaDati` viene riportato invece che ignorato.

Se `completa` è `false`, vale la stessa regola del passo 3: **niente numeri**.

Perché per nome e non tutto:

- riversare l'oggetto intero fa scattare il filtro di sicurezza del browser su
  alcune chiavi, che tornano `[BLOCKED: Base64 encoded data]` e sembrano un errore
  di Unicò senza esserlo;
- una riga non porta tutte le chiavi delle colonne (33 colonne, 21 chiavi osservate
  sulla ricerca Impianto). La distinzione fra **chiave assente** e **valore vuoto**
  si tiene con `f in n.data`, non con `??`: `a.x ?? null` restituisce `null` sia se
  la chiave manca, sia se vale `null`, sia se vale `undefined`. Il conteggio in
  `assenti` è quindi la sola parte che dice davvero *«questa chiave non è arrivata»*.

  Non è teoria: su tutti gli impianti attivi di una sandbox, `Comune__Provincia` è assente
  su molte righe e `Comune__Descrizione` su altre. Con `??` sarebbero stati un
  numero solo.

  **Attenzione a cosa si può concludere da due conteggi marginali: niente.** Da due conteggi
  non segue che uno sia un sottoinsieme dell'altro, quindi non segue neanche il
  risultato della sottrazione. Se serve la scomposizione, si misura l'incrocio:

  ```js
  (() => {
    const riquadri = Array.from(document.querySelectorAll('.search-results'))
      .filter(e => e.offsetParent !== null);
    if (riquadri.length !== 1)
      return { errore: 'riquadri di risultati visibili: ' + riquadri.length };
    const box = riquadri[0];
    const api = box.querySelector('.ag-root-wrapper').__agComponent.gridApi;
    const m = box.innerText.match(/Sono stati trovati\s+([\d.]+)\s+risultati/);
    const dichiarati = m ? Number(m[1].replace(/\./g, '')) : null;
    let senzaEntrambi = 0, soloProvincia = 0, soloDescrizione = 0, conEntrambi = 0;
    let senzaDati = 0;
    api.forEachNodeAfterFilter(n => {
      if (!n.data) { senzaDati++; return; }
      const p = 'Comune__Provincia' in n.data, d = 'Comune__Descrizione' in n.data;
      if (!p && !d) senzaEntrambi++;
      else if (!p) soloProvincia++;
      else if (!d) soloDescrizione++;
      else conEntrambi++;
    });
    const contati = senzaEntrambi + soloProvincia + soloDescrizione + conEntrambi;
    return {
      senzaEntrambi, soloProvincia, soloDescrizione, conEntrambi,
      dichiarati, contati, senzaDati,
      completa: dichiarati !== null && contati === dichiarati && senzaDati === 0
    };
  })()
  ```

  Anche qui `completa` non è decorazione: un blocco che conta categorie e scarta i
  nodi senza dati rimetterebbe lo scarto silenzioso da un'altra porta, con la
  scomposizione che sembra tornare perché nessuno ha confrontato la somma con il
  dichiarato.

  Misurato su una sandbox: alcune righe senza né comune né provincia, altre con comune ma
  senza provincia, **0** con provincia ma senza comune, tutti gli altri completi. La
  somma torna al totale dichiarato, zero nodi scartati.
  Ora sono due problemi di anagrafica distinti *perché è stato contato*, non perché
  la sottrazione tornava.

I nomi dei campi si scoprono così, una volta per ricerca:

```js
(() => {
  const riquadri = Array.from(document.querySelectorAll('.search-results'))
    .filter(e => e.offsetParent !== null);
  if (riquadri.length !== 1)
    return { errore: 'riquadri di risultati visibili: ' + riquadri.length };
  const c = riquadri[0].querySelector('.ag-root-wrapper').__agComponent;
  const visti = new Set();
  return c.columnApi.getAllColumns()
    .map(col => col.getColDef())
    .filter(d => d.field && !visti.has(d.field) && visti.add(d.field))
    .map(d => ({ campo: d.field, intestazione: d.headerName }));
})()
```

Il `Set` non è pignoleria: fra le colonne della ricerca Impianto
`MotivoDismissione__Descrizione` è definita **due volte**.

E anche qui si parte dal riquadro visibile, non da `document.querySelector`: leggere
le colonne della ricerca precedente e applicarle a quella corrente produce un'estrazione
che passa la prova di completezza — il numero di righe torna — con **tutti i campi
nulli**. Completa e inutile insieme.

## Passo 5 — Aggregare, e dire come

Conteggi, somme e raggruppamenti si fanno sui dati estratti, non a occhio sulla
griglia. Nella risposta devono comparire tre cose:

1. **Il numero.**
2. **Su cosa è calcolato** — azienda, entità, filtri attivi, incluso quel
   `Attivi` che era già lì.
3. **Che la prova è passata**, con il totale dichiarato.

Esempio del tono giusto: *«N impianti attivi su <azienda>. Dichiarati
N, estratti N.»* — non *«circa N impianti»*.

## Quando i numeri non tornano

Non insistere con varianti dello stesso tentativo. Tre tentativi sostanziali sullo
stesso sintomo e poi si cambia diagnosi: il modello del problema è sbagliato, non il
tentativo. Riporta cosa hai visto, con i numeri, e chiedi.

## `Esporta` non è questa strada

Il menu ⋮ della griglia ha `Esporta`, e su NET l'esportazione passa dal client FTP:
il file non arriva sul PC, va ripreso da Esplora Risorse. Nel web **non è ancora
stato verificato** cosa faccia. Finché non lo è, per rispondere a una domanda si usa
la lettura della griglia descritta qui, non l'esportazione.

---

## Nota: per le tabelle vale il contrario

Quanto detto sopra — la rotta scritta a mano non cambia la ricerca — **vale per le
ricerche**. Per le **tabelle** `location.hash = '#/tabelle/<Entita>/table'` **funziona**,
ed è il modo più rapido di aprirle. Ma una rotta inesistente **lascia in silenzio la
tabella precedente**: si verifica sempre il titolo di `div.main-tab.selected`.
Metodo e rotte in `references/tabelle-rotte.md`.

## Strada diretta: il backend del web (produzione, sola lettura)

Quando la domanda riguarda **cosa c'è dentro ogni impianto** (installati, piano di
manutenzione, storico interventi), la ricerca avanzata non basta. Il web legge da un
backend ServiceStack, `/backend/<modulo>/json/reply/<Operazione>?…&u=…&c=…`. Si chiama
**dalla pagina**, con i cookie della sessione e gli stessi `u`/`c` che il web mette in
ogni chiamata (si leggono intercettando un `XMLHttpRequest.open`). Header:
`content-type: application/json`, `x-requested-with: XMLHttpRequest`. Solo GET:
scrivere da qui è vietato come dall'API.

| Operazione (modulo `assistenza`) | Parametri | Cosa torna |
|---|---|---|
| `AlberoImpianto` | `Id` (id impianto) | albero dell'installato: `TUTTI` (radice = impianto) → `CALDAIA` / `REFRIGERATORE` / `UIR` / `COMPONENTE` / `BRUCIATORE`, ognuno con `Stato`, marca, modello, date, e **`ListaOpMan`** con `Periodicita`, `DataPrecedente`, `DataProgrammata`, `DataLegale` |
| `PianoDiManutenzione` | `IdImpianto`, `Tipologia`, `IdInstallato` | le stesse operazioni, per un nodo |
| `AttivitaGeneriche` | `IdImpianto` | interventi, RdI e attività ufficio dell'impianto, con data e tipologia intervento |
| `InterventiSuInstallato` | `IdImpianto`, `IdInstallato`, `TipologiaInstallato` | interventi legati a una macchina |
| `QueryModelliGruppoFrigo` | — | modelli GF con condensatore/evaporatore/classificazione F-Gas (**dati poco affidabili**: WSAT XEM risulta aria/aria) |
| `QueryTipologieImpianto` | `IncludiOpMan=true` | tipologie con il piano di default (`OpManDefault`) |
| `QueryModelliUIR` | — | i modelli di unità interna ; `QueryModelliUnitaInterne` risponde 405 |

Un id impianto inesistente risponde `405 {"Installati":[]}`. Lo stesso `{"Installati":[]}`
arriva se a `AlberoImpianto` si passa `IdImpianto` invece di `Id` (produzione, 14/10/2026): un
albero vuoto non prova un impianto vuoto. Il giro completo su tutti gli
impianti, 6 richieste in parallelo, dura decine di secondi.

**Portare i dati fuori.** `javascript_tool` tronca ogni stringa restituita a circa
1000 caratteri, e il filtro blocca le sequenze simili a base64. `fetch` verso
`127.0.0.1` è bloccato dalla CSP, `window.open` dal blocco popup, `get_page_text`
legge solo il contenuto principale della pagina. Funziona così: si mette il testo in
una `textarea` temporanea, la si seleziona, si preme `cmd+c` con lo strumento
`computer`, poi `pbpaste > file` da Bash. La textarea va tolta subito dopo.
Attenzione: gli appunti dell'utente vengono sovrascritti.
