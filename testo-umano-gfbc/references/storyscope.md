# StoryScope: Investigating idiosyncrasies in AI fiction

Russell, Rajendhran, Pham, Iyyer, Wieting — University of Maryland, Google DeepMind.
arXiv:2604.03136v6 [cs.CL], 10 agosto 2026. Licenza CC0. Codice e dati:
https://github.com/jenna-russell/storyscope (prompt, 51.336 racconti AI, feature per
racconto; i racconti umani non sono rilasciati per copyright).

Questo file riporta tutto il contenuto del paper che serve a scrivere: metodo, numeri,
tabelle complete, limiti. Le regole operative stanno in `../SKILL.md`; qui ci sono le prove.

## 1. Domanda e risultato

I detector di testo AI lavorano sullo stile (parole come «delve», trattini lunghi,
sintassi). Lo stile però è effimero: GPT-5.4 ha ridotto i trattini; un fine-tuning
sullo stile umano fa scendere il rilevamento nella scrittura creativa dal 97% al 3%
(Chakrabarty et al., 2026). Il paper chiede se i racconti AI si distinguono da quelli
umani **senza** segnali stilistici, usando solo scelte narrative a livello di discorso
(agency dei personaggi, discontinuità cronologica, esplicitazione del tema…), che per
essere «umanizzate» richiedono riscritture strutturali, non ritocchi.

Risultato: le sole feature narrative (257) raggiungono **93,2% macro-F1** nel
riconoscimento umano/AI e **68,4%** nell'attribuzione a sei fonti, cioè oltre il 97% di
quanto ottiene il modello che usa anche lo stile. Trenta feature «core» bastano per
l'84,8%. Dopo un editing di superficie che rimuove gli artefatti stilistici (LAMP), il
rilevamento resta al **93,9%**. I cinque modelli AI occupano una regione condivisa dello
spazio narrativo; i racconti umani sono più dispersi e più rari (percentile medio di
rarità 0,71 contro 0,49).

Contesto citato in apertura: nel marzo 2026 Hachette ha ritirato il romanzo horror *Shy
Girl* segnalato come ~78% AI; Pangram ha stimato AI-generata circa il 20% di un campione
di 14.000 romanzi autopubblicati su Amazon (+41% anno su anno).

## 2. Dati

- 10.272 racconti umani estratti da Books3 (antologie di racconti individuate con
  Gemini 2.5 Flash su titoli e blurb; uso dichiarato solo accademico).
- Per ogni racconto umano, Gemini 2.5 Flash (giugno 2025) ricava un prompt di scrittura
  che conserva personaggi, ambientazione e direzione tematica (prompt in Figura 6:
  inizia con «Write a short story», nomina almeno un personaggio o luogo, un solo
  paragrafo ≤ 120 parole, niente «in the style of», niente seconda persona).
- Lo stesso prompt va a cinque LLM: Gemini 3 Flash, Kimi K2.5, DeepSeek V3.2, Claude
  Sonnet 4.6, GPT-5.4. Sei «fonti» in tutto; 61.608 racconti; 24 rifiuti.
- Lunghezza media 4.753 parole. Il prompt chiede «approximately N words»
  (media 6.242, mediana 5.000).

| Fonte | Media parole | Mediana | Scarto medio dal target | Entro ±10% |
|---|---|---|---|---|
| Umani | 6.403 | 5.035 | — | — |
| Gemini 3 Flash | 3.155 | 2.967 | −3.089 | 19,4% |
| GPT-5.4 | 6.651 | 6.515 | +409 | 9,6% |
| Claude Sonnet 4.6 | 6.817 | 6.187 | +575 | 38,4% |
| DeepSeek V3.2 | 2.946 | 2.693 | −3.296 | 12,8% |
| Kimi K2.5 | 3.274 | 3.005 | −2.968 | 15,6% |

Le identità delle fonti sono anonimizzate in tutti i prompt rivolti agli LLM; l'ordine
di presentazione nei confronti è randomizzato.

## 3. Pipeline StoryScope

