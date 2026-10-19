# La mia organizzazione su Unicò

Compilato il <GG/MM/AAAA> · release Unicò <es. 2026.3>
Procedura: `references/primo-avvio.md` della skill `unico3-gfbc`.
Marcature: `[letto GG/MM/AAAA]` da Unicò, `[detto dal titolare]` (o da un altro ruolo) dall'utente.

Questo file contiene dati dell'azienda: resta su questo computer, fuori da ogni repository.

## Aziende

| Azienda | Nome | Produzione o prova | Note |
|---|---|---|---|
| C<tenant>/A1 | <...> | <produzione> | <...> |

Variabili di shell impostate: `UNICO3_SANDBOX=<...>` · `UNICO3_AUTORIZZATE=<vuota>`

## Persone e ruoli

| Ruolo | Chi | Come raggiungerlo |
|---|---|---|
| Titolare (dà l'ok alle scritture) | <...> | <...> |
| Login a Unicò per la skill | <utente Unicò> | |
| Commerciale | <...> | <...> |
| Ufficio tecnico | <...> | <...> |
| Magazzino | <...> | <...> |
| Amministrazione | <...> | <...> |

Operatore RDI dell'agente: <nome nella tabella OperatoreRdI, oppure «nessuno»>

# Configurazione per azienda

Una sezione per ogni azienda censita (punto 4 del primo avvio). La skill usa solo quella
dell'azienda letta dalla URL; un'azienda senza sezione non è censita.

## C<tenant>/A<n> — <nome>

### CRM: attività ed esiti

| Tipologia attività ufficio | Chi la fa | Esito → `AzioneSuccessiva` → destinazione |
|---|---|---|
| <...> | <...> | <esito> → <ProgrammaAttivita / ChiudiTicket / ApriRdI> → <tipologia> |

Tipologie RDI in uso: <...>
Tipologie intervento in uso: <...>
Tipologie impianti in uso: <...>

### Manutenzione e contratti

| Sigla operazione | Significato | Periodicità tipica |
|---|---|---|
| <...> | <...> | <...> |

Tipologie contratti: <...>

### Magazzino

| Magazzino | Uso |
|---|---|
| <...> | <ricambi / finiti / furgoni ...> |

Causali usate per il carico DDT fornitore: <...> · per i resi: <...>
Listino base: <...> · listino di vendita: <...>

### Articoli di servizio

| Segnaposto ART_… nei file della skill | Codice articolo da noi |
|---|---|
| `ART_MANODOPERA` | <...> |
| `ART_MANODOPERA_PREV` | <...> |
| `ART_MATERIALE_PREV` | <...> |
| `ART_MATERIALE_GENERICO` | <...> |
| `ART_DIRITTO_CHIAMATA` | <...> |
| `ART_TRASPORTO` | <...> |
| `ART_CANONE` | <...> |
| `ART_MAN_PDC` | <...> |
| `ART_MAN_IBRIDO` | <...> |

### Numerazioni e documenti (solo lettura)

<registri in uso e tipologie documenti di intervento>

# Abitudini (tutta l'organizzazione)

- Codice impianto nelle mail e nelle note: <es. «IMP 123»>
- Foto degli impianti: <dove stanno>
- Aree di Unicò non usate: <...>
- Cosa la skill non deve mai fare, oltre alla zona rossa: <...>
