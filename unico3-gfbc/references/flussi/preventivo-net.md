# Preventivo su Unicò NET — procedura osservata (produzione)

Eseguita per intero su un preventivo di prova: testata, una decina di righe
(macchine con sconto di riga, trasporto, righe a distinta per materiale e manodopera), imponibile
come atteso. Lasciato **in bozza, non numerato**. Osservato su un caso solo.

## Dove si fa

- **I preventivi si fanno solo su Unicò NET** . Il web non ha il
  modulo: vedi `cosa-il-web-non-fa.md`.
- NET si apre dal **portale di login di Unicò: icona «Unico3»
  nella sezione Applicazioni**, che apre una scheda `html5.html`. Gira
  **nel browser** (non è la RemoteApp `.rdp`): è un canvas, non un DOM.
- Azienda: la si legge dalla **barra del titolo** del canvas, `C<tenant>_AZIENDA<n> - <ragione sociale>`:
  il numero dice quale azienda è attiva; se sia una sandbox lo dice solo `UNICO3_SANDBOX`. La URL non la dice, e la
  **porta** della scheda cambia da una sessione all'altra.
- **Chiudere la scheda o fare il Logoff del portale non chiude la sessione di NET**
  (in sandbox): al rientro non compare il Login, l'azienda è quella di
  prima e i moduli lasciati aperti sono ancora aperti. Per chiuderla davvero: nella
  finestra principale **File → Esci (F9)**; la scheda si chiude da sola e al rientro
  ricompare il Login. Le sessioni lasciate aperte sono anche il modo più facile di
  arrivare a «impossibile avviare più di 3 moduli».
- Coordinate misurate a 1280×800 (modulo, testata, dialogo di riga,
  tendine, barra in basso) sono indicate nelle sezioni seguenti.
  Sul Mac la finestra è diversa: si rileggono dallo screenshot.

- **NET può non partire da certe reti** (06/10/2026): «Connection interrupted!» o pagina
  d'errore. `nc -vz <host NET> <porta>` va in timeout mentre la 443 dello stesso host risponde:
  la porta NET è irraggiungibile dall'IP pubblico. Rimedio: un'altra rete (hotspot).
  Il blocco non è fisso: si prova prima con `nc -vz`.

## Canvas: cosa fa perdere tempo

- È un canvas: si guida con click a coordinate e tastiera (`computer`), non con
  `javascript_tool`.
- **Il canvas si ridimensiona** (cambio zoom del browser, finestra). Caso visto il
  01/10: il desktop remoto si è ridisegnato più piccolo (bordo marrone a destra) ma
  **l'input è rimasto sulla scala vecchia**: click = coordinate visibili × 1,112, cioè
  le coordinate calibrate prima continuano a funzionare e quelle lette dallo
  screenshot nuovo no. Dopo un ridimensionamento: un click di prova su un campo
  innocuo e uno zoom per vedere dove è finito. Più tardi, nella stessa sessione, il canvas è
  tornato a tutto schermo e la scala a 1:1: la regola non è fissa, si rimisura ogni
  volta (il cursore del mouse nello screenshot mostra dove è arrivato il click).
- **Testo: si incolla, non si digita.** `computer type` perde caratteri e accenti.
  Funziona un evento paste sul `contenteditable` della pagina:
  `const d=document.querySelector('[contenteditable]'); d.focus(); const dt=new DataTransfer(); dt.setData('text/plain',t); d.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}))`.
  Accenti e «Ø» passano; **il trattino lungo «–» no** (usare «-»). Cliccare il campo e
  **attendere 1–2 s** prima di incollare, altrimenti il testo va nel campo precedente.
- **Selezionare tutto un campo**: click destro → menu Windows → «Seleziona tutto».
  `ctrl+a` scrive «a». Per svuotare un campo corto: `End` + BackSpace a gruppi di 10
  con una pausa fra i gruppi (a raffica qualcuno si perde: controllare con uno zoom).
- **Codice articolo in riga**: cliccare, attendere 1 s, poi scrivere (senza attesa si
  perde il primo carattere) e confermare con **`Return`** — con `Tab` il codice può
  restare non risolto. Se il tipo riga resta «ARTICOLO» su un codice a distinta, si
  sceglie a mano «Articolo a distinta» nella tendina Tipo riga e si riscrive il codice.
