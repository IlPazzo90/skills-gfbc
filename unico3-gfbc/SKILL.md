---
name: unico3-gfbc
description: Opera su Unicò 3 (il gestionale di Futura SI), guidando Chrome. Usare quando serve un dato dal gestionale — impianti, scadenze di manutenzione, interventi, contratti, clienti, magazzino — o quando si chiede di fare qualcosa dentro Unicò. Trigger - "unicò", "unico3", "gestionale", "quanti impianti", "scadenze manutenzione", "rapporti di intervento", "ricerca impianti".
---

# unico3

## Configurazione

Due variabili d'ambiente, entrambe vuote di default:

- `UNICO3_SANDBOX` — le aziende di prova, con il tenant, separate da virgola
  (es. `C1234/A3,C1234/A2`). Su queste le scritture ordinarie sono libere. Ogni azienda
  non dichiarata qui vale produzione.
- `UNICO3_AUTORIZZATE` — i permessi permanenti, cioè i tipi di azione consentiti anche
  in produzione senza chiedere ogni volta. Oggi accetta solo `crea_articolo`.

Il login lo fa una persona a ogni sessione: le credenziali non si toccano mai.

Pilota **Unicò Web** dentro il Chrome dell'utente, con l'estensione del browser.
Unicò3 "classico" è una RemoteApp Windows e da qui non è raggiungibile. Solo web.

## Prima di qualunque cosa, in quest'ordine

**0. Leggi `~/.config/unico3/organizzazione.md`.** È quello che la skill sa della *tua*
azienda: aziende, ruoli e, per ogni azienda censita, catena del CRM, sigle, magazzini. Della
configurazione usa solo la sezione dell'azienda letta dalla URL (passo 1). Se non esiste o ha ancora i
segnaposto `<...>`, è il primo avvio: proponi di fare il punto con
`references/primo-avvio.md` (solo lettura, una volta). Finché non c'è, sigle, tipologie e
nomi citati nei `references/` sono **esempi dell'azienda d'origine**, non la tua
configurazione: dillo quando li usi.

**1. Leggi l'azienda dalla URL e dichiarala in chat.**

```
https://app.dc3.unico3.cloud/?c=/C<tenant>/A3/#/...
                              └── qui ──┘
```

L'identificativo comprende il **tenant**. Un'azienda vale **sandbox** solo se
`C<tenant>/A<n>` compare in `UNICO3_SANDBOX` (definizione in `references/guardrail.md`,
§5.1); ogni altra vale **produzione**. «A3» da solo non nomina un'azienda — nomina la
terza azienda di *qualche* installazione.
Aprendo Unicò dal portale si finisce sull'azienda predefinita: verifica dopo ogni
apertura. Mai dedurre l'azienda dal testo della pagina — il riquadro Sessione Corrente
elenca tutti i numeri insieme. La funzione giusta è `u3.sessione.azienda_da_url`.

**2. Leggi `references/guardrail.md`.** Non è opzionale.

La versione eseguibile è `u3/guardrail.py` — si invoca da Bash quando serve decidere
(esempio in `u3/README.md`). ⚠️ **Ma non gira da sola**: la skill è conoscenza +
procedura, e i test di `u3/` non provano che il lavoro su Unicò sia corretto. Quella
prova sono le misure nei `references/flussi/`. Su una sandbox le scritture ordinarie
sono libere; in produzione servono anteprima e ok esplicito. **Le operazioni irreversibili
sono vietate in produzione e chiedono conferma anche su una sandbox** — perché una sandbox non è per forza vuota: può
contenere lo storico reale, impianti e documenti veri. Annullare una numerazione lì è un
danno vero.

Zona rossa, in breve: annullamento numerazione, accorpamenti, ricalcolo preventivo,
chiusure d'esercizio e magazzino, liquidazione IVA, invii telematici, fatturazione
elettronica, presentazione effetti, rinomina di una voce di tabella, eliminazione
insoluti, **operazioni massive con filtri attivi**. Fermati e spiega perché, non
aggirarla.

**3. Se stai per scrivere e l'azienda non è una sandbox, chiedi.** Eccezione: i tipi di
azione in `UNICO3_AUTORIZZATE` (oggi `crea_articolo`, guardrail 5.1-ter); modificare gli
articoli esistenti no.