Tre stadi, guidati dalla tassonomia NarraBench (Hamilton et al., 2025), di cui il paper
adotta 10 dimensioni su 12: Agent, Social Network, Event, Plot, Structure, Setting,
Time, Revelation, Perspective, Style (esclusi Paratext e Motivation). La dimensione
temporale riprende ordine/durata/frequenza di Genette (1980); l'arco di trama Tian et
al. (2024).

1. **Template strutturati.** GPT-5.1 estrae da ogni racconto un JSON per le dieci
   dimensioni (personaggi con ruolo, tratti, traiettoria emotiva e di motivazione,
   trope; relazioni; sequenza di eventi con chi/dove/cosa/quando; catena causale;
   schema narrativo; temi, morale, ostacolo, conflitto, arco; luoghi, epoca,
   atmosfera; suspense, curiosità, sorprese; struttura temporale, durata, flashback,
   salti; punto di vista, focalizzazione, parlanti; allusioni, figure, immagini,
   complessità sintattica, linguaggio valutativo). Il template astrae dalla superficie
   verbale: i confronti ragionano sul contenuto narrativo. Prova di necessità: senza
   template le top-20 feature scoperte sono stilistiche (umorismo, registro, tipo di
   allusione); con template sono strutturali (archi emotivi, traiettorie relazionali,
   densità di eventi, flashback); solo 6 su 20 in comune.
2. **Analisi comparativa fra fonti.** Pool di scoperta: 100 prompt × 6 fonti = 600
   racconti, tenuti fuori dal corpus principale. GPT-5.1 con reasoning alto riceve i
   sei template dello stesso prompt (in batch di 3,1 prompt in media, 32 batch) e
   produce note per fonte e dimensione, divergenze e un sommario di pattern
   ricorrenti. Comprime ~2,7 M token di testo grezzo in ~686 K token di osservazioni.
3. **Scoperta delle feature.** Dieci prompt «esperti», uno per dimensione, chiedono a
   GPT-5.1 feature discriminanti come domande chiuse con risposte discrete. Tre
   esecuzioni, unione: 408 candidate. Deduplicazione con embedding F2LLM-4B, single
   linkage a coseno 0,85 (0,90 lasciava duplicati evidenti): 304 feature finali, 65
   cluster fusi. Tipi: categoriche 124, ordinali 59, scale 1–5 45, binarie 44,
   multi-selezione 32.

**Assegnazione.** Gemini 3 Flash con thinking minimo valuta ogni racconto su tutte le
304 feature, una dimensione per chiamata (la chiamata unica copriva il 68,4% delle
feature, per dimensione il 95,4%). Ripetibilità su 5 esecuzioni: Krippendorff α = 0,90,
Cohen κ medio 0,89. Validazione umana su 240 item (12 racconti, 2 annotatori): κ
umano–modello medio 0,84 (0,91 e 0,77), κ umano–umano 0,74.

**Confine dello stile.** Feature di stile = texture di frase (dizione, sintassi, ritmo,
densità figurativa, registro, allusione a livello di prosa); non-stile = contenuto e
struttura (eventi, causalità, chiusura, ruoli, topologia delle relazioni,
ambientazione, ordine temporale). Regola per i casi grigi: se si risponde solo dalla
texture è stile. Densità sensoriale, profondità di accesso interiore e discontinuità
cronologica sono classificate non-stile. Un audit con GPT-5.4 marca 47 feature come
stilistiche (39 della dimensione Style + 8 altrove); ne restano 257 per il modello
«Narrative».

**Classificatore.** XGBoost (scelto su lineari e random forest) con SHAP per
l'importanza per feature. Colonne codificate: 1.108 (Narrative + Style), 958
(Narrative), 129 (Style only). Iperparametri da grid search sulla validazione: binario
420 alberi, profondità 8, λ = 2,0; sei classi 500 alberi, profondità 7, λ = 1,0. Split per prompt: 7.383 train / 1.405 val / 1.384 test;
finale addestrato su train+val (52.707 racconti) e valutato su 8.301 racconti. Binario
con peso 5:1 sulla classe umana; una classe «tutto AI» farebbe 83,3% accuratezza, per
questo si riportano macro-F1 e AUPRC.

