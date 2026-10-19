# Carico DDT fornitore nel web — procedura eseguita (produzione)

Eseguita su due DDT di fornitori.
Esiste dalla **release 2026.3**; prima si faceva solo dal
terminale. In produzione è una scrittura: serve l'ok del titolare.

## Convenzioni (ricavate dai carichi da fornitore già presenti)

- **Una distinta per DDT.** Tutte le righe del DDT nello stesso movimento.
- **Data movimento = data del DDT**, non la data di registrazione.
- **Descrizione** = `<impianto> - <CLIENTE>` con eventuale `- prev.NNN/26`, oppure
  `SCORTA MAGAZZINO` / `<impianto> ... + SCORTA`.
- **Destinazione**: `MU Materiale in uscita` se il materiale è per un lavoro preciso,
  `MC Magazzino Centrale` se è scorta, il **furgone** del tecnico se va a lui.
- **Causale** `Carico da fornitore | Acquisto` (altre: Garanzia, Conto lavorazione, Reso).
- **Riferimenti**: Tipo `D.d.t.`, Numero e Data del DDT così come stampati.
- **Prezzo**: sui DDT di solito i prezzi sono di **listino, non scontati**. Il prezzo
  netto giusto è quello dell'**offerta o della conferma d'ordine**: se c'è (ticket
  dell'impianto, ordine fornitore), si carica quello. La differenza DDT contro offerta
  **non è un'anomalia e non si segnala al fornitore** (convenzione d'esempio; es. prezzo di listino sul DDT più alto di quello d'offerta:
  resta quello d'offerta). Senza offerta né
  conferma si carica il prezzo del DDT. «Aggiorna listino base» resta spento (cambierebbe
  un articolo esistente: serve l'ok).
- «Ordine N» scritto su un DDT può essere il **numero d'impianto**, non un ordine.
  Gli ordini fornitore veri di Unicò
  si leggono dalla ricerca `Materiale in ordine` (numerazione `NNN/26`).
- Anagrafiche con nome diverso dal DDT: la ragione sociale sul DDT può differire da quella in anagrafica
  (stesso indirizzo); un fornitore può avere **due** anagrafiche: si usa quella con la sede della P.IVA stampata sul DDT;
  un DDT intestato a un distributore si carica sull'anagrafica del distributore (ordine N/26).
- **Prima di caricare, cercare i doppioni**: la ricerca `Movimento di magazzino` senza
  filtri carica in AG Grid tutti i movimenti, si filtra per fornitore
  (`ClienteFornitore__Nominativo`) e finestra di date attorno al DDT. Un DDT
  può risultare già caricato con data diversa da quella del DDT.
- DDT senza prezzi (convenzione d'esempio): ultimo prezzo d'acquisto (anagrafica,
  conferma d'ordine, preventivo); se manca riga a 0 e segnalazione all'amministrazione.
  Si registra solo materiale: resi di noleggio, strumenti in riparazione, attrezzatura
  (idropulitrice, borsa portautensili) restano fuori.

## Prima del carico

1. L'articolo deve esistere. Cercarlo **per codice e per descrizione** (webservice
   `/magazzino/articoli/elenco/da/{id}`, campo `Scheda`, e ricerca globale; le pagine sono da
   1000 e ripartono **compreso** l'id passato, quindi si tolgono i doppioni per `Scheda.Id`): il codice del
   DDT può differire da quello in anagrafica.
   Se manca si crea (5.1-ter), sul modello di un articolo simile.
2. **Articolo di tipo Matricola: la riga vuole la matricola, obbligatoria.** Se il DDT non
   la riporta si prende dalla DiCo o dalla fattura al cliente (caso di una wallbox: tabulato
   componenti della DiCo N/26).

## Passi

1. `Magazzino → Azioni → Crea movimento` → modale «Nuovo movimento magazzino», Testata.
2. Data movimento, Descrizione, Numero e Data riferimento: input normali, si scrivono con
   il setter nativo di `value` + evento `input`. Appena aperta la modale le etichette non
   sono ancora pronte: attendere 1–2 s prima di cercarle. ⚠️ «Data movimento» nasce con la
   data di oggi: con un DDT di oggi riscriverci lo stesso testo non cambia il binding, e la
   PUT porta l'istante in cui si è aperta la modale (`2026-10-15T08:56:52.332Z`), non
   `2026-10-15`. Con un DDT di oggi la data si lascia com'è; con un'altra data si scrive
   [misurato 15/10/2026, sandbox].
3. `Da` → pulsante **Fornitore** → campo «Seleziona fornitore»: scrivere un filtro, la voce
   è un `x-option` con «codice | ragione sociale | indirizzo».
4. `A` → **Magazzino** (già selezionato) → tendina: `MC` / `MU`. Per un furgone: pulsante
   **Furgone** accanto a Magazzino, poi la tendina dei furgoni. La voce è la `Descrizione`
   intera della tabella `Furgone` (`#/tabelle/Furgone/table`), «FURGONE n» seguito dal
   nome del tecnico, non «FURGONE n» da sola: un'etichetta accorciata non trova la voce
   [misurato 15/10/2026, sandbox].
5. Causale e Tipo riferimento: tendine con `x-option`.
6. **AVANTI** passa ai Dettagli **senza salvare**.
7. `+` → modale «Aggiorna movimento magazzino»: Articolo (filtro + `x-option`), Lotto o
   **Matricola**, Quantità, Prezzo, Importo. ⚠️ **Cambiare la Quantità ricalcola il Prezzo
   dal listino base** con un `POST` asincrono, che sovrascrive un prezzo scritto nello stesso
   script: prima la Quantità, poi si aspetta il ricalcolo, poi Prezzo e Importo. ⚠️ Prezzo
   impostato da script **non ricalcola l'Importo**: impostare anche Importo, poi rileggere.
   Gli importi **con la virgola** («12,34»): sul campo già formattato il punto diventa il
   separatore delle migliaia, «12.34» → 1.234,00 [misurato 14/10/2026, produzione]. CONFERMA aggiunge la riga **solo
   nella modale**: non salva niente (passano solo i `POST` di calcolo
   `ValoriMovimentoSchedaArticoloRequest`), e un ANNULLA del movimento la butta
   [misurato 14/10/2026, sandbox]. ⚠️ **La colonna Quantità del DDT va letta riga per riga**: un
   importo di riga è spesso cumulativo (l'importo vale per tutti i pezzi della riga,
   non per un pezzo). Prezzo netto unitario = importo di riga / quantità; verificare
   che la somma delle righe dia l'imponibile merce del DDT [misurato 19/10/2026, produzione].
8. Controllare il **Totale** contro il DDT, poi **CONFERMA**: il movimento si salva e la
   modale si chiude. È una sola `PUT …/magazzino/json/reply/UpsertMovimentoMagazzino`, che
   torna 204 **senza identificativo**: la prova è la Verifica qui sotto.

## Verifica

Ricerca `Movimento di magazzino` (filtro `Cod. articolo`, oppure `Da` → Fornitore + `Dal` = data del DDT; CERCA), poi il modello AG Grid
(`__agComponent.gridOptions.api.forEachNode`): Data, fornitore, destinazione, causale,
descrizione, quantità, prezzo, importo, `NumeroDistinta`. La griglia **non mostra** i
riferimenti DDT: si leggono aprendo il movimento (doppio click sulla riga apre «Modifica
movimento magazzino»; uscire con ANNULLA).

## Giro a script (07/10/2026, più DDT in un colpo)

> **Helper non inclusi.** `window.U3`, `U.fill`, `rowFill`, `setPrice`, `window.__mov` sono funzioni
> scritte in pagina con `javascript_tool` durante le sessioni d'origine e non sono nel repository:
> qui c'è la logica, il codice va riscritto prima di usare il giro a script. Senza, si segue il giro a click.

Helper in pagina (`window.U3`): `pick(label, filtro, regex)` sulle `.x-select-value` per
etichetta, `openMov()` dalla tessera, `testata()`, `row()` / `rowOk()`, `salva()`. Il giro
gira senza `await` (limite 45 s di `javascript_tool`) e scrive in `U3.log`; si ferma se
fornitore, magazzino, causale, articolo, «Aggiorna listino base» acceso o totale non
tornano. ⚠️ L'input «Data» del riferimento va preso per etichetta **esatta**: `startsWith`
prende «Data movimento». L'«+» dei Dettagli è il secondo `x-icon` visibile della modale.
Stesso schema per creare articoli: UM si sceglie con filtro
`Numero` (la voce è «N Numero»).

## Giro a click con browser_batch (15/10/2026)

Più robusto dello script puro: testata e righe a **click reali** a coordinate (viewport 1568x713),
con `javascript_tool` solo per `U.fill` (Data, Descrizione) e per riga/prezzo (`rowFill(codice,qta,null)`
poi `setPrice(prezzo,qta)`, **prezzo numerico**: una stringa dà «toFixed is not a function»).
- Fornitore, magazzino A e causale: click sul campo, scrivere il filtro, **attendere 3-4 s**, click
  sulla voce (primo risultato a (930,304) per il fornitore; MU a (920,350); «Acquisto» a (535,417)).
  Una voce non cliccata lascia il campo vuoto senza errore.
- ⚠️ Se la testata è incompleta **AVANTI non avanza e non dice niente**: il «+» non apre nulla e
  `rowFill` scrive il codice articolo nel campo Fornitore, azzerando fornitore e causale. Sintomo
  nel batch: `Illegal invocation` in `U.setv`. Rimedio: cmd+a nel campo, riscrivere, rifare i
  click, riverificare con uno zoom prima di AVANTI. Uno screenshot subito dopo ANNULLA può essere
  vecchio.
- Il prezzo proposto è il listino base lordo: va sempre riscritto col prezzo del documento.
- Verifica: ricerca Movimento di magazzino → CERCA → `window.__mov` dal modello AG Grid
  (`.ag-root-wrapper` → `__agComponent.gridOptions.api.forEachNode`), filtro su `NumeroDistinta`.
  Il conteggio sale di una unità per riga.
- Listini fornitore: la tendina «Listino» del nuovo listino elenca i listini già creati per ciascun fornitore.
- Nuovo articolo + listino a click: Magazzino (icona carrello a (26,339)) → tessera → Codice,
  Descrizione, prezzi (con virgola), UM «Numero», IVA «22», Gruppo «Ricamb» → CONFERMA (1131,609) →
  LISTINI (85,295) → «+» (1497,641) → Listino, Codice per ordine, prezzi → CONFERMA (970,540).
