# Adempimenti — catasti, DiCo, ricevute fiscali, comunicazioni

Quello che esce da Unicò e va a un ente. **Tutto quanto sta qui è irreversibile o quasi**:
un invio telematico non si ritira, una comunicazione all'Agenzia va corretta con un invio
sostitutivo. **La skill non lo esegue mai**, nemmeno su richiesta e nemmeno su una sandbox: il guardrail lo
vieta (`VERSO_ESTERNO`). Prepara, mostra, e l'invio lo fa una persona.

---

## Invio telematico ai catasti energetici regionali

La **distinta** è un raccoglitore di RCEE da mandare al catasto.

### 1. Creare la distinta

Dalla **ricerca RCEE**: si cercano e selezionano i rapporti, poi ⋮ → **`distinta`**. Il
numero è proposto progressivo. Elementi già in un'altra distinta **vengono trasferiti in
quella nuova**; in alternativa si possono **rimuovere** da una distinta esistente.

I catasti non si comportano tutti uguale: alcuni accettano **tipo 1 e 2 insieme**, altri
vogliono **un tipo solo**, altri **distinte separate per ente territoriale**. Quindi a
volte servono più distinte, ed è il catasto a dettare come.

### 2. Wizard `Assistenza → Invio telematico`

1. **CAT** (solo aziende multiCAT con P.IVA diverse). La stella porta in cima i preferiti,
   e agli avvii successivi **mostra solo quelli**.
2. **Impostazioni** — cambiano per ente: **API key** per gli invii via web service, oppure
   il **codice manutentore**.
3. **Selezione distinta** — vengono mostrate **solo le distinte del tipo dell'ente scelto**.
4. **Controllo** — gli RCEE con problemi in rosso; espandendo la riga si legge cosa:
   **errori bloccanti in rosso**, **errori non bloccanti in giallo** (passano lo stesso, ma
   andrebbero sistemati).

   Tre pulsanti a destra: **aggiorna validazioni** · **apri la scheda impianto**
   sull'intervento che contiene l'RCEE · **apri l'intervento nella sezione RCEE**, con gli
   errori evidenziati nell'anteprima. Man mano che si correggono, spariscono dalla lista.

5. **Invio o esportazione** — per i catasti con **web service** il tasto è `invio`; per
   tutti gli altri diventa **`esporta`**, che scarica un **CSV** da caricare a mano sul
   sito del catasto.

### Cosa è supportato oggi

Web service: **CIRCE** e **CRITER**. Disponibili anche **SIERT**, **CURMIT**, **UCIT**,
**CIT-CAL** e l'invio delle **province di L'Aquila e Pescara**. Gli altri **sono in attesa
che il catasto stesso si aggiorni**.

> **CRITER c'è** — è la risposta a una domanda che era rimasta aperta. Per l'Emilia-Romagna
> l'invio è via web service, quindi parte da dentro Unicò.

Per **CIRCE e CRITER** si può inviare **direttamente dalla scheda intervento**: ⋮ →
`Invia tutti RCEE` o `Invia questo RCEE`. Da lì si può anche **escludere un RCEE
dall'invio** (escluso, **non parte nemmeno se è dentro una distinta**) o eliminarlo.

### Il pezzo che sta a monte

- **Tabella Comuni** → **Ente** e **tipo di rapporto di controllo** (nazionale o regionale)
- **Tabella Enti** → i contenitori da associare ai comuni, per i catasti che vogliono
  l'invio diviso per zona
- **Tabella Tecnici** → **codice manutentore** per ente: senza, l'invio non parte
- **Anagrafica del Terzo Responsabile** → **codice CURIT** (Lombardia)
- **Impostazioni supervisore** → **Viario** lombardo, che può essere `Suggerimento` o
  **`Bloccante`** sugli indirizzi delle schede impianto

---

## F-Gas

Vedi `assistenza.md` per la compilazione. Quel che conta qui: **cinque tabelle vanno
predisposte prima** (anagrafiche azienda, tecnici, scheda anagrafica dell'operatore,
fluidi F-Gas, operazioni di manutenzione), altrimenti l'invio telematico non parte.
Il modulo fa anche **l'allineamento dei codici identificativi degli apparecchi**.

---

## Dichiarazione di Conformità — EC744

**Non è software Futura**: è **EC744 di Edilclima**, integrato in Unicò, con il modulo per
il **disegno degli schemi di impianto** — un piccolo CAD con librerie a norma UNI. Ha un
**help in linea proprio**, dentro il modulo.

