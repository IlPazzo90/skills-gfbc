# Flusso 2 — Ricerca avanzata

Procedura **eseguita e misurata** su una sandbox, non dedotta dalla guida. I numeri
qui sotto sono riproducibili: se rifacendola escono diversi, o i dati sono cambiati o la
procedura è stata seguita male.

Serve quando la ricerca semplice non ha il campo, o quando la domanda riguarda **cosa c'è
dentro l'impianto** (installati, contratti, operazioni) e non l'impianto in sé.

---

## Passo 0 — Azienda, e apri il costruttore

Azienda dalla URL, dichiarata. Poi `Assistenza → Ricerca`, entità, scheda **`Avanzata`**.

⚠️ **Passare da Semplice ad Avanzata NON travasa i criteri.** Verificato: con `%COGNOME`
compilato nella semplice, l'avanzata si è aperta con «Nessuna condizione aggiunta». Il
travaso si fa **solo** da `⋮ → Trasforma in ricerca avanzata`, dalla semplice.

## Passo 1 — Libera lo schermo

**Il pannello dei risultati copre il costruttore.** Si collassa con la maniglia:

```js
document.querySelector('div.expand-collapse').click()   // oppure il click a coordinate
```

Senza questo, i click sulle condizioni finiscono sulla griglia sottostante.

## Passo 2 — Costruisci

`AGGIUNGI CONDIZIONE` per una regola, `AGGIUNGI GRUPPO` per annidare. Ogni gruppo ha il
suo **`Soddisfa [tutte le | almeno una delle]`** — AND oppure OR, e vale *solo per quel
livello*.

Il campo si cerca digitando, **ma il filtro non gradisce più parole**: `gruppo term` →
«Nessun risultato»; `termic` → due campi. **Usa una parola sola.**

### Gli operatori cambiano con il tipo di campo

| Tipo di campo | Cosa compare |
|---|---|
| **Booleano** (es. `Dismesso`) | due bottoni **`Vero` / `Falso`**, senza operatore |
| **Tabellato** (es. `Marca`) | `Soddisfa condizione`, **`È uno dei seguenti`**, `È vuoto`, `Non è vuoto` — **niente «Uguale a»** |
| **Relazionale** (es. `Gruppi termici attivi`) | `Almeno uno`, `Se presenti, tutti`, `Nessuno`, `Almeno`, `Al massimo`, `Esattamente` → **aprono un sottogruppo annidato** |

### ⚠️ Tre trappole misurate

**1. Un campo booleano nasce con `Vero` già selezionato.** Scegli `Dismesso` e non tocchi
altro → stai cercando **gli impianti dismessi**, l'opposto di quello che quasi sempre
serve. Guarda sempre quale dei due bottoni è acceso.

**2. `Almeno uno` e `Se presenti, tutti` danno risposte diversissime.** Stessa domanda in
testa — «gli impianti con caldaia Immergas» — misurata su una sandbox:

| Operatore | Risultato |
|---|---|
| `Almeno uno` → Marca = Immergas | **N** |
| `Se presenti, tutti` → Marca = Immergas | **M** (molto di più) |

`Se presenti, tutti` **include tutti gli impianti che non hanno affatto un GT attivo**:
la condizione è vacuamente vera. Su un parco reale la differenza può essere di un ordine di grandezza.
**Usa `Almeno uno` per «ce n'è uno che…», `Se presenti, tutti` solo per «non ce n'è
nessuno che NON…»**, e in quel caso aggiungi anche una condizione di presenza.

**3. Esistono campi quasi omonimi che non sono la stessa cosa**: `Gruppi termici` e
**`Gruppi termici attivi`**. Il primo conta anche i dismessi. Per una domanda operativa
serve quasi sempre il secondo. Stesso discorso altrove: **leggi l'etichetta per intero**.

### Sui valori tabellati

Digitando `immergas` la tendina propone **`Immergas S.p.A.`** *e* **`NO-<MARCA>`**: due
marche diverse, e la seconda significa l'opposto. Non prendere la prima che compare.

