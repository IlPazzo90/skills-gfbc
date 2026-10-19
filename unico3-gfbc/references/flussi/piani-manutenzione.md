# Piani di manutenzione delle macchine — procedura eseguita (produzione)

Eseguita in produzione: prova su poche macchine, poi giro a script su centinaia di
macchine senza contratto e senza piano. In produzione è una scrittura: serve l'ok del titolare
(prova su poche macchine, poi blocchi verificati).

Le regole di contenuto (quale voce, che periodicità, che data) sono dell'azienda: quelle qui sotto sono un
esempio di convenzione, da adattare. In breve: GT → MANC annuale + AF e RB
biennali; GF senza contratto → MAOPDC annuale (PDC novembre, clima/chiller aprile); MAN
solo sui componenti; il piano sta sulla macchina, non sull'impianto.
AF e RB dei GT: **allineati al CRITER** (RR 1/2017
Emilia-Romagna, Allegato B, note 3–5). Gas/GPL, potenza utile complessiva dei generatori
**attivi** dello stesso impianto: **< 35 kW → Biennale**, generatore nuovo: primo controllo
a 4 anni; **≥ 35 kW → Annuale**, primo a 2 anni (il CRITER conta dall'installazione,
l'azienda dalla prima accensione). La periodicità resta quella ordinaria anche sul
generatore nuovo («non sono quadriennali, sono sempre biennali»): cambia solo la prima
scadenza. Con storico: ultima AF/RB (colonna «Ultima», `DataPrecedente`) + periodicità,
altrimenti ultima manutenzione eseguita + periodicità. Senza storico, o se la data è già
passata: data della MANC. Vale per gas e GPL: per gasolio, pellet e legna le periodicità di
AF e RB non sono state date, si chiedono al titolare. 
Potenza: tabella `#/tabelle/ModelloGruppoTermico/table`, AG Grid
→ `PotenzaNominaleKW` per `Id` = `IdModello` del nodo CALDAIA (alcuni modelli sono a 0: si giudica
dal nome). Storico per singola macchina:
`InterventiSuInstallato {IdImpianto, IdInstallato, TipologiaInstallato:'CALDAIA'}` →
`Interventi[]` (Data, TipologiaIntervento, Esito, Descrizione; `IsEvasa` è sempre false).
Prima accensione: intervento «1^ Accensione», oppure `AlberoImpianto` → nodo CALDAIA →
`DataPrimaAccensione`; `Stato` dice se è Dismesso. Ultima
manutenzione = qualunque intervento con manutenzione/pulizia/igienizzazione/sanificazione
nella descrizione; avviamento o prima accensione valgono come base (+12 mesi).

## Prima di scrivere, per ogni impianto (dal vivo, non dal censimento)

- **Tag «CLIENTE A CONTRATTO»**: `SchedaImpianto {IdImpianto}` → `Tags[]` (il tag definito dall'azienda). Se c'è
  e il contratto non si trova (impianto, anagrafica, storicizzati, ticket), mail
  d'anomalia al referente e il piano non si tocca.
- **Contratti**: `Contratti {IdImpianto}` → `Risultati[]` (non un array diretto). Con un
  contratto attivo il piano segue il contratto.
- **Piano attuale**: `PianoDiManutenzione {IdImpianto, Tipologia, IdInstallato}`.
  Tipologia: `CALDAIA` per i GT (`GT` dà 400), `REFRIGERATORE` per i GF, `COMPONENTE`,
  `UIR`, `TUTTI` con IdInstallato 0 per le voci sull'impianto.
- ⚠️ **Id impianto ≠ codice impianto**: la rotta usa l'Id, l'intestazione mostra il
  Codice. Per confrontare l'intestazione si legge
  `SchedaImpianto.Codice`.

## Web

1. Rotta `#/assistenza/impianto/<Id>/dettagli/<GT|GF>/<IdInstallato>/altri-dati`, poi
   clic sulla scheda verticale «Piano di manutenzione» (`div.vertical-tab`). ⚠️ Andando
   direttamente su `/piano-di-manutenzione` la griglia resta quella della macchina
   precedente, anche dopo un reload, e la tendina esclude le voci del piano vecchio.
2. `+` in basso a destra (l'`x-fab` visibile più a destra) → modale «Nuova operazione di
   manutenzione». Installato già proposto: la macchina della rotta.
3. Tipologia: filtro per descrizione (AF → «Analisi», RB → «Rilascio», MANC →
   «generatore», MAOPDC → «PDC»); trova anche il codice: «MANC» → MANC Manutenzione
   generatore calore [sandbox, 15/10/2026]. Le `x-option` arrivano **lente** (anche 10 s,
   «Caricamento...»), e col testo scritto tutto d'un fiato non arrivano mai: si cancella
   l'ultima lettera e la si riscrive (`interazione.md`). Il testo
   dell'opzione è `MAOPDCManutenzione ord. PDC/Chiller` (codice e descrizione attaccati
   in `textContent`).
4. Periodicità (Annuale, Biennale…), Scad. progr. `gg/mm/aaaa` (setter nativo + input,
   change, blur). Ultima e Scad. legale vuote.
5. CONFERMA: il salvataggio può impiegare 6–10 s prima che la modale si chiuda.
6. Modifica di una voce: clic sulla riga → matita a destra → «Modifica operazione di
   manutenzione» → MODIFICA. Una voce sull'impianto **si sposta** cambiando
   «Installato», non si cancella.
   Da script (`PM.editOne(code, data)`, 09/10): riga AG Grid del piano trovata per
   descrizione (MANC «Manutenzione generatore calore», AF «Analisi combustione», RB
   «Rilascio bollino»), `mousedown/mouseup/click` sulla prima `.ag-cell`, poi la matita
   (l'`<a>` visibile con lo stesso `path d` dell'icona), controllo del codice nella
   modale, Scad. progr. col setter nativo, MODIFICA. Circa 20 s a macchina con 3 voci.
   Coda `PMeditQ`/`PMeditLog`, sorgente `PM3src`; rilettura dal backend dopo ogni macchina.
   Periodicità nella modale di modifica: è un `enum-picker`, il valore si legge da
   `.x-select-value` (non c'è input); le opzioni arrivano lente (~30 s). Dopo MODIFICA il
   `ux-dialog-container` resta nel DOM qualche secondo. `Runtime.evaluate` con await su
   modale va in timeout: il giro si lancia senza await e si interroga.
   **Nella modale di modifica anche la Tipologia si cambia** : una
   voce sbagliata (es. MAOPDC su un GF a contratto) si **converte** nella voce giusta
   (VGUE) invece di cancellarla, così il classificatore non blocca.
   Installato, Tipologia e Periodicità si cambiano **nella stessa MODIFICA** (produzione,
   14/10/2026, le tre voci da caldaia precaricate da «Impianto
   Residenziale» portate su GF1 e U01). Il selettore «Seleziona impianto/installato» è un
   albero, con la freccia per i figli; il suo MODIFICA conferma solo la scelta. Cambiato
   l'Installato, la Tipologia si svuota e va scelta di nuovo.
   Lo spostamento è una sola `PUT …/UpsertOperazioniDiManutenzione` col corpo che porta
   `OpMan.Id` (la creazione non lo porta), e la risposta restituisce lo stesso Id: la voce
   non si duplica e il nodo Impianto resta senza voci [sandbox, 15/10/2026, voce portata
   dall'impianto al GT2, riletta da `AlberoImpianto`]. Un doppio clic sulla riga del
   piano apre «Nuova operazione» invece della modifica: si annulla e si usa la matita.
   Rotta dei componenti: `/dettagli/CMP/<IdInstallato>/…` (GT, GF, CMP); `PM.addG`
   funziona anche lì passando come match il modello (es. «BAPICOT»).
7. Cliccando a coordinate sbagliate si apre «Modifica informazioni» della macchina:
   ANNULLA.
8. ⚠️ **La tipologia dell'impianto può vietare il piano sulla macchina.** In sandbox, con
   «Riscaldamento semplice <35 kW», il `+` del piano è spento sul nodo Impianto e la
   CONFERMA di una voce sul GT torna 500: «Un impianto semplice può avere operazioni di
   manutenzione solo sull'impianto». Con «complesso» o «misto» la voce va sulla macchina
   [misurato 14/10/2026, sandbox]. In produzione le tipologie sono altre: se compare quel messaggio è
   la tipologia, e cambiarla (testata espansa → matita della sezione TIPOLOGIA,
   `PUT …/UpsertTipologiaImpianto {IdImpianto, IdTipologia}` → 204) è una scrittura da
   proporre al titolare. La modale si chiama «Modifica tipologia» e il pulsante che salva è
   **MODIFICA**. Le matite della testata compaiono solo col mouse sopra, e vicino alla
   TIPOLOGIA ci sono quelle dei tag, dell'anagrafica e del codice: prima di toccare un
   campo si guarda il titolo della modale [sandbox, 17/10/2026, più prove: ogni
   volta una modale sbagliata aperta e chiusa con ANNULLA prima di quella giusta].

## Giro a script

Helper in pagina `window.PM` (**non incluso** nel repository: la logica è descritta qui per
riscriverlo):
`go(imp,t,id)` naviga e verifica rotta e codice in intestazione; `runQ` per ogni
macchina controlla che il piano sia vuoto, aggiunge le voci con `addG` (controlla che
l'Installato contenga la matricola mostrata, tipologia, periodicità e data prima di
CONFERMA) e rilegge dal backend; si ferma al primo errore. Il giro gira senza `await`
(limite 45 s di `javascript_tool`) e si controlla a intervalli.
Circa 10 s a macchina con una voce, 30 s con tre. Dopo ore di lavoro la pagina rallenta
fino a bloccare `Runtime.evaluate` (36k nodi DOM): si ricarica il tab.

Coda persistente: job in `localStorage.PMq`, esiti in `PMlog`, sorgente degli helper in
`PM2src`; `runQ(40)` si mette in pausa ogni 40 macchine e un ciclo `auto` lo riavvia
finché il DOM resta sotto 15k nodi. Per fermare a metà si sostituisce `addG` con una
funzione che lancia un errore: la macchina in corso resta parziale e va completata a mano.

**Ricaricare il tab**: `location.reload()`, cmd+r e `navigate` sulla stessa URL non
bastano (cambia solo l'hash) e un `beforeunload` «Leave site?» blocca. Funziona
`navigate` con `force: true` verso una query diversa (`?r=N&c=/C<tenant>/A1/#/home`).
Dopo il reload `SchedaImpianto` torna **400** se manca l'header `x-eventsession-id`
(altre letture, come `PianoDiManutenzione`, passano): si intercetta `setRequestHeader`
di `XMLHttpRequest`, si apre un impianto qualunque e lo si copia nelle chiamate.
⚠️ `window.__U3H` è un **oggetto** `{nomeHeader: valore}`, non la stringa: salvandoci la
stringa `SchedaImpianto` resta 400.

⚠️ **Mai usare un secondo tab di Unicò mentre gira una coda**: il tab in background ha i
timer rallentati e il giro si blocca.
⚠️ Il classificatore dei permessi di Claude Code nega il clic su OK delle cancellazioni
(«Vuoi eliminare l'operazione…») anche con l'ok dell'utente: le fa lui a mano o concede
il permesso. Non si aggira.

Codici delle tipologie: `U3B('assistenza/json/reply/QueryTipologieOperazioniDiManutenzione',{Take:500}).Elementi`
(anche oltre cento voci, a seconda della configurazione).

## Gruppi frigo: controllo perdite F-gas (CF) e RCEE tipo 2 (CEECDZ) — 09–11/10/2026, produzione

Regole di esempio (da adattare): CF **con la stessa data della manutenzione**, solo sui GF che
la norma obbliga, solo impianti e macchine attivi, contratti esclusi (li segue l'assistenza).
- **CF** (codice `CF` «Controllo perdite - FGAS»; attenzione ai doppioni con codice diverso). Reg. UE
  2024/573 art. 5: t CO2e = kg × GWP / 1000; < 5 t esente, ≥ 5 annuale, ≥ 50 semestrale,
  ≥ 500 trimestrale. HFO puri o quota HFO delle miscele (Allegato II): ≥ 1 kg annuale,
  ≥ 10 semestrale, ≥ 100 trimestrale, vale la frequenza più stretta. Rilevatore di perdite
  → frequenza dimezzata. Ermetico < 10 t (e HFO < 2 kg) esente. R-290/R-744/R-717 non F-gas.
- **CEECDZ** («CEE Condizionamento»): CRITER (RR ER 1/2017) sopra 12 kW ogni 4 anni
  (`Quadriennale`), da 100 kW ogni 2 (`Biennale`). PDC reversibile: potenza maggiore fra
  freddo e caldo (FAQ SEZ.4-006); apparecchi su sottosistemi diversi: conta il singolo
  (SEZ.3-053, SEZ.4-005); stesso sottosistema: si somma (casi dubbi → al titolare). Esclusi
  gli scaldacqua PDC solo ACS. Si scrive **solo con potenza certa** (macchina o modello in
  Unicò, scheda, rivenditore), mai su stime.
- Potenza e carica: nodo REFRIGERATORE di `AlberoImpianto` (`PotenzaFrigoriferaNominale`,
  `PotenzaTermicaNominale`, `ListaCircuiti[].Kg/FluidoFrigogeno{GWP}/IsRilevamentoPerdite`,
  `Modello.IsErmeticoCircuiti`), poi tabella `ModelloGruppoFrigo` (centinaia di modelli:
  `PotenzaFrigoriferaKW`, `PotenzaTermicaKW`, `Tipologia`).

**Tabella Fluidi GAS** (`#/tabelle/FluidoGas/table`), corretta l'09/10 sul Reg. 2024/573
(Allegato I AR4, miscele per Allegato VI; propano 0,02 da Allegato VI AR6, il 517/2014
diceva 3). Il campo GWP accetta solo interi. Modifica: griglia virtualizzata (si scorre
`.ag-body-viewport` finché compare la cella), `mousedown/mouseup/click/dblclick` sulla
`.ag-cell` → «Modifica fluido GAS» → GWP (input number), Categoria (x-select HFC|HCFC|CFC|
HFO|HC, valore in `.x-select-value`) → MODIFICA. Il clic a coordinate non funziona.

**Giro a script** (`PM.runX(key[, max])`, helper **non incluso**: va riscritto, insieme
all'hook degli header): coda `[imp,'GF',id,[[codice,periodicità,'gg/mm/aaaa']]]`, salta se
la voce c'è già, rilegge dal backend e si ferma al primo errore. Dopo un reload
gli helper vanno ricaricati, poi si apre un impianto qualunque per catturare
`x-eventsession-id` (senza, `SchedaImpianto` torna 400).
- La lista della **Periodicità è virtualizzata**: `pick` scorre `div.options.open` finché
  compaiono Semestrale, Quadriennale, Biennale.
- Testo dell'opzione = codice + descrizione attaccati: `CEECDZCEE Condizionamento` non
  passa il controllo «maiuscola+minuscola» dopo il codice → regex dedicata (`PM.RX`).
- ⚠️ **Finestra Chrome nascosta = giro fermo**: con `visibilityState` hidden le tendine non
  caricano. Ridimensionare non basta, AppleScript non vede la finestra del gruppo MCP: la
  porta davanti il titolare.
- Velocità misurata: 10–30 s a macchina con una voce.
- Salvataggio di una voce = `PUT backend/assistenza/json/reply/UpsertOperazioniDiManutenzione`,
  corpo di **una voce sola**: `{OpMan{IdImpianto (stringa), IdentificativoMacchina{Id,
  TipoMacchina}, IdTipoOperazione, Periodicita, NumeroGiorni, NumeroMesi}}`, più `OpMan.Id`
  in modifica. `DataProgrammata` dipende dal nodo: sulla voce di un GT viaggia sempre,
  `null` se vuota; sulla voce del nodo Impianto (`TipoMacchina` `TUTTI`) la chiave manca
  [sandbox, 16/10/2026]. Il corpo è completo: chi riscrive una voce rimanda
  la `DataProgrammata` letta, o la azzera. Risposta `{Id}`.
  Lettura del piano: `GET …/PianoDiManutenzione?IdImpianto=<Id>&Tipologia=TUTTI` per il
  nodo Impianto (le voci hanno `IdentificativoMacchina {Id: <Id impianto>, TipoMacchina:
  "TUTTI"}`), `&Tipologia=CALDAIA&IdInstallato=<Id GT>` per un GT. Risposta
  `{OperazioniDiManutenzione: [{Id, IdentificativoMacchina, IdTipoOperazione,
  TipoOperazione{Codice, Descrizione, Id}, Periodicita}]}`, più `DataInAgenda`,
  `OraInAgenda`, `DurataInAgenda` per le voci in agenda; i campi vuoti mancano.
  `Periodicita` è maiuscola (`ANNUALE`, `BIENNALE`, …). In sandbox AF e RB stanno sul nodo
  Impianto, non sul GT [sandbox, 16/10/2026]. Eliminazione di una
  voce: `PUT …/CancellaOperazioneDiManutenzione {IdImpianto (stringa), IdOpMan}` → 204
  [misurato 14/10/2026, sandbox]. Prima scrivevo «upsert di lista»: il corpo non era stato
  catturato. Non chiamarli a mano: si salva dall'interfaccia, come ogni scrittura.
