# Changelog

## 2026-10-19 (secondo intervento)

- Primo avvio: `unico3-gfbc/references/primo-avvio.md` e `ufficio-acquisti-gfbc/references/primo-avvio.md` guidano il nuovo utente a fare il punto sulla sua organizzazione (aziende, ruoli, catena del CRM, tabelle di configurazione, fornitori, prezzi, autonomie). Quello che la skill impara della singola azienda va in `~/.config/unico3/organizzazione.md` e `~/.config/ufficio-acquisti/`, fuori dal repository.
- `ufficio-acquisti-gfbc`: i file da compilare passano da `references/` a `modelli/`; nuovo modello `autonomie.md` per quello che il titolare concede oltre la tabella di partenza.
- `posta.py`: `--help` funziona senza configurazione; chiavi obbligatorie mancanti in `graph.env` danno un messaggio invece di un traceback.
- README: installazione da clone pulito (`mkdir -p`, percorsi espliciti, pytest in un venv solo per i test, `websocket-client` non necessario), primo avvio, aggiornamento.
- Corretti tre riferimenti in `ufficio-acquisti-gfbc/references/strumenti.md` che puntavano a file di `unico3-gfbc` senza prefisso.
- Verifiche: audit d'installazione da clone pulito in una home finta; 156 test; `u3.fatti`; gitleaks; scansione dei riferimenti a file; comandi del primo avvio provati in una home finta.

## 2026-10-19

- Prima versione pubblica di `unico3-gfbc` e `ufficio-acquisti-gfbc`, ricavate dalle skill interne e ripulite dai dati dell'azienda d'origine (persone, clienti, fornitori, prezzi, codici, infrastruttura).
- `unico3-gfbc`: aziende sandbox e permessi permanenti da variabili d'ambiente (`UNICO3_SANDBOX`, `UNICO3_AUTORIZZATE`), vuote di default; profilo Chrome in `~/.unico3-profile`.
- `ufficio-acquisti-gfbc`: `posta.py` configurabile (dominio, caselle, firma) da `~/.config/ufficio-acquisti/graph.env`; fornitori, prezzi, ricorrenti e pratiche aperte come modelli da compilare.
- `unico3-gfbc`: `elimina_documento` ed `elimina_intervento` classificate irreversibili (vietate in produzione); helper di pagina non distribuiti dichiarati come tali.
- Verifiche: 156 test verdi, `u3.fatti` senza divergenze, gitleaks pulito; sei round di revisione adversariale cross-model (Codex), 25 finding tutti corretti, esito «verificato con riserve». Il verbale cita i dati rimossi e resta privato, fuori dal repository.
