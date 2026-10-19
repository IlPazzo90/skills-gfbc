# Unicò Mobile — l'app dei tecnici

Non la piloto io, ma **quasi tutto quello che trovo in ufficio ci è passato attraverso**:
capire cosa il tecnico può e non può fare spiega metà dei dati che leggo.

Tre versioni: **Lite** (gratuita, sola consultazione), **Standard**, **Smart** (a
abbonamento). Android e iOS, **ma Futura consiglia Android**: è lì che tutte le
funzionalità sono garantite.

---

## Il funzionamento offline, e la trappola che ne deriva

L'app funziona **senza rete**: al login scarica in memoria le tabelle che le servono.
Quasi tutta la compilazione dell'intervento avviene offline e **resta salvata nell'app**,
finché non si fa **logout**.

Da qui tre conseguenze operative:

1. Se l'ufficio **modifica una tabella dopo** che il tecnico ha caricato i dati, il
   tecnico deve **`forza aggiornamento`** (con copertura). Unicò propone da sé
   l'aggiornamento quando incontra un dato che non conosce.
2. Le **operazioni massive sulle tabelle** desincronizzano quelle copie locali → errore
   **«nuvoletta rossa»** → **i dati dell'intervento non si salvano e vanno rifatti a
   mano**. Prima di una massiva: **logout di tutti i tecnici**.
3. Nello stato «inviato ma non ancora ricevuto» **non si fa logout**: si perde tutto.

---

## Scheda impianto mobile

