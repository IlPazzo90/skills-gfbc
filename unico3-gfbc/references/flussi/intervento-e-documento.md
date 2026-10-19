# Flusso 4 — Intervento, documento, numerazione

**Eseguito su una sandbox** (vedi
`guardrail.md` §5.1-bis). Risultato: un intervento,
un rapportino con una riga di manodopera.

> ⚠️ Autorizzato: creare, compilare, **numerare**.
> Vietato in ogni caso: **mandare al cliente** (mail/SMS) e **inviare ai catasti**.

---

## 1. Creare l'intervento

Scheda impianto → **ATTIVITÀ** → `+` → tre voci: *Nuova attività ufficio*, *Nuova
richiesta di intervento*, **`Nuovo intervento eseguito`**.

Wizard in **2 passi**.

**Passo 1 — Dati intervento.** Precompilati data, tecnico (`Non segnalato`) e CAT.
Obbligatoria la **Tipologia intervento**. Descrizione e Note hanno l'icona del
**glossario** per pescare frasi precodificate. C'è la casella **`Ritorno`**.

**Passo 2 — Operazioni di manutenzione**, ad albero:
`Impianto → GT1 → Operazioni Straordinarie / Operazioni Ordinarie`.

Spuntando *Manutenzione ordinaria* (Annuale), le tre colonne si compilano **subito, a
schermo, prima di salvare**:

| | prima | dopo la spunta |
|---|---|---|
| Ultima esecuzione | vuota | **03/09/2026** (= data intervento) |
| Scadenza legale | vuota | **03/09/2027** |
| Scadenza programmata | vuota | **03/09/2027** |

**Se non si spunta l'operazione, nessuna scadenza si muove.** L'impianto risulta visitato
e scaduto insieme. È la regola cardine, ora verificata anche in creazione da zero.

L'intervento nasce **senza ticket**: la colonna TICKET resta vuota. Il ticket lega
attività d'ufficio e richieste, **non l'esecuzione**.

## 2. Aprire la scheda intervento

Dalla riga: **⋮ → `Apri intervento`** (le altre voci: *Apri in agenda*, *Stampa*,
*Elimina*). Si apre **in una tab nuova**.

Quello che si vede, e conferma la mappa:

- badge della tipologia **colorato** col colore della tabella (per esempio sigla su fondo rosso)
- **RIFERIMENTO RDI** vuoto — l'intervento non nasce da una richiesta
- icona **sessione mobile**: verde col lucchetto chiuso = chiusa
- sezioni **FILE · FEEDBACK · RCEE · DOCUMENTO**
- riquadro arancione **DA VALIDARE** con le voci previste dalla tipologia — ad esempio
  `Controllo <ruolo>` e `Controllo Magazzino`

Le **validazioni compaiono davvero** solo quando la tipologia le prevede **e** la sessione
mobile è chiusa. Arancione = mancanti, verde = tutte fatte.

## 3. Creare il documento

`DOCUMENTO` → `+` → **`Crea documento di intervento`**.

Tipologie offerte: **Altro**, **Rapportino**, **Ricevuta fiscale**. **Le fatture non ci
sono**: nel web sono in sola lettura.

Scelta la tipologia il form si estende: **Data\*** (oggi), **Numero** (**vuoto**),
**commessa N°**, **`Importa liste materiale collegate`** — quest'ultima **funziona solo
in creazione**, dopo non si può più.

Confermato, si apre il documento con tre tab: **Testata · Dettagli · Incassi/Pagamenti**.
In testata: `Da Magazzino <nome>` (il magazzino di prelievo proposto), `Segue fattura`,
`INTESTATARIO`.

## 4. Le righe

`Dettagli` → barra a destra: **`+` · matita · cestino · duplica · ⇈ ↑ ↓ ⇊**.

Scegliendo un articolo, la riga arriva **già valorizzata**: quantità con **l'unità di
misura dell'articolo** (per la manodopera: **Ore**), prezzo dal **listino corrente**,
importo, IVA, e l'indicazione `Listino cliente` / `Listino corrente`.

Cambiando la quantità l'importo si ricalcola all'uscita dal campo: **quantità × prezzo** (es. 2,00 × 50,00 = 100,00).

