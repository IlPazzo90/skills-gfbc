"""Tests for the self-editing UI map."""
import json

import pytest

from u3 import mappa


@pytest.fixture
def percorso(tmp_path):
    file_mappa = tmp_path / "mappa.json"
    file_mappa.write_text(json.dumps({"voci": {}}), encoding="utf-8")
    return str(file_mappa)


def test_una_voce_nuova_nasce_candidata(percorso):
    mappa.registra(percorso, "impianti.riga", "tr.dati", oggi="2026-09-01")
    voce = mappa.leggi(percorso, "impianti.riga")
    assert voce["selettore"] == "tr.dati"
    assert voce["confermato_dal_titolare"] is False
    assert voce["visto_il"] == "2026-09-01"


def test_una_voce_candidata_si_usa_ma_si_dichiara(percorso):
    mappa.registra(percorso, "impianti.riga", "tr.dati", oggi="2026-09-01")
    assert mappa.selettore(percorso, "impianti.riga") == "tr.dati"
    assert mappa.e_candidata(percorso, "impianti.riga") is True


def test_la_conferma_promuove_la_voce(percorso):
    mappa.registra(percorso, "impianti.riga", "tr.dati", oggi="2026-09-01")
    mappa.conferma(percorso, "impianti.riga", oggi="2026-09-02")
    voce = mappa.leggi(percorso, "impianti.riga")
    assert voce["confermato_dal_titolare"] is True
    assert mappa.e_candidata(percorso, "impianti.riga") is False


def test_i_successi_e_i_fallimenti_si_contano(percorso):
    mappa.registra(percorso, "impianti.riga", "tr.dati", oggi="2026-09-01")
    mappa.esito(percorso, "impianti.riga", riuscito=True, oggi="2026-09-02")
    mappa.esito(percorso, "impianti.riga", riuscito=True, oggi="2026-09-03")
    mappa.esito(percorso, "impianti.riga", riuscito=False, oggi="2026-09-04")
    voce = mappa.leggi(percorso, "impianti.riga")
    assert voce["successi"] == 2
    assert voce["fallimenti"] == 1
    assert voce["ultimo_esito"] == "2026-09-04"


def test_un_selettore_nuovo_non_sovrascrive_quello_confermato(percorso):
    mappa.registra(percorso, "impianti.riga", "tr.vecchio", oggi="2026-09-01")
    mappa.conferma(percorso, "impianti.riga", oggi="2026-09-01")
    mappa.registra(percorso, "impianti.riga", "tr.nuovo", oggi="2026-09-05")
    voce = mappa.leggi(percorso, "impianti.riga")
    # Il confermato resta in uso; il nuovo aspetta in panchina.
    assert voce["selettore"] == "tr.vecchio"
    assert voce["candidato"] == "tr.nuovo"


def test_confermare_dopo_un_candidato_lo_fa_diventare_il_buono(percorso):
    mappa.registra(percorso, "impianti.riga", "tr.vecchio", oggi="2026-09-01")
    mappa.conferma(percorso, "impianti.riga", oggi="2026-09-01")
    mappa.registra(percorso, "impianti.riga", "tr.nuovo", oggi="2026-09-05")
    mappa.conferma(percorso, "impianti.riga", oggi="2026-09-06")
    voce = mappa.leggi(percorso, "impianti.riga")
    assert voce["selettore"] == "tr.nuovo"
    assert voce.get("candidato") is None


def test_chiave_assente_restituisce_none(percorso):
    assert mappa.leggi(percorso, "non.esiste") is None
    assert mappa.selettore(percorso, "non.esiste") is None


def test_fragili_sono_quelli_che_falliscono_troppo(percorso):
    mappa.registra(percorso, "solida", "a", oggi="2026-09-01")
    mappa.registra(percorso, "fragile", "b", oggi="2026-09-01")
    for _ in range(9):
        mappa.esito(percorso, "solida", riuscito=True, oggi="2026-09-02")
    mappa.esito(percorso, "solida", riuscito=False, oggi="2026-09-02")
    for _ in range(3):
        mappa.esito(percorso, "fragile", riuscito=True, oggi="2026-09-02")
    for _ in range(3):
        mappa.esito(percorso, "fragile", riuscito=False, oggi="2026-09-02")
    assert mappa.fragili(percorso) == ["fragile"]


def test_il_file_resta_leggibile_a_mano(percorso):
    mappa.registra(percorso, "impianti.riga", "tr.dati", oggi="2026-09-01")
    testo = open(percorso, encoding="utf-8").read()
    assert "\n" in testo  # indentato, non una riga sola
    assert json.loads(testo)["voci"]["impianti.riga"]["selettore"] == "tr.dati"


def test_una_scrittura_interrotta_non_corrompe_la_mappa(percorso, monkeypatch):
    mappa.registra(percorso, "impianti.riga", "tr.dati", oggi="2026-09-01")

    def dump_che_crasha(*_args, **_kwargs):
        raise OSError("crash simulato durante la scrittura")

    monkeypatch.setattr(json, "dump", dump_che_crasha)
    with pytest.raises(OSError):
        mappa.registra(percorso, "impianti.riga", "tr.rotto", oggi="2026-09-10")
    monkeypatch.undo()

    # Il file resta quello di prima, non troncato ne' a meta'.
    voce = mappa.leggi(percorso, "impianti.riga")
    assert voce["selettore"] == "tr.dati"

    cartella = str((__import__("pathlib").Path(percorso)).parent)
    residui = [n for n in __import__("os").listdir(cartella) if n.startswith(".mappa-")]
    assert residui == []


def test_mappa_corrotta_si_dichiara_invece_di_ripartire_da_vuoto(percorso):
    with open(percorso, "w", encoding="utf-8") as file_json:
        file_json.write("{questo non e' json valido")
    with pytest.raises(mappa.MappaCorrotta):
        mappa.leggi(percorso, "impianti.riga")


def test_la_promozione_non_lascia_lesito_del_vecchio_selettore(percorso):
    mappa.registra(percorso, "impianti.riga", "tr.vecchio", oggi="2026-09-01")
    mappa.conferma(percorso, "impianti.riga", oggi="2026-09-01")
    mappa.esito(percorso, "impianti.riga", riuscito=False, oggi="2026-09-03")

    mappa.registra(percorso, "impianti.riga", "tr.nuovo", oggi="2026-09-05")
    mappa.conferma(percorso, "impianti.riga", oggi="2026-09-06")

    voce = mappa.leggi(percorso, "impianti.riga")
    # L'esito del 2026-09-03 riguardava tr.vecchio: non deve sembrare
    # un esito di tr.nuovo, che non e' mai stato ancora provato.
    assert voce["ultimo_esito"] is None


def test_e_candidata_su_chiave_assente_e_prudente(percorso):
    # Nessuna storia confermata per una chiave mai vista: non e' sicuro
    # dichiararla "non candidata", altrimenti la skill userebbe un percorso
    # inesistente spacciandolo per verificato.
    assert mappa.e_candidata(percorso, "non.esiste") is True
