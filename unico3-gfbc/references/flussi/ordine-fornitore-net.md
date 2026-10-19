# Ordine a fornitore su Unicò NET — procedura eseguita (produzione)

Eseguita una volta: un ordine a un fornitore con più righe, stato Confermato. Il web non ha gli
ordini a fornitore: si fanno da **NET**, Magazzino → «Ordine a fornitore». In produzione è una
scrittura che impegna soldi: serve l'ok del titolare.
Stati e tipi di riga: `references/magazzino.md`, sezione «Ordini a fornitore».

## Il lag del NET

NET è un desktop remoto in HTML5: i click si accodano e vengono eseguiti in ritardo. Un
click ripetuto perché «non è successo niente» può aprire un dialogo dopo, su un altro
documento (può aprirsi Numera su un ordine già evaso; annullato, l'ordine è
riletto EVASO). Quindi: **un campo alla volta, zoom per controllare, poi il campo dopo**.
Mai cliccare due volte un pulsante che non ha risposto.

## Coordinate (finestra Ordine, frame 1568×648, finestra in posizione di default)

| Comando | Coordinate |
|---|---|
| Salva | 523,572 |
| Nuovo | 598,572 |
| Cerca | 640,572 |
| Numera | 683,572 |
| Stampa | 726,572 |
| Ritorna | 481,575 |
| «...» fornitore | 1113,142 |
| «+» righe (scheda Dettagli) | 1193,297 |

Le coordinate cambiano se la finestra si sposta: verificare con uno screenshot.

## Passi

1. **Nuovo**. Fornitore dal «...». Il pagamento si precompila dall'anagrafica
   si cambia con quello concordato.
2. **Rif.to interno**: massimo **30 caratteri**, il resto si perde. Convenzione:
   `prev.NNN/26 - <codice impianto>`; due preventivi:
   «prev.NNN/26-<imp> NNN/26-<imp>».
3. **Alla c.a.** il referente; **Testo iniziale**: offerta del fornitore con numero e data,
   cantiere, prezzi di riferimento, resa (franco loro sede / ritiro a nostra cura).
   Il campo tiene **circa 255 caratteri** e taglia il resto senza avviso (16/10/2026):
   si scrive corto e si rilegge che l'ultima parola ci sia.
   **Banca** (banca d'appoggio RiBa): **su NET non si imposta**. La lente «...» apre una
   finestra di ricerca a dimensione zero e vuota, poi manda la finestra Ordine dietro; Tabelle →
   Banche dice «versione obsoleta del modulo» e va in errore run-time 91/440 (13/10/2026). Si
   lascia vuota.
4. **Salva la testata prima di aprire Dettagli.**
5. **Righe** con «+». Il codice si conferma con **Return**:
   - articolo con listino di quel fornitore: il prezzo arriva dal listino, si controlla con l'offerta;
   - articolo **senza listino** del fornitore: lente «...» → Cerca Articolo, Cod. Interno + Return;
     prezzo e Cod. fornitore si scrivono a mano;
   - contributi (RID e simili): **Articolo manuale**, U.d.m. «N» (servono circa 4 scroll da 3 tick
     nella tendina).
   Dopo «Salva» il dialogo della riga resta aperto: matita 1109,267 per la riga dopo,
   freccia esci 1109,234 per chiudere.
6. Il totale in basso si confronta con l'offerta/conferma del fornitore.
7. **Numera**: propone il progressivo; si sceglie **Confermato** (667,366) e **OK** (877,298).
8. **Stampa** → «Ordine» → spuntare **Prezzi** e **Usa Logo** → Stampa. Il PDF arriva in
   ~/Downloads come `AAAAMMGGThhmmss-tmpXXX.pdf`: si rinomina e si controlla con `pdftotext`.
9. Il PDF va in una **bozza** mail (non si spedisce da soli), nota UA sulle attività dei ticket.

## Verifica

Cerca → N° + stati Confermato/Evaso spuntati (la spunta In elaborazione è già attiva) →
Cerca: con un solo risultato apre direttamente l'ordine. Si legge lo Stato in testata.