⚠️ **L'aliquota IVA proposta va guardata.** Sul mio rapportino è arrivata **`N17` REVERSE
CHARGE** — corretta per un'impresa edile, **sbagliata su un cliente privato**. Viene
dall'articolo o dall'anagrafica, non da un ragionamento: la propone e basta.

⚠️ **Come è codificata la manodopera** (e perché non va confusa): in sandbox esistono
più articoli di manodopera — tutti **Fuori inventario**, come vuole la regola
delle commesse. Ma un articolo di manodopera generica è di tipo **Semplice**:
quello **movimenta il magazzino**. Il tipo è scritto in fondo a ogni riga della tendina.

⚠️ **Dopo `CONFERMA` il dialogo non si chiude: si svuota per la riga successiva.** Chi non
lo sa pensa di aver perso la riga e preme ANNULLA — che apre la conferma *«I dati inseriti
e non salvati andranno persi»*. La riga confermata **è già salvata**: si risponde `ESCI`.
E si risponde **subito**: una conferma lasciata aperta sopravvive alla navigazione.

Nel **⋮ dei dettagli**: *Modifica a blocchi* · *Crea lista materiale* · *Importa da lista
materiale* · **Elimina documento**. `Forza/rimuovi stato fatturato` compare **solo** se il
rapportino è «segue fattura».

## 5. Numerare — e qui il web non fa quello che dice la guida

**Nel web non esiste una funzione «Numera».** Non è nel ⋮ dei dettagli né in quello della
testata (che sono lo stesso menù). Il numero si scrive **a mano**:

> click sul campo **`N°`** in testata → dialogo **`Modifica dati testata`** → campo
> **Numero** libero → `MODIFICA`.

**Nessun progressivo viene proposto.** Il campo resta vuoto e accetta quello che scrivi.

### La verifica che conta: la numerazione non congela il documento

La guida ufficiale dice che dopo la numerazione il documento è congelato e va sbloccato
con un «annullamento numerazione». **Nel web non è così.** Verificato meccanicamente sul
rapportino già numerato:

```
riga riaperta in modifica → 12 campi editabili (quantità 2.00, prezzo a 4 decimali,
descrizione, sconto…), 1 solo campo bloccato: il codice articolo
```

E il codice articolo è bloccato **sempre**, anche prima di numerare.

**Due conseguenze pratiche, e nessuna è teorica:**

1. **Il numero è una responsabilità dell'operatore, non del programma.** Niente contatore,
   niente controllo di unicità visibile: **duplicati e buchi si creano senza un solo
   avviso**. Prima di numerare a mano su un'azienda vera **va guardato qual è l'ultimo
   numero usato**.
2. **Un documento numerato resta modificabile.** Comodo, e pericoloso: quello che il
   cliente ha in mano può divergere da quello che c'è a sistema, senza traccia.

La guida descrive il **terminale**, dove numerare congela ed esiste l'annullamento
numerazione con tutti i suoi effetti sui movimenti. **Nel web quella meccanica non c'è**:
non applicare al web le cautele scritte per NET, e viceversa.

---

## Controllo finale

1. L'operazione di manutenzione è stata **spuntata**? (altrimenti nessuna scadenza)
2. L'**aliquota IVA** proposta è giusta per *questo* cliente?
3. L'articolo di manodopera è **Fuori inventario** e non Semplice?
4. Il **numero** non collide con uno già usato?
5. Le **validazioni** sono ancora arancioni?
6. Nessuna conferma di uscita è rimasta aperta?

**Lasciato in sandbox:** un intervento e un rapportino (2 ore di
manodopera), non stampato, non inviato a nessuno.

---

# Contratti — eseguito

`Scheda impianto → CONTRATTI → +`. Wizard **2 passi**: *Dati generali* → *Copertura*.

**Dati generali**: `Tipologia contratto *` · **`N° *` precompilato a `0`** (anche qui
numerazione manuale) · Suffisso · `Data stipula *` · Tecnico · Inizio/Fine copertura ·
`Tacito rinnovo` + Anni + Fine tacito · Importo · Riferimento.

⚠️ **La tipologia porta con sé dei default.** Scelta una tipologia, la casella
**`Tacito rinnovo` si è spuntata da sola** con `Anni 1` e la fine tacito calcolata,
**senza che io la toccassi**. Su un contratto vero questo va guardato: il tacito rinnovo
è una clausola, non un dettaglio.

