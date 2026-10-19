# Fatti misurati — il registro canonico

Ogni numero che questa skill afferma sta qui **una volta sola**, con la data e il modo
in cui è stato misurato. Gli altri file lo ripetono pure — un testo pieno di rimandi non
si legge — ma ripeterlo vuol dire poterlo lasciare indietro.

Perciò esiste il controllo:

```bash
cd <cartella della skill> && python3 -m u3.fatti
```

Legge questa tabella, cerca la *traccia* di ogni fatto in `SKILL.md` e in tutti i
`references/`, e segnala **file:riga** dove il numero scritto è un altro. È la rete che
il 04/09/2026 mancava, quando «72 tabelle», «16 entità cercabili» e «la numerazione
congela il documento» erano sopravvissute in tre file dopo essere state smentite.

## Come si aggiunge un fatto

Un fatto entra qui quando è stato **misurato**, non letto. La colonna *Come* deve dire
con quale prova: se non sai scriverla, non è un fatto, è un'impressione.

La **traccia** è una regex Python con un gruppo di cattura sul numero. Due vincoli:

- **niente `|`** dentro la traccia — spezzerebbe la cella della tabella;
- dev'essere abbastanza stretta da non prendere frasi che parlano d'altro.

Se una riga contiene di proposito un numero diverso, si marca con `<!-- fatti:ok -->` e
il controllo la salta. Serve per le frasi legittime; non per zittire una divergenza vera.

## Il registro

| Chiave | Valore | Misurato il | Traccia | Come |
|---|---|---|---|---|
| scritture-per-conferma | 1 | 14/10/2026 | `CONFERMA misurata ha fatto ([\d.]+) sola scrittura` | sandbox, registratore di `fetch`/`XMLHttpRequest` nella pagina incrociato con il registro di rete del browser, su impianto, GT, GF, piano, articolo, listino, DDT, attività, RDI |
| endpoint-scrittura-web | 13 | 14/10/2026 | `([\d.]+) endpoint di scrittura misurati` | stessa misura, endpoint `PUT` distinti |
| righe-nel-dom | 26 | 03/09/2026 | `[Dd]OM ne \w+ ([\d.]+)` | stessa ricerca: righe renderizzate nel DOM |
| entita-assistenza | 23 | 03/09/2026 | `Assistenza[ :—-]+\*{0,2}([\d.]+) entità` | tendina «Cosa stai cercando» letta dal modello, non a schermo: la prima lettura ne mostrava 16 |
| entita-amministrazione | 10 | 03/09/2026 | `Amministrazione[ —-]+\*{0,2}([\d.]+) entità` | stessa tendina in area Amministrazione |
| tabelle-web | 68 | 03/09/2026 | `([\d.]+) tabelle in tutto` | conteggio delle voci nell'elenco tabelle del web |

## Fatti non numerici, quindi non controllabili qui

Restano scritti dove servono, ma vale la pena tenerli in vista:

- **Una sandbox è un'azienda dichiarata in `UNICO3_SANDBOX`; ogni altra vale produzione.**
  Il tenant fa parte dell'identificativo: «A3» da solo non nomina niente.
- **Una sandbox non è per forza vuota.** Può contenere storico vero: le operazioni
  irreversibili chiedono conferma anche lì.
- **Il web non fa contabilità né ciclo Installazione.** I movimenti di magazzino sì, dalla
  release 2026.3 (misurato 07/10/2026, carichi DDT). Quella
  parte della guida descrive il terminale Windows. Vedi `cosa-il-web-non-fa.md`.
- **In NET la numerazione e lo stato del preventivo si salvano all'OK del dialogo Numera, e il numero proposto porta l'ultimo suffisso usato** (15/10/2026, sandbox): al primo preventivo dell'anno il suffisso va corretto a mano. NET non blocca la modifica di un preventivo Presentato.
- **Nel web la numerazione di un documento non lo congela** — al contrario di quanto
  dice la guida per Unicò NET.
