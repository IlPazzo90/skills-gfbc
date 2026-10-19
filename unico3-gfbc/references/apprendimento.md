# Come questa skill impara

Unicò cambia, e questa skill è stata scritta da qualcuno che il programma lo stava
imparando. Quindi contiene errori che non sa ancora di avere. Il modo di scoprirli è
usarla; il modo di non riperderli è questo file.

Non è un invito generico a «documentare». È una procedura con un rito di chiusura e un
controllo eseguibile.

---

## 1. Quando scatta

Tre innesti, e basta uno:

| Innesto | Come si riconosce |
|---|---|
| **Smentita** | Un file dice X, Unicò fa Y. Il selettore non c'è, la rotta apre un'altra cosa, il campo si chiama diversamente. |
| **Novità** | Ho fatto qualcosa che nei file non c'era: un'area mai aperta, un flusso mai eseguito, un comportamento mai visto. |
| **Cambiamento** | Futura SI ha aggiornato il programma. Quello che era vero resta scritto, ma non è più vero. |

Il caso più insidioso è il terzo, perché non produce un errore: produce una procedura
che gira e restituisce la cosa sbagliata.

> **Regola pratica.** Se durante una sessione ho dovuto capire qualcosa che nei
> `references/` non c'era, quella cosa va scritta **prima di chiudere la sessione**.
> Non «quando c'è tempo»: la sessione dopo riparte da zero e la scoperta è persa.

---

## 2. La regola che vale più di tutte: si consolida, non si appende

Il modo naturale di aggiornare un file è aggiungere in fondo *«Correzione del …»*. È
comodo, ed è sbagliato: chi legge dall'alto **incontra prima la versione smentita**, e
di solito smette di leggere quando ha trovato una risposta.

`mappa-web.md` ne è la prova: porta ancora in coda un blocco *«Correzione e censimento
del 03/09/2026»* con la verità nuova, mentre più su restava la vecchia.

Quindi:

1. **La correzione si scrive dove stava l'errore.** Si riscrive il paragrafo.
2. Se la storia serve — perché la vecchia versione era plausibile e qualcuno potrebbe
   riproporla — resta **una riga**, non un blocco: *«prima leggevo 16: era una pagina
   sola della tendina»*.
3. Se dopo la modifica due punti del file dicono cose diverse, **il file è rotto**, non
   «in evoluzione».

E prima di scrivere, si cerca: `grep -rn "<parola chiave>" SKILL.md references/`. Metà
delle contraddizioni nasce dallo scrivere in un file secondo qualcosa che stava già in
un altro.

---

## 3. Che grado di verità ha quello che sto scrivendo

Tre marcature, e vanno usate:

- **`[misurato GG/MM/AAAA]`** — l'ho eseguito e ho letto il risultato. È l'unica che
  autorizza un numero.
- **`[da guida]`** — sta nella guida ufficiale, non l'ho visto succedere. La
  guida descrive anche Unicò NET, che sul web non esiste: `cosa-il-web-non-fa.md`.
- **`[da verificare]`** — dedotto, plausibile, non provato. Usabile, ma dichiarato.

**Dove misura e guida divergono vince la misura**, e si scrive che divergono: sapere che
la guida dice un'altra cosa evita di «correggere» domani la misura riportandola alla
guida.

Una `[da verificare]` diventa misurata solo quando qualcosa è **andato a buon fine**
usandola. Non quando sembra giusta.

---

## 4. Dove va cosa

| Ho scoperto | Va in |
|---|---|
| Una rotta, un selettore, la struttura di una schermata | `mappa-web.md` (rotte tabella: `tabelle-rotte.md`) |
| Una trappola dell'interfaccia che è costata tempo | `interazione.md`, scritta **come si evita**, non come è successa |
| **Un numero** | `fatti-misurati.md` — riga nel registro — *poi* nel testo che lo usa |
| Una procedura che ho eseguito per intero | un file in `flussi/`, con i passi veri e i punti dove mi sono fermato |
| Come si comporta un'area del programma | il `references/` di quell'area |
| Un'azione che può fare danno | `guardrail.md` **e** `u3/guardrail.py`, con il test prima |
| Un'azione che il web non fa | `cosa-il-web-non-fa.md` |
| Un fatto permanente sul lavoro dell'utente | la memoria dell'agente |
| Una cosa da sistemare che non sistemo adesso | una nota o una issue del repository, non un blocco in fondo al file |
| Qualunque cosa delle precedenti | una riga nel diario locale, con la data, se lo tieni |

Un diario locale, non versionato, se lo vuoi, può nominare clienti e importi veri. Nei
file che invece stanno su git — procedure, `fatti-misurati.md` — un caso si cita per
numero (cliente N, impianto N), mai per nome.

Il diario non duplica i file: dice *cosa è successo quel giorno e dove è finito*. Serve
fra sei mesi, quando una riga strana sembrerà paranoia e la domanda sarà «perché».

---

## 5. Il rito di chiusura — quattro comandi

Prima di dire che una sessione su Unicò è finita:

```bash
cd <cartella della skill>
python3 -m u3.fatti          # nessun file contraddice il registro
python3 -m pytest -q         # i guardrail e gli helper reggono
git status --short           # cosa ho toccato davvero
git add -A && git commit     # messaggio descrittivo
```

`python3 -m u3.fatti` è la parte che non si salta. Il 04/09/2026 tre numeri smentiti
erano sopravvissuti in tre file diversi, e li ho trovati per caso con un `grep`. Ora
c'è la rete: legge il registro e dice **file:riga** dove qualcuno dice un altro numero.

> Se in chat ho affermato un numero nuovo, quel numero **deve** essere nel registro.
> Un numero detto e non registrato è un numero che la prossima sessione non ha.

---

## 6. Potatura — un file che cresce sempre smette di essere letto

- Un `references/` oltre le ~500 righe si spezza per area o si accorcia.
- Due paragrafi che dicono la stessa cosa: ne resta uno.
- Codice in `u3/` che non è più il percorso scelto si marca **dormiente** in
  `u3/README.md`. Non si cancella, ma non deve sembrare vivo.

---

## 7. Cosa la skill **non** impara da sola

Qui l'automatismo si ferma e si chiede:

1. **Restringere la zona rossa.** Si estende sola, si restringe solo se lo dice
   il responsabile. Se una regola sembra troppo severa, la si segnala — non la si allenta.
2. **Cambiare un verdetto di `u3/guardrail.py`.** Il codice si tocca dopo il test, e
   il test si scrive con dentro il motivo.
3. **Promuovere un `[da verificare]`** senza una prova che qualcosa ha funzionato.
4. **Cancellare una misura di una sessione precedente** perché oggi ne ho una diversa.
   Se il numero è cambiato, sono cambiati i dati o è cambiato Unicò: si scrivono
   **entrambe le date**, non si sovrascrive in silenzio.
5. **Scrivere su un'azienda che non è una sandbox** — la conferma di ieri non vale oggi.

---

## 8. E la cosa che nessuna di queste regole sostituisce

Il controllo dei fatti prova che i file **concordano fra loro**. Non prova che
concordino con Unicò. Questa skill è stata scritta e riletta dallo stesso autore, e i
punti ciechi di chi scrive sono gli stessi di chi rilegge.

L'unica prova esterna è una verifica indipendente: un modello di famiglia diversa, promptato per
confutare, con le misure sul tavolo. Va rifatto **dopo ogni sessione di apprendimento
consistente** — non solo la prima volta.
