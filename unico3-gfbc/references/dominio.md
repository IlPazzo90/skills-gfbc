# Dominio Unicò 3

Quello che la skill deve sapere per non fare danni. Estratto dallo spec di
progetto; la fonte primaria sono il wiki Unicò NET e i webinar di Futura SI, che stanno
sul portale Futura e non sono inclusi qui.

**Attenzione:** il wiki descrive soprattutto Unicò NET. Dove il web si comporta
diversamente è segnalato. La fonte aggiornata sul web è la doc ufficiale, che si
legge solo da dentro la sessione autenticata.

## Impianto ≠ Cliente
L'impianto è la scheda tecnica (area Assistenza); il cliente è l'anagrafica (dati
contabili). Un impianto può non avere cliente collegato. Più impianti possono fare capo a
un unico cliente.

## Classi di impianto
**Riscaldamento semplice** (un generatore, tre operazioni: manutenzione ordinaria, analisi
di combustione, rilascio bollino — visualizzate nella scheda del generatore, non in un
piano separato). **Riscaldamento complesso** (fino a 999 generatori, piano di manutenzione
personalizzato). **Condizionamento / Refrigerazione** (fino a 999 gruppi frigo, ciascuno
con fino a 24 unità interne). **Altro** (tipologie libere: trattamento acqua, solare,
piscine, estintori…). **Teleriscaldamento** (modulo opzionale).
Dal DPR 74/2013 esistono anche gli **impianti misti**.
La tipologia si può cambiare dopo l'inserimento solo se congruente (il programma impedisce
di trasformare un riscaldamento in un condizionamento se ci sono già generatori).

## Codici
Il codice impianto è numerico progressivo automatico, forzabile. `Assegna codice libero`
recupera i buchi. Stesso meccanismo per i codici Cliente/Fornitore.
Il campo `Gruppo` (6+3 caratteri alfanumerici) serve a classificare per le ricerche.
I `Tag` (fino a 5 per impianto) sono solo SMART.

## Struttura dell'installato
Gerarchia padre-figlio: impianto → gruppi termici (`G1`…`G999`) / gruppi frigo
(`R1`…`R999`) / componenti → figli (bruciatori, componenti, unità interne `U01`…).
I vincoli di parentela sono imposti dal programma.
Nel web l'inserimento parte dal **codice prodotto o modello**: si cerca, e la tipologia la
deduce il sistema dalla tabella. Modelli non tabellati ammessi solo per i componenti, per
retrocompatibilità, e sconsigliati.