- **Finestra nascosta**: NET si apre in una finestra Chrome a parte. Se è coperta o
  ridotta a icona, `document.visibilityState` è `hidden`, il canvas non si ridisegna e i
  click non arrivano; ridimensionarla non serve. Si chiede al titolare di portarla in primo
  piano.
- **Il canvas mostra valori vecchi.** Dopo una modifica salvata, riaprendo il
  preventivo la Descrizione di testata può comparire col testo di prima (08/10:
  quella lunga dell'originale) mentre il valore vero è quello nuovo: si vede
  cliccando nel campo e premendo `Home`. Stessa cosa per totali e righe subito dopo un
  salvataggio. Prima di correggere un valore «sbagliato», attendere e rileggerlo col
  focus nel campo.
- **A volte smette di ridisegnarsi** dopo i click: una domanda «Salvare le modifiche?»
  può essere aperta ma invisibile. Non premere tasti alla cieca.
- **Massimo 3 moduli aperti**: oltre compare «impossibile avviare più di 3 moduli».
  Chiudere le schede articolo aperte in sola lettura (Ritorna, poi **No** a «Salvare
  le modifiche apportate?»).
- Le finestre aperte si ritrovano in **Processi attivi** (la taskbar non sempre
  risponde ai click).
- Il **pannello appunti** di NET intercetta la tastiera; se chiuso, si riapre dalla
  barra in alto (tab «v», icona appunti) prima di incollare testi lunghi.

## Testata, poi dettagli

0. **L'anagrafica dev'essere Cliente (con codice).** «Cerca Anagrafica» di NET vede solo
   clienti/fornitori: un'anagrafica nata come semplice riferimento d'impianto (solo
   Occupante, senza codice) **non esce**, né per nominativo né per cognome. Si rimedia dal
   web: impianto → Riferimenti → `Aggiungi ruolo` → **Cliente** → CONFERMA; il codice viene
   assegnato subito. Anche la ricerca
   globale del web, categoria Anagrafiche, non trova le anagrafiche senza codice.

0. **NET riapre il desktop sull'ultima scheda usata** (sandbox):
   la scheda INSTALLAZIONE si clicca sempre, anche se sembra già selezionata. Su
   AMMINISTRAZIONE il punto (105,482) di «Preventivo» è «Scheda anagrafica» e apre una
   scheda anagrafica nuova.
1. Il modulo (scheda **INSTALLAZIONE → Preventivo**) **si apre già su un preventivo
   nuovo, n. 0** (15/10/2026, sandbox): «Nuovo» non serve, e premuto su una bozza salvata apre
   Numera (sotto). `...` di **Anagrafica**: l'indirizzo viene copiato in testata
   ed è modificabile (CAP correggibile lì). Nella ricerca, **codice cliente nel campo
   Codice + Cerca** carica direttamente l'anagrafica e chiude il dialogo da solo
   (13/10/2026; di nuovo il 15/10 in sandbox). La tendina Impianto
   mostra l'**id interno** dell'impianto, non il codice.
2. Descrizione, testo iniziale, testo finale, validità, pagamento.
3. **Il tab Dettagli si attiva solo dopo aver salvato la testata.** Il salvataggio crea
   il preventivo **in stato ELABORAZIONE come «Preventivo n. 0»**; da lì si attivano
   `Elimina` e `Numera`. **Non numerare** senza ok: la numerazione è definitiva.
   Nessun messaggio conferma il salvataggio: il segnale è la barra in basso. **Le icone
   sono dello stesso grigio scuro accese o spente; cambia l'etichetta** (nera = attivo,
   grigio chiaro in rilievo = spento). Salva diventa blu solo mentre è premuto. Misurato
   in sandbox: un controllo sul colore delle
   icone dice «non salvato» anche su una bozza salvata.

## Righe — esempio di convenzione, da adattare