**Ruoli delle feature.** Da bootstrap SHAP (B = 50 iterazioni con ricampionamento per
prompt).
*Core* (30): stabili e importanti nel binario, separazione coerente su tutti e cinque i
modelli AI, gap medio umano–AI di almeno 0,20 e dispersione fra modelli AI al massimo 0,35
(stabilità ≥ 0,55, presenza nella top-25 ≥ 0,60);
firmate come «umane» o «AI» dal verso del gap. *Fingerprint* (75): dal compito a sei
classi, importanza SHAP concentrata su una fonte con valori visibilmente diversi.

## 4. Risultati: umano vs AI (Tabella 2)

| Metodo | Feature | Macro-F1 | AUPRC |
|---|---|---|---|
| Narrative | 257 | 93,2 | 0,959 |
| Core only | 30 | 84,8 | 0,828 |
| Core + Fingerprint | 101 | 91,1 | 0,934 |
| Narrative + Style | 304 | 96,0 | 0,982 |
| Style only | 39 | 85,8 | 0,867 |
| ModernBERT (testo grezzo) | — | 99,9 | 1,00 |
| Stilometria + XGB | 144 | 99,8 | 0,999 |
| TF-IDF + XGB | 5.000 | 99,7 | 0,999 |
| Binoculars (zero-shot) | — | 55,9 | 0,404 |
| Racconti Gemini editati con LAMP | — | 93,9 | 0,988 |

Le baseline su testo grezzo sono quasi perfette: lo stile resta il segnale più forte.
Le 30 feature core valgono da sole quanto le 39 di stile. Il modello narrativo recupera
il 97% del modello combinato.

**Lunghezza.** I racconti umani sono più lunghi. Su un sottoinsieme di test bilanciato
per decili di lunghezza (2.754 racconti, mediane 4.973 vs 4.951 parole) il modello
narrativo resta a 93,2%; per terzili corti/medi/lunghi 91,6 / 94,3 / 93,7. Una
regressione sulla sola lunghezza fa 55,9%.

**Argomento.** Classificando i racconti per codice BISAC (Qwen3.5-9B), il binario va da
90,0% (mystery) a 96,2% (storico); nessuna differenza significativa fra i sei generi
con ≥ 20 prompt (Kruskal–Wallis).

**Memorizzazione.** Screening su 13-gram esatti e 8-gram: 0,70% delle coppie ad alto
rischio, concentrate in testi canonici (Yellow Wallpaper, Sleepy Hollow, Heart of
Darkness, Cthulhu, Poe, Doyle, Wilde, Dickens). Rimuovendo 169 prompt (1,67%) i
risultati non cambiano (93,18 → 93,23 binario; 68,42 → 68,68 sei classi).

**Ablazioni per dimensione.** Nessuna dimensione basta da sola (la migliore, Agents,
80,2% binario) e nessuna è necessaria (toglierla costa al massimo −1,2). Il segnale è
ridondante: trame lineari, causalità stretta, tema esplicito e minore varietà sociale
tendono a co-occorrere.

### 4.1 Cosa separa umano da AI (30 feature core, Tabella 16)

Valori: `s` = media su scala 1–5; `o` = media su codici ordinali; `→` = prevalenza %
dell'opzione indicata. Gap = umano − AI; negativo = AI più alto. AI = media dei cinque
modelli.

**AI più alto: sovra-determinazione tematica**

| Feature | Umani | AI | Gap |
|---|---|---|---|
| Esplicitazione tematica e moralizzazione (s) | 3,28 | 3,94 | −0,65 |
| Peso morale/filosofico (s) | 3,26 | 3,68 | −0,42 |
| Unità tematica (s) | 4,41 | 4,74 | −0,33 |
| Commento tematico del narratore → sì | 52% | 77% | −25 |
| Funzione del dialogo → dibattito filosofico | 34% | 59% | −25 |
| Esplicitezza dei riferimenti → echi impliciti | 50% | 72% | −22 |

