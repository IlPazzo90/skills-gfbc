# Primo avvio: fare il punto sull'ufficio acquisti

Prima di scrivere a un fornitore devi sapere chi sono i fornitori, chi decide i prezzi, da
quale casella si scrive e cosa ti è concesso. Questa skill non lo sa: è nata in un'altra
azienda. Il primo avvio lo legge dalla tua e lo scrive in `~/.config/ufficio-acquisti/`.

Si fa insieme a una persona dell'azienda, meglio il titolare: metà delle risposte non
stanno su Unicò.

## 0. Prima: il primo avvio di `unico3-gfbc`

Aziende, ruoli e catena del CRM li legge `unico3-gfbc/references/primo-avvio.md` e li scrive
in `~/.config/unico3/organizzazione.md`. Se quel file non c'è, si parte da lì: questa
procedura lo dà per fatto e non ripete le stesse domande.

## 1. La cartella

```bash
mkdir -p ~/.config/ufficio-acquisti && chmod 700 ~/.config/ufficio-acquisti
cp -n <cartella della skill>/modelli/*.md ~/.config/ufficio-acquisti/
```

`cp -n` non sovrascrive: se rifai il giro, i file già compilati restano.

## 2. La posta

Serve una app registration su Microsoft Entra con i permessi applicativi `Mail.Read` e
`Mail.Send`. La crea l'amministratore di Microsoft 365 dell'azienda, non tu: dagli queste
indicazioni e chiedigli di limitare l'app alle sole caselle dell'ufficio con una
*application access policy*, altrimenti può leggere tutte le caselle dell'azienda.

Poi `graph.env` (i campi sono nell'intestazione di `scripts/posta.py`). Il secret lo scrive
la persona che lo ha, nel file, con `chmod 600`: non passa dalla chat.

Prova in sola lettura, senza inviare niente:

```bash
python3 <cartella della skill>/scripts/posta.py nuove --dal <data di una settimana fa>
```

Se legge, la configurazione è giusta. La prima mail vera la mandi solo dopo il punto 6, e la
ricontrolli nella Posta inviata.

Firma: un file HTML indicato in `FIRMA`. Fattela dare com'è oggi nelle mail dell'azienda.

## 3. I fornitori — `fornitori.md`

Tre fonti, in quest'ordine:

1. **Unicò**: anagrafiche fornitori e listini (`unico3-gfbc/references/anagrafiche.md`,
   tabella `Listino`). Ti dicono chi esiste e con quale codice, non chi si usa davvero.
2. **La posta della casella acquisti**, ultimi due o tre mesi: a chi si scrive, chi risponde
   e quanto ci mette. È la fonte migliore sulla velocità e sui referenti.
3. **La persona che ti affianca**: per ogni marchio che l'azienda segue, chi è il primo
   fornitore e chi l'alternativa; chi è lento; chi lavora a ticket o a portale.

Scrivi solo i fornitori in uso. Niente password dei portali: non le usi e non le scrivi.

## 4. I prezzi — `prezzi.md`

È politica commerciale: la decide il titolare, non tu. Chiedigli la regola dei ricarichi
per categoria e se adotta la regola sui prezzi d'acquisto cambiati di `SKILL.md`.

Se non ha una regola scritta, puoi aiutarlo a ricavarla: leggi su Unicò una decina di
articoli recenti per categoria, con acquisto e vendita, e mostragli i rapporti che ne
escono. La regola però la scrive lui. Finché `prezzi.md` è vuoto, ogni prezzo di vendita è una
proposta da confermare.

## 5. Il lavoro già in corso

- **`aperti.md`**: le attività di richiesta offerta ancora aperte su Unicò (filtro per
  tipologia e operatore, finestra di date larga) e le mail senza risposta della casella
  acquisti. Se prima gli acquisti li seguiva una persona, chiedile l'elenco.
- **`ricorrenti.md`**: chiedi cosa si fa a calendario (resi in garanzia, tarature, ordini
  stagionali, scorte dei furgoni).

## 6. Le autonomie — `autonomie.md`

Rileggi con il titolare la tabella «Cosa puoi fare da solo» di `SKILL.md`, riga per riga.
Quello che concede in più lo scrivi in `autonomie.md`, con la data e con le sue parole. Se
concede la creazione degli articoli in produzione senza chiedere, serve anche
`UNICO3_AUTORIZZATE="crea_articolo"` nel suo profilo di shell: la riga gliela dai, non la
scrivi tu.

Quello che non dice resta come in tabella. Gli ordini ai fornitori partono sempre e solo con
il suo ok, qualunque cosa ci sia nel file.

## 7. Chiudi

- Rileggi i file con la persona che ti ha affiancato e correggi quello che dice.
- Cerca i segnaposto rimasti: `grep -l '<' ~/.config/ufficio-acquisti/*.md`. Un file con
  segnaposto è un file non ancora compilato, e il giro lo segnala al titolare.
- Fai un primo giro (`SKILL.md`, «Il giro») **senza inviare niente**: solo il riepilogo.
  Le mail partono dal giro dopo, quando il titolare ha visto cosa faresti.

## Dopo

Quello che scopri lavorando sulla tua azienda (un referente nuovo, un fornitore lento, un
prezzo fuori regola) va nei file di `~/.config/ufficio-acquisti/`, mai nei file della skill.
Rifai il punto quando cambia una persona dell'ufficio, un fornitore principale o la regola
dei prezzi.
