# Impostazioni, utenti, licenze

**Zona rossa quasi per intero.** Qui si cambia il comportamento del programma, spesso
**per tutti**, e si decide chi può fare cosa. Non ci si scrive senza richiesta esplicita
del responsabile, **nemmeno su una sandbox**.

La regola che separa il rischio: **le impostazioni normali sono per singolo utente**
(ogni postazione può averle diverse); **quelle della cartella Supervisore sono globali**.

---

## Utenti

**Username desktop**: `UxxxxNN` — `U` fisso, `xxxx` codice cliente Futura, `NN`
progressivo. l'azienda è **`U<tenant>01`**, quindi **il primo utente**, che per default è il
**Supervisore**.

Due livelli: **Base** e **Supervisore**. Il supervisore è per default `Uxxxx01`, ma si
può spostare o assegnare a più utenti (sconsigliato).

**Username mobile**: `MxxxxNN`. **Un account mobile nasce da solo per ogni tecnico in
tabella Tecnici**, di default in licenza **Lite**.

### Cosa si configura per un utente desktop

**Moduli abilitati** — si accende o si spegne ogni modulo. È così che si dà la Prima Nota
solo a chi tiene la contabilità. *Alcuni moduli sono spenti perché manca la licenza, non
perché qualcuno li ha tolti.*

- **Abilita come supervisore**
- **Abilita centralino** (se c'è l'opzione)
- **Disattiva invio SMS massivo** — resta possibile il singolo SMS
- **Imposta limite esportazione dati** — una **soglia di avviso** e un **massimo**.
  Superata la soglia **parte una mail al Supervisore**, se il suo indirizzo è compilato.
- **Imposta limite stampa** — idem per le stampe
- **Password**, e-mail, cellulare

  ⚠️ Distinzione che conta: **la password si imposta a livello di utente Unicò**, mentre
  quella di accesso al sistema **Net** si può **solo resettare su richiesta esplicita
  all'assistenza**.

**Il limite di esportazione è la cosa più rilevante per me**: un'estrazione grande può
far scattare un avviso al supervisore. Se un export non esce, prima di cercare bug si
guarda lì.

### Configurazione mobile — dal web, tabella Tecnici → tab «App mobile»

Si assegna la **licenza** (controllata sul numero di licenze libere) e poi si accende o
spegne **funzione per funzione**. Le più significative:

**Assistenza** — aggiornamento dati anagrafica · aggiornamento dati installato ·
compilazione libretto · inserimento intervento
**Documenti** — emissione ricevuta fiscale · rapportino · fattura immediata · *usa sconto
abituale in anagrafica*
**Impegni** — ricerca generica (qualunque impianto) *oppure* **ricerca mirata** (solo per
codice catastale o matricola): normalmente **si usa una o l'altra**
**Magazzino** — cerca articoli · trasferimento a furgone
**Magbar** — movimenti · rettifiche · visualizzazione prezzi di acquisto
**SMART** — moduli personalizzati · upload file · download esplosi · **firma elettronica
semplice** · visualizzazione allegati · invio documenti via e-mail · analizzatori di
combustione · **inserimento attività per l'ufficio (CRM)** · codici Portal · report
giornalieri · **georeferenziazione GPS** · **stipula/rinnovo contratti** · operazioni
F-Gas · segnala interventi di ritorno · **programma data e ora delle RdI auto-inserite** ·
validazioni personalizzate · cerca anagrafiche · orari/tecnici aggiuntivi · **modifica
tag** (solo quelli marcati «inseribili da mobile») · **forza invio dati per procedere** ·
**blocca ora chiusura nel futuro**

**Restrizioni** — blocca scelta furgone per lo scarico · **blocca prezzo a listino** ·
blocca tipo pagamento in fattura · limita la vista alla giornata odierna · **firma un
documento alla volta** · **non visualizzare il saldo impianto** · mostra scadenze aperte
delle fatture collegate · **forza «segue fattura» sui rapportini** · **disabilita logout
rapido** (svuota la cache al login) · **azzera gli importi nello storico interventi**

**Opzioni di stampa** — mostrare o no importi (rapportini e ricevute) e codici (solo
rapportini).

### Bloccare un tecnico — due comportamenti diversi

| Dove | Cosa fa |
|---|---|
| **NET**, spunta `Bloccato` | **impedisce solo i nuovi login**. ⚠️ **Le sessioni mobile attive NON vengono disconnesse.** Per staccare davvero qualcuno: **cambiare la password e fare login da un altro telefono.** |
| **Web**, ⋮ → `Disabilita utente` | **disconnette la sessione attiva** e blocca il login, con un banner e il tasto `riattiva` |
| **Web**, ⋮ → `Disconnetti` | stacca la sessione e obbliga a rifare login, **senza** disabilitare |

Se serve togliere l'accesso a qualcuno **subito**, la spunta del NET non basta.

