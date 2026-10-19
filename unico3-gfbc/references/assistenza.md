# Assistenza — impianto, attività, intervento, documenti

Fonte: guida ufficiale di Futura SI (sul portale Unicò, `…/doc/`, non inclusa qui) più quanto verificato dal vivo su una sandbox. **Dove le due divergono lo dico:
vince la misura.**

L'area Assistenza è il cuore del lavoro di un'azienda di assistenza. Le altre aree servono; questa è quella
in cui si sbaglia.

---

## La scheda impianto

Rotta: `#/assistenza/impianto/<id>/dettagli/<tipoInstallato>/<idInstallato>/<sezione>`.
Ci si arriva col doppio click su una riga di ricerca, o dalla barra globale.

**Struttura fissa**: testata in alto (dati di creazione + mappa), sezioni a sinistra,
contenuto a destra. All'apertura è su **Dettagli**.

Testata:
- click su un dato apre il wizard di modifica di *quel* dato (non c'è una modalità
  "modifica scheda")
- click sul **codice impianto** → cambio manuale, o lente → **assegna codice libero**
  (serve a coprire i buchi di numerazione)
- **tag impianto** sotto codice e nome: **solo versione SMART**.
- mappa navigabile a destra: le coordinate manuali **hanno priorità sull'indirizzo ma
  non lo modificano**; per azzerarle si entra in modifica indirizzo e si usa `reset`
- icona on/off verde = **dismetti/riattiva impianto**
- ⋮ = numerazioni, stampe, registro operazioni, **elimina impianto**

### Le spie, e cosa vuol dire davvero ciascun colore

Sono la diagnosi rapida dell'impianto. Grigia = nessuna segnalazione. Il *hover*
mostra la causa; il click porta nel posto giusto.

| Spia | Colori | Click porta a |
|---|---|---|
| **Prescrizioni** | rosso: un GT/GF/scambiatore ha prescrizioni | Attività |
| **Impianti collegati** | verde = è **padre**; giallo = è **figlio**. Padre e figlio insieme → vince il verde. Un impianto ha **al massimo un padre**, più figli | Dettagli → impianti collegati |
| **Scadenza manutenzioni** | rosso: **scadenza PROGRAMMATA** superata | Dettagli |
| **RdI aperte** | rossa: RdI aperta. Gialla: RdI **sospesa** o un **richiamo** | Attività |
| **Documenti scaduti/non pagati** | viola: scadenza aperta e scaduta. Rosso: documento «non fatturare» con saldo aperto, o «da fatturare» senza fattura emessa. Giallo: scadenza aperta non ancora scaduta | finestra saldi |
| **Blocco anagrafica** | rosso: un'anagrafica di un riferimento ha una **nota bloccante** | Riferimenti |
| **Libretto** | grigia: non esiste. Verde: esiste | crea / visualizza-aggiorna-elimina |

**La distinzione che conta**, e che non è ovvia: la spia manutenzioni si accende sulla
scadenza **programmata**. Se è passata la **legale**, la spia **resta spenta** e si
colora di rosso il piano di manutenzione nella sezione Dettagli. Chi guarda solo le
spie non vede le scadenze legali.

### Dettagli — l'albero dell'installato

A sinistra l'albero gerarchico (impianto → GT/GF/UI/Componenti → bruciatori dentro i
GT). Barra di ricerca rapida sopra; in alto a destra apri/chiudi tutti i rami.

Inserire un installato: si **seleziona il padre**, poi `+` rosa in basso a destra. Il
filtro dei tipi disponibili **dipende da cosa era selezionato** — a un impianto puoi
appendere GT, GF, UI, Componenti; i Bruciatori solo dentro un GT; gli Scambiatori solo
se la **tipologia impianto** li ammette. Se non sai se «Audax 6» è un GT o un GF, usa la
ricerca rapida in basso: propone il modello con accanto la categoria.

A destra, per l'installato selezionato: sostituzione, dismissione, eliminazione,
duplica; e le tab **Altri dati / Piano di manutenzione / Interventi / Storico
installato** (i GF hanno in più **F-Gas**).

