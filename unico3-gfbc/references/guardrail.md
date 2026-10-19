# Zona rossa

Le regole in prosa, per il router. La versione eseguibile sta in `u3/guardrail.py`
ed è quella che decide davvero: se le due divergono, vince il codice e questo file
va corretto.

## 5.1 Ambiente

Una **sandbox** è un'azienda di prova dichiarata nella variabile d'ambiente
`UNICO3_SANDBOX` (identificativi con tenant, separati da virgola, es.
`C1234/A3,C1234/A2`; vuota di default). In `u3/sessione.py` l'elenco letto è
`SANDBOX_DICHIARATE`. Ogni azienda non dichiarata vale **produzione**: nessun numero
d'azienda ha un significato fisso, A3 di un'installazione non è A3 di un'altra.

Una sandbox non è per forza vuota: può contenere lo storico reale. «Si può
sperimentare praticamente su tutto» non è «tutto»: le irreversibili chiedono conferma
anche lì, e quello che esce dall'azienda (invii, SDI, catasti) resta vietato.
Se una sandbox è stata allineata alla produzione solo in alcune tabelle, il contenuto
delle altre non vale come regola della produzione. Si copia solo dalla produzione verso
la sandbox, mai il contrario.

Prima di *ogni* azione lo script legge l'azienda attiva e la dichiara in chat.

| Azienda attiva | Lettura | Scrittura |
|---|---|---|
| Sandbox dichiarata | libera | libera (le irreversibili chiedono) |
| Produzione (ogni altra) | libera | **mai senza anteprima + OK esplicito del responsabile** |

Ogni flusso nuovo si prova prima su una sandbox.

## 5.1-bis Autorizzazione sulle sandbox

Sulle sandbox si può emettere documenti, numerarli, ecc. L'unica cosa che non si può
fare è inviarli al cliente o ai catasti.

**Cosa questo apre, e solo su una sandbox:**
emissione di documenti · **numerazione** · registrazioni di prima nota · movimenti di
magazzino · creazione di contratti, interventi, RCEE.

**Cosa resta chiuso, su qualsiasi azienda:**

| Vietato | Dove si nasconde |
|---|---|
| **Mandare qualcosa al cliente** | la casella `email` nel wizard di stampa · SMS · richieste di feedback · `Avvisare cliente` non manda nulla, ma va comunque lasciata stare |
| **Inviare ai catasti** | `Assistenza → Invio telematico` · `Invia questo RCEE` / `Invia tutti RCEE` dalla scheda intervento (CIRCE e CRITER partono **subito**, via web service) |
| **Trasmettere allo SDI** | esportazione XML seguita da invio · fatturazione elettronica integrata |

Sulla riga di confine: **esportare un file resta permesso** (resta sul disco), **premere
il tasto che lo spedisce no**. Con CIRCE e CRITER il tasto è `INVIO` e non c'è una
seconda conferma: **prima di quel wizard ci si ferma sempre**.

Questa autorizzazione vale **per le sandbox**. In un'azienda di produzione torna la
regola piena: anteprima e sì esplicito.

## 5.1-ter Permessi permanenti — `UNICO3_AUTORIZZATE`

I permessi permanenti si danno con la variabile d'ambiente `UNICO3_AUTORIZZATE`: vuota di
default, oggi accetta solo `crea_articolo`. Con `crea_articolo` il tipo azione di
`u3/guardrail.py` è **consentito anche in produzione senza chiedere ogni volta**.
Azienda non leggibile dalla URL → si chiede comunque.

**Cosa copre:** la modale «Nuovo articolo» (`magazzino.md`, «Nuovo articolo nel web») e,
**sullo stesso articolo appena creato**, listino base e primo listino fornitore.

**Cosa resta `scrittura` (in produzione si chiede):** modificare un articolo che esisteva già —
prezzi, listini, tipo, gruppo, descrizione —, Duplica, Elimina, Escluso da liste.

**Le condizioni non cambiano per il permesso:**
- prima di creare, il codice si cerca (`Cerca` → categoria Articoli): se esiste già non si
  crea un doppione, si dice;
- i dati (codice, descrizione, prezzi) vengono dalla fonte che il responsabile indica — offerta,
  listino, scheda — mai inventati; un campo che manca si segnala;
- prima di CONFERMA si rilegge ogni campo dal testo mostrato;
- a fine giro si elencano in chat codici e id creati.

## 5.2 Irreversibili — vietate in produzione, conferma su una sandbox

Il codice (`IRREVERSIBILI` in `u3/guardrail.py`) le **vieta** in produzione e su un'azienda
non riconosciuta; su una sandbox dichiarata chiede conferma. In produzione le fa una persona.