⚠️ **I campi data sono maschere, non testo libero.** Scrivendoci sopra senza selezionare
prima, il valore si è corrotto in `02/09/02/09` con l'errore rosso **«Data fine non
valida»**. Si fa **triple click** per selezionare tutto, poi si digita.

**Copertura**: albero `impianto → installati`, si spunta l'intero impianto o i singoli.
Spuntando l'impianto la copertura risulta **`TUTTI`**.

Creato: un contratto di prova, 03/09/2026 → 02/09/2027, tacito 1
anno. Badge **`CONTRATTI 1` verde** = attivo. Tre tab: **Copertura · Rate · Documenti
collegati**, con **Rate disabilitata** perché il contratto è semplice. Icone a destra:
storicizza (on/off), duplica/rinnova, elimina, stampa.

Le tipologie contratto sono configurate dall'azienda e portano default propri (tacito, durata).

*Non chiarito*: con `Anni 1` la **fine tacito** è risultata **02/09/2029**, cioè fine
copertura + 2 anni. Non so se sia la regola o un residuo del momento in cui la data fine
era invalida. **Da riverificare** prima di fidarsi del campo su un contratto vero.

---

# RCEE — l'ingresso, mappato

`Scheda intervento → RCEE → +`.

1. **`Seleziona impianto/installato`** — albero con i soli installati che ammettono un RCEE
2. **`Scegli un'azione`** — `Inizia da positivo` · `Inizia da vuoto`. *`Inizia da
   precedente` non compare se non c'è uno storico su quell'installato.*
3. Si apre **`RAPPORTO DI CONTROLLO DI EFFICIENZA ENERGETICA TIPO 1 (gruppi termici)`**

> **Il tipo lo sceglie Unicò**, da regione del comune e tipo di installato. Non si
> seleziona: compare già deciso. Per un comune dell'Emilia-Romagna → **Tipo 1**.

Prima pagina **DATI ALLEGATO**: `N° Bollino`, `N. protocollo`, e **`Tipo rapporto`** con
due voci — `EFFICIENZA ENERGETICA` e `FUNZIONALE E MANUTENZIONE`.

⚠️ **Quelle due sembrano etichette e invece sono caselle obbligatorie e mutuamente
esclusive.** Misurato:

| Stato | Messaggio |
|---|---|
| nessuna delle due | «campi non validi: IsRapportoEE, IsRapportoFM» + **«Valore obbligatorio»** |
| **entrambe** accese | stesso messaggio + **«Valore non valido»** |
| una sola | passa |

Il dialogo d'errore **espone i nomi tecnici dei campi** (`IsRapportoEE`, `IsRapportoFM`),
non le etichette: è il modo per capire *quale* campo, ma non aiuta chi non sa il modello.

Oltre questo punto il modulo prosegue per sezioni normative (A, B, …, prescrizioni) più
le analisi fumi/funzionamento/scambiatore. **Non l'ho compilato**: sono decine di campi
normativi che con dati finti non insegnano niente, e comunque **l'invio al catasto è
vietato**.

---

# Agenda — verificata

`#/agenda/calendar?...` con **tutto lo stato nella query**, confermato dal vivo:
`AttivitaInizio` · `AttivitaFine` · `Cat` · `Data` · `Days` · **`Tecnici=[…]`**
`TipoAttivita=manutenzioni`.

A sinistra lo scadenziario con le sei cartelle e, sotto *Manutenzioni*, l'elenco vero:
codice e nominativo impianto, telefono, **operazione** (`RB` rilascio bollino, `AF`
analisi fumi, `MO` manutenzione ordinaria, `C..` condizionamento), **scadenza legale e
programmata**, tipo macchina.

A destra il calendario con **una colonna per tecnico**, le sigle colorate in alto
(quelle del gruppo attivo sono evidenziate), e le **fasce arancioni con i `+`** che sono
l'**aiuto planner** — risultato attivo di default.

⋮ del calendario, confermato: **`Riassegna impegni`** · **`Visualizza aiuto planner`** (✓)
· **`Impostazioni`**. *Riassegna impegni non è stata eseguita: sposta un'intera giornata
da un tecnico a un altro ed è massiva.*