Colori: manutenzione **scaduta in rosso** (fa fede la programmata), garanzia **verde se
attiva, rossa se scaduta**. Il simbolo accanto al nome di un installato indica che **ne
ha sostituito un altro** — c'è uno storico.

### Contratti

Elenco a sinistra, dettaglio + copertura + rate + documenti a destra. Il pallino
accanto alla voce di menù conta gli scaduti/attivi.

Creazione: `+` → tipologia, numero, data stipula (obbligatori) → `avanti` → **copertura**:
l'intero impianto o un installato specifico.

Colori dei contratti, che non sono decorativi:

| Colore | Significato |
|---|---|
| **Bianco** | storicizzato |
| **Verde** | attivo (per gli avanzati: fine copertura e fine tacito rinnovo non scadute) |
| **Arancione** | fine copertura **scaduta** ma **tacito rinnovo ancora valido** |
| **Rosso** | scaduto |
| **Giallo** | attivo ma **oggi cade nel periodo di sospensione** |
| **Blu** | è solo quello selezionato |

Azioni a destra: storicizza, rinnova rate, prolunga / applica tacito rinnovo, elimina.

**Rate e copertura dal web si inseriscono** (misurato su A1 08/10/2026, smentita la guida
che le dava in sola lettura); su alcuni contratti la testata torna 500 e si corregge dal
NET. Procedura e regole definite dall'azienda: `flussi/contratti.md`. La fatturazione
automatica delle rate è funzione **SMART**, e un contratto avanzato può coprire **più
impianti dello stesso cliente**.

### Riferimenti, Altri dati, Note, File, Vincoli

- **Riferimenti**: a sinistra i riferimenti con sotto i ruoli e le figure; a destra il
  dettaglio di ciò che è selezionato — elimina, modifica, **sostituisci**, **dismetti**.
- **Altri dati**: catasto, date installazione e costruzione, dati energia, certificati,
  e gli **orari di attivazione impianto**.
- **Note**, quattro tipi, e la differenza è *dove finiscono stampate*:
  - **Principale** → stampata **sempre** sulla scheda RdI; visibile e aggiornabile da mobile
  - **Storico** → solo sulla scheda RdI «completa»
  - **Riservato** → **mai stampata**
  - **Fuori norma** → non conformità dell'impianto; visibile e aggiornabile da mobile

  I pallini colorati accanto a NOTE dicono quali tipi esistono.
- **File**: tutto ciò che è legato all'impianto, compreso quanto caricato da mobile
  (foto). Drag&drop, anteprima, stampa, download.
- **Vincoli** (SMART): **di tecnico** — «solo questi» oppure «tutti tranne questi», con
  la casella per **ignorare le competenze** della tabella Tecnici; **di orario** — su
  conferma / su appuntamento / libero, con fasce `Sempre` | `tranne` | `solo in`.
  I vincoli si vedono in agenda in fase di programmazione.

### Inserimento nuovo impianto — wizard 5 passi

Assistenza → `Nuovo impianto`. 1) dati anagrafica (`inserisci` a mano o `scegli` da
rubrica; persona fisica/giuridica; casella *ditta indiv./profess.* che apre categoria
SDI, denominazione, P.IVA, PEC) → 2) **ruoli** → 3) **figure** dei ruoli (facoltative,
modificabili dopo) → 4) dati impianto (tipologia e combustibile obbligatori; la casella
*origine nominativo impianto* copia nominativo e telefoni dall'anagrafica) → 5)
indirizzo, con coordinate selezionabili a mano sulla mappa.

---

## Attività — il CRM

Il dettaglio del modello (ticket, esiti, catena) sta in **`crm-ticket.md`**. Qui quello
che aggiunge la guida ufficiale.

**I due badge** sulla voce Attività: chiave inglese = **RdI aperte non sospese**;
cuffia = **attività ufficio e richiami da evadere**. Il badge **diventa rosso quando le
attività ufficio sono scadute**.

Elenco ticket a sinistra: **bianchi i chiusi, viola gli aperti**. Uno switch toglie il
raggruppamento per ticket; si può filtrare per sole RdI / sole attività ufficio / soli
interventi, e in quella vista **il rosso segna i non evasi**.

In alto a sinistra del dettaglio: **elimina il ticket** (solo se ancora aperto) e, per
una RdI, **vedi in agenda**. A destra: **evadi** e **modifica**.

### Come si evade una RdI — come si evade, in pratica

Dal ticket, l'icona di evasione apre la finestra di **evasione richiesta di intervento**,
che contiene la casella **`inserisci intervento`**. Selezionandola e andando avanti —
**dopo aver scelto un esito**, che è obbligatorio — il flusso prosegue **nello stesso
wizard**: dati intervento → tecnici/orari aggiuntivi → operazioni di manutenzione →
e, **se l'esito lo prevede**, una nuova attività ufficio **con lo stesso numero di ticket**.

Questo corregge quanto avevo scritto operando: dicevo «creare l'intervento non evade la
RdI». È vero **se l'intervento lo crei dalla scheda impianto** (`+` → nuovo intervento
eseguito): quello è un intervento slegato, e infatti non entra nel ticket. La strada
giusta è **partire dalla RdI e evaderla**, ed è lì che una conferma chiude la richiesta
e apre l'intervento.

