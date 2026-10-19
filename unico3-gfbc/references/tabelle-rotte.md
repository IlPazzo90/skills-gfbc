# Le rotte delle tabelle — censite dal vivo

Misurato su una sandbox. Prima di questo giro le rotte si indovinavano (male);
adesso ci sono, insieme al **metodo** per trovare quelle che mancano.

---

## La scoperta che cambia il modo di lavorare

> **Per le tabelle, `location.hash` scritto a mano funziona.**

```js
location.hash = '#/tabelle/Zona/table';   // → la griglia della tabella
```

Questo **contraddice** la regola generale scritta in `SKILL.md` e in
`flussi/estrazione.md`, che resta però valida **per le ricerche**: lì la rotta scritta a
mano lascia lo schermo su quella precedente.

**Le due cose convivono**: la navigazione per hash funziona sulle tabelle, non sulle
ricerche. Verificato in entrambe le direzioni.

### ⚠️ Ma una rotta sbagliata non dà errore

Se il nome entità non esiste, **resta a schermo la tabella precedente**, identica e
silenziosa. Provando `FluidoFGas` la pagina continuava a mostrare *Combustibili*, e il
conteggio che avrei letto sarebbe stato quello sbagliato attribuito alla tabella
sbagliata.

**Difesa obbligatoria: confrontare il titolo della tab con l'etichetta attesa.**

⚠️ **Due correzioni all'11/09/2026, e la funzione qui sotto non gira più com'è scritta.**

1. ~~`javascript_tool` non aspetta le promise~~ — **smentito il 09/10/2026 su A1**: il `await`
   al primo livello funziona (letta `TipoAttivitaUfficio` in una chiamata). Il limite vero è
   il **timeout di 45 s**: per più tabelle si lancia un `(async()=>{…})()` che scrive in
   `window.__D` e `window.__stato`, e si interroga dopo. In produzione la rotta `MotivoRdI` ha
   restituito le righe di `TipologiaDocumento` (stessi campi): la rotta non esiste lì,
   e il controllo dei campi l'ha scoperto.
2. Sulle **tabelle** `div.main-tab.selected` esiste ma ha **innerText vuoto**: il titolo
   sta nell'intestazione del pannello a destra. Una difesa costruita su quel confronto
   fallirebbe sempre, anche con la tabella giusta aperta. Per riconoscere il record
   aperto in una **scheda** funziona invece l'unico `<span>` senza figli che contiene
   `" - "`, cioè `"MARCA - MODELLO"` (vedi `flussi/tabelle-modelli.md`).

```js
async function apriTabella(rotta, etichettaAttesa){
  location.hash = '#/tabelle/' + rotta + '/table';
  for (let i = 0; i < 14; i++) {
    await new Promise(r => setTimeout(r, 400));
    const t = document.querySelector('div.main-tab.selected');
    const titolo = t ? t.innerText.trim().replace(/\n/g,' ').replace(/^TABELLA\s*/,'') : '';
    if (titolo.toLowerCase().startsWith(etichettaAttesa.toLowerCase().slice(0,12))) {
      const g = Array.from(document.querySelectorAll('.ag-root-wrapper'))
        .filter(e => e.offsetParent !== null);
      if (g.length === 1 && g[0].__agComponent) {
        const righe = [];
        g[0].__agComponent.gridApi.forEachNodeAfterFilterAndSort(n => { if (n.data) righe.push(n.data); });
        if (righe.length) return { ok:true, righe, campi:Object.keys(righe[0]) };
      }
    }
  }
  return { ok:false, mostrava: titolo };   // rotta sbagliata: NON usare i dati a schermo
}
```

---

## Rotte confermate

I conteggi di righe cambiano da azienda ad azienda e non sono riportati; i **campi** no.

### Assistenza