**4. Prima di promettere un'azione, controlla che esista.** `references/cosa-il-web-non-fa.md`
elenca cosa il web fa davvero: **non c'è contabilità** (niente prima nota, IVA, registri,
incassi), non c'è il ciclo Installazione. **I movimenti di magazzino invece ci sono** dalla
release 2026.3 (carico DDT fornitore: `references/flussi/carico-ddt-fornitore.md`). Quella
parte della guida descrive il terminale Windows, che da qui non parte.

## Come si guida

Estensione Chrome (`mcp__claude-in-chrome__*`, Claude Code). In Codex serve uno strumento
equivalente che piloti un browser con la sessione di Unicò aperta; se non c'è, dillo: la skill
resta consultazione, non guida. `javascript_tool` **funziona** — se
torna `[BLOCKED: ...]` è il filtro di sicurezza sul contenuto restituito, non lo
strumento: chiedi i campi per nome invece di riversare strutture intere.

L'interfaccia è **Aurelia**, non Angular: i menu aperti sono
`div.x-material.dropdown-menu` con voci `context-item`; i menu a tendina dei campi
espongono `[role="option"]`. Le griglie sono **AG Grid**.

**La URL dice bene l'azienda. Sulla rotta dipende da dove sei.**

- **Ricerche**: scrivere la rotta a mano **non cambia lo schermo** — si naviga a click.
- **Tabelle**: `location.hash = '#/tabelle/<Entita>/table'` **funziona davvero**
  (verificato). Ma una rotta inesistente **lascia in silenzio la tabella precedente**:
  si confronta sempre il titolo di `div.main-tab.selected` con quello atteso.
  Rotte e metodo in `references/tabelle-rotte.md`.

Per sapere cosa è davvero aperto si legge `div.main-tab.selected`, non la URL.

## Flussi

| Flusso | Dove |
|---|---|
| Estrazione dati — rispondere con numeri | `references/flussi/estrazione.md` |
| **Ricerca avanzata — procedura eseguita e misurata** | `references/flussi/ricerca-avanzata.md` |
| **Creare un impianto da zero — procedura eseguita** | `references/flussi/nuovo-impianto.md` |
| **Correggere i modelli installato (GT e frigo) — procedura eseguita** | `references/flussi/tabelle-modelli.md` |
| **Intervento, documento, numerazione — procedura eseguita** | `references/flussi/intervento-e-documento.md` |
| **Preventivo su Unicò NET — procedura osservata** | `references/flussi/preventivo-net.md` |
| **Ordine a fornitore su Unicò NET, numerazione e PDF — procedura eseguita** | `references/flussi/ordine-fornitore-net.md` |
| **Carico DDT fornitore (movimento di magazzino) — procedura eseguita** | `references/flussi/carico-ddt-fornitore.md` |
| **Contratti di manutenzione: inserimento, copertura, rate, piano — procedura eseguita** | `references/flussi/contratti.md` |
| **Piani di manutenzione delle macchine (GT, GF, impianto) — procedura eseguita** | `references/flussi/piani-manutenzione.md` |
| Costruire la domanda: filtri, ricerca avanzata, cattura, export | `references/ricerche.md` |
| CRM — ticket, attività ufficio, RDI | `references/crm-ticket.md` |
| Impianto, intervento, documenti, RCEE, F-Gas | `references/assistenza.md` |
| Agenda, planner, scadenziario | `references/agenda.md` |
| Tabelle — la configurazione del programma | `references/tabelle.md` |
| Clienti, fornitori, riferimenti, ruoli | `references/anagrafiche.md` |
| Documenti, prima nota, IVA, chiusure, fine anno | `references/amministrazione.md` |
| Articoli, giacenze, cataloghi, ordini, preventivi, commesse | `references/magazzino.md` |
| Catasti, DiCo, spesometro, ricevute fiscali, portale | `references/adempimenti.md` |
| App dei tecnici — cosa possono fare e cosa arriva in ufficio | `references/mobile.md` |
| Utenti, licenze, impostazioni globali | `references/impostazioni-e-utenti.md` |
| **Cosa il web NON può fare** | `references/cosa-il-web-non-fa.md` |
| **Rotte delle tabelle + conteggi e campi** | `references/tabelle-rotte.md` |
| Files, Impostazioni, Geolocation, Analisi dati | `references/aree-minori.md` |

