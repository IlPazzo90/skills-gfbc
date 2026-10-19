# skills-gfbc

Due skill per Claude Code (e Codex) pensate per chi usa **Unicò 3** di Futura SI, il gestionale
per aziende di installazione e assistenza impianti.

- **`unico3-gfbc`**: guida Unicò Web dentro il tuo Chrome tramite l'estensione Claude in Chrome.
  Legge impianti, scadenze, interventi, contratti, magazzino. Scrive (articoli, piani di
  manutenzione, preventivi su NET) solo dentro i guardrail descritti in `references/guardrail.md`.
- **`ufficio-acquisti-gfbc`**: fa il giro dell'ufficio acquisti. Legge le richieste d'offerta su
  Unicò, scrive ai fornitori da una casella Microsoft 365, sollecita, codifica le offerte e passa il
  lavoro al commerciale. Senza `unico3-gfbc` non funziona.

Sono nate in un'azienda di impianti e sono state ripulite dai suoi dati: clienti, fornitori,
prezzi, codici e persone non ci sono più. Restano le procedure e le trappole del gestionale, cioè
quello che costa settimane scoprire da soli.

## Installazione

```bash
git clone https://github.com/IlPazzo90/skills-gfbc.git
ln -s "$PWD/skills-gfbc/unico3-gfbc" ~/.claude/skills/unico3-gfbc
ln -s "$PWD/skills-gfbc/ufficio-acquisti-gfbc" ~/.claude/skills/ufficio-acquisti-gfbc
```

Per Codex il percorso è `~/.agents/skills/`.

## Prima di usarle

**`unico3-gfbc`.** Il login a Unicò lo fai tu: la skill non tocca credenziali. Di default ogni
azienda dell'installazione è trattata come produzione, quindi ogni scrittura chiede conferma. Se hai
un'azienda di prova, dichiarala:

```bash
export UNICO3_SANDBOX="C1234/A3"          # il tuo codice cliente e l'azienda di prova, dalla URL
export UNICO3_AUTORIZZATE="crea_articolo" # facoltativo: crea articoli in produzione senza chiedere
```

Invii verso clienti, catasti, SDI e banche restano vietati in ogni caso.

**`ufficio-acquisti-gfbc`.** Ti servono:

1. Una app registration su Microsoft Entra con i permessi `Mail.Read` e `Mail.Send`, meglio se
   limitati alle caselle dell'ufficio. La configurazione va in `~/.config/ufficio-acquisti/graph.env`,
   e l'intestazione di `scripts/posta.py` spiega i campi.
2. I quattro file da compilare in `references/`: `fornitori.md`, `prezzi.md`, `ricorrenti.md` e
   `aperti.md`. Se restano vuoti, la skill non sa a chi scrivere né a che prezzo vendere.
3. Una rilettura della tabella «Cosa puoi fare da solo» in `SKILL.md`. Di partenza è prudente:
   chiede quasi tutto e gli ordini partono solo con il tuo ok.

## Test

```bash
cd unico3-gfbc && python3 -m pytest -q
```

## Cosa non c'è

La documentazione ufficiale di Futura (guida web, wiki di Unicò NET, webinar) non è inclusa perché
non è nostra. La trovi sul portale Futura con le tue credenziali.

Le skill descrivono il comportamento di Unicò come l'abbiamo misurato fra settembre e ottobre 2026.
Futura aggiorna il prodotto: se un passaggio non torna più, il file che lo descrive va corretto.