L'AI spiega il significato invece di fidarsi del lettore: l'arco di un personaggio in
lutto finisce di norma con il narratore che enuncia la lezione imparata.

**AI più alto: performatività sensoriale e corporea**

| Feature | Umani | AI | Gap |
|---|---|---|---|
| Espressione emotiva → metafore corporee | 38% | 81% | −42 |
| Ambientazione come specchio psicologico (s) | 3,58 | 4,07 | −0,49 |
| Enfasi ambientale ed ecologica (s) | 2,83 | 3,21 | −0,38 |
| Modalità sensoriali → olfatto | 57% | 82% | −26 |
| Densità sensoriale (s) | 3,66 | 3,93 | −0,26 |
| Profondità di accesso all'interiorità (s) | 3,67 | 3,93 | −0,26 |

Dove un autore umano scrive che il personaggio «aveva paura», l'AI rende la paura come
petto che si stringe, sudore freddo, lampada che si abbassa. Gli umani usano etichette
emotive esplicite il 29% delle volte, l'AI l'8%.

**AI più alto: semplificazione strutturale**

| Feature | Umani | AI | Gap |
|---|---|---|---|
| Continuità della catena causale (s) | 3,92 | 4,20 | −0,28 |
| Granularità spaziale (o) | 2,27 | 2,53 | −0,26 |
| Agency nella risoluzione → scelta del protagonista | 46% | 69% | −23 |
| Introduzione del personaggio → descrizione esterna | 30% | 52% | −22 |
| Integrazione sottotrame → nessuna sottotrama | 57% | 79% | −22 |
| Modo di risoluzione → comprensione/accettazione interiore | 27% | 47% | −21 |
| Radicamento spaziale in apertura (o) | 2,12 | 2,33 | −0,20 |
| Investimento sul personaggio prima della minaccia (s) | 2,76 | 2,99 | −0,23 |

L'AI preferisce un binario unico con pochi fili sciolti; gli umani sono più disordinati,
con salti temporali e catene causali spezzate. Un giallo umano può aprire al funerale e
tornare indietro di decenni; l'AI racconta la stessa storia dal primo indizio alla
rivelazione.

**Umani più alto: ricchezza intertestuale**

| Feature | Umani | AI | Gap |
|---|---|---|---|
| Strategia intertestuale → riferimento esplicito nominato | 47% | 24% | +23 |
| Esplicitezza dei riferimenti → mix bilanciato | 37% | 16% | +21 |

Gli umani citano testi e autori specifici a quasi il doppio; l'AI resta su allusioni
vaghe ed evita di nominare marchi, luoghi, opere reali.

**Umani più alto: coinvolgimento del lettore**

| Feature | Umani | AI | Gap |
|---|---|---|---|
| Permeabilità della quarta parete (o) | 0,67 | 0,39 | +0,28 |
| Indirizzo diretto al lettore (o) | 0,28 | 0,07 | +0,21 |

Gli umani rompono la quarta parete nel 67% dei casi contro il 39%, si rivolgono al
lettore nel 28% contro il 7%. L'AI scrive come se nessuno guardasse.

**Umani più alto: complessità temporale**

| Feature | Umani | AI | Gap |
|---|---|---|---|
| Profondità di ricontestualizzazione dopo la sorpresa (s) | 3,28 | 2,95 | +0,34 |
| Discontinuità cronologica (s) | 2,40 | 2,12 | +0,28 |
| Inquadratura non lineare per rivelazione ritardata (s) | 1,96 | 1,68 | +0,28 |
| Intensità di anacronia (flashback/flash-forward) (s) | 2,58 | 2,31 | +0,27 |

**Umani più alto: varietà narrativa**

| Feature | Umani | AI | Gap |
|---|---|---|---|
| Varietà di luoghi (o) | 1,34 | 1,08 | +0,26 |
| Proporzione dialogo/narrazione (s) | 2,95 | 2,70 | +0,24 |
| Integrazione sottotrame → parallele al tema | 42% | 21% | +22 |
| Polarità morale del protagonista → ambivalente | 59% | 38% | +21 |
| Espressione emotiva → etichette esplicite | 29% | 8% | +21 |

