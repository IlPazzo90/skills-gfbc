# Scrivere ai fornitori

Tono diretto e cortese, frasi brevi. «Ciao <Nome>» con i referenti che ci conoscono (annotali in
`~/.config/ufficio-acquisti/fornitori.md`), «Buongiorno» con gli uffici. Il corpo chiude con «Grazie,» una volta sola: la firma
non lo ripete. La firma la aggiunge `posta.py` a **ogni** mail, anche agli inoltri (`inoltra`).
Mai inoltrare con l'endpoint Graph `forward` diretto: esce senza firma. Il corpo è HTML semplice,
con `<p>` e `<ul>`.

## Richiesta d'offerta

Oggetto: `<impianto> - Richiesta offerta`

```html
<p>Buongiorno,</p>
<p>vi chiediamo un'offerta per:</p>
<ul><li>N. 1 <ricambio></li></ul>
<p>per questa macchina: <b><marca modello></b>, matricola <b><matricola></b>.</p>
<p>In allegato le foto della targa e del ricambio. Nell'offerta indicateci anche i tempi di consegna.</p>
```

**Chiedi sempre i tempi di consegna nella prima mail**: sono metà di quello che serve al
commerciale, e se non li chiedi subito si perdono per strada.

## Sollecito

Oggetto: `Sollecito: <oggetto originale>`, oppure una risposta nello stesso thread se la mail
originale è partita dalla casella acquisti.

```html
<p>Buongiorno <Nome>,</p>
<p>il <data> vi avevamo chiesto un'offerta per <cosa, macchina, matricola>.
Non ci risulta ancora una risposta. Ci mandate prezzo e tempi di consegna?
Se è un ricambio non più disponibile, basta una riga per dircelo.</p>
```

Se il cliente è fermo, aggiungi una frase sola: «Il cliente è fermo, ci serve una risposta entro domani.»

Se prima gli acquisti li seguiva una persona che non c'è più, la prima volta che scrivi a un suo
fornitore aggiungi: «<Nome> non lavora più con noi: da ora le richieste partono da questa casella,
e le risposte vanno qui.»

## Ordine (solo dopo l'ok del titolare)

Oggetto: `<impianto> - Ordine ricambi`

```html
<p>Buongiorno <Nome>,</p>
<p>con riferimento alla vostra offerta <n.> del <data>, ordiniamo:</p>
<ul><li>N. <q> <codice> <descrizione> - € <prezzo></li></ul>
<p>Consegna presso la nostra sede: <indirizzo di consegna>.
<!-- oppure: Passiamo a ritirarlo a banco. --></p>
<p>Ci mandate la conferma d'ordine con la data di consegna?</p>
```

## Mail interne

- **All'ufficio tecnico**: per foto, matricole o codici che solo il tecnico può leggere
  sull'impianto. Indica impianto, indirizzo, ticket e **cosa fotografare**.
- **Al commerciale**: passa dalla nota dell'attività su Unicò, non dalla mail. Una mail solo se è urgente.
