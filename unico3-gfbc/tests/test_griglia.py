"""Tests for grid clean-up."""
from u3.griglia import converti, normalizza, pulisci


def test_pulisci_toglie_spazi():
    assert pulisci("  Rossi  ") == "Rossi"


def test_pulisci_trasforma_la_stringa_vuota_in_none():
    assert pulisci("   ") is None


def test_pulisci_toglie_i_surrogati_spaiati():
    assert pulisci("Caldaia \ud83d Ferroli") == "Caldaia  Ferroli"


def test_pulisci_lascia_stare_i_non_stringa():
    assert pulisci(42) == 42
    assert pulisci(None) is None


def test_converti_data_italiana_in_iso():
    assert converti("07/09/2026") == "2026-09-07"


def test_converti_lascia_stare_le_date_di_calendario_non_valide():
    # 32/13 non e' una data: meglio lasciarla intatta che spacciarla per ISO.
    assert converti("32/13/2026") == "32/13/2026"


def test_converti_numero_italiano_con_migliaia():
    assert converti("1.234,56") == 1234.56


def test_converti_numero_italiano_senza_migliaia():
    assert converti("12,50") == 12.5


def test_converti_numero_negativo():
    assert converti("-1.000,00") == -1000.0


def test_converti_lascia_stare_i_codici_che_sembrano_numeri():
    # Un codice impianto non deve diventare un float.
    assert converti("00123") == "00123"


def test_converti_lascia_stare_il_testo():
    assert converti("Via Roma 1") == "Via Roma 1"


def test_normalizza_pulisce_chiavi_e_valori():
    grezzo = [{" Nominativo ": " Rossi Mario ", "Scadenza": "07/09/2026"}]
    assert normalizza(grezzo) == [
        {"Nominativo": "Rossi Mario", "Scadenza": "2026-09-07"}
    ]


def test_normalizza_scarta_le_righe_completamente_vuote():
    grezzo = [{"a": "", "b": "   "}, {"a": "x", "b": ""}]
    assert normalizza(grezzo) == [{"a": "x", "b": None}]


def test_normalizza_ignora_le_voci_che_non_sono_righe():
    assert normalizza(["stringa", None, {"a": "x"}]) == [{"a": "x"}]


def test_normalizza_non_scarta_le_righe_di_soli_zeri():
    # 0.0 e' falsy ma non e' un valore mancante: la riga deve restare.
    grezzo = [{"Importo": "0,00", "Saldo": "0,00"}]
    assert normalizza(grezzo) == [{"Importo": 0.0, "Saldo": 0.0}]


def test_normalizza_puo_lasciare_i_valori_grezzi():
    grezzo = [{"Scadenza": "07/09/2026"}]
    assert normalizza(grezzo, converti_valori=False) == [{"Scadenza": "07/09/2026"}]
