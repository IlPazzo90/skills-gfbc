"""Tests for login and company detection."""
import pytest

from u3.sessione import (
    azienda_da_testo,
    azienda_da_url,
    classifica,
    login_effettuato,
)


def test_url_di_login_significa_non_ancora_dentro():
    url = "https://login.dc3.unico3.cloud/auth/login?r=https%3A%2F%2Fstart.dc3.unico3.cloud"
    assert login_effettuato(url) is False


def test_url_dell_applicazione_significa_dentro():
    assert login_effettuato("https://start.dc3.unico3.cloud/") is True


def test_url_vuoto_non_conta_come_login():
    assert login_effettuato("") is False


MAPPA_PROVA = {"azienda 3": "azienda3"}


def test_di_default_un_etichetta_non_rende_sandbox():
    # "Azienda 3" in the page text must not unlock writes: sandboxes are declared
    # in UNICO3_SANDBOX, never inferred from a label.
    assert azienda_da_testo("Utente 1 - Azienda 3") == "sconosciuta"


def test_riconosce_azienda_3_con_mappa_esplicita():
    assert azienda_da_testo("Utente 1 - Azienda 3", MAPPA_PROVA) == "azienda3"


def test_riconoscimento_azienda_ignora_maiuscole():
    assert azienda_da_testo("AZIENDA 3", MAPPA_PROVA) == "azienda3"


def test_azienda_non_riconosciuta_resta_sconosciuta():
    # Meglio dichiararsi ignoranti che indovinare: il guardrail chiedera conferma.
    assert azienda_da_testo("Rossi Impianti Srl") == "sconosciuta"


def test_testo_vuoto_resta_sconosciuto():
    assert azienda_da_testo("") == "sconosciuta"
    assert azienda_da_testo(None) == "sconosciuta"


def test_mappa_aziende_personalizzabile():
    mappa = {"rossi impianti": "produzione", "azienda 3": "azienda3"}
    assert azienda_da_testo("Rossi Impianti Srl", mappa) == "produzione"


def test_azienda_30_non_matcha_azienda_3():
    # "azienda 3" non deve matchare dentro "azienda 30": serve un confine di parola.
    assert azienda_da_testo("Azienda 30", MAPPA_PROVA) == "sconosciuta"


def test_azienda_3bis_non_matcha_azienda_3():
    assert azienda_da_testo("Azienda 3bis") == "sconosciuta"


# --- The company is read from the URL. It is the one source that does not lie. ---


def test_azienda_dalla_url_dell_applicazione():
    url = "https://app.dc3.unico3.cloud/?c=/C1234/A3/#/analytics"
    assert azienda_da_url(url) == "C1234/A3"


def test_azienda_dalla_url_con_altro_numero():
    assert azienda_da_url("https://app.dc3.unico3.cloud/?c=/C1234/A1/#/home") == "C1234/A1"


def test_azienda_dalla_url_a_due_cifre():
    # "A1" must not match inside "A12": the whole number is read.
    assert azienda_da_url("https://app.dc3.unico3.cloud/?c=/C1234/A12/#/") == "C1234/A12"


def test_il_tenant_fa_parte_dell_identita():
    # Another installation's third company is not our company 3.
    assert azienda_da_url("https://app.dc3.unico3.cloud/?c=/C999/A3/") == "C999/A3"


def test_url_senza_parametro_azienda_resta_sconosciuta():
    assert azienda_da_url("https://start.dc3.unico3.cloud/") == "sconosciuta"


def test_url_di_login_resta_sconosciuta():
    url = "https://login.dc3.unico3.cloud/auth/login?r=https%3A%2F%2Fstart.dc3.unico3.cloud"
    assert azienda_da_url(url) == "sconosciuta"


def test_url_vuota_resta_sconosciuta():
    assert azienda_da_url("") == "sconosciuta"
    assert azienda_da_url(None) == "sconosciuta"


def test_parametro_c_malformato_resta_sconosciuta():
    assert azienda_da_url("https://app.dc3.unico3.cloud/?c=/C1234/") == "sconosciuta"


# --- A URL that is not Unico's cannot classify the company. ---


def test_host_estraneo_resta_sconosciuta():
    # Otherwise anything producing a string with /A3/ inside it unlocks the
    # free writes of the learning environment.
    assert azienda_da_url("https://evil.example/?c=/C1234/A3/") == "sconosciuta"


