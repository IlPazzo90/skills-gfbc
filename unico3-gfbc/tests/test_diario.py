"""Tests for the session journal."""
import json

from u3 import diario


def test_una_riga_per_esecuzione(tmp_path):
    diario.annota(str(tmp_path), {"ricerca": "impianti", "righe": 12}, quando="2026-09-01T10:00:00")
    diario.annota(str(tmp_path), {"ricerca": "interventi", "righe": 3}, quando="2026-09-01T11:00:00")
    righe = diario.leggi_mese(str(tmp_path), "2026-09")
    assert len(righe) == 2
    assert righe[0]["ricerca"] == "impianti"


def test_il_file_e_diviso_per_mese(tmp_path):
    diario.annota(str(tmp_path), {"ricerca": "a"}, quando="2026-09-30T23:00:00")
    diario.annota(str(tmp_path), {"ricerca": "b"}, quando="2026-10-01T01:00:00")
    assert len(diario.leggi_mese(str(tmp_path), "2026-09")) == 1
    assert len(diario.leggi_mese(str(tmp_path), "2026-10")) == 1


def test_il_timestamp_viene_registrato(tmp_path):
    diario.annota(str(tmp_path), {"ricerca": "a"}, quando="2026-09-01T10:00:00")
    riga = diario.leggi_mese(str(tmp_path), "2026-09")[0]
    assert riga["quando"] == "2026-09-01T10:00:00"


def test_un_mese_senza_righe_restituisce_lista_vuota(tmp_path):
    assert diario.leggi_mese(str(tmp_path), "2026-01") == []


def test_le_righe_corrotte_non_fanno_esplodere_la_lettura(tmp_path):
    diario.annota(str(tmp_path), {"ricerca": "a"}, quando="2026-09-01T10:00:00")
    with open(tmp_path / "2026-09.jsonl", "a", encoding="utf-8") as file_jsonl:
        file_jsonl.write("{non e' json\n")
    assert len(diario.leggi_mese(str(tmp_path), "2026-09")) == 1


def test_ricorrenti_conta_le_ricerche_piu_usate(tmp_path):
    for _ in range(3):
        diario.annota(str(tmp_path), {"ricerca": "impianti"}, quando="2026-09-01T10:00:00")
    diario.annota(str(tmp_path), {"ricerca": "interventi"}, quando="2026-09-01T10:00:00")
    assert diario.ricorrenti(str(tmp_path), "2026-09") == [("impianti", 3), ("interventi", 1)]


def test_ogni_riga_e_json_valido_su_una_riga_sola(tmp_path):
    diario.annota(str(tmp_path), {"ricerca": "a", "note": "con\nnewline"}, quando="2026-09-01T10:00:00")
    contenuto = open(tmp_path / "2026-09.jsonl", encoding="utf-8").read()
    assert contenuto.count("\n") == 1
    assert json.loads(contenuto)["note"] == "con\nnewline"
