---
name: testo-umano-gfbc
description: >-
  Scelte di struttura per qualsiasi testo che una persona leggerà: articolo, post,
  mail, lettera, documento, racconto, copy, messaggio a un cliente. Da caricare PRIMA
  di scrivere, non dopo: le scelte narrative (cosa si spiega, come si chiude, come si
  mostra un'emozione, chi si nomina, se si parla al lettore) restano riconoscibili
  anche dopo la pulizia stilistica. Basata su StoryScope (arXiv 2604.03136).
  Trigger: scrivere, riscrivere o rivedere testo per umani; «sembra scritto dall'AI»;
  «rendilo umano»; «più naturale». Dopo la stesura passa a humanizer per la superficie.
metadata:
  version: "1.1.2"
---

# Testo umano

`humanizer` toglie i tic di superficie: «delve», trattini, triadi, chiusure a effetto.
StoryScope (Russell et al., UMD + DeepMind, 2026) mostra che non basta. Su 61.608
racconti, tolto ogni segnale di stile, un classificatore distingue umano da AI al
93,2% macro-F1. Su 278 racconti Gemini sottoposti a un editing di superficie che
rimuove cliché e prosa gonfia (LAMP), il rilevamento scende solo da 95,5% a 93,9%. Quello che tradisce è la **struttura**, e la struttura si
decide prima della prima frase. Ordine obbligato: prima queste scelte, poi la
stesura, poi `humanizer`.

**Ambito delle prove.** Il paper misura fiction in inglese, ~5.000 parole, cinque
modelli di inizio 2026 (Claude Sonnet 4.6, GPT-5.4, Gemini 3 Flash, DeepSeek V3.2,
Kimi K2.5). Le regole per testo non narrativo sono **derivate**, non misurate, e sono
marcate così. Numeri e tabelle complete: `references/storyscope.md`.

## Come si usa

1. **Prima di scrivere.** Scorri le sette scelte. Per questo pezzo decidi quali
   default AI eviti: almeno due, di norma tre. Due righe nel piano o nel messaggio,
   non un rituale. Un post da 1.500 caratteri ne regge due; un articolo o un racconto
   tutte e sette.
2. **Scrivi.** Le regole del progetto (buzzword vietate, stampo, lunghezze, marchi
   ammessi, dati veri) restano e vincono.
3. **Autoverifica** (in fondo), poi `humanizer` per la superficie.
4. **Revisione di testo altrui.** Leggi prima per struttura, poi per parole: le sette
   domande sono la griglia. Un testo pulito di parole e AI di struttura resta AI.

## Le sette scelte

Le 30 feature core del paper, raggruppate come nella sua Tabella 16. Ogni numero è
umani contro media dei cinque modelli.

### 1. Non spiegare la morale

Il narratore esplicita il tema nel 77% dei racconti AI, nel 52% di quelli umani.
Esplicitazione tematica 3,94 contro 3,28 su 5; peso morale 3,68 contro 3,26; unità
tematica 4,74 contro 4,41; dialogo come dibattito filosofico 59% contro 34%.

- Il pezzo finisce sull'ultimo fatto, non sulla lezione. Niente paragrafo che dice al
  lettore cosa ha appena capito.
- Non tutto deve servire un tema solo. Un dettaglio che non «serve» è umano.
- Le persone citate parlano di cose concrete, non di massimi sistemi.
- *Derivata, non narrativo:* niente «In sintesi» che rimastica, niente «quello che
  conta davvero è», niente morale del caso studio. Il consiglio si dà una volta,
  dentro l'argomento, non in coda.

### 2. Nomina l'emozione, non farla recitare al corpo

L'AI rende l'emozione con metafore corporee nell'81% dei casi, gli umani nel 38%.
Etichette esplicite («aveva paura»): umani 29%, AI 8%. Olfatto 82% contro 57%.
Ambiente come specchio interiore 4,07 contro 3,58; densità sensoriale 3,93 contro
3,66; accesso all'interiorità 3,93 contro 3,67.

- «Show, don't tell» è il default della macchina, non la regola umana. Scrivi «ero
  preoccupato», «mi ha dato fastidio», «il cliente era arrabbiato».
- Stomaco chiuso, mani fredde, luce che cala, odore di qualcosa: in stesura di norma
  uno per pezzo, e solo se è successo davvero. In revisione una sensazione vera non si
  cancella: si affianca al nome dell'emozione, non lo sostituisce.
- Il meteo e la stanza non commentano lo stato d'animo di nessuno.
- In un testo che afferma fatti (post, articolo, mail) l'emozione nominata è quella
  vera di chi firma: non se ne inventano per sembrare umani (vedi humanizer: niente
  aggiunte non supportate). Nella fiction è quella del personaggio, e inventarla è il
  compito.

### 3. Lascia un filo sciolto

Nessuna sottotrama: AI 79%, umani 57%. Sottotrame parallele al tema: umani 42%, AI
21%. Continuità della catena causale 4,20 contro 3,92. Risoluzione per scelta del
protagonista 69% contro 46%; per comprensione o accettazione interiore 47% contro 27%.
Protagonista moralmente ambiguo: umani 59%, AI 38%.

- Una digressione che non torna nel finale è ammessa.
- Non chiudere tutto. Il finale «e allora ho capito che…», la serena accettazione, è
  il finale che l'AI sceglie quasi il doppio delle volte (47% contro 27%).
- Chi racconta (io, l'azienda, il cliente, il tecnico) può aver sbagliato e non aver
  imparato niente. Nessuno ha sempre ragione.
- Non ogni evento deve causare il successivo. Le cose a volte succedono e basta.

### 4. Rompi la linea del tempo

Discontinuità cronologica: umani 2,40, AI 2,12. Anacronia (flashback, flash-forward)
2,58 contro 2,31. Inquadratura non lineare per ritardare una rivelazione 1,96 contro
1,68. Una rivelazione che costringe a rileggere quanto letto prima: 3,28 contro 2,95.

- Non «primo indizio → gran finale». Parti dalla fine, dal risultato, dalla
  telefonata del cliente arrabbiato, e torna indietro.
- Una rivelazione tardiva che cambia il senso delle pagine precedenti: la macchina la
  usa meno (2,95 contro 3,28).
- *Derivata, non narrativo:* in un caso studio o in un post di esperienza apri
  dall'esito o da un momento a metà. La cronologia ordinata dall'inizio è il default
  da evitare. Nei testi tecnici e procedurali l'ordine resta quello logico.

### 5. Fai i nomi

Riferimenti espliciti a opere e autori nominati: umani 47%, AI 24%. Mix di riferimenti
espliciti e impliciti: 37% contro 16%. Echi vaghi: AI 72%, umani 50%. L'AI evita di
nominare marchi, luoghi e opere reali.

- Opere, autori, marchi, luoghi, norme, prodotti, persone: col nome. «Un noto
  produttore» → il produttore. «Una normativa recente» → il decreto con la data. «Uno
  studio dice» → chi e quando, oppure taglia.
- I vincoli del progetto restano: marchi solo quelli gestiti, dati con fonte, privacy
  delle persone. Non si inventa un nome per riempire il vuoto. Un fatto vero di cui
  non si può fare il nome resta, anonimo e intero («un cliente di provincia, tre guasti
  in un inverno»). Si taglia il riferimento vago che non porta nessun fatto («alcuni
  studi dicono»).

### 6. Parla al lettore

Quarta parete rotta: umani 67%, AI 39%. Indirizzo diretto («tu», «lo so, anche a te»):
umani 28%, AI 7%. L'AI scrive come se nessuno guardasse.

- Dai del tu. Fai una domanda vera, non retorica di maniera. Un inciso rivolto a chi
  legge («l'ho pensato anch'io la prima volta»).
- Testo tecnico o legale: il tu resta, l'inciso no.

### 7. Allarga il repertorio

Introduzione del personaggio per descrizione esterna: AI 52%, umani 30% (l'impronta
umana numero uno è l'ingresso in dialogo). Radicamento spaziale in apertura 2,33
contro 2,12; granularità spaziale 2,53 contro 2,27. Dialogo su narrazione: umani 2,95,
AI 2,70. Varietà di luoghi 1,34 contro 1,08. Rarità: gli umani stanno nel 10% più raro
dello spazio narrativo nel 24,7% dei casi, l'AI nel 7,1%.

- Chi entra in scena entra parlando o facendo, non con la scheda («Marco, 45 anni,
  tecnico con vent'anni di esperienza»).
- Non aprire con l'ambientazione.
- Più voce diretta: cita le persone come hanno parlato, anche sgrammaticate.
- Cambia luogo. Un pezzo tutto nella stessa stanza è un default.
- Prima di scrivere elenca i default (apertura, ordine, chiusura, come entrano le
  persone, come si mostra l'emozione) e scartane almeno due.

## Contro-impronte per chi sta scrivendo

Ogni modello ha le sue. Chi scrive controlla le proprie, non quelle altrui.

**Claude** (Sonnet 4.6, 26 impronte, il modello AI più riconoscibile). Escalation
degli eventi la più piatta di tutte le fonti; voce narrativa la più uniforme;
reverente verso la tradizione (62% contro 39–56%: onora le convenzioni, non le
sovverte); tende all'epilogo o al flash-forward finale; evita i sogni; atmosfera
«uncanny»; preferisce i finali quieti a quelli a valanga. Sono tendenze misurate come
impronte, non assenze assolute.
→ Lascia che qualcosa peggiori davvero. Cambia registro a metà. Niente epilogo che
rassicura. Il finale può essere brusco. Una convenzione, una sola, va rotta.

**GPT / Codex** (GPT-5.4). Pettegolezzo e voci come motore (64% contro 44–55%);
distanza retrospettiva («anni fa», «ricordo quando»); sovverte le attese più degli altri
modelli AI (41% contro 27–36%; il confronto con gli umani non è riportato); riconciliazioni lasciate ambigue; evita la narrazione abituale.
→ Niente «si dice», niente cornice di ricordo a distanza. Il colpo di scena non è
obbligatorio. Racconta anche la routine («ogni lunedì mattina»).

**Gemini**: descrizione esterna del personaggio, finali ordinati, denouement lunghi,
ambientazioni cupe (88%). **DeepSeek**: anticipa il contesto cruciale che altri rimandano, narratore
visibile, emozione per indizi comportamentali. **Kimi**: in medias res, ingresso in
azione, poche impronte: è il centro generico della distribuzione AI.

## Cosa non fare

- Non applicare tutto a tutto. Tre scelte non-default in un post valgono più di sette
  forzate. Il paper misura una regione dello spazio, non una checklist da riempire.
- Testo tecnico, legale, normativo, procedurale: pesano 1, 5, 6. Le altre poco o
  niente. Un manuale non ha bisogno di flashback.
- Non inventare nomi, fatti o emozioni per «umanizzare» un testo che afferma fatti.
  Vale la regola di humanizer: nessuna aggiunta non supportata dalla fonte o da chi
  firma; la fiction è esente, perché lì inventare è il compito.
- Non usare questa skill per far passare per umano un testo che va dichiarato AI dove
  la dichiarazione è dovuta.

## Autoverifica, prima di humanizer

1. Ultimo paragrafo: un fatto o una lezione?
2. Emozioni: nominate o recitate dal corpo e dall'ambiente?
3. Il pezzo chiude tutto? C'è almeno un filo lasciato?
4. Ordine: cronologico dall'inizio? Se sì, perché?
5. Riferimenti: quanti col nome, quanti vaghi?
6. Il lettore è nominato almeno una volta dove ha senso?
7. Le persone entrano parlando o facendo, o con la scheda? Quanta voce diretta?
8. L'impronta del modello che sta scrivendo: controllata?

## Riferimenti

- `references/storyscope.md`: metodo, tutte le tabelle, impronte, limiti del paper.
- `references/blocco-runtime.md`: il blocco da appendere ai system prompt delle app che
  generano testo per un cliente a runtime.
- `humanizer` (https://github.com/blader/humanizer, skill di terzi da installare a
  parte): superficie, dopo la stesura.