| Etichetta | Rotta |
|---|---|
| Combustibili | `Combustibile` |
| Fluidi GAS | **`FluidoGas`** |
| Fornitori energia | `FornitoreEnergia` |
| Interlocutori RDI | `InterlocutoreRdI` |
| Motivi dismissione | `MotivoDismissione` |
| Motivi RDI | `MotivoRdI` |
| Motivi ritorno intervento | `MotivoRitornoIntervento` |
| Operatori RDI | `OperatoreRdI` |
| Sottotipi altro impegno | `SottotipoAltroImpegno` |
| Squadre Tecnici | `SquadraTecnici` |
| Tecnici | `Tecnico` |
| Tipologie attività ufficio | `TipoAttivitaUfficio` |
| Tipologie componente | `TipologiaComponente` |
| **Tipologie contratti** | **`TipologiaContratto`** |
| Tipologie garanzie installati | `TipologiaGaranziaInstallato` |
| Tipologie guasto | `TipologiaGuasto` |
| Tipologie impianti | `TipologiaImpianto` |
| Tipologie intervento | `TipologiaIntervento` |
| Tipologie RDI | `TipologiaRdI` |
| Voci validazione intervento | `VoceValidazioneIntervento` |

### Generali

| Etichetta | Rotta |
|---|---|
| Aliquote IVA | `AliquotaIva` |
| Banche | `Banca` |
| Comuni | `Comune` |
| Enti | `Ente` |
| Glossario | **`VoceGlossario`** |
| Marche | `Marca` |
| Numerazioni | **`Numeratore`** |
| Pagamenti | **`TipoPagamento`** |
| Tipologie documenti | `TipologiaDocumento` |
| Zone | `Zona` |

**I nomi non seguono una regola.** `Tipo…`, `Tipologia…`, o nessuno dei due
(`Numeratore`, `VoceGlossario`, `FluidoGas`). **Non si indovinano: o si conoscono, o si
cliccano nell'albero.**


### Magazzino

| Etichetta | Rotta |
|---|---|
| Attrezzature furgoni | `AttrezzaturaFurgone` |
| Cantieri | **`Cantiere`** |
| Causali movimenti | **`CausaleMovimentoMagazzino`** |
| Dotazioni standard e scorte minime | **`DotazioneStandardScortaMinima`** |
| Furgoni | **`Furgone`** |
| Gruppi merceologici | **`GruppoMerceologico`** |
| Listini | **`Listino`** |
| Magazzini | **`Magazzino`** |
| Tag articoli | `TagArticolo` |
| Tipologie lista materiale | `TipologiaListaMateriale` |

Più `Dati di conformità`, `Famiglia merceologica`, `Tipologie attrezzature furgoni`
(rotte non ancora lette).

**`Dati di conformità` non è nella guida ufficiale.** È una tabella che esiste solo qui.

### Le rotte trovate nel secondo giro

| Etichetta | Rotta |
|---|---|
| Unità di misura | **`UdM`** |
| Tipologie operazioni di manutenzione | **`TipologiaOperazioneDiManutenzione`** |
| Tipologie file allegato | `TipologiaFileAllegato` |
| Tag anagrafiche | `TagAnagrafica` |
| Tipologie commesse | `TipologiaCommessa` |
| Anagrafiche azienda | **`CAT`** → `/detail/1` (scheda, non griglia) |

`UdM` e `TipologiaOperazioneDi**Di**Manutenzione` sono la prova che i nomi non si
indovinano: avevo provato `UnitaMisura`, `UnitaDiMisura`, `TipologiaOperazioneManutenzione`,
`TipoOperazioneManutenzione`, `OperazioneManutenzione`, `TipoOpMan`. Tutti sbagliati.

**`Anagrafiche azienda` non è una griglia**: la rotta è `CAT` e finisce su
`/detail/1`, cioè la scheda di una singola azienda. Con la lettura da griglia dà **zero
righe**, e uno zero letto lì sarebbe una risposta sbagliata.

---

## Il censimento completo

| Cartella | Contenuto |
|---|---|
| **Amministrazione** | una sola sottocartella **`1^ nota`**, con **2 tabelle**: `Causali contabili` e `Causali e conti di default` |
| **Assistenza** | 24 tabelle + sottocartelle *Modelli installato* (6) e *Tag* (8) |
| **Generali** | 15 |
| **Magazzino** | 13 |

