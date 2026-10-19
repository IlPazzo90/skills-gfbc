# Ricerche ed estrazioni

Come si interroga Unicò. La **meccanica di lettura della griglia** (paginazione,
prova di completezza) sta in `flussi/estrazione.md`; qui c'è **come si costruisce la
domanda**.

Ogni modulo (Assistenza, Magazzino, Amministrazione) ha la sua sezione `Ricerca`, e
ogni ricerca ha due facce: **semplice** e **avanzata**. Si apre sempre sulla semplice.

---

## Ricerca semplice

Si sceglie **l'area** (l'entità) e cambiano i campi sotto. Si compila, `CERCA` o
**Invio**. In alto a destra: `reset`, **salva/condividi**, e ⋮.

La cosa da sapere: dal ⋮ c'è **`Trasforma in ricerca avanzata`**, che **traduce da sola
i criteri compilati** nel linguaggio avanzato. È la strada giusta quando serve un
criterio che la semplice non espone: si imposta il grosso a mano, poi si traduce e si
affina. Non si riparte da zero.

### La convenzione `%`, che vale ovunque

Senza `%` il campo **inizia con**. Con `%` davanti, **contiene**.
Si concatenano: `%valvola%sfera%` per stringere il tiro.

Esempio: `%ROSSI` trova anche GROSSI, `ROSSI` no.

Alcune maschere accettano **intervalli** su campi numerici o data (da… a…).

### Filtro cattura

Presente in tutte le maschere. Limita la ricerca a un sottoinsieme **catturato** in
precedenza, o al suo **complementare** (`Liberi`).

Serve a superare il limite vero delle ricerche: ognuna è settoriale. Dalla ricerca
*Operazioni di manutenzione* si filtra benissimo sulle operazioni, ma **non si sa nulla**
della caldaia, dei contratti o dei documenti. La **cattura** lega i risultati di ricerche
diverse a passi successivi: catturo gli impianti che mi interessano da una ricerca, e
nella successiva parto da quel sottoinsieme.

---

## Ricerca avanzata (SMART)

È un query builder booleano vero. Si aggiungono **condizioni** e **gruppi**.

Il selettore a inizio gruppo dice se valgono **`tutte le`** (AND) o **`almeno una delle`**
(OR). I gruppi si annidano: è lì che sta la potenza.

Operatori, per genere di campo:

| Operatore | Cosa fa |
|---|---|
| `Uguale a` / `Diverso da` | confronto esatto |
| `Contiene` / `Inizia con` / `Finisce con` / `Non contiene` | testo parziale |
| `È vuoto` / `Non è vuoto` | presenza del dato |
| `LIKE` | come la `LIKE` di SQL — per chi sa cosa sta facendo |
| `Maggiore/Minore di`, `≥`, `≤`, `Uguale a n°` | numeri e **date** |
| `Almeno uno` | apre un **sottogruppo**: almeno un elemento collegato deve soddisfarlo |
| `Almeno n°` / `Al massimo n°` / `Esattamente n°` | come sopra, con conteggio |
| **`Se presenti, tutti`** | passa chi **non ha** l'elemento **oppure** ce l'ha e **tutti** soddisfano la condizione |
| `Nessuno` | apre un sottogruppo: **nessuna** condizione deve essere soddisfatta |
| `Soddisfa condizione` | apre un sottogruppo che va soddisfatto **per intero** |
| `È uno dei seguenti` | selezione multipla da tabella |
| `Vero/Falso` | booleani (es. *impianto dismesso = falso* → solo gli attivi) |

**`Se presenti, tutti` è quello che si sbaglia**: «bruciatori, se presenti tutti
Immergas» restituisce **anche gli impianti senza bruciatore**. Se servono solo quelli
che ce l'hanno, va aggiunta una condizione di presenza.

**Nella ricerca Impianto `Attivi` è preselezionato.** Chi chiede «quanti impianti
abbiamo» e non tocca quel gruppo ottiene **solo gli attivi**, e la maschera non lo dice.
Va sempre dichiarato quale delle due risposte si sta dando.

---

## Il menù ⋮ dei risultati

Uguale in semplice e avanzata:

- **Stampa** → moduli di stampa
- **Esporta** → pdf o xlsx, tutti i risultati o solo i selezionati, **in locale o nel
  cloud** di Unicò. *(Nel web **non** passa dal client FTP: quella è la meccanica di
  Unicò NET.)* Verificato: export completo, N risultati → N+1 righe con l'intestazione,
  senza riga TOTALI e senza il progressivo `N°`.
- **Personalizza campi** → quali colonne. ⚠️ **Va rilanciata la ricerca** perché abbia effetto.
- **Personalizza ordinamento** → una o più colonne. ⚠️ Idem, **va rilanciata**. Rifà la
  query **sul server**: `columnApi` non riporta nessun `sort`. La scelta **persiste**
  riaprendo il dialogo; si toglie con la ✕ + `MODIFICA`.