### Wizard RdI — tre passi, e cosa c'è dentro davvero

1. **Dati**: operatore, ticket (obbligatorio), tipologia, motivo.
2. **Operazioni di manutenzione**: ordinarie e straordinarie. Le durate impostate nella
   tabella operazioni **si sommano** e propongono la **durata stimata**; la freccia la
   conferma (resta modificabile al passo dopo).
3. **Pianificazione**: orario e durata anche **trascinando sulla mini-agenda**. Sulla
   mini-agenda si vedono i **vincoli** (barre rosse: orario; area intera barrata:
   competenze tecnico) e in **grigio** gli orari in cui il tecnico non lavora o è in pausa.

Le quattro caselle della pianificazione:
- **blocca cambio tecnico** — impedisce lo spostamento a un altro tecnico da agenda
- **blocca cambio orario** — idem per l'orario
- **avvisare il cliente** — mette in agenda un banner con l'icona del telefono: *promemoria
  di chiamare il cliente*. **Non manda niente da solo** — è un promemoria all'ufficio.
- **non visibile da mobile** — la RdI non compare al tecnico sull'app

**Bacchetta magica**: apre una ricerca che propone le **migliori combinazioni
tecnico/data/orario in base ai costi**.

### Aiutanti, orari aggiuntivi, squadre

Casella `aiutanti/orari aggiuntivi` → aggiunge **un passo** al wizard.

Il tecnico della pianificazione è il **principale** (caposquadra). **I vincoli di orario
e competenza si controllano solo su di lui**: sugli aiutanti si verifica **soltanto la
disponibilità** — se hanno un impegno che si sovrappone, errore bloccante.

Se l'orario dell'aiutante coincide con quello del principale compare un **lucchetto**
nella colonna *sincronizza*: cambiando l'orario del principale (anche col drag&drop in
agenda) **si spostano anche i sincronizzati**. Gli altri no, si aggiornano a mano.

**Squadre tecnici**: scelta una squadra, si spunta da sé `aiutanti/orari aggiuntivi`, il
principale diventa il caposquadra e gli aiutanti vengono precaricati sincronizzati.
**La squadra non viene salvata sulla RdI** — è solo un modo veloce di compilare. Quindi
si può modificare liberamente dopo averla scelta, e **toccare la tabella Squadre non
cambia nulla sulle RdI già compilate**.

### RdI multiple e altri impegni — solo da agenda

Tasto destro su un punto vuoto dell'agenda: **nuova RdI**, **crea richieste multiple**,
**altri impegni**.

- **RdI da agenda**: come dalla scheda impianto, ma va scelto anche l'impianto. Gli
  impianti con collegamenti hanno un'icona che ne mostra padri e figli **senza entrare
  nella scheda**.
- **RdI multiple**: ricorrenza settimanale o mensile. **La mensile non è il giorno del
  mese ma il giorno della settimana**: dal terzo mercoledì nascono terzi mercoledì, non
  giorni 20. «Per un totale di X occorrenze» **include la prima**. Tre avvertenze vere:
  può metterci parecchio; le RdI generate sono **indipendenti**, si cancellano e
  modificano una per una; **non guarda i festivi**, quindi genera anche a Ferragosto.