**Manutenzione ordinaria a privato** (non contratto): una riga sola dall'articolo di
manutenzione, prezzo da listino, IVA agevolata. `<ART_MAN_PDC>` = pompa di calore;
`<ART_MAN_IBRIDO>` = impianto ibrido (prezzo netto dal listino, IVA inclusa in stampa).


Esempio di convenzione, da adattare:

- **Manodopera pura → `<ART_MANODOPERA_PREV>`**, articolo a distinta, una riga per lavorazione con la
  **descrizione cambiata** (es. «SMONTAGGIO N. 2 CLIMATIZZATORI…») e nella distinta ore,
  pasti, km. Mai l'articolo di manodopera semplice come riga diretta.
- **Materiale di installazione → `<ART_MATERIALE_PREV>`**
  a distinta, una riga per categoria (linee frigorifere, collegamenti elettrici, scarico
  condensa, canali e plenum, staffaggi e minuteria) con gli articoli unitari e le
  quantità in distinta. Il materiale non codificato va in distinta come **`<ART_MATERIALE_GENERICO>`**
  (generico, costo 0) con la descrizione cambiata.
- Descrizioni **sempre in MAIUSCOLO**.
- Macchine codificate con il **ricarico di listino**; nel preventivo lo **sconto di riga**
  porta al ricarico voluto (la politica dei ricarichi è dell'azienda).
- **Diritto di chiamata → `<ART_DIRITTO_CHIAMATA>`**: ha un'**IVA predefinita** diversa; sul privato
  in manutenzione straordinaria va portata a mano all'aliquota agevolata.
- Materiale a corpo senza componenti noti (es. «MATERIALE IDRAULICO PER ALLACCIO»):
  `<ART_MATERIALE_PREV>` con la descrizione cambiata, prezzo di riga a mano, costo lasciato al componente
  predefinito.
- Trasporto: articolo **`<ART_TRASPORTO>`**, fuori inventario: si usa cambiando la descrizione
  («TRASPORTO MATERIALE IN CANTIERE») e il prezzo.

## Dialogo «Inserimento dettagli PREVENTIVO»

Si apre col «+» del tab Dettagli. Campi: Tipo riga, Codice, Descrizione, Descr. estesa,
Pr. forfait / Pr. analitico, griglia Distinta con **Aggiorna**, poi Q.tà, Prezzo unit.,
Sconto %, Prezzo acq. A destra: ← esci, matita **Salva riga**.

- **Descrizione di riga: circa 60 caratteri.** Il resto va in **Descr. estesa**.
- **Dopo «Salva riga» il dialogo resta aperto su una riga nuova** (tipo ARTICOLO): si
  continua a inserire senza riaprirlo.
- **Sconto di riga**: si scrive in «Sconto %», l'importo si ricalcola (es. 1.000,00
  − 30% = 700,00). Visto a video, coincide col totale.

### Distinta