E in fondo alla tendina c'è **`Aggiungi elemento`**, che **crea una voce nuova in
tabella**. È una scrittura: un click distratto sull'ultima riga sporca la tabella Marche.

## Passo 3 — Cerca, e aspetta davvero

⚠️ **Leggere il conteggio troppo presto restituisce «Sono stati trovati 0 risultati»**, e
uno zero prematuro è **indistinguibile da uno zero vero**. Mi è successo: ho letto dopo
2,5 secondi fissi e ho creduto a un risultato vuoto che in realtà conteneva tutti gli impianti attivi.

**Non usare un'attesa a tempo. Aspetta la condizione:**

```js
function stato(){
  const riq = Array.from(document.querySelectorAll('.search-results'))
    .filter(e => e.offsetParent !== null);
  if (riq.length !== 1) return {pronto:false, motivo:'riquadri '+riq.length};
  const m = (riq[0].innerText.match(/trovati\s+([\d.]+)\s+risultati/i)||[])[1];
  const dich = m ? parseInt(m.replace(/\./g,''),10) : null;
  const g = riq[0].querySelector('.ag-root-wrapper');
  if (!g || !g.__agComponent) return {pronto:false, motivo:'griglia assente', dich};
  const n = [];
  g.__agComponent.gridApi.forEachNodeAfterFilterAndSort(x => { if (x.data) n.push(1); });
  return {pronto: dich !== null && n.length === dich, dich, modello: n.length};
}
let s, giri = 0;
while (giri < 20) { s = stato(); if (s.pronto) break; await new Promise(r=>setTimeout(r,500)); giri++; }
```

Quando si rifà una ricerca **dopo averne già fatta un'altra**, aggiungi al criterio di
uscita `&& dich !== <valorePrecedente>`: altrimenti la funzione trova subito «pronto» sul
risultato vecchio, che è ancora a schermo e già coerente.

**È la stessa prova di completezza dell'estrazione**: dichiarato dal contatore = righe nel
modello. Misurato: N dichiarati, N nel modello, **25 righe nel DOM**.

## Passo 4 — Il numero in basso non è la tua query

⚠️ Il contatore accanto a `CERCA` mostra **l'ultima ricerca eseguita**, non i criteri
attualmente compilati. Cambiando l'operatore da `Se presenti, tutti` ad `Almeno uno`
continuava a mostrare il conteggio precedente finché non ho ripremuto `CERCA`.

**Mai riportare un numero senza aver premuto `CERCA` dopo l'ultima modifica ai criteri.**

## Passo 5 — Salvare la ricerca

`SALVA` → nome + casella **`Condivisa`**. La rotta diventa
`.../avanzata/savedSearch/<id>` e compare una barra col nome.

**`Condivisa` la rende disponibile a tutti gli utenti dell'azienda**: si spunta solo se è
quello che si vuole. Chi la riceve **può modificarla ma non salvarla** — deve farne una
copia.

Poi `SALVA` diventa un menù con **`salva modifiche`** e **`crea una copia`**.
Si ricarica da `⋮ → carica ricerca salvata`, in due sezioni: *le mie ricerche* (col
cestino) e *ricerche condivise*.

---

## L'esempio completo, riproducibile

Domanda: **quanti impianti attivi hanno almeno un gruppo termico attivo Immergas?**

```
Soddisfa [tutte le] seguenti condizioni
├── Dismesso ............................ Falso
└── Gruppi termici attivi ............... Almeno uno
    └── Soddisfa [tutte le] seguenti condizioni
        └── Marca ....................... È uno dei seguenti → Immergas S.p.A.
```

**Risposta su una sandbox: N.** Prova di completezza passata — N dichiarati, N nel
modello. Salvata come *TEST AUTOMAZIONE - Attivi con almeno un GT Immergas*
(`savedSearch/1`), non condivisa.

Controprova che la struttura è corretta: togliendo il ramo relazionale restano **tutti gli impianti attivi**,
che è il totale già verificato per un'altra strada (ricerca semplice con
`Attivi` preselezionato). **Due percorsi indipendenti, stesso numero.**
