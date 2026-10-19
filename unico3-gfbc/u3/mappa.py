"""The UI map, as data the skill can edit.

Every selector carries its history: when it was first seen, whether the owner has
confirmed a result produced with it, and how often it has worked since.

The rule that keeps this honest: a selector that has never produced a confirmed
result is a *candidate*. Candidates are usable, but the skill says so out loud,
and a candidate never displaces a confirmed selector until the owner confirms it
in turn.
"""
from __future__ import annotations

import json
import os
import tempfile
from typing import List, Optional

SOGLIA_FRAGILE = 0.2  # oltre un quinto di fallimenti, il selettore e' fragile
MINIMO_TENTATIVI = 4  # sotto questo numero non si giudica


class MappaCorrotta(Exception):
    """Raised when mappa.json exists but is not valid JSON.

    We refuse to silently start over from empty: that would throw away every
    confirmed selector without telling anyone. Better to stop loudly and let a
    human look at the file (it's plain, editable JSON) than to quietly forget
    what the skill has learned.
    """


def _carica(percorso: str) -> dict:
    if not os.path.exists(percorso):
        return {"voci": {}}
    with open(percorso, encoding="utf-8") as file_json:
        testo = file_json.read()
    try:
        dati = json.loads(testo)
    except json.JSONDecodeError as errore:
        raise MappaCorrotta(
            f"{percorso} non e' JSON valido ({errore}). "
            "Non riparto da una mappa vuota: correggi il file a mano o "
            "ripristina un backup, cosi' non si perde quello che e' gia' stato imparato."
        ) from errore
    dati.setdefault("voci", {})
    return dati


def _salva(percorso: str, dati: dict) -> None:
    cartella = os.path.dirname(percorso) or "."
    os.makedirs(cartella, exist_ok=True)
    # Write to a temp file in the same directory, then os.replace: that's an
    # atomic rename on POSIX and Windows, so a crash mid-write never leaves
    # mappa.json truncated or half-written. The temp file lives alongside the
    # target so the replace stays on the same filesystem.
    descrittore, percorso_temp = tempfile.mkstemp(
        dir=cartella, prefix=".mappa-", suffix=".tmp"
    )
    try:
        with os.fdopen(descrittore, "w", encoding="utf-8") as file_json:
            json.dump(dati, file_json, ensure_ascii=False, indent=2, sort_keys=True)
            file_json.write("\n")
            file_json.flush()
            os.fsync(file_json.fileno())
        os.replace(percorso_temp, percorso)
    except BaseException:
        if os.path.exists(percorso_temp):
            os.remove(percorso_temp)
        raise


def leggi(percorso: str, chiave: str) -> Optional[dict]:
    """The whole record for a key, or None."""
    return _carica(percorso)["voci"].get(chiave)


def selettore(percorso: str, chiave: str) -> Optional[str]:
    """The selector currently in use for a key."""
    voce = leggi(percorso, chiave)
    return voce["selettore"] if voce else None


def e_candidata(percorso: str, chiave: str) -> bool:
    """True when the selector in use has never been confirmed.

    A key that doesn't exist yet has, by definition, no confirmed history
    either — so it counts as a candidate too. Answering False for an unknown
    key would let the skill claim an unverified path is trusted just because
    it forgot to register it first; True is the safe default.
    """
    voce = leggi(percorso, chiave)
    if not voce:
        return True
    return not voce.get("confermato_dal_titolare", False)


def registra(percorso: str, chiave: str, nuovo_selettore: str, oggi: str) -> None:
    """Record a selector seen in the wild.

    A brand new key starts as a candidate. If the key already holds a *confirmed*
    selector, the new one waits in `candidato` instead of displacing it.
    """
    dati = _carica(percorso)
    voce = dati["voci"].get(chiave)

    if voce is None:
        dati["voci"][chiave] = {
            "selettore": nuovo_selettore,
            "visto_il": oggi,
            "confermato_dal_titolare": False,
            "successi": 0,
            "fallimenti": 0,
            "ultimo_esito": None,
            "candidato": None,
        }
    elif voce.get("confermato_dal_titolare"):
        if voce["selettore"] != nuovo_selettore:
            voce["candidato"] = nuovo_selettore
            voce["candidato_visto_il"] = oggi
    else:
        voce["selettore"] = nuovo_selettore
        voce["visto_il"] = oggi

    _salva(percorso, dati)


def conferma(percorso: str, chiave: str, oggi: str) -> None:
    """The owner checked a result: promote what produced it."""
    dati = _carica(percorso)
    voce = dati["voci"].get(chiave)
    if voce is None:
        return
    if voce.get("candidato"):
        voce["selettore"] = voce["candidato"]
        voce["visto_il"] = voce.get("candidato_visto_il", oggi)
        voce["candidato"] = None
        voce.pop("candidato_visto_il", None)
        voce["successi"] = 0
        voce["fallimenti"] = 0
        # The old counters belonged to the selector that just got replaced;
        # ultimo_esito would otherwise still point at a run of the old path,
        # which reads as evidence about a selector that's gone. Reset it too.
        voce["ultimo_esito"] = None
    voce["confermato_dal_titolare"] = True
    voce["confermato_il"] = oggi
    _salva(percorso, dati)


def esito(percorso: str, chiave: str, riuscito: bool, oggi: str) -> None:
    """Record whether the selector found anything this time."""
    dati = _carica(percorso)
    voce = dati["voci"].get(chiave)
    if voce is None:
        return
    voce["successi" if riuscito else "fallimenti"] += 1
    voce["ultimo_esito"] = oggi
    _salva(percorso, dati)


def fragili(percorso: str) -> List[str]:
    """Keys that fail often enough to deserve a better selector."""
    risultato = []
    for chiave, voce in _carica(percorso)["voci"].items():
        tentativi = voce.get("successi", 0) + voce.get("fallimenti", 0)
        if tentativi < MINIMO_TENTATIVI:
            continue
        if voce.get("fallimenti", 0) / tentativi > SOGLIA_FRAGILE:
            risultato.append(chiave)
    return sorted(risultato)
