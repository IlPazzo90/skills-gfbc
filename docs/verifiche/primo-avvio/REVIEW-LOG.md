# Review log — primo avvio e prontezza all'installazione

Arbitro: Claude (Opus 5.5) → Reviewer: Codex (`gpt-6.1-sol`, quota Codex «tight»: massimo 3 round, dal router AOS).

## Round 0 — check meccanici
- Audit da clone pulito (subagente Sonnet, home finta, sola lettura) sul commit pubblicato: trovati README incompleto (niente `mkdir -p`, pytest non installato, `websocket-client` non citato, versione Python), 3 riferimenti in `strumenti.md` senza prefisso `unico3-gfbc/`, `posta.py --help` che richiedeva la configurazione e `KeyError` con chiave obbligatoria mancante. Tutti corretti.
- `websocket-client`: serve solo a `u3/chrome.py`, dichiarato abbandonato in `u3/README.md` → non necessario; README lo dice.
- `posta.py`: `--help` senza config → stampa l'uso, rc 0; config assente → messaggio, rc 1; config senza `GRAPH_SECRET`/`DOMINIO` → «incompleta, mancano: …», rc 1; config minima → `acquisti@esempio.it`.
- Comandi del primo avvio (`mkdir`, `cp -n modelli/*.md`) eseguiti in una home finta: file creati, 5 modelli con segnaposto rilevati da `grep -l '<'`.
- Scansione dei riferimenti `references|u3|scripts|modelli/...` in tutti i .md: nessun riferimento morto.
- pytest 156 passed; `u3.fatti` 6 fatti, nessuna divergenza; gitleaks pulito.

## Round 1 — Codex `gpt-6.1-sol` (configurato, non degradato)
| # | Sev | Finding | Esito | Evidenza / correzione |
|---|---|---|---|---|
| 1 | MAJOR | primo avvio acquisti non scatta se mancano i .md con `graph.env` presente | ACCETTATO | condizione letta: vero; ora «se manca uno dei file della tabella» |
| 2 | MAJOR | primo avvio non raccoglie `TipologiaImpianto` né i codici degli articoli di servizio `<ART_…>` usati da preventivi e contratti | ACCETTATO | 9 segnaposto contati nei references; aggiunti riga tabella e punto 5 «Articoli di servizio» + tabella nel modello |
| 3 | MAJOR | README promette il passaggio agli acquisti, ma il primo avvio di unico3 non lo dice | ACCETTATO | `rg ufficio-acquisti` vuoto; aggiunto in «Chiudi» |
| 4 | MAJOR | apprendimento: ogni numero nel registro versionato vs numeri aziendali locali | ACCETTATO | distinti «numero sul programma» (registro) e «numero sulla tua azienda» (organizzazione.md) in tabella e regola; nota anche nel primo avvio |
| 5 | MAJOR | README per Codex non dice che servono gli strumenti del browser | ACCETTATO | SKILL.md e README: in Codex serve uno strumento equivalente, altrimenti solo consultazione |
| 6 | MINOR | `posta.py` traceback con config non leggibile (`IsADirectoryError`) | ACCETTATO | riprodotto; ora `OSError` → messaggio, rc 1 |
Check: pytest 156 passed; u3.fatti OK; gitleaks pulito.

## Round 2 — Codex `gpt-6.1-sol` (configurato, non degradato)
| # | Sev | Finding | Esito | Evidenza / correzione |
|---|---|---|---|---|
| 7 | MINOR | etichette `<ART_…>` del modello compilato restano «segnaposto» e riattiverebbero il primo avvio | ACCETTATO | riprodotto; etichette senza parentesi angolari. Trovati dall'arbitro anche l'intestazione della tabella e la marcatura `[detto da <ruolo>]`: corretti. Dopo: le sole `<…>` rimaste nel modello sono campi da compilare |
| 8 | MINOR | rito di chiusura con `python3 -m pytest` mentre il README installa pytest solo nel venv | ACCETTATO | SKILL.md e apprendimento.md ora usano `.venv/bin/python -m pytest -q`; provato: venv nuovo + pytest → 156 passed |
| 9 | MINOR | `FIRMA` illeggibile → traceback all'avvio | ACCETTATO | riprodotto con `FIRMA=/`; ora messaggio, rc 1 |
Check: pytest 156 passed (venv pulito); u3.fatti OK; gitleaks pulito.

## Round 3 — Codex `gpt-6.1-sol` (configurato, non degradato; ultimo round, tetto 3 per quota «tight»)
| # | Sev | Finding | Esito | Evidenza / correzione |
|---|---|---|---|---|
| 10 | MAJOR | gli esiti raccolti dalla tendina Evadi non danno la destinazione (`AzioneSuccessiva`, `IdTipoAttivitaDaProgrammare`) e saltano le tipologie senza pratiche | ACCETTATO | confermato su `crm-ticket.md` «Il motore degli esiti»; ora gli esiti si leggono da `TipoAttivitaUfficio` con azione e destinazione, export per le tabelle grandi; colonna del modello allineata |
| 11 | MAJOR | configurazione senza chiave azienda, mentre tipologie ed esiti cambiano da azienda ad azienda | ACCETTATO | confermato su `crm-ticket.md`; modello con «Configurazione per azienda» e una sezione `C<tenant>/A<n>`; primo avvio: punti 4-5 per ogni azienda; SKILL.md e ciclo.md: si usa solo la sezione dell'azienda letta dalla URL, un'azienda senza sezione non è censita |
Check: u3.fatti OK; gitleaks pulito.

## Verdetto: VERIFICATO CON RISERVE

Tre round Codex (tetto ridotto a 3 dal router AOS per quota Codex «tight»), nessun PASS. 11 finding, tutti verificati e accettati: 7 MAJOR, 4 MINOR; nessuno confutato, nessun BLOCKER.
Riserve:
- Le correzioni del round 3 (esiti e configurazione per azienda) non sono state rilette da Codex.
- Il primo avvio è una procedura scritta, non provata su una vera installazione Unicò di un'altra azienda: la prima esecuzione reale va trattata come `[da verificare]`.
- In Codex la guida del browser dipende da uno strumento che il repository non fornisce.