- **Cattura** → crea il sottoinsieme per la ricerca successiva
- **Mostra totali** → riga fissata in fondo. **Non** entra nei conteggi né
  nell'esportazione, quindi non rovina la prova di completezza.
- **Trasforma in ricerca avanzata** (solo dalla semplice)

**Le griglie dei risultati non si ordinano dalle intestazioni**: ogni colonna ha
`sortable: false`, `filter: false`, e la griglia `suppressContextMenu: true`. Vale solo
qui: le griglie delle **tabelle**, dell'**agenda** e del **piano di manutenzione** si
ordinano col click sull'intestazione, si trascinano, si raggruppano e si filtrano — la
guida ufficiale descrive **quelle**.

---

## Ricerche salvate (SMART)

`salva` a destra → nome + eventuale **condivisione**. Salvata, compare una barra colorata
col nome, e segnala se ci sono modifiche non salvate.

Poi il tasto `salva` ha due voci:
- **salva modifiche** — sovrascrive, e da qui si aggiunge/toglie la condivisione
- **crea una copia** — duplica con un nome diverso; funziona **anche su una ricerca
  condivisa da altri**

`⋮ → carica ricerca salvata` mostra due sezioni: **le mie ricerche** (con il cestino) e
**ricerche condivise**. **Una ricerca condivisa si può modificare ma non salvare**: per
tenersi le modifiche bisogna farne una copia. Chi condivide non rischia che gliela
cambino sotto.

---

## Personalizzazione delle maschere (Unicò NET)

Solo nel terminale, `Utilità → Personalizza`. Se la voce non c'è, quella ricerca **non è
personalizzabile**.

- **Visualizza dati in griglia** — albero dei campi disponibili a sinistra, ordine di
  colonna al centro (frecce su/giù), `OK` / `ReSet` / `Ritorna`. Effetto **alla ricerca
  successiva**.
- **Personalizza criterio** — i criteri modificabili sono quelli **in rosso**. Ogni
  criterio ha una **preposizione** (`AND` / `OR`) e un **operatore**
  (`LIKE` predefinito = inizia con, `=`, `<>`, `>`, `>=`, `<`, `<=`).

La guida stessa avvisa che un uso sbagliato «può portare a risultati imprevedibili e/o
blocchi del sistema». Non è un posto dove sperimentare.

**Totali colonna** (NET): `Utilità → Totali colonna`, su tutti i record o solo i
selezionati, scegliendo la colonna.

**Esportazione in NET**: Excel (default), Testo (`;` — CSV) o Open Office; tutti i dati
o i selezionati; due riquadri per scegliere e ordinare i campi; poi **parte il client
FTP**. È la differenza principale col web.

---

## Stampe

Si aprono da moltissimi punti e **propongono stampe diverse a seconda della scheda**
(impianto, intervento, contratto, anagrafica…).

Il menù ha: **tipo stampa** (solo quelle non nascoste), **nome personalizzato** (nel web
**resta salvato** per le stampe successive — in NET era temporaneo), **formato** (PDF di
default), **opzioni** specifiche della stampa (anch'esse ricordate), e due caselle che
**aggiungono passi al wizard**:

- **salva in cloud** → si sceglie il percorso; il nome di default è
  `nome stampa + anno + mese + giorno + ora + minuti`
- **email** → **manda una mail per conto dell'azienda**. Mittente e indirizzo dall'anagrafica
  CAT, destinatario dalla mail del *responsabile corrispondenza* della scheda impianto,
  oggetto = nome stampa; cc, ccn, copia al mittente, e un'icona che propone gli altri
  indirizzi legati alla scheda.

  **Questa manda posta a un cliente.** La skill non la spunta mai, nemmeno
  su richiesta e nemmeno su una sandbox (`VERSO_ESTERNO`): la spunta una persona.

`Impostazioni stampa` (dal ⋮ del menù stampa): l'elenco **completo**, comprese le
nascoste (sfondo grigio); **sigla** originale non modificabile + sigla personalizzata
che è quella che finisce stampata (serve a allinearsi alle sigle del sistema qualità
aziendale); **nascondi**; **logo** da abbinare alle stampe che prevedono `usa logo`.

In NET la stessa cosa si chiama `ESCLUDI DA ELENCO`, e ci sono i formati carta: A4
(A3/A5 non usati), *German Standard Fanfold 8½×12* per il modulo continuo ad aghi (es.
allegati G prestampati), **etichetta 89×36** (Dymo Labelwriter) e **etichetta triplex
70×46** (kit barcode Futura). Il formato **resta memorizzato**. Stampante e n° copie
sono parametri morti: si scelgono nel client di stampa locale.
