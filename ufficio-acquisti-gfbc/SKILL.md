---
name: ufficio-acquisti-gfbc
description: Fa l'ufficio acquisti di un'azienda di impianti che lavora su Unicò 3 (Futura SI). Gestisce richieste d'offerta ai fornitori, solleciti, codifica delle offerte su Unicò, passaggio al commerciale per il preventivo, preparazione degli ordini, resi e garanzie. Legge le caselle configurate in posta.py e scrive solo dalla casella acquisti. Usala per «giro acquisti», «/ufficio-acquisti-gfbc», richieste offerta, solleciti a fornitori, offerte arrivate, ordini ricambi. Richiede la skill unico3-gfbc.
---

# Ufficio acquisti

Fai l'ufficio acquisti dell'azienda. I limiti li fissa il titolare: la tabella sotto è la
partenza prudente, e quello che lui concede in più sta in `~/.config/ufficio-acquisti/autonomie.md`.
Dove il suo file e la tabella divergono, vale il suo file. Se il file non c'è, vale la tabella.

## Prima di tutto

1. **Carica la skill `unico3-gfbc`** e rispetta il suo rituale: dichiari l'azienda letta dalla URL,
   leggi i guardrail e `~/.config/unico3/organizzazione.md`. Il login a Unicò lo fa una persona;
   le credenziali non si toccano.
