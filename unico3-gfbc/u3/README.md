# u3/ — cosa è vivo, cosa dorme, e cosa i test garantiscono davvero

Scritto il 04/09/2026 riallineando il pacchetto all'architettura scelta.

## La cosa da sapere per prima

**Durante l'uso normale della skill, questo codice non viene eseguito.**

La skill funziona come conoscenza + procedura: leggo i `references/`, guido Chrome con
l'estensione e con JavaScript nella pagina. Nessun modulo Python sta nel percorso.

Quindi: **i test verdi non dicono che la skill funziona.** Dicono che queste funzioni
si comportano come previsto se qualcuno le chiama. È una garanzia reale ma stretta, e va
citata per quello che è — non come prova che il lavoro su Unicò sia corretto. Quella prova
sono le misure nei `references/flussi/`, e una verifica esterna che non ho ancora fatto.

## Vivo — vale la pena chiamarlo

**`sessione.py`** — `azienda_da_url()` e `classifica()`. È la regola più importante di
tutta la skill: *da quale azienda sto operando*. Robusta contro host stranieri, tenant
diversi e parametri ambigui: se qualcosa non torna risponde `"sconosciuta"`, che fa
chiedere invece di indovinare.

**`guardrail.py`** — `valuta(Azione)` restituisce `consenti` / `conferma` / `vieta`.
Tre categorie: `VERSO_ESTERNO` (mai, su nessuna azienda), `IRREVERSIBILI`,
`SEMPRE_CONFERMA`, più `SCRITTURE_ESPLICITE` consentite sulle sandbox (`UNICO3_SANDBOX`) e `AUTORIZZATE_OVUNQUE`
(da `UNICO3_AUTORIZZATE`, vuota di default; oggi solo `crea_articolo`) consentite anche in produzione. Il ramo finale è la rete
di sicurezza: **un tipo di azione mai classificato ricade su `conferma`**.

Si usano da riga di comando quando serve decidere:

```bash
python3 -c "
from u3.sessione import azienda_da_url, classifica
from u3.guardrail import Azione, valuta
az = classifica(azienda_da_url('<la URL letta dal browser>'))
print(valuta(Azione(tipo='invio_telematico', bersaglio='rcee', azienda=az)))
"
```

**`fatti.py`** — l'unico modulo che **va eseguito a ogni chiusura di sessione**:

```bash
cd <cartella della skill> && python3 -m u3.fatti
```

Legge il registro canonico `references/fatti-misurati.md` e cerca la *traccia* di ogni
fatto in `SKILL.md` e in tutti i `references/`. Dove trova un numero diverso stampa
**file:riga** ed esce 1. Non prova che i numeri siano giusti — prova che i file **non
si contraddicono fra loro**, che è il difetto che il 04/09/2026 ha prodotto tre
affermazioni smentite sopravvissute in tre file. Protocollo: `references/apprendimento.md`.

**`griglia.py`** — normalizza date `gg/mm/aaaa` e numeri `1.234,56`, e ripulisce i
surrogati Unicode che fanno esplodere `print`. Utile quando un dump di griglia arriva come
testo invece che dal modello AG Grid.

## Dorme — resta per riferimento, non è il percorso

**`chrome.py`** — pilotava un Chrome dedicato via DevTools Protocol. **Architettura
abbandonata** il 03/09/2026: si è scelto il Chrome normale con l'estensione, e
Python non guida l'estensione.

**`mappa.py`** — mappa dei selettori come JSON auto-editabile, con lo storico delle
conferme. Buona idea, ma la mappa **vive in markdown** (`references/mappa-web.md`,
`tabelle-rotte.md`) perché è quella che leggo io.

**`diario.py`** — un record per sessione. Mai collegato a niente.

**`scripts/ricognizione.py`** — la ricognizione di fase 0 via CDP. Superata: la
ricognizione è stata fatta dall'estensione, e i risultati sono nei `references/`.

**Non si cancellano.** Se un giorno servisse un percorso
programmatico — un cron che estrae senza una persona davanti — `chrome.py` e `mappa.py`
sono il punto da cui ripartire.

## Se tocchi guardrail.py

Un test verifica che **ogni azione classificata abbia il suo motivo** in `MOTIVI`.
Aggiungere una voce a `IRREVERSIBILI`, `VERSO_ESTERNO` o `SEMPRE_CONFERMA` senza scrivere
il perché fa fallire la suite — di proposito: un verdetto senza spiegazione è un muro, e
davanti a un muro la gente cerca il modo di aggirarlo.
