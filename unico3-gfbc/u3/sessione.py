"""Where are we: past the login, and on which company.

The company map is deliberately small and overridable. Anything not recognised
comes back as "sconosciuta", which makes the guardrail ask instead of guess.
"""
from __future__ import annotations

import os
import re
from typing import Iterable, Optional
from urllib.parse import parse_qs, urlparse

HOST_LOGIN = "login.dc3.unico3.cloud"

# Empty on purpose: a label like "Azienda 3" says nothing about being a sandbox.
# Being a sandbox is declared in UNICO3_SANDBOX, see below.
AZIENDE_NOTE: dict = {}

# The app carries the active company in the query string, e.g.
#   https://app.dc3.unico3.cloud/?c=/C1234/A3/#/analytics
# Observed 02/09/2026. Two tabs on two companies at once is a consequence of
# this, and so is the fact that reading the company off the page text is
# hopeless: the company menu lists every company at once.
# The parameter must be exactly /C<tenant>/A<company>/, not a string that
# happens to contain one: without the anchors, any text with "/A3/" inside it
# would be classified as the environment where writes need no confirmation.
#
# The tenant is part of the identity and is not thrown away. "A3" on its own
# does not name a company: it names the third company of *some* installation.
# A declared sandbox is one installation's company 3, not anybody's company 3.
SCHEMA_AZIENDA = re.compile(r"^/(C\d+)/(A\d+)/$")

# And it has to come from Unico. The comparison is against the whole domain,
# not "ends with": "unico3.cloud.example.com" is not Unico.
DOMINIO = "unico3.cloud"

# Which companies are safe to write to without asking. Empty by default.
#
# Being a sandbox is a DECISION, not something the URL or the data can tell
# us. A company that looks dormant may still hold real invoicing: numbering a
# test document there writes into a real fiscal register, and undoing a
# numbering is the first entry of the red zone. Only the owner of the
# installation declares a sandbox, in UNICO3_SANDBOX, tenant-qualified and
# comma-separated, e.g. UNICO3_SANDBOX="C1234/A3,C1234/A2".
# Tenant-qualified: another installation's A3 is somebody else's company.
# Note what this does NOT unlock: everything in guardrail.IRREVERSIBILI still
# returns "conferma" on a sandbox, so numbering a document, merging entries,
# recalculating a quote or closing a period still stops and asks. Ordinary
# writes are what become free there, not the destructive ones.
def _sandbox_da_ambiente() -> frozenset:
    voci = (v.strip() for v in os.environ.get("UNICO3_SANDBOX", "").split(","))
    return frozenset(v for v in voci if SCHEMA_AZIENDA.match("/" + v + "/"))


SANDBOX_DICHIARATE: frozenset = _sandbox_da_ambiente()


def login_effettuato(url: str) -> bool:
    """True when the tab has got past the login redirect."""
    if not url:
        return False
    return HOST_LOGIN not in url


def azienda_da_url(url: Optional[str]) -> str:
    """Read the active company out of the URL. This is the reliable one.

    Returns a tenant-qualified id — "C1234/A1", "C1234/A3", ... — or
    "sconosciuta". Prefer this over azienda_da_testo everywhere: the URL names
    exactly one company, the page text names all of them.

    A URL that is not Unico's returns "sconosciuta". This is not paranoia
    about hostile input: "sconosciuta" is what makes the guardrail ask, and
    "A3" is what makes it stop asking. A stray string shaped like a company
    parameter must not be able to buy the quiet answer.
    """
    if not url:
        return "sconosciuta"
    pezzi = urlparse(url)
    ospite = (pezzi.hostname or "").lower()
    if ospite != DOMINIO and not ospite.endswith("." + DOMINIO):
        return "sconosciuta"
    trovate = set()
    for valore in parse_qs(pezzi.query).get("c", []):
        trovato = SCHEMA_AZIENDA.match(valore)
        if trovato:
            trovate.add("{}/{}".format(trovato.group(1), trovato.group(2)))
    # A URL naming two different companies names none of them. Taking the first
    # would let the order of the parameters decide, and the order knows nothing
    # about which company is actually active.
    if len(trovate) != 1:
        return "sconosciuta"
    return trovate.pop()


def classifica(azienda: Optional[str], sandbox: Optional[Iterable[str]] = None) -> str:
    """Turn a company id into the risk class guardrail.valuta() understands.

    Anything not explicitly declared a sandbox is production. Being wrong in
    that direction costs an extra confirmation; being wrong the other way
    costs a document numbered in a real fiscal register.
    """
    dichiarate = SANDBOX_DICHIARATE if sandbox is None else frozenset(sandbox)
    if "sconosciuta" in dichiarate:
        raise ValueError(
            "'sconosciuta' non puo' essere dichiarata sandbox: e' il valore che "
            "fa scattare il ramo prudente, dichiararla lo disattiverebbe"
        )
    if not azienda or azienda == "sconosciuta":
        return "sconosciuta"
    return "azienda3" if azienda in dichiarate else "produzione"


def azienda_da_testo(testo: Optional[str], aziende: Optional[dict] = None) -> str:
    """Map the company label shown in the UI to a stable identifier.

    DEPRECATED in favour of azienda_da_url(): the URL carries the active
    company unambiguously, the page text does not. Kept only as a last-resort
    cross-check on a screen whose URL is unavailable.

    IMPORTANT: this assumes `testo` contains ONLY the active-company label,
    not a dump of the page. Passing the full innerText is wrong by
    construction: if a menu lists the other companies alongside the active
    one, that listing triggers a false positive (e.g. a dropdown showing
    "Azienda 3" as an option while you're actually on produzione gets read
    as if you were on azienda3). The right selector — one that isolates just
    the active-company label — still needs to be found during ricognizione.
    """
    if not testo:
        return "sconosciuta"
    tabella = AZIENDE_NOTE if aziende is None else aziende
    for frammento, identificativo in tabella.items():
        pattern = r"\b" + re.escape(frammento) + r"\b"
        if re.search(pattern, testo, re.IGNORECASE):
            return identificativo
    return "sconosciuta"
