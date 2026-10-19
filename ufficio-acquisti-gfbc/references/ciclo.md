# Il ciclo di una richiesta

Le tipologie di attività e gli esiti qui sotto sono **un esempio reale** di CRM Unicò configurato
per un'azienda di assistenza impianti. I nomi nella tua installazione possono essere diversi:
la prima volta che li incontri, leggili nel dialogo Evadi e correggi questo file.

## 1. Come nasce: la catena su Unicò

Su Unicò le attività di un ticket si incatenano tramite l'esito (vedi
`unico3-gfbc/references/crm-ticket.md`). Una catena tipica:

```
ELABORAZIONE PREVENTIVO   (commerciale)  --esito «Codifica articoli e prezzi»-->
CODIFICA ARTICOLI E PREZZI               --esito «Richiesta offerta fornitore»-->
RICHIESTA OFFERTA FORNITORE (assegnata all'ufficio acquisti)
```

**Catena del lavoro accettato**, esempio: `ELABORAZIONE PREVENTIVO` esito «Inviato a cliente» →
`RISCONTRO PREVENTIVO` esito «Accettato» → `VERIFICA MATERIALE` esito «Materiale da ordinare» →
`CONTROLLO ACCETTAZIONE` lasciata **pianificata**: è l'attesa della merce del fornitore, si evade al
ricevimento. Nel dialogo Evadi l'Operatore RDI parte dall'utente collegato: si mette l'operatore
dell'agente. Al passo dopo, per lasciare l'attività libera si sceglie «Non selezionato», in testa
alla tendina. Tutto avviene in un solo wizard: si evade un passo, AVANTI, l'ultimo si pianifica.

Il commerciale mette nella nota cosa serve: ricambio, macchina, matricola, dove sono le foto.
**La nota del commerciale è il capitolato della richiesta.**

Esiti tipici di RICHIESTA OFFERTA FORNITORE: `Offerta ricevuta` · `Non fornibile - verifica alternativa` ·
`Articolo introvabile/irreperibile` · `Annulla ticket`. Con **Offerta ricevuta** il dialogo propone
CODIFICA ARTICOLI E PREZZI: se gli articoli sono già codificati si sceglie **Evadi ora** con esito
`Articoli codificati`, AVANTI, e il passo dopo è **ELABORAZIONE PREVENTIVO**: Pianifica, Operatore RDI
il commerciale, «Da eseguire entro» scritto a mano (il setter da script non lo prende), nota con
codice, acquisto, vendita e disponibilità.

## 2. La richiesta al fornitore

- **Scelta del fornitore:** uno specializzato per marchio, da `fornitori.md`. Ne interpelli due solo
  se il prezzo è alto, la disponibilità è dubbia o il primo ha già detto «obsoleto».
- **Oggetto:** `<impianto> - Richiesta offerta`. Il testo segue `scrivere-ai-fornitori.md`.
- **Foto:** di targa e ricambio, dagli allegati del ticket Unicò o da dove l'azienda le raccoglie.
  Senza foto e matricola non si scrive: si chiedono all'ufficio tecnico.
- **Dopo l'invio:** nota nell'attività Unicò, per esempio
  `06/10 UA: chiesta offerta a <fornitore> (<referente>@) - <cosa>`. Attività aperta: matita del
  pannello → «Modifica attività ufficio» → campo Note, riga nuova in testa → CONFERMA (non evade).
  Attività evasa: menu ⋮ → «Aggiorna note».

## 3. Solleciti

Soglie di partenza, da tarare sui tempi dei tuoi fornitori:

| Caso | Primo sollecito | Poi |
|---|---|---|
| Cliente fermo (guasto, urgenza) | dopo **3 giorni lavorativi** | secondo dopo altri 3; poi fornitore alternativo e avviso al titolare |
| Normale | dopo **6 giorni lavorativi** | secondo dopo 6; dopo il secondo senza risposta, fornitore alternativo |
| Il fornitore ci ha fatto una domanda | **nessun sollecito**: la palla è nostra | rispondi o chiedi il dato all'ufficio tecnico |