- `<ART_MANODOPERA_PREV>` arriva con **<ART_MANODOPERA> 1** (prezzi di acquisto e vendita dal listino); `<ART_MATERIALE_PREV>`
  con **<COMPONENTE_MATERIALE>** (manicotto 1", con il suo costo di listino). In entrambi i casi in **Pr. forfait**.
- **La griglia della distinta non si modifica direttamente**: una quantità scritta in
  cella non resta. Si clicca **Aggiorna**, che apre «Dettaglio articolo a DISTINTA»
  (Cod. articolo, Descrizione, Q.tà, Prezzo vendita, Prezzo acquisto; ← , «+», matita
  Salva, cestino).
- Il codice del componente è in sola lettura: il «...» accanto apre «Cerca Articolo»
  col focus su Cod. Interno; si scrive il codice e `Return`. Con un solo risultato
  entra subito, con più risultati si sceglie la riga e OK.
- **Salvare un componente che ne sostituisce uno esistente chiude il dettaglio**.
  **Salvare un componente aggiunto con «+» apre un dettaglio nuovo vuoto**: si usa
  subito per il componente successivo («...», codice, quantità, Salva), e alla fine
  si chiude con ←.
- In **forfait** i prezzi del componente sono disattivati (BackSpace lì cancella la
  descrizione, non il prezzo). Il prezzo di riga si scrive in «Prezzo unit.» e il
  **costo di riga in «Prezzo acq.», modificabile a mano**: per le righe materiale si
  mette la somma dei costi dei componenti (es. le linee frigorifere), altrimenti
  resta il costo del componente predefinito.
- **Modificare una riga già salvata**: selezionarla nella griglia dei Dettagli e
  matita a destra; si apre lo stesso dialogo, già compilato, con il fuoco su Q.tà. Dopo
  «Salva riga» il dialogo passa a una riga nuova vuota: si esce con ←. La modifica resta
  **in sospeso fino a `Salva` in basso**, come la cancellazione col cestino (15/10/2026
  notte, sandbox, su un numerato).
- **Pr. analitico** ricalcola prezzo e costo dal listino dei componenti: per `<ART_MANODOPERA_PREV>`
  è il modo giusto (ore × tariffa + pasti × prezzo + km × prezzo, ciascuno dal listino del
  componente; il costo si ricalcola allo stesso modo).
- **Descrizione di un componente** (es. «POSA UNITÀ INTERNA» rinominato
  «LINEA FRIGORIFERA COMPLETA AL METRO»): nel «Dettaglio articolo a DISTINTA» click
  destro sulla Descrizione → **Seleziona tutto** → incollare con l'evento paste. Scritta
  con `type` arriva storpiata (08/10/2026).
- **IVA di riga**: la tendina sotto il prezzo nel dialogo riga ha anche **N18**
  (inversione contabile, cliente con reverse charge); il valore va
  riletto dopo la scelta, la tendina non sempre prende il primo click.
- **Distinta lunga senza crash** (<ART_MATERIALE_PREV> con 22 componenti, 06/10/2026): per ogni
  componente **Aggiorna → «+» → «...» → codice → `Return`**; con più risultati doppio
  click sulla prima riga (il codice esatto viene per primo); quantità con `End` +
  `BackSpace` + valore (il triplo click non seleziona); Salva componente, poi **← per
  chiudere** il dettaglio vuoto che si riapre da solo. **Non usare «...» nel dettaglio
  riaperto in automatico**: dà «errore run-time 360 — Oggetto già caricato» e il modulo
  Preventivi si chiude, perdendo tutto ciò che non era salvato.

## Prima di chiudere

- **Le righe esistono sul server solo dopo `Salva` in basso.** «Salva riga» nel dialogo
  non basta: una disconnessione («Network not available!») o l'errore 360 le perdono.
  Checkpoint frequente: Salva riga → ← → `Salva` in basso → selezionare la riga →
  matita per riaprirla.
- **Copiare le righe da un altro preventivo**: menu della finestra **Utilità →
  Importa da preventivi**, si sceglie il preventivo e **Seleziona Tutti** (CTRL+T):
  shift e ctrl non selezionano righe singole. Porta distinte, sconti, IVA e costi; le
  righe che non servono si tolgono dopo. «Duplica preventivo» è disattivato.
- **Cestino** a destra: chiede «Si desidera veramente eliminare il record corrente?»,
  Sì elimina e rinumera. **Frecce ↑↓**: spostano la riga selezionata di una posizione
  per click (verificato il 06/10/2026).
- **Barra in basso con un menu aperto**: un click può finire su «Numera». Prima di
  cliccare nella barra, screenshot; se c'è un menu aperto, `Escape`. **Senza menu aperti
  `Escape` chiude l'intero modulo Preventivi** (13/10/2026): si riapre con Cerca +
  Cod. Anagr., e quello che non era salvato è perso. Se si apre il dialogo Numera, **Annulla**
  e verificare che Numero sia ancora 0.
- **`Nuovo` su un preventivo non numerato apre il dialogo Numera**: non è un click
  sbagliato, il programma chiede cosa fare della bozza. **Il predefinito è «Preventivo
  N°» con il numero già proposto** (sandbox): OK senza guardare la numera,
  zona rossa. **«Non numerare» → OK** lascia la bozza a n. 0 / ELABORAZIONE e apre il
  preventivo vuoto (verificato l'08/10/2026 su quattro bozze, controllate poi con Cerca);
  anche **Annulla** lascia la bozza a n. 0 e passa a un preventivo vuoto (15/10/2026, sandbox).
  Siccome il modulo si apre già su un n. 0, Nuovo non serve quasi mai.
- **Testata**: Descrizione tiene circa 48 caratteri e taglia il resto. La tabella
  Pagamenti non ha «40% all'ordine»: si sceglie «30% ALL`ORDINE…» da `...` e si corregge
  il testo nel campo (Home, Delete, «4»); il campo è testo libero. Scrivere nel campo
  Pagamento senza passare da `...` apre la ricerca da solo. Il menu a tendina Impianto
  a volte non prende il primo click: rileggere il campo.
- **Tastiera lenta sul canvas HTML5**: tasti in fila senza pause si perdono o finiscono
  nel campo sbagliato (una data digitata è finita nel Testo iniziale; `ctrl+a` ha
  scritto «a»). Un secondo di attesa fra click, tasto e testo; per sostituire un numero
  End + BackSpace ripetuto, poi il valore.
- In griglia dei Dettagli: righe numerate, «⊞» sulle righe a distinta, totale
  **Imponibile** in basso. Il «⊞» aperto inserisce sotto una riga **senza numero** (sfondo
  giallo, carattere piccolo: componente, U.d.m., quantità del padre × distinta, costo) e fa
  scendere di una tutte le righe sotto; alla riapertura del preventivo i «⊞» sono tutti
  chiusi (18/10/2026, sandbox). Chi conta le righe per posizione non lo clicca mai. Importo, IVA e Costo della riga stanno fuori vista a destra:
  si leggono con lo scorrimento orizzontale (sei click sulla freccia, a 1280×800). Le frecce ↑↓ a destra spostano la riga selezionata.
- La griglia dietro al dialogo di inserimento può mostrare **righe fantasma** (vista
  una riga durante una desincronizzazione): uscendo dal dialogo la griglia vera
  non l'aveva. Controllare la griglia dei Dettagli, non quella sotto al dialogo.
- `Salva` in basso conferma; Numero resta 0, stato ELABORAZIONE. **Il primo Salva non
  dà nessun messaggio**: si riconosce dalla barra in basso, dove Elimina, Numera, Stampa
  e Calcola si accendono (15/10/2026, sandbox). **Non usare** Numera,
  Stampa, Calcola né l'icona di ricalcolo (⟳) a destra: zona rossa senza ok.
- **Numera** (solo su ok esplicito del titolare): apre il dialogo «Numera» con il numero
  proposto (es. `N/26`), l'opzione «Non numerare» e lo **Stato** (In elaborazione,
  Presentato, Accettato, Respinto, Esecuzione in corso, Esecuzione completata, Parz.
  fatturato, Fatturato; predefinito lo stato attuale). Lo stato si cambia **solo** da
  qui: il campo Stato di testata non si modifica. OK assegna numero e stato **e li salva
  subito**, senza messaggi e senza aspettare `Salva` (15/10/2026 notte, sandbox: il numero è
  rimasto anche dopo Ritorna → No). Il titolo diventa «Preventivo: n. N/26 - <codice> -
  <cliente>» e il campo Numero è blu.
  - **La proposta è l'ultimo numero più uno con l'ultimo suffisso usato**: in sandbox, fermo
    al 2024, ha proposto il suffisso **24**. Cambiare il suffisso non ricalcola il numero. Al
    primo preventivo di un anno nuovo la proposta porta il suffisso dell'anno prima: si
    controlla il suffisso prima di OK.
  - Su un preventivo **già numerato** lo stesso dialogo cambia lo stato (Presentato →
    OK: salvato subito) e il secondo radio diventa **«Annulla numerazione»: zona rossa**.
  - Numera con modifiche non salvate chiede prima «Salvare le modifiche apportate?»;
    con No il dialogo si apre comunque e le modifiche restano nel modulo, non salvate.
  - **Annulla** del dialogo: su un numerato resta sullo stesso preventivo; su una bozza
    passa a un preventivo nuovo vuoto.
  - Su un Presentato NET lascia cambiare e salvare la **testata** (si spegne solo
    Importa), ma **non salva una riga**: la matita «Salva riga» del dialogo di riga non
    fa niente e il dialogo resta pieno, senza messaggi; in ELABORAZIONE salva e il
    dialogo si svuota (sandbox). Per cambiare le righe di un Presentato:
    Numera → In elaborazione → OK, righe, Salva, Numera → Presentato → OK. Dopo il passaggio in Accettato, titolo finestra e campo
  Numero aggiornati dopo Salva. Il primo click su Numera può andare a vuoto: si guarda lo screenshot prima
  di ricliccare.
- **PDF**: `Stampa` (561,740) nella barra → «Modulo di stampa», scegliere «Preventivo»
  (360,239) e `Stampa` (408,645) (non «Stampa su file» (348,474), che esporta solo
  Excel/Word; **mai «Email» (455,645)**, accanto a Stampa: manda dal programma). Il client
  HTML5 **scarica il PDF in ~/Downloads** come `AAAAMMGGThhmmss.mmm-tmpXXXX.pdf`, senza
  nulla di visibile sul canvas: ogni click è un download in più. Arriva 3-5 s dopo il
  click, ~50 KB, con una `HEAD` sull'origine di NET (`…/socket.io/JWN/download5/…`).
  La URL della `HEAD` ha una query anti-cache di sole cifre, «_» e «.» (misurata il 18/10/2026:
  un registro che taglia le query non la mostra, e un filtro di rete che non la prevede blocca il PDF).
  Su un server TSPlus può comparire sopra il dialogo Login un «Errore di applicazione» di
  «AutoIt v3: svcr.exe»: si chiude con OK; finché c'è, il dialogo Login non si riconosce.
  Il Modulo di stampa **resta aperto** dopo la stampa: si chiude con Ritorna (354,645)
  (18/10/2026, sandbox). Si rinomina
  `Preventivo NNN-AA <cliente>.pdf` nella cartella del cliente.
- **Colonna Sconto % in stampa**: menu della finestra preventivo **Impostazioni →
  Stampa** → «Impostazione di stampa», uno schema del layout a pulsanti: grigio =
  nascosto. Il pulsante **Sconto** sta fra «Pr.Unit» e «Importo» nella riga articolo;
  click per attivarlo, poi OK (926,175); Ritorna (926,209) scarta. Pulsanti: Sconto
  (798,405), Imposta (835,563), Totale ivato (835,583). Acceso = testo nero e bordo
  spesso, spento = testo grigio; un click scambia. Per riconoscerli da codice si contano i
  pixel quasi neri, non l'impronta esatta, che cambia fra due aperture (18/10/2026, sandbox).
  **Si attiva solo se il preventivo ha sconti di riga**
  (convenzione). Verificato su N/26: la colonna «Sconto %»
  compare con lo sconto di riga delle tre macchine. **L'impostazione resta per i preventivi successivi** (N/26 è uscito con la
  colonna vuota): su ogni preventivo **senza sconti** si apre la schermata e lo si
  spegne prima di stampare (verificato il 06/10/2026).
