"""Tests for the canonical-facts consistency check.

The defect this guards against is real and happened on 03/09/2026: three
numbers ("72 tabelle", "16 entita cercabili", "la numerazione congela il
documento") survived in older files after later measurements proved them
wrong. A skill that contradicts itself is worse than an incomplete one -
whoever reads it cannot tell which half to believe.
"""
import pytest

from u3.fatti import Divergenza, Fatto, controlla, leggi_registro

REGISTRO = """
# Fatti misurati

| Chiave | Valore | Misurato il | Traccia | Come |
|---|---|---|---|---|
| impianti-x | 1234 | 03/09/2026 | `([\\d.]+) impianti` | conteggio nel modello AG Grid |
| tabelle | 68 | 03/09/2026 | `([\\d.]+) tabelle` | voci della sidebar |
"""


class TestLeggiRegistro:
    def test_legge_le_righe_della_tabella(self):
        registro = leggi_registro(REGISTRO)
        assert set(registro) == {"impianti-x", "tabelle"}

    def test_tiene_valore_data_e_traccia(self):
        f = leggi_registro(REGISTRO)["impianti-x"]
        assert f.valore == "1234"
        assert f.misurato_il == "03/09/2026"
        assert f.traccia == r"([\d.]+) impianti"

    def test_ignora_intestazione_e_separatore(self):
        # Senza questo, "Chiave" e "---" diventerebbero due fatti fantasma.
        assert "Chiave" not in leggi_registro(REGISTRO)
        assert "---" not in leggi_registro(REGISTRO)

    def test_registro_senza_tabella_e_vuoto_non_esplode(self):
        assert leggi_registro("# Niente qui\n\ntesto libero\n") == {}


class TestControlla:
    def test_valore_giusto_non_produce_nulla(self):
        registro = leggi_registro(REGISTRO)
        assert controlla(registro, {"a.md": "Ci sono 1234 impianti."}) == []

    def test_valore_diverso_e_una_divergenza(self):
        registro = leggi_registro(REGISTRO)
        div = controlla(registro, {"vecchio.md": "Le 72 tabelle di Unico."})
        assert len(div) == 1
        assert div[0].chiave == "tabelle"
        assert div[0].trovato == "72"
        assert div[0].atteso == "68"
        assert div[0].file == "vecchio.md"

    def test_dice_la_riga_esatta(self):
        registro = leggi_registro(REGISTRO)
        testo = "riga uno\nriga due\nLe 72 tabelle.\n"
        div = controlla(registro, {"x.md": testo})
        assert div[0].riga == 3

    def test_i_punti_di_migliaia_non_contano(self):
        # Unico scrive "1.234": stesso numero, altra grafia.
        registro = leggi_registro(REGISTRO)
        assert controlla(registro, {"a.md": "trovati 1.234 impianti"}) == []

    def test_marcatore_inline_esenta_la_riga(self):
        # Serve per le frasi legittime: "le 12 tabelle di magazzino".
        registro = leggi_registro(REGISTRO)
        testo = "Le 12 tabelle di magazzino. <!-- fatti:ok -->"
        assert controlla(registro, {"x.md": testo}) == []

    def test_il_registro_stesso_non_si_controlla(self):
        # Il registro contiene i valori canonici per definizione: passarlo
        # al controllo produrrebbe rumore, non informazione.
        registro = leggi_registro(REGISTRO)
        assert controlla(registro, {"references/fatti-misurati.md": REGISTRO}) == []

    def test_piu_divergenze_nello_stesso_file(self):
        registro = leggi_registro(REGISTRO)
        div = controlla(registro, {"x.md": "3000 impianti\ne 72 tabelle\n"})
        assert {d.chiave for d in div} == {"impianti-x", "tabelle"}

    def test_traccia_non_valida_non_fa_cadere_il_controllo(self):
        # Una regex scritta male nel registro e un errore di battitura, non
        # un motivo per lasciare senza controllo tutti gli altri fatti.
        registro = {
            "rotto": Fatto("rotto", "1", "oggi", "([non chiusa", "x"),
            "buono": Fatto("buono", "68", "oggi", r"([\d.]+) tabelle", "x"),
        }
        div = controlla(registro, {"x.md": "72 tabelle"})
        assert [d.chiave for d in div] == ["buono"]


