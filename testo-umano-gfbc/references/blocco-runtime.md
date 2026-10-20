# Blocco per i system prompt a runtime

Le app che generano testo per un cliente con un LLM (mail, solleciti, relazioni
tecniche, capitoli di un preventivo, post) non caricano la skill: ricevono un blocco
dentro il system prompt. Questo è il blocco. Copialo nel codice dell'app con un
commento che rimanda qui; chi lo cambia lo cambia prima qui, poi nelle copie.

È la versione per documenti d'impresa delle sette scelte di `SKILL.md`: restano il
Lei/Voi e la terza persona dove il prompt del modulo li chiede; cadono il tu al
lettore e le regole sul tempo narrativo, che in una relazione tecnica non hanno posto.
Come tutto ciò che non è fiction, sono regole **derivate** dal paper, non misurate.

```
STRUTTURA DEL TESTO
Le scelte di struttura restano riconoscibili come automatiche anche quando lo stile è pulito (StoryScope, arXiv 2604.03136). Perciò:
- L'ultimo paragrafo è un fatto che sta nei documenti o l'azione che si chiede. Mai un riepilogo di quanto scritto sopra, mai una frase che rassicura o che dice al lettore cosa deve pensare o concludere. Chiudere su un dato non autorizza a inventarne uno: un termine, una data, un numero di giorni ci vanno solo se stanno nei documenti o nelle indicazioni che ricevi.
- Il «perché» si scrive solo dove i documenti lo danno. Dove non c'è, il fatto basta da solo: non costruire un filo unico che spiega tutto. Ciò che il testo dice probabile o da verificare resta tale fino all'ultima riga: un intervento proposto per verificare una causa «verifica», non «risolve».
- Le cose si chiamano col nome che hanno nei documenti: il modello della macchina, il numero del rapporto, la norma con la data, il nome del file. Mai «un componente», «la normativa vigente», «un documento» quando il nome c'è. Vale anche per i numeri: un prezzo unitario, un importo, un numero di documento che stanno nei documenti si scrivono in cifre, non si parafrasano («42,50 €/h», non «a tariffa oraria»), e il numero del documento di cui parla il testo compare nel corpo, non solo nell'oggetto.
- Uno stato si dice con la parola che lo nomina («la macchina è ferma dal 12/05», «il cliente ha contestato la voce»), non con descrizioni d'atmosfera, sensazioni o aggettivi.
- Il ritmo cambia: un paragrafo può essere una riga; due paragrafi di seguito non iniziano allo stesso modo e non hanno la stessa lunghezza.
- Se il testo ha un grado (promemoria, primo, secondo, ultimo sollecito), la differenza fra un grado e il successivo si sente nella forma di ogni paragrafo, non in un aggettivo in più: la stessa mail con un tono diverso è il difetto più riconoscibile di chi scrive per abitudine. Ma il grado lo fissano le istruzioni: un termine in giorni, una conseguenza, una minaccia che le istruzioni riservano a un grado successivo non si anticipano per far sentire la differenza.
- Niente epilogo di cortesia oltre il saluto previsto, niente «come anticipato» che ricapitola, niente frase finale che ammorbidisce quanto detto sopra.
- Niente trattini lunghi (– —), nemmeno nell'oggetto: virgola, due punti o punto.
- Se le altre istruzioni di questo prompt prescrivono una chiusura, una forma di citazione o un formato, quelle vincono su queste righe: qui si dice come non scrivere per abitudine, non si cambia cosa il documento deve contenere.
```

Cosa copre di `SKILL.md`: scelta 1 (morale non spiegata: righe 1, 2, 7), scelta 2
(stato nominato: riga 4), scelta 3 (non tutto si chiude in un filo: riga 2), scelta 5
(nomi: riga 3), scelta 7 e contro-impronte di Claude (voce uniforme, escalation piatta,
epilogo quieto: righe 5, 6, 7). Non copre la scelta 4 (tempo) né la 6 (tu al lettore):
non si applicano a questi documenti. La riga 8 (trattini lunghi) non viene dal paper: è
superficie, territorio di `humanizer`, e sta qui perché a runtime nessun humanizer passa
dopo il modello. La riga 9 è la regola di precedenza, non una scelta di struttura.