- **Cliente privato = prezzi IVA inclusa** (convenzione). Due posti:
  1. Impostazioni → Stampa: nel blocco dei totali accendere **Imposta** e **Totale
     ivato** (di default grigi; «Totale» resta acceso).
  2. Modulo di stampa: **prima** si clicca il modulo «Preventivo» nell'elenco, **poi** si
     toglie «Ometti IVA» (665,457) e si spunta «Prezzi Ivati» (665,508). Selezionare il
     modulo **carica le spunte salvate per quel modulo**: se le cambi prima, vanno perse
     in silenzio. Quelle salvate sono **le spunte dell'ultima stampa**, non i default
     (18/10/2026, sandbox: dopo una stampa con Prezzi Ivati, la scelta di «Preventivo» l'ha
     lasciata accesa, e un click alla cieca l'ha spenta: PDF a prezzi netti). Quindi
     dopo la scelta **si guarda ogni spunta** e si clicca solo quella diversa dal voluto.
  Risultato su N/26 (produzione): la colonna «Prezzo Unit.» mostra l'ivato con 4 decimali (il
  prezzo netto a 4 decimali portato a ivato), l'importo arrotonda a 2, poi Totale netto,
  Imposta e Totale ivato coerenti. Sul N/26 di sandbox (18/10/2026) l'ivato è uscito **a 2
  decimali** e la colonna «IVA %» **sparisce** con Prezzi Ivati;
  il numero esce «PREVENTIVO N° N/26» sulla riga della data. Si controlla sempre il PDF
  con `pdftotext -layout`.
  Per un'azienda restano i default (Ometti IVA, prezzi netti).
  **Con l'IVA agevolata (beni significativi) la stampa a prezzi ivati è giusta anche se
  sembra strana**: le righe «Storno valore bene significativo agevolato» e «Valore del bene
  significativo agevolato» escono ivate ad aliquote diverse (lo storno al 22, il valore al
  10 su N/26) e la somma delle righe torna col **Totale ivato**, non col netto. Non è un
  errore: non togliere «Prezzi Ivati» (togliendolo si ottengono prezzi netti incoerenti).