class TestRegistroReale:
    """Il registro vero deve restare leggibile dal codice, non solo da me."""

    def test_il_file_esiste_e_ha_dei_fatti(self):
        from pathlib import Path

        percorso = Path(__file__).resolve().parent.parent / "references" / "fatti-misurati.md"
        assert percorso.exists(), "references/fatti-misurati.md manca"
        registro = leggi_registro(percorso.read_text(encoding="utf-8"))
        assert len(registro) >= 5, f"solo {len(registro)} fatti nel registro"

    def test_le_tracce_sono_regex_valide(self):
        import re
        from pathlib import Path

        percorso = Path(__file__).resolve().parent.parent / "references" / "fatti-misurati.md"
        for chiave, fatto in leggi_registro(percorso.read_text(encoding="utf-8")).items():
            try:
                compilata = re.compile(fatto.traccia)
            except re.error as e:  # pragma: no cover - il messaggio serve solo se fallisce
                pytest.fail(f"{chiave}: traccia non compilabile ({e})")
            assert compilata.groups >= 1, f"{chiave}: la traccia deve catturare il valore"

    def test_i_reference_non_contraddicono_il_registro(self):
        # Questo e il test che conta: gira su tutti i .md della skill.
        from u3.fatti import raccogli_documenti, registro_reale

        div = controlla(registro_reale(), raccogli_documenti())
        assert div == [], "\n".join(str(d) for d in div)


def test_divergenza_si_legge_da_sola():
    d = Divergenza(chiave="tabelle", file="x.md", riga=3, trovato="72", atteso="68")
    testo = str(d)
    assert "x.md:3" in testo and "72" in testo and "68" in testo


class TestTracceMorte:
    """Una traccia che non aggancia nessuna riga non protegge niente.

    Il controllo passava lo stesso: nessun file contraddiceva il fatto, perche'
    nessun file lo nominava. Un fatto cosi' sembra sorvegliato e non lo e'.
    """

    def test_segnala_una_traccia_che_non_compare_da_nessuna_parte(self):
        from u3.fatti import tracce_morte

        registro = leggi_registro(
            "| Chiave | Valore | Misurato il | Traccia | Come |\n"
            "|---|---|---|---|---|\n"
            "| usata | 7 | 01/01/2026 | `([\\d.]+) mele` | conta |\n"
            "| morta | 9 | 01/01/2026 | `([\\d.]+) pere` | conta |\n"
        )
        morte = tracce_morte(registro, {"references/a.md": "ci sono 7 mele sul tavolo"})
        assert morte == ["morta"]

    def test_una_traccia_agganciata_non_e_morta(self):
        from u3.fatti import tracce_morte

        registro = leggi_registro(
            "| Chiave | Valore | Misurato il | Traccia | Come |\n"
            "|---|---|---|---|---|\n"
            "| usata | 7 | 01/01/2026 | `([\\d.]+) mele` | conta |\n"
        )
        assert tracce_morte(registro, {"references/a.md": "7 mele"}) == []

    def test_il_registro_stesso_non_conta_come_aggancio(self):
        """La riga del registro contiene sempre il numero: non e' una prova."""
        from u3.fatti import tracce_morte

        registro = leggi_registro(
            "| Chiave | Valore | Misurato il | Traccia | Come |\n"
            "|---|---|---|---|---|\n"
            "| sola | 5 | 01/01/2026 | `([\\d.]+) noci` | conta |\n"
        )
        morte = tracce_morte(registro, {"references/fatti-misurati.md": "5 noci"})
        assert morte == ["sola"]

    def test_nel_registro_reale_nessun_fatto_e_senza_presidio(self):
        from u3.fatti import raccogli_documenti, registro_reale, tracce_morte

        morte = tracce_morte(registro_reale(), raccogli_documenti())
        assert morte == [], "fatti che nessun file nomina: " + ", ".join(morte)