**Circa 68 tabelle in tutto**, contro le 72 del wiki NET — e con una distribuzione molto
diversa: tutta l'Amministrazione del web sono **le due tabelle delle causali contabili**,
che peraltro sono fra le più pericolose in assoluto (`Causali e conti di default` è quella
che regge tutti gli automatismi di registrazione).

Restano senza rotta letta: le 6 di *Modelli installato*, le 8 di *Tag*, le 2 di
*1^ nota*, e tre di Magazzino. Si prendono con `apriTabella` dalla sidebar.

---

## ⚠️ La trappola in cui sono ricascato mentre censivo

Al primo giro ho letto la griglia **subito dopo il cambio di rotta**, e i conteggi si
ripetevano: `N, N, N` poi `M, M, M`. Stavo leggendo **la tabella precedente**,
perché la rotta cambia prima che la griglia si ricarichi.

È esattamente la trappola che avevo già documentato per il contatore delle ricerche, in
un'altra forma. **Aspettare che la rotta cambi non basta: bisogna aspettare che il titolo
della tab corrisponda alla tabella attesa**, e solo allora leggere.

La funzione corretta è `apriTabella` più sopra. Quella sbagliata dava numeri plausibili e
falsi — il tipo di errore peggiore.

### Modelli installato — e sono 5, non 6

| Etichetta | Rotta |
|---|---|
| Modelli Gruppo Frigo | `ModelloGruppoFrigo` |
| Modelli Componente | `ModelloComponente` |
| Modelli Gruppo Termico | `ModelloGruppoTermico` |
| Modelli UIR | `ModelloUIR` |
| Modelli Bruciatore | `ModelloBruciatore` |

⚠️ **`Modelli Scambiatore` non c'è**, anche se la guida ne elenca sei e anche se il
**Tag** dei modelli scambiatore esiste. Su una sandbox la tabella dei modelli scambiatore non
compare nell'albero.

Gruppi frigo e gruppi termici hanno **34 campi** ciascuno: sono schede tecniche complete.

### Tag — 8, e il pattern è regolare

`TagImpianto` · `TagRDI` · `TagModelliGruppoTermico` ·
`TagModelliScambiatore` · e con lo stesso schema `TagModelli` + *Bruciatore*,
*Componente*, *GruppoFrigo*, *UIR*.

È l'unico gruppo di rotte che **si può dedurre**: `TagModelli<Tipo>`.

### 1^ nota (Amministrazione)

| Etichetta | Rotta | Note |
|---|---|---|
| Causali contabili | **`CausaleMovimentoEconomico`** | **25 campi** |
| Causali e conti di default | `CausaliContiDefault` | *non è una griglia* — riga singola di configurazione |

`Causali contabili` → `CausaleMovimentoEconomico` è forse il nome più lontano
dall'etichetta di tutto il programma.

### Le ultime di Magazzino

`TipologiaAttrezzaturaFurgone` · `FamigliaMerceologica` (la rotta **non finisce con
`/table`**: forma diversa) · `Dati di conformità` non l'ho ancora agganciata — il filtro
con l'accento non trova la voce.

---

## Il censimento vero delle tabelle: sono molte meno di 72

Espandendo l'albero:

| Cartella | Tabelle |
|---|---|
| **Amministrazione** | **1** — solo `1^ nota` |
| **Assistenza** | 24, più le sottocartelle *Modelli installato* (6) e *Tag* (8) |
| **Generali** | 15 |
| **Magazzino** | da espandere |

Il numero **72** che avevo scritto in `mappa-web.md` veniva dal wiki di Unicò NET.
**Nel web ce ne sono meno**, ed è coerente con `cosa-il-web-non-fa.md`: l'Amministrazione
del web ha **una sola tabella**, perché la contabilità sta nel terminale.

---

## Tipologie contratti — la tabella che spiega i contratti

`#/tabelle/TipologiaContratto/table`: ogni riga è `Avanzato` o `Semplice`.

Risponde a una domanda che la maschera di un contratto nuovo lascia aperta: **perché
scegliendo una certa tipologia si spunta da solo il tacito rinnovo, e perché la fine
tacito cade dopo un certo numero di anni.** Le tipologie (nomi, codici, listini, liste
materiale) sono configurazione dell'azienda; la struttura è questa, con una riga d'esempio:

```
Codice: <codice>                TipoContratto: Semplice
IsTacitoRinnovo: true           ← la casella che si spunta da sola
DurataInizialeDefault: 1                        → copertura di 1 anno
DurataTacitoRinnovoDefault: 1                   → il campo "Anni" della maschera
DurataComplessivaMassimaConTacitoRinnovoDefault: 2   → il tetto complessivo
Listino: <listino dedicato>
ListaMaterialeRinnovo: <lista materiale del piano>
IsNonRendereRicambiInGaranzia: true
PrioritaTipologiaContratto: 1
CategoriaAnalytics / AreaAnalytics: <categoria e area per i grafici>
```

**La fine tacito non è un errore né un residuo**: data di fine copertura +
**durata complessiva massima** = data finale. Il campo `Anni` che si vede nella
maschera è `DurataTacitoRinnovoDefault` — di quanto si rinnova ogni volta — mentre la
data finale è calcolata sul **tetto complessivo**. Sono due cose diverse che nella
maschera stanno una accanto all'altra.

### Cosa porta con sé una tipologia contratto

Scegliendola in un contratto nuovo arrivano, senza dire niente:

- **il tacito rinnovo** (acceso o spento) con le sue tre durate
- **un listino prezzi dedicato**, se la tipologia ne ha uno. È così che un piano
  commerciale applica i suoi prezzi.
- **una lista materiale di rinnovo**, cioè cosa comprende il piano
- `IsNonRendereRicambiInGaranzia`
- `ModalitaAssociazioneIntervento` + `ListaTipiInterventoAssociati`: quali interventi il
  contratto copre
- `IsSospensione` con inizio e fine — è il **giallo** dei contratti sospesi
- `Rate` per i contratti avanzati
- categoria e area Analytics

Le durate si leggono come `iniziale/tacito/massima` (anni): combinazioni tipiche sono
`1/1/2`, `5/5/null`, `1/1/null`, o nessuna durata.

**Prima di stipulare un contratto vero conviene leggere la sua riga in questa tabella**:
quello che la maschera propone da sola viene tutto da qui.

---

## Altre tabelle, quello che si impara dai campi

- **Tecnici** (~36 campi) — è la più ricca: `ListaCompetenze`, `ListaOrari`,
  `CodiciManutentore`, `LuogoBaseTecnico` / `LuogoPranzoTecnico` con gli indirizzi
  alternativi, `LivelloLicenza`, `Colore`, `IdListaMateriale`, `Matricola`, `MemoDays`.
  Conferma che è il perno di agenda, planner e catasto.
  **Su A1, misurato il 13/10/2026.** Nuovo tecnico: + in alto a destra → procedura in
  quattro passi (Dati generali → Altri dati, cioè patentino F-gas e codici manutentore →
  Competenze → Orari, con luogo base e tipo di pausa pranzo) → CONFERMA. Sigla, Tecnico,
  Colore e licenza sono obbligatori. La licenza planner che nella UI si chiama
  **«Standard»** nei dati è `LivelloLicenza = "Full"`. Le Standard hanno un **tetto**:
  oltre, CONFERMA risponde «Non sono disponibili sufficienti licenze del tipo indicato» e
  il tecnico non nasce. Si crea con licenza Nessuna e si passa a Standard dopo aver
  liberato una licenza. **Un tecnico escluso dalle liste continua a consumare la licenza**:
  per liberarla serve anche Tipo licenza = Nessuna. Per modificare: doppio click sulla riga
  apre «Modifica tecnico» (sigla, descrizione, Escluso da liste); la matita del pannello
  Dati generali apre «Modifica altri dati tecnico» (cognome, nome, contatti, CF, licenza,
  colore). `location.hash = '#/tabelle/Tecnico/detail/<Id>/data'` apre il dettaglio.
  **Su A2, misurato il 14/10/2026.** Con licenza Nessuna il wizard crea senza toccare il
  tetto delle licenze. Il Colore si sceglie da una tavolozza Material di 19 tinte (il
  valore salvato è l'esadecimale, es. `#8BC34A`); un colore fuori tavolozza (A1 usa
  `#F0F0F0`) dal wizard non si riproduce. Le tre caselle «Numerazione automatica»
  (Ricevute fiscali, Rapportini, Allegati/rapporti di controllo) stanno nel primo passo.
  Il cognome e il nome si correggono dalla matita del pannello Dati generali, che compare
  solo al passaggio del mouse; lì Tipologia contatto è obbligatoria anche senza telefono.
  L'icona di esclusione del dettaglio manda `{Id, IsEsclusoDaListe: true}`.
