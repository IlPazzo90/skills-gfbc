# Strumenti

## `scripts/posta.py`

Configurazione in `~/.config/ufficio-acquisti/graph.env` (permessi 600), descritta nell'intestazione
dello script. Serve una app registration Microsoft Entra con permessi applicativi `Mail.Read` e
`Mail.Send`, meglio se limitati alle sole caselle dell'ufficio con una application access policy.

```bash
P=~/.claude/skills/ufficio-acquisti-gfbc/scripts/posta.py
python3 $P nuove --dal 2026-10-06                     # inbox delle caselle configurate
python3 $P cerca "123 - Richiesta offerta" --casella acquisti
python3 $P leggi acquisti <id>
python3 $P allegati acquisti <id> /tmp/offerta
python3 $P inoltra acquisti <id> --a tecnico@azienda.it --corpo nota.html   # inoltro con firma
python3 $P invia --a referente@fornitore.it --oggetto "123 - Richiesta offerta" --corpo corpo.html [--allega foto.jpg]
```

`invia` spedisce sempre dalla casella `MITTENTE`, mette `MAGAZZINO` in copia se configurato e
aggiunge la firma. **Non può rispondere dentro un thread di un'altra casella**: scrivi una mail nuova
con lo stesso oggetto e nel testo richiama la richiesta originale (data e contenuto). Dopo l'invio
controlla la Posta inviata.

## Unicò

- Skill `unico3-gfbc`: agenda, attività, ticket (`unico3-gfbc/references/crm-ticket.md`), articoli e listini
  (`unico3-gfbc/references/magazzino.md`), preventivi NET (`unico3-gfbc/references/flussi/preventivo-net.md`).
- Webservice in sola lettura per verificare articoli e prezzi: `/magazzino/articoli/codice/{c}`.
- Nell'agenda le attività ufficio si filtrano scrivendo il nome nel campo sopra la griglia; la
  finestra di date si allarga con `AttivitaInizio` nella query.