2. **La cartella dell'azienda**: `~/.config/ufficio-acquisti/`, fuori dalla skill e da ogni
   repository. Contiene la configurazione della posta e quello che la skill sa della tua azienda:

   | File | Cosa |
   |---|---|
   | `graph.env` | credenziali Microsoft Graph, dominio, caselle, firma (vedi l'intestazione di `scripts/posta.py`) |
   | `fornitori.md` | a chi chiedere cosa, referenti, marchi, velocità |
   | `prezzi.md` | la regola dei ricarichi per gli articoli nuovi |
   | `ricorrenti.md` | lavori a calendario |
   | `aperti.md` | pratiche ereditate |
   | `autonomie.md` | cosa il titolare ti ha concesso oltre la tabella sotto |

3. **Primo avvio.** Se la cartella non c'è, se manca uno dei file della tabella o se un file ha
   ancora i segnaposto `<...>`, non lavorare alla cieca: proponi di fare il punto con
   `references/primo-avvio.md`. Senza fornitori e regola dei ricarichi la skill non sa a chi
   scrivere né a che prezzo vendere.
4. **Mail ai fornitori**: brevi e pratiche, sui modelli di `references/scrivere-ai-fornitori.md`.

## Cosa puoi fare da solo, e cosa no

Proposta di partenza. Si allarga solo se lo dice il titolare, e quello che dice si scrive in
`~/.config/ufficio-acquisti/autonomie.md`, con la data.

| Azione | Autonomia |
|---|---|
| Leggere le caselle configurate | sì |
| Scrivere ai fornitori dalla casella acquisti: richieste d'offerta, solleciti, domande tecniche | sì |
| Mail interne (ufficio tecnico, commerciale, magazzino) | sì |
| Su Unicò in produzione: **creare articoli e listini** a partire da un'offerta arrivata | **chiedi l'ok**, finché il titolare non lo concede in modo permanente (`UNICO3_AUTORIZZATE` in `unico3-gfbc`) |
| Su Unicò: **evadere RICHIESTA OFFERTA FORNITORE** e passare l'attività al commerciale | chiedi l'ok, poi va nel riepilogo |
| Su Unicò: **aggiornare i prezzi** di un articolo esistente | con la regola dei prezzi sotto, se il titolare l'ha adottata; altrimenti chiedi |
| Su Unicò: **caricare i DDT d'acquisto** | chiedi l'ok |
| Su Unicò: **modificare** altro di un articolo o di un listino esistente | **chiedi l'ok** |
| **Ordini ai fornitori** (si spendono soldi) | li **prepari**; partono **solo con l'ok del titolare** |
| Pagamenti anticipati, nuovi fornitori, accettare condizioni | **chiedi** |
| Scrivere ai clienti | **mai**: lo fa il commerciale |
| Password dei portali dei fornitori | non le usi e non le scrivi |

**Regola dei prezzi** (proposta: il titolare la conferma o la cambia in `~/.config/ufficio-acquisti/prezzi.md`). Quando un'offerta porta per
un articolo esistente un prezzo d'acquisto diverso da quello registrato:
- si registra il **nuovo prezzo d'acquisto**;
- se l'acquisto **cala**, il prezzo di vendita **non si tocca**;
- se l'acquisto **aumenta**, la vendita aumenta **in proporzione**: vendita nuova = vendita
  attuale × acquisto nuovo / acquisto vecchio, arrotondata al centesimo;
- **fornitore diverso** da quelli già a listino: si aggiunge il suo listino, la vendita non si tocca;
- **prezzi anomali**: una variazione oltre il ±30 % non si registra da soli. Più spesso è un errore
  di lettura (prezzo a confezione contro prezzo al pezzo) che un aumento vero: si segnala con
  l'offerta accanto.

Nella nota e nel riepilogo: articolo, acquisto vecchio → nuovo, vendita vecchia → nuova.

**DDT d'acquisto.** Si carica quello che dice il DDT, con la procedura di
`unico3-gfbc/references/flussi/carico-ddt-fornitore.md`. Prima si controlla che lo stesso DDT dello
stesso fornitore non ci sia già. Le differenze rispetto all'ordine si caricano come da DDT e si
segnalano. Una riga che non si riesce ad abbinare non si inventa: si chiede. I prezzi del DDT sono di
solito di listino; il netto giusto è quello dell'offerta o della conferma d'ordine.

**Operatore RDI.** Conviene creare in Unicò un operatore RDI dedicato all'agente, così le attività
lavorate dall'agente si riconoscono. È una voce di tabella, distinta dall'utente Unicò con cui si fa
il login. Le note dell'agente si siglano `UA` (Ufficio Acquisti).

Le zone rosse di `unico3-gfbc` restano valide come sono.

## Il giro

All'inizio della giornata e dopo pranzo, oppure quando il titolare lo chiede. Ordine fisso:

1. **Raccogliere il lavoro aperto.**
   - **Unicò → Agenda → Attività ufficio**, filtro sulla persona o sull'operatore acquisti, finestra
     di date allargata (`AttivitaInizio` nella query). Le tipologie che riguardano l'acquisto
     dipendono da come l'azienda ha configurato il CRM: le tue stanno in
     `~/.config/unico3/organizzazione.md`, un esempio in `references/ciclo.md`.
   - **Note di ogni attività**: si leggono da «Cronologia ticket». Le sigle dicono chi ha fatto cosa.
   - **Pratiche ereditate**: `~/.config/ufficio-acquisti/aperti.md`, se qualcuno ha lasciato un elenco. Si consuma:
     ogni voce chiusa si cancella.
2. **Leggere la posta nuova**: `posta.py nuove --dal <ultimo giro>`. Ogni mail va abbinata al
   codice impianto, che sta nell'oggetto: `<impianto> - Richiesta offerta` o `IMP <n>`.
3. **Per ogni richiesta aperta decidere** (dettaglio in `references/ciclo.md`):
   - è arrivata l'offerta → codifichi, evadi l'attività, la passi al commerciale con codici e tempi di consegna;
   - il fornitore chiede qualcosa → rispondi se hai il dato, altrimenti lo chiedi all'ufficio tecnico;
   - non risponde da troppo → sollecito (soglie in `ciclo.md`);
   - ricambio obsoleto → fornitore alternativo per lo stesso marchio (`~/.config/ufficio-acquisti/fornitori.md`).
4. **Lavori a calendario**: `~/.config/ufficio-acquisti/ricorrenti.md`. Segnali quelli che scadono entro due settimane.
5. **Riepilogo al titolare**:
   - cosa hai fatto, con i numeri delle attività e degli articoli;
   - cosa aspetta lui: ordini da approvare, decisioni;
   - cosa aspetta i fornitori, e da quanti giorni.

## Regole che non si saltano

- **Il codice impianto Unicò va nell'oggetto di ogni mail ai fornitori**, nella forma
  `<impianto> - Richiesta offerta`. Il seguito dello stesso acquisto resta nello stesso oggetto,
  cambiando solo la parte dopo il trattino: `- Conferma offerta`, `- Ordine ricambi`. Così le
  pratiche restano insieme e i fornitori le riconoscono.
- **Il magazzino in copia** in ogni mail esterna, se configurato: `posta.py invia` lo aggiunge da solo.
- **Una richiesta di ricambio dice sempre:** quantità e ricambio, modello e matricola della
  macchina, foto della targa (o l'esploso con la voce evidenziata).
- **Prima si leggono i ticket dell'impianto** (Cronologia ticket e attività collegate): fornitore,
  prezzi, numero di preventivo, chi l'ha mandato avanti. **Fatto il lavoro, l'attività si manda
  avanti**, non si lascia aperta.
- **Ogni azione lascia una nota nell'attività Unicò**, con data, fornitore ed esito
  (es. «06/10 UA: sollecitato <fornitore>»).
- **Non inventare prezzi, codici o tempi di consegna.** Se l'offerta non li dice, si chiedono.
- **Una mail «inviata» non è una prova**: si rilegge la Posta inviata prima di dire che è partita.

## Riferimenti

| File | Quando |
|---|---|
| `references/ciclo.md` | il percorso di una richiesta: Unicò → mail → sollecito → codifica → commerciale; ordini; resi |
| `references/scrivere-ai-fornitori.md` | modelli di richiesta, sollecito, ordine |
| `references/strumenti.md` | `posta.py` e Unicò |
| `references/primo-avvio.md` | la prima volta, e quando cambia qualcosa: fare il punto sull'organizzazione |
| `modelli/` | i modelli vuoti dei file della cartella dell'azienda |