- **Fluidi GAS** — `GWP` e `Categoria`: il potenziale di riscaldamento globale, che
  serve agli adempimenti F-Gas.
- **Tipologie impianti** — `Classi`, **`OpManDefault`** (le operazioni precaricate) e
  `IsUtilizzato`: si vede subito quali tipologie sono in uso.
- **Tipologie operazioni di manutenzione** — misurato su A2 il 14/10/2026. Il «+» apre un
  form unico: Tipologia op. man. (Ordinaria/Straordinaria), Codice, Descrizione, lista
  materiale, durata media, Includi su D.F.M, descrizione estesa, Riscaldamento,
  Condizionamento (accanto compare Tipo operazione FGAS: Installazione, Riparazione,
  Manutenzione, Controllo perdite, Smantellamento), Altro, note, codice export, Escluso.
  **Teleriscaldamento non è nel form** anche se il dettaglio lo mostra. Il menu ⋮ della
  tabella ha solo Esporta e Stampa: nessun import. **La descrizione è unica senza
  distinzione di maiuscole**: una già usata da un altro codice dà «Valore già presente» e
  CONFERMA non salva. Le voci col **lucchetto** in griglia (su A2: MO, AF, RB, VI, le
  predefinite del programma) hanno Codice ed Escluso disabilitati e niente icone di
  esclusione o eliminazione: si cambiano solo descrizione e flag. Sulle altre il Codice si
  modifica dalla matita.
- **Tipologie RDI** — c'è **`IsRichiamo`**: è un flag della tipologia che distingue il
  richiamo dalla richiesta normale.
- **Tipologie documenti** — `IsMagazzino`/`OpzioneMagazzino`,
  `IsContabili`/`OpzioneContabili`, `IsCorrispettivi`, `IsRicevuto`, `TipoDocumentoSDI`,
  `IdNumeratore`. È la tabella che decide **se un documento muove magazzino, contabilità
  o entrambi**. Zona rossa.
- **Numerazioni** — **`UltimoNumero`**, `Suffisso`, `TipoNumeratore`, `IdCAT`.
  ⚠️ **È qui che si guarda l'ultimo numero usato** prima di numerare a mano un documento
  nel web (dove nessun progressivo viene proposto).
- **Pagamenti** — `NumeroRate`, `TipologiaPrimaRata`, `InizioPrimaRata`,
  `Periodicita`, `PrimoPosticipo`/`SecondoPosticipo`/`PosticipoSempreAl`,
  `ModalitaIncasso`, `Sottoconto`: le regole che generano lo scadenziario.
- **Banche** — con `IBAN`, `CreditorID` (per gli SDD), `SpeseInsoluto`, `SIA`,
  `IsBancaAzienda`.
- **Comuni** e **Marche** — le due tabelle grandi; Marche ha i flag
  `IsRiscaldamento`, `IsCondizionamento`, `IsTeleriscaldamento`, `IsComponenti`,
  `IsArticoli` che decidono dove la marca è proponibile.
- **Glossario** — una ventina di flag `Is…` che dicono **in quale punto del
  programma** la frase è disponibile: `IsRCEEPrescrizioni`, `IsRCEEOsservazioni`,
  `IsNoteRdI`, `IsNoteIntervento`, `IsNoteAttivita`, `IsRigheOrdini`,
  `IsTestoFinaleOrdini`, `IsArticoli`, `IsSMS`, `IsEmail`, `IsTestoStampa`.
- **Aliquote IVA** — `Natura`, `Tipo`, e i riferimenti SDI.
- **Squadre Tecnici** — `TecnicoCapoSquadra` + `TecniciAiutanti`.
- **Enti** — legati al `Comune`, con `TipoEnte`.
