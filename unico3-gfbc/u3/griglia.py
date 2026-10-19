"""Turn a raw grid dump from the page into rows that are safe to answer with.

Unico shows dates as gg/mm/aaaa and numbers as 1.234,56. Page text can also
carry lone Unicode surrogates, which raise UnicodeEncodeError on print.
"""
from __future__ import annotations

import datetime
import re
from typing import Any, List, Optional

_SURROGATI = re.compile(r"[\ud800-\udfff]")
_DATA_IT = re.compile(r"^(\d{2})/(\d{2})/(\d{4})$")
# Italian decimal: needs a comma. Bare digit runs stay strings, so codes like
# "00123" are not turned into numbers.
_NUMERO_IT = re.compile(r"^-?(?:\d{1,3}(?:\.\d{3})+|\d+),\d+$")


def pulisci(valore: Any) -> Any:
    """Trim, drop lone surrogates, turn an empty string into None."""
    if not isinstance(valore, str):
        return valore
    ripulito = _SURROGATI.sub("", valore).strip()
    return ripulito or None


def converti(valore: Any) -> Any:
    """Turn Italian dates into ISO and Italian decimals into floats."""
    if not isinstance(valore, str):
        return valore
    data = _DATA_IT.match(valore)
    if data:
        giorno, mese, anno = data.groups()
        try:
            # Reject calendar-invalid dates (e.g. 32/13/2026) instead of
            # silently emitting a bogus ISO-looking string.
            datetime.date(int(anno), int(mese), int(giorno))
        except ValueError:
            return valore
        return f"{anno}-{mese}-{giorno}"
    if _NUMERO_IT.match(valore):
        return float(valore.replace(".", "").replace(",", "."))
    return valore


def normalizza(righe: List[Any], converti_valori: bool = True) -> List[dict]:
    """Clean a raw grid dump, dropping rows that carry no data at all."""
    risultato = []
    for riga in righe:
        if not isinstance(riga, dict):
            continue
        pulita = {}
        for chiave, valore in riga.items():
            nuovo = pulisci(valore)
            if converti_valori:
                nuovo = converti(nuovo)
            pulita[pulisci(chiave) or chiave] = nuovo
        if any(valore is not None for valore in pulita.values()):
            risultato.append(pulita)
    return risultato