I fornitori lenti si annotano in `fornitori.md`: a loro il sollecito va a tutti gli indirizzi conosciuti.

## 4. L'offerta arriva → codifica → commerciale

1. **Leggi l'offerta** (`posta.py leggi` / `allegati`). Ti servono: codice del fornitore,
   descrizione, prezzo netto, sconto, trasporto, **tempi di consegna**, validità. Se mancano i tempi
   di consegna li chiedi nella stessa risposta: il commerciale ne ha bisogno.
2. **Cerca su Unicò** se l'articolo esiste già (webservice `/magazzino/articoli/codice/{c}`, oppure
   la ricerca globale). Se esiste allo stesso prezzo, non fai nulla. Se esiste con un altro
   fornitore, aggiungi il listino del nuovo. Se è lo stesso fornitore con un prezzo diverso, applichi
   la **regola dei prezzi** di `SKILL.md`. Ogni altra modifica a un articolo esistente richiede l'ok.
3. **Crea l'articolo** se non c'è, con la procedura di `unico3-gfbc/references/magazzino.md`:
   codice del produttore se è certo, altrimenti quello del fornitore; listino del fornitore con il
   **codice per ordine**; descrizione in MAIUSCOLO. Prezzo di vendita: `references/prezzi.md`.
   Quando la regola non copre il caso, nel riepilogo scrivi che il prezzo va confermato.
4. **Verifica** via webservice che articolo e listino esistano con i valori giusti.
5. **Evadi RICHIESTA OFFERTA FORNITORE** con l'esito che passa a ELABORAZIONE PREVENTIVO, assegnata
   al commerciale. La nota contiene, una riga per articolo:
   `<codice> <descrizione> - <fornitore> - € <netto> - consegna <tempi> - offerta <n.> del <data>`.
   Se un ricambio è obsoleto, scrivilo insieme all'alternativa proposta.
6. Le **altre offerte** della stessa pratica che arrivano dopo aggiungono solo il listino, più una
   riga di nota all'attività del commerciale se è ancora aperta.

## 5. Preventivo accettato → materiale → ordine

Quando il commerciale manda avanti un preventivo, su Unicò nasce **VERIFICA MATERIALE** per
l'ufficio acquisti:

1. Controlla le giacenze delle righe del preventivo (webservice giacenze o scheda articolo).
2. Per ogni riga mancante **prepara l'ordine**: fornitore, codice per ordine, quantità, prezzo
   dell'offerta, consegna in sede o ritiro a banco.
3. **Mostra l'ordine al titolare** e aspetta l'ok. Poi lo mandi dalla casella acquisti nello stesso
   oggetto della richiesta, con `- Ordine ricambi`.
4. Annota il numero della conferma d'ordine e la data di consegna prevista. Alla consegna il DDT si
   registra su Unicò come **carico da fornitore**: `unico3-gfbc/references/flussi/carico-ddt-fornitore.md`.

**L'ordine formale in PDF** si emette da Unicò NET (Magazzino → «Ordine a fornitore»), con i prezzi e
il pagamento concordati, numerato, stampato con Prezzi e Logo. Procedura:
`unico3-gfbc/references/flussi/ordine-fornitore-net.md`. La mail con il PDF parte solo con l'ok del titolare.

## 6. Resi, garanzie, riparazioni

- **Reso di un ricambio sbagliato o difettoso:** prima l'autorizzazione del fornitore, poi il DDT di
  reso da Unicò, il collo e il ritiro del corriere.
- **Garanzie dei costruttori:** spesso il ticket lo apre il distributore o il centro assistenza;
  si mandano matricola, foto e rapportino.
- **Fornitori che lavorano a ticket** (Zendesk e simili): si risponde sempre nel thread del ticket.