**Prima di toccare l'interfaccia leggi `references/interazione.md`.** Contiene le
regole che costano tempo se non le sai: il pannello dei risultati copre i campi del
filtro, un click su un campo coperto finisce sulla griglia e sporca la selezione, le
griglie delle ricerche non si ordinano dalle intestazioni, e un filtro che sembra non
cambiare niente di solito non è stato scritto.

I file sopra descrivono **come funziona** ogni area, dalla guida ufficiale più quanto
verificato dal vivo. Dove i due divergono lo dicono, e **vince la misura**. Una
procedura passo-passo eseguibile esiste per ora solo per l'estrazione: per le altre si
mappa il caso concreto, si scrive la procedura, poi la si esegue — in quest'ordine.

## La regola che non si salta

**Una griglia troncata ha lo stesso aspetto di una griglia completa.** Su una
ricerca con migliaia di risultati, il DOM ne conteneva 26. Nessun numero esce da qui senza
la prova di completezza descritta in `flussi/estrazione.md`: totale dichiarato da
Unicò contro totale nel modello della griglia. Se non coincidono, si dice che non
coincidono.

## Imparare — non è opzionale

Unicò cambia, e questa skill l'ha scritta qualcuno che il programma lo stava
imparando: contiene errori che non sa ancora di avere. **Quello che si scopre
usando Unicò si scrive prima di chiudere la sessione**, altrimenti la sessione
dopo riparte da zero.

La procedura completa — quando scatta, dove va cosa, che grado di verità ha —
sta in **`references/apprendimento.md`**. Tre cose da qui:

1. **Si consolida, non si appende.** La correzione si scrive **dove stava
   l'errore**, non in fondo al file: chi legge dall'alto incontrerebbe prima la
   versione smentita. Prima di scrivere: `grep -rn "<parola>" SKILL.md references/`.
2. **Un numero misurato va in `references/fatti-misurati.md`**, il registro
   canonico — poi nel testo che lo usa.
3. **Un diario delle sessioni, se lo vuoi, è un file locale non versionato**: può
   nominare clienti e importi veri e non va su GitHub.

**Quello che riguarda la tua azienda** (una sigla, un ruolo, un'abitudine) va in
`~/.config/unico3/organizzazione.md`, mai nei `references/`: quelli sono del repository e
descrivono Unicò, non la tua configurazione.

**Rito di chiusura sessione**, dalla cartella della skill (`unico3-gfbc/`):

```bash
python3 -m u3.fatti            # nessun file contraddice il registro — non si salta
.venv/bin/python -m pytest -q  # guardrail e helper (venv del README; o python3 se pytest è globale)
```

`u3/fatti.py` è la rete che il 04/09/2026 mancava, quando tre numeri smentiti erano
sopravvissuti in tre file diversi. Dice **file:riga** dove qualcuno afferma un altro
numero.

L'unica cosa che la skill **non** impara da sola è allargarsi la zona rossa. Quella
si estende solo, mai si restringe senza una decisione esplicita del responsabile. E il
controllo dei fatti prova che i file concordano **fra loro**, non con Unicò: la prova
esterna è una verifica indipendente, da rifare dopo ogni sessione di apprendimento
consistente.

## Riferimenti

| File | Quando |
|---|---|
| `~/.config/unico3/organizzazione.md` | sempre, prima di agire: la tua azienda |
| `references/primo-avvio.md` | la prima volta, e quando cambiano release, persone o configurazione |
| `references/guardrail.md` | sempre, prima di agire |
| `references/mappa-web.md` | per sapere dove sta una cosa e cosa è già stato verificato |
| `references/dominio.md` | per capire il significato di quello che si legge o scrive |
| `references/fatti-misurati.md` | **prima di affermare un numero**, e quando se ne misura uno nuovo |
| `references/apprendimento.md` | quando qualcosa non torna, o si è scoperto qualcosa di nuovo |
| `references/flussi/estrazione.md` | ogni volta che si risponde con un numero |

La guida ufficiale (Help on-line e wiki Unicò NET) sta sul portale Futura SI, dietro il
login, e non è inclusa in questo repository per i diritti. Da lì si scarica dal browser
autenticato (`curl` prende un 302); i file `references/` di area ne sono il riassunto, e
si torna alla guida quando serve un dettaglio che il riassunto non ha.
