"""Canonical measured facts, and the check that the files still agree with them.

A number measured once lives in `references/fatti-misurati.md`. Every other file
may repeat it - readability beats indirection - but repeating it means it can go
stale. This module reads the register and tells you where a file says something
else.

Run it from the skill directory:

    python3 -m u3.fatti

Exit code 1 when something diverges, so it can gate the end of a session.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
REGISTRO = RADICE / "references" / "fatti-misurati.md"

# The register holds the canonical values by definition, and the learning
# protocol quotes examples of divergence on purpose.
ESCLUSI = {"references/fatti-misurati.md", "references/apprendimento.md"}

# Anything on this line is a deliberate, different number - not a stale copy.
ESENZIONE = "<!-- fatti:ok -->"


@dataclass(frozen=True)
class Fatto:
    chiave: str
    valore: str
    misurato_il: str
    traccia: str
    come: str


@dataclass(frozen=True)
class Divergenza:
    chiave: str
    file: str
    riga: int
    trovato: str
    atteso: str

    def __str__(self) -> str:
        return (
            f"{self.file}:{self.riga} — '{self.chiave}' vale {self.atteso}, "
            f"qui c'e scritto {self.trovato}"
        )


def _numero(testo: str) -> str:
    """1.234 e 1234 sono lo stesso numero scritto in due modi."""
    return testo.replace(".", "").replace(" ", "").strip()


def _spoglia(cella: str) -> str:
    """Toglie i backtick con cui la traccia sta scritta nel markdown."""
    return cella.strip().strip("`").strip()


def leggi_registro(testo: str) -> dict[str, Fatto]:
    """Parses the markdown table into {chiave: Fatto}."""
    registro: dict[str, Fatto] = {}
    for riga in testo.splitlines():
        riga = riga.strip()
        if not riga.startswith("|"):
            continue
        celle = [c.strip() for c in riga.strip("|").split("|")]
        if len(celle) < 4:
            continue
        chiave = _spoglia(celle[0])
        if not chiave or chiave.lower() == "chiave" or set(chiave) <= {"-", ":"}:
            continue
        registro[chiave] = Fatto(
            chiave=chiave,
            valore=_numero(_spoglia(celle[1])),
            misurato_il=_spoglia(celle[2]),
            traccia=_spoglia(celle[3]),
            come=_spoglia(celle[4]) if len(celle) > 4 else "",
        )
    return registro


def controlla(registro: dict[str, Fatto], documenti: dict[str, str]) -> list[Divergenza]:
    """Every match of a fact's `traccia` must carry that fact's value."""
    divergenze: list[Divergenza] = []
    for fatto in registro.values():
        try:
            pattern = re.compile(fatto.traccia, re.IGNORECASE)
        except re.error:
            # A broken regex in the register is a typo to fix, not a reason to
            # leave every other fact unchecked.
            continue
        if pattern.groups < 1:
            continue
        for nome, testo in sorted(documenti.items()):
            if nome in ESCLUSI:
                continue
            for n, riga in enumerate(testo.splitlines(), start=1):
                if ESENZIONE in riga:
                    continue
                for match in pattern.finditer(riga):
                    trovato = _numero(match.group(1))
                    if trovato != fatto.valore:
                        divergenze.append(
                            Divergenza(
                                chiave=fatto.chiave,
                                file=nome,
                                riga=n,
                                trovato=match.group(1),
                                atteso=fatto.valore,
                            )
                        )
    return divergenze


def registro_reale() -> dict[str, Fatto]:
    if not REGISTRO.exists():
        return {}
    return leggi_registro(REGISTRO.read_text(encoding="utf-8"))


def raccogli_documenti() -> dict[str, str]:
    """The skill's own prose: SKILL.md plus references/. Not docs/ - that is
    the vendor's guide, and correcting Futura SI is not our job."""
    documenti: dict[str, str] = {}
    for percorso in [RADICE / "SKILL.md", *sorted((RADICE / "references").rglob("*.md"))]:
        if percorso.exists():
            documenti[str(percorso.relative_to(RADICE))] = percorso.read_text(encoding="utf-8")
    return documenti


def tracce_morte(registro: dict[str, Fatto], documenti: dict[str, str]) -> list[str]:
    """Facts whose `traccia` matches nothing anywhere.

    `controlla` stays silent for these: no file contradicts the value because no
    file mentions it. The fact looks guarded and is not - so a later edit can
    quietly change the number in prose without the check ever noticing.

    The register itself does not count as a mention: its own row always carries
    the value, which would make every trace look alive.
    """
    morte: list[str] = []
    for chiave, fatto in registro.items():
        try:
            pattern = re.compile(fatto.traccia, re.IGNORECASE)
        except re.error:
            continue
        if pattern.groups < 1:
            continue
        visto = any(
            pattern.search(riga)
            for nome, testo in documenti.items()
            if nome not in ESCLUSI
            for riga in testo.splitlines()
        )
        if not visto:
            morte.append(chiave)
    return morte


def main() -> int:
    registro = registro_reale()
    if not registro:
        print(f"registro assente o vuoto: {REGISTRO}")
        return 1
    documenti = raccogli_documenti()
    divergenze = controlla(registro, documenti)
    morte = tracce_morte(registro, documenti)
    if divergenze:
        print(f"{len(divergenze)} divergenze:")
        for d in divergenze:
            print(f"  {d}")
    if morte:
        print(f"{len(morte)} fatti che nessun file nomina (traccia senza presidio):")
        for chiave in morte:
            print(f"  {chiave} - o si cita il numero dove serve, o si toglie dal registro")
    if divergenze or morte:
        return 1
    print(f"{len(registro)} fatti, nessuna divergenza, nessuna traccia morta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