Due modi di aprirla: da **ricerca impianto** (sola lettura) e dall'**impegno in agenda**
(con più dati — RdI, note, libretto — e, se il tecnico è abilitato, **modifiche che
arrivano subito in Unicò**, esattamente come se le facesse l'ufficio).

Testata: dati impianto e **tag**, più le icone **telefono** (apre i riferimenti con i
numeri, e toccandone uno parte la chiamata), **matita** (modifica — **inibibile da
configurazione**), **fotocamera** per scansionare il **codice Portal**, e ⋮ per i tag.

Sotto la testata, gli **avvisi colorati**: presenza di **insoluti** · **contratti**, con
il colore del loro stato e **una riga per contratto** · **note fuori norma** ·
**localizzazione non accurata**, che il tecnico può correggere a mano sulla mappa
(diventa verde).

Sezioni: **Richiesta di intervento** (comprese le note importanti e le operazioni da
fare; `visualizza piano completo` mostra tutto il piano di manutenzione — **le correzioni
alle operazioni si fanno solo in compilazione**) · **Contratti** · **Note impianto** per
tipologia · **Installato** (si aggiunge, si modifica, si **sostituisce**, e si appendono
installati figli, tipo un bruciatore su un GT; ci sono i PDF associati: libretto,
esplosi) · **File** · **Interventi** (storico con ricambi e file) · **Riferimenti**
(anche pescando un **installatore da rubrica**) · **Dati libretto** (le sezioni non
gestite altrove; la **sezione 4 si compila da sola** compilando gli installati).

L'icona mappa apre la posizione e **lancia il navigatore** del telefono.

---

## Compilazione intervento — il wizard, passo per passo

Si naviga con `>` e `<`. Alcuni passi dipendono dalla configurazione dell'utente.

**0. Controllo validazioni** *(personalizzazione)* — messaggi **rossi bloccanti**,
**arancioni** solo avvisi. È qui che l'azienda impone i suoi controlli prima che si
cominci.

**1. Testata** — CAT, tipologia intervento, **esito** con la spunta per il **ritorno**,
descrizione, orari. L'inizio arriva dalla RdI, la fine si mette a mano o col tasto
**`adesso`**, poi **`calcola`** riempie la durata. Da qui si aggiungono **aiutanti e
orari aggiuntivi** che l'ufficio non aveva previsto, e si **leggono i dati
dall'analizzatore**.

**2. Operazioni eseguite** — quelle segnate dall'ufficio in **grassetto**, le altre in
grigio; il tecnico può spuntare **anche quelle non previste**.

> Spuntando un'operazione, **la data dell'intervento diventa l'ultima esecuzione e le
> scadenze legale e programmata si ricalcolano sulla periodicità**. È la stessa regola
> misurata dal lato ufficio: **se il tecnico non spunta, la scadenza non si sposta** e
> l'impianto resta scaduto pur essendo stato visitato.

`+` aggiunge operazioni **straordinarie**.

**3. Richiesta attività ufficio** — il tecnico apre un'attività all'ufficio (controllo
saldo, prendi appuntamento, fai un preventivo). **Assegnata a un operatore la vede solo
lui; senza assegnazione la vedono tutti.**

**4. Note** — finiscono **nella stampa del rapportino**.

**5. Contratti** — si rinnovano, si storicizzano, e se ne inserisce uno nuovo (tipologia,
inizio copertura, apparecchio coperto).

**6. Documento** — tipo (rapportino, ricevuta fiscale, fattura immediata, altro);
**`scarica articoli da`** propone il **furgone del tecnico** se assegnato in tabella,
altrimenti il centrale; `segue fattura`; **`fattura a`** propone l'anagrafica cliente se
ha CF e P.IVA, altrimenti gli altri riferimenti — e **un'anagrafica "libera" viene
convertita automaticamente in cliente**; aliquota IVA preferenziale.
Dettagli: articoli di magazzino, manuali, testi; **si elimina una riga trascinandola a
sinistra**; le righe si precompilano dalle **liste materiale** legate a tecnico,
tipologia intervento o contratto.

**7. Numerazione e incasso** — numero automatico o manuale secondo configurazione, poi la
spunta **`incassato`**: se non incassato, chiede tipo di pagamento e banca d'appoggio; se
incassato, chiede importo e tipo, e **se resta un residuo chiede anche pagamento e banca
per quello**.

**8. Foto** — dalla fotocamera o dalla galleria.

**9. Moduli** — **RCEE** e **DAM** dove la regione li prevede, più i **moduli
personalizzati (in giallo)**: contratti particolari, privacy… già **precompilati** con i
dati di ufficio. Per l'RCEE si sceglie **«da esito positivo»** o **«vuoto»**.

**10. Firma** — una firma per tutti i documenti oppure **una per documento**, secondo
l'impostazione del supervisore. `visualizza` mostra il PDF.

**11. Seconda schermata di validazioni** *(personalizzazione)*.

**12. Invio dati** — **è l'unico passo che richiede rete**. Senza segnale l'app ritenta
da sola.

**13. Stampa documenti** — PDF, **stampa su stampante portatile**, invio via mail ai
riferimenti (l'icona rosa manda **tutti i documenti a tutti gli indirizzi** in una volta).

Dopo l'invio **il tecnico può ancora rientrare e correggere**, e reinviare — **finché
l'ufficio non contrassegna l'intervento come «chiuso»**. Da quel momento sparisce dalla
sua app. È la leva che ha l'ufficio per fissare il dato.

---

## Impostazioni lato tecnico

- **Nascondi numero** — attiva di default: le chiamate fatte dall'app partono con numero
  nascosto
- **Timer intervento** — start e stop compilano inizio e fine da soli
- **Cambio password**
- **Tabelle e stampe** — `forza aggiornamento` e scelta della stampante
- **Firma** — la firma del tecnico si registra qui. ⚠️ **Dopo un logout va rifatta.**
- **Analisi combustione** — scelta dell'analizzatore; il nome dice già l'integrazione
  (WiFi, Bluetooth, QR)

## Stampanti portatili supportate

**STAR SM-T400i** · **Zebra ZQ-520** · **Brother RJ-4230B** · **Brother PJ-763**.

L'accortezza che fa la differenza in fase di abbinamento Bluetooth: **non basta che il
telefono veda la stampante come dispositivo — deve vederla come *stampante***, con
l'icona giusta. Abbinarla come device generico **poi non stampa**.

- **Brother RJ/PJ** — codice di sicurezza sui due schermi, `Associa`. Le **PJ non hanno
  schermo**, quindi niente codice.
- **Zebra** — codice a 6 cifre, `associa` sul telefono e **entro un paio di secondi il
  tasto `V`** sulla stampante.
- **STAR** — PIN, di default **`1234`** o **`0000`**.

Poi va **selezionata anche nelle impostazioni dell'app**. Per la STAR si indica pure il
numero di copie per RC e documenti. In alternativa **PrintShare** produce **A4**, da
mandare via mail o stampare altrove.
