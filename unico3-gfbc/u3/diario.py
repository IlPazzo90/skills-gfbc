"""One structured record per run, split by month.

Raw material for improvement: what keeps breaking, and which questions come back
often enough to deserve a search of their own.

Contains customer data. Stays on the machine, out of git.
"""
from __future__ import annotations

import json
import os
import re
from collections import Counter
from datetime import datetime
from typing import List, Optional, Tuple

# ISO-ish "YYYY-MM-DD..." — anything starting like this sorts into the right
# monthly file. We don't require a full ISO 8601 timestamp, just this prefix.
_QUANDO_VALIDO = re.compile(r"^\d{4}-\d{2}-\d{2}")


def _adesso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def annota(cartella: str, record: dict, quando: Optional[str] = None) -> None:
    """Append one record to the current month's journal.

    `quando` exists only so tests can pin the timestamp and land a record in
    a specific month's file deterministically. Callers doing real work should
    leave it out and let it default to "now" — passing your own clock here is
    only for tests.

    The journal is a side log, not the operation it's recording. A record
    that fails to serialize (e.g. it contains a `datetime` or a `set` because
    a filter object leaked in) must never abort the caller's real work: we
    fall back to a degraded record that captures what we can, instead of
    raising.
    """
    momento = quando or _adesso()
    if not _QUANDO_VALIDO.match(momento):
        raise ValueError(
            f"quando deve iniziare con AAAA-MM-GG, ricevuto: {momento!r}"
        )
    os.makedirs(cartella, exist_ok=True)
    riga = dict(record)
    riga["quando"] = momento
    try:
        testo = json.dumps(riga, ensure_ascii=False)
    except TypeError:
        riga_degradata = {
            chiave: valore
            for chiave, valore in riga.items()
            if _e_serializzabile(valore)
        }
        riga_degradata["quando"] = momento
        riga_degradata["_diario_errore"] = "record non serializzabile, campi non json rimossi"
        testo = json.dumps(riga_degradata, ensure_ascii=False)
    percorso = os.path.join(cartella, f"{momento[:7]}.jsonl")
    with open(percorso, "a", encoding="utf-8") as file_jsonl:
        file_jsonl.write(testo + "\n")


def _e_serializzabile(valore) -> bool:
    try:
        json.dumps(valore)
        return True
    except TypeError:
        return False


def leggi_mese(cartella: str, mese: str) -> List[dict]:
    """Read one month. Corrupt lines are skipped, not fatal."""
    percorso = os.path.join(cartella, f"{mese}.jsonl")
    if not os.path.exists(percorso):
        return []
    righe = []
    with open(percorso, encoding="utf-8") as file_jsonl:
        for linea in file_jsonl:
            linea = linea.strip()
            if not linea:
                continue
            try:
                righe.append(json.loads(linea))
            except json.JSONDecodeError:
                continue
    return righe


def ricorrenti(cartella: str, mese: str) -> List[Tuple[str, int]]:
    """Which searches got used, most used first."""
    conteggio = Counter(
        riga.get("ricerca") for riga in leggi_mese(cartella, mese) if riga.get("ricerca")
    )
    return sorted(conteggio.items(), key=lambda voce: (-voce[1], voce[0]))
