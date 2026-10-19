"""Red-zone rules: decide whether an action may run unattended.

Encodes the guardrail spec for Unico3 automation. Reads are always fine.
Writes depend on which company is active. A handful of operations are
irreversible and never run without the owner saying so out loud.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

# Anything that leaves the building. Never automatic, on any company: the
# training environment opens writes and numbering but the line is drawn
# exactly here. A "conferma" would be one distracted yes away from mail
# reaching a real customer.
VERSO_ESTERNO = {
    "invio_telematico",
    "fattura_elettronica",
    "presentazione_effetti",
    "invio_email",
    "invio_sms",
    "richiesta_feedback",
}

# Operations that destroy history or cannot be undone.
IRREVERSIBILI = {
    "annulla_numerazione",
    "accorpa",
    "ricalcolo_preventivo",
    "chiusura_esercizio",
    "chiusura_magazzino",
    "liquidazione_iva",
    "rigenera_libretto",
    "rinomina_voce_tabella",
    "elimina_insoluto",
    "importa_modelli",
    "elimina_documento",
    "elimina_intervento",
}

# Writes allowed on the training environment but never automatic elsewhere.
SCRITTURE_ESPLICITE = {"numerazione"}

# Writes the owner authorises once and for all, production included.
# Empty by default; set UNICO3_AUTORIZZATE="crea_articolo" to allow creating
# new articles without asking. Only creation: modifying an existing article
# stays a plain "scrittura" and still asks. Unknown company still asks.
# Nothing in VERSO_ESTERNO or IRREVERSIBILI can be unlocked this way.
AUTORIZZATE_OVUNQUE = frozenset(
    v.strip() for v in os.environ.get("UNICO3_AUTORIZZATE", "").split(",")
    if v.strip() in {"crea_articolo"}
)

# Settings apply to every user, and merely clicking inside a box is enough to
# raise "unsaved settings". Always ask, on any company.
SEMPRE_CONFERMA = {"salva_impostazioni"}

MOTIVI = {
    "invio_telematico": "l'invio telematico esce verso il catasto, e con CIRCE e CRITER parte subito senza una seconda conferma",
    "fattura_elettronica": "la fattura elettronica esce verso lo SDI",
    "invio_email": "la stampa con la casella email spuntata esce verso il cliente",
    "invio_sms": "l'SMS esce verso il cliente",
    "richiesta_feedback": "la richiesta di feedback esce verso il cliente",
    "importa_modelli": "l'importazione massiva dei modelli e irreversibile e sovrascrive i modelli esistenti",
    "salva_impostazioni": "le impostazioni valgono per tutti gli utenti, e basta entrare in un riquadro perche Unico le consideri modificate",
    "annulla_numerazione": "annullare la numerazione cancella i movimenti contabili e di magazzino collegati e lascia un buco che il programma non recupera",
    "accorpa": "l'accorpamento sostituisce la voce ovunque e poi elimina l'originale: non si torna indietro",
    "ricalcolo_preventivo": "il ricalcolo sovrascrive i prezzi senza possibilita di recuperare gli originali",
    "chiusura_esercizio": "la chiusura definitiva non e piu modificabile ne ripetibile",
    "chiusura_magazzino": "la chiusura genera i movimenti di chiusura e apertura dell'anno",
    "liquidazione_iva": "la registrazione definitiva congela i valori del periodo",
    "presentazione_effetti": "la presentazione della distinta effetti esce verso la banca: una volta partita, e partita",
    "rigenera_libretto": "il libretto di impianto esportato vive scollegato da Unico: rigenerarlo significa cancellare quello esistente e perdere tutto cio che era stato inserito solo li",
    "rinomina_voce_tabella": "rinominare una voce di tabella cambia lo storico all'indietro, tutti i record che la usavano si ritrovano il nome nuovo; la strada giusta e 'Escluso da liste' sulla vecchia piu una voce nuova",
    "elimina_documento": "Elimina documento sul documento di intervento cancella in modo definitivo e irreversibile",
    "elimina_intervento": "eliminare un intervento non si annulla",
    "elimina_insoluto": "un insoluto non e modificabile, va eliminato e reinserito, e l'eliminazione toglie una registrazione contabile",
}


@dataclass(frozen=True)
class Azione:
    """What the skill is about to do, described well enough to judge it."""

    tipo: str
    bersaglio: str
    azienda: str
    filtri_attivi: bool = False
    n_elementi: int = 1


@dataclass(frozen=True)
class Verdetto:
    """consenti = procedi; conferma = chiedi al titolare; vieta = non farlo."""

    esito: str
    motivo: str


def valuta(azione: Azione) -> Verdetto:
    """Judge an action against the red-zone rules."""
    if azione.tipo == "lettura":
        return Verdetto("consenti", "lettura: nessun effetto sui dati")

    # Prima di tutto il resto: cio che esce non si fa, nemmeno in prova.
    if azione.tipo in VERSO_ESTERNO:
        return Verdetto("vieta", MOTIVI.get(azione.tipo, "questa azione esce verso terzi"))

    if azione.tipo in SEMPRE_CONFERMA:
        return Verdetto("conferma", MOTIVI.get(azione.tipo, "azione che cambia la configurazione"))

    if azione.tipo in AUTORIZZATE_OVUNQUE:
        if azione.azienda in ("azienda3", "produzione"):
            return Verdetto("consenti", f"'{azione.tipo}' autorizzata in modo permanente dal titolare")
        return Verdetto(
            "conferma",
            "non riesco a leggere quale azienda e attiva: confermami dove sto creando",
        )

    if azione.tipo in SCRITTURE_ESPLICITE:
        if azione.azienda == "azienda3":
            return Verdetto("consenti", "autorizzata esplicitamente sull'ambiente di prova")
        return Verdetto("conferma", f"'{azione.tipo}' fuori dall'ambiente di prova: serve il tuo ok")

    if azione.tipo in IRREVERSIBILI:
        motivo = MOTIVI.get(azione.tipo, "operazione irreversibile")
        if azione.azienda == "azienda3":
            return Verdetto("conferma", f"{motivo} (sei sull'ambiente di prova)")
        if azione.azienda == "produzione":
            return Verdetto("vieta", f"{motivo}: non la eseguo in produzione")
        # Azienda sconosciuta: potrebbe essere produzione. Su un'operazione
        # irreversibile non si rischia, si tratta come il caso peggiore.
        return Verdetto(
            "vieta",
            f"{motivo}: non so su quale azienda sto operando, non rischio "
            "un'operazione irreversibile senza saperlo",
        )

    # La trappola dei filtri e meccanica di Unico, non dipende da quale
    # azienda e attiva: vince su qualsiasi altro controllo, anche
    # sull'azienda sconosciuta.
    if azione.tipo == "massiva" and azione.filtri_attivi:
        return Verdetto(
            "vieta",
            "operazione massiva con filtri attivi: Unico modifica anche le righe "
            "selezionate ma non visibili. Azzera i filtri, poi si riparte",
        )

    if azione.azienda == "sconosciuta":
        return Verdetto(
            "conferma",
            "non riesco a leggere quale azienda e attiva: confermami dove sto scrivendo",
        )

    if azione.tipo == "massiva":
        return Verdetto(
            "conferma",
            f"operazione massiva su {azione.n_elementi} elementi di {azione.bersaglio}",
        )

    if azione.tipo == "scrittura":
        if azione.azienda == "azienda3":
            return Verdetto("consenti", "scrittura sull'ambiente di prova")
        return Verdetto("conferma", "scrittura in produzione: serve il tuo ok")

    return Verdetto("conferma", f"azione '{azione.tipo}' non classificata: chiedo prima")
