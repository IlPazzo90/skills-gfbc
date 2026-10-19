# Contratti di manutenzione: inserimento e allineamento (produzione)

Procedura eseguita in produzione su decine di contratti.
In produzione è una scrittura: serve l'ok del titolare.

## Regole (esempio di convenzione, da adattare)

- **Fonte = PDF del preventivo accettato** (stipula = data di accettazione). ⚠️ **Tutti i
  modelli di preventivo dell'azienda hanno il tacito rinnovo**: la pagina «Tariffe
  manutenzione straordinaria / Diritti esclusivi / **Durata del contratto**» è
  un'**immagine**, `pdftotext` non la legge (verificato a vista).
  Clausola (esempio): un anno dal primo giorno del mese dopo l'accettazione, rinnovo automatico di
  anno in anno salvo disdetta con raccomandata/PEC con preavviso.
  Quindi **tacito sì, 1 anno**, salvo eccezioni scritte. Eccezione di legge: **enti
  pubblici** (Comuni) → tacito no, è vietato per la PA.
- **Copertura: si spuntano le singole macchine**, mai «TUTTI» (impianto intero). Per un
  AZI su più impianti: tutte le macchine degli impianti coperti, salvo quelle escluse dal
  preventivo.
- **Rate: solo future.** Una rata già fatturata non si inserisce; se c'è, si toglie.
- **Contratto scaduto**: se era a tacito (quasi sempre, vedi sopra) → si correggono le
  date, **niente proposta**. Solo se il preventivo aveva davvero una scadenza → attività
  «1. PROPOSTA MANUTENZIONE» a chi gestisce i rinnovi (nuovo ticket). ⚠️ Gli esiti
  di «1. PROPOSTA MANUTENZIONE» sono solo Appuntamento, Da richiamare, Non risponde e
  «4.x … Negativo»: **non c'è un esito neutro per chiuderla**. Aperta per errore → si
  aggiorna la nota (✏️ → Note → CONFERMA) e la chiude chi la gestisce.
- **Piano allineato al contratto, per tutti**: ogni macchina coperta ha le sue voci
  (GF: VGUE/CFUNZ/CF; UIR: MAN; PF; CDUR/CFUNZ…) con la frequenza del preventivo e la
  prima esecuzione programmata.
- **Riferimenti**: «per togliere si sostituisce non si cancella» (pulsante ⇅ Sostituisci)
  e la sostituzione o dismissione vuole la **data inizio incarico**. Il ruolo che conta per
  il contratto è **Cliente**; «Dest. corr.» si aggiunge quando lo chiede il titolare.

## Web

- Rotte: `#/assistenza/impianto/<Id>/contratti`, dettaglio in
  `/contratti/<IdContratto>/copertura`. Se il pannello dettaglio non compare: passare da
  `/riferimenti` e tornare.
- **Le rate dal web si inseriscono** (smentito il vecchio «rate in sola lettura»): riga con
  articolo canone del contratto (es. `<ART_CANONE>`), prezzo, IVA, scadenza, competenza. Prezzo impostato da script non
  ricalcola l'Importo: si scrive anche quello e si rilegge. Reverse charge = IVA **N18**.
  Privati IVA 10%. **Enti pubblici**: aliquota come nelle loro fatture
  (lette da `/documenti/emessi` del webservice
  con `IsSupportoDistinte=true`).
- ⚠️ **L'articolo canone nella tendina Articolo dà «Nessun risultato»**: è «Fuori inventario» e
  `RicercaRapidaArticoli` parte con il filtro `TipiArticolo` sui soli «Semplice». Si
  toglie quel parametro dalla richiesta (hook su `XMLHttpRequest.open`) e lo trova.
- Convenzione testata: N° = numero del preventivo, Suffisso = anno a due cifre,
  Riferimento «Prev. N/26 Rev.1», tecnico vuoto. Nel wizard la Copertura elenca solo
  gli impianti dove l'anagrafica ha il ruolo Cliente.
- **«Modifica copertura»** (matita in alto a destra della copertura) funziona anche sui
  contratti creati da un altro utente. La griglia è **AG Grid virtualizzata**: si legge con
  `__agComponent.gridOptions.api.forEachNode`; le checkbox cliccate via JS sono lente, ma il
  modello si aggiorna. Si verifica sempre dal backend.
- Sui contratti **creati da un altro utente** il **salvataggio della testata torna 500**
  (`PUT assistenza/json/reply/UpsertContratto` → 500; anche
  senza toccare il riferimento). Su quelli creati da noi passa. Date e tacito si
  correggono dal **NET** (vedi sotto). Il web non dice il motivo del 500.
- Nel contratto nuovo il **tacito a volte si accende da solo** dopo l'inserimento delle
  date: ricontrollare prima di salvare.

## NET (Unicò NET HTML5)

