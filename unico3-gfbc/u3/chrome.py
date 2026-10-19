"""Drive a dedicated Chrome over the DevTools protocol.

Always a dedicated profile. Sharing the profile with Playwright races on
Default/Cookies and wipes the session the user just created.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.request
from typing import Any, List, Optional

PROFILO_PREDEFINITO = os.path.expanduser("~/.unico3-profile")
PORTA_PREDEFINITA = 9222


def comando_avvio(profilo: str, porta: int, url: str) -> List[str]:
    """Build the argv that starts a debuggable Chrome on its own profile."""
    return [
        "open",
        "-na",
        "Google Chrome",
        "--args",
        f"--user-data-dir={profilo}",
        f"--remote-debugging-port={porta}",
        "--no-first-run",
        "--no-default-browser-check",
        url,
    ]


def avvia(url: str, profilo: str = PROFILO_PREDEFINITO, porta: int = PORTA_PREDEFINITA) -> None:
    """Open Chrome on the given URL. Returns as soon as the launcher exits."""
    subprocess.run(comando_avvio(profilo, porta, url), check=True)


def elenca_target(porta: int = PORTA_PREDEFINITA) -> List[dict]:
    """Ask the browser what tabs it has open."""
    with urllib.request.urlopen(f"http://127.0.0.1:{porta}/json", timeout=5) as risposta:
        return json.load(risposta)


def scegli_target(target: List[dict], frammento_url: str) -> Optional[dict]:
    """Pick the first page tab whose URL contains the fragment."""
    for singolo in target:
        if singolo.get("type") == "page" and frammento_url in singolo.get("url", ""):
            return singolo
    return None


def attendi_target(
    frammento_url: str,
    porta: int = PORTA_PREDEFINITA,
    timeout: int = 300,
    intervallo: float = 2.0,
) -> dict:
    """Poll until a matching tab shows up. Used to wait for the user to log in."""
    scadenza = time.time() + timeout
    ultimo_errore = None
    while time.time() < scadenza:
        try:
            trovato = scegli_target(elenca_target(porta), frammento_url)
            if trovato:
                return trovato
        except OSError as errore:  # browser not up yet
            ultimo_errore = errore
        time.sleep(intervallo)
    raise TimeoutError(
        f"nessuna scheda su '{frammento_url}' entro {timeout}s (ultimo errore: {ultimo_errore})"
    )


class Scheda:
    """A CDP connection to one browser tab."""

    def __init__(self, ws_url: str, timeout: int = 30):
        import websocket  # imported here so the pure helpers stay dependency-free

        self._ws = websocket.create_connection(ws_url, timeout=timeout)
        self._id = 0
        self._timeout = timeout

    def _invia(self, metodo: str, parametri: Optional[dict] = None, timeout: Optional[float] = None) -> dict:
        # The socket-level timeout only covers a single recv(): every unrelated
        # CDP event (Page.loadEventFired, console logs, polling traffic...) resets
        # it. A chatty page can keep the loop fed forever without ever delivering
        # our id, so we also need an overall wall-clock deadline here.
        scadenza_totale = timeout if timeout is not None else self._timeout
        scadenza = time.time() + scadenza_totale
        self._id += 1
        self._ws.send(json.dumps({"id": self._id, "method": metodo, "params": parametri or {}}))
        while True:
            if time.time() > scadenza:
                raise TimeoutError(
                    f"nessuna risposta a '{metodo}' entro {scadenza_totale}s "
                    "(la pagina manda eventi ma non risponde alla nostra richiesta)"
                )
            messaggio = json.loads(self._ws.recv())
            if messaggio.get("id") == self._id:
                return messaggio

    def valuta(self, espressione: str) -> Any:
        """Run JS in the page and return the JSON-serialisable result."""
        risposta = self._invia(
            "Runtime.evaluate",
            {"expression": espressione, "returnByValue": True, "awaitPromise": True},
        )
        risultato = risposta.get("result", {})
        if "exceptionDetails" in risultato:
            testo = risultato["exceptionDetails"].get("text", "errore JS")
            raise RuntimeError(f"JS fallito: {testo}")
        return risultato.get("result", {}).get("value")

    def url(self) -> str:
        """The URL the tab is currently on."""
        return self.valuta("location.href") or ""

    def chiudi(self) -> None:
        self._ws.close()
