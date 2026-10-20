# skills-gfbc

Skill per Claude Code (e Codex). Le prime due sono pensate per chi usa **Unicò 3** di Futura SI,
il gestionale per aziende di installazione e assistenza impianti; la terza vale per chiunque
faccia scrivere testi a un modello.

- **`unico3-gfbc`**: guida Unicò Web dentro il tuo Chrome tramite l'estensione Claude in Chrome.
  Legge impianti, scadenze, interventi, contratti, magazzino. Scrive (articoli, piani di
  manutenzione, preventivi su NET) solo dentro i guardrail descritti in `unico3-gfbc/references/guardrail.md`.
- **`ufficio-acquisti-gfbc`**: fa il giro dell'ufficio acquisti. Legge le richieste d'offerta su
  Unicò, scrive ai fornitori da una casella Microsoft 365, sollecita, codifica le offerte e passa il
  lavoro al commerciale. Senza `unico3-gfbc` non funziona.
- **`testo-umano-gfbc`**: le scelte di struttura da fare *prima* di scrivere un testo che una
  persona leggerà (articolo, post, mail, relazione), ricavate dal paper StoryScope
  ([arXiv 2604.03136](https://arxiv.org/abs/2604.03136)): come si chiude, come si nomina
  un'emozione, cosa si lascia aperto, chi si nomina. In `testo-umano-gfbc/references/blocco-runtime.md` c'è la
  versione da incollare nei system prompt delle app che generano testo per i clienti. Non
  dipende da Unicò. Dopo la stesura si abbina bene a
  [humanizer](https://github.com/blader/humanizer), che pulisce la superficie.

Le skill di Unicò sono nate in un'azienda di impianti e sono state ripulite dai suoi dati: clienti, fornitori,
prezzi, codici e persone non ci sono più. Restano le procedure e le trappole del gestionale, cioè
quello che costa settimane scoprire da soli.

## Installazione

Serve Python 3.9 o più recente, Chrome con l'estensione Claude in Chrome e, per gli acquisti,
una casella Microsoft 365.

```bash
cd ~/Progetti                      # o dove tieni i tuoi repository
git clone https://github.com/IlPazzo90/skills-gfbc.git
cd skills-gfbc

mkdir -p ~/.claude/skills
ln -s "$PWD/unico3-gfbc" ~/.claude/skills/unico3-gfbc
ln -s "$PWD/ufficio-acquisti-gfbc" ~/.claude/skills/ufficio-acquisti-gfbc
ln -s "$PWD/testo-umano-gfbc" ~/.claude/skills/testo-umano-gfbc
```

Python, Chrome e Microsoft 365 servono solo alle skill di Unicò: `testo-umano-gfbc` è solo testo.

Per Codex il percorso è `~/.agents/skills/` al posto di `~/.claude/skills/`. Attenzione: per
guidare Unicò `unico3-gfbc` usa gli strumenti dell'estensione Claude in Chrome, che esistono in
Claude Code. In Codex serve un tuo strumento equivalente per pilotare il browser (per esempio
un server MCP di automazione browser); senza, Codex può consultare le procedure ma non
lavorare dentro Unicò. Le skill usano solo
la libreria standard di Python: per usarle non c'è niente da installare.

Per lanciare i test serve pytest. Il modo che funziona su ogni Python è un ambiente virtuale:

```bash
cd unico3-gfbc
python3 -m venv .venv && .venv/bin/pip install pytest
.venv/bin/python -m pytest -q && python3 -m u3.fatti
```

`websocket-client`, dichiarato in `pyproject.toml`, serve solo a `unico3-gfbc/u3/chrome.py`, un pilota di
Chrome via DevTools che non si usa più (vedi `unico3-gfbc/u3/README.md`).

## Primo avvio: la skill impara la tua azienda

Le procedure valgono per ogni installazione di Unicò, la configurazione no. Le sigle delle
manutenzioni, i magazzini, le tipologie del CRM, gli esiti, i ruoli citati nei file sono
esempi dell'azienda dove le skill sono nate.

Al primo uso apri Unicò in Chrome, fai il login e chiedi a Claude:

> fai il punto sulla mia organizzazione

`unico3-gfbc` gira per le tabelle in sola lettura (aziende, tipologie, esiti, magazzini,
listini, numerazioni), ti fa qualche domanda su persone e ruoli e scrive tutto in
`~/.config/unico3/organizzazione.md`. Poi `ufficio-acquisti-gfbc` fa lo stesso per la sua
parte: fornitori, regola dei prezzi, pratiche aperte e cosa le concedi. I suoi file vanno in
`~/.config/ufficio-acquisti/`.

Quei file stanno fuori dal repository apposta: contengono i dati della tua azienda e un
`git pull` per aggiornare le skill non li tocca. Le procedure del giro sono in
`unico3-gfbc/references/primo-avvio.md` e `ufficio-acquisti-gfbc/references/primo-avvio.md`.

Due cose le decidi tu, non la skill, e vanno nel profilo di shell (`~/.zshrc` o `~/.bashrc`):

```bash
export UNICO3_SANDBOX="C1234/A3"          # le aziende di prova, dalla URL: lì scrive senza chiedere
export UNICO3_AUTORIZZATE="crea_articolo" # facoltativo: crea articoli in produzione senza chiedere
```

Senza queste righe ogni azienda è trattata come produzione e ogni scrittura chiede conferma.
Invii verso clienti, catasti, SDI e banche restano vietati in ogni caso. Il login a Unicò lo
fai sempre tu: la skill non tocca credenziali.

Per la posta ti serve una app registration su Microsoft Entra con i permessi `Mail.Read` e
`Mail.Send`, limitata alle caselle dell'ufficio. La crea il tuo amministratore Microsoft 365.
La procedura del primo avvio spiega cosa chiedergli e come scrivere `graph.env`.

## Aggiornare

`git pull` nella cartella del clone. Se la skill impara qualcosa di nuovo su Unicò (una rotta,
una trappola, un comportamento cambiato), lo scrive nei suoi `references/`: per tenere quelle
modifiche fai un fork, oppure apri una issue qui e la correzione arriva a tutti.

## Cosa non c'è

La documentazione ufficiale di Futura (guida web, wiki di Unicò NET, webinar) non è inclusa perché
non è nostra. La trovi sul portale Futura con le tue credenziali.

Le skill descrivono il comportamento di Unicò come l'abbiamo misurato fra settembre e ottobre 2026.
Futura aggiorna il prodotto: se un passaggio non torna più, il file che lo descrive va corretto.