Assistenza → Estrazione dati → Contratti → filtro **Numero** dal/al (o Cod. Impianto;
clic, attesa, secondo clic, poi scrivere: il primo clic dà solo il focus) → Cerca →
doppio clic sulla riga → finestra «Contratti del cliente …». Tacito, date, copertura e
rate sono lì. Si modifica con la **matita** a destra della testata. Tacito: clic sulla
checkbox, anni dalla tendina. ⚠️ **Le date di copertura non si scrivono da tastiera**:
pulsante calendario accanto al campo → frecce dell'anno → giorno → OK.
**File → Salva**: nessun messaggio di conferma, la finestra resta aperta; si chiude con
la freccia ←. ⚠️ **La lista della ricerca non si aggiorna** dopo il salvataggio (né con
Cerca, né nella colonna Durata): per controllare si riapre il contratto o si legge il
backend. Dopo un salvataggio dal NET il backend web può restare **lento 30–60 s** (le
richieste sembrano appese): si riprova con timeout lungo, non si risalva.
Eseguito su più contratti
verificati dal backend o
riaprendo il contratto. ⚠️ Il filtro **Numero** della ricerca è il numero del preventivo
(colonna N° contr.), non l'Id del contratto. Il NET mostra la vera natura delle
macchine «Generico» (es. addolcitore, split).

## Backend (lettura e verifica)

Helper `window.U3B(rotta, corpo)` **non incluso**: una POST JSON alla rotta del backend con gli header della sessione.
`window.U3B('assistenza/json/reply/Contratti',{IdImpianto|IdAnagrafica})` →
InizioCopertura, FineCopertura, IsTacitoRinnovo, DurataTacitoRinnovo,
`Copertura[].IdentificativoMacchina{Id,TipoMacchina}`, `Rate[]` (DataScadenza,
DataCompetenzaInizio/Fine, ImportoNetto, ImportoIvato, Stato). Se torna `[BLOCKED]`,
chiedere solo i campi. `PianoDiManutenzione {IdImpianto,Tipologia,IdInstallato}` per il
piano, `AttivitaGeneriche {IdImpianto}` per le attività ufficio e gli interventi (Descrizione = nota, NumeroTicket, `TipologiaAttivita`, `HasFilesAllegati`: dice quali attività hanno file).
**Allegati dell'impianto** (le copie firmate dei contratti stanno qui, cartella «Preventivi
Approvati»): `generale/json/reply/FilesAllegatiRequest {IdImpianto}` → `[{Id, Path}]`; il
file si scarica con `generale/json/reply/Download?Open=true&Path=<Path>&u=…&c=…`. Le
scansioni non hanno testo: si leggono a vista (pdf.js da cdnjs dentro la scheda di Unicò,
render su canvas in overlay; il visore PDF di Chrome in una scheda di sfondo non si aggiorna).

## Attività ufficio collegate

Evadere **RISCONTRO PREVENTIVO** con esito «3. Accettato - CTR MAN» apre un wizard a tre
passi: RISCONTRO → **INSERIMENTO RATE CONTRATTO** → **INSERIMENTO PIANO DI MANUTENZIONE**,
ognuno «Evadi ora» con esito (1. Rate inserite / 1. Inserito) e nota, poi CONFERMA. ⚠️
**Lo stato del preventivo resta «Presentato»** (verificato): dal web il
preventivo ha solo «Stampa», lo stato si cambia dal NET.

Audit dei contratti (09/10/2026, sola lettura): `PreventiviSchedaImpianto {IdImpianto}`
(Risultati: Id, Numero, Suffisso, Data, Descrizione, Stato), `DettaglioPreventivoSchedaImpianto
{IdPreventivo, IdImpianto}` (Righe, Imponibile), `AlberoImpianto {Id}` → `Installati[]`:
ogni nodo ha `Tipologia`, l'oggetto sotto quella chiave, `ListaOpMan` (il piano) e
`ListaInstallatiFigli`. <ART_MANODOPERA_PREV> compare su tutti i preventivi: non distingue i contratti.
⚠️ Nei messaggi alle persone si usa il **Codice** impianto, non l'Id.

Catena del ticket: … RISCONTRO PREVENTIVO (3. Accettato - CTR MAN) → **INSERIMENTO RATE
CONTRATTO** (esito «1. Rate inserite») → **INSERIMENTO PIANO DI MANUTENZIONE** (esito
«1. Inserito»). Inserite le rate, se l'attività è aperta si evade con nota UA.
Lista attività: `#/assistenza/impianto/<Id>/attivita/?Group=true&IdImpianto=<Id>&Type=Tutti`
(senza IdImpianto giusto resta la lista dell'impianto precedente). Nota di un'attività già
evasa: riga → menu ⋮ del pannello → **Aggiorna note** → MODIFICA (non riapre l'attività).
Nota di un'attività **aperta**: il menu ⋮ ha solo Stampa, Cambia impianto, Elimina; si usa la
matita del pannello → «Modifica attività ufficio» → Note (textarea) → CONFERMA, l'attività resta aperta.
Nuova attività dal web: se la tendina Ticket è vuota si sceglie «Apri nuovo ticket».
