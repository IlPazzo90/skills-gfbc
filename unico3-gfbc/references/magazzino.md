# Magazzino, preventivi, commesse

Articoli, giacenze, movimenti, inventario, cataloghi, ordini, e il ciclo
**preventivo → commessa → consuntivo**.

---

## La struttura: un solo magazzino, tanti depositi

Magazzino Centrale + **magazzini periferici, cantieri e furgoni**. Il concetto che regge
tutto:

> **Tutto ciò che sta in centrale, periferici, cantieri e furgoni è giacenza aziendale**,
> e l'inventario li somma tutti.

Le scorte **scendono** con gli **scarichi a cliente** (DDT di vendita, rapportini…) e con
i **resi a fornitore**. **Salgono** con i **carichi da fornitore** e con i **resi da
cliente**. Quello che è stato **consegnato al cliente non è più disponibilità aziendale**
e non compare più negli inventari.

---

## La scheda articolo

**Quattro tipologie** di articolo, e **la tipologia si cambia solo finché l'articolo non
è mai stato movimentato**. È la decisione da non sbagliare all'inizio.

Obbligatori: **tipologia, descrizione, codice** (alfanumerico, **univoco**; 24 caratteri
nel web, 16 nel terminale) e **unità di misura**.

Campi che contano più di quanto sembri:

- **Codice a barre** — EAN13. Se si lascia vuoto, **Unicò ne assegna uno interno valido**;
  se lo si scrive sbagliato l'errore è **bloccante**, ma il programma sa calcolare il
  **check-digit**.
- **Listino base** — i due prezzi di riferimento, acquisto e vendita
- **IVA** — proposta in fatturazione, **ma un'aliquota preferenziale sull'anagrafica
  cliente ha la precedenza**
- **Escluso da liste** — per gli articoli obsoleti: già movimentati, quindi non
  cancellabili, ma spariscono dalle ricerche
- **Nascondi in stampa** — esclusi dalla stampa dei documenti; servono solo a movimentare
- **c/Acquisti** e **c/Vendite** — contropartite contabili di default
- **Carburante** — serve alla fattura elettronica, che vuole quella marcatura
- **Famiglia merceologica** — codifica UNI/CEN
- **Dati conformità** — finiscono nell'**allegato materiali della Dichiarazione di
  Conformità**
- **Scorta minima** — sotto soglia esce un avviso *solo se il flag è attivo nelle
  impostazioni movimenti*; **Lotto riordino** = quanto si ordina di solito

### Listini sull'articolo — perché non basta il prezzo

Un articolo può avere **quanti listini si vuole**, e ogni listino porta **prezzo di
acquisto, prezzo di vendita, codice a barre e `Codice ordine`**.

Il codice ordine è la parte importante: **scegliere un listino significa scegliere il
codice con cui l'articolo verrà ordinato a quel fornitore**. Un solo articolo interno,
tanti codici fornitore. E ogni listino può essere **agganciato a una voce di catalogo**,
così l'aggiornamento del catalogo aggiorna il listino.

Sul lato vendita: listini diversi per acquirente o situazione (garanzia, contratto), e il
listino si può **legare al singolo cliente o al contratto** perché si applichi da solo.

Su A1 (misurato il 16/10/2026 dal webservice): oltre a `LB` (listino base) e ai listini
dei fornitori (una sigla per fornitore), molti articoli hanno **`LUP` = «ULTIMO PREZZO»**,
che porta l'ultimo prezzo d'acquisto e spesso vendita 0. Per sapere quanto è stato pagato
l'ultima volta si legge `LUP`, non il listino del fornitore.

I gas tecnici sono a **litri di bombola** (`AZOTO`, `OSSIGENO`, `ACETILENE`, UdM `l`), i
refrigeranti a **kg**: un'offerta «a bombola» si divide per i litri della bombola prima di
confrontarla.

### Giacenze

Allocazione su ogni deposito, più il riepilogo:

- **Totale giacenza** = somma di tutti i depositi
- **Totale impegnato** = quantità inserite **in commessa** (l'icona mostra dove)
- **Totale disponibile** = giacenza − impegnato
- **Ordinato non evaso** = negli ordini fornitore ancora aperti
- **Totale dotazione standard** = somma delle scorte minime, e se la giacenza è sotto
  compare il **reintegro** con i pezzi mancanti

Doppio click (o matita) su una riga di deposito per cambiare **scorta minima, scaffale e
posizione** su *quel* deposito.

### Matricole, distinta, movimenti, file

- **Matricole** — solo per articoli a matricola; togliendo `visualizza solo esistenti` si
  vedono anche quelle **transitate** e non più presenti.
- **Distinta** — solo per articoli a distinta; in fondo il **TOTALE ANALITICO** calcola
  acquisto e vendita sommando i componenti al listino base.
- **Movimenti** — **dall'ultimo inventario in poi**; per vedere prima serve la spunta
  `visualizzare movimenti antecedenti`.
- **File allegati** — quelli di tipologia **Foto** compaiono nel riquadro immagine della
  scheda.

Utilità: **crea articolo da catalogo** · **modifica tipologia** (solo verso una
compatibile) · **duplica ultimo articolo inserito** (tutto tranne il codice).

### Nuovo articolo nel web — misurato su A1

Permesso: in produzione creare un articolo chiede conferma, a meno che il titolare non l'abbia autorizzato in modo permanente con `UNICO3_AUTORIZZATE=crea_articolo` (`guardrail.md`, 5.1-ter).
⚠️ **Il guardrail della skill non basta a Claude Code.** Un subagent in modalità automatica
può essere bloccato dal classificatore dei permessi nel creare un articolo su A1
(«Modify Shared Resources», «Auto-Mode Bypass»), anche con l'ok del titolare girato dalla
sessione principale e con una regola `autoMode.allow` scritta dall'agente stesso: un
permesso che l'agente si concede non conta. La creazione va fatta **dalla sessione
principale con il titolare che approva il prompt**, o a mano da lui. Non delegare scritture
su A1 a un subagent in background.

`#/magazzino/home/actions` → tessera **Nuovo articolo** → modale «Nuovo articolo»: Tipo
articolo (Semplice / Matricola / Fuori inventario / Distinta), Codice, **Descrizione (massimo
60 caratteri)**, Prezzo acquisto, Prezzo vendita, Marca, Codice a barre, Lotto riordino,
Unità di misura, Aliquota IVA, Gruppo merceologico, Conto acquisti e vendite (predefiniti
dell'azienda). **CONFERMA** salva e apre `#/magazzino/articolo/<id>/altri-dati`:
il nuovo id nella URL è la prova che l'articolo esiste. Prezzi acquisto/vendita della modale
finiscono nel **listino base**.

- Le tendine (Marca, UM, IVA, Gruppo) sono liste virtuali: le voci sono `x-option`, in `position: fixed` (visibilità con `getClientRects().length`, non `offsetParent`, che è sempre null — 06/10/2026) (misurato 30/09/2026 via script; il 24/09 si era scritto `div.picker`) (non
  `[role=option]`) e compaiono solo **dopo aver scritto un filtro** nel campo (`Numero`, `22`,
  `Prodotti`); a vuoto mostrano solo le prime. Si attende la voce fino a qualche secondo:
  sotto carico IVA e Gruppo arrivano tardi, e il tipo Matricola a volte non prende.
  Su A2 il 15/10/2026 il Tipo articolo (Fuori inventario, Distinta) non ha preso 3 volte su 4
  al primo click della modale appena aperta: si riapre la tendina e si rilegge il tipo.
  Fuori inventario cambia da solo il conto vendite.
- Prima di CONFERMA **rileggere ogni campo** dal testo mostrato (non da `input.value`, che
  per le tendine resta vuoto): due volte su 40 una tendina non aveva preso, e la rilettura
  ha fermato il salvataggio.
- Descrizione oltre 60 caratteri: CONFERMA mostra «Ci sono dati non validi, impossibile
  continuare» e non salva.
- Annulla con dati inseriti chiede «I dati … andranno persi» (RITORNA / ESCI).
- `javascript_tool` si interrompe dopo 45 s: un giro di più articoli va lanciato senza
  `await` e letto a intervalli da una variabile di pagina.
- **Aprire e compilare in due chiamate separate** (misurato creando più articoli di fila): la modale aperta e compilata nello stesso script trova i campi non ancora
  montati. Ogni tendina ~2–3 s; IVA e Gruppo vanno scelti uno alla volta, rileggendo.
- Le modali chiuse restano nel DOM nascoste **con i valori di prima**: lo script deve
  lavorare sulla modale visibile (`getClientRects().length`), non sulla prima trovata.
  `Escape` su una modale compilata apre la domanda RITORNA / ESCI.

Correggere tipo o gruppo di un articolo già creato (misurato su A1 il 25/09/2026, id N):
**tipo** → click sul badge del tipo (`Semplice`) in testata → modale «Modifica anagrafica
articolo» → tendina Tipo articolo → MODIFICA (Semplice → Matricola accettato; compare la voce
MATRICOLE a sinistra). **Gruppo, marca, UM, IVA** → freccina a sinistra della testata per
espanderla → click sulla riga dei dati → modale «Modifica informazioni» → MODIFICA.
Il menu `…` della scheda ha solo Registro operazioni / Duplica / Elimina.

Apparecchi (split, caldaie): **tipo Matricola, gruppo FINITI «Prodotti finiti»**, non
RICAMB: è la convenzione dell'azienda di riferimento, da definire per ogni azienda. Gli articoli
creati prima della convenzione possono essere ancora Semplice/RICAMB: non prenderli a modello.

Prezzo di un articolo **senza listini fornitore** (appena creato): testata espansa → click su
«LISTINO BASE» → modale «Modifica listino base» (acquisto, vendita) → MODIFICA. Nei campi
importo si scrive **con la virgola**, digitando o da script: il punto digitato viene scartato («123.45» diventa 12345) e su un campo già formattato viene letto come separatore delle migliaia (`interazione.md`, regola 5). Una volta un valore col punto scritto da script su un campo vuoto è arrivato giusto: non è una regola.

Solo la vendita del listino base, anche su un articolo **con** listini fornitore (per esempio una serie di apparecchi
a ricarico percentuale fisso): la stessa modale «Modifica listino base» si apre dalla testata e cambia solo
la base; i listini dei fornitori restano come sono. Da script scrivere nell'input (setter + `input`/`change`)
non basta, il valore non arriva al salvataggio: va messo nel modello del componente,
`xNumberInput.au.controller.viewModel.value = '123.45'` (stringa, **punto** decimale: è il valore, non il
testo formattato), poi il bottone `ux-dialog-container x-button a` con testo «Modifica». Rileggere dopo il
salvataggio: la verifica fatta quel giorno è il riallineamento dell'app esterna da Unicò (tutti uguali).

Prezzo di un articolo esistente: scheda → **LISTINI** → selezionare la riga del listino
fornitore → matita → «Modifica listino», nuovo prezzo, spunta **Aggiorna listino base** →
MODIFICA. Senza la spunta cambia solo il listino del fornitore.
I prezzi tengono **al massimo 4 decimali** (esempio: 1,234567 salvato come 1,2346): un
prezzo a bombola diviso per i litri non torna al centesimo sulla riga d'ordine.

Guida da script (misurata in produzione su un lotto di articoli e listini): la modale è `ux-dialog-body`; i campi
sono `x-text-input` / `x-number-input` / `x-select`, riconoscibili dal testo della loro `label`.
⚠️ **Mai cambiare `location.hash` con una modale aperta**: la modale resta sopra la nuova
scheda con i dati dell'articolo precedente (visto: «Modifica listino» con il codice d'ordine
dell'antifreeze sulla scheda della vaschetta). Prima di MODIFICA controllare che il «Codice per
ordine» della modale sia quello dell'articolo aperto. Se la modale si pianta a metà chiusura,
ricaricare la pagina. Articolo senza listino fornitore: `+` rosso → «Nuovo listino» (Listino,
codice per ordine, prezzi, spunta Aggiorna listino base) → CONFERMA.

---

## Movimenti di magazzino

> **Nel web dal 2026.3**: `Magazzino → Azioni → Crea movimento`. Procedura eseguita su A1
> per i DDT d'acquisto in `flussi/carico-ddt-fornitore.md` (07/10/2026).

Molti nascono da soli emettendo o registrando documenti. La funzione manuale serve per i
**carichi iniziali**, per i **carichi da ordine fornitore** e per le movimentazioni
straordinarie.

Due fasi: **testata** (comune a tutte le righe) e **dettagli**. In testata sono
obbligatorie **origine (`Da`)** e **destinazione (`A`)**, e **la causale viene pilotata
da quella scelta**. La sezione **Riferimenti** (numero e data del DDT del fornitore)
serve a ritrovare i movimenti dopo — vale la pena compilarla.

### Rettifiche — due causali che non sono intercambiabili

Si ottengono mettendo **origine e destinazione entrambe su Magazzino Centrale**.

| Causale | Quando | Effetto sul prezzo |
|---|---|---|
| **Carico iniziale** | prima giacenza di un articolo mai movimentato | **aggiorna l'ultimo prezzo di carico** ed **entra nel calcolo dell'inventario** → **va valorizzato**, altrimenti l'inventario esce sbagliato |
| **Carico / Scarico di rettifica** | la giacenza reale è diversa da quella a sistema | **non altera il prezzo unitario** → si può lasciare prezzo 0 |

Sceglierle a caso è il modo più semplice di falsare l'inventario.

---

## Inventario e valorizzazione

Si valorizza **in qualsiasi momento e anche a una data passata** (i movimenti successivi
alla data vengono scartati), per allocazione o sul complessivo, con filtro sulla giacenza.

**Tutti e tre i metodi guardano solo il prezzo di acquisto**: il valore degli scarichi non
conta. Quindi **i carichi devono sempre avere il prezzo**, o il calcolo non vale niente.

| Metodo | Note |
|---|---|
| **Prezzo medio ponderale** | il più accurato — **ma va in crisi con le giacenze negative** |
| **Ultimo prezzo di acquisto** | l'ultimo carico registrato |
| **Prezzo acquisto listino** | il prezzo di acquisto del listino base |

### La trappola della giacenza negativa

La guida porta due tabelle identiche per quantità e prezzi, in cui l'unica differenza è
uno **scarico datato prima dell'ultimo carico**. Nel primo caso il valore di magazzino è
corretto; nel secondo la giacenza passa **per un periodo in negativo** e il prezzo medio
si falsa — e **l'errore si trascina sulle movimentazioni future**.

Un articolo non può esistere in quantità negativa: quando succede, l'unica valorizzazione
sensata è **ultimo prezzo** o **listino**.

**Chiusura inventario** → vedi la sequenza di fine anno in `amministrazione.md`:
prerequisito assoluto **nessuna giacenza negativa**, e una volta chiuso i movimenti sono
**storicizzati e immodificabili**.

---

## Catalogo

I cataloghi dei fornitori si importano in formato **Excel**, **testo ASCII** (delimitato o
a lunghezza fissa) e **ANGAISA 5.1 / 6.0**, più il tracciato FUTURA e alcuni proprietari.

> **Gli articoli di catalogo NON diventano articoli di magazzino.**

Ed è voluto: un catalogo ha migliaia di righe, e importarle tutte significherebbe gestire
decine di migliaia di codici inutili. Si passa a magazzino **uno per uno**, con
`Crea articolo da catalogo`.

Quando lo si fa nasce un **collegamento dinamico** fra la voce di catalogo e **uno dei
listini** dell'articolo: aggiornando il catalogo si aggiorna il listino. La spunta
**`Aggiorna listino base`** estende il collegamento anche al listino base.

**Aggiorna dati di catalogo** si comporta in due modi: con **un articolo selezionato**
apre tutto in modifica; con **più articoli** apre la modifica per criteri comuni — è così
che si assegnano in blocco marca, gruppo, UdM e IVA, e che si **calcola il prezzo di
acquisto applicando uno sconto in cascata** (`45+5+3%`) sul prezzo di vendita, che è la
situazione normale quando arriva un listino nuovo.

### Importazione catalogo nel web — wizard 4 passi

1. **Sorgente e destinazione** — file `xls`, `xlsx` o `csv`, dal PC o dal **cloud Unicò**;
   nuovo catalogo o **catalogo esistente** (allora si sceglie anche il listino). La
   **data di importazione** conta: importando su un catalogo esistente **le date vengono
   confrontate**, quindi va messa **successiva all'ultima importazione**.
2. **Mappatura campi** — l'abbinamento colonna→campo è **euristico**: va controllato.
   Per i campi tabellati (UdM, Marca, Gruppo, IVA) si può scegliere direttamente la voce
   di tabella. Qui si applicano anche **sconti o maggiorazioni** su acquisto e vendita.
   ⚠️ Unicò **ricorda le scelte precedenti**: se il fornitore cambia l'ordine delle
   colonne, **prezzo di acquisto e di vendita finiscono invertiti** senza dire niente.
3. **Anteprima** — prima e dopo; tutte le righe selezionate di default, ma si può scegliere.
4. **Configurazione** — solo importando su un catalogo esistente:
   - **aggiungi nuove voci al catalogo**
   - **elimina voci obsolete** — solo se **non hanno articoli di magazzino collegati** e
     se la data del nuovo catalogo è **successiva**
   - **aggiorna voci catalogo** — sovrascrive quelle corrispondenti
   - **aggiorna prezzi articoli a magazzino (listino)**
   - **aggiorna descrizioni articoli a magazzino**

---

## Liste materiale

Il **copia-incolla fra documenti** di Unicò. Da qualunque documento le righe di dettaglio
si salvano in una lista (data, tipologia, descrizione), e la lista si reimporta altrove,
anche solo in parte.

Si collegano a **tecnico, tipologia intervento, operazione di manutenzione** e a
**tipologia documento**, e da lì entrano nei documenti — anche quelli emessi da mobile.

Utilità: **copia da lista** (sommando più liste si costruisce un preventivo informale) ·
**copia da lista Magbar** (terminali barcode) · **ricalcolo** (es. vendita = acquisto
+45%) · **modifica a blocchi** di sconto e IVA.

---

## Ordini a fornitore

**Si fanno su Unicò NET**, non sul web: procedura eseguita, coordinate e trappole in
`references/flussi/ordine-fornitore-net.md`.

**Quattro stati**, e ognuno cambia cosa si può fare:

| Stato | Significato |
|---|---|
| **In elaborazione** | aperto, modificabile, **non ancora inoltrato**; **non può generare carichi** |
| **Confermato** | trasmesso al fornitore; **la numerazione è obbligatoria** |
| **Sospeso** | numerato ma sospeso: **non genera carichi**, riattivabile quando si vuole |
| **Evaso** | il carico è stato registrato con `importa` (o forzato a mano da `Numera`) |

La numerazione **non passa dalla tabella Numerazioni**: è un progressivo automatico. Per
ripartire da 1 si numera a `1` il primo ordine dell'anno, o si azzera da
`Utilità → Numerazione`.

Quattro tipi di riga: **articolo** (carico automatico all'evasione) · **articolo a
distinta** (**genera una riga per ogni componente semplice**) · **articolo manuale**
(anche pescato dal catalogo) · **testo** (anche da glossario).

In basso, **in rosso, l'importo minimo previsto per l'ordine**.

### Importa — le due funzioni che fanno risparmiare tempo vero

**Da sottoscorta**: il **Listino è obbligatorio** — per cercare su tutto il magazzino si
sceglie il **LISTINO BASE**, a cui tutti gli articoli sono per forza associati. La marca
è facoltativa. Poi si sceglie la quantità:
- **Reintegro** — quanto serve per **tornare alla scorta minima**
- **Lotto riordino** — la quantità fissa della scheda articolo

**Da ordine ANGAISA**: se il fornitore fornisce il file dell'ordine fatto online, si
importa e **si evita di ridigitare tutto** per il carico.

---

## Preventivi

**Si fanno su Unicò NET** (nel browser, dal portale): procedura e convenzioni dell'azienda
(codici di riga, maiuscolo, sconto di riga) in `flussi/preventivo-net.md`.

Testata: data · **numero e stato si cambiano solo con la funzione `Numera`** · cliente
(da anagrafica o digitato per i nuovi) · alla c.a. · descrizione · **testo iniziale** e
**testo finale** (anche da **glossario**) · validità · pagamento · **note interne, mai
stampate** · file allegati.

Righe: i tipi soliti più **Totale di sezione** (max **99**) e **Salto pagina**.

**Le sezioni del preventivo si trasferiscono alla commessa** che ne deriva, che risulta
divisa nelle stesse «sottocommesse».

**Importazione da altri preventivi**: si cerca, si selezionano le righe, si importa.

### Costo, Fabbisogno, Ricalcolo

- **Costo** — margine e ricarico, in valore e percentuale, in **due sezioni**: la prima
  sui costi di riga, la seconda su un **listino di riferimento** scelto liberamente. Se
  il listino non ha il prezzo di un articolo si ripiega sul **listino base**.
- **Fabbisogno** — tutto il materiale necessario, raggruppato per codice, con le
  disponibilità sui depositi periferici espandibili con `+`.
- **Ricalcolo** — per categoria di articoli (semplici, manuali, fuori inventario, distinte
  analitiche, distinte a forfait), con ricarico/sconto (**negativo = sconto**) o
  ricalcolando **da un listino di acquisto o vendita** (fino a **due listini in ordine
  preferenziale**, poi il base), e arrotondamento a intero, decimo o centesimo.

  **Il ricalcolo si applica solo uscendo dalla schermata con conferma** — così si simula
  quanto si vuole. Ma la guida avverte: **rispondendo Sì i prezzi originali non si
  recuperano più**.

**Personalizzazione della stampa** (`Impostazioni → Stampa`): ogni sezione si accende o
si spegne cliccandoci — **in rilievo si stampa, ribassata e grigia no**. Si decide se
stampare intestazione, indirizzo, telefono, alla c.a., data e luogo, oggetto, testi,
**codice e descrizione articolo** (spegnendola si spengono anche le sottosezioni),
**prezzo unitario e sconto**, importo, descrizione estesa, **dettaglio della distinta**,
totali di sezione, totali generali, validità, pagamento.

---

## Commesse

**Prerequisito onesto, scritto nella guida**: senza un magazzino ben codificato le
commesse non servono a niente.

Regola di base: **una commessa = un cliente**. Più commesse sullo stesso cliente sì; più
clienti sulla stessa commessa no.

### La manodopera è un articolo

Non c'è un campo «ore». Le ore si codificano come **articoli fuori inventario** che
rispettano **tre condizioni**:

1. tipologia **Fuori inventario**
2. la parola **«Manodopera»** (o «Mano d'opera») **nella descrizione**
3. unità di misura in **Ore** o **Minuti** (i minuti vengono convertiti: 30 min → 0,5 ore)

Se ne possono codificare quanti se ne vuole, per distinguere costi e prezzi diversi.

⚠️ Nel rapportino c'è anche un campo **`Ore effettive`**, ma **non entra nel conteggio**:
per le ore fa fede **solo la manodopera nelle righe di dettaglio**. `Ore effettive` serve
**esclusivamente ad Analytics**.

### Testata

Obbligatori **data di apertura** e **cliente**. Poi: **numero** (progressivo da `Numera`;
forzandolo, Unicò **impedisce** un numero già usato nell'anno e **avvisa** — senza
bloccare — sulle incongruenze di cronologia), data prevista di chiusura, **valore stimato**
(indicatore, **slegato** da preventivo e consuntivo), **rif. cantiere**, preventivi
collegati (sola lettura), tipologia, descrizione, note, **edificio** (la stessa
classificazione della Dichiarazione di Conformità).

### Le righe, e i due colori che raccontano tutto

- **Riga di commessa** — sfondo **bianco**, è il preventivato. Ha `Q.tà commessa` e
  `Q.tà consegnata`, quest'ultima aggiornata dai documenti collegati.
- **Riga in economia** — sfondo **azzurro**: consuntivo **non previsto**, oppure
  **l'eccedenza** rispetto al preventivato.

**La quantità consegnata non può mai superare quella di commessa**: l'eccesso genera da
sé una riga in economia. E una riga finisce in economia anche solo perché **al momento
dell'inserimento non è stata collegata** alla riga di commessa — si rimedia dopo con la
funzione **`Associa`** (più righe documento possono puntare a una sola riga di commessa).

La **Sezione** è un numero intero che divide la commessa (1 = riscaldamento, 2 = idrico…),
con una **`Legenda`** testuale opzionale per le stampe.

**Articoli a distinta**, due comportamenti: **a forfait** — i componenti non mostrano
prezzi, il prezzo di vendita è quello deciso, ma **il costo resta la somma dei
componenti**; **analitica** — anche la vendita è la somma, e **la cella del prezzo
unitario si blocca**.

**Importa Preventivo**: solo preventivi **dello stesso cliente** e **solo in stato
`Presentato` o `Accettato`**.

### I documenti che muovono la commessa

Si collega valorizzando il campo **`Commessa`** in testata.

- **Documenti che generano movimenti di magazzino** → aggiornano il **consegnato**
- **Documenti solo contabili** (fattura emessa) → aggiornano solo gli **acconti**
  (fatturazione «a corpo»)
- **Fattura accompagnatoria** → fa **entrambe** le cose

**Rapportino di commessa**: prima il riferimento alla commessa, poi data, tecnico,
descrizione, note, `Inserisci`, e infine **prelievo merce + causale di trasporto** —
**vanno indicati anche se il rapportino contiene solo manodopera**, pur non avendo
effetto. Poi si accende `Dettagli`. Il pulsante **`Commessa`** su una riga apre il
dettaglio e collega la riga alla riga di commessa giusta.

### Nota di consegna — la scorciatoia e il suo rischio

Serve al caso normale: materiale comprato dal grossista e portato **direttamente in
cantiere**. Contabilmente il giro è neutro (entra ed esce), e la nota di consegna
**consuntiva sulla commessa senza generare alcun movimento di magazzino**, evitando
carico + trasferimento + scarico.

⚠️ **Se lo stesso materiale finisce anche nei rapportini giornalieri, il consuntivo
raddoppia.** Non è un bug: è una procedura che va decisa e insegnata al personale, una
volta sola, e poi rispettata.

### Controllo commessa — le funzioni di calcolo

- **Analisi** — su previsione o su consegnato, per sezione o complessiva. Divide per
  **articoli semplici, distinte a forfait, articoli manuali, voci fuori inventario e
  manodopera**, e per ognuna dà **valore di commessa, costo, differenza, margine %
  (costo/valore) e ricarico % (valore/costo)**. Si può **esplodere per gruppo
  merceologico**, e una seconda sezione rifà gli stessi conti **usando un listino** invece
  dei costi di riga — è il modo per capire da dove viene uno scostamento.
- **Fabbisogno** — per codice: previsto, consegnato, **residuo**, impegnato, giacenza
  totale, espandibile per deposito.
- **Totali** — materiale di commessa, consegnato, **in economia**, acconti; i segni si
  cambiano cliccando ripetutamente sui pulsanti (`+`, `−`, neutro).
- **Ricalcola commessa** — massivo, per tipo di riga (tutte / solo commessa / solo
  economia / solo selezionate) e per categoria di articoli. Serve quando i costi si
  muovono all'improvviso, o per simulare l'effetto di uno sconto o di un cambio
  fornitore. **Le modifiche si applicano solo confermando all'uscita.**

### I due metodi

- **A consuntivo** — la commessa è un contenitore: si collegano DDT, rapportini e note di
  consegna e si legge il consuntivo. Nessuna riga di preventivo necessaria.
- **A preventivo** — si parte da un preventivo (importato o inserito a mano) e si misura
  **lo scostamento**.

Limite dichiarato: Unicò è pensato per **commesse private e di piccola dimensione**, non
per grandi lavori in subappalto o con committenti pubblici. È una scelta, non una
mancanza.
