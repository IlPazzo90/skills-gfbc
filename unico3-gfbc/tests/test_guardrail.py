"""Tests for the red-zone rules."""
import pytest

from u3.guardrail import Azione, valuta


def azione(**kwargs):
    base = dict(tipo="lettura", bersaglio="impianto", azienda="azienda3")
    base.update(kwargs)
    return Azione(**base)


def test_lettura_sempre_consentita_anche_in_produzione():
    v = valuta(azione(tipo="lettura", azienda="produzione"))
    assert v.esito == "consenti"


def test_scrittura_libera_su_azienda_di_prova():
    v = valuta(azione(tipo="scrittura", azienda="azienda3"))
    assert v.esito == "consenti"


def test_scrittura_in_produzione_chiede_conferma():
    v = valuta(azione(tipo="scrittura", azienda="produzione"))
    assert v.esito == "conferma"
    assert "produzione" in v.motivo


def test_azienda_sconosciuta_blocca_la_scrittura():
    v = valuta(azione(tipo="scrittura", azienda="sconosciuta"))
    assert v.esito == "conferma"
    assert "azienda" in v.motivo


def test_azienda_sconosciuta_non_blocca_la_lettura():
    v = valuta(azione(tipo="lettura", azienda="sconosciuta"))
    assert v.esito == "consenti"


@pytest.mark.parametrize(
    "tipo",
    [
        "annulla_numerazione",
        "accorpa",
        "ricalcolo_preventivo",
        "chiusura_esercizio",
        "chiusura_magazzino",
        "liquidazione_iva",
        "invio_telematico",
        "fattura_elettronica",
                "rigenera_libretto",
        "rinomina_voce_tabella",
        "elimina_insoluto",
    ],
)
def test_operazioni_irreversibili_vietate_in_produzione(tipo):
    v = valuta(azione(tipo=tipo, azienda="produzione"))
    assert v.esito == "vieta"


@pytest.mark.parametrize(
    "tipo",
    [
        "annulla_numerazione",
        "accorpa",
        # presentazione_effetti e' passata a VERSO_ESTERNO il 04/09/2026:
        # esce verso la banca, quindi ora e' "vieta", non "conferma".
        "rigenera_libretto",
        "rinomina_voce_tabella",
        "elimina_insoluto",
    ],
)
def test_operazioni_irreversibili_solo_su_conferma_in_prova(tipo):
    v = valuta(azione(tipo=tipo, azienda="azienda3"))
    assert v.esito == "conferma"


def test_operazione_irreversibile_su_azienda_sconosciuta_e_vietata():
    # Azienda sconosciuta potrebbe essere produzione: su un'operazione
    # irreversibile non basta chiedere conferma, va bloccata come in
    # produzione (caso peggiore).
    v = valuta(azione(tipo="accorpa", azienda="sconosciuta"))
    assert v.esito == "vieta"


def test_massiva_con_filtri_attivi_sempre_vietata():
    v = valuta(azione(tipo="massiva", azienda="azienda3", filtri_attivi=True))
    assert v.esito == "vieta"
    assert "filtr" in v.motivo


def test_massiva_senza_filtri_chiede_conferma_e_dice_quanti():
    v = valuta(azione(tipo="massiva", azienda="azienda3", n_elementi=27))
    assert v.esito == "conferma"
    assert "27" in v.motivo


def test_massiva_con_filtri_attivi_vietata_anche_con_azienda_sconosciuta():
    # La trappola dei filtri e meccanica di Unico, non dipende da quale
    # azienda e attiva: deve vincere anche quando non sappiamo su quale
    # azienda stiamo operando.
    v = valuta(azione(tipo="massiva", azienda="sconosciuta", filtri_attivi=True))
    assert v.esito == "vieta"
    assert "filtr" in v.motivo


def test_tipo_sconosciuto_non_passa_di_default():
    v = valuta(azione(tipo="qualcosa_di_nuovo", azienda="azienda3"))
    assert v.esito == "conferma"


def test_ogni_operazione_irreversibile_ha_il_suo_motivo():
    # Senza questo, aggiungere una voce a IRREVERSIBILI e scordare il motivo
    # fa scattare il fallback generico: la skill vieta ma non sa spiegare perche.
    # Esteso il 04/09/2026: MOTIVI ora copre anche le azioni che escono verso
    # terzi e quelle che chiedono sempre conferma. La garanzia non cambia -
    # niente verdetto senza una spiegazione - ma vale su tutte le categorie.
    from u3.guardrail import IRREVERSIBILI, MOTIVI, SEMPRE_CONFERMA, VERSO_ESTERNO

    classificate = IRREVERSIBILI | VERSO_ESTERNO | SEMPRE_CONFERMA
    assert classificate == set(MOTIVI), (
        f"senza motivo: {classificate - set(MOTIVI)}; "
        f"motivo orfano: {set(MOTIVI) - classificate}"
    )