Conseguenza pratica: le domande sulla DiCo si risolvono lì dentro, non nella guida Unicò.
Quello che Unicò fornisce sono i dati: **dati conformità della scheda articolo** (finiscono
nell'**allegato materiali**) e il campo **Edificio** della commessa, che ricalca la
classificazione della DiCo.

---

## Ricevute fiscali

Tre modi, e non sono equivalenti:

- **Da intervento** — emesse registrando l'intervento eseguito
- **A saldo** — se la ricevuta dell'intervento non era stata incassata. **Non ha righe di
  dettaglio**, solo l'importo pagato; in stampa si può però riportare come **testo** il
  riepilogo delle righe della ricevuta «padre», che **può essere solo una ricevuta emessa
  in un intervento di assistenza**
- **Al banco** — **sempre considerata interamente incassata**, per costruzione: non
  ammette incasso parziale. Serve a tenere puliti i riepiloghi dei corrispettivi. Per il
  pagamento differito si usano DDT o fatture accompagnatorie.

Nella **tabella Tipologie documenti** la sezione Corrispettivi chiede appunto di scegliere
fra **«ricevuta fiscale al banco»** e **«a saldo intervento»**.

---

## Spesometro / Comunicazione polivalente

Unicò **precompila** la comunicazione **in forma analitica** dai dati di prima nota, la
lascia correggere, e genera il file telematico conforme.

`Elabora` sull'anno scelto produce i quadri:

| Quadro | Contenuto | Come |
|---|---|---|
| **FE** | vendite | precompilato dalle fatture di vendita |
| **FR** | acquisti | precompilato dalle fatture di acquisto |
| **NE** | note di variazione emesse | precompilato |
| **NR** | note di variazione ricevute | precompilato |
| **DF** | operazioni senza fattura | **manuale** |
| **FN** | soggetti non residenti | **manuale** |
| **SE** | acquisti servizi da non residenti | **manuale** |

Poi `Salva`, e da lì si abilita `Aggiorna` per le integrazioni. Si annulla con
**`Deregistra`** dal menù Opzioni.

Cose da sapere prima di fidarsi del precompilato:

- **L'unico controllo automatico è sul tipo di operazione IVA.** Gli importi con codice
  **«escluso IVA» non vengono riepilogati**; se un documento ha *solo* importi esclusi,
  compare con imponibile e imposta a **0** e **va escluso a mano**.
- **Gli importi vengono troncati**, senza decimali.
- **Le fatture cointestate producono una riga sola**, con il nominativo principale: le
  righe per gli altri cointestatari **si aggiungono a mano**.
- I campi **Autofattura**, **documento riepilogativo** e **IVA non esposta** sono
  precompilati sempre a **«No»**: li corregge il compilatore.
- Codice fiscale e partita IVA sono **alternativi e obbligatori**; i campi in **rosso**
  sono obbligatori e finché non sono pieni **i pulsanti restano spenti**.
- Nelle note di variazione **l'imponibile è sempre obbligatorio, l'imposta no** — perché
  ci sono casi (nota emessa oltre l'anno) in cui non c'è.

Prima di generare il file va compilata la tabella **`dati invio telematico`** con i dati
di chi trasmette: attenzione a **codice attività ATECO 2007** e **e-mail**, entrambi
**obbligatori**.

`Utilità → creazione del file per l'invio telematico clienti-fornitori` (i campi
**protocolli** si compilano **solo** per invio sostitutivo o annullamento) → `crea`.
Se mancano dati esce un **file di testo con gli errori**. Il file prodotto sta in
`Spesometro → Azienda1` con estensione **`.nsp`** e si scarica da
`Utilità → esplora risorse`.

---

## Il portale

`https://portale.unico3.cloud/` (per l'azienda: `start.dcN.unico3.cloud`). Contiene: **App**
(le applicazioni), **SMS** (stato del sistema di messaggistica), **Contatti**,
**Unicò Chef** (i video formativi), **Shop**, **Supporto remoto**, **Help on-line** — che
è la guida da cui viene tutto questo — e il **Blog FuturaSI** con aggiornamenti di prodotto
e normativi.

**Area Applicazioni**, due nature:
- **terminalizzate** — modalità **Windows** (serve scaricare un client la prima volta) o
  **Browser** (Chrome, Firefox, Edge). *La RemoteApp Windows da qui non parte: qui
  esiste solo il web.*
- **web** — oggi **Geolocation**, **Planner** e **Unicò Web**. Il «doppio binario» è
  dichiarato: le applicazioni Windows verranno riscritte progressivamente.

Le raccomandazioni sulle password sono esplicite, e una vale la pena ricordarla:
**quando un operatore viene sostituito la password non si passa al successivo — si chiede
il reset all'assistenza**.

---

## Menù iniziale (terminale)

Quattro cartelle — **Amministrazione, Magazzino, Installazione, Assistenza** — con i
programmi sopra e le **estrazioni dati** sotto. Agenda e Memo stanno in alto a destra.
Il pannello **Processi attivi** mostra cosa sta girando e permette la **chiusura forzata**
con la ✕.

**Ricerca rapida full-text**: si sceglie il tipo (Impianto, Anagrafica, Articolo) e si
digita in **qualsiasi ordine, anche parziale**. Chiavi:

- **Impianto** — codice, nominativo, comune, indirizzo, **codice portale**
- **Articolo** — qualunque codice (interno, barre, fornitore), descrizione, marca
- **Anagrafica** — codice, nominativo, comune, indirizzo, codice fiscale / P.IVA

Nel **web** l'equivalente è la barra in alto a destra, che si raggiunge da qualsiasi punto
col tasto **`\`** e cerca su impianti, articoli, voci di catalogo, anagrafiche **e perfino
i nomi delle tabelle**, mostrando **i primi 5 risultati per categoria**.

---

## Importazione massiva modelli

`Utilità` della tabella modelli → **`importa modelli`** → si sceglie la **marca**
(disponibile secondo le abilitazioni del CAT: **Baxi, Westen, Immergas** per GT e
bruciatori; **Immergas** per gruppi frigo e componenti).

Unicò preseleziona i modelli **già presenti con codice Unicò corrispondente**, anche se
hanno un nome diverso. Opzioni: **sovrascrivi rendimento**, **allinea descrizione Unicò**,
filtro per codice o nome, seleziona/deseleziona tutto.

Se un modello in tabella **non ha il codice prodotto** (o ce l'ha sbagliato) non viene
accoppiato: si sceglie a mano nella colonna **`Modello Unicò`**. **Lasciando la colonna
vuota viene creato un modello nuovo.**

La freccia accanto alla selezione apre l'anteprima della sovrascrittura: **in rosso
barrato il vecchio, in verde il nuovo**. Vale la pena guardarla, perché
**l'importazione è irreversibile**.

Ricordare il seguito: aggiornato il modello, sulle schede impianto **resta il codice
vecchio** finché non si usa **`Allinea codice prodotto`** dalla selezione multipla.
