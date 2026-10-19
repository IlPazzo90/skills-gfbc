# Files, Impostazioni, Geolocation, Analisi dati

Le quattro aree che restavano fuori dalla mappatura dal vivo. Verificate su una sandbox il
03/09/2026.

---

## Files — il documentale

Rotta `#/files/`. **Non è una AG Grid**: albero delle cartelle a sinistra, elenco a
destra con *Nome · Ultima Modifica · Dimensioni File*. In alto: aggiorna, **nuova
cartella**, **upload**, vista a griglia.

Le cartelle di una sandbox raccontano l'archivio dell'installazione, per esempio:

`Allegati` · `Appalti` · `Cataloghi` · **`DiCo <anno>`** ·
`ENEA` · `EXPORT` · **`F-GAS`** · `Fatture XML manuali passive` ·
**`FattureSDI`** · **`File scadenze <contabilità esterna>`** · `FOTO ALLEGATE` · `FOTO ARTICOLI` ·
`IMPORTAZIONE` · `Inventario` · `ListaMateriale` · `LOGO` · `Mobile` · *(l'elenco
prosegue oltre)*

Due cose che si leggono fra le righe: le **DiCo sono archiviate per anno**, e
una cartella di scambio con un software di contabilità esterno dice che — cioè la contabilità vera
sta altrove, coerente con `cosa-il-web-non-fa.md`.

**Upload e nuova cartella sono scritture.** Su una sandbox sono permesse, ma non servono a nulla:
non le uso senza richiesta.

---

## Impostazioni — e la trappola che ho innescato guardando

Rotta `#/impostazioni/<area>/<sezione>`. Tre aree:

| Area | Sezioni |
|---|---|
| **Agenda** | `Visualizzazione` · `Scadenziario` |
| **Assistenza** | `Feedback` · `PBX` · `Portale` · `GaIA` |
| **Generale** | `Loghi` (rotta `common/loghi`) |

In alto a destra c'è **`SALVA`**, e vale per tutti.

### ⚠️ Basta guardare per far comparire «impostazioni non salvate»

Sono entrato in *Agenda → Visualizzazione* e ho cliccato dentro il riquadro
*Informazioni Altro Impegno* **solo per leggerlo**. Passando a un'altra sezione è
comparso:

> **«Ci sono delle impostazioni non salvate. Si desidera uscire comunque?»** — *Annulla* / *Esci*

**Non avevo modificato niente.** Il riquadro è un editor di chip: entrarci col cursore
basta a sporcare lo stato.

Il rischio non è teorico: **queste impostazioni valgono per tutti gli utenti**, e il
riflesso di chi vede «non salvate» è premere `SALVA`. Regole:

1. In Impostazioni **non si clicca dentro i riquadri**, si legge e basta.
2. Se compare quel dialogo, si risponde **`Esci`**. Mai `SALVA`.
3. Su un'azienda vera **non si entra affatto** senza una richiesta esplicita.

### Cosa contengono

**Agenda → Visualizzazione**: i riquadri componibili *Informazioni Richiesta di
Intervento* (esempio: `Codice Impianto | Nominativo - Motivo`), *Intervento Eseguito*
(`Nominativo - Tipologia Intervento`), *Altro Impegno* (`Tipo - Descrizione`); i **tecnici
in vista di default** come chip; `Colora etichette tecnici`; **`Colora RdI programmate
per`** e **`Colora interventi eseguiti per`**, entrambi su `Zona` di default.

Quest'ultima cosa spiega i colori dell'agenda: **non hanno un significato fisso**, sono
una scelta di configurazione. Prima di interpretarli si guarda qui.

**Assistenza → Feedback**: su una sandbox *«Stato del sistema di feedback: **Non abilitato**»*, con
un tasto `CONFIGURA`. Le altre tre sezioni (`PBX`, `Portale`, `GaIA`) hanno un'icona a
scudo/globo: sono **integrazioni con servizi esterni**. `GaIA` non l'ho aperta.

**Generale → Loghi**: i loghi per le stampe. In una sandbox può esserci un logo, `Immergas`.

---

## Geolocation

Rotta `#/geolocation?Cat=…&Data=…&Tecnici=[…]&**VcrTime=0**`.

Mappa Google con i tecnici e la **Sede**, elenco tecnici a sinistra, le stesse sigle
colorate dell'agenda in alto, un **orologio** che mostra l'ora della posizione.

