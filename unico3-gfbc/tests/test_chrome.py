"""Tests for the Chrome launch and target selection."""
import json
import time

import pytest

from u3.chrome import Scheda, comando_avvio, scegli_target


def test_comando_avvio_usa_profilo_dedicato_e_porta():
    argv = comando_avvio("/tmp/profilo", 9222, "https://start.dc3.unico3.cloud/")
    assert "--user-data-dir=/tmp/profilo" in argv
    assert "--remote-debugging-port=9222" in argv
    assert argv[-1] == "https://start.dc3.unico3.cloud/"


def test_comando_avvio_non_riusa_il_profilo_predefinito():
    # Condividere il profilo con Playwright azzera i cookie: mai farlo.
    argv = comando_avvio("/tmp/profilo", 9222, "https://esempio")
    assert not any(a.startswith("--user-data-dir=") and "Default" in a for a in argv)


def test_scegli_target_prende_la_pagina_giusta():
    target = [
        {"type": "background_page", "url": "chrome-extension://x", "webSocketDebuggerUrl": "ws://x"},
        {"type": "page", "url": "https://start.dc3.unico3.cloud/impianti", "webSocketDebuggerUrl": "ws://ok"},
    ]
    assert scegli_target(target, "unico3.cloud")["webSocketDebuggerUrl"] == "ws://ok"


def test_scegli_target_ignora_i_non_pagina():
    target = [{"type": "worker", "url": "https://start.dc3.unico3.cloud/w", "webSocketDebuggerUrl": "ws://no"}]
    assert scegli_target(target, "unico3.cloud") is None


def test_scegli_target_senza_corrispondenza_restituisce_none():
    target = [{"type": "page", "url": "https://google.com", "webSocketDebuggerUrl": "ws://no"}]
    assert scegli_target(target, "unico3.cloud") is None


class _WebSocketFinto:
    """Simula websocket.create_connection senza aprire alcun socket."""

    def __init__(self, messaggi):
        self._messaggi = list(messaggi)
        self.inviati = []

    def send(self, testo):
        self.inviati.append(json.loads(testo))

    def recv(self):
        return json.dumps(self._messaggi.pop(0))

    def close(self):
        pass


def _scheda_con_messaggi(messaggi, timeout=5):
    """Costruisce una Scheda collegata a un websocket finto, senza rete."""
    scheda = object.__new__(Scheda)
    scheda._id = 0
    scheda._timeout = timeout
    scheda._ws = _WebSocketFinto(messaggi)
    return scheda


class _WebSocketChiacchierone:
    """Simula una pagina che manda eventi CDP senza sosta, mai la risposta attesa."""

    def __init__(self):
        self.inviati = []

    def send(self, testo):
        self.inviati.append(json.loads(testo))

    def recv(self):
        # Sempre un evento senza "id": non arriva mai la risposta alla nostra richiesta.
        return json.dumps({"method": "Network.dataReceived", "params": {}})

    def close(self):
        pass


def test_valuta_solleva_su_eccezione_js():
    # Forma reale della risposta CDP a Runtime.evaluate quando il JS lancia:
    # {"id": N, "result": {"result": {...}, "exceptionDetails": {...}}}
    # exceptionDetails e' un fratello di "result" dentro il payload annidato,
    # non al primo livello del messaggio.
    risposta_con_eccezione = {
        "id": 1,
        "result": {
            "result": {"type": "object", "subtype": "error", "className": "Error"},
            "exceptionDetails": {
                "exceptionId": 1,
                "text": "Uncaught",
                "lineNumber": 0,
                "columnNumber": 0,
                "exception": {"type": "object", "subtype": "error", "description": "Error: boom"},
            },
        },
    }
    scheda = _scheda_con_messaggi([risposta_con_eccezione])
    with pytest.raises(RuntimeError):
        scheda.valuta("throw new Error('boom')")


def test_valuta_restituisce_il_valore_su_successo():
    risposta_ok = {"id": 1, "result": {"result": {"type": "string", "value": "ciao"}}}
    scheda = _scheda_con_messaggi([risposta_ok])
    assert scheda.valuta("'ciao'") == "ciao"


def test_invia_scarta_eventi_non_richiesti_e_prende_la_risposta_giusta():
    # Il CDP manda anche eventi senza campo "id" (es. Page.loadEventFired):
    # _invia deve scartarli e continuare finche' non arriva l'id che aspetta.
    evento_senza_id = {"method": "Page.loadEventFired", "params": {}}
    risposta_ok = {"id": 1, "result": {"result": {"type": "string", "value": "ok"}}}
    scheda = _scheda_con_messaggi([evento_senza_id, risposta_ok])
    assert scheda.valuta("'ok'") == "ok"


def test_invia_solleva_timeout_complessivo_se_la_pagina_chiacchiera_e_non_risponde():
    # Il timeout del socket e' per singola recv(): ogni evento in arrivo lo
    # resetta. Una pagina che manda eventi senza sosta ma non risponde mai al
    # nostro id deve comunque far scattare un deadline complessivo, non restare
    # appesa per sempre. Timeout volutamente cortissimo per non rallentare la suite.
    scheda = object.__new__(Scheda)
    scheda._id = 0
    scheda._timeout = 0.1
    scheda._ws = _WebSocketChiacchierone()

    inizio = time.time()
    with pytest.raises(TimeoutError):
        scheda._invia("Runtime.evaluate", {"expression": "1"})
    durata = time.time() - inizio

    assert durata < 2.0  # non deve mai avvicinarsi al timeout reale di 30s
