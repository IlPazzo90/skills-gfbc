# Cosa il web può fare, e cosa no

**Censito cliccando le voci `Azioni` di ogni area su una sandbox, il 03/09/2026.** È la mappa che
mancava: la guida ufficiale descrive **Unicò nel suo insieme**, ma buona parte di quelle
funzioni **vive solo nel terminale Windows**, che da qui non parte.

Serve saperlo prima di promettere qualcosa al responsabile.

---

## Le azioni davvero disponibili, area per area

| Area | Azioni |
|---|---|
| **Assistenza** | `Nuovo impianto` · `Invio telematico` |
| **Magazzino** | `Nuovo articolo` · `Nuova voce catalogo` · `Crea articoli da catalogo` · `Importa catalogo Excel/CSV` · `Importa catalogo dal database` |
| **Amministrazione** | `Nuova anagrafica` · `Nuova anagrafica da impianto` |
| **Agenda** | calendario, scadenziario, planner |
| **Analisi dati** | Cruscotti · Analisi |
| **Tabelle · Files · Impostazioni · Geolocation** | come da mappa |

Più tutto quello che si fa **dentro** una scheda già aperta: attività, RdI, interventi,
documenti, contratti, RCEE, piani di manutenzione.

---

## ⛔ Quello che nel web NON c'è

### Contabilità: non esiste

**In Amministrazione ci sono due sole azioni, entrambe anagrafiche.** Non c'è:

- **Prima nota** — nessuna registrazione contabile
- **Registrazione documenti ricevuti** e **Ricezione SDI**
- **Incassi e pagamenti**, compensazioni, insoluti
- **Presentazione effetti**, distinte CBI, SDD
- **Liquidazione IVA**, registri fiscali, libro giornale
- **Bilancio**, mastrini, partitari, piano dei conti
- **Chiusure d'esercizio**, spesometro

Tutto `amministrazione.md` descrive **il terminale**. È conoscenza utile per capire i
dati che leggo e per parlare con chi tiene la contabilità, **ma da qui non si esegue**.

> **Conseguenza netta: questa skill non fa contabilità.** Se serve, la fa una persona dal
> terminale Windows. Dirlo subito è più utile che scoprirlo a metà.

### Magazzino: movimenti sì (dal 2026.3), inventario no

**Smentito il 07/10/2026:** con la release **2026.3** (annuncio Futura SI del 21/09/2026,
«Gestione movimenti di magazzino») il web ha la tessera **`Crea movimento`** e la ricerca
**`Movimento di magazzino`**: carichi da fornitore, resi, trasferimenti, con testata,
dettagli e riferimenti al DDT. Usata per registrare DDT d'acquisto:
`flussi/carico-ddt-fornitore.md`. Il 03/09 la tessera non c'era.

Resta senza azione propria: **Inventario** e la sua chiusura, `Ordini a fornitore` (si
leggono dalla ricerca `Materiale in ordine`, non si creano) e `Liste materiale`.

### Documenti: solo quelli di intervento

Si creano **rapportini, ricevute fiscali e «altro» dentro un intervento**. Le **fatture
sono in sola lettura**, e non esiste l'emissione documenti come modulo a sé (DDT,
fatture, preventivi, commesse).

### Installazione: assente

Preventivi, commesse, rapportini di commessa, note di consegna, DiCo EC744: **nessuna
voce di menù**. `magazzino.md` le descrive per il terminale.

**I preventivi si fanno su Unicò NET**, che si apre nel browser dalla prima icona della
sezione App del portale: procedura in `flussi/preventivo-net.md`.

---

## ✅ Quello che il web fa bene, ed è quasi tutto quello che serve all'azienda

- **Assistenza completa**: impianti, installati, piani di manutenzione, riferimenti,
  contratti, note, file, vincoli, tag
- **Il CRM**: ticket, attività d'ufficio, RdI, esiti e catene
- **Interventi**: creazione, operazioni eseguite, validazioni, collaudi, anomalie, RCEE,
  F-Gas, e i **documenti di intervento** con numerazione
- **Agenda e planner**
- **Ricerche**, semplici e avanzate, con cattura, export e ricerche salvate
- **Tabelle**: tutta la configurazione
- **Analisi dati**: cruscotti e analisi

Il lavoro quotidiano di un'azienda di assistenza sta **quasi tutto** in questa colonna.
Quello che manca è il ciclo amministrativo, che è di chi fa la contabilità.

---

## Perché è così

Il portale lo dichiara: le applicazioni Unicò sono di due nature, **terminalizzate** e
**web**, e *«la sezione Unicò Web è destinata ad accogliere tutte le attuali applicazioni
Windows che verranno progressivamente riscritte»*. È una **migrazione in corso**, non una
divisione di ruoli.

Quindi questa pagina **invecchia**: alla prossima sessione, se una voce nuova compare in
`Azioni`, va aggiornata qui. E la regola pratica resta:

> **Prima di dire «lo faccio», si guarda se l'azione esiste nel menù.** La guida
> ufficiale non è una promessa su cosa c'è nel web.