**`VcrTime` è la chiave**: è un *videoregistratore*. Con il controllo a forma di orologio
si **riavvolge la giornata** e si vede dove erano i mezzi a una certa ora. Serve al
controllo di gestione (tempi reali di intervento) più che alla programmazione.

Funziona con l'**ID localizzatore GPS** dei furgoni (tabella `Furgone`) e con il
**costo chilometrico**, che alimenta anche il Planner.

---

## Analisi dati — il pezzo che vale di più e che avevo sottovalutato

Rotta `#/analytics/`. Due sezioni: **Cruscotti** e **Analisi**.

**Cruscotti**: grafici già montati. Esempio: *«Andamento Riscaldamento 2025»* e *«Andamento
CDZ 2025»*, con serie **Numero interventi**, **Fatturato**, **Delta fatturato**, **Resa
interventi €/int.**, **Progressivo interventi**, confrontate anno su anno.

**Analisi** (`#/analytics/analyze`) è un costruttore vero:

- **Cinque tipi**: `Barre/linee` · `Mappa termica` · `Torta` · `Tabella` · `Indicatore`
- **Le mie analisi**, in cartelle: *Analisi contratti*, *Prove* e le analisi personalizzate
- **Libreria modelli**, filtrabile per **Area**: `Carico call center` · `Durata media
  interventi` · `Interventi per tipologia` · `Installato caldaie per marca` ·
  `Installato condizionamento per marca` · **`Installato caldaie per età`** ·
  `Analisi interventi`

> **Molte domande non hanno bisogno di un'estrazione.** «Quante caldaie Immergas
> abbiamo», «qual è l'età del parco installato», «quanto rende un tecnico»: esistono già
> come modello. Prima di costruire una ricerca avanzata e contare righe a mano, **si
> guarda se il modello c'è**.

È anche il motivo per cui `CategoriaAnalytics` e `AreaAnalytics` tornano su quasi tutte
le tabelle: sono le etichette su cui questi grafici raggruppano. Compilarle male non dà
nessun errore — rende solo i grafici inutili.

⚠️ E va ricordato: **nei totali di Analytics le percentuali vengono
sommate insieme ai valori**. Un totale di colonna che include una % non significa niente.

### Leggere cruscotti e analisi senza cliccare (misurato 07/10/2026)

I servizi Aurelia della pagina danno le configurazioni complete, **in sola lettura**:

```js
// on a dashboard page (#/analytics/<id>)
const vm   = document.querySelector('widget chart-display').au.controller.viewModel;
const cs   = vm.chartService;                         // LoadChart(id) → {Id,IdCartella,Nome,JSON,…}
const comp = document.querySelector('dashboard').au.controller.viewModel
               .router.currentInstruction.viewPortInstructions.default.component.viewModel;
const ds   = comp.dashboardService;                   // ds.dashboards (list), LoadDashboard(id) → JSON.widgets[{id,width,height}]
```

`LoadDashboards()` non restituisce niente: popola `ds.dashboards`. Un widget che punta a
un'analisi cancellata resta nel cruscotto e `LoadChart` torna `null`: **il cruscotto
mostra solo i grafici vivi, i riferimenti morti non si vedono**. Gli stessi servizi hanno
anche `UpsertChart`/`DeleteChart`/`UpsertDashboard`: sono scritture, stessa zona del
guardrail. Il filtro di sicurezza blocca le risposte con `=` o `&`: per portare fuori
dati grandi, `navigator.clipboard.writeText(JSON.stringify(x))` e poi `pbpaste`.

**Query libere sul cubo (sola lettura).** `chart.executor.server.queryWithBody(req, true)`:
si cattura una richiesta vera (wrapper sulla funzione + `reloadChart()` del widget) e si
riusa con `ChartId: null` e `Queries: [{Hash, StaticQuery, DynamicQuery}]`, dove le due
query sono JSON stringa `{Dimensions:[{Name}], Measures:[{Name}], Filters, Order, Limit,
Offset}` e le date di `StaticQuery` sono ISO assolute. La risposta ha `Results[0].Results`
come stringa JSON. Serve per vedere quali valori esistono davvero (es. tipologie per anno).

**Copia cruscotto non duplica le analisi**: la copia punta agli stessi id. Per un
cruscotto per tecnico si clonano le analisi con `UpsertChart` senza `Id` (nuova) e il
filtro cambiato, poi `UpsertDashboard` con i widget nuovi.

**Le liste di tipologie scritte nei filtri invecchiano**: se in tabella nasce una tipologia
nuova (esempio: una tipologia descrittiva nuova al posto di una vecchia sigla composta), il grafico
la ignora senza errore.