### 4.2 L'editing di superficie non cambia la struttura

LAMP (Chakrabarty et al., 2025) riscrive a livello di span sette categorie di artefatti
AI (cliché, esposizione ridondante, prosa «viola»…) con 25 esempi di scrittori
professionisti. Applicato a 278 racconti Gemini, riscrittore Gemini stesso: il
rilevamento narrativo passa da 95,5% a 93,9% macro-F1 (AUPRC da 0,996 a 0,988), −1,6
punti. Togliere frasi fatte e prosa gonfia non tocca linearità causale, esplicitazione
tematica, sovra-descrizione sensoriale.

## 5. Attribuzione a sei fonti (Tabella 3 e 12)

| Metodo | Feature | Macro-F1 | Acc. |
|---|---|---|---|
| Narrative | 257 | 68,4 | 68,4% |
| Core only | 30 | 46,5 | 46,8% |
| Core + Fingerprint | 101 | 63,4 | 63,6% |
| Narrative + Style | 304 | 77,3 | 77,3% |
| Style only | 39 | 60,4 | 60,5% |
| ModernBERT / Stilometria / TF-IDF | — | 99,8 / 99,6 / 99,5 | — |

F1 per classe (con stile / solo narrativa): umani 0,93 / 0,89; Claude 0,89 / 0,77; GPT
0,82 / 0,73; Gemini 0,67 / 0,60; DeepSeek 0,66 / 0,57; Kimi 0,67 / 0,55. Le sei coppie
più confuse sono tutte AI–AI; la maggiore (Gemini↔DeepSeek, 222 e 207 racconti) supera
di molto la più comune confusione con gli umani (umani↔Kimi, 46).

**Geometria.** Nello spazio z-scored con distanza euclidea, la distanza media fra
centroide umano e centroidi AI è 6,6 contro 4,3 fra centroidi AI (1,6×); la coppia
umano–AI più vicina (6,2) è più distante della coppia AI–AI più lontana (6,0). Gli
umani sono più dispersi: distanza media dal proprio centroide 33,2 contro 27,4 (+22%),
raggio mediano dei 10 vicini 33,1 contro 29,2.

**Rarità.** Rarità per racconto = distanza media dai k = 25 vicini più prossimi nello
spazio train+val. Percentile medio umani 0,71, AI 0,49 (Cohen d = 0,83, AUC 0,73). Nel
10% più raro: 24,7% degli umani, 7,1% degli AI; nell'1% più raro 3,0% contro 0,6%. Per
prompt, il racconto umano è il più raro dei sei nel 57,8% dei casi (caso: 16,7%).
Composizione delle code sul test (1.377 racconti per fonte):

| Coda | Umani | Claude | GPT | DeepSeek | Kimi | Gemini |
|---|---|---|---|---|---|---|
| Top 1% | 42 | 5 | 5 | 11 | 6 | 14 |
| Top 5% | 180 | 33 | 34 | 58 | 64 | 45 |
| Top 10% | 340 | 66 | 71 | 127 | 135 | 88 |

Numero di impronte per fonte: umani 32, Claude 26, GPT 11, Gemini 11, DeepSeek 7,
Kimi 3.

### Impronte per fonte (Tabella 17, prime 5 per rapporto di unicità)

**Umani** — introduzione del personaggio → in dialogo (unicità 21,4); ampiezza di
focalizzazione → focale singolo (15,7); modo di indirizzo del narratore → nessun
indirizzo diretto (12,6); ritmo delle rivelazioni → concentrato in fondo (7,7);
ambizione letteraria → genere crossover (6,8); + 27 altre (visibilità del trattenere,
tecniche atmosferiche, densità di sottotrame, naming, posizione del twist…).

**Claude Sonnet 4.6** («keeps it cool», profilo più distintivo fra gli AI) — forza
dell'escalation degli eventi (SHAP 0,402, unicità 22,4): l'intensità cresce meno che in
ogni altra fonte; diversità dei tipi di evento (0,491; 10,7); ambito temporale del
finale → epilogo/flash-forward (8,9); sogni/visioni come distorsione temporale → no
(7,7); atmosfera → uncanny/haunted (4,6); + 21 altre (densità di eventi, modalità di
conflitto, traiettoria relazionale, eteroglossia, chiusura…). Voce narrativa la più
uniforme. Approccio reverente/continuista alla tradizione: onora ed estende le
convenzioni invece di sovvertirle (62% contro 39–56%). Finali quieti, non «a valanga».