def test_host_che_finisce_per_caso_con_il_dominio_resta_sconosciuta():
    assert azienda_da_url("https://unico3.cloud.evil.example/?c=/C1234/A3/") == "sconosciuta"


def test_stringa_che_non_e_una_url_resta_sconosciuta():
    assert azienda_da_url("not even a url?c=/C1234/A3/") == "sconosciuta"


def test_parametro_c_senza_il_segmento_del_tenant_resta_sconosciuta():
    assert azienda_da_url("https://app.dc3.unico3.cloud/?c=/WRONG/A3/") == "sconosciuta"


def test_coda_dopo_l_azienda_resta_sconosciuta():
    # The parameter must be exactly /C<n>/A<n>/, not "something containing it".
    assert azienda_da_url("https://app.dc3.unico3.cloud/?c=/C1234/A3/altro/") == "sconosciuta"


def test_due_aziende_discordanti_nella_stessa_url_restano_sconosciute():
    # Taking the first would let the parameter order decide, and the more
    # permissive of the two would win half the time.
    url = "https://app.dc3.unico3.cloud/?c=/C1234/A3/&c=/C1234/A1/"
    assert azienda_da_url(url) == "sconosciuta"
    assert azienda_da_url(url.replace("A3/&c=/C1234/A1", "A1/&c=/C1234/A3")) == "sconosciuta"


def test_la_stessa_azienda_ripetuta_non_e_ambigua():
    url = "https://app.dc3.unico3.cloud/?c=/C1234/A3/&c=/C1234/A3/"
    assert azienda_da_url(url) == "C1234/A3"


def test_sottodominio_di_unico3_va_bene():
    assert azienda_da_url("https://app.dc3.unico3.cloud/?c=/C1234/A3/#/home") == "C1234/A3"
    assert azienda_da_url("https://start.dc3.unico3.cloud/?c=/C999/A2/") == "C999/A2"


# --- Being a test environment is a decision, not something you can deduce. ---


def test_senza_sandbox_dichiarate_ogni_azienda_e_produzione():
    # The default must be expensive in the right direction: with no sandbox
    # declared, even company 3 is production.
    assert classifica("C1234/A3", sandbox=set()) == "produzione"
    assert classifica("C1234/A1", sandbox=set()) == "produzione"


def test_senza_variabile_nessuna_sandbox(monkeypatch):
    # Out of the box nothing is a sandbox: the owner declares one.
    monkeypatch.delenv("UNICO3_SANDBOX", raising=False)
    import importlib
    import u3.sessione as s
    importlib.reload(s)
    assert s.SANDBOX_DICHIARATE == frozenset()
    assert s.classifica("C1234/A3") == "produzione"


def test_sandbox_dalla_variabile_d_ambiente(monkeypatch):
    monkeypatch.setenv("UNICO3_SANDBOX", "C1234/A3, C1234/A2, robaccia")
    import importlib
    import u3.sessione as s
    importlib.reload(s)
    try:
        assert s.SANDBOX_DICHIARATE == frozenset({"C1234/A3", "C1234/A2"})
        assert s.classifica("C1234/A2") == "azienda3"
        assert s.classifica("C1234/A1") == "produzione"
        assert s.classifica("C999/A2") == "produzione"
    finally:
        monkeypatch.delenv("UNICO3_SANDBOX")
        importlib.reload(s)


def test_l_azienda_3_di_un_altro_tenant_non_e_la_sandbox():
    # "A3" alone names no company: it names somebody's third company.
    assert classifica("C999/A3") == "produzione"


def test_una_sandbox_dichiarata_esplicitamente_viene_riconosciuta():
    assert classifica("C1/A9", sandbox={"C1/A9"}) == "azienda3"


def test_azienda_non_dichiarata_resta_produzione_anche_con_una_sandbox_nota():
    assert classifica("C1234/A3", sandbox={"C1/A9"}) == "produzione"


def test_azienda_sconosciuta_resta_sconosciuta():
    assert classifica("sconosciuta") == "sconosciuta"
    assert classifica("") == "sconosciuta"
    assert classifica(None) == "sconosciuta"


def test_sandbox_non_puo_contenere_sconosciuta():
    # Declaring "sconosciuta" a sandbox would bypass the cautious branch.
    with pytest.raises(ValueError):
        classifica("sconosciuta", sandbox={"sconosciuta"})