⋮ dà anche **`Reimposta password`** e **`Copia impostazioni`** (copia tutto tranne
username e password su altri tecnici; **serve un numero di licenze libere congruo**).

---

## Impostazioni — Supervisore (globali)

**Assistenza**
- **Numera chiamate** — ogni RdI prende un numero univoco progressivo
- **Disabilita eliminazione Attività/RDI** — senza privilegi di supervisore non si
  cancella più niente. *È il modo giusto di proteggere lo storico.*
- **Numera interventi**
- **Contratti attivi multipli** — permette più di un contratto attivo sullo stesso impianto
- **Viario** — solo Lombardia: controllo degli indirizzi contro il viario del catasto
  **CURIT**, in tre modi: `Disabilitato`, `Suggerimento`, **`Bloccante`** (non si inserisce
  un indirizzo non compatibile)
- **Rapporti di controllo → forza stagione termica**

**Mobile**
- **Abilita gestione nuovi rapporti**
- **Visualizza solo impegni odierni** — limita la consultazione dell'app alla giornata

**Agenda SMART** — intervallo in minuti · settimana lavorativa

---

## Impostazioni — per utente

**Generali** — per articoli manuali, IVA e UdM proposte **fisse** o **le ultime usate**
(vale come schema per moltissime opzioni) · **ricerca rapida** per articoli e voci di
contratto · CAT proposto (multiCAT) · centralino: numero interno, durata dell'alert,
modalità click-to-call.

**Unicò** — quale tab mettere in primo piano nel menù iniziale · risoluzione monitor e
dimensione delle finestre di terminalizzazione.

**Amministrazione**
- valori proposti per tipo soggetto e tipo documento
- **modalità bozza** (documenti emessi, ricevuti, ordini, liste materiale, movimenti):
  velocizza l'inserimento, ma **richiede un `Ridisegno` finale**
- **riporta lo scadenziario nelle note del documento**
- **prezzo di carico calcolato** — nei documenti in ingresso: prezzo netto, oppure
  **prezzo di listino + sconto**
- **Ricezione SDI → articoli non codificati**: importarli come **articolo manuale** o
  **creare un nuovo articolo di magazzino**
- **Applica regime IVA per cassa** — attiva di default la spunta sui documenti

**Magazzino**
- marca e gruppo proposti nella scheda articolo
- **nascondi magazzini/cantieri a giacenza nulla**
- origine (`DA`) e destinazione (`A`) proposte nei movimenti
- **attiva controllo giacenza negativa** → avvisa
- **blocca inserimento** → **impedisce** i movimenti che porterebbero in negativo

  Queste due meritano attenzione: la **giacenza negativa falsa il prezzo medio ponderale**
  dell'inventario e **l'errore si trascina in avanti**. Il blocco è la difesa vera.

**Assistenza**
- tipologia impianto proposta · **quale cartella della scheda impianto aprire di default**
- **controllo saldi aperti esteso** oltre al cliente anche a Occupante, Amministratore,
  Proprietario — è ciò che fa accendere la spia dei documenti su riferimenti diversi dal
  cliente
- valori proposti per operatore, interlocutore, motivo, tipologia, tecnico delle RdI
- **Programma intervento**: `Le ore` (orario preciso), `Mattino`, `Pomeriggio`,
  `Qualsiasi ora`
- **Attiva chiamata multipla** — più RdI sullo stesso impianto nella stessa giornata
- **Non proporre alcun ticket**
- **testo SMS predefinito** per l'impianto e per il tecnico
- **Riferimenti**: chi è per default il **Responsabile impianto** (occupante o
  proprietario) e chi il **destinatario della corrispondenza** (occupante, proprietario,
  amministratore, terzo responsabile, progettista, installatore, cliente).
  *Questa seconda scelta decide a chi va la mail quando si stampa con invio e-mail.*
- interventi: tecnico e tipologia proposti · **descrizione = tipologia**
- contratti: **data inizio = data stipula**
- libretto: **esporta interventi e analisi** a partire da una data

**Agenda** — giorni precedenti e successivi visualizzati · ordinamento · e le quattro
scelte del **cosa mostrare per quale data** (manutenzioni per scadenza legale o
programmata; richiami per data richiamo o inserimento; chiamate per inserimento o
intervento programmato; altri impegni per appuntamento o messaggio).

**Agenda SMART** — intervallo in minuti · finestra oraria · **cosa fa il tasto destro**:
tooltip sull'impianto **oppure menù contestuale per inserire** (la guida consiglia il
secondo) · testo mostrato in agenda · gruppo e ordinamento dei tecnici.

---

## Impostazioni nel web

`#/impostazioni/<area>/<sezione>` — tre aree: **Agenda**, **Assistenza**, **Generale**.
Più **Impostazioni Feedback**, **Impostazioni Loghi** e **Stampe**.

Vale la stessa regola: **cambiano il comportamento per tutti**, e in agenda **bisogna
premere `Salva`** (compare un avviso se restano modifiche non salvate).