⚠️ **Nel web la numerazione è diversa da quella descritta per NET** — misurato il
03/09/2026. Non esiste «Numera»: il numero è un **campo libero della testata**, nessun
progressivo viene proposto, e **numerare NON congela il documento** (riga riaperta dopo la
numerazione: 12 campi ancora editabili). Quindi nel web **non c'è un annullamento
numerazione da temere, ma c'è un rischio nuovo**: duplicati e buchi si creano senza alcun
avviso. **Prima di numerare a mano su un'azienda vera, si guarda l'ultimo numero usato.**

**Annullare la numerazione di un documento.** Cancella anche tutti i movimenti contabili e
di magazzino collegati e lascia un buco nella sequenza che il programma non recupera da
solo. La cronologia numero/data dev'essere congruente. Vale per fatture, DDT, ricevute,
preventivi, ordini, e per il protocollo dei documenti ricevuti.

**Operazioni massive sulle tabelle web** (eliminazione, modifica, esclusione da liste,
accorpamento). Unicò chiede già di digitare il numero di elementi coinvolti, ma con un
filtro attivo **modifica anche le righe selezionate ma non visibili** — avvisa
("N righe selezionate non visibili"), non blocca.
Regola: nessuna operazione massiva senza conferma esplicita, e **mai con filtri attivi**.
Prima si azzerano i filtri, si mostra la selezione reale, poi si procede.