## Riferimenti impianto — 9 tipologie
Occupante, Proprietario, Amministratore, Terzo Responsabile, Conduttore, Progettista,
Installatore, Cliente di Fatturazione, Referente (×2). Alcuni collegabili a un'anagrafica,
altri a inserimento libero. Due flag: **Responsabile impianto** (solo sui primi quattro,
pilota la stampa sui rapporti di controllo) e **Destinatario corrispondenza** (pilota
indirizzi ed SMS; in mancanza vale l'indirizzo della scheda impianto).

## Note impianto — 4 tipi con limiti diversi
| Tipo | Limite | Stampa | Spia |
|---|---|---|---|
| Principali | 255 caratteri | sulle schede di chiamata | verde |
| Storiche | 4096 | solo su scheda completa | — |
| Riservate | 4096 | mai | rossa |
| Fuori norma | 256 | — | gialla |

Priorità di accensione della spia: verde → gialla → rossa.

## Le spie della scheda impianto
Impianti collegati (verde = primario, giallo = secondario), Libretto (verde = compilato),
Manutenzione scaduta, Ticket aperto (SMART), Richiesta di intervento aperta, Saldo
scoperto, Contratto (verde attivo / rosso scaduto), Note, Blocco cliente (lucchetto).
Il blocco cliente si accende inserendo una nota di tipo `CLIENTE BLOCCATO` sull'anagrafica:
**si propaga a tutti gli impianti collegati**.

## Contratti
Stati: **Attivo** / **Storico**. Riga verde se coperto alla data odierna, rossa se scaduto.
Inserendo un nuovo contratto attivo con data di stipula successiva, il precedente viene
**storicizzato automaticamente**. Più contratti attivi sullo stesso impianto solo se
l'opzione è abilitata.
La tipologia contratto può portare un **Listino Contratto**, che in fase di emissione del
documento di intervento ha priorità sul listino del cliente.

## Piano di manutenzione
Per tutte le tipologie tranne il riscaldamento semplice. Ogni operazione ha:
`Tipo` (da tabella), `Periodicità` (o `MANUALE` se non fissa), `Precedente` (aggiornata dagli
interventi) e **due scadenze distinte: Legale e Programmata**. La legale è quella di norma,
la programmata è quella effettivamente pianificata (normalmente ≤ legale).
Il wiki raccomanda **non più di 6-7 operazioni** per piano.
In SMART le operazioni si possono assegnare alla singola macchina o al singolo componente.
Esiste un piano di manutenzione di default per tipologia di impianto.

## RDI (Richiesta di Intervento) — tre stati
**Registrata** (dati minimi: data e tecnico; non ancora in agenda) → **Programmata** (con
data, ora e durata: diventa appuntamento) → **Evasa** (solo quando si redige il consuntivo
dell'intervento).
Il tecnico è obbligatorio; se ignoto si usa la voce precodificata `Non segnalato`. Di
default viene proposto l'ultimo tecnico che ha visitato l'impianto.
La durata si esprime in multipli di mezz'ora.
Colori nello storico chiamate: rosso = aperta, nero = evasa, sfondo giallo = richiamo.
Il **Richiamo** è la chiamata che il cliente chiede di rimandare; si gestisce in una
sezione dedicata dell'agenda e diventa appuntamento cambiando tipologia.
Esiste `Impegna Aiutante` per bloccare in agenda anche un secondo tecnico.

## Agenda
A sinistra gli **impegni** non programmati, su quattro cartelle: Manutenzioni, Richiami,
Chiamate, Altri impegni. A destra gli **appuntamenti**.
Impegno → appuntamento richiede tecnico + data + ora + durata. Il programma **segnala e
impedisce** le sovrapposizioni sullo stesso tecnico. Gli appuntamenti si spostano in
drag & drop e si colorano con il colore della zona.
Planning settimanale (un tecnico, 7 giorni) e giornaliero (tutti i tecnici).
I **memo** sono post-it elettronici con data, destinatario (o `TUTTI`) e testo.

## Intervento
Spuntare un'operazione come eseguita **aggiorna automaticamente le date di scadenza
successive** in base alla periodicità; togliere la spunta torna indietro. Le date restano
modificabili a mano.
**Se le operazioni non vengono spuntate, le scadenze successive non vengono generate.**
È il perno di tutto il ciclo manutenzione.
Documento rilasciato: Ricevuta Fiscale (corrispettivo), Rapportino, Fattura o Fattura
accompagnatoria, oppure nessuno. Il flag `Segue fattura` toglie gli importi dai
corrispettivi e pretende un cliente in anagrafica (con CF o P.IVA).
Il prelievo merce viene proposto dal **furgone associato al tecnico**, altrimenti dal
magazzino centrale.
Il totale documento è forzabile "a corpo": se fuori quadratura, la stampa mostra solo il
totale complessivo.
La sessione net-mobile è `Aperta` finché non viene convalidata a `Chiuso`.

## Ricerche (estrazione dati)
Presenti in ogni area, sotto `ESTRAZIONE DATI`. Filtri, poi funzioni di utilità.

- `%` davanti a una stringa = "contiene"; concatenabile: `%valvola%sfera%`. Senza `%` è
  "inizia con". La ricerca ignora maiuscole/minuscole.
- Ricerche per **intervalli** su campi numerici e data.
- **Cattura**: costruisce sottoinsiemi e li incrocia fra ricerche diverse; il check
  `liberi` seleziona l'insieme complementare. È il modo per superare la settorialità delle
  singole maschere.
- **Ordina** (doppio click sulla riga = ordine inverso), **Totali colonna** (menu Utilità),
  **Esportazione**.
- **Personalizza** (menu Utilità, solo su alcune ricerche): campi in rosso = criteri
  personalizzabili; preposizione `AND`/`OR`; operatori `LIKE` (default, "inizia con"), `=`,
  `<>`, `>`, `>=`, `<`, `<=`. Permette anche di scegliere le colonne della griglia.
- Selezione in griglia: `CTRL` + click per singole righe, `SHIFT` per blocchi,
  **`CTRL + T` per selezionare tutto**.
- **Esportazione**: Excel (default), Testo/CSV con separatore `;`, OpenOffice. Si scelgono
  i campi con i due riquadri. **Al termine parte il client FTP**: il file non arriva
  direttamente sul PC, va scaricato da `Esplora Risorse`.

## Tabelle
~70 tabelle. Nel web sono in un unico elenco (icona in basso a sinistra), ricercabili per
nome, raggruppabili per area; su NET sono divise per area.
Meccanica comune: `Aggiungi`, `Salva`, `Elimina`, e il check **`Escluso da liste`** che
nasconde una voce senza perderne lo storico.
Nel web la griglia è in stile Excel: ordinamento, raggruppamento per colonna con conteggi,
filtri, colonne mostrabili/nascondibili dal menu "tre linette" sull'intestazione, ripristino
colonne. Esportazione PDF/Excel dal menu in alto a sinistra — sostituisce le stampe, che
nel web non ci sono.
Si possono creare voci al volo dal campo tabellato di una scheda: vengono create e
assegnate in un colpo solo.
Tabelle notevoli: Comuni (con Ente di controllo, Zona, durezza acqua, periodo di
riscaldamento, import ISTAT), Zone (sigla + colore, usati in agenda), Tecnici (sigla,
colore, lista materiale, numerazione automatica di RF e rapportini, certificazione F-Gas,
competenze, orari, impegni/ferie), Numerazioni (i contatori dei documenti), Tipologie
Documenti (decide se un documento genera movimenti di magazzino, contabili o nessuno),
Operazioni Manutenzione, Tipologie Intervento (con lista materiale collegata), Tag Impianti.

## Magazzino — quattro tipologie di articolo
**Semplice**, **a matricola** (quantità sempre 1, matricola obbligatoria), **fuori
inventario** (manodopera, trasferte, diritto di chiamata — escluso da ogni computo di
inventario), **a distinta** (kit di articoli semplici o fuori inventario).
La tipologia si può cambiare **solo se l'articolo non è mai stato movimentato**.
La **manodopera** si riconosce così: articolo fuori inventario, unità di misura `Ore` o
`min`, e la parola "manodopera" nella descrizione. È la convenzione che regge la
valorizzazione delle commesse.
Magazzino centrale + magazzini periferici, cantieri e furgoni: i trasferimenti interni non
cambiano la giacenza complessiva; solo scarico a cliente e carico da fornitore la muovono.

## Preventivi
Testata (cliente, descrizione, testo iniziale e finale dal Glossario, validità, pagamento,
note interne mai stampate), righe di dettaglio, poi `Numera` — che assegna il numero **e**
cambia lo stato.
Righe speciali: **Totali di sezione** (fino a 99) e **Salto pagina**. Le sezioni del
preventivo diventano le **sezioni della commessa** che ne deriva.
Funzioni: `Costo` (margini vs listino), `Fabbisogno` (materiale necessario), `Ricalcolo`
(irreversibile: sovrascrive i prezzi senza possibilità di recuperarli — la skill non lo
esegue in produzione; su una sandbox chiede conferma, vedi `references/guardrail.md` §5.2),
importazione righe da altri preventivi.
La stampa è personalizzabile sezione per sezione (intestazione, prezzi, sconti, importi,
descrizioni estese, distinte…).

## Documenti — la meccanica comune
Tre fasi sempre: **testata → righe di dettaglio → numerazione/registrazione**. Dopo la
registrazione il documento è congelato **nel terminale**; nel web la numerazione **non congela** (misurato — `flussi/intervento-e-documento.md`).
Tipi di riga: Articolo, Articolo a distinta, Articolo manuale, Testo (dal Glossario).
Sconti in cascata ammessi (`20+10+5`).
Il prezzo arriva dal **listino corrente** evidenziato in azzurro nella maschera; cambiarlo
lo rende corrente fino alla modifica successiva.

## Catasti regionali
Il wiki elenca **CIRCE** (Veneto), **CURIT** (Lombardia), **CIT** (Piemonte), **AFE**
(Firenze). L'Emilia-Romagna ha **CRITER**, che nel wiki non compare. Il wiki è vecchio:
**Unicò invia a CRITER**, via web service, anche dalla scheda intervento
(`adempimenti.md`). L'invio resta zona rossa (irreversibile verso terzi, `guardrail.md`):
l'agente non invia né registra niente al catasto.
Le periodicità dei controlli vengono dalla norma regionale, che in Emilia-Romagna attua il
DPR 74/2013: RR 1/2017, Allegato B (`flussi/piani-manutenzione.md`). Quelle CURIT
(Lombardia) non sono ancora state scritte.

## File allegati
**Massimo 2 MB per file.** Formati ammessi: doc/docx/rtf, xls/xlsx, ppt/pptx, pdf,
jpeg/bmp/wmf/png/gif, txt/csv/xml, an5/an6 (ANGAISA), f55 (DiCo), documenti OpenOffice,
mdb, rib, rar/zip.
Su NET i file devono passare dal client FTP (`Esplora Risorse`); nel web si caricano in
drag & drop con anteprima inline.

## Scorciatoie da tastiera (Unicò Web)
Rendono l'automazione molto più stabile del click a coordinate.

| Tasto | Effetto |
|---|---|
| `\` | focus sulla ricerca rapida (in alto a destra) |
| `Alt` + `←` / `→` | passa da un tab aperto all'altro |
| `Alt` + `↑` / `↓` | scorre le sezioni della scheda impianto; `Invio` per entrare |
| `Tab` / `Invio` | navigazione e conferma in tutti i form |
| `CTRL + T` | seleziona tutte le righe di una griglia |

## Altre interazioni del web
La modifica si apre cliccando **dentro il riquadro**, non su una matita; alla conferma il
dato è già salvato. La barra icone a sinistra è l'area di lavoro e cambia colore secondo la
scheda aperta; la chiave inglese crea un nuovo impianto. L'eliminazione di un impianto
richiede di digitare "elimina".

## Validazioni Mobile
Configurate dall'azienda, non da Futura. Blocchi (rosso) e avvisi (giallo), a due momenti:
prima della chiusura intervento e prima dell'invio dati. Coprono dati obbligatori
(matricola, data installazione, dati catastali, POD/PDR), coerenza fra passaggi, F-Gas
banca dati, `segue fattura` che pretende CF o P.IVA. Esiste la tabella
`Voci di validazione intervento`.
Le **precompilazioni** (richiedono il modulo magazzino) riempiono le righe del rapportino
da liste materiale collegate a tipologia intervento, operazioni, contratti o tecnico.
Esistono **righe nascoste** (es. costo orario del tecnico): visibili internamente, non al
cliente.
I **moduli personalizzati** (contratto, privacy, garanzie di marca) possono **scrivere sulla
scheda anagrafica** — la privacy compilata imposta "informativa consegnata" e "consenso
prestato".