**GPT-5.4** («likes to gossip») — ruolo di pettegolezzo e voci → saliente (0,200;
22,1; 64% contro 44–55%); distanza temporale del narratore → retrospettiva distante
(6,8), storie inquadrate come riflessioni su fatti di anni o decenni prima; strategia
verso le attese del lettore → le sovverte (3,9; 41% contro 27–36%); narrazione
iterativa/abituale → no (3,2); riconciliazione/perdono → parziale o ambiguo (2,6); + 6
altre (salienza della comunità, enfasi sociale, competenza del lettore,
individualizzazione, profondità psicologica). Reti sociali corali a livello umano.

**Gemini 3 Flash** — traiettoria sociale del protagonista → si espande (5,0);
bilanciamento del discorso → prevalentemente diretto (3,6); schema narrativo →
assedio/ordalia (3,5); naming → nome proprio (3,2); struttura cronologica → flashback
frequenti (3,1); + 6 altre. Finali più ordinati, denouement estesi, ambientazioni più
cupe (88% «bleak and oppressive»). Default: descrizione esterna del personaggio.

**DeepSeek V3.2** — presenza/visibilità del narratore (4,1); espressione emotiva →
indizi comportamentali (3,6); orientamento trama vs atmosfera (2,9); collocazione del
backstory → interfogliato uniformemente (2,7); scene di racconto incastonato (2,2);
+ 2 altre (stagioni/tempo ciclico…). Anticipa il contesto cruciale che altre fonti
rimandano.

**Kimi K2.5** — introduzione del personaggio → in azione (3,7); ingresso narrativo →
in medias res (3,0); etichettatura esplicita dei tratti → no (2,0). Meno impronte, F1
più basso: centro generico della distribuzione AI.

## 6. Cosa il paper dice di sé

- **Ambito misurato:** racconti in inglese, ~5.000 parole, generati da un prompt che
  ricalca un racconto umano pubblicato; cinque modelli di inizio 2026. Nessuna misura
  su saggistica, articoli, post, mail, testi in italiano.
- **Costo:** ~4,4 k$ in tutto: ~2.800 $ per generare i racconti, ~1.600 $ per estrarre
  le feature con Gemini 3 Flash.
- **Proxy di originalità:** rarità statistica nello spazio delle decisioni narrative,
  collegata alla nozione di originalità di Torrance (1966) e alla soglia minima del
  diritto d'autore statunitense (Feist 1991; US Copyright Office 2023).
- **Durabilità:** le feature narrative dovrebbero resistere più dello stile
  all'evoluzione dei modelli, perché cambiarle richiede riscritture strutturali.
- **Etica:** Books3 usato solo a fini accademici; LLM e coding agent (Claude Code e
  Codex) usati per aiutare e rifinire la scrittura del paper e alcune tabelle.

## 7. Lavori citati utili

- Chakrabarty et al. 2025 (LAMP, riscrittura a span degli artefatti AI); 2026
  (fine-tuning su stile umano abbatte il rilevamento da 97% a 3%).
- Hamilton et al. 2025 (NarraBench, tassonomia delle dimensioni narrative).
- Reinhart et al. 2025 (gli LLM convergono su una grammatica e retorica ristrette).
- Beguš 2024 (storie umane: più sfumatura culturale, ambiguità emotiva, svolte
  inattese di GPT). Nonaka & Perry 2025 (strutture sociali più semplici nella fiction
  AI). Doshi & Hauser 2024; Jiang et al. 2025 (gli LLM riducono la diversità
  collettiva). Xu et al. 2025a (elementi di trama ripetuti fra generazioni).
- Russell et al. 2025 (esperti umani riconoscono l'AI con accuratezza quasi perfetta).