**Tutti gli "Accorpa".** Fondono due voci in una sostituendo l'origine ovunque e poi
eliminandola. Esistono per: anagrafiche (solo tipo Rubrica; **l'origine viene eliminata
dall'archivio**), comuni, zone, marche, modelli gruppi termici, modelli bruciatori,
modelli gruppi frigo, modelli unità interne, modelli componenti. Nessuno è reversibile.

**Rinominare una voce di tabella per riusarla.** Cambi "Mario" in "Luca" e vent'anni di
storico diventano di Luca. Si usa `Escluso da liste` + voce nuova. Vale per operatori,
tecnici, tipologie intervento, tutto.

**Ricalcolo preventivo.** Il wiki è esplicito: confermando, i prezzi vengono modificati
"senza possibilità di recuperare i prezzi originali". Si può simulare quanto si vuole
prima di uscire; l'uscita con conferma è il punto di non ritorno.

**Chiusura esercizio contabile "definitiva"** — non più modificabile né ripetibile.
**Chiusura magazzino di fine anno** — genera i movimenti di chiusura/apertura.
**Registrazione definitiva della liquidazione IVA** — congela i valori del periodo.
Nessuna di queste è roba da skill.

**Personalizzazione ricerche.** Il wiki avverte che un uso errato "può portare a risultati
imprevedibili e/o blocchi del sistema". La skill può leggere la personalizzazione
esistente; non la modifica senza richiesta esplicita.

**Insoluti** — non modificabili: in caso di errore vanno eliminati e reinseriti.

**Importazione massiva modelli** (GT, gruppi frigo, componenti). La guida ufficiale la
dichiara **irreversibile**. C'è un'anteprima che mostra in rosso barrato il vecchio e in
verde il nuovo: si guarda sempre prima di confermare. E **lasciare vuota la colonna
`Modello Unicò` crea un modello nuovo** invece di aggiornarne uno.

**Forza / rimuovi stato fatturato** su un documento di intervento. È una forzatura di
stato contabile, non una correzione di forma.

**Elimina documento** dal menù Utilità del documento di intervento: la guida dice
«definitivamente ed in maniera irreversibile».

**Deregistra** una comunicazione dello spesometro, e **Escludi RCEE dall'invio telematico**
(escluso, **non parte nemmeno se è dentro una distinta**).

## 5.2-bis Operazioni massive: il danno che non si vede sullo schermo

Oltre a quanto già detto sui filtri attivi, la guida ufficiale segnala un effetto che non
compare in nessun dialogo:

> Le operazioni massive sulle tabelle possono **desincronizzare le tabelle memorizzate
> offline sui telefoni dei tecnici**. Il sintomo è l'errore **«nuvoletta rossa»** in
> Unicò Mobile, e in quel caso **i dati dell'intervento non si salvano e vanno reinseriti
> a mano**.

Procedura corretta secondo Futura: **logout di tutti i tecnici prima**, login dopo. Su
un'azienda in produzione è un intervento da concordare con il responsabile e da fare fuori
dall'orario di campo — non a metà mattina.

**Altre operazioni che sovrascrivono in blocco**, tutte da confermare:
`Copia vincoli orari` fra tecnici · `Copia impostazioni` mobile · `Importa da furgone` ·
`Importa da tabelle magazzino` e `Importa da lista materiale` **con l'opzione
«sovrascrivi»**, che *cancella tutto prima di incollare* · `Riassegna impegni` in agenda,
che sposta un'intera giornata da un tecnico a un altro · **RdI multiple**, che generano
N richieste **indipendenti** (si cancellano una per una) e **non guardano i festivi**.

## 5.2-ter Azioni che escono verso il cliente

**Stampa con `email` spuntata.** Il wizard aggiunge un passo e **manda davvero una mail**,
con mittente dall'anagrafica CAT e destinatario dal *responsabile corrispondenza* della
scheda impianto. **Non si spunta mai**, nemmeno su richiesta e nemmeno su una sandbox (può contenere
indirizzi di clienti veri): il guardrail la vieta (`VERSO_ESTERNO`). La spunta la mette una persona.

Stesso divieto per **SMS** e **richieste di feedback**.

*Chiarimento utile, misurato sulla guida*: la casella **`Avvisare il cliente`** nel wizard
RdI **non manda niente**. Mette un banner con l'icona del telefono in agenda — è un
promemoria per l'ufficio. Non va confusa con le due sopra.

## 5.2-quater Impostazioni: basta guardare per sporcare

Entrando in `Impostazioni → Agenda → Visualizzazione` e cliccando **solo per leggere**
dentro un riquadro di chip, uscendo compare *«Ci sono delle impostazioni non salvate»*.
**Nessuna modifica era stata fatta.**

Le impostazioni valgono **per tutti gli utenti**, e il riflesso di chi legge quel
messaggio è premere `SALVA`. Regola: in Impostazioni **si legge senza cliccare dentro i
riquadri**; se il dialogo compare si risponde **`Esci`**; su un'azienda vera **non si
entra** senza richiesta esplicita.

## 5.3 Distruzioni silenziose da evitare

**Eliminare invece di sostituire.** Su gruppi termici, gruppi frigo, unità interne,
componenti e riferimenti esistono `Sostituisci` e `Dismetti`, che conservano lo storico.
Eliminare lo perde. La skill usa sempre Sostituisci/Dismetti.

**Il Libretto di Impianto è scollegato.** Una volta esportato vive per conto suo:
modificare la scheda impianto non aggiorna il libretto, e viceversa. L'unico modo di
riallinearlo è cancellarlo e rigenerarlo — cioè perdere tutto quello che era stato
inserito solo lì.

**Nota di consegna + rapportino sullo stesso materiale** raddoppia le quantità a
consuntivo di commessa.

**Modifica di una voce di tabella** = modifica in tutti i punti dove è usata.

**Voci col lucchetto** = di sistema. Non si toccano. Sono fisse anche: le operazioni di
manutenzione `MO` (Manutenzione Ordinaria), `AF` (Analisi di combustione) e `RB` (Rilascio
Bollino); le causali movimenti precaricate; le unità di misura; la famiglia merceologica;
il "Magazzino Centrale"; le causali "Movimento di chiusura" e "Movimento di apertura".

**Cancellazione bloccata dall'integrità referenziale** — messaggio
"Impossibile eliminare, verrebbe violata l'integrità referenziale del sistema". Non è un
errore da aggirare: è il sistema che protegge lo storico.

## 5.4 Fuori dall'automazione, punto

Fatturazione elettronica, invii telematici ai catasti regionali, presentazione effetti,
liquidazioni IVA, chiusure d'esercizio. Sono irreversibili verso terzi.

## 5.5 Regola di qualità del dato

**Il dato va nel campo giusto, mai nelle note.** Se serve dire "non mandare Mario in
quell'impianto" si usano i vincoli impianto (SMART), non una nota libera. Quando la skill
scrive, usa i campi tabellati; se un valore non esiste in tabella, lo segnala invece di
ripiegare su testo libero.

Sulla varietà: le tipologie intervento devono essere varie al punto giusto — né una sola
"manutenzione ordinaria" per tutto, né cinquanta tipi di sostituzione. Il dettaglio sta
nelle righe del rapportino.

## 5.6 Regola di classificazione per il router

Quando classifichi un'azione prima di passarla a `valuta()`, se non è chiaramente una
lettura o una scrittura ordinaria, **usa un nome specifico** — `personalizza_ricerca`,
`accorpa`, `rinomina_voce_tabella`, quello che è. Non etichettarla come `scrittura`
generica per comodità.

Un tipo che il codice non conosce finisce nel ramo prudente di `valuta()` e chiede
conferma — è la rete di sicurezza per tutto ciò che non è ancora stato codificato come
`IRREVERSIBILI`. Etichettare tutto come `scrittura` aggira questa rete senza che nessuno
se ne accorga: un'operazione pericolosa ma non catalogata passerebbe liscia su una sandbox
come una scrittura qualunque.

Caso concreto: `personalizza_ricerca` non è irreversibile (si può rimettere a posto), quindi
non sta in `IRREVERSIBILI`. Ma è rischiosa — il wiki avverte che un uso errato "può
portare a risultati imprevedibili e/o blocchi del sistema". Classificarla con il suo nome
proprio, invece che come `scrittura`, basta a farla cadere nel ramo che chiede conferma.