- **IVA agevolata 10% (DM 29/12/1999)**: pompa di calore al 22, tutto il resto al 10
  (compresi gli articoli di servizio), poi menu finestra **Utilità → «Ricalcola preventivo per
  prestazioni con iva agevolata 10%»** → Sì. Aggiunge da solo le tre righe dei beni
  significativi (valore, storno, valore agevolato). Non è il «Ricalcolo» dei prezzi di
  `guardrail.md` §5.2, ma modifica le righe del preventivo: in produzione è una scrittura che
  chiede l'ok esplicito, come ogni scrittura (`scrittura` → `conferma`). Nel dubbio la fa una persona. Il menu Utilità a volte non si disegna:
  click singolo e 3 s di attesa. IVA di riga: nel dialogo riga, tendina IVA sotto il prezzo.
- **Testi di testata**: niente «Gentili Signori»; testo iniziale di due o tre righe
  (oggetto della proposta e rimando al fascicolo con schede e tavole), il dettaglio
  tecnico va nel fascicolo. **Testo finale**, schema d'esempio
  (da adattare): riga vuota, `Consegna lavori: <da concordare | 15/20 giorni
  dall'accettazione, salvo ritardi da parte del fornitore>.`, riga vuota,
  `Esclusioni: I.V.A. come applicato da legge, <esclusioni specifiche>, e tutto quanto
  non espressamente sopra menzionato.`
  Per svuotare un campo testo: click, click destro →
  **Seleziona tutto**, di nuovo click destro → **Elimina**, poi incollare. Il testo a
  volte risulta già selezionato e Elimina è subito attivo, ma non sempre (08/10/2026,
  Elimina grigio al primo click destro su tre bozze su quattro): si guarda il menu
  con uno zoom prima di cliccare.