- **Altri impegni**: ferie, corsi, tutto ciò che non è intervento. Possono durare più
  giorni e occupare più tecnici. I sottotipi si personalizzano nella tabella
  `sottotipi altro impegno`.

---

## Scheda intervento

Si apre col doppio click sull'intervento o da ⋮ → `apri intervento`, **in una tab nuova**.

Testata: numero intervento, codice e nome impianto (con tasto per riaprire la scheda),
data/ora/durata, tecnico, e **l'icona della sessione mobile** — rossa col lucchetto
aperto = sessione **aperta**, verde chiusa = **chiusa**. Si apre e chiude da qui.
⋮ → stampe (non attive) ed **elimina intervento**, irreversibile.

Dati principali: CAT, tipologia, riferimento RdI, orari/tecnici aggiuntivi. Per le
tipologie impianto con `riscaldamento complesso > 35 kW` compare il **numero di rapporto
di controllo CT**.

**Trappola sugli orari aggiuntivi**: cambiando l'orario dell'intervento cambiano **solo**
gli aggiuntivi che avevano **stessa data e stesso orario**. Gli altri restano dov'erano.

Note libere: 4000 caratteri. **Ritorno su intervento**: da spuntare quando il tecnico è
tornato per un problema causato da un intervento precedente (che si seleziona).

**Operazioni di manutenzione eseguite** (a destra): le date sono modificabili **solo
sull'operazione più recente in ordine cronologico**. Togliere la spunta a una non più
recente — sconsigliato — cancella i dati di quella ma **non tocca la più recente**, che
resta il riferimento per il piano di manutenzione.

### Validazioni (SMART)

Sono il controllo di reparto: commerciale, amministrazione ecc. spuntano che
l'intervento è a posto. Compaiono **solo se** la tipologia intervento prevede almeno
una voce (tabella *voci di validazione intervento*) **e la sessione mobile è chiusa**.
Sfondo **arancione** finché mancano, **verde** quando sono tutte fatte. Ogni voce accetta
una nota breve.

Non è solo un promemoria: nel terminale servono a **filtrare la fatturazione massiva**
(solo documenti interamente validati) e la **creazione della distinta per invio
telematico** (RCEE validati, anche una singola validazione specifica).

### Collaudi

La sezione compare solo per le tipologie intervento con `aggiorna collaudo`. Propone gli
installati **senza data di collaudo**; `registra` chiede tecnico, numero documento,
importo, garanzia, e i dati finiscono **nella sezione «messa in funzione» dell'installato**
sulla scheda impianto.

### Anomalie (personalizzazione)

I controlli che l'app mobile fa prima dell'intervento — bloccanti o solo avvisi (SDI
mancante, e-mail responsabile mancante) — possono essere **ribaltati in ufficio**. La
sezione «anomalie» con sfondo rosso e pallino numerato ha due pulsanti: **corretta**
(chiede una nota) e **non gestita** (chiede il motivo). Dopo: sfondo **bianco** se
gestita, **grigio** se ignorata; la freccetta le riapre.

---

## Documenti di intervento

Il web **crea, modifica e cancella** rapportini, ricevute fiscali e «altro». Le
**fatture sono in sola lettura**.

Creazione: `+` accanto alla sezione → tipologia → testata precompilata con
- **data** obbligatoria, oggi di default
- **numero** proposto dalla numerazione (⚠️ zona rossa: numerare è scrivere in un registro)
- **collegato a commessa** — solo rapportini, se esistono commesse aperte e numerate per
  quel cliente
- **importa liste materiale** — righe collegate a tecnico, tipologia intervento e/o
  operazione di manutenzione. **Solo in creazione**: dopo non si può più.

Tre sezioni: **testata**, **dettagli**, **incassi/pagamenti**.

**Dettagli**: righe di tipo *articolo*, *articolo a distinta*, *articolo manuale*, *riga
di testo*. La casella **sostituzione** apre una seconda pagina per i dati della
sostituzione. La casella **nascondi in stampa/fattura elettronica** azzera gli importi e
tinge la riga di grigio.