class TestVersoEsterno:
    """Owner's rule: "l'unica cosa che non puoi fare e inviarli al
    cliente o ai catasti". That is a refusal, not a confirmation prompt: on a
    training environment everything else is allowed, so a "conferma" here would
    be one distracted yes away from mail reaching a real customer.
    """

    @pytest.mark.parametrize(
        "tipo",
        [
            "invio_telematico",
            "fattura_elettronica",
            "presentazione_effetti",
            "invio_email",
            "invio_sms",
            "richiesta_feedback",
        ],
    )
    @pytest.mark.parametrize("azienda", ["azienda3", "produzione", "sconosciuta"])
    def test_vietato_ovunque(self, tipo, azienda):
        verdetto = valuta(Azione(tipo=tipo, bersaglio="x", azienda=azienda))
        assert verdetto.esito == "vieta"

    def test_il_motivo_dice_che_esce(self):
        verdetto = valuta(Azione(tipo="invio_email", bersaglio="stampa", azienda="azienda3"))
        assert "esce" in verdetto.motivo


class TestAzioniImparateSulCampo:
    """Actions met while training on A3 that the rules did not name yet."""

    def test_numerare_e_scrittura_consentita_su_a3(self):
        # Authorised explicitly: "puoi emettere documenti, numerarli".
        verdetto = valuta(Azione(tipo="numerazione", bersaglio="rapportino", azienda="azienda3"))
        assert verdetto.esito == "consenti"

    def test_numerare_in_produzione_chiede(self):
        verdetto = valuta(Azione(tipo="numerazione", bersaglio="rapportino", azienda="produzione"))
        assert verdetto.esito == "conferma"

    def test_salvare_impostazioni_chiede_sempre(self):
        # Settings apply to every user, and merely clicking inside a box raises
        # "unsaved settings" - so this must never be automatic.
        for azienda in ("azienda3", "produzione"):
            verdetto = valuta(Azione(tipo="salva_impostazioni", bersaglio="agenda", azienda=azienda))
            assert verdetto.esito == "conferma"

    def test_importazione_massiva_modelli_e_irreversibile(self):
        verdetto = valuta(Azione(tipo="importa_modelli", bersaglio="gruppi termici", azienda="azienda3"))
        assert verdetto.esito == "conferma"
        assert "irrevers" in verdetto.motivo.lower()


class TestCreaArticolo:
    """Standing permission to create articles, when the owner grants it."""

    @pytest.mark.parametrize("azienda", ["azienda3", "produzione"])
    def test_creare_articolo_consentito(self, azienda, monkeypatch):
        import u3.guardrail as g
        monkeypatch.setattr(g, "AUTORIZZATE_OVUNQUE", frozenset({"crea_articolo"}))
        verdetto = g.valuta(Azione(tipo="crea_articolo", bersaglio="articolo", azienda=azienda))
        assert verdetto.esito == "consenti"

    def test_senza_autorizzazione_creare_in_produzione_chiede(self, monkeypatch):
        import u3.guardrail as g
        monkeypatch.setattr(g, "AUTORIZZATE_OVUNQUE", frozenset())
        verdetto = g.valuta(Azione(tipo="crea_articolo", bersaglio="articolo", azienda="produzione"))
        assert verdetto.esito == "conferma"

    def test_creare_articolo_su_azienda_sconosciuta_chiede(self):
        verdetto = valuta(Azione(tipo="crea_articolo", bersaglio="articolo", azienda="sconosciuta"))
        assert verdetto.esito == "conferma"

    def test_modificare_articolo_esistente_in_produzione_chiede_ancora(self):
        # The permission covers creation only, not edits to existing articles.
        verdetto = valuta(Azione(tipo="scrittura", bersaglio="articolo", azienda="produzione"))
        assert verdetto.esito == "conferma"


def test_eliminazioni_irreversibili_vietate_in_produzione():
    for tipo in ("elimina_documento", "elimina_intervento"):
        assert valuta(Azione(tipo, "record", "produzione")).esito == "vieta"