- **Data «Validità al»**: incollata non entra, e digitata con le barre viene troncata
  («31/10/202») e poi scartata. Si scrive **solo le cifre**: click, attesa, `Home`,
  `31102026`.
- Pagamento: la lista **non scorre** con la rotella: si filtra scrivendo nel campo
  Pagamento (es. `%VISTA%`) e `Cerca`. Nella lista dei pagamenti **OK prende la prima voce**, non quella
  evidenziata: si sceglie con **doppio click** sulla riga.

## Altre osservazioni (produzione)

- **Operatore**: la tendina in testata; per i preventivi preparati da un agente automatico si sceglie l'operatore previsto dall'azienda.
- **Login di NET**: all'ingresso compare «Login» con Azienda e Terminale: si clicca Connetti, non chiede credenziali. **Azienda propone l'ultima usata dal terminale**, non sempre `Azienda1` (15/10/2026: dopo una sessione su Azienda2 è ricomparso su Azienda2): si guarda il campo, o si sceglie la voce dalla tendina, prima di Connetti, e dopo si controlla il titolo.
- **`Escape` con la finestra Preventivo in primo piano la chiude** (Ritorna), senza domande se era salvata. Non usarlo per chiudere i menu. **Ritorna** (in basso a sinistra) su una bozza appena aperta ha chiuso il modulo senza domande con una modifica non salvata, che si è persa (15/10/2026, sandbox); su un numerato con testata o righe modificate chiede invece «Salvare le modifiche apportate?» (Sì/No), e **No scarta tutto, righe comprese** (15/10/2026 notte, sandbox). Dopo Ritorna si guarda la schermata: con la domanda aperta un click su INSTALLAZIONE → Preventivo apre un **secondo** modulo, e il primo resta dietro con la domanda (lo si ritrova dalla barra in basso). **Mai chiudere la finestra di NET con quella domanda aperta**: la sessione remota resta viva e al login successivo NET non mostra il Login, si ricollega e ritrova modulo e domanda (18/10/2026, sandbox). «No» (717,476) funziona anche lì. Sì (633,476), No (717,476).
- **All'apertura di un preventivo è selezionata l'ultima riga** dei Dettagli: matita o cestino senza un click di riga agiscono sull'ultima. Righe a y = 254 + 20·(N−1), click a x 300 (18/10/2026, sandbox). Matita (1196,318), cestino (1196,355) → Sì (682,476), «+» (1196,242) → Codice (460,241) + `Enter` (`Tab` non carica l'articolo); la riga nuova va in fondo. Il «Prezzo acq.» di riga è unitario, e la colonna **Costo** della griglia mostra il costo unitario anche sulle righe da più pezzi (per esempio su una riga da 2 ore); il Costo complessivo in basso è la somma di quantità × unitario (18/10/2026, sandbox).
- **Cerca → Cod. Anagr.**: con un solo preventivo del cliente lo apre direttamente, senza passare dalla lista. Vale anche per **N° e suffisso**: con un solo risultato il preventivo si apre (15/10/2026 notte, sandbox). Le date Dal/Al sono già sull'anno corrente. Campi del dialogo: N° (435,235), suffisso (499,235), Dal (443,254), Al (627,254), Cerca (1061,220), Annulla (1061,285). Una data si sostituisce con click, `End`, dieci `BackSpace`, un secondo di pausa e le cifre senza barre (`01012000`); `Home` + cifre no. Senza pausa dopo i `BackSpace` o subito dopo l'apertura del dialogo le cifre si perdono o finiscono in N° (18/10/2026, sandbox). Con zero o più risultati il dialogo resta aperto («Totale Record selezionati = N»). Nella lista la riga si sceglie sul **selettore a sinistra**: un click sulle celle non sposta la selezione.
- **Riga libera per una macchina o un kit non codificato**: articolo `<ART_MATERIALE_GENERICO>` come riga diretta (doppio click su <ART_MATERIALE_GENERICO> fra i due risultati), descrizione cambiata, prezzo e **Prezzo acq.** a mano (somma dei costi dei componenti).
- **`<ART_MANODOPERA_PREV>`**: Aggiorna → Q.tà del componente <ART_MANODOPERA> (ore) → Salva chiude il dettaglio. Il Prezzo acq. di riga **non si ricalcola** in forfait: si scrive a mano ore × costo orario.
  **Seconda forma, misurata in sandbox**: le ore nella **Q.tà della riga**, distinta non toccata. NET la accetta: Importo = ore × prezzo, Prezzo acq. resta il costo orario **unitario**, la riga del componente nel «⊞» segue da sola (Ore 2 su una riga da 2). Senza componenti in distinta NET rifiuta <ART_MANODOPERA_PREV> del tutto («l'articolo a distinta selezionato non presenta dettagli. Impossibile continuare!»). In sandbox `Enter` su <ART_MANODOPERA_PREV> propone **prezzo 0 e IVA 22**, nessun dialogo; il tipo di riga diventa «ARTICOLO A DISTINTA» con la griglia Distinta e Aggiorna al posto della descrizione estesa, e i campi sotto restano dove sono in un articolo semplice. In produzione il prezzo proposto non è misurato: prezzo e IVA si scrivono comunque sempre.
- La tendina Impianto mostra l'**id interno** dell'impianto finché non si riapre il preventivo.

## Non ancora verificato

Selezione di righe singole in «Importa da preventivi» (solo Seleziona Tutti provato).