Selezione multipla: **CTRL** per righe sparse, **SHIFT** per un intervallo. Poi cancella
in blocco o apri la **modifica a blocchi**.

Menù **utilità** (⋮), e qui ci sono cose che vanno maneggiate con attenzione:
- **Modifica a blocchi** — cambia massivamente sconto, IVA, nascondi in stampa…
- **Forza/rimuovi stato fatturato** — solo se il rapportino è «segue fattura». È una
  forzatura di stato contabile: **non si fa senza richiesta esplicita**.
- **Crea lista materiale** dalle righe / **Importa da lista materiale**
- **Elimina documento** — «definitivamente ed in maniera irreversibile». Zona rossa.

---

## RCEE

Dalla sezione RCEE dell'intervento, `+` → scegli l'installato → una delle tre partenze:

- **Inizia da positivo** — precompilato con esiti positivi
- **Inizia da precedente** — copia l'ultimo RCEE di quell'installato
- **Inizia da vuoto**

Il **tipo (1, 1B, 2, 3) lo sceglie Unicò** in base a **regione dell'installato e tipo
impianto**, e i modelli cambiano parecchio da regione a regione. Compilazione per
sezioni: dati allegato (n° bollino, n° RCEE) → A → B → … → prescrizioni.

Poi: modifica per sezione, elimina, **escludi da invio telematico** (compare un simbolo
accanto all'installato; si reinclude allo stesso modo), stampa. Un **triangolino**
accanto all'RCEE = ci sono **prescrizioni**.

**Analisi** (fumi / funzionamento / scambiatore): si inseriscono **solo dopo** aver
creato l'RCEE, dalla tab `analisi` con l'icona di modifica. Nell'analisi fumi due campi
hanno la **calcolatrice**: calcolo automatico una volta compilati gli altri.

## Operazioni F-Gas

Si inseriscono nella scheda intervento, ma **prima** vanno predisposte cinque cose,
altrimenti l'invio telematico non parte:

1. **Tabella anagrafiche azienda**: numero e identificativo F-Gas (*spesso uguali, non
   sempre*)
2. **Tabella tecnici**: codice fiscale e numero di certificazione F-Gas del tecnico
3. **Scheda anagrafica** dell'operatore: e-mail, profilo gas, codice fiscale
4. **Tabella Fluidi F-Gas**: dati corretti
5. **Tabella Operazioni di Manutenzione**: l'operazione va marcata di tipo
   **condizionamento** e poi le si assegna il **tipo di operazione F-Gas**

Nelle «operazioni eseguite» della scheda impianto le operazioni F-Gas sono **grigie se
non compilate, azzurre se compilate almeno in parte**. Si entra cliccando l'area e poi
il **fiocco di neve**. I **circuiti** dipendono dalla scheda tecnica del gruppo frigo:
pallino viola = compilato, cestino = svuota il circuito.

Per salvare: `modifica` per tornare alle operazioni di manutenzione, poi **ancora
`modifica`** per salvare davvero. Due conferme, non una.

---

## Cosa aggiunge il modulo SMART (se l'azienda lo ha)

Tag su impianto e su modello installato · vincoli orario/tecnico su impianto · vincoli e
base lavorativa del tecnico · **competenze dei tecnici** usate in programmazione ·
operazioni illimitate nel piano di manutenzione · **piano di manutenzione per macchina** ·
chiamate e interventi **per macchina** (quindi storico per componente) · operazioni
straordinarie su chiamata/intervento · **F-Gas** · viste agenda a spie / quadratoni /
timeline · vincoli visibili in agenda · **contratti avanzati** con apparecchi coperti e
rate, e **fatturazione automatica delle rate in scadenza** · **CRM**: attività d'ufficio,
gestione a **ticket**, ed **esiti che generano l'attività successiva o chiudono il ticket**.

L'ultima riga è la definizione ufficiale di ciò che avevo misurato sul campo: **un esito
può chiudere il ticket**. È lì che si chiude un ticket — non c'è un pulsante «chiudi».
